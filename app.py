import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="🤖 Debu Expert Bot", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #0a0a0f; color: #f1f5f9; }
    </style>
""", unsafe_allow_html=True)

# Session State
if "brain_data" not in st.session_state:
    st.session_state.brain_data = ""

# Sidebar
with st.sidebar:
    st.title("🧠 Debu Expert Brain")
    brain = st.text_area("Apna Knowledge Base yahan paste karo:", value=st.session_state.brain_data, height=350)
    if st.button("💾 Save Brain"):
        st.session_state.brain_data = brain
        st.success("✅ Brain Save Ho Gaya!")

# Main Screen
st.title("🤖 Debu Expert Chat Bot")
api_key = st.text_input("Gemini API Key", type="password")
question = st.text_area("Apna Sawal Likho:")

# Logic
if st.button("🚀 Get Answer"):
    if not api_key:
        st.error("❌ API Key daaliye.")
    elif not st.session_state.brain_data:
        st.error("❌ Pehle Sidebar mein Brain Save kijiye.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
            Tum ek Expert Financial Analyst ho.
            BRAIN DATA: {st.session_state.brain_data}
            USER QUESTION: {question}
            
            STRICT RULES:
            1. Sirf BRAIN DATA aur LIVE DATA ka hi use karo.
            2. Khud se koi bhi prediction, number ya balance mat banao.
            3. Agar data available nahi hai, to seedha bolo: "Data Available Nahi Hai."
            4. Apni taraf se koi guessing mat karo, poori research karke jawab do.
            5. Jawab ke ant mein 'Data Source: Brain/Live Data' zaroor likho.
            """
            
            with st.spinner("🤖 Researching & Analyzing..."):
                response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"❌ Error: {e}")
