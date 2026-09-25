## Why

The BTP E-Learning Platform SRS v1.0 (BTP-EL-SRS-001) defines a bilingual LMS with 16 functional modules, ~19 data entities, a zoned data-center/cloud deployment, and 14 open architecture decisions — but contains no visual architecture artifacts. A complete, review-ready diagram set is needed so stakeholders and engineers can validate the design before HLD/LLD work begins.

## What Changes

- Create a single multi-page draw.io file (`btp-lms-architecture.drawio`) in the repository containing **10 pages across 8 diagrams**:
  1. **System Context (C4 L1)** — actors + external systems (BTP SSO/identity, government email/SMS gateways, inactive payment stub)
  2. **Logical Component Architecture** — internal services (auth, course, curriculum, enrollment, assessment, certification, notifications, reporting, CMS/admin); Parent Course → Language Version pivot highlighted
  3. **Network / Deployment Architecture** — zoned layout (Edge → DMZ → private app subnet → private data subnet + integration layer), load balancers, app servers, background workers, primary DB + read replica, cache, search, object storage
  4. **Core Data Model (ERD)** — ~19 entities, split across 2 pages: learning domain + platform/audit domain
  5. **State / Lifecycle Diagram** — course version (Draft → Published → Archived), enrollment statuses, account statuses
  6. **Sequence Diagrams (3 pages)** — (a) Auth & SSO incl. account linking + OTP; (b) Learning lifecycle: discover → enroll (version-bound) → progress → assessment → auto-completion → certificate issuance; (c) Content publishing workflow
  7. **Integration & Async Processing** — BTP API gateway, email/SMS gateways, background workers, retry/idempotency, delivery logs
  8. **Observability, Backup & Disaster Recovery** — log/metric/audit flows to monitoring + SIEM, backup schedule with PITR and restore testing, production → DR failover paths
- All diagrams drawn **cloud-based**: components depicted as cloud-hosted/managed-service-style building blocks (edge protection, managed load balancing, managed database/cache/search/object storage, monitored compute) using generic hyperscaler-style iconography — **no vendor is named or branded in any diagram**
- Open decisions (ARCH-01…14) rendered as dashed elements labeled *"pending decision"*
- v1 scope only: payment drawn as inactive stub; no instructor role (per BR-007)
- Native draw.io shape libraries used for icons; legend + zone color-coding on every page
- Security controls (TLS, encryption at rest, MFA, WAF policy, secrets management) annotated on the deployment and observability diagrams rather than a separate page
- Environment promotion flow (Dev → Staging → UAT → Production → DR) shown as an inset on the deployment diagram

## Capabilities

### New Capabilities
- `system-diagrams`: The complete architecture diagram set for the BTP E-Learning Platform — context, logical components, deployment, data model, lifecycles, key sequences, integrations, and observability/backup/DR views, maintained as a single multi-page draw.io file

### Modified Capabilities
<!-- None — this is the first change; no existing specs are modified. -->

## Impact

- **Affected specs:** none (new `system-diagrams` capability only)
- **Affected code:** none — documentation-only change
- **Outputs:** 1 `.drawio` file (10 pages) under version control in this repository, plus proposal/tasks tracking
- **Consumers:** architecture reviewers, HLD/LLD authors, engineering team, client stakeholders (diagrams are the visual companion to BTP-EL-SRS-001)
