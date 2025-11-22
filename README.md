# front-end-ASIC-design-LMM-tool-using-RAG
Automated Front-End VLSI Design tool. Uses an LLM-RAG pipeline to transform high-level design specifications into PPA-optimized, synthesizable RTL IP blocks (Verilog/VHDL). Features an iterative verification loop for bug correction and quality assurance.
# 🤖 Automated Front-End VLSI Design AI Tool using LLM RAG

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository hosts a cutting-edge, end-to-end AI tool that automates the front-end VLSI (Very Large-Scale Integration) design flow. It utilizes a **Retrieval-Augmented Generation (RAG) pipeline** powered by a Large Language Model (LLM) to convert high-level functional specifications into **synthesizable, PPA-optimized Register-Transfer Level (RTL) IP blocks** with a closed-loop verification process.

## ✨ Key Features

* **Spec-to-RTL Generation:** Automatically translates natural language specifications (architecture, functional requirements, protocols) into Verilog/VHDL code, including complex Finite State Machines (FSMs) and Testbenches (TB).
* **PPA Optimization:** The LLM is conditioned to generate RTL focused on achieving the best balance of **Power, Performance, and Area (PPA)** efficiency.
* **Verification-in-the-Loop:** Simulation results (waveforms, coverage logs) are fed back to the LLM to **iteratively correct and refine** the generated RTL until it fully matches the specification.
* **Contextual Accuracy (RAG):** The **RAG engine** grounds the generation by retrieving relevant information from a dedicated **Knowledge Base** (RTL libraries, protocols, reference guides), significantly reducing LLM "hallucinations."
* **Web Interface:** A user-friendly React frontend for file upload, parameter configuration, execution, and output visualization.

***

## 💡 VLSI Design Flow (RAG Pipeline)

The system operates in a continuous, iterative loop to ensure functional correctness and quality standards. 

| Step | Component | Description |
| :--- | :--- | :--- |
| **1. Input & Parsing** | **NLP Parser** (`file_parser.py`) | Upload specification documents and use NLP to extract structured constraints. |
| **2. Retrieval** | **RAG Engine** (`rag_service.py`) | Query the **Knowledge DB** (`vector_db/`) to retrieve relevant golden RTL and reference protocols. |
| **3. Generation** | **LLM Spec-to-RTL** (`rtl_generator.py`) | LLM generates **RTL (Verilog/VHDL)** and **Testbench/VIP** focused on **PPA efficiency**. |
| **4. Verification** | **Post-Processing & Sim** | RTL is checked (Lint, Synthesis Check, STA, CDC) and simulated (UVM, FV). Generates **Waveforms** and **Coverage Logs**. |
| **5. Correction** | **Iterative Loop** | **Verification results are fed back** to the LLM for automated bug correction until spec match is achieved. |
| **6. Final Output** | **Synthesizable IP** | The stable, verified, and PPA-optimized **Synthesizable RTL IP block** is produced. |

***

Markdown

# 🤖 Automated Front-End VLSI Design AI Tool using LLM RAG

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository hosts a cutting-edge, end-to-end AI tool that automates the front-end VLSI (Very Large-Scale Integration) design flow. It utilizes a **Retrieval-Augmented Generation (RAG) pipeline** powered by a Large Language Model (LLM) to convert high-level functional specifications into **synthesizable, PPA-optimized Register-Transfer Level (RTL) IP blocks** with a closed-loop verification process.

## ✨ Key Features

* **Spec-to-RTL Generation:** Automatically translates natural language specifications (architecture, functional requirements, protocols) into Verilog/VHDL code, including complex Finite State Machines (FSMs) and Testbenches (TB).
* **PPA Optimization:** The LLM is conditioned to generate RTL focused on achieving the best balance of **Power, Performance, and Area (PPA)** efficiency.
* **Verification-in-the-Loop:** Simulation results (waveforms, coverage logs) are fed back to the LLM to **iteratively correct and refine** the generated RTL until it fully matches the specification.
* **Contextual Accuracy (RAG):** The **RAG engine** grounds the generation by retrieving relevant information from a dedicated **Knowledge Base** (RTL libraries, protocols, reference guides), significantly reducing LLM "hallucinations."
* **Web Interface:** A user-friendly React frontend for file upload, parameter configuration, execution, and output visualization.

***

## 💡 VLSI Design Flow (RAG Pipeline)

The system operates in a continuous, iterative loop to ensure functional correctness and quality standards. 

| Step | Component | Description |
| :--- | :--- | :--- |
| **1. Input & Parsing** | **NLP Parser** (`file_parser.py`) | Upload specification documents and use NLP to extract structured constraints. |
| **2. Retrieval** | **RAG Engine** (`rag_service.py`) | Query the **Knowledge DB** (`vector_db/`) to retrieve relevant golden RTL and reference protocols. |
| **3. Generation** | **LLM Spec-to-RTL** (`rtl_generator.py`) | LLM generates **RTL (Verilog/VHDL)** and **Testbench/VIP** focused on **PPA efficiency**. |
| **4. Verification** | **Post-Processing & Sim** | RTL is checked (Lint, Synthesis Check, STA, CDC) and simulated (UVM, FV). Generates **Waveforms** and **Coverage Logs**. |
| **5. Correction** | **Iterative Loop** | **Verification results are fed back** to the LLM for automated bug correction until spec match is achieved. |
| **6. Final Output** | **Synthesizable IP** | The stable, verified, and PPA-optimized **Synthesizable RTL IP block** is produced. |

***

## 📁 Repository Structure

The project is a full-stack application with a Python/FastAPI backend, a dedicated RAG knowledge base, and a React/Vite frontend.

front-end-ASIC-design-LMM-tool-using-RAG/ ├── README.md # This file ├── requirements.txt

├── .env.example # Template for environment variables ├── docker-compose.yml # Containerized setup for the stack | ├── backend/ # FastAPI backend API (LLM and Verification orchestration) │ └── app/ │ ├── services/ # Core business logic │ │ ├── rag_service.py # Vector DB/Retrieval interface │ │ ├── llm_service.py # LLM communication wrapper │ │ ├── rtl_generator.py # Main generation and correction logic │ │ └── vip_generator.py # Verification IP generation │ └── utils/ │ ├── file_parser.py # NLP-based specification extraction │ └── prompts.py # LLM prompt templates | ├── knowledge_base/ # External information for RAG │ ├── specs/ # Reference design specifications │ ├── protocols/ # Protocol documents (e.g., AXI, I2C, UART) │ └── vector_db/ # Stored vector embeddings (ignored via .gitignore) | └── frontend/ # React/Vite web interface └── src/ └── pages/ # Main application views (Upload, Generate, Outputs) | └── examples/ # Reference examples ├── axi4_lite/ # Example files for AXI4-Lite generation └── uart/ # Example files for UART generation

***

## 🚀 Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/OWNER/front-end-ASIC-design-LMM-tool-using-RAG.git](https://github.com/OWNER/front-end-ASIC-design-LMM-tool-using-RAG.git)
    cd front-end-ASIC-design-LMM-tool-using-RAG
    ```
2.  **Setup Environment Variables:**
    ```bash
    cp .env.example .env
    # Edit the .env file with your LLM API key (e.g., GEMINI_API_KEY=...)
    ```
3.  **Run with Docker (Recommended):**
    ```bash
    # Build and run the entire stack (backend, frontend, vector db)
    docker-compose up --build
    ```

The application will be accessible at `http://localhost:3000`.



## 📁 Repository Structure

The project is a full-stack application with a Python/FastAPI backend, a dedicated RAG knowledge base, and a React/Vite frontend.
