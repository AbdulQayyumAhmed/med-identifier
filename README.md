# MediSearch Pakistan 💊
### Professional Clinical AI Medicine Analytics & Clinical Indexing

**MediSearch Pakistan** is a high-performance Retrieval-Augmented Generation (RAG) system designed for the Pakistan pharmaceutical index. It enables users to search for medications via brand names, generic formulations, or medical symptoms, providing detailed clinical analytics, dosage forms, and safety protocols through a premium corporate-grade interface.

---

## 🚀 Key Features

- **Semantic Search Engine**: Beyond exact keyword matches, find medicines based on their uses (indications), symptoms, or generic formulas.
- **Clinical RAG Pipeline**: Combines **Sentence Transformers** (MiniLM-L6-v2) and **FAISS** (Facebook AI Similarity Search) for high-integrity retrieval.
- **Intelligent suggestions**: Features a fuzzy-matching search suggestion system (Did You Mean?) to handle typos and common misspellings.
- **Premium Corporate UI**: A sophisticated dark-mode dashboard built with **Streamlit**, featuring CSS-enhanced components and responsive layouts.
- **Comprehensive Data Points**: View generic names, indications, side effects, dosage forms, and verified clinical sources.

---

## 🏗️ Technical Architecture

- **Frontend**: Streamlit (Python) with custom CSS & FontAwesome integration.
- **Vector Database**: FAISS (Index-FlatL2) for sub-millisecond retrieval.
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`).
- **Data Engineering**: Pandas for cleaning and indexing 1,000+ medicine records.
- **Safety**: Built-in Clinical Disclaimer and pharmaceutical safety protocols.

---

## 📂 Project Structure

```bash
FYP/
├── medicine_identifier/
│   ├── app.py              # Main application entry point
│   ├── requirements.txt    # Python dependencies
│   ├── data/
│   │   ├── medicine_data.csv        # Raw dataset
│   │   ├── medicine_index.faiss     # Encrypted vector index
│   │   └── medicine_mappings.pkl    # Metadata mappings
│   └── src/
│       ├── data_prep.py     # Data cleaning engine
│       ├── vector_db.py     # Index creation script
│       └── rag_pipeline.py  # Core AI logic (Retrieval)
└── README.md
```

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd FYP
   ```

2. **Install dependencies**:
   ```bash
   pip install -r medicine_identifier/requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run medicine_identifier/app.py
   ```

---

## ⚖️ Medical Disclaimer

> [!CAUTION]
> This application is for **educational and research purposes only**. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

---

## 📜 Metadata
- **Version**: 3.4
- **Index**: Clinical v3.3
- **Status**: Production-Ready Corporate Release
