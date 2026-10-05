# Lab 3 - Component Modelling & Architectural Pattern Selection

Architecture design for the Internal Microservice Catalog & Health Portal, extending the requirements (Lab 1) and Agile planning (Lab 2).

## Architecture Selected
**Microservices Architecture**, compared against Layered and Client-Server.

## Components
- Web Portal UI
- Auth Service
- API Gateway
- Catalog Service
- Health Monitor Service
- Dependency Graph Service
- API Docs Service
- Notification Service
- Catalog DB, Metrics DB, Graph DB, Docs Store
- External systems: Monitored Microservices, Email / Slack

## Key Interfaces
IPortalAPI, IAuth, ICatalog, IHealth, IDependency, IDocs, IAlert, ISend, IHealthCheck, IApiSpec, plus a data interface for each database.

## Files
- [lab3_component_diagram.png](lab3_component_diagram.png) - UML component diagram
- [lab3_justification.pdf](lab3_justification.pdf) - 1-page architecture justification
