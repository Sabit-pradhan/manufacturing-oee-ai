# Manufacturing OEE Monitoring & AI Analytics System

An end-to-end manufacturing analytics application that combines Overall
Equipment Effectiveness (OEE) reporting, machine anomaly detection,
data-quality analysis, and a retrieval-augmented AI Copilot.

> **Project status:** Portfolio / demonstration application\
> **Data status:** The manufacturing dataset used in this project is
> synthetic. OEE and anomaly results should be treated as provisional
> analytical outputs, not verified live-factory measurements.

------------------------------------------------------------------------

## 1. Project Overview

Manufacturing operations generate data from machines, production counts,
quality inspections, shifts, and machine-state events. Reviewing these
sources separately makes it difficult for production teams to understand
equipment performance, identify unusual behaviour, and investigate
operational questions.

This project brings those data sources together in one application. It
provides:

-   A dashboard for viewing manufacturing and machine performance.
-   OEE calculations using Availability, Performance, and Quality.
-   Machine-level and production-line reporting.
-   Anomaly detection using an Isolation Forest implementation.
-   Data-quality issue summaries.
-   A document-based RAG pipeline that retrieves relevant project and
    manufacturing documentation.
-   An AI Copilot that combines retrieved documentation with available
    manufacturing analytics and generates natural-language responses.

The application uses a Next.js frontend, a FastAPI backend, PostgreSQL
with pgvector, and locally hosted Ollama models.

## 2. Main Objectives

1.  Consolidate manufacturing reference data and operational records in
    PostgreSQL.
2.  Calculate OEE metrics from production, quality, shift, and
    machine-state data.
3.  Present machine and production performance through a dashboard.
4.  identify statistically unusual machine observations and data-quality
    issues.
5.  Allow users to ask questions in natural language through an AI
    Copilot.
6.  Ground Copilot answers in retrieved documentation and the analytics
    exposed by the backend.

## 3. Technology Stack

  -----------------------------------------------------------------------
  Layer                   Technology              Responsibility
  ----------------------- ----------------------- -----------------------
  Frontend                Next.js, React,         Dashboard and Copilot
                          TypeScript              interface

  Backend                 Python, FastAPI         REST APIs and
                                                  application logic

  Database                PostgreSQL              Manufacturing and
                                                  application data

  Vector search           pgvector                Similarity search over
                                                  document embeddings

  Embeddings              Ollama                  Convert text into
                          `nomic-embed-text`      vectors

  LLM                     Ollama `llama3.1`       Generate Copilot
                                                  responses

  Anomaly detection       Isolation Forest        Identify statistically
                                                  unusual observations

  Data processing         Python, Pandas,         Data loading and
                          SQLAlchemy              analytics

  API documentation       FastAPI Swagger UI      Explore backend
                                                  endpoints
  -----------------------------------------------------------------------

The embedding model used in the current implementation returns
768-dimensional vectors. The `document_chunks.embedding` column is
configured as `VECTOR(768)`.

## 4. High-Level Architecture

``` text
                         USER
                           |
                           v
                Next.js / React Dashboard
                 |                    |
                 |                    |
          OEE & Anomaly UI        AI Copilot Chat
                 |                    |
                 +---------+----------+
                           |
                           v
                    FastAPI Backend
                           |
             +-------------+--------------+
             |             |              |
             v             v              v
        OEE Services  Anomaly Services  Copilot Service
             |             |              |
             |             |        +-----+------+
             |             |        |            |
             v             v        v            v
        PostgreSQL     Isolation   pgvector    Ollama
        Manufacturing  Forest      Retrieval   LLM
        Tables         and Data    and RAG      llama3.1
                       Quality
```

### Request flow

**Dashboard analytics**

1.  The user opens the dashboard.
2.  The frontend requests data from FastAPI.
3.  The API calls the relevant OEE or anomaly service.
4.  Services query PostgreSQL and calculate or retrieve the required
    metrics.
5.  The API returns structured data to the frontend.

**AI Copilot**

1.  The user submits a question in the Copilot interface.
2.  The backend creates an embedding using `nomic-embed-text`.
3.  pgvector searches the `document_chunks` table for semantically
    similar content.
4.  The analytics service determines whether the question matches
    supported manufacturing analytics categories.
5.  Relevant document context and available analytics are assembled into
    the LLM prompt.
6.  Ollama runs `llama3.1` to generate a natural-language answer.
7.  The API returns the answer, retrieved sources, and analytics context
    to the frontend.

The analytics routing is based on implemented question-category and
keyword rules. It is not an unrestricted natural-language-to-SQL agent.

## 5. Dataset and Data Model

The project uses a synthetic manufacturing dataset covering 90 days,
from **2026-01-01 to 2026-03-31**.

### Dataset scale

  Dataset item                       Quantity
  -------------------------------- ----------
  Plant                                     1
  Production lines                          5
  Machines                                 30
  Products                                 20
  Shift records                           270
  Production orders                   154,168
  Production count records            491,156
  Quality inspection records          491,156
  Canonical machine-state events       95,662

The data loader reported approximately **1,232,468 inserted rows**
across the listed datasets.

### Production shifts

Three shifts are represented:

-   Shift A: 06:00--14:00
-   Shift B: 14:00--22:00
-   Shift C: 22:00--06:00

### Main database tables

  Table                   Purpose
  ----------------------- -------------------------------------------
  `plants`                Plant reference information
  `production_lines`      Production-line reference information
  `machines`              Machine master data and line association
  `products`              Product reference information
  `shifts`                Shift dates, codes, and timings
  `production_orders`     Production-order records
  `production_counts`     Production and count records
  `quality_inspections`   Quality inspection records
  `state_events`          Canonical machine-state events
  `document_chunks`       Text chunks and vector embeddings for RAG

The `document_chunks` table stores the document name, document type,
chunk index, text content, embedding, metadata, and creation timestamp.

## 6. OEE Analytics

Overall Equipment Effectiveness (OEE) is calculated from three
components:

\[ OEE = Availability `\times `{=tex}Performance `\times `{=tex}Quality
\]

The three components are expressed as ratios between 0 and 1 during
calculation. They may be displayed as percentages in the dashboard.

### Availability

\[ Availability =
`\frac{Operating\ Time}{Planned\ Production\ Time}`{=tex} \]

Availability represents the portion of planned production time during
which the machine was operating.

### Performance

\[ Performance =
`\frac{Ideal\ Cycle\ Time \times Total\ Count}{Operating\ Time}`{=tex}
\]

Performance compares actual production speed with the configured ideal
cycle time.

### Quality

\[ Quality = `\frac{Good\ Count}{Total\ Count}`{=tex} \]

Quality represents the proportion of produced units classified as good.

### OEE implementation notes

The OEE services calculate machine-level results and provide daily,
shift, and production-line reporting. Downtime event intervals are
clipped to the shift window, overlapping intervals are merged, and
planned breaks are excluded from planned production time.

The current calculation has important limitations:

-   Source machine-state events are sampled and do not form a continuous
    timeline.
-   Ideal cycle times have not been calibrated against each machine.
-   Count corrections are excluded because reliable linkage is not
    available.
-   Changeover time is excluded from downtime.
-   Overlapping RUN intervals were resolved in the canonical event
    dataset.

For these reasons, the OEE values are provisional and should not be
presented as certified factory KPIs.

## 7. Machine Anomaly Detection

The application includes an Isolation Forest-based anomaly detection
service.

Isolation Forest is an unsupervised machine-learning algorithm. It
isolates observations by recursively partitioning feature space.
Observations that are easier to isolate can be flagged as unusual
relative to the data distribution.

The backend exposes anomaly functionality through the anomaly API:

-   Summary of machine anomaly results.
-   Anomaly results for a specified machine.
-   Data-quality issue summary and records.

An anomaly is a statistically unusual observation. It does **not**
automatically mean that a machine has failed or that a specific
component is defective.

The project also has a separate data-quality analysis service. This is
important because unusual records can arise from incomplete,
inconsistent, duplicated, or otherwise problematic source data.

## 8. AI Copilot and RAG

The Copilot combines document retrieval with manufacturing analytics.

### Document ingestion

The document pipeline supports:

-   PDF
-   DOCX
-   TXT
-   Markdown

The current chunking implementation uses a default chunk size of 1,000
characters and an overlap of 150 characters. Each chunk is embedded and
stored in PostgreSQL through pgvector.

### Embedding generation

Ollama runs `nomic-embed-text` to create 768-dimensional embeddings. The
backend validates the embedding dimension before storing or querying
vectors.

### Vector retrieval

The retrieval service embeds the user's question and performs
cosine-distance similarity search against `document_chunks`.

The most relevant chunks are selected and included as supporting context
for the answer.

### LLM response generation

Ollama runs `llama3.1` to generate a response using the retrieved
documents and available analytics context.

### Hybrid analytics

The analytics service connects Copilot questions to existing backend
services. Implemented categories include:

-   Machine and daily OEE
-   Availability, performance, quality, and downtime
-   Production-line OEE
-   Shift OEE
-   Machine-to-line mapping
-   Isolation Forest anomaly insights
-   Data-quality findings

The Copilot can use the resulting analytics context to explain available
results in natural language. Its routing is currently rule/keyword
based, so a question outside the supported categories may rely primarily
on document retrieval.

### Maintenance recommendations

The Copilot prompt is designed to provide advisory maintenance
suggestions based on available anomaly and operational context. These
are recommendations generated by the LLM, not validated maintenance
diagnoses or predictions from a separately trained
predictive-maintenance model.

### RAG limitations

-   Answers depend on the quality and coverage of ingested documents.
-   Similarity retrieval can return related but not fully relevant
    chunks.
-   The LLM can still generate incorrect statements; answers should be
    reviewed for important operational decisions.
-   Analytics coverage depends on the question-routing rules and the
    backend services available for that category.
-   The current implementation should not be described as an autonomous
    industrial control system.

## 9. Backend API

The FastAPI application exposes the following implemented routes.

  -------------------------------------------------------------------------------------------------
  Method                  Endpoint                                          Purpose
  ----------------------- ------------------------------------------------- -----------------------
  GET                     `/health`                                         Backend health endpoint

  GET                     `/docs`                                           Interactive Swagger API
                                                                            documentation

  GET                     `/api/v1/oee/shift/{shift_id}`                    Shift-level OEE report

  GET                     `/api/v1/oee/daily/{report_date}`                 Daily OEE report

  GET                     `/api/v1/oee/trend?start_date=...&end_date=...`   OEE trend for a date
                                                                            range

  GET                     `/api/v1/anomalies/summary`                       Anomaly and
                                                                            data-quality summary

  GET                     `/api/v1/anomalies/machine/{machine_id}`          Anomalies for a machine

  GET                     `/api/v1/anomalies/data-quality`                  Data-quality issue
                                                                            records

  POST                    `/api/v1/copilot/ask`                             Ask the manufacturing
                                                                            AI Copilot
  -------------------------------------------------------------------------------------------------

The Copilot request accepts a question and an optional `top_k` value
controlling the number of document chunks retrieved. The default is 3.

## 10. Frontend

The Next.js dashboard provides a dark industrial / SCADA-style
interface.

The project includes:

-   Manufacturing overview and OEE dashboard.
-   Machine overview showing the 30 machines.
-   Production-line and machine performance views.
-   Anomaly and data-quality information.
-   AI Copilot chat interface with answers and retrieved document
    sources.

The Copilot frontend sends a POST request to `/api/v1/copilot/ask` and
displays the returned answer and source information.

## 11. Project Folder Structure

The following is the main structure discussed and implemented during
development. Individual files may have additional modules.

``` text
manufacturing-oee-ai/
├── backend/
│   ├── app/
│   │   ├── ai_copilot/
│   │   │   ├── document_loader.py
│   │   │   ├── chunking_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── document_ingestion_service.py
│   │   │   ├── retrieval_service.py
│   │   │   ├── rag_service.py
│   │   │   └── analytics_service.py
│   │   ├── anomaly_detection/
│   │   │   ├── anomaly_service.py
│   │   │   └── data_quality_service.py
│   │   ├── api/
│   │   │   ├── oee_routes.py
│   │   │   ├── anomaly_routes.py
│   │   │   └── copilot.py
│   │   ├── data_generation/
│   │   │   └── database_loader.py
│   │   ├── database/
│   │   │   └── connection.py
│   │   ├── models/
│   │   └── services/
│   │       ├── oee_service.py
│   │       ├── oee_reporting_service.py
│   │       ├── daily_oee_service.py
│   │       ├── oee_trend_service.py
│   │       └── line_oee_service.py
│   ├── create_tables.py
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   └── CopilotChat.tsx
│   │   └── lib/
│   │       └── api.ts
│   └── .env.local
└── data/
    └── processed/
```

## 12. Running the Project Locally

### Prerequisites

-   Python installed
-   Node.js and npm installed
-   PostgreSQL installed and running
-   Ollama installed and running
-   Required Ollama models available locally

The models used by this implementation are:

``` powershell
ollama pull nomic-embed-text
ollama pull llama3.1
```

### Backend setup

Open PowerShell:

``` powershell
cd "C:\Users\asus\Desktop\manufacturing-oee-ai\manufacturing-oee-ai\backend"
```

Activate the backend virtual environment:

``` powershell
.\venv\Scripts\Activate.ps1
```

Start FastAPI:

``` powershell
python -m uvicorn app.main:app --reload
```

Alternatively, use the backend interpreter directly:

``` powershell
& ".\venv\Scripts\python.exe" -m uvicorn app.main:app --reload
```

Backend:

-   API base URL: `http://127.0.0.1:8000`
-   Swagger UI: `http://127.0.0.1:8000/docs`
-   Health endpoint: `http://127.0.0.1:8000/health`

### Frontend setup

Open a second PowerShell terminal:

``` powershell
cd "C:\Users\asus\Desktop\manufacturing-oee-ai\manufacturing-oee-ai\frontend"
npm run dev
```

Frontend:

``` text
http://localhost:3000
```

The frontend `.env.local` should contain:

``` env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### Database configuration

The backend `.env` should contain the PostgreSQL connection settings:

``` env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=manufacturing_oee_db
DB_USER=postgres
DB_PASSWORD=YOUR_LOCAL_POSTGRES_PASSWORD
```

Use the actual local password in the local `.env` file. Do not commit
credentials to Git.

## 13. Database Initialization and Data Loading

The schema creation and dataset loading were completed during
development.

Schema creation command:

``` powershell
python create_tables.py
```

Dataset loader command:

``` powershell
python -m app.data_generation.database_loader
```

**Important:** The loader previously used INSERT operations. Do not run
it repeatedly against the same populated database unless the loader has
been made idempotent or the target tables have been intentionally reset.
Re-running it may duplicate records.

The vector table is separate from the manufacturing tables. Existing
document chunks should not be deleted or recreated unless intentionally
re-ingesting documents.

## 14. Current Implementation Status

Based on the development work recorded for this project:

  -----------------------------------------------------------------------
  Area                                Recorded status
  ----------------------------------- -----------------------------------
  Project setup and architecture      Implemented

  PostgreSQL schema                   Created

  Manufacturing data ingestion        Completed

  OEE services and API routes         Implemented

  Machine and line analytics          Implemented

  Isolation Forest anomaly service    Existing implementation

  Data-quality analysis               Existing implementation

  FastAPI application                 Implemented

  Next.js SCADA dashboard             Implemented

  30-machine dashboard overview       Added and user confirmed visible

  Document loading and chunking       Implemented

  Ollama embeddings                   Implemented

  pgvector document retrieval         Implemented and previously
                                      demonstrated

  Document-based RAG Copilot          Previously demonstrated working

  Hybrid analytics context            Code implemented

  Anomaly explanation / maintenance   Code supplied; final end-to-end
  prompt                              confirmation not recorded

  Project README                      This document
  -----------------------------------------------------------------------

This status table distinguishes features that were previously
demonstrated from code that was supplied but not confirmed end-to-end.

## 15. Known Limitations and Responsible Interpretation

This is a portfolio and demonstration application built with synthetic
data. Important limitations include:

1.  **Synthetic data:** The dataset does not represent a verified live
    factory.
2.  **Sampled machine events:** State events are not a continuous sensor
    stream.
3.  **OEE calibration:** Ideal cycle times are not machine-calibrated.
4.  **Count corrections:** Corrections are excluded pending reliable
    record linkage.
5.  **Changeovers:** Changeover time is excluded from downtime
    calculations.
6.  **Anomaly interpretation:** Isolation Forest flags unusual
    observations; it does not prove a fault.
7.  **Maintenance advice:** LLM recommendations are advisory and require
    human review.
8.  **Copilot routing:** Analytics selection uses implemented
    keyword/category rules rather than unrestricted NL-to-SQL.
9.  **LLM reliability:** Generated answers can be inaccurate and should
    be checked before operational use.
10. **Deployment:** The project is intended to run locally. Docker,
    cloud deployment, and production monitoring are outside the current
    scope.

## 16. Future Enhancements (Optional)

These are possible future improvements, not features claimed as
completed:

-   Connect live PLC, SCADA, or IoT sensor feeds.
-   Calibrate ideal cycle times for each machine and product.
-   Establish validated downtime and changeover classifications.
-   Link count corrections to their original production records.
-   Add role-based access control and audit trails.
-   Add automated RAG evaluation with a curated question-and-answer
    dataset.
-   Add feedback capture for Copilot answer quality.
-   Add validated predictive-maintenance models using labelled failure
    history.
-   Add scheduled data refresh and operational alerting.

## 17. Interview Explanation

### Short project introduction

"I developed a Manufacturing OEE Monitoring and AI Analytics System to
bring production performance, machine anomalies, and manufacturing
documentation into one application.

On the backend, I used Python and FastAPI, with PostgreSQL for
manufacturing data. I implemented OEE calculations covering
Availability, Performance, and Quality, with machine-level, shift-level,
daily, and production-line reporting.

For anomaly detection, I integrated an Isolation Forest-based service
and separate data-quality analysis. On the frontend, I used Next.js and
React to build a dark industrial SCADA-style dashboard that includes an
overview of 30 machines.

I also developed an AI Copilot using a RAG architecture. Documents are
loaded, split into chunks, embedded using Ollama's `nomic-embed-text`,
and stored in PostgreSQL using pgvector. When a user asks a question,
the system retrieves relevant document chunks and combines them with
supported manufacturing analytics. Ollama's `llama3.1` then generates a
natural-language response with supporting sources.

The current project uses synthetic manufacturing data, so I describe its
OEE and anomaly outputs as demonstration results rather than validated
live factory measurements."

### Key technical points to explain

-   **Why PostgreSQL?** It stores structured manufacturing records and
    works with pgvector for vector similarity search.
-   **Why pgvector?** It allows document embeddings to be stored and
    searched alongside relational application data.
-   **Why RAG?** It grounds generated responses in relevant project
    documentation rather than relying only on the LLM's general
    knowledge.
-   **Why Ollama?** It allows the embedding and language models to run
    locally.
-   **Why Isolation Forest?** It provides an unsupervised approach for
    identifying unusual observations when labelled failure data is not
    available.
-   **How is OEE calculated?** Multiply Availability, Performance, and
    Quality ratios.
-   **Does an anomaly mean machine failure?** No. It indicates an
    unusual observation that requires investigation.
-   **Is the Copilot an autonomous maintenance system?** No. It provides
    explanations and advisory recommendations for human review.

------------------------------------------------------------------------


