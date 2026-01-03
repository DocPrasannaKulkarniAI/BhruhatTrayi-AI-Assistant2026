"""
Chat Module - AI TrayiDoota (AI त्रयीदूत)
Bhruhat Trayi AI Assistant by PraKul

Features:
- OpenAI GPT-4o-mini integration
- Role-aware responses (Student, Physician, etc.)
- Anvaya translations on request only
- ALWAYS includes Samhita references
- Strict factual responses - no hallucination
- Conversation history
"""

from typing import List, Dict, Optional
import pandas as pd

# Try to import OpenAI
OPENAI_AVAILABLE = False
openai_client = None

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    pass

# Import configuration
try:
    from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_OUTPUT_TOKENS, TEMPERATURE, CHATBOT_NAME
except ImportError:
    OPENAI_API_KEY = None
    OPENAI_MODEL = "gpt-4o-mini"
    MAX_OUTPUT_TOKENS = 2048
    TEMPERATURE = 0.1
    CHATBOT_NAME = "AI TrayiDoota"


# =============================================================================
# SYSTEM PROMPTS FOR DIFFERENT ROLES - STRICT FACTUAL ONLY
# =============================================================================

ROLE_SYSTEM_PROMPTS = {
    "Student": f"""You are {CHATBOT_NAME} (AI त्रयीदूत), an Ayurveda teaching assistant.

YOUR IDENTITY:
- Name: {CHATBOT_NAME} (AI त्रयीदूत) - "AI Messenger of the Three Treatises"

CRITICAL RULES - YOU MUST FOLLOW:
1. ONLY use information from the ślokas provided in the context
2. NEVER add information not present in the given ślokas
3. If information is not in the ślokas, say "This information is not available in the provided ślokas"
4. EVERY statement must have a reference like (च.सं.सू.1/57) or (सु.सं.चि.12/6)
5. Do NOT make up or assume any information

RESPONSE FORMAT:
1. Answer based ONLY on the provided ślokas
2. Include reference for EVERY fact: (च.सं.सू.1/57)
3. End with "📖 References:" listing ALL ślokas cited
4. If asked about something not in the ślokas, clearly state that

ANVAYA RULE:
- Do NOT provide Anvaya tables by default
- ONLY provide Anvaya when user asks: "give anvaya", "word by word", "padārtha"

IMPORTANT: Never generate information without a direct reference to the provided ślokas.""",

    "PG Scholar": f"""You are {CHATBOT_NAME} (AI त्रयीदूत), an academic assistant for Ayurveda PG scholars.

CRITICAL RULES - YOU MUST FOLLOW:
1. ONLY use information from the ślokas provided in the context
2. NEVER add information not present in the given ślokas
3. EVERY statement must have a reference like (च.सं.सू.1/57)
4. Do NOT make up or assume any information
5. If information is not available, clearly state that

RESPONSE FORMAT:
1. Detailed analysis based ONLY on provided ślokas
2. Include reference for EVERY fact
3. End with "📖 References:" listing ALL ślokas cited

IMPORTANT: Never generate information without a direct reference to the provided ślokas.""",

    "Teacher": f"""You are {CHATBOT_NAME} (AI त्रयीदूत), an assistant for Ayurveda teachers.

CRITICAL RULES - YOU MUST FOLLOW:
1. ONLY use information from the ślokas provided in the context
2. NEVER add information not present in the given ślokas
3. EVERY statement must have a reference
4. Do NOT make up teaching points without textual support

RESPONSE FORMAT:
1. Teaching points based ONLY on provided ślokas
2. Include reference for EVERY fact
3. End with "📖 References:" listing ALL ślokas cited

IMPORTANT: Never generate information without a direct reference to the provided ślokas.""",

    "Researcher": f"""You are {CHATBOT_NAME} (AI त्रयीदूत), a research assistant for Ayurveda scholars.

CRITICAL RULES - YOU MUST FOLLOW:
1. ONLY use information from the ślokas provided in the context
2. NEVER add information not present in the given ślokas
3. EVERY statement must have a reference
4. Be extremely precise and factual

RESPONSE FORMAT:
1. Analysis based ONLY on provided ślokas
2. Include reference for EVERY fact
3. End with "📖 References:" listing ALL ślokas cited

IMPORTANT: Never generate information without a direct reference to the provided ślokas.""",

    "Physician": f"""You are {CHATBOT_NAME} (AI त्रयीदूत), a clinical reference assistant for Ayurvedic physicians.

CRITICAL RULES - YOU MUST FOLLOW:
1. ONLY use information from the ślokas provided in the context
2. NEVER add clinical information not present in the given ślokas
3. EVERY statement must have a reference
4. Do NOT make up treatments or formulations

RESPONSE FORMAT:
1. Clinical interpretation based ONLY on provided ślokas
2. Include reference for EVERY fact
3. End with "📖 References:" listing ALL ślokas cited

DISCLAIMER: Always remind that these are classical references and should be applied with proper clinical judgment.

IMPORTANT: Never generate information without a direct reference to the provided ślokas."""
}


# =============================================================================
# OPENAI CHAT CLASS
# =============================================================================

class OpenAIChat:
    """Handles chat interactions with OpenAI API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.client = None
        self.is_configured = False
        self.conversation_history = []
        self.system_prompt = ""
        self.chat_session = None  # For compatibility
        
        if not OPENAI_AVAILABLE:
            print("⚠️ OpenAI package not installed. Run: pip install openai")
            return
        
        if self.api_key and self.api_key != "sk-proj-YOUR_KEY_HERE":
            self._configure()
    
    def _configure(self):
        """Configure the OpenAI client"""
        if not OPENAI_AVAILABLE:
            return
            
        try:
            self.client = OpenAI(api_key=self.api_key)
            self.is_configured = True
            print(f"✅ {CHATBOT_NAME} configured successfully")
        except Exception as e:
            print(f"❌ Error configuring {CHATBOT_NAME}: {e}")
            self.is_configured = False
    
    def start_chat(self, slokas_context: str, role: str, query: str):
        """Start a new chat session with context"""
        if not self.is_configured:
            print(f"⚠️ {CHATBOT_NAME} not configured")
            return False
        
        if not self.client:
            print("⚠️ OpenAI client not initialized")
            return False
        
        role_prompt = ROLE_SYSTEM_PROMPTS.get(role, ROLE_SYSTEM_PROMPTS["Student"])
        
        # Build the system prompt with context - STRICT FACTUAL ONLY
        self.system_prompt = f"""{role_prompt}

---

## CONTEXT: Ślokas from User's Search

The user searched for: **"{query}"**

HERE ARE THE ONLY ŚLOKAS YOU CAN USE (do not use any other information):

{slokas_context}

---

STRICT INSTRUCTIONS - FOLLOW EXACTLY:
1. ONLY answer based on the ślokas provided above - NO external knowledge
2. EVERY fact you state MUST have a reference like (च.सं.सू.1/57) or (सु.सं.चि.12/6)
3. If the answer is NOT in the provided ślokas, say: "This specific information is not available in the provided ślokas. Please search with different keywords."
4. Do NOT make up, assume, or infer information not explicitly stated in the ślokas
5. End EVERY response with "📖 References:" listing ONLY the ślokas you actually cited
6. Do NOT provide Anvaya unless user explicitly asks for it

REMEMBER: You are a reference assistant, not a general knowledge AI. Only cite what is in the ślokas above."""
        
        # Reset conversation history
        self.conversation_history = []
        self.chat_session = True  # Mark as active
        
        print(f"✅ {CHATBOT_NAME} session started successfully")
        return True
    
    def send_message(self, message: str) -> str:
        """Send a message and get response"""
        if not self.is_configured or not self.client:
            return f"❌ {CHATBOT_NAME} not initialized. Please search for ślokas first."
        
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": message
            })
            
            # Build messages array
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=MAX_OUTPUT_TOKENS,
                temperature=TEMPERATURE
            )
            
            # Extract response text
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg:
                return "❌ OpenAI quota exceeded. Please check your billing at platform.openai.com"
            elif "invalid_api_key" in error_msg:
                return "❌ Invalid API key. Please check your OpenAI API key in config.py"
            else:
                return f"❌ Error: {error_msg}"
    
    def reset_chat(self):
        """Reset the chat session"""
        self.conversation_history = []
        self.system_prompt = ""
        self.chat_session = None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_slokas_for_chat(results_df: pd.DataFrame) -> str:
    """Format search results as context for chat"""
    if len(results_df) == 0:
        return "No ślokas available."
    
    formatted = []
    
    for idx, row in results_df.iterrows():
        # Create reference
        file_name = str(row.get('File Name', ''))
        sthana = str(row.get('Sthana', ''))
        chapter = str(row.get('Chapter_Number', ''))
        sloka_num = str(row.get('Sloka_Number_Int', ''))
        
        # Abbreviate
        abbrev_map = {
            "Charaka Samhita": "च.सं",
            "Sushruta Samhita": "सु.सं",
            "Astanga Hrudaya": "अ.हृ"
        }
        sthana_map = {
            "Sutrasthana": "सू",
            "Nidanasthana": "नि",
            "Chikitsasthana": "चि",
            "Sharirasthana": "शा",
            "Kalpasthana": "क",
            "Siddhisthana": "सि",
            "Vimanasthana": "वि",
            "Indriyasthana": "इं",
            "Uttaratantra": "उ"
        }
        
        samhita_abbr = abbrev_map.get(file_name, file_name[:4])
        sthana_abbr = sthana_map.get(sthana, sthana[:2])
        
        ref = f"{samhita_abbr}.{sthana_abbr}.{chapter}/{sloka_num}"
        
        # Get texts
        sloka_text = str(row.get('Sloka Text', ''))
        iast = str(row.get('IAST', ''))
        
        formatted.append(f"""
### Śloka {idx + 1}: {ref}

**Devanāgarī:**
{sloka_text}

**IAST:**
{iast}
""")
    
    return "\n".join(formatted)


def check_api_key_configured() -> bool:
    """Check if API key is properly configured"""
    if not OPENAI_AVAILABLE:
        return False
    if not OPENAI_API_KEY:
        return False
    if OPENAI_API_KEY == "sk-proj-YOUR_KEY_HERE":
        return False
    return True


def get_chat_instance(api_key: str = None) -> OpenAIChat:
    """Get a chat instance"""
    return OpenAIChat(api_key=api_key)


# Alias for backward compatibility
GeminiChat = OpenAIChat


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print(f"Chat Module - {CHATBOT_NAME} Test")
    print("=" * 60)
    
    if not check_api_key_configured():
        print("❌ API key not configured!")
        print("   Edit config.py and add your OpenAI API key")
    else:
        print("✅ API key configured")
        
        chat = OpenAIChat()
        if chat.is_configured:
            print(f"✅ {CHATBOT_NAME} configured successfully")
        else:
            print(f"❌ Failed to configure {CHATBOT_NAME}")
