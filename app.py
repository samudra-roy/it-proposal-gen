import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# 1️⃣ Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2️⃣ Initialize Gemini client
client = genai.Client(api_key=api_key)

# 3️⃣ Streamlit page setup
st.set_page_config(page_title="IT Project Proposal Generator", page_icon="💡", layout="wide")

# 🎨 Styling and Branding
st.markdown(
    """
    <style>
    .main-title {
        font-size: 32px;
        font-weight: 700;
        color: #2E86C1;
        text-align: center;
    }
    .subtitle {
        font-size: 18px;
        color: #7F8C8D;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">💼 IT Project Proposal Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Created by Samudra Roy | Powered by Google Gemini</div>', unsafe_allow_html=True)
st.divider()

# 🧠 Session state for persistence
if "proposal_text" not in st.session_state:
    st.session_state.proposal_text = ""

# 4️⃣ Sidebar Inputs
st.sidebar.header("🧠 Project Inputs")

client_name = st.sidebar.text_input("Client Name")
project_title = st.sidebar.text_input("Project Title")
problem_statement = st.sidebar.text_area("Problem Statement")

project_type = st.sidebar.selectbox(
    "Project Type",
    ["AI / ML", "Web App", "Cloud / DevOps", "Data Engineering", "Cybersecurity", "ERP / Business Automation"],
)

key_tech = st.sidebar.text_input("Key Technologies (comma separated)")
expected_outcome = st.sidebar.text_area("Expected Outcomes")
duration = st.sidebar.text_input("Duration or Budget")

tone = st.sidebar.radio(
    "Tone of Proposal",
    ["Formal Corporate", "Innovative Startup", "Technical Deep-Dive", "Simple & Client Friendly"],
    index=0,
)

# ✨ Helper: Create well-formatted PDF (manual only)
def create_pdf(text, client_name, project_title):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom Styles
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    subheading_style = ParagraphStyle(
        "SubHeading",
        parent=styles["Heading2"],
        textColor="#2E86C1",
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        leading=14,
        spaceAfter=8,
    )

    story = []

    # Add Title Section
    story.append(Paragraph(f"Project Proposal for {client_name or 'Client'}", heading_style))
    story.append(Paragraph(f"<b>Title:</b> {project_title or 'Untitled Project'}", subheading_style))
    story.append(Spacer(1, 12))

    # Add Content
    for line in text.split("\n"):
        if not line.strip():
            continue
        if line.lower().startswith("##"):
            story.append(Paragraph(line.replace("##", "").strip(), subheading_style))
        else:
            story.append(Paragraph(line.strip(), body_style))
        story.append(Spacer(1, 8))

    doc.build(story)
    buffer.seek(0)
    return buffer


# 5️⃣ Generate Proposal Button
if st.button("🚀 Generate Proposal"):
    with st.spinner("Generating your proposal... ✨"):
        prompt = f"""
        You are a professional IT business proposal writer for the Indian IT industry.

        Client: {client_name or 'Confidential Client'}
        Project Title: {project_title or 'Untitled Project'}
        Project Type: {project_type}
        Problem: {problem_statement or 'Describe the client problem clearly.'}
        Key Technologies: {key_tech or 'AI, Python, Cloud'}
        Expected Outcomes: {expected_outcome or 'Efficiency improvement, automation, cost savings.'}
        Duration/Budget: {duration or '3 months / ₹10 Lakhs'}
        Tone: {tone}

        Write a structured, polished, and realistic proposal including:
        1. Executive Summary
        2. Problem Statement
        3. Proposed Solution (customized for {project_type})
        4. Technical Approach
        5. Expected Outcomes
        6. Implementation Plan (timeline & budget)
        7. Why Choose Us (for Indian IT industry context)

        Make sure tone and writing style reflect: {tone}.
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        st.session_state.proposal_text = response.text.strip()
        st.success("✅ Proposal Generated Successfully!")

# 6️⃣ Display and Download
if st.session_state.proposal_text:
    st.divider()
    st.subheader("📜 Generated Proposal:")
    st.markdown(st.session_state.proposal_text)
    st.info("You can now export your proposal as a professional PDF below 👇")

    # Only prepare + show download when clicked
    if st.button("📄 Prepare PDF for Download"):
        pdf_buffer = create_pdf(st.session_state.proposal_text, client_name, project_title)
        st.download_button(
            label="⬇️ Download Proposal as PDF",
            data=pdf_buffer,
            file_name=f"{project_title or 'proposal'}.pdf",
            mime="application/pdf"
        )
