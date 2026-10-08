FROM kong:3.9.3

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl jq \
    && rm -rf /var/lib/apt/lists/*

COPY keycloak-entrypoint.sh /usr/local/bin/keycloak-entrypoint
RUN chmod 0755 /usr/local/bin/keycloak-entrypoint

USER kong
ENTRYPOINT ["/usr/local/bin/keycloak-entrypoint"]
CMD ["kong", "docker-start"]
