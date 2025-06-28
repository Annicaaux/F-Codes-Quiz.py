import streamlit as st
import datetime as datetime, time
import random 


# --Titel der Aplikation--
st.set_page_config(
    page_title="Ernie, Bernie, ich muss lernie sonst werd ich sterbie",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# --Css-Stil 
# --- Custom CSS - Optimiert für Mobile ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #A0616A 0%, #6B2C3A 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container spacing fixes */
    .element-container {
        margin-bottom: 1rem !important;
    }
    
    .stMarkdown {
        margin-bottom: 0.5rem !important;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        font-size: clamp(2rem, 5vw, 3rem);
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: white;
        font-size: clamp(1rem, 3vw, 1.2rem);
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    /* Tab styling - Mobile optimized */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255, 255, 255, 0.1);
        padding: 6px;
        border-radius: 25px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        overflow-x: auto;
        flex-wrap: nowrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        min-height: 40px;
        padding: 8px 16px;
        background: transparent;
        border-radius: 20px;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
        font-size: 0.9rem;
        white-space: nowrap;
        flex-shrink: 0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B5A6B, #6B2C3A) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(139, 90, 107, 0.4);
    }
    
    
    /* Group header - Mobile responsive */
    .group-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .group-icon {
        width: clamp(50px, 12vw, 60px);
        height: clamp(50px, 12vw, 60px);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: clamp(1.2rem, 4vw, 1.8rem);
        background: linear-gradient(135deg, #A0616A, #6B2C3A);
        color: white;
        box-shadow: 0 4px 15px rgba(160, 97, 106, 0.3);
        flex-shrink: 0;
    }
    
    .group-title {
        font-size: clamp(1.1rem, 4vw, 1.4rem);
        font-weight: 600;
        color: #1f2937 !important;
        margin: 0;
        line-height: 1.3;
    }
    
    /* Meta information - Mobile stack */
    .group-meta {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
        font-size: 0.85rem;
        color: #6b7280;
        flex-wrap: wrap;
    }
    
    .meta-item {
        display: flex;
        align-items: center;
        gap: 0.3rem;
        background: #f3f4f6;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-weight: 500;
        font-size: 0.8rem;
        flex-shrink: 0;
    }
    
    /* Question styling */
    .group-question {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #BE185D;
    }
    
    .question-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #831843;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .question-text {
        font-style: italic;
        color: #374151;
        font-size: clamp(0.9rem, 3vw, 1.1rem);
        line-height: 1.5;
    }
    
    .spaces-badge {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        color: #831843;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #F9A8D4;
        display: inline-block;
    }
    
    /* Form improvements */
    .form-title {
        text-align: center;
        font-size: clamp(1.3rem, 4vw, 1.8rem);
        font-weight: 600;
        color: #374151;
        margin-bottom: 1.5rem;
        line-height: 1.3;
    }
    
    /* Button styling - Touch friendly */
    .stButton > button {
        background: linear-gradient(135deg, #A0616A, #6B2C3A);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(160, 97, 106, 0.4);
        min-height: 44px; /* Touch target size */
        font-size: 0.9rem;
        width: 100%;
    }
    
    
    /* Input styling - Mobile friendly */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stTimeInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 0.8rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        min-height: 44px; /* Touch target */
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stTimeInput > div > div > input:focus {
        border-color: #A0616A;
        box-shadow: 0 0 0 3px rgba(160, 97, 106, 0.1);
        outline: none;
    }
    
    /* Metrics styling - Mobile grid */
    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: clamp(1.5rem, 5vw, 2rem);
        font-weight: 700;
        color: white;
        line-height: 1;
    }
    
    .metric-label {
        font-size: clamp(0.8rem, 2.5vw, 0.9rem);
        color: rgba(255, 255, 255, 0.8);
        margin-top: 0.5rem;
        line-height: 1.2;

    /* Mobile specific adjustments */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 0.8rem;
            padding: 6px 12px;
        }
        
        .group-header {
            flex-direction: column;
            align-items: flex-start;
            text-align: left;
        }
        
        .group-meta {
            flex-direction: column;
            gap: 0.3rem;
        }
        
        .meta-item {
            width: fit-content;
        }
        
        /* Smaller padding on mobile */
        .group-card, .form-container, .my-group-card, .pinnwand-container {
            padding: 1rem;
            margin: 0.5rem auto;
        }
        
        /* Stack columns on mobile */
        .stColumns {
            flex-direction: column !important;
        }
        
        .stColumn {
            width: 100% !important;
            margin-bottom: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 0.7rem;
            padding: 4px 8px;
        }

     
    /* Text color fixes for all containers */
    .stForm, .stExpander, .stSelectbox label, .stTextInput label, 
    .stTextArea label, .stTimeInput label, .stSlider label,
    .stRadio label, .stCheckbox label {
        color: #374151 !important;
    }

  
</style>
""", unsafe_allow_html=True)

 # Title and subtitle
st.markdown('<h1 class="main-title">Ernie, Bernie, ich muss lernie</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">sonst werd ich sterbie</p>', unsafe_allow_html=True)
   
""", unsafe_allow_html=True)

   
