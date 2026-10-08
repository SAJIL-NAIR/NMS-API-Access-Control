#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${1:-}" == "kong" && "${2:-}" == "docker-start" ]]; then
    realm="${KEYCLOAK_REALM:-nms-realm}"
    keycloak_url="${KEYCLOAK_INTERNAL_URL:-http://keycloak:8080}"
    jwks_url="${keycloak_url%/}/realms/${realm}/protocol/openid-connect/certs"
    template="${KONG_DECLARATIVE_CONFIG_TEMPLATE:-/kong/config/kong.yml}"
    output="${KONG_DECLARATIVE_CONFIG:-/tmp/kong.yml}"
    workdir="$(mktemp -d)"
    trap 'rm -rf "$workdir"' EXIT

    for attempt in {1..60}; do
        if curl --fail --silent "$jwks_url" --output "$workdir/jwks.json"; then
            break
        fi
        if [[ "$attempt" -eq 60 ]]; then
            echo "Unable to retrieve Keycloak signing keys from ${jwks_url}" >&2
            exit 1
        fi
        sleep 2
    done

    key_count="$(jq '[.keys[] | select(.use == "sig" and .alg == "RS256" and (.x5c | length > 0))] | length' "$workdir/jwks.json")"
    if [[ "$key_count" != "1" ]]; then
        echo "Expected exactly one published RS256 signing key from Keycloak; found ${key_count}" >&2
        exit 1
    fi

    jq -r '.keys[] | select(.use == "sig" and .alg == "RS256") | .x5c[0]' "$workdir/jwks.json" \
        | base64 --decode > "$workdir/signing-cert.der"
    openssl x509 -inform DER -in "$workdir/signing-cert.der" -pubkey -noout > "$workdir/signing-key.pem"

    awk -v key_file="$workdir/signing-key.pem" '
        /__KEYCLOAK_RSA_PUBLIC_KEY__/ {
            while ((getline key_line < key_file) > 0) {
                print "          " key_line
            }
            close(key_file)
            found = 1
            next
        }
        { print }
        END {
            if (!found) {
                print "Keycloak public-key placeholder is missing from the Kong configuration" > "/dev/stderr"
                exit 1
            }
        }
    ' "$template" > "$output"

    export KONG_DECLARATIVE_CONFIG="$output"
fi

exec /docker-entrypoint.sh "$@"
