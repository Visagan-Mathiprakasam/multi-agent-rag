# 🤖 Self-Adaptive Multi-Agent RAG Framework

**Intelligent Decision Support Across Agriculture, Finance, Energy, Healthcare, and Education**

A web-based intelligent decision-support system that uses Retrieval-Augmented Generation (RAG), multiple specialized AI agents, and a coordinator that dynamically selects agents and retrieval strategies based on the user's query domain and complexity.

## 🏗️ Architecture

```
User Query
    ↓
Query Classifier (Domain + Complexity Detection)
    ↓
Adaptive Agent Coordinator
    ↓
Dynamic Agent Selection
    ↓
RAG Retrieval (ChromaDB + Sentence Transformers)
    ↓
Domain-Specific Analysis (Specialized Agents)
    ↓
Verification Agent (Evidence Checking)
    ↓
Confidence Evaluation
    ↓
Additional Retrieval if needed
    ↓
Final Evidence-Grounded Response
```

### Adaptive Behavior

| Complexity | Workflow |
|---|---|
| **LOW** | Retrieval → Domain Agent → Response |
| **MEDIUM** | Retrieval → Domain Agent → Verification → Response |
| **HIGH** | Retrieval → Multiple Domain Agents → Verification → Re-retrieval if needed → Response |

## 📁 Project Structure

```
multi_agent_rag/
├── app.py                  # Streamlit UI
├── requirements.txt        # Python dependencies
├── .env.example            # API key template
├── README.md               # This file
├── agents/
│   ├── base_agent.py       # Base class for domain agents
│   ├── coordinator.py      # LangGraph workflow orchestration
│   ├── retrieval_agent.py  # Document retrieval agent
│   ├── verification_agent.py # Evidence verification agent
│   ├── agriculture_agent.py
│   ├── finance_agent.py
│   ├── energy_agent.py
│   ├── healthcare_agent.py
│   └── education_agent.py
├── rag/
│   ├── document_loader.py  # PDF/TXT loading and chunking
│   ├── embeddings.py       # Sentence Transformer embeddings
│   ├── vector_store.py     # ChromaDB vector store
│   └── retriever.py        # Document retrieval
├── data/
│   ├── agriculture/        # Agriculture knowledge documents
│   ├── finance/            # Finance knowledge documents
│   ├── energy/             # Energy knowledge documents
│   ├── healthcare/         # Healthcare knowledge documents
│   └── education/          # Education knowledge documents
├── evaluation/
│   └── evaluate.py         # Evaluation and comparison script
└── utils/
    ├── config.py           # Central configuration
    └── confidence.py       # Confidence calculation
```

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.9 or higher
- A Google Gemini API key ([Get one here](https://aistudio.google.com/apikey))

### 2. Install Dependencies
```bash
cd multi_agent_rag
pip install -r requirements.txt
```

### 3. Configure API Key
```bash
# Copy the example env file
copy .env.example .env

# Edit .env and add your API key
# GOOGLE_API_KEY=your-actual-api-key
```

### 4. Add Documents (Optional)
Sample knowledge documents are included in the `data/` folder. You can add your own PDF or TXT files to any domain folder:
```
data/agriculture/   → Agriculture documents
data/finance/       → Finance documents
data/energy/        → Energy documents
data/healthcare/    → Healthcare documents
data/education/     → Education documents
```

### 5. Run the Application
```bash
streamlit run app.py
```

### 6. First-Time Setup
After launching, click **"Ingest/Refresh Documents"** in the sidebar to load documents into the vector database.

## 💡 Demo Scenarios

1. **Agriculture**: "What factors should be considered before choosing a crop?"
2. **Finance**: "What factors should be considered when evaluating investment risk?"
3. **Energy**: "What are the advantages and limitations of solar energy?"
4. **Healthcare**: "What are common causes of iron deficiency?"
5. **Education**: "How can a student create a study plan for an upcoming examination?"
6. **Multi-domain (Complex)**: "Should a manufacturing company consider solar energy based on its energy requirements and financial constraints?"

## 📊 Evaluation

Run the evaluation script to compare Basic RAG vs. Adaptive Multi-Agent RAG:
```bash
python evaluation/evaluate.py
```

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Google Gemini (gemini-2.0-flash) |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| Agent Orchestration | LangGraph |
| RAG Utilities | LangChain |
| Document Loading | PyPDF, LangChain loaders |

## ⚠️ Disclaimers

- **Healthcare**: This system provides general health information only. It is NOT a substitute for professional medical advice.
- **Finance**: Financial information is for educational purposes. Consult a qualified financial advisor for specific decisions.
- This is an academic mini-project prototype and not intended for production use.
