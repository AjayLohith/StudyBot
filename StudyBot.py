import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load Environment Variables
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# Streamlit UI
st.set_page_config(page_title="StudyBot", page_icon="📚")

st.header("📚 StudyBot")

# Test API Key
if google_api_key:
    st.success(" Google API Key Loaded Successfully")
else:
    st.error(" GOOGLE_API_KEY not found in .env")
    st.stop()

# Sidebar
with st.sidebar:
    st.title("My Notes")
    file = st.file_uploader(
        "Upload your PDF",
        type="pdf"
    )

# Process PDF
if file is not None:

    # Read PDF
    pdf_reader = PdfReader(file)

    text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    st.subheader("Extracted Text")
    st.text_area(
        "PDF Content",
        text,
        height=500
    )

    # Split Text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    st.subheader("Chunks")

    st.write(f"Total Chunks: {len(chunks)}")

    with st.expander("View Chunks"):
        st.write(chunks)

    # Embedding Model
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=google_api_key
    )


    # Test Embedding

    try:
        vector = embeddings.embed_query("Hello StudyBot")

        st.success(" Embedding Model Working Successfully!")

        st.write("Embedding Dimension:", len(vector))

    except Exception as e:
        st.error(f"Embedding Error:\n{e}")


    # Vector Storing
    try:
        vector_store = FAISS.from_texts(chunks, embeddings)
        st.success(" Vector Store Created Successfully!")

    except Exception as e:
        st.error(f"FAISS Error:\n{e}")