"""
Query Analyzer Module
Bhruhat Trayi AI Assistant by PraKul

This module analyzes user queries to determine:
1. Query Type (Concept, Treatment, Etiology, Symptoms, Diet)
2. Subject (Doṣa, Disease, Concept, Treatment procedure)
3. Sthāna Priority (which sections to prioritize)
4. Chapter Priority (which chapters to boost)
5. Pathya-Apathya requirements
"""

import re
from typing import Dict, List, Tuple, Optional

# =============================================================================
# QUERY TYPE DETECTION
# =============================================================================

QUERY_TYPE_KEYWORDS = {
    "concept": {
        "english": [
            "what is", "tell me about", "define", "explain", "describe",
            "meaning of", "introduction to", "basics of", "understand",
            "concept of", "definition", "overview", "about"
        ],
        "sanskrit": [
            "svarupa", "स्वरूप", "lakshana", "लक्षण", "paribhasha", "परिभाषा",
            "guna", "गुण", "karma", "कर्म"
        ],
        "priority_sthana": {
            "Sutrasthana": 50,
            "Sharirasthana": 40,
            "Vimanasthana": 30,
            "Nidanasthana": 20,
            "Chikitsasthana": 10
        }
    },
    
    "treatment": {
        "english": [
            "treatment", "treat", "manage", "management", "cure", "remedy",
            "therapy", "how to treat", "medicine for", "drug for",
            "prescription", "healing", "what to do for"
        ],
        "sanskrit": [
            "chikitsa", "चिकित्सा", "upakrama", "उपक्रम", "aushadha", "औषध",
            "bheshaja", "भेषज", "upachara", "उपचार", "shamana", "शमन",
            "shodhana", "शोधन", "oushadha", "ओषध"
        ],
        "priority_sthana": {
            "Chikitsasthana": 50,
            "Kalpasthana": 40,
            "Siddhisthana": 40,
            "Nidanasthana": 30,  # For Apathya (causes to avoid)
            "Sutrasthana": 20
        },
        "include_nidana_as_apathya": True
    },
    
    "etiology": {
        "english": [
            "cause", "causes", "reason", "why", "how does", "etiology",
            "origin", "source", "factor", "what causes", "due to"
        ],
        "sanskrit": [
            "nidana", "निदान", "hetu", "हेतु", "karana", "कारण",
            "nimitta", "निमित्त", "prakopa", "प्रकोप"
        ],
        "priority_sthana": {
            "Nidanasthana": 50,
            "Sutrasthana": 40,
            "Chikitsasthana": 20
        }
    },
    
    "symptoms": {
        "english": [
            "symptoms", "signs", "features", "characteristics", "how to identify",
            "presentation", "manifestation", "clinical features", "diagnosis"
        ],
        "sanskrit": [
            "lakshana", "लक्षण", "rupa", "रूप", "linga", "लिङ्ग",
            "chihna", "चिह्न", "purvarupa", "पूर्वरूप", "upadrava", "उपद्रव"
        ],
        "priority_sthana": {
            "Nidanasthana": 50,
            "Chikitsasthana": 30,
            "Sutrasthana": 20
        }
    },
    
    "diet": {
        "english": [
            "diet", "food", "pathya", "apathya", "what to eat", "what to avoid",
            "nutrition", "dietary", "regimen", "lifestyle"
        ],
        "sanskrit": [
            "pathya", "पथ्य", "apathya", "अपथ्य", "ahara", "आहार",
            "anna", "अन्न", "bhojana", "भोजन", "vihara", "विहार"
        ],
        "priority_sthana": {
            "Sutrasthana": 50,
            "Chikitsasthana": 40,
            "Nidanasthana": 30  # Causes = Apathya
        },
        "include_nidana_as_apathya": True
    },
    
    "prognosis": {
        "english": [
            "prognosis", "curable", "incurable", "outcome", "result",
            "can it be cured", "is it treatable"
        ],
        "sanskrit": [
            "sadhya", "साध्य", "asadhya", "असाध्य", "yapya", "याप्य",
            "arishta", "अरिष्ट", "mrityu", "मृत्यु"
        ],
        "priority_sthana": {
            "Nidanasthana": 50,
            "Indriyasthana": 40,
            "Sutrasthana": 30
        }
    },
    
    "procedure": {
        "english": [
            "procedure", "panchakarma", "vamana", "virechana", "basti",
            "nasya", "raktamokshana", "how to perform", "method"
        ],
        "sanskrit": [
            "karma", "कर्म", "vidhi", "विधि", "vamana", "वमन",
            "virechana", "विरेचन", "basti", "बस्ति", "nasya", "नस्य"
        ],
        "priority_sthana": {
            "Siddhisthana": 50,
            "Kalpasthana": 50,
            "Chikitsasthana": 40,
            "Sutrasthana": 20
        }
    }
}


# =============================================================================
# SUBJECT DETECTION - DOṢA
# =============================================================================

DOSHA_KEYWORDS = {
    "vata": {
        "terms": ["vata", "vāta", "वात", "vayu", "vāyu", "वायु", "anila", "अनिल", "pavana", "पवन"],
        "aspects": {
            "svarupa": ["स्वरूप", "svarupa", "definition", "what is"],
            "guna": ["गुण", "guna", "property", "quality", "ruksha", "laghu", "shita"],
            "sthana": ["स्थान", "sthana", "location", "seat", "where"],
            "karma": ["कर्म", "karma", "function", "action", "what does"],
            "prakopa": ["प्रकोप", "prakopa", "aggravation", "increase", "vrddhi"],
            "kshaya": ["क्षय", "kshaya", "decrease", "deficiency"],
            "chikitsa": ["चिकित्सा", "chikitsa", "treatment", "upakrama"]
        },
        "subtypes": ["prana", "प्राण", "udana", "उदान", "samana", "समान", "apana", "अपान", "vyana", "व्यान"]
    },
    
    "pitta": {
        "terms": ["pitta", "पित्त", "pittam"],
        "aspects": {
            "svarupa": ["स्वरूप", "svarupa", "definition", "what is"],
            "guna": ["गुण", "guna", "property", "ushna", "tikshna", "drava"],
            "sthana": ["स्थान", "sthana", "location", "seat"],
            "karma": ["कर्म", "karma", "function", "action"],
            "prakopa": ["प्रकोप", "prakopa", "aggravation"],
            "kshaya": ["क्षय", "kshaya", "decrease"],
            "chikitsa": ["चिकित्सा", "chikitsa", "treatment"]
        },
        "subtypes": ["pachaka", "पाचक", "ranjaka", "रञ्जक", "sadhaka", "साधक", "alochaka", "आलोचक", "bhrajaka", "भ्राजक"]
    },
    
    "kapha": {
        "terms": ["kapha", "कफ", "shleshma", "श्लेष्मा", "श्लेष्म", "sleshma"],
        "aspects": {
            "svarupa": ["स्वरूप", "svarupa", "definition", "what is"],
            "guna": ["गुण", "guna", "property", "guru", "shita", "snigdha"],
            "sthana": ["स्थान", "sthana", "location", "seat"],
            "karma": ["कर्म", "karma", "function", "action"],
            "prakopa": ["प्रकोप", "prakopa", "aggravation"],
            "kshaya": ["क्षय", "kshaya", "decrease"],
            "chikitsa": ["चिकित्सा", "chikitsa", "treatment"]
        },
        "subtypes": ["avalambaka", "अवलम्बक", "kledaka", "क्लेदक", "bodhaka", "बोधक", "tarpaka", "तर्पक", "shleshaka", "श्लेषक"]
    }
}


# =============================================================================
# SUBJECT DETECTION - DISEASES
# =============================================================================

DISEASE_KEYWORDS = {
    # Metabolic
    "jwara": {
        "terms": ["jwara", "jvara", "ज्वर", "fever", "pyrexia"],
        "chapter_keywords": ["ज्वर", "jwara", "jvara"]
    },
    "prameha": {
        "terms": ["prameha", "प्रमेह", "madhumeha", "मधुमेह", "diabetes", "meha"],
        "chapter_keywords": ["प्रमेह", "prameha", "मधुमेह", "madhumeha"]
    },
    "sthaulya": {
        "terms": ["sthaulya", "स्थौल्य", "obesity", "medoroga", "मेदोरोग", "overweight"],
        "chapter_keywords": ["स्थौल्य", "sthaulya", "मेद", "meda"]
    },
    
    # Digestive
    "grahani": {
        "terms": ["grahani", "grahaṇī", "ग्रहणी", "ibs", "malabsorption", "sprue"],
        "chapter_keywords": ["ग्रहणी", "grahani", "grahaṇī"]
    },
    "atisara": {
        "terms": ["atisara", "atisāra", "अतिसार", "diarrhea", "loose motion"],
        "chapter_keywords": ["अतिसार", "atisara", "atisāra"]
    },
    "arshas": {
        "terms": ["arshas", "arśas", "अर्श", "piles", "hemorrhoids"],
        "chapter_keywords": ["अर्श", "arshas", "arśas"]
    },
    "ajirna": {
        "terms": ["ajirna", "ajīrṇa", "अजीर्ण", "indigestion", "dyspepsia"],
        "chapter_keywords": ["अजीर्ण", "ajirna"]
    },
    
    # Skin
    "kushtha": {
        "terms": ["kushtha", "kuṣṭha", "कुष्ठ", "skin disease", "leprosy", "dermatosis"],
        "chapter_keywords": ["कुष्ठ", "kushtha", "kuṣṭha"]
    },
    
    # Respiratory
    "kasa": {
        "terms": ["kasa", "kāsa", "कास", "cough"],
        "chapter_keywords": ["कास", "kasa", "kāsa"]
    },
    "shvasa": {
        "terms": ["shvasa", "śvāsa", "श्वास", "asthma", "breathlessness", "dyspnea"],
        "chapter_keywords": ["श्वास", "shvasa", "śvāsa"]
    },
    "rajayakshma": {
        "terms": ["rajayakshma", "rājayakṣmā", "राजयक्ष्मा", "tuberculosis", "consumption"],
        "chapter_keywords": ["राजयक्ष्मा", "rajayakshma"]
    },
    
    # Musculoskeletal
    "vatavyadhi": {
        "terms": ["vatavyadhi", "vātavyādhi", "वातव्याधि", "vata disorder", "neurological"],
        "chapter_keywords": ["वातव्याधि", "vatavyadhi", "vātavyādhi"]
    },
    "amavata": {
        "terms": ["amavata", "āmavāta", "आमवात", "rheumatoid", "arthritis"],
        "chapter_keywords": ["आमवात", "amavata"]
    },
    "sandhivata": {
        "terms": ["sandhivata", "sandhivāta", "संधिवात", "osteoarthritis", "joint pain"],
        "chapter_keywords": ["संधिवात", "sandhivata"]
    },
    
    # Urinary
    "mutrakricchra": {
        "terms": ["mutrakricchra", "mūtrakṛcchra", "मूत्रकृच्छ्र", "dysuria", "urinary"],
        "chapter_keywords": ["मूत्रकृच्छ्र", "mutrakricchra"]
    },
    "ashmari": {
        "terms": ["ashmari", "aśmarī", "अश्मरी", "stone", "calculus", "kidney stone"],
        "chapter_keywords": ["अश्मरी", "ashmari"]
    },
    
    # Neurological
    "apasmara": {
        "terms": ["apasmara", "apasmāra", "अपस्मार", "epilepsy", "seizure"],
        "chapter_keywords": ["अपस्मार", "apasmara"]
    },
    "unmada": {
        "terms": ["unmada", "unmāda", "उन्माद", "insanity", "psychosis", "mania"],
        "chapter_keywords": ["उन्माद", "unmada"]
    },
    "pakshaghata": {
        "terms": ["pakshaghata", "pakṣāghāta", "पक्षाघात", "paralysis", "hemiplegia", "stroke"],
        "chapter_keywords": ["पक्षाघात", "pakshaghata"]
    },
    
    # Bleeding
    "raktapitta": {
        "terms": ["raktapitta", "रक्तपित्त", "bleeding disorder", "hemorrhage"],
        "chapter_keywords": ["रक्तपित्त", "raktapitta"]
    },
    
    # Swelling
    "shotha": {
        "terms": ["shotha", "śotha", "शोथ", "swelling", "edema", "inflammation"],
        "chapter_keywords": ["शोथ", "shotha", "śotha"]
    },
    
    # Abdominal
    "udara": {
        "terms": ["udara", "उदर", "ascites", "abdominal"],
        "chapter_keywords": ["उदर", "udara"]
    },
    "gulma": {
        "terms": ["gulma", "गुल्म", "abdominal mass", "phantom tumor"],
        "chapter_keywords": ["गुल्म", "gulma"]
    },
    
    # Anemia
    "pandu": {
        "terms": ["pandu", "pāṇḍu", "पाण्डु", "anemia", "pallor"],
        "chapter_keywords": ["पाण्डु", "pandu"]
    },
    
    # Cardiac
    "hridroga": {
        "terms": ["hridroga", "hṛdroga", "हृद्रोग", "heart disease", "cardiac"],
        "chapter_keywords": ["हृद्रोग", "hridroga"]
    },
    
    # Headache
    "shiroroga": {
        "terms": ["shiroroga", "śiroroga", "शिरोरोग", "headache", "shirahshula"],
        "chapter_keywords": ["शिरोरोग", "shiroroga", "शिरः"]
    },
    
    # Poisoning
    "visha": {
        "terms": ["visha", "viṣa", "विष", "poison", "toxin", "poisoning"],
        "chapter_keywords": ["विष", "visha", "viṣa"]
    }
}


# =============================================================================
# CONCEPT KEYWORDS
# =============================================================================

CONCEPT_KEYWORDS = {
    "agni": {
        "terms": ["agni", "अग्नि", "digestive fire", "jatharagni", "जाठराग्नि", "digestion"],
        "related": ["mandagni", "मन्दाग्नि", "vishamagni", "विषमाग्नि", "tikshnagni", "तीक्ष्णाग्नि"]
    },
    "ama": {
        "terms": ["ama", "āma", "आम", "toxin", "undigested"],
        "related": ["amavisha", "आमविष", "amadosha", "आमदोष"]
    },
    "ojas": {
        "terms": ["ojas", "ओजस्", "ojah", "vital essence", "immunity"],
        "related": ["bala", "बल", "vyadhikshamatva", "व्याधिक्षमत्व"]
    },
    "dhatu": {
        "terms": ["dhatu", "dhātu", "धातु", "tissue", "saptadhatu", "सप्तधातु"],
        "related": ["rasa", "rakta", "mamsa", "meda", "asthi", "majja", "shukra"]
    },
    "mala": {
        "terms": ["mala", "मल", "waste", "purisha", "mutra", "sveda"],
        "related": ["पुरीष", "मूत्र", "स्वेद"]
    },
    "srotas": {
        "terms": ["srotas", "स्रोतस्", "channel", "nadi", "नाडी"],
        "related": ["pranavaha", "annavaha", "rasavaha"]
    },
    "prakriti": {
        "terms": ["prakriti", "prakṛti", "प्रकृति", "constitution", "body type"],
        "related": ["vata prakriti", "pitta prakriti", "kapha prakriti"]
    },
    "dinacharya": {
        "terms": ["dinacharya", "dinacaryā", "दिनचर्या", "daily routine", "daily regimen"],
        "related": ["prabhata", "प्रभात", "ratri", "रात्रि"]
    },
    "ritucharya": {
        "terms": ["ritucharya", "ṛtucaryā", "ऋतुचर्या", "seasonal routine", "seasonal regimen"],
        "related": ["hemanta", "shishira", "vasanta", "grishma", "varsha", "sharad"]
    },
    "panchakarma": {
        "terms": ["panchakarma", "pañcakarma", "पञ्चकर्म", "five procedures", "purification"],
        "related": ["vamana", "virechana", "basti", "nasya", "raktamokshana"]
    }
}


# =============================================================================
# MAIN ANALYZER CLASS
# =============================================================================

class QueryAnalyzer:
    """Analyzes user queries and determines search priorities"""
    
    def __init__(self):
        self.query_types = QUERY_TYPE_KEYWORDS
        self.dosha_keywords = DOSHA_KEYWORDS
        self.disease_keywords = DISEASE_KEYWORDS
        self.concept_keywords = CONCEPT_KEYWORDS
    
    def analyze(self, query: str) -> Dict:
        """
        Main analysis function
        Returns comprehensive analysis of the query
        """
        query_lower = query.lower()
        
        # Detect query type
        query_type = self._detect_query_type(query_lower)
        
        # Detect subject
        subject_type, subject_name, subject_data = self._detect_subject(query_lower)
        
        # Get Sthana priorities
        sthana_priority = self._get_sthana_priority(query_type)
        
        # Get chapter keywords (for disease queries)
        chapter_keywords = self._get_chapter_keywords(subject_type, subject_name)
        
        # Determine if Nidana should be included as Apathya
        include_nidana_apathya = self._should_include_nidana_apathya(query_type)
        
        # Get aspect hints (for Dosha queries)
        aspect = self._detect_aspect(query_lower, subject_type, subject_data)
        
        return {
            "original_query": query,
            "query_type": query_type,
            "subject_type": subject_type,  # "dosha", "disease", "concept", "general"
            "subject_name": subject_name,  # e.g., "vata", "prameha", "agni"
            "subject_data": subject_data,  # Full keyword data
            "sthana_priority": sthana_priority,
            "chapter_keywords": chapter_keywords,
            "include_nidana_apathya": include_nidana_apathya,
            "aspect": aspect,
            "search_hints": self._generate_search_hints(query_type, subject_type, subject_name, aspect)
        }
    
    def _detect_query_type(self, query: str) -> str:
        """Detect the type of query"""
        scores = {}
        
        for qtype, data in self.query_types.items():
            score = 0
            
            # Check English keywords
            for keyword in data["english"]:
                if keyword in query:
                    score += 10
            
            # Check Sanskrit keywords
            for keyword in data["sanskrit"]:
                if keyword in query:
                    score += 15  # Higher weight for Sanskrit terms
            
            scores[qtype] = score
        
        # Find highest scoring type
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        # Default to "concept" for general queries
        return "concept"
    
    def _detect_subject(self, query: str) -> Tuple[str, Optional[str], Optional[Dict]]:
        """Detect the subject of the query (Dosha, Disease, or Concept)"""
        
        # Check for Dosha
        for dosha_name, data in self.dosha_keywords.items():
            for term in data["terms"]:
                if term in query:
                    return ("dosha", dosha_name, data)
        
        # Check for Disease
        for disease_name, data in self.disease_keywords.items():
            for term in data["terms"]:
                if term in query:
                    return ("disease", disease_name, data)
        
        # Check for Concept
        for concept_name, data in self.concept_keywords.items():
            for term in data["terms"]:
                if term in query:
                    return ("concept", concept_name, data)
        
        return ("general", None, None)
    
    def _get_sthana_priority(self, query_type: str) -> Dict[str, int]:
        """Get Sthana priorities based on query type"""
        if query_type in self.query_types:
            return self.query_types[query_type].get("priority_sthana", {})
        
        # Default priorities
        return {
            "Sutrasthana": 30,
            "Nidanasthana": 20,
            "Chikitsasthana": 20,
            "Sharirasthana": 15,
            "Kalpasthana": 10,
            "Siddhisthana": 10
        }
    
    def _get_chapter_keywords(self, subject_type: str, subject_name: Optional[str]) -> List[str]:
        """Get chapter keywords for boosting specific chapters"""
        if subject_type == "disease" and subject_name:
            if subject_name in self.disease_keywords:
                return self.disease_keywords[subject_name].get("chapter_keywords", [])
        
        return []
    
    def _should_include_nidana_apathya(self, query_type: str) -> bool:
        """Determine if Nidana should be included as Apathya"""
        if query_type in self.query_types:
            return self.query_types[query_type].get("include_nidana_as_apathya", False)
        return False
    
    def _detect_aspect(self, query: str, subject_type: str, subject_data: Optional[Dict]) -> Optional[str]:
        """Detect specific aspect being asked about (for Dosha queries)"""
        if subject_type != "dosha" or not subject_data:
            return None
        
        aspects = subject_data.get("aspects", {})
        
        for aspect_name, keywords in aspects.items():
            for keyword in keywords:
                if keyword in query:
                    return aspect_name
        
        return None
    
    def _generate_search_hints(self, query_type: str, subject_type: str, 
                               subject_name: Optional[str], aspect: Optional[str]) -> List[str]:
        """Generate search hints for better results"""
        hints = []
        
        # Add subject terms
        if subject_type == "dosha" and subject_name:
            hints.extend(self.dosha_keywords[subject_name]["terms"][:3])
            if aspect:
                hints.append(aspect)
        
        elif subject_type == "disease" and subject_name:
            hints.extend(self.disease_keywords[subject_name]["terms"][:3])
        
        elif subject_type == "concept" and subject_name:
            hints.extend(self.concept_keywords[subject_name]["terms"][:3])
        
        # Add query type hints
        if query_type == "treatment":
            hints.extend(["चिकित्सा", "chikitsa", "उपक्रम"])
        elif query_type == "etiology":
            hints.extend(["निदान", "nidana", "हेतु", "कारण"])
        elif query_type == "symptoms":
            hints.extend(["लक्षण", "lakshana", "रूप"])
        elif query_type == "diet":
            hints.extend(["पथ्य", "pathya", "आहार"])
        
        return hints


# =============================================================================
# RESULT BALANCER
# =============================================================================

class ResultBalancer:
    """Balances search results to include appropriate mix of content"""
    
    @staticmethod
    def balance_results(results_df, query_analysis: Dict, max_results: int = 10):
        """
        Balance results based on query type
        For treatment queries: 50% chikitsa, 30% nidana (apathya), 20% pathya
        """
        import pandas as pd
        
        if len(results_df) == 0:
            return results_df
        
        query_type = query_analysis.get("query_type", "concept")
        include_nidana = query_analysis.get("include_nidana_apathya", False)
        
        if query_type in ["treatment", "diet"] and include_nidana:
            # Categorize results by Sthana
            chikitsa = results_df[results_df['Sthana'].str.contains('Chikitsa|Kalpa|Siddhi', case=False, na=False)]
            nidana = results_df[results_df['Sthana'].str.contains('Nidana', case=False, na=False)]
            sutra = results_df[results_df['Sthana'].str.contains('Sutra', case=False, na=False)]
            others = results_df[~results_df.index.isin(chikitsa.index) & 
                               ~results_df.index.isin(nidana.index) &
                               ~results_df.index.isin(sutra.index)]
            
            # Calculate counts
            chikitsa_count = min(len(chikitsa), int(max_results * 0.5))
            nidana_count = min(len(nidana), int(max_results * 0.3))
            pathya_count = min(len(sutra), int(max_results * 0.2))
            remaining = max_results - chikitsa_count - nidana_count - pathya_count
            
            # Combine
            balanced = pd.concat([
                chikitsa.head(chikitsa_count),
                nidana.head(nidana_count),
                sutra.head(pathya_count),
                others.head(remaining)
            ])
            
            return balanced.head(max_results).reset_index(drop=True)
        
        return results_df.head(max_results).reset_index(drop=True)


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def analyze_query(query: str) -> Dict:
    """Convenience function to analyze a query"""
    analyzer = QueryAnalyzer()
    return analyzer.analyze(query)


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    # Test queries
    test_queries = [
        "Tell me about Vata",
        "What is Kapha?",
        "Prameha treatment",
        "Causes of Jwara",
        "Symptoms of Kushtha",
        "Pathya in Grahani",
        "What causes obesity?",
        "How to treat diabetes?",
        "Definition of Agni",
    ]
    
    analyzer = QueryAnalyzer()
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        result = analyzer.analyze(query)
        print(f"  Type: {result['query_type']}")
        print(f"  Subject: {result['subject_type']} - {result['subject_name']}")
        print(f"  Aspect: {result['aspect']}")
        print(f"  Sthana Priority: {result['sthana_priority']}")
        print(f"  Chapter Keywords: {result['chapter_keywords']}")
        print(f"  Include Nidana as Apathya: {result['include_nidana_apathya']}")
        print(f"  Search Hints: {result['search_hints']}")
