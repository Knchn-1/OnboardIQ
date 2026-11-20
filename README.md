# OnboardIQ

**DEMONSTRATION ONLY - NOT APPROVED FOR REAL-WORLD USE**

OnboardIQ is an AI-powered employee onboarding and organizational knowledge assistant being designed for **Northstar Technologies**, a fictional Indian IT-services enterprise.

---

## 1. Corporate Knowledge Base

The complete Northstar Technologies corporate policy documents, employee directory, RAG ingestion metadata, access-control rules, and evaluation datasets are organized and maintained under [`knowledge_base/`](knowledge_base/README.md).

For full details regarding the corporate policies, master data, and RAG manifests, please refer directly to [`knowledge_base/README.md`](knowledge_base/README.md).

---

## 2. Unresolved Items & Integrity Status

In accordance with project governance standards, the following 4 unresolved items are documented:

1. **Organizational Hierarchy Anomalies**: The employee directory contains 13 employees across 6 canonical departments. Five department heads report to unlisted C-suite roles (CTO, COO, CFO), and EMP-001 (CEO) has department *Executive Leadership*, creating 6 disconnected roots. These roles remain explicitly unassigned rather than fabricating identities.
2. **Statutory Position Verification**: 8 statutory-adjacent topics (leave minima under state Shops & Establishments Acts, overtime comp-off, POSH Internal Committee constitution, retirement age, gratuity, and DPDP Act compliance) carry the explicit label *"Statutory position to be verified by qualified legal/HR counsel before real-world use."* and are logged in the Legal Review Register pending qualified legal review.
3. **PDF Generation Status**: PDF policy documents are labeled `REBUILT_FROM_SOURCE` and marked `PARTIALLY_VERIFIED`. Native DOCX conversion via Word COM was unavailable in the sandboxed build environment; documents were rebuilt using ReportLab 4.5.0 and inspected via automated geometry checks and rendered PNG screenshots.
4. **Third-Party Template Licensing**: The raw templates located in `source/` are downloaded third-party documents whose commercial licensing has not been established. All knowledge-base documents in `knowledge_base/` were rewritten in original Northstar prose. To prevent unauthorized distribution of third-party templates, the `source/` directory is strictly **gitignored**.

---

## 3. Application Architecture & Development Status

The production application stack is currently in the initial scaffolding phase. All application features are **PLANNED** and not yet implemented:

- **Frontend** *(PLANNED)*: React + TypeScript + Tailwind CSS single-page application (scaffold to be created in `frontend/`).
- **Backend** *(PLANNED)*: FastAPI REST API with async database access (scaffold in `backend/app/`).
  - Currently implemented: Minimal health check endpoint only (`GET /health` returning `{"status":"ok"}`).
  - Planned: Authentication, fail-closed RAG retrieval, chat assistant, onboarding checklist workflows.
- **Database** *(PLANNED)*: PostgreSQL 16 with the `pgvector` extension (configured via `docker-compose.yml`).

---

## 4. Local Infrastructure

The database service can be launched via Docker Compose:

```bash
# Copy placeholder environment variables
cp .env.example .env

# Start PostgreSQL with pgvector
docker-compose up -d db
```
