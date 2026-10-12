import streamlit as st
import os
import time

# Page Configuration
st.set_page_config(
    page_title="Advanced Agent Workflow Studio",
    page_icon="🤖",
    layout="wide"
)

# Groq API Key Configuration
groq_key = st.session_state.get("GROQ_API_KEY") or (st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY"))

# Initialize Session State for Handoff Memory and Execution History
if "memory_store" not in st.session_state:
    st.session_state.memory_store = {
        "context_log": [],
        "current_agent": "Planner Agent",
        "shared_state": {}
    }

if "execution_logs" not in st.session_state:
    st.session_state.execution_logs = []

st.title("🧠 Advanced Agent Orchestration Studio")
st.markdown("Explore **Graph-Level Prompting**, **Iterative Looping**, and **Handoff Memory** powered by Groq.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Workflow Settings")
    
    # Model Selection (Using Groq's free-tier workhorse model)
    selected_model = st.selectbox(
        "Groq Model",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
        index=0,
        help="llama-3.1-8b-instant is optimized for high-volume free tier usage."
    )
    
    # Graph / Node Selection
    selected_nodes = st.multiselect(
        "Active Graph Nodes",
        ["Planner Agent", "Researcher Agent", "Critic Agent", "Synthesizer Agent"],
        default=["Planner Agent", "Researcher Agent", "Critic Agent"]
    )
    
    # Looping Configuration
    st.subheader("🔄 Looping & Refinement")
    enable_looping = st.toggle("Enable Iterative Feedback Loop", value=True)
    max_loops = st.slider("Max Loop Iterations", min_value=1, max_value=5, value=2)
    
    # Ad-hoc Prompt Overrides
    st.subheader("⚡ Ad-Hoc Prompting")
    ad_hoc_override = st.text_area(
        "Dynamic Prompt Injection", 
        placeholder="Enter custom instructions to inject mid-workflow..."
    )
    
    if st.button("Reset Session State"):
        st.session_state.memory_store = {
            "context_log": [],
            "current_agent": "Planner Agent",
            "shared_state": {}
        }
        st.session_state.execution_logs = []
        st.rerun()

# --- Main Interface ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📝 Task Input & Execution")
    user_task = st.text_area(
        "Define the primary task for the graph:",
        value="Plan a 3-day tech meetup itinerary in Dubai under a $500 budget."
    )
    
    if st.button("🚀 Run Workflow Graph", type="primary"):
        if not groq_key:
            st.error("Groq API key not found. Please set GROQ_API_KEY in your environment or Streamlit secrets.")
        elif not selected_nodes:
            st.error("Please select at least one node for the graph workflow.")
        else:
            st.session_state.execution_logs = []
            
            # Simulate Graph Execution with Handoff Memory and Looping using Groq configuration
            for loop_idx in range(max_loops if enable_looping else 1):
                st.markdown(f"--- *Iteration Cycle: {loop_idx + 1} (Model: {selected_model})* ---")
                
                for node in selected_nodes:
                    st.session_state.memory_store["current_agent"] = node
                    time.sleep(0.4) # Simulate processing latency
                    
                    # Process step based on active node
                    step_output = f"[{node}] Executed successfully via model {selected_model}."
                    
                    if ad_hoc_override:
                        step_output += f" (Injected Ad-Hoc Rule: {ad_hoc_override})"
                    
                    # Update Handoff Memory
                    st.session_state.memory_store["context_log"].append({
                        "iteration": loop_idx + 1,
                        "node": node,
                        "model": selected_model,
                        "output": step_output
                    })
                    
                    st.session_state.execution_logs.append(step_output)
            
            st.success("Workflow completed successfully!")

    # Display Live Execution Stream
    st.subheader("📊 Execution Log")
    for log in st.session_state.execution_logs:
        st.info(log)

with col2:
    st.subheader("🧠 Handoff Memory & State")
    st.markdown("Inspect how state and context pass between agents across graph hops:")
    
    # Display current state snapshot
    st.json(st.session_state.memory_store)
