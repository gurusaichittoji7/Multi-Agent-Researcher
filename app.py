import streamlit as st
from researcher import app
import uuid

st.set_page_config(page_title="Agentic Researcher", page_icon="🕵️")
st.title("🕵️ Multi-Agent Research Assistant")

# 1. Setup Persistent Session State
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "phase" not in st.session_state:
    st.session_state.phase = "input"

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# --- PHASE 1: INPUT ---
if st.session_state.phase == "input":
    topic = st.text_input("What do you want me to research?")
    if st.button("Start Research"):
        st.session_state.topic = topic
        # Run until the first interrupt (Planner)
        for event in app.stream({"topic": topic}, config):
            st.write(event)
        st.session_state.phase = "approval"
        st.rerun()

# --- PHASE 2: APPROVAL ---
elif st.session_state.phase == "approval":
    st.info(f"Topic: {st.session_state.topic}")
    state = app.get_state(config)
    st.success("✅ Planner has finished. Please review the plan:")
    st.write(state.values.get("plan"))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve & Research"):
            # Resume the graph (passing None resumes from checkpoint)
            for event in app.stream(None, config):
                st.write(event)
            st.session_state.phase = "complete"
            st.rerun()
    with col2:
        if st.button("❌ Reject"):
            st.session_state.phase = "input"
            st.rerun()

# --- PHASE 3: FINAL REPORT ---
elif st.session_state.phase == "complete":
    final_state = app.get_state(config)
    st.markdown("### 📄 Final Research Report")
    st.write(final_state.values.get("report", "No report generated."))
    if st.button("Start New Research"):
        st.session_state.phase = "input"
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()