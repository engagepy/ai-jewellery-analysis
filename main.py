import os
import io
import base64
import streamlit as st
from PIL import Image
import openai

def check_password():
    if "password_correct" not in st.session_state:
        st.text_input(
            "Enter passcode", 
            type="password", 
            key="password",
            on_change=lambda: st.session_state.update(
                password_correct=st.session_state["password"] == "1111"
            )
        )
        return False
    return st.session_state["password_correct"]

if not check_password():
    st.stop()

# Configure page layout
st.set_page_config(layout="wide", page_title="Kalyan Jewellers AI Analyzer")

# Custom CSS for futuristic UI
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .css-1d391kg {
        padding: 1rem;
        border-radius: 15px;
        background: rgba(255,255,255,0.05);
    }
    .stButton>button {
        background-color: #D4AF37;
        color: white;
        border-radius: 25px;
    }
    .upload-section, .analysis-section {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 15px;
        margin: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

key = os.environ.get('OPENAI_API_KEY')

client = openai.OpenAI(api_key=str(key)) 

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def analyze_jewelry(image_file):
    base64_image = encode_image(image_file)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are Kalyan AI, an expert jewelry analysis system for Kalyan Jewellers.
                Analyze the jewelry and provide details in the following structure:

                ## Market Classification
                • Target Customer Segment
                • Event/Occasion Suitability
                • Regional Style (South Indian/North Indian/Western/Fusion)

                ## Product Details
                • Jewelry Category
                • Primary Materials
                • Stone Details (if present)
                • Design Elements
                • Craftsmanship Techniques

                ## Value Assessment
                | Material Type | Purity | Estimated Price Range (INR) | Quality Indicators |
                |--------------|---------|---------------------------|-------------------|
                | Gold         | 22K     | ₹XX,XXX - ₹XX,XXX        | [Indicators]     |
                | Gold         | 18K     | ₹XX,XXX - ₹XX,XXX        | [Indicators]     |

                ## Business Insights
                • Unique Selling Points
                • Collection Placement
                • Market Differentiation
                • Competition Analysis"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this jewelry piece for Kalyan Jewellers inventory."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )

    return response.choices[0].message.content

def main():
    # Header
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🏆 AI Jewelry Analyzer")
        st.markdown("*Transforming Jewelry Analysis with AI*")

    # Main content in two columns
    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("### Image Input")
        tab1, tab2 = st.tabs(["📸 Camera", "📤 Upload"])
        
        with tab1:
            camera_image = st.camera_input("Capture Jewelry")
            if camera_image:
                image_file = camera_image
                
        with tab2:
            uploaded_file = st.file_uploader("Choose image", type=["jpg", "jpeg", "png"])
            if uploaded_file:
                image_file = uploaded_file

        if 'image_file' in locals():
            image = Image.open(image_file)
            st.image(image, use_container_width=True)

    with right_col:
        st.markdown("### Analysis Results")
        if 'image_file' in locals():
            with st.spinner("🔍 Analyzing with Kalyan AI..."):
                image_file.seek(0)
                analysis = analyze_jewelry(image_file)
                st.markdown(analysis)

    # Footer
    st.markdown("---")
    st.markdown("*© 2024 Kalyan Jewellers - Trust of Generations - AI Research Wing*")

if __name__ == "__main__":
    main()
