"""
Enhanced Search Module
Bhruhat Trayi AI Assistant by PraKul

This module combines:
1. Semantic Search (AI embeddings)
2. Query Analysis (type, subject detection)
3. Sthana Priority Boosting
4. Chapter Priority Boosting
5. Pathya-Apathya Logic
6. Result Balancing
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re

from query_analyzer import QueryAnalyzer, ResultBalancer, analyze_query


# =============================================================================
# CONFIGURATION
# =============================================================================

APP_DIR = Path(__file__).parent

# Embedding files
EMBEDDINGS_PATH = APP_DIR / "sloka_embeddings.npy"

# Sthana name normalization (handle variations in database)
STHANA_NORMALIZATION = {
    "sutrasthana": "Sutrasthana",
    "sutra sthana": "Sutrasthana",
    "sūtrasthāna": "Sutrasthana",
    
    "nidanasthana": "Nidanasthana",
    "nidana sthana": "Nidanasthana",
    "nidānasthāna": "Nidanasthana",
    
    "sharirasthana": "Sharirasthana",
    "sharira sthana": "Sharirasthana",
    "śārīrasthāna": "Sharirasthana",
    
    "chikitsasthana": "Chikitsasthana",
    "chikitsa sthana": "Chikitsasthana",
    "cikitsāsthāna": "Chikitsasthana",
    
    "kalpasthana": "Kalpasthana",
    "kalpa sthana": "Kalpasthana",
    "kalpasthāna": "Kalpasthana",
    
    "siddhisthana": "Siddhisthana",
    "siddhi sthana": "Siddhisthana",
    "siddhisthāna": "Siddhisthana",
    
    "indriyasthana": "Indriyasthana",
    "indriya sthana": "Indriyasthana",
    
    "vimanasthana": "Vimanasthana",
    "vimana sthana": "Vimanasthana",
    "vimānasthāna": "Vimanasthana",
    
    "uttaratantra": "Uttaratantra",
    "uttara tantra": "Uttaratantra",
    "uttarasthana": "Uttaratantra",
}


# =============================================================================
# ENHANCED SEARCH CLASS
# =============================================================================

class EnhancedSearch:
    """
    Enhanced search combining semantic search with intelligent prioritization
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.analyzer = QueryAnalyzer()
        self.balancer = ResultBalancer()
        
        # Load embeddings if available
        self.embeddings = None
        self.model = None
        self._load_embeddings()
    
    def _load_embeddings(self):
        """Load embeddings and model for semantic search"""
        if not EMBEDDINGS_PATH.exists():
            print("⚠️ Embeddings not found. Using keyword search only.")
            return
        
        try:
            from sentence_transformers import SentenceTransformer
            
            self.embeddings = np.load(EMBEDDINGS_PATH)
            self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
            print("✅ Semantic search loaded successfully")
        except ImportError:
            print("⚠️ sentence-transformers not installed. Using keyword search only.")
        except Exception as e:
            print(f"⚠️ Error loading embeddings: {e}")
    
    def _normalize_sthana(self, sthana: str) -> str:
        """Normalize Sthana name for consistent matching"""
        if pd.isna(sthana):
            return ""
        
        sthana_lower = str(sthana).lower().strip()
        
        for pattern, normalized in STHANA_NORMALIZATION.items():
            if pattern in sthana_lower:
                return normalized
        
        return sthana
    
    def _get_sthana_boost(self, row, sthana_priority: Dict[str, int]) -> int:
        """Get boost score based on Sthana priority"""
        sthana = self._normalize_sthana(row.get('Sthana', ''))
        
        for priority_sthana, boost in sthana_priority.items():
            if priority_sthana.lower() in sthana.lower():
                return boost
        
        return 0
    
    def _get_chapter_boost(self, row, chapter_keywords: List[str]) -> int:
        """Get boost score if chapter matches disease keywords"""
        if not chapter_keywords:
            return 0
        
        chapter = str(row.get('Chapter', '')).lower()
        
        for keyword in chapter_keywords:
            if keyword.lower() in chapter:
                return 100  # High boost for matching chapter
        
        return 0
    
    def _semantic_search(self, query: str, top_k: int = 50) -> List[Tuple[int, float]]:
        """Perform semantic search and return indices with scores"""
        if self.model is None or self.embeddings is None:
            return []
        
        from numpy.linalg import norm
        
        # Create query embedding
        query_embedding = self.model.encode([query], convert_to_numpy=True)[0]
        
        # Calculate similarities
        similarities = []
        for i, emb in enumerate(self.embeddings):
            sim = np.dot(query_embedding, emb) / (norm(query_embedding) * norm(emb) + 1e-8)
            similarities.append((i, float(sim)))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def _keyword_search(self, query: str, search_hints: List[str], top_k: int = 50) -> List[Tuple[int, float]]:
        """Perform keyword search as fallback"""
        results = []
        
        # Combine query words with search hints
        search_terms = query.lower().split() + [h.lower() for h in search_hints]
        search_terms = list(set(search_terms))
        
        for idx, row in self.df.iterrows():
            score = 0
            
            # Search in all text columns
            text_columns = ['Sloka Text', 'IAST', 'Roman', 'Chapter']
            combined_text = ' '.join([str(row.get(col, '')).lower() for col in text_columns])
            
            for term in search_terms:
                if term in combined_text:
                    score += 1
            
            if score > 0:
                results.append((idx, score))
        
        # Sort by score
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_k]
    
    def search(self, query: str, max_results: int = 10, 
               selected_samhitas: List[str] = None) -> Tuple[pd.DataFrame, Dict]:
        """
        Main search function with enhanced prioritization
        
        Returns:
            - results DataFrame
            - query analysis dict
        """
        
        # Step 1: Analyze query
        analysis = self.analyzer.analyze(query)
        
        # Step 2: Filter by samhita if specified
        if selected_samhitas:
            samhita_map = {
                "Charaka Saṃhitā": "Charaka Samhita",
                "Suśruta Saṃhitā": "Sushruta Samhita",
                "Aṣṭāṅga Hṛdaya": "Astanga Hrudaya"
            }
            selected_internal = [samhita_map.get(s, s) for s in selected_samhitas]
            working_df = self.df[self.df['File Name'].isin(selected_internal)].copy()
        else:
            working_df = self.df.copy()
        
        if len(working_df) == 0:
            return pd.DataFrame(), analysis
        
        # Step 3: Perform semantic search (or keyword fallback)
        search_query = query
        if analysis['search_hints']:
            search_query = query + ' ' + ' '.join(analysis['search_hints'][:5])
        
        if self.model is not None and self.embeddings is not None:
            # Semantic search
            semantic_results = self._semantic_search(search_query, top_k=100)
            initial_indices = [idx for idx, score in semantic_results if idx in working_df.index]
            initial_scores = {idx: score for idx, score in semantic_results}
            search_method = "semantic"
        else:
            # Keyword fallback
            keyword_results = self._keyword_search(query, analysis['search_hints'], top_k=100)
            initial_indices = [idx for idx, score in keyword_results if idx in working_df.index]
            initial_scores = {idx: score for idx, score in keyword_results}
            search_method = "keyword"
        
        if len(initial_indices) == 0:
            return pd.DataFrame(), analysis
        
        # Step 4: Apply priority boosting
        boosted_scores = []
        
        for idx in initial_indices:
            row = self.df.loc[idx]
            
            base_score = initial_scores.get(idx, 0)
            
            # Apply Sthana boost
            sthana_boost = self._get_sthana_boost(row, analysis['sthana_priority'])
            
            # Apply Chapter boost (for disease queries)
            chapter_boost = self._get_chapter_boost(row, analysis['chapter_keywords'])
            
            # Calculate final score
            final_score = (base_score * 100) + sthana_boost + chapter_boost
            
            boosted_scores.append((idx, final_score, sthana_boost, chapter_boost))
        
        # Step 5: Sort by boosted score
        boosted_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Step 6: Get top results
        top_indices = [idx for idx, score, sb, cb in boosted_scores[:max_results * 2]]
        results = self.df.loc[top_indices].copy()
        
        # Add scores for debugging
        score_map = {idx: (score, sb, cb) for idx, score, sb, cb in boosted_scores}
        results['_total_score'] = results.index.map(lambda x: score_map.get(x, (0, 0, 0))[0])
        results['_sthana_boost'] = results.index.map(lambda x: score_map.get(x, (0, 0, 0))[1])
        results['_chapter_boost'] = results.index.map(lambda x: score_map.get(x, (0, 0, 0))[2])
        
        # Step 7: Balance results (for treatment queries)
        results = self.balancer.balance_results(results, analysis, max_results)
        
        # Add search method to analysis
        analysis['search_method'] = search_method
        
        return results, analysis
    
    def get_search_explanation(self, analysis: Dict) -> str:
        """Generate human-readable explanation of search logic"""
        lines = []
        
        lines.append(f"🔍 **Query Type:** {analysis['query_type'].title()}")
        
        if analysis['subject_type'] != 'general':
            lines.append(f"📌 **Subject:** {analysis['subject_name'].title()} ({analysis['subject_type'].title()})")
        
        if analysis['aspect']:
            lines.append(f"🎯 **Aspect:** {analysis['aspect'].title()}")
        
        if analysis['sthana_priority']:
            top_sthanas = sorted(analysis['sthana_priority'].items(), key=lambda x: x[1], reverse=True)[:3]
            sthana_str = ', '.join([f"{s}" for s, p in top_sthanas])
            lines.append(f"📚 **Priority Sections:** {sthana_str}")
        
        if analysis['include_nidana_apathya']:
            lines.append(f"⚠️ **Including Nidāna as Apathya** (causes = what to avoid)")
        
        if analysis.get('search_method'):
            method_emoji = "🧠" if analysis['search_method'] == 'semantic' else "🔤"
            lines.append(f"{method_emoji} **Search Method:** {analysis['search_method'].title()}")
        
        return '\n'.join(lines)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_enhanced_search(df: pd.DataFrame) -> EnhancedSearch:
    """Create an enhanced search instance"""
    return EnhancedSearch(df)


def enhanced_search(df: pd.DataFrame, query: str, max_results: int = 10,
                   selected_samhitas: List[str] = None) -> Tuple[pd.DataFrame, Dict, str]:
    """
    Convenience function for enhanced search
    
    Returns:
        - results DataFrame
        - query analysis dict
        - search explanation string
    """
    searcher = EnhancedSearch(df)
    results, analysis = searcher.search(query, max_results, selected_samhitas)
    explanation = searcher.get_search_explanation(analysis)
    
    return results, analysis, explanation


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    # Test with sample data
    print("Enhanced Search Module - Test")
    print("=" * 60)
    
    # Create sample DataFrame for testing
    sample_data = {
        'File Name': ['Charaka Samhita'] * 5,
        'Sthana': ['Sutrasthana', 'Nidanasthana', 'Chikitsasthana', 'Chikitsasthana', 'Kalpasthana'],
        'Chapter': ['I दीर्घञ्जीवितीय', 'प्रमेहनिदान', 'प्रमेहचिकित्सा', 'ज्वरचिकित्सा', 'मदनकल्प'],
        'Chapter_Number': [1, 4, 6, 3, 1],
        'Sloka_Number_Int': [1, 1, 1, 1, 1],
        'Sloka Text': [
            'आयुर्वेद definition śloka',
            'प्रमेह causes निदान śloka',
            'प्रमेह treatment चिकित्सा śloka',
            'ज्वर treatment चिकित्सा śloka',
            'वमन procedure śloka'
        ],
        'IAST': [''] * 5,
        'Roman': [''] * 5,
        'ASCII': [''] * 5
    }
    
    df = pd.DataFrame(sample_data)
    
    # Test queries
    test_queries = [
        "Tell me about Prameha",
        "Prameha treatment",
        "Causes of Jwara",
        "What is Vata?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        results, analysis, explanation = enhanced_search(df, query, max_results=5)
        
        print(explanation)
        print(f"\nResults: {len(results)} ślokas found")
        
        if len(results) > 0:
            for _, row in results.iterrows():
                print(f"  - {row['Sthana']} / {row['Chapter'][:30]}...")
