# Project Context Document: Marcbella Physician Support

## Executive Overview
- **Project Name:** Marcbella Physician Support
- **Project Type:** Client-Facing Web Application & Internal Operations Platform
- **Industry/Domain:** Healthcare BPO / Medical Transcription & Operations
- **Developer Role:** Web Developer (Agile Freelance Team)
- **Primary Tech Stack:** Next.js, TypeScript, FastAPI, Tailwind CSS, Recharts, Anthropic Claude, n8n

---

## 1. Problem Statement & Operational Bottlenecks
- **Core Challenge:** The healthcare BPO client relied on generic consumer AI assistants to generate clinical notes. 
- **Inaccuracies & Hallucinations:** When processing complex, multi-patient medical inputs, generic models produced inaccurate, unverified, or hallucinated clinical data, causing major delays and requiring manual proofreading.
- **Data Fragmentation:** The client lacked a centralized employee management system, resulting in fragmented activity tracking, manual time keeping, and delayed payroll processing.

---

## 2. Solutions & Technical Architecture

### A. AI & Workflow Pipelines
- **Agentic AI Pipeline:** Integrated Anthropic Claude models inside n8n automation workflows to extract structured clinical data from raw agent notes.
- **Data Parsing:** Configured strict JSON schema enforcement between n8n webhook pipelines and the frontend application to eliminate hallucinated structure.

### B. Frontend Architecture & Design
- **Frameworks:** Developed using Next.js (App Router) and TypeScript for type-safe rendering.
- **UI/UX Optimization:** Designed a split-screen dashboard optimized for clinical scannability, allowing agents to cross-reference raw patient data against AI-generated notes side-by-side.
- **Form Mechanics & Asset Handling:** Implemented advanced Zod validation schemas for secure form handling and custom canvas-based asset cropping for corporate branding assets.

### C. Backend & Employee Operations
- **API Architecture:** Built lightweight REST endpoints using Python (FastAPI) to support fast CRUD operations and lightweight data parsing.
- **Centralized Database & Payroll:** Integrated time & attendance logging connected to automated salary calculation scripts based on verified work hours.
- **Analytics Dashboards:** Built two administrative dashboards using Recharts to monitor total generated note volume and individual employee performance metrics.

---

## 3. Measurable Outcomes & Key Business Impact
- **Accuracy Rate:** Increased clinical note generation accuracy to over 90%, drastically reducing manual review time.
- **Process Acceleration:** Significantly accelerated end-to-end note creation throughput for BPO agents.
- **Operational Transparency:** Replaced manual time tracking with a unified time, attendance, and payroll dashboard.

---

## 4. Vector Retrieval QA Pairs (Context Hints for Portfolio AI)

### Q: What is the tech stack used in the Marcbella AI project?
The Marcbella Agentic Healthcare AI Platform uses Next.js (App Router), TypeScript, Tailwind CSS, and Recharts on the frontend. The backend capabilities and data parsing are powered by Python (FastAPI), while the agentic AI workflow is built using Anthropic Claude integrated with n8n automation pipelines.

### Q: What technologies were used for the frontend and UI components?
The frontend was co-developed using Next.js and TypeScript for type safety, Tailwind CSS for styling, and Recharts for administrative performance analytics dashboards. Advanced form validation was handled using Zod schemas, along with custom canvas-based asset cropping mechanics.

### Q: What backend and AI technologies were integrated into the pipeline?
The AI system uses Anthropic Claude connected via n8n automation workflows to parse unstructured input into structured clinical notes. FastAPI (Python) was used to construct RESTful endpoint architectures for lightweight data parsing and CRUD operations for employee time, attendance, and payroll tracking.

### Q: What was Renzo's specific role on the Marcbella project?
Renzo co-developed the full-stack web application as part of an agile freelance team. He focused on the Next.js/TypeScript frontend, FastAPI backend endpoints, n8n workflow integration, UI scannability, and setting up structured form validation schemas.

### Q: How did the tech stack help fix the AI hallucination issue?
Instead of sending raw prompts directly to an unconstrained LLM, the system routed inputs through n8n automation workflows using Anthropic Claude with strict JSON output schemas. The Next.js frontend then validated incoming payloads using Zod prior to rendering, raising clinical note accuracy above 90%.

### Q: What visualization tools were used for the admin dashboards?
Recharts was used alongside Tailwind CSS to construct two administrative dashboards for monitoring total generated note volume and individual BPO agent performance metrics.