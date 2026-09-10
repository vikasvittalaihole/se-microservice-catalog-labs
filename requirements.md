# Requirements Table — Internal Microservice Catalog & Health Portal

## Functional Requirements

| ID | Description | Priority | Acceptance Criteria | Rationale |
|----|--------------|----------|----------------------|-----------|
| FR-001 | The system shall ping microservice health endpoints at 30-second intervals and compute rolling 24-hour service availability percentages. | High | Pass: Downtime recorded and alert dispatched on 3 consecutive failed health probes. Fail: Unreachable service marked healthy. | Real-time visibility into service health is the core value proposition of the portal. |
| FR-002 | The system shall automatically discover and register microservices by scanning a configured service registry or Kubernetes namespace. | High | Pass: A newly deployed service appears in the catalog within 5 minutes without manual entry. Fail: Service remains unlisted after deployment. | Manual registration doesn't scale past a handful of services and leads to stale catalogs. |
| FR-003 | The system shall aggregate and display OpenAPI/Swagger documentation for each registered microservice in a unified UI. | Medium | Pass: Selecting a service shows its current API spec with endpoint list and schemas. Fail: Docs are missing, outdated, or require navigating to the source repo. | Centralized docs reduce onboarding time and cross-team friction for API consumers. |
| FR-004 | The system shall render an interactive dependency graph showing which services call which other services. | High | Pass: Clicking a node highlights its direct upstream and downstream dependencies. Fail: Graph fails to render or omits known dependency edges. | Understanding blast radius before a deploy or incident is a primary use case for architects. |
| FR-005 | The system shall dispatch downtime alerts to a configured notification channel (e.g., Slack, email, webhook) when a service is marked unhealthy. | High | Pass: An alert is received within 60 seconds of a service being marked down. Fail: No alert is sent, or it is delayed beyond the SLA. | Alerting is what converts passive monitoring into actionable incident response. |

## Non-Functional Requirements

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|----|------|--------------|----------|----------------------|-----------|
| NFR-001 | Performance & Security | The service catalog dependency graph viewer must render interactive node architectures containing up to 200 services smoothly. | High | Pass: Benchmarking tests confirm target latency and security standards under simulated peak load. | Enterprises with large microservice fleets need the tool to remain usable at scale, not just in demos. |
| NFR-002 | Reliability | The health-check pinger subsystem must maintain at least 99.9% uptime independent of the main portal UI's availability. | High | Pass: Health checks continue running and logging even if the web UI is down, verified via a chaos/failover test. Fail: Monitoring stops when the UI process crashes. | The monitoring system itself must be more reliable than the services it watches, or outages go undetected. |