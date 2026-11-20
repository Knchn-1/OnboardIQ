# Project Specification — OnboardIQ / Northstar Technologies

## 1. Product context
OnboardIQ is planned as an AI-powered employee onboarding and organizational knowledge assistant. Employees should be able to ask grounded questions about company policies, procedures, departments, roles, contacts, internal workflows and onboarding tasks. Responses should cite the source document, section and PDF page where available.

The knowledge base is being prepared before the application. Do not build the production application in this work package.

## 2. Company profile
Northstar Technologies is a fictional Indian IT-services company focused on software engineering, data analytics, AI and cloud solutions.

- Head office: Nagpur, Maharashtra.
- Other offices: Pune, Maharashtra; Bengaluru, Karnataka.
- Departments (exactly six): HR, IT, ENG, DA, FIN, SCS.
- Do not add a seventh department. A corporate-wide owner classification, if truly required, must be separate from the department list and justified in the decision log.

The supplied Directory is the authority for employees and any company facts it explicitly contains. If the Directory differs from this specification on an employee or organizational fact, preserve the Directory and flag the conflict.

## 3. Intended knowledge domains
- People and organization: employee directory, departments, reporting lines, contact routing.
- HR: handbook, conduct, attendance, leave, onboarding, referral, performance and promotion.
- IT: acceptable use, account/device setup, information security, incident reporting.
- Engineering: development workflow, source control, code review, release practices.
- Data & Analytics: data access, data handling, analytics delivery and quality practices.
- Finance & Administration: expenses, reimbursements, travel and approvals.
- Sales & Customer Success: customer communication, handoffs, escalation and service practices.

## 4. Intended downstream RAG pipeline
Document ingestion → text extraction → structure-aware chunking → embeddings → PostgreSQL/pgvector → PostgreSQL full-text search → hybrid retrieval → Reciprocal Rank Fusion → cross-encoder reranking → authorization-aware context assembly → LLM response → citations.

The knowledge base must retain:
- source filename and hash;
- document ID and version;
- section ID and heading path;
- page range when reliably available;
- lifecycle state;
- audience and resolved allowed groups;
- provenance and source-of-truth references;
- chunk ID and indexing status.

## 5. Non-goals
- Do not build the React/FastAPI application.
- Do not connect to a real HR system or employee database.
- Do not use real employee personal data beyond the supplied fictional Directory.
- Do not claim legal compliance or production readiness.
- Do not create multi-tenant or multi-company functionality.
