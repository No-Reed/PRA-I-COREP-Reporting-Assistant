# 🏦 PRA-I: COREP Reporting Assistant

**PRA-I** is an AI-powered regulatory reporting assistant designed for UK Banks subject to the PRA Rulebook. It automates the interpretation of complex **COREP (Common Reporting)** templates using a Hybrid AI Architecture.

## 🚀 Key Capabilities

### 1. Hybrid Intelligence Engine
* **Privacy-First Logic:** Uses a **Local Llama 3.1** model (simulated via Ollama) for strict regulatory reasoning and sensitive data handling.
* **Cloud retrieval:** Uses **Gemini 1.5 Flash** for high-speed document retrieval and summarization.

### 2. Dynamic Context Switching
The system automatically detects the reporting context and switches its logic engine:
* **Credit Risk Mode:** Enforces **Standardised Approach** rules (e.g., SME < €1m = Retail Class, Mortgage < 80% LTV = Secured Class).
* **Liquidity Mode (LCR):** Enforces **HQLA Haircuts** (e.g., Level 2B Corporate Bonds = 50% Haircut, Major Index Equities = Level 2B).

### 3. Hallucination Guardrails
* **Chain-of-Thought (CoT) Prompting:** Forces the AI to validate thresholds (e.g., "Is 70 days > 90 days?") before assigning a risk weight.
* **Negative Constraints:** Explicitly prevents the recommendation of IRB templates for Standardised banks.

## 🛠️ Technical Architecture

* **Frontend:** Streamlit (Custom "Dark Mode" UI)
* **Database:** ChromaDB (Vector Store for RAG)
* **Orchestration:** LangChain
* **Source Data:** Automatically ingests PRA Rulebook & Annex II Reporting Instructions via Cloud Links.

## 🧪 Benchmark Success

| Test Scenario | Result | Status |
| :--- | :--- | :--- |
| **SME Threshold** | Correctly identified SME <€1m as **Retail (75% RW)**. | ✅ PASSED |
| **Mortgage Collateral** | Correctly identified Residential Collateral as **Secured (35% RW)**. | ✅ PASSED |
| **LCR Equities** | Correctly classified Euro Stoxx 50 shares as **Level 2B (50% Haircut)**. | ✅ PASSED |

## 📦 Deployment

This project is deployed on **Railway**.
* **Live Demo:** [Insert your Railway Link Here]
* **Note:** The cloud deployment uses Google Gemini for all inference to ensure stability.

---