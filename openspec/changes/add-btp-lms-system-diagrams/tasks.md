## 1. Tooling & File Setup

- [x] 1.0 Install and configure tooling: draw.io desktop (`brew install --cask drawio`) + a draw.io MCP server (`claude mcp add`) so diagram XML can be generated/edited agentically; verify create-page / add-element / save round-trip works
- [x] 1.1 Create `btp-lms-architecture.drawio` (via MCP) with 10 named pages and a shared style palette (zone colors, fonts, dashed "pending decision" style)
- [x] 1.2 Build the reusable legend block (shapes, colors, line types, ARCH-pending tag, stub-entity marker) and place it on every page
- [x] 1.3 Verify draw.io generic cloud/network shape libraries resolve correctly in the desktop app (no external icon imports)

## 2. Context & Component Views

- [x] 2.1 Page 1 — System Context (C4 L1): actors (Learner, Admin, System/Worker) + external systems (BTP SSO/identity, gov email/SMS gateways, payment stub, monitoring/SIEM); cite SRS §4, §5.15
- [x] 2.2 Page 2 — Logical Component Architecture: 10 internal services with dependencies; visually emphasize Parent Course → Language Version pivot; annotate no-instructor-role note (BR-007); cite SRS §5, §7

## 3. Deployment View

- [x] 3.1 Page 3 — Zoned deployment: Edge → DMZ → private app subnet → private data subnet + integration layer, with LB pair, 2 app servers, 1–2 workers, primary DB + read replica, cache, search, object storage, monitoring node; cite SRS §13 baseline
- [x] 3.2 Annotate security controls on page 3: TLS 1.2+, WAF, encryption at rest, MFA, RBAC least-privilege, secrets management
- [x] 3.3 Add environment-promotion inset (Dev → Staging → UAT → Production → DR) and mark ARCH-pending elements (hosting, CDN, HA model, DR targets) as dashed with ARCH ids
- [x] 3.4 Add legend note mapping each generic block to its managed-service category
- [x] 3.5 Page 0 — AWS Cloud System Design (stakeholder-requested addition): Route 53 → CloudFront → WAF/Shield → ALB → EC2 in 2 AZs + Lambda workers, RDS Multi-AZ + replica, ElastiCache, OpenSearch, S3, SQS, SES/SNS, CloudWatch/Backup/Secrets Manager/KMS/IAM, cross-region DR; spec amended with an AWS-exception requirement

## 4. Data & Lifecycle Views

- [x] 4.1 Page 4 — ERD learning domain: Parent Course, Course Language Version, Module, Lesson, Media, Enrollment, Progress, Question Bank/Question, Assessment, Attempt/Answer, Certificate Template/Certificate (with cardinality: 1 Parent → 1–2 versions)
- [x] 4.2 Page 5 — ERD platform/audit domain: User, Learner Profile, Notification/Delivery Log, Category/Topic/Tag, Audit Log, Integration Mapping, System Setting; stub-repeated shared entities with page refs
- [x] 4.3 Page 6 — State/lifecycle diagram: course version (Draft → Published → Archived), enrollment statuses, account statuses; cite SRS §5.3–5.6

## 5. Sequence Diagrams

- [x] 5.1 Page 7 — Auth & SSO sequence: BTP SSO login, account linking, self-registration with OTP verification, session management; cite SRS §5.2
- [x] 5.2 Page 8 — Learning lifecycle sequence: discover → enroll (version-bound, duplicate prevention) → progress tracking → assessment attempt/grading → auto-completion → async certificate issuance (incl. worker); cite SRS §5.5–5.8
- [x] 5.3 Page 9 — Content publishing sequence: parent course creation → version cloning → curriculum build → draft/publish workflow → archiving; cite SRS §5.3–5.4

## 6. Integration & Ops Views

- [x] 6.1 Page 10 — Integration & async processing: BTP API gateway (role mapping, retry/idempotency), email/SMS gateway flows, background worker jobs, delivery logs; cite SRS §5.15–5.16
- [x] 6.2 Page 10 (or companion lane) — Observability, backup & DR: log/metric/audit flows to monitoring + SIEM, daily backup with PITR + restore testing, Production → DR failover with RPO/RTO placeholders pending NDC/BCC approval

## 7. Review & Finalize

- [x] 7.1 Vendor-neutrality pass: confirm no cloud provider or product brand appears anywhere (Solr permitted only as an SRS-baseline note)
- [x] 7.2 SRS traceability pass: every page's cited sections verified against BTP-EL-SRS-001; all 14 ARCH decisions appear where relevant
- [ ] 7.3 Layout polish pass in draw.io desktop app (alignment, spacing, overlapping edges)
- [ ] 7.4 Final review with stakeholder; capture feedback as follow-up change proposals
