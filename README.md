# NMS API Access Control

A secure and containerized access-control layer for Network Management System (NMS) Northbound APIs using Kong API Gateway, Keycloak, JWT authentication, and rate limiting.

---

## Overview

Network Management Systems (NMS) expose Northbound APIs (NBIs) that allow external applications, services, and clients to retrieve and manage network-related information.

Directly exposing these APIs can increase the attack surface and make it difficult to centrally control authentication, authorization, traffic management, and access policies.

**NMS API Access Control** demonstrates an architecture where an API Gateway is placed between external clients and the NMS Northbound API.

The gateway acts as a centralized security and traffic-control layer:

```text
                         External Client
                               |
                               v
                    +----------------------+
                    |       Keycloak       |
                    | Authentication & JWT |
                    +----------+-----------+
                               |
                         Access Token
                               |
                               v
                    +----------------------+
                    |        Kong          |
                    |     API Gateway      |
                    |                      |
                    |  JWT Validation      |
                    |  Rate Limiting       |
                    |  Request Routing     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |       Mock NMS       |
                    |      FastAPI API      |
                    |                      |
                    |   Northbound API     |
                    +----------------------+
