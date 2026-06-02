import os
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.utilities import SerpAPIWrapper
import wikipedia

# -----------------------
# Load environment variables
# -----------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY") or st.secrets.get("SERPAPI_API_KEY")
# -----------------------
# Streamlit UI config
# -----------------------
st.set_page_config(page_title="AI Search Engine", page_icon="🔍", layout="wide")

st.title("🔍 AI Search Engine")
st.markdown("AI Agent with SerpAPI + Wikipedia + Tool Tracking")

# -----------------------
# Session State Init
# -----------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "tool_logs" not in st.session_state:
    st.session_state.tool_logs = []

# -----------------------
# LLM (Groq)
# -----------------------
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# -----------------------
# SerpAPI Setup
# -----------------------
search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)

def search_tool_with_log(query):
    st.session_state.tool_logs.append(f"🔎 Search Tool called → {query}")
    result = search.run(query)
    st.session_state.tool_logs.append("✅ Search Tool finished")
    return result

search_tool = Tool(
    name="Search",
    func=search_tool_with_log,
    description="Use for real-time internet search"
)

# -----------------------
# Wikipedia Tool
# -----------------------
def wiki_tool_with_log(query):
    st.session_state.tool_logs.append(f"📚 Wikipedia Tool called → {query}")
    try:
        result = wikipedia.summary(query, sentences=2)
        st.session_state.tool_logs.append("✅ Wikipedia Tool finished")
        return result
    except Exception as e:
        return f"Wikipedia error: {str(e)}"

wiki_tool = Tool(
    name="Wikipedia",
    func=wiki_tool_with_log,
    description="Use for general knowledge questions"
)

# -----------------------
# Agent
# -----------------------
agent = initialize_agent(
    tools=[search_tool, wiki_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# -----------------------
# Input UI
# -----------------------
query = st.text_input("Enter your question", placeholder="e.g. Who is Elon Musk?")

# -----------------------
# Run Button
# -----------------------
if st.button("Search"):

    if not query:
        st.warning("Please enter a question")

    else:
        # RESET logs every query
        st.session_state.tool_logs = []

        with st.spinner("Thinking..."):

            try:
                response = agent.run(query)

                # Save chat history
                st.session_state.history.append({
                    "question": query,
                    "answer": response
                })

            except Exception as e:
                st.error(f"Error: {str(e)}")

# -----------------------
# Tool Execution Logs
# -----------------------
if st.session_state.tool_logs:
    st.markdown("## 🛠️ Tool Execution Steps")

    for log in st.session_state.tool_logs:
        if "Search" in log:
            st.info(log)
        elif "Wikipedia" in log:
            st.success(log)
        else:
            st.write(log)

# -----------------------
# Chat History
# -----------------------
if st.session_state.history:
    st.markdown("## 🧠 Chat History")

    for chat in reversed(st.session_state.history):
        st.markdown(f"**You:** {chat['question']}")
        st.markdown(f"**AI:** {chat['answer']}")
        st.markdown("---")