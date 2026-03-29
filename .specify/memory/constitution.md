<!--
Sync Impact Report
Version: (unversioned template) → 1.0.0
Modified principles: five template principle placeholders → I. Client Confidentiality & Data Minimization; II. Spec-Driven Delivery; III. Auditability & Accountability; IV. Testing Discipline; V. Simplicity & Justified Complexity
Added sections: Legal & Compliance Constraints; Development Workflow & Quality Gates (replacing generic Section 2 and Section 3 placeholders)
Removed sections: None
Templates: .specify/templates/plan-template.md ✅ | .specify/templates/spec-template.md ✅ | .specify/templates/tasks-template.md ✅ | .specify/templates/checklist-template.md ✅ (no change required) | .specify/templates/agent-file-template.md ✅ (no change required)
Follow-up TODOs: None
-->

# Law Office Constitution

## Core Principles

### I. Client Confidentiality & Data Minimization

Systems MUST treat client and matter information as confidential. Features MUST collect and retain only data necessary for stated requirements. Access MUST follow least privilege; credentials and secrets MUST NOT be embedded in source code or logs. Rationale: Legal practice imposes confidentiality obligations; architecture and implementation must reflect them.

### II. Spec-Driven Delivery

User-visible behavior and material scope MUST be defined in `spec.md` before implementation proceeds. Implementation plans MUST reference the active specification; task lists MUST map to user stories or explicit requirements. Scope changes MUST update `spec.md` and the plan. Rationale: Traceability from need to delivery and predictable change control.

### III. Auditability & Accountability

Where features record or process client or matter data, designs MUST support traceability appropriate to the domain (for example: material state changes, authentication events, or access to sensitive records). Implementations MUST NOT disable logging, audit hooks, or monitoring solely to mask defects. Rationale: Defensible records support professional and regulatory expectations.

### IV. Testing Discipline

When the feature specification requests automated tests or defines acceptance scenarios, those tests MUST be implemented in the same delivery increment (red-green-refactor when feasible). Contract or integration tests are REQUIRED at boundaries between modules or external systems when those boundaries are in scope. Rationale: Reduces error risk in high-stakes domains.

### V. Simplicity & Justified Complexity

Teams MUST prefer the simplest design that satisfies requirements and constitution gates. Additional layers, services, or abstractions MUST be justified in the implementation plan or complexity tracking. Undocumented complexity violates this constitution. Rationale: Simpler systems are easier to secure, test, and maintain.

## Legal & Compliance Constraints

- Features MUST align with applicable professional conduct rules and privacy obligations for the jurisdictions and practice areas in scope. When requirements are ambiguous, assumptions MUST be stated in the specification and confirmed before release.
- Third-party services that process client or matter data MUST be identified in the plan with data flows, retention, and subprocessors as appropriate.
- Cryptographic, retention, and access policies MUST match the sensitivity of data handled; use NEEDS CLARIFICATION in specs when policy is undecided.

## Development Workflow & Quality Gates

- The Constitution Check in `plan.md` MUST pass before Phase 0 research and MUST be re-evaluated after Phase 1 design.
- Pull requests that touch authentication, client or matter data, or external integrations SHOULD be checked against this constitution; material conflicts require spec or plan updates before merge.
- Use `/speckit.analyze` for non-trivial features to validate alignment before merge.

## Governance

This constitution supersedes informal practices when they conflict. Amendments require editing `.specify/memory/constitution.md`, incrementing **CONSTITUTION_VERSION** under semantic rules, updating **Last Amended**, and propagating material changes to dependent templates and commands.

**Versioning policy**: MAJOR for backward-incompatible principle changes or removals; MINOR for new principles or materially expanded guidance; PATCH for clarifications, wording, and non-semantic fixes.

**Compliance review**: Reviewers SHOULD verify constitution gates on changes affecting privileged data, security controls, or regulatory posture.

**Version**: 1.0.0 | **Ratified**: 2025-03-24 | **Last Amended**: 2025-03-24
