"""
Global configuration file for the Agentic Research Assistant
"""

import os

# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
AGENTS_DIR = os.path.join(BASE_DIR, "agents")
GRAPH_DIR = os.path.join(BASE_DIR, "graph")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

COURSE_FILE = os.path.join(DATA_DIR, "iisc_courses.json")
ROADMAP_OUTPUT = os.path.join(OUTPUT_DIR, "roadmap.txt")


# =========================================================
# LLM CONFIGURATION
# =========================================================

LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.2


# =========================================================
# PAPER SEARCH SETTINGS
# =========================================================

ARXIV_MAX_RESULTS = 40
BIORXIV_MAX_RESULTS = 40

PAPER_START_YEAR = "2023-01-01"


# =========================================================
# TREND ANALYSIS SETTINGS
# =========================================================

MAX_TREND_KEYWORDS = 15
MIN_PAPERS_FOR_TRENDS = 10


# =========================================================
# PAPER RECOMMENDATION SETTINGS
# =========================================================

TOP_PAPER_RECOMMENDATIONS = 5


# =========================================================
# EMBEDDING MODEL
# =========================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# =========================================================
# DEBUG / VERBOSE FLAGS
# =========================================================

DEBUG_MODE = True
PRINT_AGENT_STEPS = True