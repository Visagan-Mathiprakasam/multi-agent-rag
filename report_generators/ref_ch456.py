import os
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, PageBreak, Image
from reportlab.lib import colors
from ref_styles import (
    title_style, h1_style, h2_style, body_style, body_noindent_style,
    bullet_style, caption_style, make_placeholder_box, USABLE_WIDTH
)

IMG_DIR = r"C:\Users\visag\.gemini\antigravity\brain\16632dba-7765-414e-bb84-677366a2f22c\scratch\images"
img_5_1 = os.path.join(IMG_DIR, "fig_5_1_architecture.png")
img_5_2 = os.path.join(IMG_DIR, "fig_5_2_context.png")
img_5_3 = os.path.join(IMG_DIR, "fig_5_3_use_case.png")
img_5_4 = os.path.join(IMG_DIR, "fig_5_4_activity.png")
img_5_5 = os.path.join(IMG_DIR, "fig_5_5_dfd.png")
img_5_6 = os.path.join(IMG_DIR, "fig_5_6_wireframe.png")
img_6_1 = os.path.join(IMG_DIR, "fig_6_1_routing_seq.png")
img_6_2 = os.path.join(IMG_DIR, "fig_6_2_fusion_flow.png")

def get_ch456_pages():
    story = []

    # =========================================================================
    # PAGE 11: CHAPTER 4 - SYSTEM ANALYSIS, 4.1 REQUIREMENTS (FR & NFR)
    # =========================================================================
    p11 = [
        Paragraph("4. SYSTEM ANALYSIS", title_style),
        Paragraph("4.1 Requirement Specification", h1_style),
        Paragraph(
            "The requirement specification outlines the functional and non-functional requirements of the Self-Adaptive Multi-Agent RAG Framework. These specifications define the core capabilities, behavioural boundaries, and operational constraints necessary for production-grade execution.",
            body_style
        ),
        Paragraph("Functional Requirements", h2_style),
        Paragraph("The functional requirements describe the primary operations that the system must execute:", body_noindent_style),
        Paragraph("1. Query Routing: The system must classify user queries into Direct, Vector, Web, or Hybrid execution paths.", bullet_style),
        Paragraph("2. Document Ingestion: The system must parse and chunk textual documents into dense embeddings.", bullet_style),
        Paragraph("3. Semantic Retrieval: The system must query ChromaDB and return top-k semantically relevant chunks.", bullet_style),
        Paragraph("4. Web Information Retrieval: The system must execute DuckDuckGo search queries for real-time information.", bullet_style),
        Paragraph("5. Answer Synthesis: The system must synthesize context from multiple sources into a coherent response with citations.", bullet_style),
        Paragraph("6. Triad Metric Evaluation: The system must compute Context Relevance, Groundedness, and Answer Relevance.", bullet_style),
        Paragraph("7. Output Visualization: The system must render the answer, source chunks, and metrics in an interactive web UI.", bullet_style),
        Paragraph("8. Resilient Fallbacks: The system must execute offline deterministic answers during API or network downtime.", bullet_style),
        Paragraph("Non-Functional Requirements", h2_style),
        Paragraph("The non-functional requirements define the expected quality attributes and performance parameters:", body_noindent_style),
        Paragraph("&bull; Usability: The web interface should provide clear query inputs and visual trace badges for intuitive exploration.", bullet_style),
        Paragraph("&bull; Performance: Retrieval and routing should complete within sub-second thresholds to minimize total latency.", bullet_style),
        PageBreak()
    ]
    story.extend(p11)

    # =========================================================================
    # PAGE 12: NFR CONT, 4.2 EXISTING SYSTEM, 4.3 PROPOSED SYSTEM
    # =========================================================================
    p12 = [
        Paragraph("&bull; Reliability: The multi-agent pipeline must handle malformed queries and API connection timeouts gracefully without crashing.", bullet_style),
        Paragraph("&bull; Maintainability: Each agent must be implemented as an independent, decoupled module following clear interface contracts.", bullet_style),
        Paragraph("&bull; Security: OpenRouter API keys and private environment credentials must remain secured in environment variables.", bullet_style),
        Paragraph("&bull; Compatibility: The platform must execute cross-platform on standard Windows, Linux, and macOS environments.", bullet_style),
        Paragraph("4.2 Characteristics of Existing System", h1_style),
        Paragraph(
            "Existing retrieval-augmented generation architectures rely predominantly on linear, single-pass execution chains. When a user issues a prompt, the system unconditionally transforms the text into an embedding vector, retrieves chunks from a static database, and sends them to an LLM.",
            body_style
        ),
        Paragraph(
            "This naive paradigm suffers from multiple critical drawbacks. First, simple conversational queries incur unnecessary latency and token costs by triggering useless retrieval routines. Second, when the required knowledge is outside the vector index, the system provides irrelevant context, leading to confident hallucinations.",
            body_style
        ),
        Paragraph(
            "Third, standard pipelines lack the ability to consult live internet resources for breaking news or time-sensitive data. Finally, conventional systems provide no automated self-evaluation, presenting hallucinated outputs without confidence flags.",
            body_style
        ),
        Paragraph("4.3 Proposed System", h1_style),
        Paragraph(
            "The proposed system establishes an autonomous multi-agent ecosystem coordinated through a LangGraph state machine to resolve these limitations.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p12)

    # =========================================================================
    # PAGE 13: 4.3 CONT & 4.4 FEASIBILITY STUDY
    # =========================================================================
    p13 = [
        Paragraph(
            "In the proposed framework, an intelligent Query Router agent evaluates incoming queries to determine the optimal retrieval strategy. Factual queries mapped to internal domain knowledge trigger the Semantic Retriever, which accesses ChromaDB collections.",
            body_style
        ),
        Paragraph(
            "Queries requiring real-time, temporal, or general internet knowledge trigger the Live Web Search Agent. For multi-faceted queries, a Hybrid mode executes parallel retrieval across both internal vector stores and external web feeds.",
            body_style
        ),
        Paragraph(
            "The Multi-Source Synthesizer merges all evidence chunks into a unified response with numbered in-line citations. Immediately following synthesis, the Automated Evaluator assesses Context Relevance, Groundedness, and Answer Relevance to ensure high fidelity.",
            body_style
        ),
        Paragraph(
            "The entire workflow is managed within a unified Streamlit dashboard, giving users full transparency into agent reasoning, retrieval distances, and evaluation metrics.",
            body_style
        ),
        Paragraph("4.4 Feasibility Study", h1_style),
        Paragraph(
            "A comprehensive feasibility study was conducted to confirm the technical, economic, operational, and schedule viability of the project.",
            body_style
        ),
        Paragraph("Technical Feasibility", h2_style),
        Paragraph(
            "The project is technically viable as it builds upon mature, open-source technologies including LangGraph, ChromaDB, Sentence-Transformers, and Python. The OpenRouter API provides reliable, OpenAI-compatible access to cutting-edge language models with extensive documentation and community support.",
            body_style
        ),
        Paragraph("Economic Feasibility", h2_style),
        Paragraph(
            "The system is economically highly viable. It leverages free open-source software libraries, lightweight local embeddings, and cost-effective or free-tier models via OpenRouter, eliminating expensive infrastructure licenses or specialized cloud hardware.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p13)

    # =========================================================================
    # PAGE 14: FEASIBILITY CONT & 4.5 SRS (PURPOSE, INPUTS, PROCESSING)
    # =========================================================================
    p14 = [
        Paragraph("Operational Feasibility", h2_style),
        Paragraph(
            "Operationally, the platform provides an intuitive, web-based chat interface requiring no technical expertise from end users. For administrators, modular code separation allows effortless ingestion of new enterprise documents and replacement of underlying LLM models without system restructuring.",
            body_style
        ),
        Paragraph("Schedule Feasibility", h2_style),
        Paragraph(
            "The project was executed in structured iterative sprints: initial data ingestion and ChromaDB configuration, agent module development, LangGraph state machine orchestration, UI engineering, and end-to-end evaluation benchmarking.",
            body_style
        ),
        Paragraph("4.5 Software Requirement Specification", h1_style),
        Paragraph(
            "The Software Requirement Specification (SRS) establishes the functional scope, operational boundaries, inputs, and outputs of the multi-agent framework.",
            body_style
        ),
        Paragraph("Purpose", h2_style),
        Paragraph(
            "The purpose of the system is to provide intelligent, verifiable, and multi-source question-answering by adaptively routing queries across local vector knowledge bases and live web search engines.",
            body_style
        ),
        Paragraph("Inputs", h2_style),
        Paragraph(
            "The system accepts natural language user queries, configuration parameters (model selection, similarity thresholds), and unstructured text documents for database ingestion.",
            body_style
        ),
        Paragraph("Processing", h2_style),
        Paragraph(
            "Processing involves prompt classification, dense vector similarity calculation, asynchronous web scraping, context fusion synthesis, and automated Triad metric computation.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p14)

    # =========================================================================
    # PAGE 15: SRS CONT (OUTPUTS, OPERATING CONDITIONS, LIMITATIONS)
    # =========================================================================
    p15 = [
        Paragraph("Outputs", h2_style),
        Paragraph(
            "The primary outputs include the synthesized final answer, detailed source citations with URLs or document identifiers, agent execution logs, and quantitative RAG Triad scores (0.0 to 1.0).",
            body_style
        ),
        Paragraph("Operating Conditions", h2_style),
        Paragraph(
            "The system operates in a Python 3.10+ virtual environment on standard server or workstation hardware. An active internet connection is required for external OpenRouter LLM inference and live DuckDuckGo web searches. When offline, deterministic fallback synthesizers ensure continued demonstration capability.",
            body_style
        ),
        Paragraph("Limitations", h2_style),
        Paragraph(
            "The framework's response quality is bounded by the capabilities of the selected LLM and the completeness of the ingested document collection. In extremely rare instances of network timeouts or DuckDuckGo rate limiting, web retrieval may degrade to cached or vector-only context.",
            body_style
        ),
        Paragraph(
            "Furthermore, while the automated RAG Triad provides strong heuristic confidence, it remains an automated validation process rather than an absolute legal or medical guarantee of factual accuracy.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p15)

    # =========================================================================
    # PAGE 16: CHAPTER 5 - SYSTEM DESIGN & 5.1 ARCHITECTURE / WORKFLOW
    # =========================================================================
    p16 = [
        Paragraph("5. SYSTEM DESIGN", title_style),
        Paragraph("5.1 System Architecture / Overall Workflow", h1_style),
        Paragraph(
            "The system architecture defines the modular decomposition and interaction patterns of the Self-Adaptive Multi-Agent RAG Framework. The platform is structured into five cooperative functional layers: Presentation Layer, Agent Orchestration Layer, Retrieval & Tool Layer, Knowledge Storage Layer, and Inference Layer.",
            body_style
        ),
        Paragraph(
            "At runtime, the LangGraph StateGraph acts as the centralized controller, passing a typed AgentState dictionary across nodes. Each node encapsulates a specialized agent with discrete responsibilities, ensuring strict separation of concerns.",
            body_style
        ),
        Paragraph(
            "The complete execution workflow progresses through the following sequential stages:",
            body_noindent_style
        ),
        Paragraph("1. Initialize application, verify API connectivity, and load vector collections.", bullet_style),
        Paragraph("2. Accept natural language query and routing preferences from the user.", bullet_style),
        Paragraph("3. Query Router evaluates query intent and complexity.", bullet_style),
        Paragraph("4. Route execution: Direct LLM, Vector Retrieval, Web Search, or Hybrid.", bullet_style),
        Paragraph("5. Retrieve semantically matching document chunks from ChromaDB.", bullet_style),
        Paragraph("6. Execute live DuckDuckGo web search when real-time context is needed.", bullet_style),
        Paragraph("7. Synthesizer merges context into a cohesive response with citations.", bullet_style),
        Paragraph("8. Evaluator calculates Context Relevance, Groundedness, and Answer Relevance.", bullet_style),
        Paragraph("9. Streamlit displays final answer, execution trace, citations, and evaluation metrics.", bullet_style),
        PageBreak()
    ]
    story.extend(p16)

    # =========================================================================
    # PAGE 17: FIGURE 5.1 & 5.2 CONTEXT DIAGRAM
    # =========================================================================
    p17 = [
        Image(img_5_1, width=USABLE_WIDTH, height=150),
        Paragraph("Figure 5.1: Architecture of the Self-Adaptive Multi-Agent RAG Framework.", caption_style),
        Paragraph("5.2 Context Diagram", h1_style),
        Paragraph(
            "A context diagram illustrates the system as a centralized process and details its external boundaries and data interactions with external entities.",
            body_style
        ),
        Paragraph(
            "The primary external entities interacting with the Multi-Agent RAG System are the End User / Knowledge Worker, the OpenRouter LLM API Gateway, the DuckDuckGo Search Engine, and the ChromaDB Persistent Storage.",
            body_style
        ),
        Paragraph("Main entities and data flows:", body_noindent_style),
        Paragraph("&bull; User: Submits natural language queries and receives validated answers with citations.", bullet_style),
        Paragraph("&bull; ChromaDB: Receives document embeddings and supplies relevant context chunks.", bullet_style),
        Paragraph("&bull; DuckDuckGo: Receives web search queries and returns fresh news and articles.", bullet_style),
        Paragraph("&bull; OpenRouter API: Receives prompt templates and returns LLM reasoning completions.", bullet_style),
        PageBreak()
    ]
    story.extend(p17)

    # =========================================================================
    # PAGE 18: FIGURE 5.2 & 5.3 USE CASE DIAGRAM
    # =========================================================================
    p18 = [
        Image(img_5_2, width=USABLE_WIDTH, height=150),
        Paragraph("Figure 5.2: Context Diagram of the Proposed System.", caption_style),
        Paragraph("5.3 Use Case Diagram", h1_style),
        Paragraph(
            "The use case diagram defines the primary functional interactions between human actors, system administrators, and external API services.",
            body_style
        ),
        Paragraph("Main Use Cases:", body_noindent_style),
        Paragraph("1. Submit Natural Language Query (User)", bullet_style),
        Paragraph("2. Inspect Agent Reasoning Trace (User)", bullet_style),
        Paragraph("3. View Source Documents and Citations (User)", bullet_style),
        Paragraph("4. Ingest and Re-index Domain Documents (Administrator)", bullet_style),
        Paragraph("5. Configure LLM Model and API Keys (Administrator)", bullet_style),
        Paragraph("6. Classify Query Intent and Complexity (Router Agent)", bullet_style),
        Paragraph("7. Execute Dense Semantic Search (Retriever Agent)", bullet_style),
        Paragraph("8. Perform Live Web Search and Scraping (Web Agent)", bullet_style),
        Paragraph("9. Calculate Automated RAG Triad Scores (Evaluator Agent)", bullet_style),
        PageBreak()
    ]
    story.extend(p18)

    # =========================================================================
    # PAGE 19: FIGURE 5.3 & 5.4 ACTIVITY DIAGRAM
    # =========================================================================
    p19 = [
        Image(img_5_3, width=USABLE_WIDTH, height=150),
        Paragraph("Figure 5.3: Use Case Diagram of the Proposed System.", caption_style),
        Paragraph("5.4 Activity Diagram", h1_style),
        Paragraph(
            "An activity diagram illustrates the chronological control flow and decision branching of the system during query execution.",
            body_style
        ),
        Paragraph(
            "The workflow initiates upon user query submission. The state machine invokes the Router agent. Based on intent classification, the workflow branches to retrieve vector documents, scrape web pages, or both. After retrieval, parallel evidence streams merge into the Synthesizer node. The synthesized output is evaluated for hallucination, and the final state is dispatched to the Streamlit UI.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p19)

    # =========================================================================
    # PAGE 20: FIGURE 5.4 & 5.5 DATA FLOW DIAGRAM (LEVEL 0 & LEVEL 1)
    # =========================================================================
    p20 = [
        Image(img_5_4, width=USABLE_WIDTH, height=150),
        Paragraph("Figure 5.4: Activity Diagram for Query Processing and Adaptive RAG.", caption_style),
        Paragraph("5.5 Data Flow Diagram / Algorithm Workflow", h1_style),
        Paragraph(
            "A Data Flow Diagram (DFD) models the transformation of data as it passes through the various processing entities of the application.",
            body_style
        ),
        Paragraph("Level 0 DFD", h2_style),
        Paragraph(
            "At Level 0, the entire framework is represented as a single transformational process. User queries and knowledge documents enter the system, and grounded answers, citations, and evaluation metrics flow out.",
            body_style
        ),
        Paragraph("Level 1 DFD", h2_style),
        Paragraph(
            "At Level 1, the system decomposes into five distinct sub-processes: Process 1: Document Ingestion and Vector Embedding; Process 2: Query Classification and Intent Routing; Process 3: Semantic Vector Retrieval; Process 4: Web Scraping and Information Extraction; and Process 5: Multi-Source Synthesis and Triad Evaluation.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p20)

    # =========================================================================
    # PAGE 21: PROCESSES CONT & FIGURE 5.5 DATA FLOW DIAGRAM
    # =========================================================================
    p21 = [
        Paragraph("Process 1: Ingestion and Vector Embedding", h2_style),
        Paragraph("Unstructured text is parsed, recursively chunked, embedded via all-MiniLM-L6-v2, and stored in ChromaDB.", body_style),
        Paragraph("Process 2: Query Intent Routing", h2_style),
        Paragraph("User prompt is analyzed to determine complexity, domain alignment, and temporal necessity.", body_style),
        Paragraph("Process 3: Semantic Vector Search", h2_style),
        Paragraph("Retriever queries ChromaDB with cosine similarity and extracts top-k context passages.", body_style),
        Paragraph("Process 4: Real-Time Web Scraping", h2_style),
        Paragraph("DuckDuckGo executes live web searches and extracts relevant snippet text.", body_style),
        Paragraph("Process 5: Synthesis and Evaluation", h2_style),
        Paragraph("Context is merged, LLM generates the answer, and the evaluator scores Context Relevance and Faithfulness.", body_style),
        Spacer(1, 4),
        Image(img_5_5, width=USABLE_WIDTH, height=145),
        Paragraph("Figure 5.5: Data Flow Diagram of the Proposed System.", caption_style),
        PageBreak()
    ]
    story.extend(p21)

    # =========================================================================
    # PAGE 22: ALGORITHM STEPS & 5.6 DATABASE / DATASET DESIGN
    # =========================================================================
    p22 = [
        Paragraph("Multi-Agent Coordination Algorithm", h1_style),
        Paragraph("The core coordination logic follows these deterministic steps:", body_noindent_style),
        Paragraph("1. Receive incoming user query $Q$ from interface.", bullet_style),
        Paragraph("2. Query Router evaluates intent vector and classifies into route $R \\in \\{\\text{Direct, Vector, Web, Hybrid}\\}$.", bullet_style),
        Paragraph("3. If $R = \\text{Vector}$ or $R = \\text{Hybrid}$, retrieve $K$ nearest chunks from ChromaDB using cosine distance.", bullet_style),
        Paragraph("4. If distance exceeds SIMILARITY_DISTANCE_THRESH = 0.45, dynamically promote query to Hybrid.", bullet_style),
        Paragraph("5. If $R = \\text{Web}$ or $R = \\text{Hybrid}$, trigger DuckDuckGo search and extract top 5 snippets.", bullet_style),
        Paragraph("6. Aggregate retrieved passages into unified evidence context $C$.", bullet_style),
        Paragraph("7. Invoke Synthesizer agent with evidence $C$ and query $Q$ to produce grounded response $A$.", bullet_style),
        Paragraph("8. Evaluator calculates Triad metrics ($S_{\\text{CR}}, S_{\\text{G}}, S_{\\text{AR}}$) and returns results.", bullet_style),
        Paragraph("5.6 Database / Dataset Design", h1_style),
        Paragraph(
            "The system utilizes ChromaDB for dense vector storage and persistent collection management. Document chunks are represented as high-dimensional vectors accompanied by rich metadata.",
            body_style
        ),
        Paragraph("Input Data: Enterprise text documents across domain verticals.", body_style),
        Paragraph("Configuration Data: Routing confidence thresholds, top-k parameters, and OpenRouter model slugs.", body_style),
        Paragraph("Processing Data: Intermediate state vectors, similarity distance scores, and agent execution logs.", body_style),
        PageBreak()
    ]
    story.extend(p22)

    # =========================================================================
    # PAGE 23: OUTPUT DATA, TABLE 5.1 & 5.7 UI DESIGN
    # =========================================================================
    table_51_data = [
        [Paragraph("<b>Data Item</b>", body_noindent_style), Paragraph("<b>Purpose / Specification</b>", body_noindent_style)],
        [Paragraph("Raw Text Chunks", body_noindent_style), Paragraph("Segmented passages of 500 characters with 50-char overlap", body_noindent_style)],
        [Paragraph("Dense Embeddings", body_noindent_style), Paragraph("384-dimensional float vectors generated by all-MiniLM-L6-v2", body_noindent_style)],
        [Paragraph("Metadata Records", body_noindent_style), Paragraph("Document title, category, chunk_id, creation timestamp", body_noindent_style)],
        [Paragraph("Similarity Scores", body_noindent_style), Paragraph("Cosine distance metric used for relevance cutoff filtering", body_noindent_style)],
        [Paragraph("Web Search Results", body_noindent_style), Paragraph("Title, snippet URL, and body text returned by DuckDuckGo", body_noindent_style)],
        [Paragraph("Synthesized Response", body_noindent_style), Paragraph("Grounded answer text formatted with markdown citation keys", body_noindent_style)],
        [Paragraph("Triad Metric Scores", body_noindent_style), Paragraph("Normalized float scores [0.0 - 1.0] for relevance and faithfulness", body_noindent_style)]
    ]
    t51 = Table(table_51_data, colWidths=[140, USABLE_WIDTH - 140])
    t51.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))

    p23 = [
        Paragraph("Output Data", h2_style),
        Paragraph(
            "Output data consists of the final synthesized answer, in-line citation references, and quantitative evaluation scores.",
            body_style
        ),
        Paragraph("Table 5.1: Vector Store and State Data Schema", caption_style),
        t51,
        Spacer(1, 4),
        Paragraph("5.7 User Interface Design", h1_style),
        Paragraph(
            "The user interface is engineered as an interactive web dashboard using Streamlit. It provides a modern dual-pane layout: a main dialogue pane for chat queries and synthesized answers, and an expandable sidebar for system configuration.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p23)

    # =========================================================================
    # PAGE 24: FIGURE 5.6 UI WIREFRAME & SUMMARY
    # =========================================================================
    p24 = [
        Paragraph(
            "The interface incorporates expandable inspection cards enabling users to view the exact text chunks retrieved from ChromaDB, inspect DuckDuckGo search URLs, review agent reasoning logs, and explore RAG Triad scorecards.",
            body_style
        ),
        Spacer(1, 4),
        Image(img_5_6, width=USABLE_WIDTH, height=165),
        Paragraph("Figure 5.6: Streamlit User Interface Architecture and Wireframe Layout.", caption_style),
        Paragraph("Summary", h1_style),
        Paragraph(
            "This chapter established the complete system design, architectural layers, UML diagrams, data schemas, and user interface layout for the framework. The multi-agent architecture ensures modularity, high testability, and resilient fallback execution.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p24)

    # =========================================================================
    # PAGE 25: CHAPTER 6 - SYSTEM IMPLEMENTATION & 6.1 MODULE DESCRIPTION
    # =========================================================================
    p25 = [
        Paragraph("6. SYSTEM IMPLEMENTATION", title_style),
        Paragraph("6.1 Module Description", h1_style),
        Paragraph(
            "The implementation of the Self-Adaptive Multi-Agent RAG Framework is organized into distinct, loosely-coupled modules. Each module encapsulates specific functional logic and interfaces through standardized data contracts.",
            body_style
        ),
        Paragraph("The primary modules are:", body_noindent_style),
        Paragraph("1. Document Ingestion and Vector Store Module", bullet_style),
        Paragraph("2. Query Router Agent Module", bullet_style),
        Paragraph("3. Semantic Retriever Agent Module", bullet_style),
        Paragraph("4. Live Web Search Agent Module", bullet_style),
        Paragraph("5. Multi-Source Synthesis Module", bullet_style),
        Paragraph("6. System Integration and LangGraph Module", bullet_style),
        Paragraph("6.1.1 Document Ingestion and Vector Store Module", h2_style),
        Paragraph(
            "This module parses unstructured domain documents, cleans and normalizes raw text, and generates dense vector embeddings using Sentence-Transformers (all-MiniLM-L6-v2). Embeddings and chunk metadata are indexed in persistent ChromaDB collections.",
            body_style
        ),
        Paragraph("6.1.2 Query Router Agent Module", h2_style),
        Paragraph(
            "The Query Router inspects incoming natural language questions to classify intent. It applies few-shot prompt instructions and classification heuristics to route queries into Direct LLM, Vector Retrieval, Web Search, or Hybrid paths.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p25)

    # =========================================================================
    # PAGE 26: 6.1.3, 6.1.4, 6.1.5 MODULE DESCRIPTIONS
    # =========================================================================
    p26 = [
        Paragraph("6.1.3 Semantic Retriever Agent Module", h2_style),
        Paragraph(
            "The Retriever agent connects to ChromaDB and performs dense similarity search using cosine distance. It extracts the top-k most relevant text chunks based on the embedded query representation.",
            body_style
        ),
        Paragraph(
            "The module evaluates retrieval distances against a predefined similarity threshold. If retrieved chunks fail to meet the relevance bar, the module automatically signals the orchestrator to trigger web search fallback.",
            body_style
        ),
        Paragraph("6.1.4 Live Web Search Agent Module", h2_style),
        Paragraph(
            "The Web Search agent queries the DuckDuckGo Search API to retrieve fresh, external information for real-time, market, or open-domain topics. It extracts webpage titles, snippet summaries, and source URLs, formatting them for prompt injection.",
            body_style
        ),
        Paragraph(
            "Built-in timeout handling and rate-limit retry logic ensure that network delays do not halt overall pipeline execution.",
            body_style
        ),
        Paragraph("6.1.5 Answer Synthesis Module", h2_style),
        Paragraph(
            "The Synthesizer agent aggregates evidence retrieved from internal vector stores and external web feeds. It constructs a strictly grounded prompt instruction and invokes the OpenRouter API to produce a clear, authoritative response with numbered citations.",
            body_style
        ),
        Paragraph(
            "The module incorporates deterministic offline fallbacks that produce structured extractive summaries even when cloud API endpoints are unavailable.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p26)

    # =========================================================================
    # PAGE 27: 6.1.6 INTEGRATION MODULE & 6.2 DATASET DESCRIPTION
    # =========================================================================
    p27 = [
        Paragraph("6.1.6 System Integration Module", h2_style),
        Paragraph(
            "The system integration module leverages LangGraph to construct a stateful directed execution graph. It defines typed state dictionaries, registers nodes for each agent, configures conditional edges based on router decisions, and manages end-to-end execution flow.",
            body_style
        ),
        Paragraph(
            "This module also provides the Streamlit front-end integration, bridging user UI interactions with the underlying multi-agent graph.",
            body_style
        ),
        Paragraph("6.2 Dataset Description and Data Collection", h1_style),
        Paragraph(
            "The framework was populated and evaluated using a multi-domain corpus of authoritative technical and enterprise documents spanning Artificial Intelligence, Cloud Infrastructure, Healthcare, and Financial Systems.",
            body_style
        ),
        Paragraph(
            "Unlike simple toy datasets, the corpus incorporates complex semi-structured reports, academic surveys, and corporate whitepapers to rigorously test chunking and retrieval performance.",
            body_style
        ),
        Paragraph("Input Data Characteristics:", body_noindent_style),
        Paragraph("&bull; Domain Coverage: AI/ML, Cloud Computing, Healthcare Informatics, and Quantitative Finance.", bullet_style),
        Paragraph("&bull; Document Format: Unstructured PDF documents, structured Markdown documentation, and plain text files.", bullet_style),
        Paragraph("&bull; Document Scale: Over 150 document sections chunked into approximately 600 distinct dense vector passages.", bullet_style),
        Paragraph("&bull; Live Web Feed: Unbounded real-time web articles indexed dynamically via DuckDuckGo Search.", bullet_style),
        PageBreak()
    ]
    story.extend(p27)

    # =========================================================================
    # PAGE 28: 6.3 DATA PREPROCESSING
    # =========================================================================
    p28 = [
        Paragraph("6.3 Data Preprocessing", h1_style),
        Paragraph(
            "Data preprocessing transforms unstructured source documents into clean, semantically dense vector chunks suitable for indexing and retrieval.",
            body_style
        ),
        Paragraph("6.3.1 Document Text Extraction", h2_style),
        Paragraph(
            "Source documents are ingested using automated loaders that parse PDF, Markdown, and TXT formats, stripping extraneous formatting characters, headers, and footers.",
            body_style
        ),
        Paragraph("6.3.2 Text Cleaning and Normalization", h2_style),
        Paragraph(
            "Extracted text undergoes Unicode normalization, removal of non-printable ASCII artifacts, whitespace consolidation, and punctuation standardization to ensure high embedding fidelity.",
            body_style
        ),
        Paragraph("6.3.3 Recursive Character Chunking", h2_style),
        Paragraph(
            "Documents are segmented using a recursive character chunker with a target chunk size of 500 characters and an overlap window of 50 characters, preserving contextual continuity across chunk boundaries.",
            body_style
        ),
        Paragraph("6.3.4 Dense Embedding Vectorization", h2_style),
        Paragraph(
            "Each chunk is passed to the all-MiniLM-L6-v2 model, which computes a 384-dimensional dense semantic vector representing the passage's conceptual meaning.",
            body_style
        ),
        Paragraph("6.3.5 Handling Missing or Corrupt Documents", h2_style),
        Paragraph(
            "The ingestion pipeline implements exception handling to bypass corrupted files and log parsing warnings without interrupting batch processing.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p28)

    # =========================================================================
    # PAGE 29: 6.4 FEATURE ENGINEERING AND EXTRACTION
    # =========================================================================
    p29 = [
        Paragraph("6.4 Feature Engineering and Extraction", h1_style),
        Paragraph(
            "In retrieval-augmented generation systems, feature engineering centers on semantic representation, similarity scoring, and query intent extraction.",
            body_style
        ),
        Paragraph("6.4.1 Semantic Embedding Vectors", h2_style),
        Paragraph(
            "Dense embeddings map discrete words and sentences into a continuous mathematical vector space where semantically similar concepts reside in close spatial proximity, overcoming the vocabulary mismatch limitations of keyword search.",
            body_style
        ),
        Paragraph("6.4.2 Cosine Distance Metric", h2_style),
        Paragraph(
            "Semantic similarity between query vector $u$ and document chunk vector $v$ is computed using cosine distance:",
            body_style
        ),
        Paragraph(
            "Cosine Distance = 1.0 - [ (u &bull; v) / ( ||u|| ||v|| ) ]",
            caption_style
        ),
        Paragraph(
            "A cosine distance close to 0.0 indicates extreme semantic alignment, whereas values approaching 1.0 indicate orthogonal or unrelated content.",
            body_style
        ),
        Paragraph("6.4.3 Threshold-Based Routing Decisions", h2_style),
        Paragraph(
            "The query routing agent computes classification probabilities across candidate pathways, mapping queries with high temporal or breaking-news markers directly to the Web Search agent.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p29)

    # =========================================================================
    # PAGE 30: 6.5 MODEL ARCHITECTURE AND ALGORITHM DESIGN
    # =========================================================================
    p30 = [
        Paragraph("The implementation uses the following calibrated configuration thresholds:", body_noindent_style),
        Paragraph("&bull; SIMILARITY_DISTANCE_THRESH = 0.45", bullet_style),
        Paragraph("&bull; TOP_K_RETRIEVAL_CHUNKS = 4", bullet_style),
        Paragraph("&bull; MAX_WEB_SEARCH_RESULTS = 5", bullet_style),
        Paragraph("&bull; EVALUATION_MIN_CONFIDENCE = 0.70", bullet_style),
        Paragraph("6.5 Model Architecture and Algorithm Design", h1_style),
        Paragraph(
            "The core architecture couples a LangGraph cyclic state machine with an ensemble of agent nodes and cloud LLMs accessed via OpenRouter.",
            body_style
        ),
        Paragraph("The complete processing sequence executes as follows:", body_noindent_style),
        Paragraph("1. Query intake and state initialization inside AgentState dictionary.", bullet_style),
        Paragraph("2. Router agent executes zero-shot classification prompt via OpenRouter.", bullet_style),
        Paragraph("3. State machine evaluates conditional edge and directs flow to target agent node.", bullet_style),
        Paragraph("4. Retriever agent queries ChromaDB and extracts top-k nearest chunks.", bullet_style),
        Paragraph("5. Web Search agent queries DuckDuckGo and aggregates external snippets.", bullet_style),
        Paragraph("6. Synthesizer formats evidence context and prompts LLM to generate answer.", bullet_style),
        Paragraph("7. Evaluator grades Context Relevance, Groundedness, and Answer Relevance.", bullet_style),
        Paragraph("8. Completed state dictionary is returned to Streamlit for UI rendering.", bullet_style),
        Paragraph(
            "This state-driven architecture guarantees modularity, enabling developers to replace individual agents or adjust routing thresholds without altering other pipeline components.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p30)

    # =========================================================================
    # PAGE 31: 6.6 ROUTER & RETRIEVER IMPLEMENTATION & FIGURE 6.1
    # =========================================================================
    p31 = [
        Paragraph("6.6 Implementation of the Routing and Retrieval System", h1_style),
        Paragraph(
            "The routing and retrieval subsystem forms the analytical engine of the platform. The implementation consists of the following operational steps:",
            body_style
        ),
        Paragraph("1. Load OpenRouter API credentials and initialize OpenAI-compatible client.", bullet_style),
        Paragraph("2. Ingest user query and execute classification prompt in router.py.", bullet_style),
        Paragraph("3. Parse structured JSON response containing route choice and rationale.", bullet_style),
        Paragraph("4. If vector route chosen, invoke ChromaDB query in retriever.py.", bullet_style),
        Paragraph("5. Filter returned chunks based on SIMILARITY_DISTANCE_THRESH.", bullet_style),
        Paragraph("6. Inject retrieved chunks into shared state context list.", bullet_style),
        Spacer(1, 4),
        Image(img_6_1, width=USABLE_WIDTH, height=150),
        Paragraph("Figure 6.1: Multi-Agent Routing and Retrieval Sequence Flowchart.", caption_style),
        PageBreak()
    ]
    story.extend(p31)

    # =========================================================================
    # PAGE 32: 6.7 WEB SEARCH & SYNTHESIS IMPLEMENTATION & FIGURE 6.2
    # =========================================================================
    p32 = [
        Paragraph("6.7 Implementation of the Web Search and Synthesis System", h1_style),
        Paragraph(
            "The web search and synthesis subsystem handles external information gathering and multi-source context fusion. Implementation steps include:",
            body_style
        ),
        Paragraph("1. Initialize DuckDuckGo search client within web_search.py.", bullet_style),
        Paragraph("2. Format search query and retrieve top web page results.", bullet_style),
        Paragraph("3. Clean search snippets and map source URLs to citation indices.", bullet_style),
        Paragraph("4. Concatenate vector chunks and web snippets into unified prompt context.", bullet_style),
        Paragraph("5. Invoke Synthesizer LLM with strict grounding instructions.", bullet_style),
        Paragraph("6. Parse synthesized response, verifying in-line citation accuracy.", bullet_style),
        Spacer(1, 4),
        Image(img_6_2, width=USABLE_WIDTH, height=150),
        Paragraph("Figure 6.2: Multi-Source Context Fusion and Fallback Synthesis Flowchart.", caption_style),
        PageBreak()
    ]
    story.extend(p32)

    # =========================================================================
    # PAGE 33: 6.8 SYSTEM INTEGRATION, SECURITY & SUMMARY
    # =========================================================================
    p33 = [
        Paragraph("6.8 System Integration and Execution", h1_style),
        Paragraph(
            "The complete system integrates vector ingestion, agent state orchestration, external search tools, and web interface visualization into a single executable pipeline.",
            body_style
        ),
        Paragraph("Execution Procedure:", body_noindent_style),
        Paragraph("1. Clone repository and initialize Python virtual environment.", bullet_style),
        Paragraph("2. Install dependencies via pip install -r requirements.txt.", bullet_style),
        Paragraph("3. Configure OPENROUTER_API_KEY in .env configuration file.", bullet_style),
        Paragraph("4. Populate data/ directory with domain knowledge documents.", bullet_style),
        Paragraph("5. Execute data ingestion pipeline via python rag/vector_store.py.", bullet_style),
        Paragraph("6. Verify ChromaDB collection persistence and chunk counts.", bullet_style),
        Paragraph("7. Launch Streamlit web dashboard via streamlit run app.py.", bullet_style),
        Paragraph("8. Input test query and observe real-time agent execution trace.", bullet_style),
        Paragraph("9. Inspect retrieved context chunks, citations, and Triad metrics.", bullet_style),
        Paragraph("10. Evaluate offline fallback operation by disabling network access.", bullet_style),
        Paragraph("Security Considerations", h2_style),
        Paragraph(
            "API tokens are isolated strictly within local .env files and omitted from version control via .gitignore. No private user queries or proprietary enterprise documents are permanently stored on third-party servers.",
            body_style
        ),
        Paragraph("Summary", h1_style),
        Paragraph(
            "This chapter detailed the implementation of the six core modules, data preprocessing, feature engineering, routing logic, and system execution procedure.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p33)

    return story
