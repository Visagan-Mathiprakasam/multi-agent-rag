"""
Central configuration for the Multi-Agent RAG Framework.
All configurable parameters are defined here.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Keys ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")


def get_api_key():
    """Retrieve current OpenRouter API key from environment or config."""
    return os.getenv("OPENROUTER_API_KEY", "") or OPENROUTER_API_KEY


# --- Model Configuration ---
LLM_MODEL = "openrouter/free"
AVAILABLE_MODELS = [
    "openrouter/free",
    "google/gemma-4-31b-it:free",
    "qwen/qwen3.8-27b:free",
    "nvidia/nemotron-3.5-lightning:free",
    "z-ai/glm-5.2:free",
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    "google/gemma-3-27b-it",
]
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- OpenRouter Config ---
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def get_active_model():
    """Return the currently selected model (overridable via env var)."""
    return os.getenv("ACTIVE_LLM_MODEL", LLM_MODEL)


# --- RAG Configuration ---
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 5  # Number of documents to retrieve

# --- Confidence Configuration ---
CONFIDENCE_THRESHOLD = 0.6  # Below this triggers re-retrieval
MAX_RETRIEVAL_ROUNDS = 2    # Maximum retrieval attempts

# --- Domains ---
DOMAINS = ["agriculture", "finance", "energy", "healthcare", "education"]

# Keywords for domain detection (used by the Coordinator Agent)
DOMAIN_KEYWORDS = {
    "agriculture": [
        "crop", "soil", "farm", "irrigation", "agriculture", "harvest",
        "fertilizer", "pest", "seed", "livestock", "farming", "cultivation",
        "plantation", "drought", "yield", "agricultural", "manure", "organic",
        "monsoon", "wheat", "rice", "maize", "cotton"
    ],
    "finance": [
        "finance", "investment", "budget", "stock", "loan", "interest",
        "tax", "revenue", "profit", "financial", "bank", "insurance",
        "portfolio", "risk", "return", "debt", "equity", "capital",
        "mutual fund", "savings", "cost", "expense", "money"
    ],
    "energy": [
        "energy", "solar", "wind", "electricity", "power", "renewable",
        "fossil", "nuclear", "grid", "battery", "fuel", "emission",
        "carbon", "watt", "kilowatt", "consumption", "photovoltaic",
        "turbine", "hydropower", "biomass", "coal", "oil", "gas"
    ],
    "healthcare": [
        "health", "medical", "disease", "treatment", "symptom", "diagnosis",
        "patient", "medicine", "hospital", "clinical", "doctor", "therapy",
        "nutrition", "vitamin", "deficiency", "iron", "anemia", "blood",
        "wellness", "diet", "exercise", "mental health", "infection"
    ],
    "education": [
        "education", "study", "learn", "student", "exam", "curriculum",
        "school", "university", "course", "teaching", "assessment", "grade",
        "academic", "homework", "lecture", "tutorial", "study plan",
        "learning", "scholarship", "research", "semester", "syllabus"
    ]
}

# --- Paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PERSIST_DIR = os.path.join(PROJECT_ROOT, "chroma_db")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# --- Complexity Thresholds ---
COMPLEXITY_WORD_THRESHOLD_MEDIUM = 10
COMPLEXITY_WORD_THRESHOLD_HIGH = 20
