## Context

The BTP E-Learning Platform SRS v1.0 (BTP-EL-SRS-001) exists as text only. Architecture reviews, HLD/LLD authoring, and client sign-off all need a shared visual reference. The SRS is a draft: 14 architecture decisions (ARCH-01…14) and 28 approval items (AP-001…028) are open, so diagrams must stay honest about what is decided vs. pending. The deployment target is a managed cloud-style environment (hosting location itself is ARCH-pending); diagrams must therefore read as provider-neutral cloud architecture.

## Goals / Non-Goals

**Goals:**
- One version-controlled draw.io file covering context, components, deployment, data, lifecycles, sequences, integrations, and ops (10 pages, 8 diagrams)
- Provider-neutral cloud-style rendering: managed-service building blocks and generic hyperscaler-style icons, no vendor naming or branding
- Traceability: every element maps to an SRS section; open items visually flagged as pending
- Review-ready quality: legends, zone color-coding, consistent notation on every page

**Non-Goals:**
- HLD/LLD documents themselves (separate change)
- Mermaid/SVG/PNG exports (add later on request)
- Diagramming the testing matrix, gamification internals, or out-of-scope content production
- Naming or depicting any specific cloud provider

## Decisions

0. **Tooling: local draw.io desktop + MCP-driven XML generation** → diagrams are generated and edited programmatically via a draw.io MCP server (which writes/edits `.drawio` XML), then visually refined in a locally installed draw.io desktop instance (`brew install --cask drawio`). Rationale: MCP handles structure, pages, and element creation agentically; the desktop app handles what XML generation does poorly (layout polish) and is the review/preview surface. No draw.io web/Confluence dependency — everything stays local and version-controlled. Fallback if the MCP server proves unreliable: write the `.drawio` XML directly (it is plain, well-documented XML).
1. **Single multi-page `.drawio` file, not one file per diagram** → cross-page references stay intact, one artifact to review/version. Alternative (file per diagram) rejected: sync burden across 8 files.
2. **Provider-neutral cloud styling** → draw.io generic cloud/network shape libraries; components named by role ("managed relational database", "edge protection", "object storage"), not by product. AWS-style libraries may *inspire* visual language but no AWS branding, names, or logos appear. Rationale: hosting provider is an open decision (ARCH-01); vendor-neutral diagrams survive any outcome and avoid implying commitments the SRS does not make.
3. **C4-style layering for pages 1–2** → context first, then containers/components; matches how reviewers naturally zoom in.
4. **ERD split into two pages** (learning domain / platform & audit domain) → ~19 entities on one page would be unreadable; shared entities (User, Course) repeated as stubs with page references.
5. **State diagram as a first-class page** → the SRS makes lifecycles (course version, enrollment, account) normative; ERD and sequences cannot express transitions.
6. **Ops concerns get their own page** (observability, backup/PITR, DR failover) → SRS §13 has enough substance (SIEM, restore testing, RPO/RTO pending NDC/BCC approval) that folding it into deployment would hide it.
7. **Pending decisions as dashed elements** with a "pending decision (ARCH-xx)" tag, not omissions or invented choices.
8. **draw.io over Mermaid** → only draw.io supports zoned network layouts with icon libraries; Mermaid cannot express the deployment diagram adequately.

## Risks / Trade-offs

- [MCP/manual XML generation produces rough layout] → Structure generated programmatically; final alignment pass done in the draw.io desktop app before review
- [Icon styles for generic shapes vary across draw.io versions] → Stick to built-in shape libraries shipped with the desktop app; no external icon imports
- [SRS is a draft; diagrams will drift if SRS changes] → Each page carries its SRS section reference; diagram updates triggered by SRS version bumps (tracked in tasks)
- [Provider-neutral naming may feel abstract to reviewers expecting concrete products] → Legend on the deployment page maps each generic block to example managed-service categories

## Migration Plan

Not applicable — additive documentation change. Rollback = delete the file and change folder.

## Open Questions

- AWS-specific page (page 0) added per stakeholder direction, superseding the provider-neutral rule for that page only — hosting/CDN/SSO-protocol decisions it visualizes remain formally open (ARCH) until the client confirms AWS as the target.

- Should PNG/SVG exports be generated as CI artifacts later? (deferred)
- DR site naming once RPO/RTO targets are approved (NDC/BCC pending) — placeholders used until then
- Exact search infrastructure labeling (Solr named in SRS baseline; rendered generically, with Solr as a note) — confirm at review
