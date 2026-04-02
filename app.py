import streamlit as st
import os
import pandas as pd
from src.data_prep import clean_data
from src.vector_db import create_vector_db
from src.rag_pipeline import MedicineRAG

# Page Configuration
st.set_page_config(
    page_title="Pakistan Medicine Identifier (RAG AI)",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Premium Corporate Identity
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');

    /* Global Typography */
    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Professional Corporate Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
    }

    /* Enhanced Hero Title */
    .hero-title {
        background: linear-gradient(to right, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        letter-spacing: -1.5px;
        text-align: center;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        font-weight: 400;
        letter-spacing: 2px;
        text-align: center;
        text-transform: uppercase;
    }

    /* Clinical Dark Card (Dynamic Height) */
    .medicine-card {
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 26px;
        margin-bottom: 25px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        color: #ffffff !important;
        height: auto !important; /* Allow content to define height */
    }

    .medicine-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        border-color: rgba(59, 130, 246, 0.4);
        background: rgba(30, 41, 59, 0.85) !important;
    }

    .medicine-card h4 {
        color: #3b82f6 !important; /* Azure Blue */
        font-size: 1.6rem !important;
        margin-bottom: 18px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: -0.5px;
        border-bottom: 2.5px solid rgba(59, 130, 246, 0.2);
        padding-bottom: 10px;
        margin-top: 0;
    }

    .label {
        font-weight: 700;
        color: #94a3b8; /* Lighter Slate */
        margin-right: 10px;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }

    /* Premium Search Input */
    .stTextInput label {
        display: none !important;
    }
    .stTextInput input {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1.5px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 50px !important;
        color: white !important;
        padding: 20px 30px !important;
        font-size: 1rem !important;
        outline: none !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.05) !important;
        letter-spacing: 0.3px;
    }
    .stTextInput input::placeholder {
        color: rgba(148, 163, 184, 0.6) !important;
        font-weight: 400 !important;
        font-style: italic !important;
    }
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 3px rgba(59, 130, 246, 0.15), inset 0 1px 0 rgba(255,255,255,0.05) !important;
        outline: none !important;
    }

    /* Kill Streamlit's red focus indicator */
    .stTextInput div[data-baseweb="input"],
    .stTextInput [data-baseweb="base-input"],
    .stTextInput div[data-baseweb="input"]:focus-within {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* Search Suggestions: solid blue, white text */
    div[data-testid="stHorizontalBlock"] .stButton > button {
        background: #3b82f6 !important;
        background-color: #3b82f6 !important;
        background-image: none !important;
        border: none !important;
        color: white !important;
        border-radius: 30px !important;
        font-size: 0.95rem !important;
        transition: none !important;
        box-shadow: none !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
    }

    /* Keep same color on all states */
    div[data-testid="stHorizontalBlock"] .stButton > button:hover,
    div[data-testid="stHorizontalBlock"] .stButton > button:active,
    div[data-testid="stHorizontalBlock"] .stButton > button:focus {
        background: #3b82f6 !important;
        background-color: #3b82f6 !important;
        background-image: none !important;
        border: none !important;
        color: white !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* Main Action Button (Emerald Green) */
    div.stButton > button:not([key*="sug_btn_"]) {
        background: #10b981 !important;
        background-color: #10b981 !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 18px 35px !important;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.4) !important;
        font-size: 1.1rem !important;
    }

    /* Keep same green on all states */
    div.stButton > button:not([key*="sug_btn_"]):hover,
    div.stButton > button:not([key*="sug_btn_"]):active,
    div.stButton > button:not([key*="sug_btn_"]):focus {
        background: #10b981 !important;
        background-color: #10b981 !important;
        color: white !important;
        transform: none !important;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.4) !important;
    }

    /* Professional Clinical Disclaimer */
    .disclaimer {
        margin-top: 15px;
        background: rgba(239, 68, 68, 0.03);
        border: 1px solid rgba(239, 68, 68, 0.1);
        padding: 10px;
        border-radius: 8px;
        font-size: 0.75rem;
        color: #fca5a5;
        line-height: 1.4;
    }

    /* Sidebar Refinement */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }

    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# App Hero Section
st.markdown("""
<div style="text-align: center; padding: 20 px 0;">
    <h1 class="hero-title">MediSearch Pakistan</h1>
    <p class="hero-subtitle">Industrial AI Medicine Analytics & Clinical Indexing</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <i class="fas fa-shield-halved" style="font-size: 3rem; color: #3b82f6; margin-bottom: 15px;"></i>
            <h2 style='color: #ffffff; margin-bottom: 0; font-size: 1.5rem;'>MEDISEARCH AI</h2>
            <p style='color: #64748b; font-size: 0.75rem;'>Clinical Index v3.3</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Medical Safety Protocol
    st.markdown("""
        <h3 style='color: #94a3b8; font-size: 1.1rem; margin-bottom: 15px;'>
            <i class='fas fa-triangle-exclamation' style='margin-right: 8px;'></i> SAFETY PROTOCOL
        </h3>
    """, unsafe_allow_html=True)
    
    st.info("""
    **Corporate Compliance:**
    1. Educational / Research reference only.
    2. Consultation with a Licensed Practitioner is mandatory.
    3. Not a substitute for professional medical advice.
    """)
    
    st.divider()
    st.markdown("<div style='text-align: center; color: #3b82f6; font-size: 0.8rem;'><i class='fas fa-microchip'></i> Neural Engine Synchronized</div>", unsafe_allow_html=True)

# Ensure data and models are ready
DATA_DIR = 'data'
RAW_DATA_PATH = os.path.join(DATA_DIR, 'medicine_data.csv')
CLEANED_DATA_PATH = os.path.join(DATA_DIR, 'medicine_cleaned.csv')
INDEX_PATH = os.path.join(DATA_DIR, 'medicine_index.faiss')
MAPPINGS_PATH = os.path.join(DATA_DIR, 'medicine_mappings.pkl')

@st.cache_resource
def initialize_rag(_mtime):
    if not os.path.exists(INDEX_PATH) or not os.path.exists(MAPPINGS_PATH):
        if os.path.exists(RAW_DATA_PATH):
            with st.spinner("Initializing Clinical Index..."):
                clean_data(RAW_DATA_PATH, CLEANED_DATA_PATH)
                create_vector_db(CLEANED_DATA_PATH, INDEX_PATH, MAPPINGS_PATH)
        else:
            st.error("Error: Dataset missing.")
            return None
    
    return MedicineRAG(INDEX_PATH, MAPPINGS_PATH)

import time
csv_mtime = os.path.getmtime(RAW_DATA_PATH) if os.path.exists(RAW_DATA_PATH) else 0
rag = initialize_rag(csv_mtime)

if rag:
    # Centered Search Layout
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        # Initialize suggestions state
        if "selected_query" not in st.session_state:
            st.session_state.selected_query = None

        # Search Header
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <i class="fas fa-magnifying-glass" style="color: #3b82f6; font-size: 1.3rem;"></i>
                <span style="color: #94a3b8; font-size: 1rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">Search Medicine</span>
            </div>
        """, unsafe_allow_html=True)

        # Search Input
        user_query = st.text_input(
            "Search",
            placeholder="Type a medicine name, generic, or symptom...",
            key="main_search",
            label_visibility="collapsed"
        )
        st.markdown("<p style='color: #64748b; font-size: 0.75rem; margin: 8px 0 0 15px; font-style: italic;'><i class='fas fa-circle-info' style='margin-right: 6px;'></i>For informational purposes only. Always consult a licensed doctor before taking any medication.</p>", unsafe_allow_html=True)
        
        # Suggestions Logic
        suggestions = []
        if user_query:
            suggestions = rag.get_suggestions(user_query)
        
        if suggestions:
            st.markdown(f"<p style='color: #94a3b8; font-size: 0.8rem; margin: 15px 0 5px 0;'><i class='fas fa-magnifying-glass'></i> DID YOU MEAN?</p>", unsafe_allow_html=True)
            sug_cols = st.columns(len(suggestions))
            for i, sug in enumerate(suggestions):
                # Custom keys starting with 'sug_btn_' will be targeted by CSS
                if sug_cols[i].button(sug, key=f"sug_btn_{i}", use_container_width=True):
                    st.session_state.selected_query = sug
                    st.rerun()

        # Decide which query to resolve
        final_query = st.session_state.selected_query if st.session_state.selected_query else user_query
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        search_btn = st.button("RUN CLINICAL ANALYTICS", use_container_width=True)

    # Execution
    if final_query or (search_btn if 'search_btn' in locals() else False):
        query_to_run = final_query.lower() if final_query else ""
        if query_to_run:
            with st.spinner(f"Analyzing Clinical Index for: {final_query}..."):
                results = rag.query(query_to_run, k=10)
                st.session_state.selected_query = None

                if results:
                    # Categorize Results: Top 3 and 3 Other Relevant
                    top_matches = results[:3]
                    other_relevant = results[3:6]

                    # 1. Top Matches Row
                    st.markdown(f"""
                        <h3 style='color: #ffffff; margin-top: 30px; margin-bottom: 20px;'>
                            <i class='fas fa-award' style='color: #fbbf24; margin-right: 12px;'></i> 
                            TOP CLINICAL MATCHES FOR '{final_query.upper()}'
                        </h3>
                    """, unsafe_allow_html=True)
                    
                    top_cols = st.columns(3)
                    
                    # Icons for all data points
                    icon_map = {
                        "Generic Name": "flask-vial",
                        "Used for": "notes-medical",
                        "Side Effects": "triangle-exclamation",
                        "Dosage Form": "prescription-bottle",
                        "Dosage Amount": "pills",
                        "Source Reference": "certificate"
                    }
                    
                    fields_to_show = ["Generic Name", "Used for", "Side Effects", "Dosage Form", "Dosage Amount"]
                    
                    for i, r in enumerate(top_matches):
                        with top_cols[i]:
                            fields_html = ""
                            # Map keys to clinical labels
                            data_map = {
                                "Generic Name": r.get("generic_name", ""),
                                "Used for": r.get("indications", ""),
                                "Side Effects": r.get("side_effects", ""),
                                "Dosage Form": r.get("dosage_form", ""),
                                "Dosage Amount": r.get("dosage", "")
                            }
                            
                            for label in fields_to_show:
                                val = data_map[label]
                                if val and str(val).lower() not in ["", "nan", "information not available"]:
                                    if label == "Generic Name":
                                        fields_html += f'<p style="font-size: 1.05rem; margin-bottom: 12px; line-height: 1.5; color: #ffffff;"><span class="label" style="color: #94a3b8;">{label}:</span> <strong style="color: #e2e8f0;">{val}</strong></p>'
                                    else:
                                        fields_html += f'<p style="font-size: 1rem; margin-bottom: 10px; line-height: 1.5; color: #cbd5e1;"><span class="label" style="color: #94a3b8;">{label}:</span> {val}</p>'
                            
                            source_val = r.get("source", "Standard Reference")
                            st.markdown(f"""
                            <div class="medicine-card" style="border-top: 4px solid #3b82f6;">
                                <h4 style="margin-top: 0; color: #3b82f6; font-size: 1.4rem;">{r.get('brand_name', 'Unknown Brand').upper()}</h4>
                                {fields_html}
                                <div style="margin-top: 20px; border-top: 1px solid rgba(148, 163, 184, 0.1); padding-top: 12px; font-size: 0.8rem; color: #94a3b8; font-style: italic;">
                                    <i class="fas fa-certificate" style="color: #3b82f6;"></i> &nbsp;Verified Source: {source_val}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                    # 2. Other Relevant Row
                    if other_relevant:
                        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
                        st.markdown(f"""
                            <h3 style='color: #94a3b8; margin-bottom: 25px; font-weight: 600;'>
                                <i class='fas fa-layer-group' style='margin-right: 15px;'></i> 
                                RELEVANT PHARMACEUTICAL OPTIONS
                            </h3>
                        """, unsafe_allow_html=True)
                        
                        rel_cols = st.columns(len(other_relevant))
                        
                        for i, r in enumerate(other_relevant):
                            with rel_cols[i]:
                                fields_html = ""
                                data_map = {
                                    "Generic Name": r.get("generic_name", ""),
                                    "Used for": r.get("indications", ""),
                                    "Side Effects": r.get("side_effects", ""),
                                    "Dosage Form": r.get("dosage_form", ""),
                                    "Dosage Amount": r.get("dosage", "")
                                }
                                for label in fields_to_show:
                                    val = data_map[label]
                                    if val and str(val).lower() not in ["", "nan", "information not available"]:
                                        if label == "Generic Name":
                                            fields_html += f'<p style="font-size: 1.05rem; margin-bottom: 12px; line-height: 1.5; color: #ffffff;"><span class="label" style="color: #94a3b8;">{label}:</span> <strong style="color: #e2e8f0;">{val}</strong></p>'
                                        else:
                                            fields_html += f'<p style="font-size: 1rem; margin-bottom: 10px; line-height: 1.5; color: #cbd5e1;"><span class="label" style="color: #94a3b8;">{label}:</span> {val}</p>'
                                
                                st.markdown(f"""
                                <div class="medicine-card" style="border-top: 4px solid #64748b;">
                                    <h4 style="margin-top: 0; color: #3b82f6; font-size: 1.4rem;">{r.get('brand_name', 'Unknown Brand').upper()}</h4>
                                    {fields_html}
                                    <div style="margin-top: 20px; border-top: 1px solid rgba(148, 163, 184, 0.1); padding-top: 12px; font-size: 0.8rem; color: #94a3b8; font-style: italic;">
                                        <i class="fas fa-building"></i> &nbsp;Clinical Pharma Index
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color: #fca5a5; background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2); padding: 20px; border-radius: 12px; text-align: center;'><i class='fas fa-circle-exclamation' style='margin-right: 10px;'></i> NO HIGH-INTEGRITY MATCHES FOUND FOR THIS QUERY.</p>", unsafe_allow_html=True)
                    st.info("The query doesn't match our clinical records. Please enter a valid PKR brand name, generic formulation, or medical symptom.")
else:
    st.warning("System initialization failed.")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.85rem;'>MediSearch AI v3.4 | Pakistan Pharmaceutical Analytics Index | 2024 Corporate Release</p>", unsafe_allow_html=True)
