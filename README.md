# 🔍 AI Search Engine (LangChain + Groq + Tools)

An AI-powered search engine using LangChain agents, Groq LLM, SerpAPI, Wikipedia.  
It intelligently selects tools to answer user queries in real-time.

---

## 🚀 Features
- AI Agent (LangChain)
- Real-time web search (SerpAPI)
- Wikipedia knowledge base
- Streamlit UI
- Chat history + tool logs

---

## ⚙️ Setup

```bash
pip install -r requirements.txt
streamlit run app.py



🔑 API Keys

.env or Streamlit Secrets:

GROQ_API_KEY=your_key  
SERPAPI_API_KEY=your_key


🧠 Run Flow

User → Agent → Tools (Search / Wiki / arXiv) → Groq LLM → Answer

👨‍💻 Author

Sai Krishna
