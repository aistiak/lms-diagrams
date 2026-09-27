# BTP E-Learning Platform — Architecture Diagrams



---

## 0 · System Context
The platform as one box with its actors and external systems — BTP SSO/Identity, government email/SMS gateways, inactive payment stub, monitoring/SIEM.

![System Context](images/01-system-context.png)

## 1 · Logical Component Architecture
Internal services across application and data tiers; the **Parent Course → Language Versions** bilingual model is highlighted (BR-001).

![Logical Components](images/02-components.png)

## 2 · Network / Deployment Architecture
Five color-coded zones — Edge → DMZ → private app subnet → private data subnet → integration/identity — with the server baseline, security annotations, and environment promotion inset.

![Deployment](images/03-deployment.png)

## 3 · Core Data Model — Learning Domain
ERD of the learning domain: parent course, language versions, curriculum, enrollment, progress, assessments, and certificates.

![ERD Learning Domain](images/04-erd-learning.png)

## 4 · Core Data Model — Platform & Audit Domain
ERD of the platform domain: users, profiles, admin roles, notifications and delivery logs, audit/login trails, taxonomy, integration mapping, settings.

![ERD Platform Domain](images/05-erd-platform.png)

## 5 · State / Lifecycle Diagram
Status transitions for course language versions, enrollments, and user accounts.

![State Lifecycles](images/06-state-lifecycles.png)

## 6 · Sequence — Auth & SSO
BTP SSO login, self-registration with OTP verification, and account linking.

![Auth & SSO Sequence](images/07-seq-auth-sso.png)

## 7 · Sequence — Learning Lifecycle
Discover → enroll → learn/progress → assessment → async completion and certificate issuance.

![Learning Lifecycle Sequence](images/08-seq-learning.png)

## 8 · Sequence — Content Publishing
Admin creates a parent course once, adds Bangla + English versions, builds curriculum, then publishes and maintains per version.

![Content Publishing Sequence](images/09-seq-publishing.png)

## 9 · Integration, Observability, Backup & DR
BTP API gateway and async job flow (retry, idempotency, dead-letter), plus SIEM shipping, PITR backups, and DR failover.

![Integration, Observability, Backup & DR](images/10-integration-ops-dr.png)

---

## Resource Sizing Estimates (CPU / Memory)

Indicative sizing per registered-user tier, assuming ~8–10% peak concurrency, video served by CloudFront (app tier serves API/pages only), and Lambda offloading async work (certificates, notifications). Quiz/exam bursts are the DB-heavy path.

| Registered users | Peak concurrent | App tier (EC2, per AZ) | RDS (Multi-AZ) | Read replica | ElastiCache | Search (OpenSearch) |
|---:|---:|---|---|---|---|---|
| 500 | ~50 | 2× 2 vCPU / 4 GB | 2 vCPU / 4 GB | — | 1 vCPU / 1 GB | — (RDS FTS) |
| 1,000 | ~100 | 2× 2 vCPU / 8 GB | 2 vCPU / 8 GB | — | 1 vCPU / 2 GB | optional 1× 2 vCPU / 8 GB |
| 2,000 | ~200 | 2× 4 vCPU / 8 GB | 4 vCPU / 16 GB | — | 2 vCPU / 4 GB | 1× 2 vCPU / 8 GB |
| 5,000 | ~500 | 2–3× 4 vCPU / 16 GB (ASG) | 8 vCPU / 32 GB | 1× 4 vCPU / 16 GB | 4 vCPU / 8 GB | 2× 2 vCPU / 8 GB |
| 10,000 | ~1,000 | 3–4× 8 vCPU / 16 GB (ASG) | 8 vCPU / 32 GB | 1–2× 8 vCPU / 32 GB | 8 vCPU / 16 GB | 3× 2 vCPU / 8 GB |

**Notes**

- The SRS §13 baseline (2× 8 vCPU / 16 GB app servers, 8 vCPU / 16–32 GB DB) corresponds to the **5,000–10,000 user** tier — treat it as the provisioning target, with smaller tiers as a staged rollout path.
- Use autoscaling (ASG on CPU ~60% / request count) rather than fixed headroom; minimum 1 node per AZ for HA.
- Exam-week spikes: size the DB for quiz bursts (reads + writes per attempt), pre-scale before known exam windows; everything else can scale elastically.
- These are planning estimates, not contractual capacity figures (SRS lists performance targets as optimization goals, not guarantees).
