# 🏦 PRA-I: COREP Reporting Assistant

**PRA-I** (PRA Intelligence) is an AI-powered regulatory reporting assistant designed for UK Banks subject to the PRA Rulebook. It automates the interpretation of complex **COREP (Common Reporting)** templates using a Hybrid AI Architecture.

## 🚀 Key Capabilities

### 1. Hybrid Intelligence Engine
* **Privacy-First Logic:** Support for **Local Llama 3.1** (via Ollama) for strict regulatory reasoning and sensitive data handling.
* **Cloud Power:** Seamless fallback to **Gemini 1.5 Flash** for high-speed document retrieval and complex summarization.

### 2. Dynamic Context Switching
The system automatically detects the reporting context and switches its logic engine:
* **Credit Risk Mode:** Enforces **Standardised Approach** rules (e.g., SME < €1m = Retail Class, Mortgage < 80% LTV = Secured Class).
* **Liquidity Mode (LCR):** Enforces **HQLA Haircuts** (e.g., Level 2B Corporate Bonds = 50% Haircut).

### 3. Hallucination Guardrails
* **Chain-of-Thought (CoT) Prompting:** Forces the AI to validate thresholds (e.g., "Is 70 days > 90 days?") before assigning a risk weight.
* **Negative Constraints:** Explicitly prevents the recommendation of IRB templates for Standardised banks.

## 🌐 Deployment Architecture

We offer two deployment modes to balance **Accessibility** vs. **Data Privacy**:

### Option A: Cloud-Native (Public Demo)
* **Host:** Streamlit Community Cloud
* **AI Backend:** Google Gemini 1.5 Flash
* **Use Case:** Instant access, high availability, no setup required.
* **Live Link:** https://pra-i-corep-reporting-assistant-hueujpnvs7ydtgzuhwp56h.streamlit.app

### Option B: Secure Local Tunnel (Privacy Mode via ngrok)
* **Host:** On-Premise / Local Laptop
* **AI Backend:** Llama 3.1 (8B) running locally via Ollama.
* **Role of ngrok:** We use **ngrok** to securely tunnel the local "Privacy-First" version of the app to external stakeholders without uploading sensitive data to the cloud.

#### 🔧 How to Run via ngrok
This allows you to run the app on your secure machine (using local Llama) but share a URL with your team.

1.  **Start Ollama (Locally):**
    Ensure your local LLM is running:
    ```bash
    ollama run llama3.1
    ```

2.  **Start the App (Locally):**
    Open a terminal in the project folder and run:
    ```bash
    streamlit run app.py
    ```
    *The app will launch at `http://localhost:8501`*

3.  **Open the Tunnel:**
    Open a **second** terminal window in the project folder (where `ngrok.exe` is located) and run:
    ```bash
    ngrok http 8501
    ```

4.  **Access:**
    Copy the "Forwarding" URL provided by ngrok (e.g., `https://a1b2-c3d4.ngrok-free.app`). Anyone with this link can access your local, private PRA-I instance.

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Custom "Dark Mode" UI)
* **Orchestration:** LangChain
* **Vector Database:** ChromaDB (Local Persistence)
* **Infrastructure:** Streamlit Cloud / ngrok
* **LLMs:** Meta Llama 3.1 (Local) + Google Gemini 1.5 Flash (Cloud)

## 🧪 Benchmark Success

| Test Scenario | Result | Status |
| :--- | :--- | :--- |
| **SME Threshold** | Correctly identified SME <€1m as **Retail (75% RW)**. | ✅ PASSED |
| **Mortgage Collateral** | Correctly identified Residential Collateral as **Secured (35% RW)**. | ✅ PASSED |
| **LCR Equities** | Correctly classified Euro Stoxx 50 shares as **Level 2B (50% Haircut)**. | ✅ PASSED |

---
