from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib import colors
from ref_styles import (
    title_style, h1_style, h2_style, body_style, body_noindent_style,
    bullet_style, caption_style, USABLE_WIDTH
)

def get_ch123_pages():
    story = []

    # =========================================================================
    # PAGE 1: CHAPTER 1 - INTRODUCTION & 1.1 BACKGROUND & 1.2 PROBLEM STATEMENT
    # =========================================================================
    p1 = [
        Paragraph("1. INTRODUCTION", title_style),
        Paragraph("1.1 Background of the Study", h1_style),
        Paragraph(
            "Large Language Models (LLMs) have achieved remarkable success in natural language processing and text generation. However, fundamental constraints limit their enterprise utility, specifically knowledge cutoff dates, factual hallucinations, and lack of access to private domain documents. Retrieval-Augmented Generation (RAG) addresses these issues by grounding LLMs with authoritative external knowledge.",
            body_style
        ),
        Paragraph(
            "Conventional RAG systems rely on static single-pass retrieval pipelines that convert queries into vector embeddings and retrieve top-k chunks. While effective for simple questions, static pipelines struggle with complex, multi-hop, or time-sensitive inquiries, frequently retrieving noisy context or hallucinating when internal databases lack answers.",
            body_style
        ),
        Paragraph(
            "The project titled \"Self-Adaptive Multi-Agent RAG Framework\" introduces an autonomous, state-driven multi-agent architecture. Built using Python, LangGraph, and ChromaDB, the system dynamically routes queries, conducts semantic vector searches, executes live web searches, and validates responses through automated evaluation.",
            body_style
        ),
        Paragraph(
            "The framework leverages the OpenRouter API for multi-model inference and provides an interactive Streamlit web dashboard for real-time visualization of agent decision traces and confidence scores.",
            body_style
        ),
        Paragraph("1.2 Problem Statement", h1_style),
        Paragraph(
            "Manual information retrieval across disparate repositories is slow and prone to oversight. Traditional single-agent RAG treats all queries identically, wasting compute on simple greetings while failing on complex multi-hop inquiries.",
            body_style
        ),
        Paragraph(
            "Existing systems lack real-time web fallbacks and automated self-verification mechanisms. These limitations create an urgent need for an integrated, self-adaptive multi-agent solution.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p1)

    # =========================================================================
    # PAGE 2: 1.2 CONT, 1.3 OBJECTIVES OF THE PROJECT, 1.4 SCOPE OF THE PROJECT
    # =========================================================================
    p2 = [
        Paragraph(
            "Therefore, there is an urgent need for an integrated, self-adaptive multi-agent system that dynamically determines the optimal retrieval path, integrates live web search when internal databases are insufficient, and evaluates answer faithfulness in real time.",
            body_style
        ),
        Paragraph(
            "This project aims to develop a robust, modular multi-agent RAG platform that dynamically coordinates specialized agents through a state machine, incorporates live web search fallbacks, and executes automated RAG Triad evaluations.",
            body_style
        ),
        Paragraph("1.3 Objectives of the Project", h1_style),
        Paragraph("The main objectives of the project are:", body_noindent_style),
        Paragraph(
            "1. To develop a modular, self-adaptive multi-agent RAG framework using Python, LangGraph, and the OpenRouter API.",
            bullet_style
        ),
        Paragraph(
            "2. To implement an intelligent Query Router agent that categorizes queries into Direct LLM, Vector Retrieval, Live Web Search, or Hybrid execution paths.",
            bullet_style
        ),
        Paragraph(
            "3. To design and deploy a dense semantic vector database using ChromaDB and Sentence-Transformers for domain document retrieval.",
            bullet_style
        ),
        Paragraph(
            "4. To integrate a real-time Web Search Agent using DuckDuckGo to handle temporal, volatile, and open-domain inquiries.",
            bullet_style
        ),
        Paragraph(
            "5. To construct a Multi-Source Answer Synthesizer that merges vector chunks and web snippets with explicit source attribution.",
            bullet_style
        ),
        Paragraph(
            "6. To implement an automated RAG Triad Evaluator measuring Context Relevance, Groundedness, and Answer Relevance with an interactive Streamlit UI.",
            bullet_style
        ),
        Paragraph("1.4 Scope of the Project", h1_style),
        Paragraph(
            "The scope of this project encompasses query intent classification, multi-agent workflow orchestration, persistent vector indexing, real-time web information extraction, context synthesis, and quantitative evaluation.",
            body_style
        ),
        Paragraph(
            "The prototype processes internal knowledge corpora across diverse domains including Artificial Intelligence, Healthcare, and Finance, while utilizing live DuckDuckGo search queries for real-time validation and updates.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p2)

    # =========================================================================
    # PAGE 3: 1.4 CONT & 1.5 SIGNIFICANCE OF THE PROJECT
    # =========================================================================
    p3 = [
        Paragraph(
            "The system incorporates deterministic offline fallback synthesizers to ensure uninterrupted operation during network outages or external API rate limits, making it highly resilient for academic demonstration and enterprise testing.",
            body_style
        ),
        Paragraph(
            "The scope is restricted to textual document ingestion (PDF, Markdown, TXT) and structured web text scraping. Audio, video, and non-textual multimedia formats are reserved for future architectural enhancements.",
            body_style
        ),
        Paragraph(
            "The framework serves as an extensible software prototype designed to validate adaptive multi-agent retrieval concepts and is not intended to directly replace commercial search engines without further horizontal scaling.",
            body_style
        ),
        Paragraph("1.5 Significance of the Project", h1_style),
        Paragraph(
            "This project demonstrates how multi-agent collaboration and state-machine orchestration can eliminate the core failure modes of standard RAG pipelines, including retrieval hallucinations, context drowning, and outdated knowledge.",
            body_style
        ),
        Paragraph(
            "By implementing dynamic routing, the system conserves substantial computational resources and API token expenditure by bypassing expensive vector retrievals for straightforward conversational queries, reserving complex hybrid pipelines only for demanding requests.",
            body_style
        ),
        Paragraph(
            "The integration of the OpenRouter API democratizes access to advanced LLM capabilities by allowing developers to switch dynamically between free-tier models and state-of-the-art frontier models without rewriting codebase logic.",
            body_style
        ),
        Paragraph(
            "Furthermore, embedding an automated RAG Triad evaluation loop directly into the response lifecycle provides unprecedented transparency and reliability for enterprise knowledge workers and academic researchers.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p3)

    # =========================================================================
    # PAGE 4: CHAPTER 2 - LITERATURE SURVEY / EXISTING STUDIES & 2.1 REVIEW
    # =========================================================================
    p4 = [
        Paragraph("2. LITERATURE SURVEY / EXISTING STUDIES", title_style),
        Paragraph("2.1 Review of Existing Systems and Research Works", h1_style),
        Paragraph(
            "Retrieval-Augmented Generation has evolved rapidly since its formal introduction by Lewis et al. in 2020. The foundational paradigm augmented pre-trained language models with external dense passage retrieval, dramatically reducing knowledge memorization requirements. However, early implementations relied on static dual-encoder mechanisms that suffered from low retrieval precision and poor cross-domain generalization.",
            body_style
        ),
        Paragraph(
            "Gao et al. (2023) surveyed advanced RAG architectures, categorizing them into Naive, Advanced, and Modular RAG. Advanced RAG incorporates pre-retrieval query rewriting, sentence-window chunking, and post-retrieval re-ranking. While these enhancements improved retrieval precision, the underlying execution flow remained fundamentally linear and incapable of autonomous decision-making.",
            body_style
        ),
        Paragraph(
            "To introduce self-correction, Asai et al. (2023) proposed Self-RAG, an architecture that trains models to output special reflection tokens determining whether retrieval is necessary and evaluating chunk relevance. Similarly, Yan et al. (2024) introduced Corrective RAG (CRAG), which evaluates retrieved documents and dynamically triggers web search when retrieval confidence falls below a set threshold.",
            body_style
        ),
        Paragraph(
            "Jeong et al. (2024) developed Adaptive-RAG, demonstrating that query complexity classification can dynamically select between non-retrieval, single-step retrieval, and multi-step iterative retrieval strategies. However, existing implementations are frequently coupled to proprietary LLM APIs and lack modular, multi-agent frameworks capable of executing hybrid retrieval with automated Triad validation.",
            body_style
        ),
        Paragraph(
            "LangGraph and LangChain emerged as state-of-the-art developer frameworks for coordinating stateful multi-agent workflows using directed cyclic graphs, enabling resilient agent collaboration, cyclic reflection loops, and persistent session state.",
            body_style
        ),
        Paragraph(
            "In parallel, vector databases such as ChromaDB, FAISS, and Qdrant provided high-performance HNSW vector indexing, enabling sub-millisecond similarity search across millions of embedded text representations.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p4)

    # =========================================================================
    # PAGE 5: 2.1 CONT, 2.2 COMPARATIVE ANALYSIS, 2.3 RESEARCH GAP
    # =========================================================================
    p5 = [
        Paragraph(
            "For quantitative performance benchmarking, the RAG Triad framework formalized by TruLens establishes three essential dimensions: Context Relevance, Groundedness (Faithfulness), and Answer Relevance, ensuring rigorous end-to-end evaluation.",
            body_style
        ),
        Paragraph("2.2 Comparative Analysis", h1_style),
        Paragraph(
            "Existing retrieval systems differ significantly in their orchestration paradigms, information sources, latency profiles, and verification capabilities.",
            body_style
        ),
        Paragraph(
            "Naive RAG frameworks execute fixed retrieval for every prompt, introducing unnecessary latency on simple queries and completely failing when required knowledge is absent from the local index. Single-agent iterative frameworks improve flexibility but suffer from high token costs and single-point-of-failure vulnerabilities.",
            body_style
        ),
        Paragraph(
            "The proposed Self-Adaptive Multi-Agent RAG Framework leverages LangGraph to decouple responsibilities across specialized, single-purpose agents. Unlike traditional pipelines, it dynamically chooses between direct answering, local vector retrieval, live web search, and hybrid multi-source synthesis based on semantic query classification.",
            body_style
        ),
        Paragraph(
            "Furthermore, it bridges the gap between private enterprise corpora and real-time internet knowledge, guaranteeing comprehensive information coverage at a fraction of the operating cost.",
            body_style
        ),
        Paragraph("2.3 Research Gap and Limitations of Existing Systems", h1_style),
        Paragraph(
            "Most commercial and open-source RAG architectures suffer from architectural rigidity. They assume that local vector collections are always complete, up to date, and sufficient to answer all incoming user inquiries.",
            body_style
        ),
        Paragraph(
            "When queries involve real-time events, market developments, or out-of-domain concepts, existing systems generate authoritative-sounding hallucinations because they cannot query the live internet dynamically.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p5)

    # =========================================================================
    # PAGE 6: 2.3 CONT & 2.4 PROPOSED SYSTEM AND PROPOSED APPROACH
    # =========================================================================
    p6 = [
        Paragraph(
            "A second major limitation is the absence of real-time automated verification. Production pipelines generally return generated text to the user without validating whether the LLM hallucinated beyond the retrieved context.",
            body_style
        ),
        Paragraph(
            "Finally, heavy dependency on single commercial API providers creates high recurring costs, rate-limit vulnerability, and service outage risks for developers.",
            body_style
        ),
        Paragraph("2.4 Proposed System and Proposed Approach", h1_style),
        Paragraph(
            "The proposed system, titled \"Self-Adaptive Multi-Agent RAG Framework,\" establishes an autonomous, multi-agent architecture orchestrated through LangGraph state machines.",
            body_style
        ),
        Paragraph(
            "The framework comprises five specialized agents: Query Router, Domain Vector Retriever, Live Web Searcher, Multi-Source Synthesizer, and Automated Triad Evaluator. Incoming queries are first classified into one of four routing pathways based on complexity and temporal intent.",
            body_style
        ),
        Paragraph(
            "For domain inquiries, the Retriever agent extracts semantically aligned chunks from a persistent ChromaDB database. When queries demand real-time information or when vector confidence is insufficient, the Web Search agent executes targeted DuckDuckGo queries.",
            body_style
        ),
        Paragraph(
            "The Synthesizer agent aggregates evidence from both knowledge channels, generating a coherent, context-grounded response with explicit source citations. The Evaluator agent then computes RAG Triad metrics to verify context relevance and groundedness.",
            body_style
        ),
        Paragraph(
            "Robust deterministic fallback logic guarantees 100% operational uptime by seamlessly serving structured answers even if cloud API keys encounter rate limits or network interruptions.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p6)

    # =========================================================================
    # PAGE 7: CHAPTER 3 - SOFTWARE REQUIREMENT ANALYSIS & 3.1 HARDWARE
    # =========================================================================
    table_31_data = [
        [Paragraph("<b>Component</b>", body_noindent_style), Paragraph("<b>Minimum / Recommended Requirement</b>", body_noindent_style)],
        [Paragraph("Computer or Laptop", body_noindent_style), Paragraph("Windows 10/11, Linux (Ubuntu 20.04+), or macOS", body_noindent_style)],
        [Paragraph("Processor", body_noindent_style), Paragraph("Multi-core CPU (Intel Core i5/i7 11th Gen+ or AMD Ryzen 5/7)", body_noindent_style)],
        [Paragraph("RAM", body_noindent_style), Paragraph("Minimum 8 GB recommended (16 GB for vector caching)", body_noindent_style)],
        [Paragraph("Storage", body_noindent_style), Paragraph("Minimum 10 GB free SSD storage for vector collections & models", body_noindent_style)],
        [Paragraph("Network Connection", body_noindent_style), Paragraph("Broadband internet connection for OpenRouter API and web scraping", body_noindent_style)],
        [Paragraph("GPU (Optional)", body_noindent_style), Paragraph("NVIDIA GPU with 4 GB+ VRAM for accelerated local embedding", body_noindent_style)]
    ]
    t31 = Table(table_31_data, colWidths=[150, USABLE_WIDTH - 150])
    t31.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))

    p7 = [
        Paragraph("3. SOFTWARE REQUIREMENT ANALYSIS", title_style),
        Paragraph("3.1 Hardware Specification", h1_style),
        Paragraph(
            "The hardware requirements define the physical computing infrastructure needed to develop, execute, and benchmark the Self-Adaptive Multi-Agent RAG Framework.",
            body_style
        ),
        Paragraph(
            "Because the system utilizes cloud-based LLM inference via the OpenRouter API alongside local embedding generation, high-end server clusters are not mandatory. A modern workstation or laptop with standard multi-core processing and sufficient RAM can comfortably execute the complete pipeline.",
            body_style
        ),
        Paragraph("The recommended hardware requirements are detailed below.", body_noindent_style),
        Spacer(1, 4),
        Paragraph("Table 3.1: Hardware Requirements", caption_style),
        t31,
        PageBreak()
    ]
    story.extend(p7)

    # =========================================================================
    # PAGE 8: 3.2 SOFTWARE SPECIFICATION
    # =========================================================================
    table_32_data = [
        [Paragraph("<b>Software / Technology</b>", body_noindent_style), Paragraph("<b>Purpose</b>", body_noindent_style)],
        [Paragraph("Python 3.10 / 3.11", body_noindent_style), Paragraph("Core programming language for pipeline development", body_noindent_style)],
        [Paragraph("LangGraph & LangChain", body_noindent_style), Paragraph("State machine framework for multi-agent graph orchestration", body_noindent_style)],
        [Paragraph("ChromaDB", body_noindent_style), Paragraph("Persistent vector database for dense semantic embeddings", body_noindent_style)],
        [Paragraph("Sentence-Transformers", body_noindent_style), Paragraph("Generates dense embeddings (all-MiniLM-L6-v2, 384 dimensions)", body_noindent_style)],
        [Paragraph("DuckDuckGo Search API", body_noindent_style), Paragraph("Live web scraping for real-time external knowledge retrieval", body_noindent_style)],
        [Paragraph("OpenRouter API", body_noindent_style), Paragraph("Gateway for unified multi-model LLM inference and reasoning", body_noindent_style)],
        [Paragraph("Streamlit", body_noindent_style), Paragraph("Interactive web application framework for UI and visual traces", body_noindent_style)],
        [Paragraph("Operating System", body_noindent_style), Paragraph("Windows, Linux, or macOS execution environment", body_noindent_style)]
    ]
    t32 = Table(table_32_data, colWidths=[150, USABLE_WIDTH - 150])
    t32.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))

    p8 = [
        Paragraph("3.2 Software Specification", h1_style),
        Paragraph(
            "The software requirements encompass the runtime libraries, language environments, database drivers, and cloud services required to execute the framework.",
            body_style
        ),
        Paragraph(
            "The software stack was selected to maximize open-source reproducibility, minimize external vendor lock-in, and provide high developer productivity.",
            body_style
        ),
        Paragraph("Table 3.2: Software Specification", caption_style),
        t32,
        Spacer(1, 6),
        Paragraph(
            "The exact versions of all installed software packages are maintained inside requirements.txt to facilitate seamless reproduction across environments.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p8)

    # =========================================================================
    # PAGE 9: 3.3 SOFTWARE TOOLS AND THEIR FEATURES
    # =========================================================================
    p9 = [
        Paragraph("3.3 Software Tools and Their Features", h1_style),
        Paragraph("Python", h2_style),
        Paragraph(
            "Python serves as the primary programming language for the framework. Its extensive ecosystem of machine learning libraries, native asynchronous support, and rich text-processing toolkits make it ideal for orchestrating agent workflows and data pipelines.",
            body_style
        ),
        Paragraph("LangGraph", h2_style),
        Paragraph(
            "LangGraph is a library designed for building stateful, multi-actor applications with LLMs using directed graphs. It allows developers to define complex cycles, conditional branching, and shared state schemas, making it the architectural backbone of our multi-agent coordination.",
            body_style
        ),
        Paragraph("ChromaDB", h2_style),
        Paragraph(
            "ChromaDB is an open-source, AI-native embedding database. It provides lightweight, serverless, and persistent vector storage with built-in HNSW indexing, enabling rapid nearest-neighbor similarity searches over document collections.",
            body_style
        ),
        Paragraph("Sentence-Transformers", h2_style),
        Paragraph(
            "The Sentence-Transformers library is utilized with the all-MiniLM-L6-v2 model to map sentences and paragraphs into a dense 384-dimensional vector space, capturing rich semantic relationships with negligible inference latency.",
            body_style
        ),
        Paragraph("DuckDuckGo Search", h2_style),
        Paragraph(
            "DuckDuckGo Search provides privacy-focused web search capabilities without requiring commercial API keys. It enables the Web Search Agent to retrieve real-time external articles, documentation, and news snippets dynamically.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p9)

    # =========================================================================
    # PAGE 10: TOOLS CONT & SUMMARY OF CHAPTER 3
    # =========================================================================
    p10 = [
        Paragraph("OpenRouter API", h2_style),
        Paragraph(
            "OpenRouter provides a unified, OpenAI-compatible API interface that bridges access to dozens of leading LLM providers, including open-source models (Meta Llama, Mistral, Gemma) and commercial models. It features automatic model routing, cost controls, and fallback switching.",
            body_style
        ),
        Paragraph("Streamlit Web Framework", h2_style),
        Paragraph(
            "Streamlit is used to build the front-end user interface. It renders reactive chat dialogues, agent execution status badges, vector chunk inspection accordions, and interactive RAG Triad evaluation scorecards without requiring complex JavaScript frameworks.",
            body_style
        ),
        Paragraph("Development Environment and IDE", h2_style),
        Paragraph(
            "The project was engineered using Visual Studio Code and Cursor, providing integrated debugging, Git source control management, and linting capabilities.",
            body_style
        ),
        Paragraph("Summary", h1_style),
        Paragraph(
            "This chapter defined the physical hardware requirements, software libraries, and external services necessary to build and run the Self-Adaptive Multi-Agent RAG Framework. The architecture balances lightweight local computing with scalable cloud LLM inference.",
            body_style
        ),
        Paragraph(
            "By integrating Python, LangGraph, ChromaDB, Sentence-Transformers, DuckDuckGo, OpenRouter, and Streamlit, the system establishes a flexible, cost-effective platform for high-accuracy information retrieval and automated answer validation.",
            body_style
        ),
        PageBreak()
    ]
    story.extend(p10)

    return story
