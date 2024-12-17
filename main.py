import os
import io
import base64
import streamlit as st
from PIL import Image
import openai

def init_styling():
    st.markdown("""
        <style>
        .main {
            background-color: #0e1117;
        }
        .stApp {
            max-width: 100%;
            margin: 0 auto;
            padding: 0 20px;
        }
        .title-gradient {
            background: linear-gradient(90deg, #00F5FF, #00C4FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 1rem;
            letter-spacing: -0.5px;
        }
        .subtitle-gradient {
            background: linear-gradient(90deg, #00C4FF, #00A3E0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        .cards-scroll-container {
            overflow-x: auto;
            padding: 20px 0;
            margin: 20px -20px;
            -webkit-overflow-scrolling: touch;
        }
        .card-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            padding: 0 20px;
            min-width: min-content;
            margin: 0 auto;
            flex-wrap: wrap;
        }
        .card {
            background: linear-gradient(145deg, rgba(20, 20, 30, 0.9), rgba(30, 30, 45, 0.9));
            border: 1px solid rgba(123, 66, 246, 0.1);
            border-radius: 20px;
            padding: 25px;
            flex: 1 1 280px;
            max-width: 300px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(123, 66, 246, 0.2);
        }
        .card-title {
            background: linear-gradient(90deg, #00F5FF, #7B42F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        }
        .card-description {
            color: #E0E0E0;
            font-size: 1.1rem;
            line-height: 1.5;
            text-align: center;
        }
        .stTextInput > div > div {
            background-color: rgba(20, 20, 30, 0.9);
            border: 1px solid rgba(123, 66, 246, 0.3);
            border-radius: 10px;
            color: #FFFFFF;
        }
        .footer-gradient {
            background: linear-gradient(90deg, #00F5FF, #7B42F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-top: 2rem;
        }
        @media (max-width: 768px) {
            .card {
                min-width: 260px;
                padding: 20px;
            }
            .title-gradient {
                font-size: 2rem;
            }
            .subtitle-gradient {
                font-size: 1.2rem;
            }
            .card-title {
                font-size: 1.2rem;
            }
            .card-description {
                font-size: 1rem;
            }
        }
        ::-webkit-scrollbar {
            height: 8px;
            background: #0e1117;
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(90deg, #00F5FF, #7B42F6);
            border-radius: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("<div class='title-gradient'>AI Jewellery Analyzer</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle-gradient'>Revolutionizing Jewellery Analysis with Advanced AI</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.text_input(
                "Enter passcode", 
                type="password", 
                key="password",
                on_change=lambda: st.session_state.update(
                    password_correct=st.session_state["password"] == "1111"
                )
            )

        st.markdown("""
            <div class='cards-scroll-container'>
                <div class='card-container'>
                    <div class='card'>
                        <div class='card-title'>Smart Metadata Generation</div>
                        <div class='card-description'>Transform your inventory with AI-powered detailed metadata generation for each jewellery piece.</div>
                    </div>
                    <div class='card'>
                        <div class='card-title'>Intelligent Cataloging</div>
                        <div class='card-description'>Revolutionize inventory management with real-time AI identification and classification.</div>
                    </div>
                    <div class='card'>
                        <div class='card-title'>Duplicate Detection</div>
                        <div class='card-description'>Maintain data integrity with advanced AI image matching and pattern recognition.</div>
                    </div>
                    <div class='card'>
                        <div class='card-title'>Enterprise Data Lake</div>
                        <div class='card-description'>Create a unified digital ecosystem with AI-driven tagging and smart analytics.</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<div class='footer-gradient'>© 2024 Kalyan Jewellers - Trust of Generations - AI Research Wing</div>", unsafe_allow_html=True)
        return False
    return st.session_state["password_correct"]

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def analyze_jewellery(image_file):
    base64_image = encode_image(image_file)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are Kalyan AI, an expert jewellery analysis system for Kalyan Jewellers.
                Analyze the jewellery and provide details in the following structure:

                ## Market Classification
                • Target Customer Segment
                • Event/Occasion Suitability
                • Regional Style (South Indian/North Indian/Western/Fusion)

                ## Product Details
                • Jewellery Category
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
                        "text": "Analyze this jewellery piece for Kalyan Jewellers inventory."
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
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='title-gradient'>AI Jewellery Analyzer</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle-gradient'>Transform Inventory Analysis</div>", unsafe_allow_html=True)

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("### Image Input")
        tab1, tab2 = st.tabs(["📸 Camera", "📤 Upload"])
        
        with tab1:
            camera_image = st.camera_input("Capture Jewellery")
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
                analysis = analyze_jewellery(image_file)
                st.markdown(analysis)

    st.markdown("---")
    st.markdown("<div class='footer-gradient'>© 2024 Kalyan Jewellers - Trust of Generations - AI Research Wing</div>", unsafe_allow_html=True)

# Initialize the app
st.set_page_config(layout="wide", page_title="Kalyan Jewellers AI Analyzer")
init_styling()

key = os.environ.get('OPENAI_API_KEY')
client = openai.OpenAI(api_key=str(key))

if not check_password():
    st.stop()
elif __name__ == "__main__":
    main()
