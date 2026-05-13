import os
from typing import TypedDict, List
from dotenv import load_dotenv

# LangGraph and LangChain imports
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

load_dotenv()

# 1. Define the 'State' - this is the shared notepad
class AgentState(TypedDict):
    topic: str
    plan: str
    research_notes: List[str]
    report: str

# 2. Initialize our "Workers"
llm = ChatOpenAI(model="gpt-4o-mini")
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# 3. Define Agent Nodes
def planner(state: AgentState):
    print("---PLANNING PHASE---")
    prompt = f"Write a 3-step search plan for the topic: {state['topic']}. Be specific."
    response = llm.invoke(prompt)
    return {"plan": response.content}

def researcher(state: AgentState):
    print("---RESEARCHING PHASE---")
    
    # Check the topic or the plan for keywords
    topic_lower = state['topic'].lower()
    
    if "style" in topic_lower or "clothes" in topic_lower or "fashion" in topic_lower:
        print("\n[AI Action] 👁️ Switching to Vision Search Mode (Looksy Engine)...")
        # In the future, this is where you'd call your Looksy API logic
        notes = ["Visual Match Found: Minimalist aesthetic with linen textures.", 
                 "Style Profile: Earthy tones, breathable fabrics suitable for Tuscany."]
    else:
        print("\n[AI Action] 🌐 Using Standard Web Search (Tavily)...")
        query = state['plan'][:100]
        search_result = tavily.search(query=query, max_results=2)
        notes = [res['content'] for res in search_result['results']]
    
    return {"research_notes": notes}

def writer(state: AgentState):
    print("---WRITING PHASE---")
    prompt = f"Using these notes: {state['research_notes']}, write a 2-paragraph summary on {state['topic']}."
    response = llm.invoke(prompt)
    return {"report": response.content}

# 4. Construct the Graph
workflow = StateGraph(AgentState)

workflow.add_node("planner", planner)
workflow.add_node("researcher", researcher)
workflow.add_node("writer", writer)

# Define the flow
workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)

# Create a memory saver to "store" the agent's progress while it waits for you
memory = MemorySaver()

# We tell the graph to STOP after the 'planner' is done
app = workflow.compile(
    checkpointer=memory,
    interrupt_after=["planner"]
)

# 5. Execute!
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1"}}
    inputs = {"topic": "What is the best summer wedding style for Italy?"}

    # --- PHASE 1: Run until the Interrupt ---
    print("\n[System] Starting Agents...")
    for event in app.stream(inputs, config):
        print(event)

    # The code will PAUSE here.
    print("\n--- HUMAN INTERVENTION REQUIRED ---")
    user_input = input("The Planner has finished. Do you approve the plan? (yes/no): ")

    if user_input.lower() == "yes":
        # --- PHASE 2: Resume from where we left off ---
        print("\n[System] Resuming... Researcher is now searching the web.")
        for event in app.stream(None, config): # 'None' tells it to resume from state
            print(event)
        
        # Print final result
        final_state = app.get_state(config)
        print("\n--- FINAL REPORT ---")
        print(final_state.values['report'])
    else:
        print("[System] Plan rejected. Exiting.")

    # This will save a 'graph.png' file in your folder so you can see the logic
try:
    with open("graph.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
    print("\n[System] Workflow diagram saved as graph.png")
except Exception:
    # This requires a couple of extra helper libraries to run, 
    # so don't worry if it skips for now.
    print("\n[System] Skipping diagram generation.")