# AB-PMJAY Claim Rejection Explanation and Grievance Recourse

## 1. Project Overview

### Project Title

**Claim Rejection Explanation and Grievance Recourse**

### Problem Statement

Build an AI-assisted system for Ayushman Bharat PM-JAY that can answer:

> **Why was the claim rejected, what valid corrective or grievance path remains, and what deadlines apply?**

The system should explain claim rejection decisions using authoritative AB-PMJAY information while ensuring that deterministic policy and eligibility rules are not overridden by an AI model.

### Core Principle

> **AI explains. Rules decide.**

The AI/LLM is responsible for generating understandable explanations from retrieved evidence.

Deterministic rules are responsible for authoritative decisions such as:

* rejection interpretation
* corrective action
* grievance route
* deadlines
* escalation
* entitlement/policy constraints

---

# 2. Planned System Architecture

The intended architecture is a hybrid system:

```text
                    Claim
                      |
          +-----------+-----------+
          |                       |
          v                       v
   Rule Database             Knowledge Base
   (Deterministic)             (RAG)
          |                       |
          v                       v
   Rule Evaluation          Vector Retrieval
          |                       |
          +-----------+-----------+
                      |
                      v
                  Validation
                      |
                      v
               AI Explanation
                      |
                      v
              Structured Output
```

The system combines:

1. **Relational/deterministic rules**
2. **Retrieval-Augmented Generation (RAG)**
3. **Bounded workflow/agentic reasoning**
4. **Structured outputs**
5. **Citation/evidence tracing**
6. **Safe failure and human escalation**

---

# 3. Authoritative Source

The main source currently being used is:

**AB-PMJAY Grievance Redressal Guidelines, December 2021**

Published by the **National Health Authority (NHA)**.

The document describes the AB-PMJAY grievance redressal mechanism, including:

* Centralized Grievance Redressal Management System (CGRMS)
* District, State and National grievance levels
* grievance officers and committees
* grievance registration
* grievance escalation
* prescribed turnaround times (TAT)
* grievance categories
* grievance resolution
* escalation when grievances are not acted upon within the prescribed time

The PDF is stored in the repository under:

```text
data/Grievance_Redressal_Guidelines.pdf
```

---

# 4. Important Source Understanding

The grievance guideline contains information about the grievance process.

For example, it describes automatic escalation when a grievance is not resolved within the prescribed TAT or when no action is taken.

The document also contains grievance categories involving claims rejected by an insurer/SHA, including full or partial claim rejection.

Important distinction:

> A grievance category mentioned in the guideline is NOT automatically a claim rejection code.

Rejection codes and deterministic claim rules will be maintained separately in the rule database.

---

# 5. Development Philosophy

The project is being developed step by step because the developer is learning AI concepts from the basics.

Important concepts already learned:

* Python basics
* variables and data types
* conditions
* functions
* lists and dictionaries
* JSON
* APIs
* validation
* Git/GitHub
* Python virtual environments
* Pydantic
* deterministic rule systems
* safe failure
* RAG
* embeddings
* cosine similarity
* semantic retrieval
* PostgreSQL
* pgvector concept

The system should remain understandable and explainable rather than becoming an opaque AI system.

---

# 6. Current Repository Structure

Current project repository:

```text
ABPMJAY-Claims-Grievance/
│
├── data/
│   ├── Grievance_Redressal_Guidelines.pdf
│   ├── Grievance_Redressal_Guidelines.txt
│   ├── chunks.json
│   ├── cleaned_chunks.txt
│   └── embedded_chunks.json
│
├── claim_checker.py
├── claim_model.py
├── rules.py
├── retrieval.py
├── requirements/requirement file
└── PROJECT_CONTEXT.md
```

Note:

The actual dependency file currently used in the project is:

```text
requirement.txt
```

It is singular.

---

# 7. Python Environment

Development is being done in **GitHub Codespaces**.

The project uses a Python virtual environment called:

```text
Agent
```

The environment contains the major packages required for the current prototype, including:

* pydantic
* pymupdf
* sentence-transformers
* scikit-learn
* scipy
* torch
* transformers

Python version can vary between Codespaces, so verify with:

```bash
python --version
```

and:

```bash
which python
```

when debugging environment problems.

---

# 8. Deterministic Rule System

The first part of the project was a simple deterministic claim checker.

The initial fictional rejection codes used during learning were:

```text
R01
R02
R03
```

These are currently **fictional/example codes** and must not be presented as official AB-PMJAY rejection codes.

The rule structure contains:

```text
cause
action
grievance_path
deadline_days
```

Rules are represented using Pydantic models.

Conceptually:

```text
Rejection Code
      |
      v
Rule Lookup
      |
      v
Rule
 ├── cause
 ├── action
 ├── grievance_path
 └── deadline_days
```

---

# 9. Rule Validation

A validation gate was implemented.

Conceptually:

```python
def is_rule_valid(rule):
    if rule is None:
        return False

    if not rule.cause:
        return False

    if not rule.action:
        return False

    if not rule.grievance_path:
        return False

    if rule.deadline_days is None:
        return False

    if rule.deadline_days < 0:
        return False

    return True
```

The purpose is:

> Never allow an incomplete rule to become an authoritative decision.

---

# 10. Evaluation Result

A structured Pydantic result model was created:

```python
class EvaluationResult(BaseModel):
    valid: bool
    rule: Rule | None
```

The evaluation flow is:

```text
Rejection Code
      |
      v
get_rule()
      |
      v
is_rule_valid()
      |
      +---- invalid ----> Safe Failure
      |
      +---- valid ------> EvaluationResult
```

This separates:

* rule lookup
* rule validation
* final evaluation result

---

# 11. Safe Failure

The system should not invent an answer when authoritative information is unavailable.

For an unknown or invalid rule:

```text
valid = False
rule = None
```

The future system should use the same principle for RAG and AI generation:

> If evidence is insufficient, abstain or escalate instead of guessing.

---

# 12. RAG Pipeline

The RAG pipeline currently follows:

```text
Official PDF
     |
     v
Text Extraction
     |
     v
Page-aware Chunking
     |
     v
chunks.json
     |
     v
Embedding Model
     |
     v
embedded_chunks.json
     |
     v
Semantic Retrieval
     |
     v
Relevant Evidence
```

---

# 13. PDF Extraction

PyMuPDF is used to extract text from the grievance guideline PDF.

The PDF is processed page-by-page so that each chunk retains source metadata.

Each chunk contains information similar to:

```json
{
  "text": "...",
  "metadata": {
    "source": "National Health Authority",
    "document": "AB-PMJAY Grievance Redressal Guidelines",
    "version": "December 2021",
    "page": 2
  }
}
```

Page numbers are important because future explanations must be traceable back to the authoritative source.

---

# 14. Chunking

The document was converted into page-aware chunks.

The current chunking approach:

* processes each PDF page independently
* removes empty lines
* removes isolated numeric page markers
* preserves headings
* preserves table-related information
* preserves deadlines and authorities
* limits chunk size

The current PDF produced approximately:

```text
52 chunks
```

The exact number may change if the chunking logic is modified.

The structured chunk dataset is:

```text
data/chunks.json
```

---

# 15. Embeddings

A pretrained embedding model is being used rather than training an embedding model from scratch.

Current model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The model produces:

```text
384-dimensional embeddings
```

For example:

```text
Text
 |
 v
Embedding Model
 |
 v
[0.12, -0.03, 0.44, ...]
```

These numbers represent the text in vector space.

Important:

> Embeddings are used for semantic retrieval. They do NOT determine whether a policy decision is valid.

---

# 16. Semantic Similarity

Cosine similarity is currently used to compare:

* query embedding
* document chunk embedding

Conceptually:

```text
User Query
    |
    v
Query Embedding
    |
    v
Compare against chunk embeddings
    |
    v
Cosine Similarity
    |
    v
Rank chunks
    |
    v
Top-K results
```

A similarity score is a mathematical measure of vector alignment.

It should NOT be interpreted as a percentage of factual correctness.

---

# 17. Current Retrieval Implementation

The current prototype loads:

```text
data/embedded_chunks.json
```

into Python.

Then it:

1. embeds the query
2. calculates cosine similarity against every chunk
3. sorts the chunks by similarity
4. returns the top results

The reusable function is conceptually:

```python
def retrieve(query, top_k=5):
    query_embedding = model.encode(query)

    for chunk in chunks:
        chunk_embedding = chunk["embedding"]

        similarity = cosine_similarity(
            [query_embedding],
            [chunk_embedding]
        )[0][0]

        chunk["similarity"] = float(similarity)

    ranked_chunks = sorted(
        chunks,
        key=lambda chunk: chunk["similarity"],
        reverse=True
    )

    return ranked_chunks[:top_k]
```

Current retrieval returns the top 5 relevant chunks by default.

---

# 18. Important Retrieval Architecture Decision

The current prototype performs vector retrieval manually in Python.

This is useful for learning and validating the concept.

However, the target architecture is:

```text
PostgreSQL
     +
pgvector
     |
     v
Database-backed vector search
```

Important distinction:

> Cosine similarity is the mathematical similarity measure.

> pgvector is the PostgreSQL extension that allows vectors to be stored and searched efficiently inside PostgreSQL.

Therefore, pgvector does not introduce the concept of retrieval. We have already implemented retrieval manually.

pgvector will make the retrieval system more scalable and integrated with the project's database.

---

# 19. PostgreSQL Status

PostgreSQL has been installed in the current Ubuntu Codespace.

Current version:

```text
PostgreSQL 16.15
```

The PostgreSQL service is running on:

```text
port 5432
```

The next database-related task is to install/configure:

```text
pgvector
```

and then move the embedded chunk data from JSON into PostgreSQL.

---

# 20. Planned PostgreSQL + pgvector Structure

The intended database will eventually contain structured knowledge such as:

```text
knowledge_chunks
----------------
id
text
source
document
version
page
embedding
```

The vector column will use pgvector.

Conceptually:

```text
knowledge_chunks
       |
       +-- text
       +-- source
       +-- document
       +-- version
       +-- page
       +-- embedding
```

The rules database will remain separate from the RAG knowledge base.

---

# 21. Rules Database vs Knowledge Base

This distinction is extremely important.

### Knowledge Base

Used for:

```text
"What does the official guideline say?"
```

Examples:

* grievance process
* escalation process
* authorities
* documented procedures
* source evidence
* TAT descriptions

### Rules Database

Used for:

```text
"What deterministic decision should the system make?"
```

Examples:

* rejection interpretation
* corrective action
* valid grievance route
* deadline
* eligibility/policy constraints

Therefore:

```text
Knowledge Base = Evidence

Rules Database = Decision Logic
```

---

# 22. Target Claim Processing Flow

The future system should work approximately like this:

```text
Claim / Rejection Information
            |
            v
      Rule Evaluation
            |
            +----------------+
            |                |
            v                v
     Deterministic       RAG Retrieval
       Decision          Official Evidence
            |                |
            +-------+--------+
                    |
                    v
               Validation
                    |
                    v
             Explanation
                    |
                    v
        Structured Response
```

The generated explanation should be grounded in retrieved evidence and deterministic rules.

---

# 23. AI/LLM Responsibility

The future generation model should:

* explain the rejection
* explain the applicable corrective path
* explain the grievance route
* explain deadlines using validated inputs
* cite supporting evidence
* communicate uncertainty
* abstain when evidence is insufficient

The LLM should NOT independently decide:

* entitlement
* official rejection validity
* policy constraints
* package/ranking rules
* grievance deadlines
* escalation rules

unless those decisions are explicitly represented in the deterministic rule system.

---

# 24. Bounded Agentic Workflow

A later project phase will introduce a bounded workflow.

The workflow may:

1. inspect available evidence
2. determine whether evidence is sufficient
3. retrieve additional evidence when necessary
4. perform one corrective retrieval/constraint relaxation if allowed
5. determine routing
6. generate an explanation
7. abstain if evidence remains insufficient
8. escalate to a human when necessary

The agent must operate inside predefined limits.

It should NOT be an unrestricted autonomous agent.

---

# 25. Abstention

Abstention is a core safety feature.

If the system cannot establish a reliable answer from:

* deterministic rules
* authoritative evidence
* validated inputs

then it should not invent an answer.

Instead:

```text
Insufficient evidence
        |
        v
Abstain / Human Escalation
```

This is preferable to a plausible but unsupported AI answer.

---

# 26. Citation and Evidence Tracing

Every generated explanation should eventually be traceable to supporting evidence.

The system should preserve information such as:

```text
Source
Document
Version
Page
Chunk
```

This allows an answer to be checked against the original authoritative document.

Future responses should therefore aim for:

```text
Claim
  |
  v
Rule
  |
  v
Evidence
  |
  v
Citation
```

---

# 27. Project Development Phases

## Phase 1 — Plain RAG

Goal:

Build a reliable retrieval and explanation pipeline.

Components:

```text
PDF
 ↓
Chunks
 ↓
Embeddings
 ↓
Vector Retrieval
 ↓
LLM Explanation
```

Use synthetic/constructed cases for testing.

---

## Phase 2 — Deterministic Rules

Add:

```text
Rule Database
+
Rule Validation
+
Structured Decision
```

Core principle:

> AI explains. Rules decide.

---

## Phase 3 — Bounded Agentic Workflow

Add:

* evidence sufficiency checking
* limited corrective retrieval
* constraint relaxation where explicitly permitted
* routing
* abstention
* human escalation
* structured trace

---

## Phase 4 — Real Data Personalization

Only after the earlier phases are stable should real-world data be introduced.

Real data should personalize or contextualize the system.

It must NOT override deterministic:

* policy rules
* entitlement rules
* package rules
* ranking rules
* deadline rules
* escalation rules

---

# 28. Evaluation Plan

The final system should be evaluated using multiple dimensions.

### Cause Accuracy

Did the system identify the correct rejection cause?

### Recourse Validity

Did it provide a valid corrective or grievance path?

### Gate Block Rate

How often did validation correctly block unsafe/incomplete decisions?

### Deadline Correctness

Did the system provide the correct deadline?

### Citation Validity

Can each explanation be traced to the correct evidence?

### Abstention Precision/Recall

Does the system abstain when it should, without abstaining unnecessarily?

### Human Plausibility

Do human reviewers consider the explanations understandable and supported?

### System Efficiency

Measure:

* latency
* token usage
* number of tool calls
* retries
* cost

---

# 29. Synthetic Data Policy

For Phases 1–3:

> Use synthetic or constructed expert-adjudicated cases.

This allows controlled testing without prematurely exposing the system to sensitive real-world data.

Real data is planned for Phase 4.

---

# 30. Important Safety/Accuracy Principles

The project must follow these principles:

1. Never invent official rejection codes.
2. Clearly label fictional/example rules as fictional.
3. Never allow the LLM to override deterministic policy.
4. Do not treat semantic similarity as factual correctness.
5. Preserve source metadata.
6. Preserve page-level traceability.
7. Validate rules before using them.
8. Abstain when evidence is insufficient.
9. Use human escalation for unresolved cases.
10. Keep authoritative documents separate from generated explanations.
11. Do not allow retrieved text to automatically become a policy decision.
12. Keep experimental/generated data separate from authoritative source material.

---

# 31. Current Progress

Completed:

* [x] Project selected
* [x] Project problem understood
* [x] AB-PMJAY grievance guideline identified
* [x] PDF added to repository
* [x] PDF text extraction
* [x] Page-aware chunking
* [x] Chunk cleaning
* [x] chunks.json created
* [x] Pretrained embedding model selected
* [x] Embedding generation tested
* [x] All chunks embedded
* [x] embedded_chunks.json created
* [x] Semantic similarity tested
* [x] Python-based vector retrieval implemented
* [x] Reusable retrieve() function implemented
* [x] Deterministic rule system created
* [x] Pydantic models introduced
* [x] Rule validation implemented
* [x] Safe failure implemented
* [x] Git/GitHub workflow established
* [x] PostgreSQL installed
* [x] PostgreSQL service running

---

# 32. Immediate Next Step

The next major technical step is:

## Install and configure pgvector

Then:

```text
embedded_chunks.json
        |
        v
PostgreSQL + pgvector
        |
        v
Vector database
        |
        v
Database-backed retrieval
```

After this works, the Python retrieval code can be changed from:

```text
JSON → Python → cosine similarity → sorting
```

to:

```text
PostgreSQL + pgvector → vector search → top-K chunks
```

The existing Python retrieval implementation should be kept until the PostgreSQL version is verified.

---

# 33. Git Checkpoint Philosophy

After completing a meaningful project milestone:

```bash
git status
git add .
git commit -m "Meaningful milestone message"
git push origin main
```

Commits should describe what was actually completed.

Examples:

```text
Add validated rule evaluation
```

```text
Add semantic chunk retrieval
```

Future commits should follow the same style.

---

# 34. Learning Style

The project is being built while learning AI from the basics.

When introducing a new technology:

1. Explain what it is.
2. Explain why the project needs it.
3. Show the smallest useful example.
4. Implement it in the project.
5. Test it.
6. Explain the output.
7. Commit the milestone.

Closely related coding steps can be bundled together to avoid unnecessary slowdown.

The explanation should remain beginner-friendly.

---

# 35. Current Mental Model

The most important mental model for the project is:

```text
                    ┌─────────────────┐
                    │      CLAIM      │
                    └────────┬────────┘
                             |
                 ┌───────────┴───────────┐
                 |                       |
                 v                       v
        ┌─────────────────┐     ┌─────────────────┐
        │  RULE DATABASE  │     │  KNOWLEDGE BASE │
        │                 │     │                 │
        │  Rules decide   │     │  RAG retrieves  │
        └────────┬────────┘     └────────┬────────┘
                 |                       |
                 └───────────┬───────────┘
                             |
                             v
                       ┌───────────┐
                       │ VALIDATION│
                       └─────┬─────┘
                             |
                             v
                       ┌───────────┐
                       │ AI / LLM  │
                       │ explains  │
                       └─────┬─────┘
                             |
                             v
                       ┌───────────┐
                       │ RESPONSE  │
                       └───────────┘
```

## Golden Rule

> **The AI should never become the authority merely because it sounds confident.**

The authority comes from validated deterministic rules and authoritative evidence.
