# Use-Case Flow Specification

## Use Case: Monitor Microservice Health & Dispatch Downtime Alert
**Related Requirement:** FR-001, FR-005
**Primary Actor:** DevOps Engineer (as alert recipient) / System (as automated actor)

### Preconditions
- The microservice is already registered in the catalog (via FR-002 discovery).
- The service's health endpoint URL is configured and reachable on the network.
- A notification channel (Slack/email/webhook) is configured for the DevOps Engineer.

### Postconditions
- The service's rolling 24-hour availability percentage is updated and stored.
- If the service failed 3 consecutive probes, its status is marked "Down" in the catalog and an alert has been dispatched.
- If the service is healthy, its status remains "Up" and no alert is sent.

### Main Success Scenario
1. The system's health-check pinger triggers a scheduled probe every 30 seconds for each registered service.
2. The system sends an HTTP request to the service's configured health endpoint.
3. The service responds with a success status (e.g., HTTP 200) within the timeout window.
4. The system logs the successful probe with a timestamp.
5. The system recalculates the rolling 24-hour availability percentage for that service.
6. The system updates the service's status as "Up" in the catalog dashboard.

### Alternate Flow: Service Fails Health Check (3 Consecutive Failures)
1. At step 3 above, the service fails to respond (timeout or non-200 status).
2. The system logs the failed probe with a timestamp.
3. The system checks the count of consecutive failed probes for this service.
4. If the count reaches 3, the system marks the service status as "Down" in the catalog.
5. The system dispatches an alert to the configured notification channel, including the service name, last-known-good timestamp, and failure count.
6. The DevOps Engineer receives the alert and begins incident triage.
7. Use case resumes at step 1 on the next scheduled probe cycle.