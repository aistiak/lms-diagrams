## ADDED Requirements

### Requirement: Single multi-page architecture file
The diagram set SHALL be maintained as one draw.io file (`btp-lms-architecture.drawio`) containing 10 pages across 8 diagrams, version-controlled in the repository.

#### Scenario: Reviewer opens the file
- **WHEN** a reviewer opens `btp-lms-architecture.drawio`
- **THEN** they find 10 named pages covering context, components, deployment, data model (2 pages), state lifecycles, sequences (3 pages), integrations, and observability/backup/DR

### Requirement: AWS deployment view (stakeholder-approved exception)
The set SHALL include a complete AWS-specific cloud system design page naming AWS services (Route 53, CloudFront, WAF, ALB, EC2, Lambda, RDS, ElastiCache, OpenSearch, S3, SQS, SES, SNS, CloudWatch, Backup, Secrets Manager, KMS, IAM) with zoned VPC layout, two AZs, and a cross-region DR plan. This page is exempt from the provider-neutral styling requirement per stakeholder direction; all other pages remain provider-neutral.

#### Scenario: AWS page present
- **WHEN** the draw.io file is opened
- **THEN** a dedicated AWS deployment page exists as page 0 with real AWS service names and icons, and the remaining pages contain no vendor branding

### Requirement: Provider-neutral cloud styling
All infrastructure SHALL be depicted as provider-neutral cloud building blocks using generic hyperscaler-style iconography, with components named by role (e.g., "managed relational database", "edge protection", "object storage"). No cloud vendor name, product name, or logo SHALL appear in any diagram.

#### Scenario: Vendor check
- **WHEN** any diagram page is inspected for vendor references
- **THEN** no cloud provider or product brand name is present, and infrastructure appears as generic managed-service blocks

### Requirement: Diagram coverage matches the SRS
The set SHALL cover: system context with all external actors/systems; logical component architecture highlighting the Parent Course → Language Version model; zoned deployment (Edge → DMZ → private app subnet → private data subnet + integration layer) with the SRS §13 server baseline; the ~19 SRS §7 entities; course-version, enrollment, and account lifecycles; auth/SSO, learning-lifecycle, and content-publishing sequences; integration and async worker flows; and observability, backup/PITR, and DR failover flows.

#### Scenario: SRS traceability
- **WHEN** each diagram page is reviewed against the SRS sections it cites
- **THEN** every cited SRS element (module, entity, zone, flow) has a corresponding visual element

### Requirement: Pending decisions are visually flagged
Every element whose behavior depends on an open SRS architecture decision (ARCH-01…14) SHALL be rendered dashed and labeled "pending decision (ARCH-xx)".

#### Scenario: Open decision rendered
- **WHEN** a reviewer inspects the deployment page for the hosting/CDN/SSO-protocol elements
- **THEN** those elements appear dashed with their ARCH identifiers, not as decided components

### Requirement: Scope fidelity to SRS v1.0
Diagrams SHALL reflect v1 scope only: payment rendered as an inactive stub, no instructor role, and out-of-scope items (content production, translation, marketing) omitted.

#### Scenario: Payment depiction
- **WHEN** the context or component diagram is reviewed
- **THEN** the payment integration appears as a clearly marked inactive/future stub

### Requirement: Readability conventions
Every page SHALL include a legend, and zoned/layered pages SHALL use consistent zone color-coding. Entities shared across ERD pages SHALL appear as stubs with page references.

#### Scenario: Cross-page entity navigation
- **WHEN** an entity appears on both ERD pages
- **THEN** each occurrence outside its home page is a stub linking to the authoritative page

### Requirement: Security controls annotated
TLS in transit, encryption at rest, MFA for privileged accounts, WAF, RBAC least-privilege, and secrets management SHALL be annotated on the deployment and observability/DR pages rather than omitted or given a separate page.

#### Scenario: Security annotation check
- **WHEN** the deployment and observability pages are reviewed
- **THEN** the six control areas above are each visible as annotations on the relevant elements

### Requirement: Environment promotion inset
The deployment page SHALL include an inset showing the environment promotion flow: Development → Staging → UAT → Production → DR.

#### Scenario: Environment flow visible
- **WHEN** a reviewer opens the deployment page
- **THEN** the five environments and their promotion direction are visible in the inset
