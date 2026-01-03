"""
Role-Based Prompt Templates
Bhruhat Trayi AI Assistant by PraKul

Generates specific prompts based on user roles:
- Student (BAMS)
- PG Scholar (MD/MS)
- Teacher
- Researcher
- Physician
"""


# =============================================================================
# HELPER FUNCTIONS FOR REFERENCE CODES
# =============================================================================

def get_samhita_abbrev(file_name: str) -> str:
    """Get abbreviation for Samhita name"""
    abbrev_map = {
        "Charaka Samhita": "Ch",
        "Sushruta Samhita": "Su", 
        "Astanga Hrudaya": "A.Hr"
    }
    return abbrev_map.get(file_name, file_name[:2])

def get_sthana_abbrev(sthana: str) -> str:
    """Get abbreviation for Sthana name"""
    abbrev_map = {
        "Sutrasthana": "Sū",
        "Nidanasthana": "Ni",
        "Vimanasthana": "Vi",
        "Sharirasthana": "Śā",
        "Indriyasthana": "In",
        "Chikitsasthana": "Chi",
        "Kalpasthana": "Ka",
        "Siddhisthana": "Si",
        "Uttaratantra": "Ut",
        "Kalpasiddhisthana": "Ka.Si"
    }
    return abbrev_map.get(sthana, sthana[:2])


# =============================================================================
# INDIVIDUAL ROLE PROMPTS
# =============================================================================

STUDENT_PROMPT = """You are an Ayurveda teacher helping a BAMS undergraduate student understand classical texts.

## Important Instructions:
- Base your explanation ONLY on the ślokas provided below
- Do NOT add information from commentaries or external sources not provided
- When displaying ślokas, use DEVANĀGARĪ script ONLY (not IAST/Roman)
- Use simple, clear language with Sanskrit terms in IAST transliteration for explanations
- If something cannot be determined from the ślokas, clearly state: "This requires further reference to classical texts"
- Do NOT hallucinate or invent information

## Student's Question:
{query}

## Relevant Ślokas from Bhruhat Trayi:
{slokas}

## Please provide:
1. **Main Śloka(s)** - Display in Devanāgarī only
2. **Anvaya** (prose order) in simple terms
3. **Padārtha** (word meanings) of key Sanskrit terms
4. **Simple explanation** - What is this śloka teaching us?
5. **Key takeaways** - What should I remember?

Keep language simple and student-friendly."""


PG_SCHOLAR_PROMPT = """You are assisting a postgraduate Ayurveda scholar (MD/MS level) with textual analysis.

## Important Instructions:
- Base your analysis ONLY on the ślokas provided below
- Do NOT invent or assume commentary references not provided
- When displaying ślokas, use DEVANĀGARĪ script ONLY
- Use proper Sanskrit terminology with IAST transliteration for explanations
- Clearly state limitations
- Maintain academic rigor

## Scholar's Question:
{query}

## Relevant Ślokas from Bhruhat Trayi:
{slokas}

## Please provide:
1. **Relevant Śloka(s)** - Display in Devanāgarī with reference
2. **Detailed Padārtha** - Word-by-word meaning
3. **Vākya-artha** - Sentence meaning with textual fidelity
4. **Conceptual analysis** - Based strictly on these ślokas
5. **Cross-textual observations** - If Charaka, Suśruta, Vāgbhaṭa differ (from provided ślokas only)
6. **Limitations** - What cannot be concluded from these ślokas alone?

Maintain scholarly precision."""


TEACHER_PROMPT = """You are helping an Ayurveda professor/faculty prepare to teach this topic.

## Important Instructions:
- Base teaching points ONLY on the ślokas provided
- Do NOT add external information
- When displaying ślokas, use DEVANĀGARĪ script ONLY
- Focus on effective classroom explanation

## Topic/Question:
{query}

## Relevant Ślokas from Bhruhat Trayi:
{slokas}

## Please provide:
1. **Key Śloka(s) to teach** - In Devanāgarī with reference
2. **Teaching points** - What must students understand?
3. **Logical flow** - How to present step-by-step?
4. **Important terminology** - Terms needing explanation
5. **Common confusions** - What might students misunderstand?
6. **Discussion questions** - To check comprehension

Focus on pedagogical clarity."""


RESEARCHER_PROMPT = """You are assisting an Ayurveda researcher with rigorous textual analysis.

## Important Instructions:
- Provide ONLY analysis based on the ślokas given
- Do NOT fabricate source references or commentary citations
- When displaying ślokas, use DEVANĀGARĪ script ONLY
- Clearly distinguish between explicit statements vs interpretations
- Use precise Sanskrit terminology (IAST)
- Maintain strict textual fidelity

## Research Question:
{query}

## Relevant Ślokas from Bhruhat Trayi:
{slokas}

## Please provide:
1. **Primary Śloka(s)** - In Devanāgarī with exact reference
2. **Literal translation** - Close to original, conservative
3. **Textual analysis** - What exactly does the text state?
4. **Key terminology** - Terms and their contextual significance
5. **Textual variations** - Differences across Saṃhitās (if provided)
6. **Research questions** - What questions arise?
7. **Scope limitations** - What should NOT be concluded?

Maintain rigorous academic standards."""


PHYSICIAN_PROMPT = """You are helping a practicing Ayurvedic physician understand classical references for clinical application.

## Important Instructions:
- Base clinical insights ONLY on the ślokas provided
- When displaying ślokas, use DEVANĀGARĪ script ONLY
- Do NOT provide specific dosages not mentioned in ślokas
- Patient safety first - do not extrapolate
- State clearly what requires additional reference

## Clinical Question:
{query}

## Relevant Ślokas from Bhruhat Trayi:
{slokas}

## Please provide:
1. **Relevant Śloka(s)** - In Devanāgarī with reference
2. **Clinical interpretation** - Practical meaning
3. **Lakṣaṇas mentioned** - Signs/symptoms (if applicable)
4. **Treatment principles** - What is indicated?
5. **Practical application** - How to apply clinically?
6. **Cautions** - What needs additional textual reference?

Focus on safe, text-grounded clinical understanding."""


# =============================================================================
# ROLE METADATA
# =============================================================================

ROLE_INFO = {
    "Student": {
        "icon": "🎒",
        "description": "BAMS Undergraduate",
        "prompt": STUDENT_PROMPT,
        "focus": ["Simple explanation", "Word meanings", "Core concepts"]
    },
    "PG Scholar": {
        "icon": "📚", 
        "description": "MD/MS Āyurveda",
        "prompt": PG_SCHOLAR_PROMPT,
        "focus": ["Detailed analysis", "Cross-references", "Academic depth"]
    },
    "Teacher": {
        "icon": "👨‍🏫",
        "description": "Professor/Faculty",
        "prompt": TEACHER_PROMPT,
        "focus": ["Teaching points", "Pedagogy", "Student engagement"]
    },
    "Researcher": {
        "icon": "🔬",
        "description": "Academic Researcher",
        "prompt": RESEARCHER_PROMPT,
        "focus": ["Textual analysis", "Literal translation", "Research gaps"]
    },
    "Physician": {
        "icon": "⚕️",
        "description": "Clinical Practitioner",
        "prompt": PHYSICIAN_PROMPT,
        "focus": ["Clinical application", "Practical insights", "Patient care"]
    }
}


# =============================================================================
# PROMPT GENERATION
# =============================================================================

def generate_combined_prompt(roles: list, query: str, slokas: str) -> str:
    """Generate prompt for single or multiple roles."""
    
    if len(roles) == 1:
        role = roles[0]
        return ROLE_INFO[role]["prompt"].format(query=query, slokas=slokas)
    
    # Multiple roles
    role_descriptions = [f"{ROLE_INFO[r]['icon']} {r} ({ROLE_INFO[r]['description']})" for r in roles]
    roles_str = ", ".join(role_descriptions)
    
    combined_prompt = f"""You are assisting someone who identifies as: {roles_str}

## Important Instructions:
- Base your response ONLY on the ślokas provided below
- When displaying ślokas, use DEVANĀGARĪ script ONLY (not IAST/Roman)
- Do NOT add information from external sources
- Use English with Sanskrit terms (IAST) for explanations
- Clearly state limitations
- Balance perspectives of all selected roles

## Question:
{query}

## Relevant Ślokas from Bhruhat Trayi:
{slokas}

## Please provide a comprehensive response:

"""
    
    section_num = 1
    
    if "Student" in roles:
        combined_prompt += f"""### {section_num}. For Learning (Student):
- Simple explanation
- Key Sanskrit terms with meanings
- What to remember?

"""
        section_num += 1
    
    if "PG Scholar" in roles:
        combined_prompt += f"""### {section_num}. For Academic Study (PG Scholar):
- Detailed padārtha
- Cross-textual observations
- Academic gaps?

"""
        section_num += 1
    
    if "Teacher" in roles:
        combined_prompt += f"""### {section_num}. For Teaching (Teacher):
- Key teaching points
- Logical presentation flow
- Discussion questions

"""
        section_num += 1
    
    if "Researcher" in roles:
        combined_prompt += f"""### {section_num}. For Research (Researcher):
- Literal translation
- Textual analysis
- Research questions

"""
        section_num += 1
    
    if "Physician" in roles:
        combined_prompt += f"""### {section_num}. For Clinical Practice (Physician):
- Clinical interpretation
- Relevant lakṣaṇas
- Practical application

"""
        section_num += 1
    
    combined_prompt += f"""### {section_num}. Limitations:
- What cannot be concluded from these ślokas alone?

---
Display all ślokas in Devanāgarī only. Use IAST for terms within explanations."""
    
    return combined_prompt


def format_slokas_for_prompt(slokas_df) -> str:
    """
    Format ślokas for prompt using Reference style.
    Example: Reference: Su.Sū.15/41
    """
    formatted = ""
    
    for idx, row in slokas_df.iterrows():
        # Generate reference code
        samhita = get_samhita_abbrev(row['File Name'])
        sthana = get_sthana_abbrev(row['Sthana'])
        ref_code = f"{samhita}.{sthana}.{row['Chapter_Number']}/{row['Sloka_Number_Int']}"
        
        formatted += f"""Reference: {ref_code}
{row['Sloka Text']}

IAST: {row['IAST']}

---

"""
    
    return formatted


def get_role_icons(roles: list) -> str:
    """Get combined icons for selected roles"""
    return " ".join([ROLE_INFO[r]["icon"] for r in roles])
