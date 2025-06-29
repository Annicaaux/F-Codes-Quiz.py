import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="🌲 Klinische Psychologie Lernwald",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS für Wald-Theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #2d5016 0%, #3e7b1f 50%, #4a7c2a 100%);
        background-attachment: fixed;
    }
    
    .stApp {
        background: linear-gradient(135deg, #2d5016 0%, #3e7b1f 50%, #4a7c2a 100%);
    }
    
    .forest-card {
        background: rgba(76, 175, 80, 0.1);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #4CAF50;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
    
    .tree-progress {
        background: linear-gradient(90deg, #2e7d32, #4caf50, #81c784);
        border-radius: 20px;
        padding: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .leaf-badge {
        background: #4CAF50;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        margin: 2px;
        display: inline-block;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1b5e20, #2e7d32);
    }
    
    h1, h2, h3 {
        color: #2e7d32 !important;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(46, 125, 50, 0.1);
        border: 2px solid #4CAF50;
    }
    
    .forest-emoji {
        font-size: 2em;
        margin: 0 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'total_points' not in st.session_state:
    st.session_state.total_points = 0
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'current_level' not in st.session_state:
    st.session_state.current_level = 1
if 'unlocked_areas' not in st.session_state:
    st.session_state.unlocked_areas = ['Einführung']

# ICD-10 F-Diagnosen Datenbank
icd_10_data = {
    "F00-F09": {
        "name": "Organische psychische Störungen",
        "codes": {
            "F00": "Demenz bei Alzheimer-Krankheit",
            "F01": "Vaskuläre Demenz",
            "F02": "Demenz bei anderenorts klassifizierten Krankheiten",
            "F03": "Nicht näher bezeichnete Demenz",
            "F04": "Organisches amnestisches Syndrom",
            "F05": "Delir",
            "F06": "Andere psychische Störungen aufgrund einer Schädigung oder Funktionsstörung des Gehirns",
            "F07": "Persönlichkeits- und Verhaltensstörung aufgrund einer Krankheit",
            "F09": "Nicht näher bezeichnete organische oder symptomatische psychische Störung"
        }
    },
    "F10-F19": {
        "name": "Psychische und Verhaltensstörungen durch psychotrope Substanzen",
        "codes": {
            "F10": "Alkohol",
            "F11": "Opioide",
            "F12": "Cannabinoide",
            "F13": "Sedativa oder Hypnotika",
            "F14": "Kokain",
            "F15": "Andere Stimulanzien",
            "F16": "Halluzinogene",
            "F17": "Tabak",
            "F18": "Flüchtige Lösungsmittel",
            "F19": "Multipler Substanzgebrauch"
        }
    },
    "F20-F29": {
        "name": "Schizophrenie, schizotype und wahnhafte Störungen",
        "codes": {
            "F20": "Schizophrenie",
            "F21": "Schizotype Störung",
            "F22": "Anhaltende wahnhafte Störungen",
            "F23": "Akute vorübergehende psychotische Störungen",
            "F24": "Induzierte wahnhafte Störung",
            "F25": "Schizoaffektive Störungen",
            "F28": "Sonstige nichtorganische psychotische Störungen",
            "F29": "Nicht näher bezeichnete nichtorganische Psychose"
        }
    },
    "F30-F39": {
        "name": "Affektive Störungen",
        "codes": {
            "F30": "Manische Episode",
            "F31": "Bipolare affektive Störung",
            "F32": "Depressive Episode",
            "F33": "Rezidivierende depressive Störung",
            "F34": "Anhaltende affektive Störungen",
            "F38": "Andere affektive Störungen",
            "F39": "Nicht näher bezeichnete affektive Störung"
        }
    },
    "F40-F48": {
        "name": "Neurotische, Belastungs- und somatoforme Störungen",
        "codes": {
            "F40": "Phobische Störungen",
            "F41": "Andere Angststörungen",
            "F42": "Zwangsstörung",
            "F43": "Reaktionen auf schwere Belastungen und Anpassungsstörungen",
            "F44": "Dissoziative Störungen",
            "F45": "Somatoforme Störungen",
            "F48": "Andere neurotische Störungen"
        }
    },
    "F50-F59": {
        "name": "Verhaltensauffälligkeiten mit körperlichen Störungen",
        "codes": {
            "F50": "Essstörungen",
            "F51": "Nichtorganische Schlafstörungen",
            "F52": "Sexuelle Funktionsstörungen",
            "F53": "Psychische oder Verhaltensstörungen im Wochenbett",
            "F54": "Psychologische Faktoren oder Verhaltensfaktoren bei anderenorts klassifizierten Krankheiten",
            "F55": "Schädlicher Gebrauch von nichtabhängigkeitserzeugenden Substanzen",
            "F59": "Nicht näher bezeichnete Verhaltensauffälligkeiten mit körperlichen Störungen"
        }
    },
    "F60-F69": {
        "name": "Persönlichkeits- und Verhaltensstörungen",
        "codes": {
            "F60": "Spezifische Persönlichkeitsstörungen",
            "F61": "Kombinierte und andere Persönlichkeitsstörungen",
            "F62": "Andauernde Persönlichkeitsänderungen",
            "F63": "Abnorme Gewohnheiten und Störungen der Impulskontrolle",
            "F64": "Störungen der Geschlechtsidentität",
            "F65": "Störungen der Sexualpräferenz",
            "F66": "Psychische und Verhaltensstörungen in Verbindung mit der sexuellen Entwicklung",
            "F68": "Andere Persönlichkeits- und Verhaltensstörungen",
            "F69": "Nicht näher bezeichnete Persönlichkeits- und Verhaltensstörung"
        }
    }
}

# Störungsbilder mit Fallbeispielen
stoerungsbilder = {
    "Depression": {
        "emoji": "🌧️",
        "patient": "Maria, 34 Jahre",
        "geschichte": "Maria fühlt sich seit Monaten niedergeschlagen, hat keine Energie mehr für Aktivitäten, die ihr früher Freude bereitet haben. Sie schläft schlecht und grübelt viel.",
        "icd": "F32/F33",
        "symptome": ["Gedrückte Stimmung", "Interessensverlust", "Antriebsmangel", "Schlafstörungen", "Schuldgefühle"],
        "gedankenpalast": "Stelle dir einen dunklen Wald vor, in dem die Bäume ihre Blätter verloren haben. Maria wandelt durch diesen Wald und findet schwer den Weg hinaus."
    },
    "Angststörung": {
        "emoji": "😰",
        "patient": "Thomas, 28 Jahre",
        "geschichte": "Thomas bekommt plötzlich Herzrasen, Schweißausbrüche und das Gefühl zu ersticken, wenn er in Menschenmengen ist. Er meidet deshalb öffentliche Verkehrsmittel.",
        "icd": "F40/F41",
        "symptome": ["Herzrasen", "Schweißausbrüche", "Atemnot", "Vermeidungsverhalten", "Panikattacken"],
        "gedankenpalast": "Stell dir vor, Thomas steht vor einem dichten Dornengestrüpp im Wald. Jeder Schritt vorwärts scheint gefährlich - das ist seine Angst."
    },
    "Schizophrenie": {
        "emoji": "🎭",
        "patient": "Andreas, 22 Jahre",
        "geschichte": "Andreas hört Stimmen, die andere nicht hören können. Er glaubt, dass seine Gedanken von anderen gelesen werden können und zieht sich zunehmend zurück.",
        "icd": "F20",
        "symptome": ["Halluzinationen", "Wahnvorstellungen", "Denkstörungen", "Sozialer Rückzug", "Ich-Störungen"],
        "gedankenpalast": "Andreas wandelt durch einen Zauberwald, wo die Realität verschwimmt - Bäume sprechen, Schatten haben eigene Stimmen."
    },
    "Bipolare Störung": {
        "emoji": "⚡",
        "patient": "Sabine, 31 Jahre",
        "geschichte": "Sabine erlebt Phasen extremer Hochstimmung, in denen sie kaum schläft und viel Geld ausgibt, gefolgt von tiefen depressiven Episoden.",
        "icd": "F31",
        "symptome": ["Manische Episoden", "Depressive Episoden", "Schlafmangel", "Größenwahn", "Stimmungsschwankungen"],
        "gedankenpalast": "Sabines Wald wechselt zwischen strahlendem Sonnenschein mit bunten Blumen und dunklen Gewittern mit Sturm."
    }
}

# Präventions- und Rehabilitationsthemen
praevention_reha = {
    "Motivational Interviewing": {
        "emoji": "💬",
        "prinzipien": ["Empathie ausdrücken", "Diskrepanzen entwickeln", "Widerstand vermeiden", "Selbstwirksamkeit fördern"],
        "techniken": ["Offene Fragen", "Aktives Zuhören", "Reflektieren", "Zusammenfassen"]
    },
    "PACE-Modell": {
        "emoji": "🏃",
        "bedeutung": {
            "P": "Partnership (Partnerschaft)",
            "A": "Acceptance (Akzeptanz)",
            "C": "Curiosity (Neugier)",
            "E": "Empathy (Empathie)"
        }
    },
    "Entscheidungswaage": {
        "emoji": "⚖️",
        "beschreibung": "Tool zur Motivationsförderung durch Abwägen von Vor- und Nachteilen einer Verhaltensänderung",
        "anwendung": "Patient listet Pro und Contra einer Veränderung auf"
    },
    "Universelle Prävention": {
        "emoji": "🛡️",
        "zielgruppe": "Gesamtbevölkerung",
        "beispiele": ["Aufklärungskampagnen", "Gesundheitsförderung in Schulen", "Stressmanagement-Programme"]
    },
    "Rehabilitation": {
        "emoji": "🔄",
        "phasen": ["Akutbehandlung", "Postakute Reha", "Langzeitrehabilitation"],
        "ziele": ["Funktionsverbesserung", "Teilhabe am gesellschaftlichen Leben", "Rückfallprophylaxe"]
    }
}

def get_user_level():
    """Berechne User Level basierend auf Punkten"""
    points = st.session_state.total_points
    if points < 100:
        return 1, "🌱 Setzling"
    elif points < 300:
        return 2, "🌿 Jungpflanze"
    elif points < 600:
        return 3, "🌳 Junger Baum"
    elif points < 1000:
        return 4, "🌲 Starker Baum"
    else:
        return 5, "🌟 Weiser Waldgeist"

def main():
    # Sidebar Navigation
    st.sidebar.markdown("## 🌲 Lernwald Navigation")
    
    # User Progress
    level, level_name = get_user_level()
    st.sidebar.markdown(f"**Level:** {level_name}")
    st.sidebar.markdown(f"**Punkte:** {st.session_state.total_points} 🍃")
    
    if st.session_state.total_questions > 0:
        accuracy = (st.session_state.correct_answers / st.session_state.total_questions) * 100
        st.sidebar.markdown(f"**Genauigkeit:** {accuracy:.1f}%")
    
    st.sidebar.progress(min(st.session_state.total_points / 1000, 1.0))
    
    # Main Navigation
    page = st.sidebar.selectbox(
        "Wähle deinen Lernpfad:",
        [
            "🏠 Waldlichtung (Start)",
            "📚 ICD-10 Kodierungsquiz",
            "🎭 Störungsbilder Gedankenpalast",
            "🧠 Diagnostische Kriterien Quiz",
            "🛡️ Prävention & Rehabilitation",
            "📊 Lernfortschritt"
        ]
    )
    
    # Main Content
    if page == "🏠 Waldlichtung (Start)":
        show_home_page()
    elif page == "📚 ICD-10 Kodierungsquiz":
        show_icd_quiz()
    elif page == "🎭 Störungsbilder Gedankenpalast":
        show_stoerungsbilder()
    elif page == "🧠 Diagnostische Kriterien Quiz":
        show_criteria_quiz()
    elif page == "🛡️ Prävention & Rehabilitation":
        show_prevention_rehab()
    elif page == "📊 Lernfortschritt":
        show_progress()

def show_home_page():
    st.title("🌲 Willkommen im Klinischen Psychologie Lernwald!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🌿 Dein Lernwald wartet auf dich!")
        st.markdown("""
        Begib dich auf eine Reise durch den Wald des Wissens und entdecke die Geheimnisse 
        der klinischen Psychologie. Jeder Baum steht für ein Lerngebiet, jedes Blatt für 
        gelerntes Wissen.
        """)
    
    # Lernbereiche Overview
    st.markdown("## 🌳 Deine Lernbereiche")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📚 ICD-10 Kodierung
        Lerne die F-Diagnosen spielerisch auswendig. Wie ein Förster, der jeden Baum 
        in seinem Wald kennt, wirst du jeden Code beherrschen.
        
        ### 🎭 Störungsbilder
        Wandle durch den Gedankenpalast und begegne verschiedenen Patienten. 
        Jeder hat seine eigene Geschichte im Wald.
        """)
    
    with col2:
        st.markdown("""
        ### 🧠 Diagnostische Kriterien
        Teste dein Wissen über die Kriterien verschiedener Störungen. 
        Wie ein Spurenleser im Wald erkennst du die Zeichen.
        
        ### 🛡️ Prävention & Rehabilitation
        Entdecke, wie man Menschen hilft, ihren Weg aus dem dunklen Wald zu finden 
        und gesund zu bleiben.
        """)
    
    # Tägliche Herausforderung
    st.markdown("## 🎯 Heutige Waldmission")
    
    daily_challenge = random.choice([
        "Lerne 5 neue ICD-10 Codes 📚",
        "Erkunde 2 Störungsbilder im Gedankenpalast 🎭",
        "Beantworte 10 Quizfragen richtig 🧠",
        "Entdecke ein Präventionskonzept 🛡️"
    ])
    
    st.info(f"**Heute:** {daily_challenge}")
    
    # Motivational Quote
    quotes = [
        "Jeder Baum war einmal ein Samen. Jeder Experte war einmal ein Anfänger. 🌱",
        "Im Wald des Wissens gibt es immer neue Pfade zu entdecken. 🌲",
        "Wie ein Baum wächst auch Wissen mit der Zeit und Pflege. 🌿",
        "Der beste Zeitpunkt, einen Baum zu pflanzen, war vor 20 Jahren. Der zweitbeste ist jetzt. 🌳"
    ]
    
    st.success(random.choice(quotes))

def show_icd_quiz():
    st.title("📚 ICD-10 Kodierungsquiz")
    st.markdown("*Wie ein Förster seine Bäume kennst du bald jeden Code!*")
    
    # Quiz Mode Selection
    quiz_mode = st.selectbox(
        "Wähle deinen Lernmodus:",
        ["Code → Störung", "Störung → Code", "Gemischt"]
    )
    
    # Category Selection
    categories = list(icd_10_data.keys())
    selected_category = st.selectbox("Wähle eine Kategorie:", ["Alle"] + categories)
    
    if st.button("🎯 Neue Quizfrage generieren"):
        generate_icd_quiz_question(quiz_mode, selected_category)
    
    # Show current question if exists
    if 'current_icd_question' in st.session_state:
        show_current_icd_question()

def generate_icd_quiz_question(mode, category):
    """Generiere eine neue ICD-10 Quiz Frage"""
    
    # Select codes based on category
    if category == "Alle":
        all_codes = {}
        for cat_data in icd_10_data.values():
            all_codes.update(cat_data["codes"])
    else:
        all_codes = icd_10_data[category]["codes"]
    
    # Random code selection
    code = random.choice(list(all_codes.keys()))
    disorder = all_codes[code]
    
    # Generate question based on mode
    if mode == "Code → Störung":
        question = f"Was bedeutet der ICD-10 Code **{code}**?"
        correct_answer = disorder
        
        # Generate wrong answers
        wrong_answers = random.sample([d for c, d in all_codes.items() if c != code], 3)
        options = [correct_answer] + wrong_answers
        
    elif mode == "Störung → Code":
        question = f"Welcher ICD-10 Code gehört zu: **{disorder}**?"
        correct_answer = code
        
        # Generate wrong codes
        wrong_answers = random.sample([c for c in all_codes.keys() if c != code], 3)
        options = [correct_answer] + wrong_answers
    
    else:  # Gemischt
        if random.choice([True, False]):
            question = f"Was bedeutet der ICD-10 Code **{code}**?"
            correct_answer = disorder
            wrong_answers = random.sample([d for c, d in all_codes.items() if c != code], 3)
        else:
            question = f"Welcher ICD-10 Code gehört zu: **{disorder}**?"
            correct_answer = code
            wrong_answers = random.sample([c for c in all_codes.keys() if c != code], 3)
        
        options = [correct_answer] + wrong_answers
    
    random.shuffle(options)
    
    st.session_state.current_icd_question = {
        "question": question,
        "options": options,
        "correct_answer": correct_answer,
        "answered": False
    }

def show_current_icd_question():
    """Zeige die aktuelle ICD Quiz Frage"""
    q = st.session_state.current_icd_question
    
    st.markdown("### 🌿 Quiz Frage")
    st.markdown(q["question"])
    
    if not q["answered"]:
        selected_option = st.radio("Wähle deine Antwort:", q["options"])
        
        if st.button("🍃 Antwort einreichen"):
            q["answered"] = True
            st.session_state.total_questions += 1
            
            if selected_option == q["correct_answer"]:
                st.session_state.correct_answers += 1
                st.session_state.total_points += 10
                st.success(f"🌳 Richtig! +10 Punkte. Die Antwort ist: {q['correct_answer']}")
                st.balloons()
            else:
                st.error(f"🍂 Falsch. Die richtige Antwort ist: {q['correct_answer']}")
            
            # Memory Palace Tip
            st.info("💡 **Eselsbrücke:** Stelle dir vor, wie diese Störung als charakteristischer Baum in deinem Gedächtniswald wächst!")
    
    else:
        st.info(f"Antwort: {q['correct_answer']}")

def show_stoerungsbilder():
    st.title("🎭 Störungsbilder Gedankenpalast")
    st.markdown("*Wandle durch den Wald der Geschichten und lerne durch Patienten-Begegnungen*")
    
    # Select disorder
    selected_disorder = st.selectbox(
        "Wähle eine Störung zum Erkunden:",
        list(stoerungsbilder.keys())
    )
    
    if selected_disorder:
        disorder_data = stoerungsbilder[selected_disorder]
        
        # Create a visual patient card
        st.markdown(f"## {disorder_data['emoji']} {selected_disorder}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 👤 Patient")
            st.markdown(f"**Name:** {disorder_data['patient']}")
            st.markdown(f"**ICD-10:** {disorder_data['icd']}")
            
            st.markdown("### 🏷️ Symptome")
            for symptom in disorder_data['symptome']:
                st.markdown(f"🍃 {symptom}")
        
        with col2:
            st.markdown("### 📖 Geschichte")
            st.markdown(disorder_data['geschichte'])
            
            st.markdown("### 🏰 Gedankenpalast")
            st.info(disorder_data['gedankenpalast'])
        
        # Interactive elements
        st.markdown("### 🎯 Lernaktivitäten")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧠 Symptome merken"):
                st.success("Präge dir die Symptome ein, indem du sie dem Patienten in deinem Gedankenpalast zuordnest!")
                st.session_state.total_points += 5
        
        with col2:
            if st.button("🎭 Rollenspiel"):
                st.success("Stelle dir vor, du führst ein Gespräch mit diesem Patienten. Was würdest du fragen?")
                st.session_state.total_points += 5
        
        with col3:
            if st.button("🔍 Differentialdiagnose"):
                st.success("Überlege, welche anderen Störungen ähnliche Symptome haben könnten!")
                st.session_state.total_points += 5
        
        # Quiz about this disorder
        if st.button("🎯 Quiz zu dieser Störung"):
            generate_disorder_quiz(selected_disorder, disorder_data)

def generate_disorder_quiz(disorder_name, disorder_data):
    """Generiere Quiz Fragen zu einer spezifischen Störung"""
    
    questions = [
        {
            "question": f"Welcher ICD-10 Code gehört zu {disorder_name}?",
            "correct": disorder_data['icd'],
            "wrong": ["F43.1", "F25.0", "F61.2"]
        },
        {
            "question": f"Welches Symptom gehört NICHT zu {disorder_name}?",
            "correct": "Wahnvorstellungen" if disorder_name != "Schizophrenie" else "Euphorie",
            "wrong": disorder_data['symptome'][:3]
        }
    ]
    
    selected_q = random.choice(questions)
    options = [selected_q["correct"]] + selected_q["wrong"]
    random.shuffle(options)
    
    st.markdown("### 🌿 Spontanes Quiz!")
    st.markdown(selected_q["question"])
    
    answer = st.radio("Deine Antwort:", options, key=f"quiz_{disorder_name}")
    
    if st.button("Antworten", key=f"submit_{disorder_name}"):
        if answer == selected_q["correct"]:
            st.success("🌳 Richtig! +15 Punkte")
            st.session_state.total_points += 15
            st.session_state.correct_answers += 1
        else:
            st.error(f"🍂 Falsch. Richtig wäre: {selected_q['correct']}")
        st.session_state.total_questions += 1

def show_criteria_quiz():
    st.title("🧠 Diagnostische Kriterien Quiz")
    st.markdown("*Erkenne die Zeichen wie ein Spurenleser im Wald*")
    
    # Hier würdest du detaillierte diagnostische Kriterien implementieren
    st.info("🚧 Dieser Bereich wird erweitert mit detaillierten DSM-5 und ICD-10 Kriterien!")
    
    # Beispiel für Kriterien-basierte Fragen
    st.markdown("### 🎯 Beispiel: Depression Kriterien")
    
    st.markdown("""
    **Hauptsymptome der Depression (ICD-10):**
    - Gedrückte, depressive Stimmung
    - Interessens- oder Freudeverlust
    - Antriebsmangel oder erhöhte Ermüdbarkeit
    
    **Zusatzsymptome:**
    - Verminderte Konzentration
    - Vermindertes Selbstwertgefühl
    - Schuldgefühle
    - Negative Zukunftsperspektiven
    - Suizidgedanken
    - Schlafstörungen
    - Verminderter Appetit
    """)
    
    if st.button("🎯 Kriterien-Quiz starten"):
        st.success("Quiz-Funktion wird implementiert! +5 Punkte für's Ausprobieren")
        st.session_state.total_points += 5

def show_prevention_rehab():
    st.title("🛡️ Prävention & Rehabilitation")
    st.markdown("*Hilf Menschen, ihren Weg aus dem dunklen Wald zu finden*")
    
    # Topic Selection
    topic = st.selectbox(
        "Wähle ein Thema:",
        list(praevention_reha.keys())
    )
    
    if topic:
        topic_data = praevention_reha[topic]
        
        st.markdown(f"## {topic_data['emoji']} {topic}")

    if topic == "Motivational Interviewing":
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🌿 Prinzipien")
            for prinzip in topic_data['prinzipien']:
                st.markdown(f"🍃 {prinzip}")

        with col2:
            st.markdown("### 🛠️ Techniken")
            for technik in topic_data['techniken']:
                st.markdown(f"🪵 {technik}")
    
        st.session_state.total_points += 5

    elif topic == "PACE-Modell":
        st.markdown("### 🌱 Bedeutung der Buchstaben:")
        for key, val in topic_data['bedeutung'].items():
            st.markdown(f"**{key}** – {val}")
        st.session_state.total_points += 5

    elif topic == "Entscheidungswaage":
        st.markdown("### ⚖️ Beschreibung:")
        st.markdown(topic_data['beschreibung'])
        st.markdown("### 📝 Anwendung:")
        st.markdown(topic_data['anwendung'])
        st.session_state.total_points += 5

    elif topic == "Universelle Prävention":
        st.markdown("### 🧍‍♂️ Zielgruppe:")
        st.markdown(topic_data['zielgruppe'])
        st.markdown("### 🧰 Beispiele:")
        for bsp in topic_data['beispiele']:
            st.markdown(f"🍃 {bsp}")
        st.session_state.total_points += 5

    elif topic == "Rehabilitation":
        st.markdown("### 🔁 Phasen:")
        for phase in topic_data['phasen']:
            st.markdown(f"🌿 {phase}")
        st.markdown("### 🎯 Ziele:")
        for ziel in topic_data['ziele']:
            st.markdown(f"🍃 {ziel}")
        st.session_state.total_points += 5

        st.success("🌳 Thema erkundet! +5 Punkte")

def show_progress():
    st.title("📊 Dein Lernfortschritt im Wald")
    st.markdown("*Hier kannst du deinen Weg durch den Wald nachvollziehen*")

    level, level_name = get_user_level()
    st.markdown(f"## Dein aktuelles Level: {level_name}")
    st.markdown(f"**Gesamtpunkte:** {st.session_state.total_points} 🍃")
    st.markdown(f"**Beantwortete Fragen:** {st.session_state.total_questions}")
    st.markdown(f"**Richtige Antworten:** {st.session_state.correct_answers}")

    if st.session_state.total_questions > 0:
        accuracy = (st.session_state.correct_answers / st.session_state.total_questions) * 100
        st.markdown(f"**Treffsicherheit:** {accuracy:.1f}%")

    # Visuelle Fortschrittsanzeige
    st.markdown("### 🌿 Fortschrittsbalken")
    st.progress(min(st.session_state.total_points / 1000, 1.0))

    st.markdown("### 🍂 Gelernte Inhalte")
    learned_modules = []
    if st.session_state.total_points > 10:
        learned_modules.append("📚 ICD-10 Quiz")
    if st.session_state.total_points > 20:
        learned_modules.append("🎭 Gedankenpalast")
    if st.session_state.total_points > 30:
        learned_modules.append("🧠 Kriterien-Quiz")
    if st.session_state.total_points > 40:
        learned_modules.append("🛡️ Präventionswissen")

    if learned_modules:
        for module in learned_modules:
            st.markdown(f"✅ {module}")
    else:
        st.info("Noch keine Module abgeschlossen – auf in den Lernwald!")

# Starte App
if __name__ == "__main__":
    main()
   

   
