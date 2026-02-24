from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from .env if present
load_dotenv()


def project_root() -> Path:
    """
    Resolve the project root directory.

    Assumes this file lives in `pmo_assistant/` under the project root.
    """
    return Path(__file__).resolve().parent.parent


BASE_DIR: Path = project_root()


# Original PMO artefact locations (Excel / Word / PPTX)
EXCEL_FILES = {
    "talent_pool": "Hackhathon_Pool Details.xlsx",
    "resource_allocation": "Hackhathon_Resource Allocation in Projects.xlsx",
    "resource_utilization": "Hackhathon_Resources Utilization_2025.xlsx",
    "resourcing_enablement": "Hackhathon_Resourcing and Enablement.xlsx",
    "third_party": "Hackhathon_Third Party Employees.xlsx",
    "csat": "CSAT - Customer ID and Name V1.0.xlsx",
    "dashboard_ddit": "Dashboard Data Dictionary - (DDIT).xlsx",
    "rca": "Projects - Root Cause Analysis (RCA) for Projects in RED or AMBER Status.xlsx",
    "project_plan": "Project ID - Project Name - Project Plan_V1.0.xlsx",
    "test_cases": "Test Cases - Project ID -Project Name V1.0.xlsx",
}

DOCX_FILES = {
    "brd_reference": "Reference BRD.docx",
    "tdd_reference": "Reference TDD.docx",
    "mom_template": "MoM - Customer Name-Monthly-Bi Weekly-Weekly-Meeting Title-YYYYMMDD.docx",
    "completion_certificate": "Project_Completion_Certificate.docx",
}

PPTX_FILES = {
    "weekly_status": "Template -Project ID - Project Name  - Weekly Status for Customer Name.pptx",
    "handover": "OppID - Opp Description - Proposal to Delivery Team Handover V1.0.pptx",
}


def resolve_file(relative_name: str) -> Path:
    """
    Resolve a file relative to BASE_DIR and return its full path.
    """
    return BASE_DIR / relative_name


# # Groq / LLM configuration
# GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")

# # Default model; can be overridden via env var
# GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# # Hugging Face / embeddings configuration
# EMBEDDING_MODEL_NAME: str = os.getenv(
#     "EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
# )

# # If true, use Hugging Face Inference / Endpoint embeddings (requires HF API key).
# # Otherwise, embeddings are computed locally via sentence-transformers.
# USE_HF_ENDPOINT_EMBEDDINGS: bool = os.getenv("USE_HF_ENDPOINT_EMBEDDINGS", "0").strip() in (
#     "1",
#     "true",
#     "True",
#     "yes",
#     "YES",
# )

# # LangChain's HF endpoint embeddings read token from HUGGINGFACEHUB_API_KEY
# HUGGINGFACEHUB_API_KEY: str | None = os.getenv("HUGGINGFACEHUB_API_KEY")

def get_groq_config() -> dict[str, str]:
    """Streamlit Cloud - ALWAYS uses st.secrets."""
    try:
        import streamlit as st
        
        # CLOUD: st.secrets (works 100%)
        api_key = st.secrets.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY missing in st.secrets!")
            
        return {
            "api_key": api_key,
            "model": st.secrets.get("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
        }
    except ImportError:
        # Not in Streamlit context
        raise RuntimeError("❌ Must run in Streamlit app! Deploy to share.streamlit.io")
    except Exception as e:
        raise RuntimeError(f"❌ Cloud config failed: {e}")

# HF Config - same pattern
def get_hf_config() -> dict[str, str | None]:
    """HF embeddings config."""
    try:
        import streamlit as st
        return {
            "api_key": st.secrets.get("HUGGINGFACEHUB_API_KEY"),
            "model_name": st.secrets.get("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"),
            "use_endpoint": st.secrets.get("USE_HF_ENDPOINT_EMBEDDINGS", "0").strip() in ("1", "true", "True", "yes", "YES")
        }
    except:
        raise RuntimeError("❌ Must run in Streamlit app!")

# Initialize globals
groq_config = get_groq_config()
GROQ_API_KEY = groq_config["api_key"]
GROQ_MODEL = groq_config["model"]

hf_config = get_hf_config()
EMBEDDING_MODEL_NAME = hf_config["model_name"]
USE_HF_ENDPOINT_EMBEDDINGS = hf_config["use_endpoint"]
HUGGINGFACEHUB_API_KEY = hf_config["api_key"]


