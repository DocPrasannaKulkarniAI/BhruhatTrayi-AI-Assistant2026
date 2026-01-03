"""
Bhruhat Trayi AI Assistant by PraKul
An AI initiative by Prof.(Dr.) Prasanna Kulkarni

Version 8.0 - Enhanced UI with AI TrayiDuta
============================================
- AI TrayiDuta (AI त्रयीदूत) chatbot integration
- Query disambiguation (Vata = Dosha vs Plant)
- Improved UI with tabular checkboxes
- Performance optimizations with caching
- Anvaya only on request
- Always includes references
- Clear input after AI response

Local Run: python -m streamlit run app.py
"""

import streamlit as st
import pandas as pd
import re
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime
import base64
import io

# =============================================================================
# PAGE CONFIG (Must be first Streamlit command)
# =============================================================================

st.set_page_config(
    page_title="Bhruhat Trayi AI Assistant by PraKul",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# IMPORTS - Custom Modules
# =============================================================================

from ayurvedic_synonyms import (
    AYURVEDIC_SYNONYMS, 
    MODERN_TO_CLASSICAL, 
    get_synonyms,
    check_modern_term,
    check_spelling,
    get_famous_keywords
)
from prompt_templates import (
    ROLE_INFO,
    generate_combined_prompt,
    format_slokas_for_prompt,
    get_role_icons
)
from query_analyzer import QueryAnalyzer, analyze_query
from enhanced_search import EnhancedSearch, enhanced_search

# Query disambiguation
try:
    from query_disambiguation import (
        get_disambiguation_suggestions,
        is_query_ambiguous,
        refine_query_with_meaning
    )
    DISAMBIGUATION_AVAILABLE = True
except ImportError:
    DISAMBIGUATION_AVAILABLE = False
    get_disambiguation_suggestions = lambda q: {"is_ambiguous": False}
    is_query_ambiguous = lambda q: False

# Chat module (optional)
CHAT_AVAILABLE = False
try:
    from chat_module import (
        OpenAIChat,
        GeminiChat,
        format_slokas_for_chat, 
        check_api_key_configured,
        get_chat_instance
    )
    CHAT_AVAILABLE = True
except ImportError:
    OpenAIChat = None
    GeminiChat = None
    format_slokas_for_chat = None
    check_api_key_configured = lambda: False
    get_chat_instance = None

# Config
try:
    from config import OPENAI_API_KEY, CHATBOT_NAME, CHATBOT_NAME_SANSKRIT
except ImportError:
    OPENAI_API_KEY = None
    CHATBOT_NAME = "AI TrayiDoota"
    CHATBOT_NAME_SANSKRIT = "AI त्रयीदूत"

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

APP_DIR = Path(__file__).parent
PARQUET_PATH = APP_DIR / "all3_cleaned.parquet"
EXCEL_PATH = APP_DIR / "all3_cleaned.xlsx"
LOGO_PATH = APP_DIR / "Atharva_Logo.jpg"

# =============================================================================
# CUSTOM CSS - Enhanced Styling
# =============================================================================

def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600&display=swap');
        
        /* ===== HEADER ===== */
        .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1.2rem;
            background: linear-gradient(135deg, #0D7377 0%, #14967A 50%, #1DB954 100%);
            padding: 1.2rem 2rem;
            border-radius: 15px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(13, 115, 119, 0.3);
        }
        
        .logo-img {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            border: 3px solid white;
            object-fit: cover;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .header-text {
            text-align: center;
            color: white;
        }
        
        .header-text h1 {
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        
        .header-text .subtitle {
            margin: 0.3rem 0 0 0;
            font-size: 1rem;
            opacity: 0.95;
            font-style: italic;
        }
        
        /* ===== TAB STYLING - BIGGER FONTS ===== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background: linear-gradient(90deg, #f0f4f8 0%, #e2e8f0 100%);
            padding: 12px;
            border-radius: 15px;
            border: 2px solid #e2e8f0;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            padding: 15px 30px !important;
            border-radius: 12px !important;
            background: white !important;
            border: 2px solid #cbd5e1 !important;
            transition: all 0.3s ease !important;
            min-width: 200px !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: #e0f2fe !important;
            border-color: #0D7377 !important;
            transform: translateY(-2px);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #0D7377, #14967A) !important;
            color: white !important;
            border-color: #0D7377 !important;
            box-shadow: 0 4px 12px rgba(13, 115, 119, 0.4) !important;
        }
        
        /* ===== SECTION HEADERS ===== */
        .section-header {
            color: #0D7377;
            font-size: 1.2rem;
            font-weight: 600;
            margin: 1.5rem 0 0.8rem 0;
            padding-bottom: 0.4rem;
            border-bottom: 3px solid #D4A03C;
        }
        
        /* ===== SELECTION BOX STYLING ===== */
        .selection-container {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 15px 20px;
            margin: 10px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        
        .selection-title {
            font-weight: 600;
            color: #0D7377;
            font-size: 1rem;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 2px solid #D4A03C;
        }
        
        /* ===== SLOKA CARDS ===== */
        .sloka-card {
            background: linear-gradient(135deg, #FFFAF0 0%, #FFF8E7 100%);
            border-radius: 12px;
            padding: 15px 20px;
            margin: 12px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            border-left: 5px solid #D4A03C;
        }
        
        .sloka-card.charaka { border-left-color: #2E7D32; }
        .sloka-card.sushruta { border-left-color: #1565C0; }
        .sloka-card.astanga { border-left-color: #E65100; }
        
        .sloka-ref {
            font-weight: 600;
            color: #0D7377;
            font-size: 0.95rem;
            margin-bottom: 10px;
        }
        
        .sloka-text {
            font-family: 'Noto Sans Devanagari', sans-serif;
            font-size: 1.15rem;
            line-height: 1.9;
            color: #2C3E50;
        }
        
        /* ===== SAMHITA BADGES ===== */
        .badge-charaka {
            background: linear-gradient(135deg, #2E7D32, #43A047);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
        }
        
        .badge-sushruta {
            background: linear-gradient(135deg, #1565C0, #1E88E5);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
        }
        
        .badge-astanga {
            background: linear-gradient(135deg, #E65100, #FB8C00);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            display: inline-block;
        }
        
        /* ===== CHAT STYLING ===== */
        .chat-header {
            background: linear-gradient(135deg, #0D7377, #14967A);
            color: white;
            padding: 18px 25px;
            border-radius: 15px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 18px;
            box-shadow: 0 4px 15px rgba(13, 115, 119, 0.3);
        }
        
        .chat-avatar {
            width: 55px;
            height: 55px;
            border-radius: 50%;
            background: linear-gradient(135deg, #D4A03C, #F4B942);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        
        .chat-info h3 {
            margin: 0;
            font-size: 1.4rem;
            font-weight: 600;
        }
        
        .chat-info p {
            margin: 3px 0 0 0;
            font-size: 0.95rem;
            opacity: 0.9;
        }
        
        .user-msg {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            padding: 14px 18px;
            border-radius: 15px;
            margin: 10px 0;
            border-left: 4px solid #1565C0;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }
        
        .bot-msg {
            background: linear-gradient(135deg, #f5f5f5, #eeeeee);
            padding: 14px 18px;
            border-radius: 15px;
            margin: 10px 0;
            border-left: 4px solid #0D7377;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }
        
        /* ===== DISAMBIGUATION BOX ===== */
        .disambig-box {
            background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
            border: 2px solid #FF9800;
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 3px 10px rgba(255, 152, 0, 0.2);
        }
        
        .disambig-title {
            color: #E65100;
            font-weight: 700;
            font-size: 1.15rem;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* ===== INFO BOXES ===== */
        .success-box {
            background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
            border-left: 5px solid #2E7D32;
            padding: 15px 20px;
            border-radius: 10px;
            margin: 12px 0;
        }
        
        .warning-box {
            background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
            border-left: 5px solid #FF9800;
            padding: 15px 20px;
            border-radius: 10px;
            margin: 12px 0;
        }
        
        .error-box {
            background: linear-gradient(135deg, #FFEBEE, #FFCDD2);
            border-left: 5px solid #D32F2F;
            padding: 15px 20px;
            border-radius: 10px;
            margin: 12px 0;
        }
        
        .info-box {
            background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
            border-left: 5px solid #1565C0;
            padding: 15px 20px;
            border-radius: 10px;
            margin: 12px 0;
        }
        
        /* ===== STATS BADGES ===== */
        .stats-container {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
            margin: 15px 0;
        }
        
        .stat-badge {
            background: linear-gradient(135deg, #0D7377, #14967A);
            color: white;
            padding: 10px 22px;
            border-radius: 25px;
            font-weight: 500;
            box-shadow: 0 3px 10px rgba(13, 115, 119, 0.3);
        }
        
        /* ===== FOOTER ===== */
        .footer {
            text-align: center;
            padding: 25px;
            margin-top: 40px;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
            color: #555;
        }
        
        /* ===== MOBILE RESPONSIVE ===== */
        @media (max-width: 768px) {
            .header-text h1 { font-size: 1.3rem !important; }
            .header-container { flex-direction: column; padding: 1rem; }
            .stTabs [data-baseweb="tab"] { 
                font-size: 1rem !important; 
                padding: 10px 15px !important;
                min-width: 120px !important;
            }
            .chat-header { flex-direction: column; text-align: center; }
        }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_session_state():
    defaults = {
        'search_history': [],
        'current_query': "",
        'confirmed_spelling': False,
        'chat_messages': [],
        'chat_context_slokas': None,
        'chat_context_query': "",
        'chat_context_role': "Student",
        'gemini_chat': None,
        'search_results': None,
        'selected_roles': ["Student"],
        'selected_samhitas': ["Charaka Samhita", "Sushruta Samhita", "Astanga Hrudaya"],
        'disambiguation_shown': False,
        'refined_query': None,
        'clear_chat_input': False,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =============================================================================
# DATA LOADING WITH CACHING (Performance Fix)
# =============================================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_database():
    """Load the database with caching for performance"""
    if PARQUET_PATH.exists():
        return pd.read_parquet(PARQUET_PATH)
    elif EXCEL_PATH.exists():
        return pd.read_excel(EXCEL_PATH)
    else:
        st.error("❌ Database not found! Place all3_cleaned.parquet in app folder.")
        st.stop()


@st.cache_data(ttl=3600, show_spinner=False)
def get_logo_base64():
    """Get logo as base64 string with caching"""
    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_samhita_class(file_name: str) -> str:
    if "Charaka" in file_name:
        return "charaka"
    elif "Sushruta" in file_name:
        return "sushruta"
    return "astanga"


def get_samhita_badge(file_name: str) -> str:
    if "Charaka" in file_name:
        return '<span class="badge-charaka">Charaka</span>'
    elif "Sushruta" in file_name:
        return '<span class="badge-sushruta">Suśruta</span>'
    return '<span class="badge-astanga">Aṣṭāṅga</span>'


def get_reference_code(row: pd.Series) -> str:
    abbrev_map = {"Charaka Samhita": "Ch", "Sushruta Samhita": "Su", "Astanga Hrudaya": "A.Hr"}
    sthana_map = {
        "Sutrasthana": "Sū", "Nidanasthana": "Ni", "Vimanasthana": "Vi",
        "Sharirasthana": "Śā", "Indriyasthana": "In", "Chikitsasthana": "Chi",
        "Kalpasthana": "Ka", "Siddhisthana": "Si", "Uttaratantra": "Ut"
    }
    samhita = abbrev_map.get(row['File Name'], row['File Name'][:2])
    sthana = sthana_map.get(row['Sthana'], row['Sthana'][:2])
    return f"{samhita}.{sthana}.{row['Chapter_Number']}/{row['Sloka_Number_Int']}"


def get_devanagari_reference(row: pd.Series) -> str:
    dev_nums = {'0': '०', '1': '१', '2': '२', '3': '३', '4': '४', 
                '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'}
    samhita_dev = {"Charaka Samhita": "च.सं", "Sushruta Samhita": "सु.सं", "Astanga Hrudaya": "अ.हृ"}
    sthana_dev = {
        "Sutrasthana": "सू", "Nidanasthana": "नि", "Vimanasthana": "वि",
        "Sharirasthana": "शा", "Indriyasthana": "इं", "Chikitsasthana": "चि",
        "Kalpasthana": "क", "Siddhisthana": "सि", "Uttaratantra": "उ"
    }
    samhita = samhita_dev.get(row['File Name'], "?")
    sthana = sthana_dev.get(row['Sthana'], "?")
    ch_num = ''.join(dev_nums.get(c, c) for c in str(row['Chapter_Number']))
    sl_num = ''.join(dev_nums.get(c, c) for c in str(row['Sloka_Number_Int']))
    return f"{samhita}.{sthana}.{ch_num}/{sl_num}"


def check_query_issues(query: str) -> Dict:
    """Check for spelling, modern terms, off-topic"""
    issues = {
        "spelling_suggestions": {},
        "modern_terms": [],
        "is_off_topic": False
    }
    
    # Off-topic check
    off_topic_words = ["python", "javascript", "programming", "code", "weather", "sports", "movie", "cricket", "football"]
    if any(w in query.lower() for w in off_topic_words):
        issues["is_off_topic"] = True
        return issues
    
    # Spelling check
    for word in query.lower().split():
        suggestion = check_spelling(word)
        if suggestion and suggestion.lower() != word.lower():
            issues["spelling_suggestions"][word] = suggestion
    
    # Modern terms
    for word in query.lower().split():
        mt = check_modern_term(word)
        if mt:
            issues["modern_terms"].append(mt)
    
    return issues


def get_query_suggestions(query: str) -> List[str]:
    """Get suggested alternative queries based on synonyms and common terms"""
    suggestions = []
    query_lower = query.lower().strip()
    words = query_lower.split()
    
    # Common Ayurvedic term mappings for suggestions
    term_suggestions = {
        # Dental terms
        "danta": ["danta dhavana (tooth brushing)", "danta roga (dental diseases)", "dantamula (gums)"],
        "davana": ["danta dhavana (tooth cleaning)", "dhavana (washing)"],
        "tooth": ["danta", "danta dhavana", "danta roga"],
        "teeth": ["danta", "danta dhavana", "dantaharsha"],
        "brushing": ["danta dhavana", "mukha prakshalana"],
        "dental": ["danta roga", "danta chikitsa"],
        
        # Doshas
        "vata": ["vata dosha", "vata vyadhi (vata diseases)", "vatashамаkа"],
        "pitta": ["pitta dosha", "pitta vyadhi", "pittashamaka"],
        "kapha": ["kapha dosha", "kapha vyadhi", "kaphashamaka"],
        "dosha": ["tridosha", "dosha prakopa", "dosha shamana"],
        
        # Common diseases - English
        "diabetes": ["prameha", "madhumeha"],
        "fever": ["jwara", "jvara"],
        "cough": ["kasa", "kāsa"],
        "cold": ["pratishyaya", "pinasa"],
        "headache": ["shiroroga", "shirahshula"],
        "skin": ["twak", "kushtha", "twak roga"],
        "arthritis": ["amavata", "sandhivata"],
        "asthma": ["shwasa", "tamaka shwasa"],
        "diarrhea": ["atisara"],
        "constipation": ["vibandha", "malabaddhata"],
        "acidity": ["amlapitta"],
        "obesity": ["sthaulya", "medoroga"],
        "anemia": ["pandu"],
        "jaundice": ["kamala"],
        
        # Body functions
        "digestion": ["agni", "jatharagni", "pachana"],
        "immunity": ["vyadhikshamatva", "ojas", "bala"],
        "strength": ["bala", "ojas"],
        "metabolism": ["agni", "dhatvagni"],
        "sleep": ["nidra", "swapna"],
        
        # Substances
        "oil": ["taila", "sneha", "abhyanga"],
        "ghee": ["ghrita", "ghṛta"],
        "milk": ["kshira", "dugdha", "go-kshira"],
        "honey": ["madhu", "kshaudra"],
        "water": ["jala", "udaka", "ambu"],
        "food": ["ahara", "anna", "bhojana"],
        
        # Treatments
        "exercise": ["vyayama"],
        "massage": ["abhyanga", "mardana"],
        "panchakarma": ["vamana", "virechana", "basti", "nasya", "raktamokshana"],
        "enema": ["basti", "vasti", "anuvasana"],
        "vomiting": ["vamana", "chardi"],
        "purgation": ["virechana"],
        "fasting": ["langhana", "upavasa"],
        "diet": ["ahara", "pathya"],
        
        # Body parts/tissues
        "blood": ["rakta", "rudhira", "shonita"],
        "bone": ["asthi"],
        "muscle": ["mamsa"],
        "fat": ["meda", "medas"],
        "marrow": ["majja"],
        "semen": ["shukra"],
        "plasma": ["rasa dhatu"],
        
        # Concepts
        "health": ["swasthya", "arogya"],
        "disease": ["roga", "vyadhi"],
        "treatment": ["chikitsa", "upachara"],
        "diagnosis": ["nidana", "roga pariksha"],
        "prognosis": ["sadhyasadhyata"],
        "etiology": ["nidana", "hetu"],
        "pathogenesis": ["samprapti"],
        "symptoms": ["lakshana", "rupa"],
        
        # Taste/properties
        "sweet": ["madhura"],
        "sour": ["amla"],
        "salt": ["lavana"],
        "bitter": ["tikta"],
        "pungent": ["katu"],
        "astringent": ["kashaya"],
        "hot": ["ushna"],
        "cold": ["shita", "sheeta"],
        
        # Miscellaneous
        "morning": ["pratahkala", "brahma muhurta"],
        "routine": ["dinacharya", "ritucharya"],
        "seasonal": ["ritucharya"],
        "daily": ["dinacharya"],
        "pregnancy": ["garbha", "garbhini paricharya"],
        "child": ["bala", "kaumara"],
        "elderly": ["vriddha", "jara"],
        "rasayana": ["rasayana", "rejuvenation"],
        "vajikarana": ["vajikarana", "aphrodisiac"],
    }
    
    # Check each word for suggestions
    for word in words:
        clean_word = word.strip('.,?!')
        if clean_word in term_suggestions:
            suggestions.extend(term_suggestions[clean_word])
    
    # Also get synonyms from ayurvedic_synonyms module
    for word in words:
        clean_word = word.strip('.,?!')
        syns = get_synonyms(clean_word)
        if syns and len(syns) > 0:
            suggestions.extend(syns[:3])  # Add top 3 synonyms
    
    # Remove duplicates and limit
    seen = set()
    unique_suggestions = []
    for s in suggestions:
        s_lower = s.lower()
        if s_lower not in seen and s_lower != query_lower and s_lower not in query_lower:
            seen.add(s_lower)
            unique_suggestions.append(s)
    
    return unique_suggestions[:6]  # Return top 6 suggestions


# =============================================================================
# UI COMPONENTS - HEADER
# =============================================================================

def render_header():
    logo_b64 = get_logo_base64()
    
    if logo_b64:
        st.markdown(f"""
        <div class="header-container">
            <img src="data:image/jpeg;base64,{logo_b64}" class="logo-img" alt="Logo">
            <div class="header-text">
                <h1>Bhruhat Trayi AI Assistant by PraKul</h1>
                <p class="subtitle">An AI initiative by Prof.(Dr.) Prasanna Kulkarni</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="header-container">
            <div class="header-text">
                <h1>🪷 Bhruhat Trayi AI Assistant by PraKul</h1>
                <p class="subtitle">An AI initiative by Prof.(Dr.) Prasanna Kulkarni</p>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_stats(df: pd.DataFrame):
    total = len(df)
    samhitas = df['File Name'].nunique()
    
    st.markdown(f"""
    <div class="stats-container">
        <span class="stat-badge">📚 {total:,} ślokas</span>
        <span class="stat-badge">📖 {samhitas} Saṃhitās</span>
        <span class="stat-badge">✅ Ready</span>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# UI COMPONENTS - SELECTION (Tabular Checkboxes)
# =============================================================================

def render_selection_panel():
    """Render text and role selection in tabular format with checkboxes"""
    
    col1, col2 = st.columns(2)
    
    # === LEFT: Text Selection ===
    with col1:
        st.markdown("""
        <div class="selection-container">
            <div class="selection-title">📚 Select Texts (Saṃhitās)</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Default all selected
        charaka = st.checkbox("Charaka Saṃhitā", value=True, key="sel_charaka")
        sushruta = st.checkbox("Suśruta Saṃhitā", value=True, key="sel_sushruta")
        astanga = st.checkbox("Aṣṭāṅga Hṛdaya", value=True, key="sel_astanga")
        
        selected_samhitas = []
        if charaka:
            selected_samhitas.append("Charaka Samhita")
        if sushruta:
            selected_samhitas.append("Sushruta Samhita")
        if astanga:
            selected_samhitas.append("Astanga Hrudaya")
    
    # === RIGHT: Role Selection ===
    with col2:
        st.markdown("""
        <div class="selection-container">
            <div class="selection-title">👤 Select Your Role</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Default Student selected
        student = st.checkbox("🎓 Student", value=True, key="sel_student")
        pg_scholar = st.checkbox("📚 PG Scholar", value=False, key="sel_pg")
        teacher = st.checkbox("👨‍🏫 Teacher", value=False, key="sel_teacher")
        researcher = st.checkbox("🔬 Researcher", value=False, key="sel_researcher")
        physician = st.checkbox("⚕️ Physician", value=False, key="sel_physician")
        
        selected_roles = []
        if student:
            selected_roles.append("Student")
        if pg_scholar:
            selected_roles.append("PG Scholar")
        if teacher:
            selected_roles.append("Teacher")
        if researcher:
            selected_roles.append("Researcher")
        if physician:
            selected_roles.append("Physician")
    
    return selected_samhitas, selected_roles


# =============================================================================
# UI COMPONENTS - DISAMBIGUATION
# =============================================================================

def render_disambiguation(query: str) -> str:
    """Show disambiguation options for ambiguous queries"""
    
    if not DISAMBIGUATION_AVAILABLE:
        return query
    
    result = get_disambiguation_suggestions(query)
    
    if not result["is_ambiguous"]:
        return query
    
    term = result["term"]
    meanings = result["meanings"]
    
    st.markdown(f"""
    <div class="disambig-box">
        <div class="disambig-title">🤔 Did you mean...</div>
        <p>The term "<b>{term}</b>" can have multiple meanings in Āyurveda:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create radio options
    options = [f"{m[0]} - {m[1]}" for m in meanings]
    options.append("🔤 Other (I'll type my own)")
    
    selection = st.radio("Select the meaning you're looking for:", options, key="disambig_radio")
    
    if selection == "🔤 Other (I'll type my own)":
        custom = st.text_input("Type your refined query:", value=query, key="custom_query")
        return custom
    else:
        # Find selected meaning and use its search hint
        idx = options.index(selection)
        if idx < len(meanings):
            hint = meanings[idx][2]
            return refine_query_with_meaning(query, hint)
    
    return query


# =============================================================================
# UI COMPONENTS - RESULTS
# =============================================================================

def render_sloka_card(row: pd.Series, idx: int):
    """Render a single sloka as a styled card"""
    samhita_class = get_samhita_class(row['File Name'])
    badge = get_samhita_badge(row['File Name'])
    ref_eng = get_reference_code(row)
    ref_dev = get_devanagari_reference(row)
    
    sloka_text = str(row.get('Sloka Text', ''))
    iast = str(row.get('IAST', ''))
    
    st.markdown(f"""
    <div class="sloka-card {samhita_class}">
        <div class="sloka-ref">
            {badge} &nbsp; <b>{ref_eng}</b> ({ref_dev})
        </div>
        <div class="sloka-text">{sloka_text}</div>
        <div style="color:#666; font-size:0.9rem; margin-top:8px; font-style:italic;">{iast}</div>
    </div>
    """, unsafe_allow_html=True)


def render_results(results: pd.DataFrame, expanded_terms: List[str], query: str, max_results: int = 15):
    """Render search results with Load More option"""
    
    total_found = len(results)
    
    st.markdown(f"""
    <div class="success-box">
        <b>✅ Found {total_found} ślokas</b> for "<i>{query}</i>"
        {f'<br><small>(Showing top {min(total_found, max_results)} results)</small>' if total_found > max_results else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Group by Samhita for better organization
    for samhita in results['File Name'].unique():
        samhita_results = results[results['File Name'] == samhita]
        
        # Create display name without HTML
        if "Charaka" in samhita:
            display_name = f"🟢 Charaka Saṃhitā ({len(samhita_results)} ślokas)"
        elif "Sushruta" in samhita:
            display_name = f"🔵 Suśruta Saṃhitā ({len(samhita_results)} ślokas)"
        else:
            display_name = f"🟠 Aṣṭāṅga Hṛdaya ({len(samhita_results)} ślokas)"
        
        with st.expander(display_name, expanded=True):
            for idx, (_, row) in enumerate(samhita_results.iterrows()):
                render_sloka_card(row, idx)
    
    # Show tip if results might be limited
    if total_found >= max_results:
        st.markdown(f"""
        <div class="warning-box">
            <b>💡 Want more results?</b><br>
            Increase the "Maximum results" slider above and search again to find more ślokas.
            Current limit: {max_results} | Try setting to 30-50 for comprehensive search.
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# UI COMPONENTS - CHAT TAB
# =============================================================================

def render_chat_header():
    """Render AI TrayiDuta chat header"""
    st.markdown(f"""
    <div class="chat-header">
        <div class="chat-avatar">🙏</div>
        <div class="chat-info">
            <h3>{CHATBOT_NAME} ({CHATBOT_NAME_SANSKRIT})</h3>
            <p>Your AI Guide to Classical Āyurvedic Texts</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_chat_tab(df: pd.DataFrame, selected_samhitas: List[str], max_results: int):
    """Render the Chat with AI tab"""
    
    render_chat_header()
    
    # Check if chat module is available
    if not CHAT_AVAILABLE:
        st.markdown("""
        <div class="warning-box">
            <h4>📦 Install Required Module</h4>
            <p>Run: <code>pip install openai</code></p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Check API key
    api_configured = OPENAI_API_KEY and OPENAI_API_KEY != "sk-proj-YOUR_KEY_HERE"
    
    if not api_configured:
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ API Key Required</h4>
            <p>Add your OpenAI API key to <code>config.py</code></p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Check search context
    if st.session_state.search_results is None or len(st.session_state.search_results) == 0:
        st.markdown("""
        <div class="info-box">
            <h4>💡 Search First</h4>
            <p>Go to <b>🔍 Search Ślokas</b> tab and search for a topic first.</p>
            <p>Then come back here to chat about those ślokas!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Show context
    st.markdown(f"""
    <div class="success-box">
        <b>📚 Context:</b> {len(st.session_state.search_results)} ślokas on "<b>{st.session_state.chat_context_query}</b>"<br>
        <b>👤 Role:</b> {st.session_state.chat_context_role}
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat
    if st.session_state.gemini_chat is None:
        with st.spinner(f"🔄 Initializing {CHATBOT_NAME}..."):
            try:
                from chat_module import OpenAIChat
                from config import OPENAI_API_KEY as API_KEY
                
                st.session_state.gemini_chat = OpenAIChat(api_key=API_KEY)
                
                if st.session_state.gemini_chat and st.session_state.gemini_chat.is_configured:
                    slokas_context = format_slokas_for_chat(st.session_state.search_results)
                    success = st.session_state.gemini_chat.start_chat(
                        slokas_context, 
                        st.session_state.chat_context_role,
                        st.session_state.chat_context_query
                    )
                    if not success:
                        st.error("❌ Failed to start chat session")
                        st.session_state.gemini_chat = None
                        return
                else:
                    st.error("❌ Could not configure AI. Check API key.")
                    st.session_state.gemini_chat = None
                    return
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                return
    
    # Check chat ready
    if not st.session_state.gemini_chat or not st.session_state.gemini_chat.chat_session:
        if st.button("🔄 Retry Initialization"):
            st.session_state.gemini_chat = None
            st.rerun()
        return
    
    # Display chat history
    st.markdown("---")
    
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-msg">
                <b>👤 You:</b> {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-msg">
                <b>🙏 {CHATBOT_NAME}:</b>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(msg["content"])
    
    # Chat input
    st.markdown("---")
    
    # Handle input clearing
    input_value = "" if st.session_state.get('clear_chat_input', False) else ""
    if st.session_state.get('clear_chat_input', False):
        st.session_state.clear_chat_input = False
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Your question:", 
            placeholder="Ask about the ślokas... (e.g., 'What are the key points?')",
            key="chat_input_field",
            label_visibility="collapsed"
        )
    with col2:
        send_btn = st.button("📤 Send", type="primary", use_container_width=True)
    
    # Quick prompts
    st.markdown("**Quick questions:**")
    qcol1, qcol2, qcol3, qcol4 = st.columns(4)
    
    with qcol1:
        if st.button("💡 Explain simply", use_container_width=True):
            user_input = "Explain these ślokas in simple terms"
            send_btn = True
    with qcol2:
        if st.button("📝 Give Anvaya", use_container_width=True):
            user_input = "Give me word-by-word Anvaya translation"
            send_btn = True
    with qcol3:
        if st.button("⭐ Key points", use_container_width=True):
            user_input = "What are the key points from these ślokas?"
            send_btn = True
    with qcol4:
        if st.button("💊 Clinical use", use_container_width=True):
            user_input = "How can this be applied clinically?"
            send_btn = True
    
    # Process input
    if send_btn and user_input and user_input.strip():
        # Add user message
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get AI response
        with st.spinner(f"🤔 {CHATBOT_NAME} is thinking..."):
            response = st.session_state.gemini_chat.send_message(user_input)
        
        # Add AI response
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Set flag to clear input on rerun
        st.session_state.clear_chat_input = True
        st.rerun()
    
    # Reset button
    st.markdown("---")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔄 Reset Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.session_state.gemini_chat = None
            st.rerun()


# =============================================================================
# UI COMPONENTS - PROMPT SECTION
# =============================================================================

def render_prompt_section(prompt: str, roles: List[str]):
    """Render copyable prompt for external use with instructions"""
    
    st.markdown('<p class="section-header">📋 Use with External AI (ChatGPT / Claude)</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <b>📌 How to use this prompt:</b>
        <ol>
            <li>Click the <b>Copy</b> button below to copy the generated prompt</li>
            <li>Open one of these AI tools:
                <ul>
                    <li>⭐ <a href="https://chatgpt.com/g/g-69550428a69c8191913b77f496161d39-bhruhat-trayi-ai-assistant-by-prakul" target="_blank"><b>Bhruhat Trayi AI Assistant by PraKul</b></a> (Custom GPT - Recommended!)</li>
                    <li>🤖 <a href="https://chat.openai.com" target="_blank">ChatGPT</a> (OpenAI)</li>
                    <li>🧠 <a href="https://claude.ai" target="_blank">Claude</a> (Anthropic)</li>
                </ul>
            </li>
            <li>Paste the prompt and press Enter</li>
            <li>Get detailed explanations with Anvaya translations!</li>
        </ol>
        <p><b>💡 Tip:</b> The Custom GPT is specifically trained for Āyurvedic texts!</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📄 Click to view/copy the generated prompt", expanded=False):
        st.text_area(
            "Generated Prompt:", 
            value=prompt, 
            height=300, 
            label_visibility="collapsed",
            help="Copy this entire prompt and paste in ChatGPT or Claude"
        )
        
        # Copy button using Streamlit's built-in
        st.markdown("👆 **Select all text above (Ctrl+A) and copy (Ctrl+C)**")
        
        st.markdown("""
        <div class="warning-box">
            <b>💡 Tip:</b> The AI TrayiDoota chatbot tab above uses the same ślokas. 
            You can chat there directly without copying!
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# UI COMPONENTS - FOOTER
# =============================================================================

def render_footer():
    st.markdown(f"""
    <div class="footer">
        🪷 <b>Bhruhat Trayi AI Assistant by PraKul</b> | Version 8.0<br>
        <small>An AI initiative by Prof.(Dr.) Prasanna Kulkarni</small><br>
        <small><i>Powered by {CHATBOT_NAME} ({CHATBOT_NAME_SANSKRIT})</i></small><br>
        <small style="color:#888;">For educational purposes. Always refer to original texts.</small>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    # Initialize
    init_session_state()
    load_css()
    
    # Load data
    df = load_database()
    
    # Render header and stats
    render_header()
    render_stats(df)
    
    # Main tabs with bigger fonts
    tab_search, tab_chat = st.tabs(["🔍 Search Ślokas", f"💬 Chat with {CHATBOT_NAME}"])
    
    # =========================================================================
    # TAB 1: SEARCH
    # =========================================================================
    with tab_search:
        st.markdown('<p class="section-header">⚙️ Settings</p>', unsafe_allow_html=True)
        
        # Selection panel (tabular checkboxes)
        selected_samhitas, selected_roles = render_selection_panel()
        
        # Max results slider with explanation
        st.markdown("""
        <div class="info-box" style="padding:10px;">
            <b>📊 Results Limit:</b> Set how many ślokas to display. 
            Higher = more comprehensive but slower. Start with 10-15 for quick searches.
        </div>
        """, unsafe_allow_html=True)
        
        col_slider1, col_slider2 = st.columns([3, 1])
        with col_slider1:
            max_results = st.slider(
                "Maximum results:", 
                min_value=5, 
                max_value=50, 
                value=15,
                step=5,
                help="More results = more comprehensive search but may include less relevant ślokas"
            )
        with col_slider2:
            st.markdown(f"**{max_results}** ślokas")
        
        # Store in session for "Load More" functionality
        if 'current_max_results' not in st.session_state:
            st.session_state.current_max_results = max_results
        
        st.markdown("---")
        
        # Search input
        st.markdown('<p class="section-header">🔍 Ask Your Question</p>', unsafe_allow_html=True)
        
        query = st.text_input(
            "Question:",
            value=st.session_state.current_query,
            placeholder="e.g., What is Vata? | Tell me about Triphala | Definition of health",
            label_visibility="collapsed",
            max_chars=500
        )
        
        # Show query suggestions ALWAYS when query has text
        if query and len(query.strip()) >= 3:
            suggestions = get_query_suggestions(query)
            if suggestions and len(suggestions) > 0:
                st.markdown("""
                <div class="disambig-box" style="padding:12px; margin:10px 0;">
                    <b>💡 Related search terms:</b> (Click to use)
                </div>
                """, unsafe_allow_html=True)
                
                num_cols = min(len(suggestions), 4)
                suggestion_cols = st.columns(num_cols)
                for i, sugg in enumerate(suggestions[:4]):
                    with suggestion_cols[i]:
                        if st.button(f"🔹 {sugg}", key=f"sugg_{i}_{sugg[:5]}", use_container_width=True):
                            st.session_state.current_query = sugg
                            st.rerun()
        
        col1, col2 = st.columns([4, 1])
        with col2:
            search_btn = st.button("🔎 Search", type="primary", use_container_width=True)
        
        # Example queries
        st.markdown("---")
        st.markdown("**Try these:**")
        ex_col1, ex_col2, ex_col3 = st.columns(3)
        with ex_col1:
            if st.button("What is Prakruti?", use_container_width=True):
                st.session_state.current_query = "What is Prakruti?"
                st.rerun()
        with ex_col2:
            if st.button("Tell me about Ojas", use_container_width=True):
                st.session_state.current_query = "Tell me about Ojas"
                st.rerun()
        with ex_col3:
            if st.button("Panchakarma procedures", use_container_width=True):
                st.session_state.current_query = "Panchakarma procedures"
                st.rerun()
        
        st.markdown("---")
        
        # Process search
        if search_btn and query.strip():
            if not selected_samhitas:
                st.error("⚠️ Select at least one Saṃhitā!")
                st.stop()
            
            if not selected_roles:
                st.error("⚠️ Select at least one role!")
                st.stop()
            
            # Check for issues
            issues = check_query_issues(query)
            
            if issues["is_off_topic"]:
                st.markdown('<div class="error-box">❌ This query seems outside Āyurveda scope.</div>', unsafe_allow_html=True)
                st.stop()
            
            # Spelling check
            if issues["spelling_suggestions"] and not st.session_state.confirmed_spelling:
                for wrong, correct in issues["spelling_suggestions"].items():
                    st.markdown(f'<div class="info-box">📝 Did you mean <b>{correct}</b> instead of <b>{wrong}</b>?</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("✅ Yes, correct it"):
                        for w, c in issues["spelling_suggestions"].items():
                            query = query.replace(w, c)
                        st.session_state.current_query = query
                        st.session_state.confirmed_spelling = True
                        st.rerun()
                with c2:
                    if st.button("❌ No, search as is"):
                        st.session_state.confirmed_spelling = True
                        st.rerun()
                st.stop()
            
            st.session_state.confirmed_spelling = False
            
            # Check disambiguation
            if DISAMBIGUATION_AVAILABLE and is_query_ambiguous(query):
                query = render_disambiguation(query)
            
            # Modern term warnings
            if issues["modern_terms"]:
                for mt in issues["modern_terms"]:
                    suggestions = ", ".join(mt["suggestions"][:3])
                    st.markdown(f'<div class="warning-box">ℹ️ "<b>{mt["term"]}</b>" is modern. Try: {suggestions}</div>', unsafe_allow_html=True)
            
            # Perform search
            with st.spinner("🔍 Searching across Bhruhat Trayi..."):
                results, analysis, explanation = enhanced_search(df, query, max_results, selected_samhitas)
            
            # Save to history
            if query not in st.session_state.search_history:
                st.session_state.search_history.append(query)
                if len(st.session_state.search_history) > 10:
                    st.session_state.search_history.pop(0)
            
            if len(results) == 0:
                st.markdown('<div class="warning-box">⚠️ No results found. Try different keywords.</div>', unsafe_allow_html=True)
            else:
                # Store for chat
                st.session_state.search_results = results
                st.session_state.chat_context_query = query
                st.session_state.chat_context_role = selected_roles[0]
                st.session_state.chat_messages = []
                st.session_state.gemini_chat = None
                
                # Show analysis
                with st.expander("🔬 Search Analysis", expanded=False):
                    st.markdown(explanation)
                
                # Render results
                render_results(results, analysis.get('search_hints', [query]), query, max_results)
                
                # Next steps
                st.markdown("---")
                st.markdown(f"""
                <div class="success-box">
                    <b>✅ {len(results)} ślokas loaded!</b><br>
                    👉 Switch to <b>💬 Chat with {CHATBOT_NAME}</b> tab to ask questions about these ślokas.
                </div>
                """, unsafe_allow_html=True)
                
                # Generate prompt
                st.markdown("---")
                slokas_formatted = format_slokas_for_prompt(results)
                prompt = generate_combined_prompt(selected_roles, query, slokas_formatted)
                render_prompt_section(prompt, selected_roles)
        
        elif search_btn:
            st.warning("⚠️ Please enter a question.")
    
    # =========================================================================
    # TAB 2: CHAT
    # =========================================================================
    with tab_chat:
        render_chat_tab(df, selected_samhitas if 'selected_samhitas' in dir() else None, max_results if 'max_results' in dir() else 10)
    
    # Footer
    st.markdown("---")
    render_footer()


if __name__ == "__main__":
    main()
