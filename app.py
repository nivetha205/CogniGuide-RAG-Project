from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from cogniguide_core import CogniGuideCore
import tempfile
import os

# --- 1. CUSTOM CSS FOR CLEAN, PROFESSIONAL LOOK ---
def inject_css():
    st.markdown(
        """
        <style>
        /* Global Styles: Clean, default white background */
        .stApp {
            font-family: 'Arial', sans-serif;
        }
        
        /* Main Title Styling: Professional and bold */
        h1 {
            color: #1E90FF; /* Dodger Blue */
            font-size: 2.5rem;
            font-weight: 700;
            border-bottom: 3px solid #1E90FF;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        
        /* Subheaders (Your Study Guide) */
        h2 {
            color: #333333;
            font-size: 1.8rem;
            font-weight: 600;
            margin-top: 30px;
        }
        
        /* Primary Button: Clean, modern blue */
        .stButton>button {
            background-color: #1E90FF; /* Dodger Blue */
            color: white;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #0077CC; /* Darker Blue on hover */
        }
        
        /* Floating Card Style for Output: Clean white card with shadow */
        .stMarkdown {
            background-color: #F8F8F8; /* Light Gray background for contrast */
            border: 1px solid #DDDDDD;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Soft shadow */
            margin-top: 20px;
        }
        
        /* Sidebar Styling */
        .css-1d391kg, .css-1lcbmhc {
            background-color: #F0F2F6; /* Light gray sidebar */
        }
        
        /* Custom Profile Box in Sidebar */
        .profile-box {
            border: 1px solid #1E90FF;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
            background-color: #FFFFFF;
        }
        .profile-box h4 {
            color: #1E90FF;
            margin-top: 0;
            margin-bottom: 5px;
            font-size: 1.1rem;
        }
        .profile-box p {
            font-size: 0.9rem;
            color: #555555;
            margin: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- 2. INJECT CSS AND START APP ---
inject_css()

st.title("CogniGuide: AI-Powered Study Guide Generator")

# --- 3. ADD PROFILE BOX TO SIDEBAR ---
st.sidebar.markdown(
    """
    <div class="profile-box">
        <h4>Profile: Nivetha</h4>
        <p>nivethashankar99@gmail.com</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 4. SIDEBAR SETTINGS ---
st.sidebar.header("⚙️ Personalization Settings")

learning_level = st.sidebar.selectbox("Learning Level", ["Beginner", "Intermediate", "Advanced"])
learning_style = st.sidebar.selectbox("Learning Style", ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"])
tone = st.sidebar.selectbox("Tone", ["Formal", "Casual", "Conversational"])
output_format = st.sidebar.selectbox("Output Format", ["Flashcards", "Summary", "Quiz"])

# --- 5. MAIN CONTENT ---
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_path = tmp_file.name

    st.success("PDF uploaded successfully! Now, ask your question and generate your guide.")

    user_query = st.text_input(
        "What topic from the PDF would you like to focus on?",
        placeholder="e.g., Explain the Transformer architecture"
    )

    if st.button("Generate Study Guide", type="primary"):
        if not user_query:
            st.error("Please enter a topic to focus on.")
        else:
            with st.spinner("Generating your study guide... This may take a moment."):
                try:
                    # Initialize CogniGuide
                    cogniguide = CogniGuideCore(tmp_path)

                    user_profile = {
                        'learning_level': learning_level.lower(),
                        'learning_style': learning_style.lower(),
                        'tone': tone.lower()
                    }

                    study_guide = cogniguide.generate_study_guide(
                        user_query,
                        user_profile,
                        output_format.lower()
                    )

                    # Display result with the new styling
                    st.subheader(f"📚 Your Personalized {output_format}")
                    st.markdown(study_guide)

                    st.download_button(
                        label="Download as Text",
                        data=study_guide,
                        file_name=f"cogniguide_{output_format.lower()}.txt",
                        mime="text/plain"
                    )

                except ValueError as ve:
                    st.error(f"Configuration Error: {ve}. Please check your .env file.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

    # Cleanup
    os.unlink(tmp_path)

