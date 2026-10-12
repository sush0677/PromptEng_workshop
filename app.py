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

# Initialize Session State
if "memory_store" not in st.session_state:
    st.session_state.memory_store = {
        "context_log": [],
        "current_agent": "Planner Agent",
        "shared_state": {}
    }

if "loop_results" not in st.session_state:
    st.session_state.loop_results = {}

st.title("Advanced Agent Orchestration Studio")
st.markdown("Explore Graph-Level Prompting, Iterative Looping, and Handoff Memory powered by Groq.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("Workflow Settings")
    
    selected_model = st.selectbox(
        "Groq Model",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
        index=0,
        help="llama-3.1-8b-instant is optimized for high-volume free tier usage."
    )
    
    selected_nodes = st.multiselect(
        "Active Graph Nodes",
        ["Planner Agent", "Researcher Agent", "Critic Agent", "Synthesizer Agent"],
        default=["Planner Agent", "Researcher Agent", "Critic Agent"]
    )
    
    st.subheader("Looping & Refinement")
    enable_looping = st.toggle("Enable Iterative Feedback Loop", value=True)
    max_loops = st.slider("Max Loop Iterations", min_value=1, max_value=5, value=2)
    
    st.subheader("Ad-Hoc Prompting")
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
        st.session_state.loop_results = {}
        st.rerun()

# --- Main Interface ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("Task Input & Execution")
    user_task = st.text_area(
        "Define the primary task for the graph:",
        value="Plan a 3-day tech meetup itinerary in Dubai under a $500 budget."
    )
    
    if st.button("Run Workflow Graph", type="primary"):
        if not groq_key:
            st.error("Groq API key not found. Please set GROQ_API_KEY in your environment or Streamlit secrets.")
        elif not selected_nodes:
            st.error("Please select at least one node for the graph workflow.")
        else:
            st.session_state.loop_results = {}
            st.session_state.memory_store["context_log"] = []
            
            total_loops = max_loops if enable_looping else 1
            
            # Execute Graph & Capture per-loop outputs
            for loop_idx in range(total_loops):
                loop_name = f"Loop Iteration {loop_idx + 1}"
                st.session_state.loop_results[loop_name] = []
                
                for node in selected_nodes:
                    st.session_state.memory_store["current_agent"] = node
                    time.sleep(0.3) # Simulate processing delay
                    
                    # Generate simulated/dynamic step output
                    step_output = f"Output from **{node}** (Model: `{selected_model}`): Processed sub-tasks for '{user_task[:30]}...'"
                    if ad_hoc_override:
                        step_output += f" | *Injected Rule:* {ad_hoc_override}"
                    
                    # Save to loop details
                    st.session_state.loop_results[loop_name].append({
                        "node": node,
                        "output": step_output
                    })
                    
                    # Log state transition
                    st.session_state.memory_store["context_log"].append({
                        "loop": loop_idx + 1,
                        "node": node,
                        "status": "completed"
                    })
            
            st.success("Graph execution workflow completed successfully!")

    # Display Graph-style Visual Execution per Loop
    st.subheader("Graph Execution Flow & Loop Breakdown")
    if st.session_state.loop_results:
        for loop_name, steps in st.session_state.loop_results.items():
            with st.expander(f"{loop_name}", expanded=True):
                # Render visual graph flow using columns or arrows
                for idx, step in enumerate(steps):
                    node_name = step["node"]
                    node_desc = step["output"]
                    
                    # Visual Node Card
                    st.markdown(f"**Step {idx+1}: `{node_name}`**")
                    st.info(node_desc)
                    
                    if idx < len(steps) - 1:
                        st.markdown("<div style='text-align: center;'><i>passes state to</i></div>", unsafe_allow_html=True)
    else:
        st.info("Click 'Run Workflow Graph' to visualize the graph execution loops.")

with col2:
    st.subheader("Handoff Memory & State")
    st.markdown("Inspect how state and context pass between agents across graph hops:")
    st.json(st.session_state.memory_store)

# --- Educational Section: Understanding Handoff Memory ---
st.markdown("---")
st.subheader("Deep Dive: What is Handoff Memory?")
st.markdown("""
**Handoff Memory** is the architectural pattern used in multi-agent graph workflows to cleanly pass execution context, state variables, and intermediate artifacts from one specialized agent node to the next.

* **Context Preservation:** When a `Planner Agent` hands off control to a `Researcher Agent`, it doesn't just pass a raw string; it transfers a structured state object containing goals, constraints, and previous findings.
* **Traceability:** Every transition logs which node handled the state, allowing developers to debug where information was modified or refined across iterative loops.
* **Decoupled Architecture:** Agents remain modular because they read from and write to a shared state pool rather than being tightly bound to each other's internal functions.
""")
