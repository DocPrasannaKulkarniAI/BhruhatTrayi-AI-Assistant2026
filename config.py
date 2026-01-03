"""
Configuration File
Bhruhat Trayi AI Assistant by PraKul

IMPORTANT: 
- Never share this file publicly
- Add config.py to .gitignore if using git
"""

# =============================================================================
# OPENAI API CONFIGURATION
# =============================================================================

# Your OpenAI API Key (Get from https://platform.openai.com/api-keys)
OPENAI_API_KEY = "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"

# Model to use
# - "gpt-4o-mini" = Cheapest, good quality (RECOMMENDED)
# - "gpt-4o" = Best quality, 10x more expensive
OPENAI_MODEL = "gpt-4o-mini"

# =============================================================================
# CHAT SETTINGS
# =============================================================================

# Maximum conversation history to maintain
MAX_CHAT_HISTORY = 20

# Maximum tokens in response
MAX_OUTPUT_TOKENS = 2048

# Temperature (0 = very focused/factual, 0.3 = balanced, 1 = creative)
# Lower = less hallucination, more factual
TEMPERATURE = 0.1

# =============================================================================
# APP SETTINGS
# =============================================================================

# AI Chatbot Name
CHATBOT_NAME = "AI TrayiDoota"
CHATBOT_NAME_SANSKRIT = "AI त्रयीदूत"

# Default settings
DEFAULT_ROLE = "Student"
DEFAULT_MAX_RESULTS = 10
