"""
Phase 2: FREE AI-Powered Semantic Search Setup
Bhruhat Trayi AI Assistant by PraKul

This script creates embeddings for all ślokas using a FREE local AI model.
Run this ONCE to set up semantic search.

Requirements:
    pip install sentence-transformers numpy

Usage:
    python setup_embeddings.py

Time: ~10-15 minutes for 25,000 ślokas (first run downloads model ~500MB)
"""

import pandas as pd
import numpy as np
from pathlib import Path
import time

# =============================================================================
# CONFIGURATION
# =============================================================================

APP_DIR = Path(__file__).parent

# Input files
PARQUET_PATH = APP_DIR / "all3_cleaned.parquet"
EXCEL_PATH = APP_DIR / "all3_cleaned.xlsx"

# Output file
EMBEDDINGS_PATH = APP_DIR / "sloka_embeddings.npy"
METADATA_PATH = APP_DIR / "sloka_metadata.parquet"

# Model - multilingual model that understands Sanskrit/Hindi + English
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# Alternative: "sentence-transformers/distiluse-base-multilingual-cased-v2"


# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

def load_database():
    """Load the ślokas database"""
    print("📂 Loading database...")
    
    if PARQUET_PATH.exists():
        df = pd.read_parquet(PARQUET_PATH)
        print(f"   Loaded from Parquet: {len(df):,} ślokas")
    elif EXCEL_PATH.exists():
        df = pd.read_excel(EXCEL_PATH)
        print(f"   Loaded from Excel: {len(df):,} ślokas")
    else:
        raise FileNotFoundError("Database not found!")
    
    return df


def create_searchable_text(df):
    """Create combined searchable text for each śloka"""
    print("📝 Creating searchable text...")
    
    # Combine all text columns for better semantic understanding
    df['search_text'] = (
        df['File Name'].fillna('').astype(str) + ' ' +
        df['Sthana'].fillna('').astype(str) + ' ' +
        df['Sloka Text'].fillna('').astype(str) + ' ' +
        df['IAST'].fillna('').astype(str) + ' ' +
        df['Roman'].fillna('').astype(str)
    )
    
    return df


def load_model():
    """Load the sentence transformer model"""
    print("🤖 Loading AI model (first run downloads ~500MB)...")
    print(f"   Model: {MODEL_NAME}")
    
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("\n❌ sentence-transformers not installed!")
        print("   Run: pip install sentence-transformers")
        raise
    
    model = SentenceTransformer(MODEL_NAME)
    print("   ✅ Model loaded!")
    
    return model


def create_embeddings(model, texts, batch_size=64):
    """Create embeddings for all texts"""
    print(f"🔢 Creating embeddings for {len(texts):,} ślokas...")
    print(f"   This may take 10-15 minutes...")
    
    start_time = time.time()
    
    # Create embeddings in batches
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    
    elapsed = time.time() - start_time
    print(f"   ✅ Done in {elapsed/60:.1f} minutes!")
    
    return embeddings


def save_embeddings(embeddings, df):
    """Save embeddings and metadata"""
    print("💾 Saving embeddings...")
    
    # Save embeddings as numpy array
    np.save(EMBEDDINGS_PATH, embeddings)
    print(f"   Embeddings saved: {EMBEDDINGS_PATH}")
    print(f"   Size: {EMBEDDINGS_PATH.stat().st_size / (1024*1024):.1f} MB")
    
    # Save metadata (for quick lookup)
    metadata = df[['File Name', 'Sthana', 'Chapter_Number', 'Sloka_Number_Int', 
                   'Sloka Text', 'IAST', 'Roman', 'ASCII']].copy()
    metadata.to_parquet(METADATA_PATH, index=False)
    print(f"   Metadata saved: {METADATA_PATH}")
    
    return True


def test_semantic_search(model, embeddings, df, query="obesity treatment"):
    """Test the semantic search"""
    print(f"\n🧪 Testing semantic search...")
    print(f"   Query: '{query}'")
    
    # Create query embedding
    query_embedding = model.encode([query], convert_to_numpy=True)
    
    # Calculate cosine similarity
    from numpy.linalg import norm
    
    similarities = []
    for i, emb in enumerate(embeddings):
        sim = np.dot(query_embedding[0], emb) / (norm(query_embedding[0]) * norm(emb))
        similarities.append(sim)
    
    # Get top 5 results
    top_indices = np.argsort(similarities)[-5:][::-1]
    
    print(f"\n   Top 5 Results:")
    print("   " + "-" * 60)
    
    for idx in top_indices:
        row = df.iloc[idx]
        sim = similarities[idx]
        print(f"   [{sim:.3f}] {row['File Name']} - {row['Sthana']} Ch.{row['Chapter_Number']}")
        print(f"           {row['Sloka Text'][:60]}...")
        print()


def main():
    """Main setup function"""
    print("=" * 70)
    print("🪷 Bhruhat Trayi AI Assistant - Semantic Search Setup")
    print("=" * 70)
    print()
    
    # Check if embeddings already exist
    if EMBEDDINGS_PATH.exists():
        print(f"⚠️  Embeddings already exist at: {EMBEDDINGS_PATH}")
        response = input("   Recreate? (y/n): ").lower()
        if response != 'y':
            print("   Skipping. Use existing embeddings.")
            return
    
    # Step 1: Load database
    df = load_database()
    
    # Step 2: Create searchable text
    df = create_searchable_text(df)
    texts = df['search_text'].tolist()
    
    # Step 3: Load model
    model = load_model()
    
    # Step 4: Create embeddings
    embeddings = create_embeddings(model, texts)
    
    # Step 5: Save
    save_embeddings(embeddings, df)
    
    # Step 6: Test
    test_semantic_search(model, embeddings, df, "obesity treatment")
    test_semantic_search(model, embeddings, df, "diabetes management")
    test_semantic_search(model, embeddings, df, "definition of health")
    
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    print()
    print("Files created:")
    print(f"   📊 {EMBEDDINGS_PATH}")
    print(f"   📋 {METADATA_PATH}")
    print()
    print("Next steps:")
    print("   1. Restart your Streamlit app")
    print("   2. The app will automatically use semantic search!")
    print()


if __name__ == "__main__":
    main()
