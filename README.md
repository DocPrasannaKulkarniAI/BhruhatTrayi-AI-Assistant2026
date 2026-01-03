# 🪷 Bhruhat Trayi AI Assistant by PraKul

## AI-Powered Classical Āyurvedic Text Explorer

**Version 8.0** | Created by **Prof.(Dr.) Prasanna Kulkarni**

---

## 📖 What is This?

The **Bhruhat Trayi AI Assistant** is a FREE, AI-powered tool for exploring classical Āyurvedic texts. It combines:

- 📚 **24,851 ślokas** from the three foundational texts (Bhruhat Trayi)
- 🤖 **AI TrayiDuta** - An intelligent chatbot for understanding ślokas
- 🔍 **Smart Search** - Finds relevant ślokas with synonym expansion
- 📝 **Role-based Responses** - Tailored for Students, Physicians, Teachers, etc.

### The Three Texts (Bhruhat Trayi):
1. **Charaka Saṃhitā** - Internal Medicine
2. **Suśruta Saṃhitā** - Surgery
3. **Aṣṭāṅga Hṛdaya** - Comprehensive Compendium

---

## 🚀 Quick Start

### Step 1: Install Requirements
```bash
pip install streamlit pandas openpyxl pyarrow openai
```

### Step 2: Add Your OpenAI API Key
1. Open `config.py`
2. Replace `sk-proj-YOUR_KEY_HERE` with your actual API key
3. Get a key from: https://platform.openai.com/api-keys

### Step 3: Run the App
```bash
python -m streamlit run app.py
```

### Step 4: Open in Browser
Go to: http://localhost:8501

---

## 📋 How to Use

### 🔍 Tab 1: Search Ślokas

1. **Select Texts** - Check which Saṃhitās to search (all selected by default)
2. **Select Role** - Choose your perspective (Student is default)
3. **Enter Question** - Type your query (e.g., "What is Vata?")
4. **Click Search** - View matching ślokas with references

#### Disambiguation Feature
If your term has multiple meanings (e.g., "Vata" = Dosha OR Plant), the app will ask you to clarify!

### 💬 Tab 2: Chat with AI TrayiDuta

1. **Search First** - Find ślokas in the Search tab
2. **Switch to Chat** - Click the "Chat with AI" tab
3. **Ask Questions** - AI TrayiDuta will explain the ślokas
4. **Quick Prompts** - Use buttons for common questions

#### Chat Features:
- 💡 **Simple Explanations** - Easy-to-understand summaries
- 📝 **Anvaya (Word-by-word)** - Request detailed translations
- 📖 **References** - Every response cites ślokas (e.g., च.सं.सू.1/57)
- ⭐ **Role-specific** - Responses tailored to your selected role

---

## 🎯 Key Features

### ✅ Smart Search
- **Synonym Expansion** - Searches for related terms automatically
- **500+ Āyurvedic Terms** - Built-in dictionary
- **Spelling Correction** - Suggests fixes for typos
- **Modern → Classical** - Converts terms like "diabetes" to "prameha"

### ✅ Query Disambiguation
Handles ambiguous terms like:
| Term | Meaning 1 | Meaning 2 |
|------|-----------|-----------|
| Vata | वात Dosha | वट Plant (Banyan) |
| Bala | बल Strength | बला Drug (Sida) |
| Amrita | अमृत Nectar | गुडूची Drug |
| Madhu | मधु Honey | मधुक Drug |

### ✅ AI TrayiDuta Chatbot
- **GPT-4o-mini** powered (cost-effective)
- **Anvaya only on request** - Keeps responses concise
- **Always cites references** - Academic integrity
- **5 Role Profiles** - Student, PG Scholar, Teacher, Researcher, Physician

### ✅ Performance Optimized
- **Cached Database** - Fast loading after first time
- **Efficient Search** - Quick results

---

## 📁 File Structure

```
BhruhatTrayi_AI_PraKul/
├── app.py                    # Main application
├── config.py                 # API key & settings
├── chat_module.py            # AI TrayiDuta chatbot
├── query_disambiguation.py   # Ambiguous term handling
├── query_analyzer.py         # Query type detection
├── enhanced_search.py        # Smart search engine
├── ayurvedic_synonyms.py     # 500+ terms dictionary
├── prompt_templates.py       # Role-based prompts
├── setup_embeddings.py       # AI embeddings (optional)
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── all3_cleaned.parquet      # Database (required)
├── sloka_embeddings.npy      # AI embeddings (optional)
├── sloka_metadata.parquet    # Metadata (optional)
└── Atharva_Logo.jpg          # Logo image
```

---

## ⚙️ Configuration

### config.py Settings

```python
# API Key (required for chat)
OPENAI_API_KEY = "sk-proj-YOUR_KEY_HERE"

# Model (gpt-4o-mini is cheapest)
OPENAI_MODEL = "gpt-4o-mini"

# Chatbot name
CHATBOT_NAME = "AI TrayiDuta"
CHATBOT_NAME_SANSKRIT = "AI त्रयीदूत"

# Response settings
MAX_OUTPUT_TOKENS = 2048
TEMPERATURE = 0.3
```

### Cost Estimate (OpenAI)

| Usage | Cost (GPT-4o-mini) |
|-------|---------------------|
| 1 chat | ~$0.001 |
| 100 chats/day | ~$0.10/day |
| 1000 chats/day | ~$1.00/day |

$5 balance = ~5,000 chat sessions!

---

## 🔧 Troubleshooting

### "Could not configure OpenAI"
1. Check your API key in `config.py`
2. Ensure no extra spaces or quotes
3. Verify key at: https://platform.openai.com/api-keys

### "OpenAI package not installed"
```bash
pip install openai
```

### "Database not found"
Place `all3_cleaned.parquet` in the same folder as `app.py`

### App is slow
- First load is slower (caching)
- Subsequent loads are fast
- Use `python -m streamlit run app.py` for best performance

---

## 📚 For Developers

### Adding New Ambiguous Terms
Edit `query_disambiguation.py`:
```python
AMBIGUOUS_TERMS = {
    "your_term": [
        ("Meaning 1", "Description", "search hint keywords"),
        ("Meaning 2", "Description", "search hint keywords"),
    ],
}
```

### Adding New Synonyms
Edit `ayurvedic_synonyms.py`:
```python
AYURVEDIC_SYNONYMS = {
    "primary_term": ["synonym1", "synonym2", "synonym3"],
}
```

---

## 🙏 Credits

- **Creator**: Prof.(Dr.) Prasanna Kulkarni
- **Institution**: (Your Institution)
- **AI Chatbot**: AI TrayiDuta (AI त्रयीदूत)
- **Powered by**: OpenAI GPT-4o-mini

---

## 📜 Disclaimer

This tool is for **educational purposes only**. Always refer to original Saṃhitā texts and consult qualified Āyurvedic practitioners for clinical decisions.

---

## 🌟 Version History

| Version | Features |
|---------|----------|
| 8.0 | AI TrayiDuta, Disambiguation, Enhanced UI |
| 7.1 | OpenAI Integration |
| 7.0 | Gemini Chat Integration |
| 6.0 | Enhanced Search, Synonyms |
| 5.0 | Role-based Prompts |

---

**सर्वे भवन्तु सुखिनः 🙏**

*May all beings be happy and healthy*
