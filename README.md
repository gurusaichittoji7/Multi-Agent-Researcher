# 🤖 Multi-Agent Research Loop (Human-in-the-Loop)

An autonomous research system built with **LangGraph** and **Streamlit** that coordinates specialized agents to perform deep-dive web research with human oversight.

## 🌟 Key Features
- **Stateful Orchestration:** Managed via a centralized `AgentState` using LangGraph to handle transitions between Planning, Researching, and Writing.
- **Interactive UI:** A Streamlit dashboard that allows real-time monitoring of agent progress.
- **Human-in-the-Loop (HITL):** A safety "Interrupt" mechanism that pauses execution after the planning phase, requiring human approval before the agent spends tokens/resources on search.
- **Intent-Based Routing:** Features a logic gate that switches between **Tavily (Web Search)** and a specialized **Vision/Style Mode** (integration-ready for Looksy) based on query context.
- **Memory Persistence:** Uses `MemorySaver` to maintain thread-specific history, allowing for session recovery.

## 🏗️ Architecture
The system consists of three primary nodes:
1. **The Planner:** Analyzes the topic and generates a multi-step research strategy.
2. **The Researcher:** Executes the plan using the Tavily API or specialized vision tools.
3. **The Writer:** Synthesizes gathered data into a structured markdown report.

## 🛠️ Tech Stack
- **Orchestration:** LangGraph
- **Frontend:** Streamlit
- **LLM:** OpenAI GPT-4o / GPT-4o-mini
- **Search Engine:** Tavily API
- **Environment:** Python 3.10+

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Multi-Agent-Researcher.git
   cd Multi-Agent-Researcher
   ```

2. **Setup Environment:**
   Create a `.env` file with your credentials:
   ```env
   OPENAI_API_KEY=sk-your-key
   TAVILY_API_KEY=tvly-your-key
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Dashboard:**
   ```bash
   streamlit run app.py
   ```