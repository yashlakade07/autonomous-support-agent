# Autonomous Support Agent 🤖⚒️

A production-ready, multi-agent support system built with **LangGraph**, **FastAPI**, and **Ollama**. This project demonstrates an agentic workflow that triages customer tickets, retrieves CRM context via **MCP**, and decides whether to resolve an issue or escalate it to a human.

## 🌟 Key Features
* **Stateful Orchestration:** Uses LangGraph to manage complex decision-making loops.
* **Local LLM Integration:** Powered by **Qwen 2.5:7b** via Ollama for data privacy and low latency.
* **Decoupled Tools (MCP):** Uses the Model Context Protocol (MCP) to interact with a CRM/Database, ensuring secure and scalable tool usage.
* **Microservices Architecture:** Fully containerized using Docker (FastAPI, Streamlit, and MCP Server).
* **Intelligent Routing:** Automatically detects sentiment and intent to handle routine tasks or escalate high-risk tickets.

---

## 🏗️ Architecture
The system is divided into three main services:
1.  **FastAPI Backend:** The brain that executes the LangGraph workflow.
2.  **MCP Server:** A tool provider that handles CRM data retrieval and ticket updates.
3.  **Streamlit UI:** A user-friendly dashboard for simulation and monitoring.

---

## 🚀 Getting Started

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Ollama](https://ollama.com/) installed and running on your host machine.

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/autonomous-support-agent.git](https://github.com/YOUR_USERNAME/autonomous-support-agent.git)
   cd autonomous-support-agent

2. **Pull the required model:**
   ```bash
   ollama pull qwen2.5:7b

3. **Launch the stack:**
   ```bash
   docker-compose up --build

4. **Access the Application:**
   *Frontend UI: http://localhost:8501
   *API Docs: http://localhost:8000/docs

🛠️ Technical Stack
Orchestration: LangGraph

LLM Interface: LangChain / Ollama

API Framework: FastAPI

Interface: Streamlit

Containerization: Docker & Docker Compose

Database Tooling: MCP (Model Context Protocol)

📖 How it Works
Triage: The system analyzes the user's message and fetches customer context from the MCP server.

Route: If the message is a routine query, it moves to the Resolution Agent. If it's aggressive or complex, it moves to the Escalation Agent.

Execute: The chosen agent performs the action (generating a response or flagging for a manager) and updates the ticket status via the MCP toolset.

## 📂 Project Structure

```bash
autonomous-support-agent/
│── backend/          # FastAPI + LangGraph workflow
│── frontend/         # Streamlit dashboard
│── mcp_server/       # CRM tool server
│── docker-compose.yml
│── requirements.txt
│── README.md

<img width="1536" height="1024" alt="ChatGPT Image May 18, 2026, 12_55_45 PM" src="https://github.com/user-attachments/assets/d471a52e-0f0c-425e-8761-49fc0a804fac" />
