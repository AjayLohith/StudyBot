import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# ------------------------------------
# Load Environment Variables
# ------------------------------------
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# ------------------------------------
# Streamlit Config
# ------------------------------------
st.set_page_config(page_title="StudyBot")

st.title("StudyBot")

if not google_api_key:
    st.error("GOOGLE_API_KEY not found")
    st.stop()

st.success("Google API Key Loaded Successfully")

# ------------------------------------
# Session State
# ------------------------------------
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

# ------------------------------------
# Sidebar
# ------------------------------------
with st.sidebar:
    st.header("Upload Notes")

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type="pdf"
    )

# ------------------------------------
# Process PDF
# ------------------------------------
if uploaded_file is not None and not st.session_state.pdf_uploaded:

    st.info("Processing PDF...")

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    if not text.strip():
        st.error("No readable text found.")
        st.stop()

    st.subheader("Extracted Text")

    st.text_area(
        "PDF Content",
        text,
        height=250
    )

    # ------------------------------------
    # Split Text
    # ------------------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    st.session_state.chunks = chunks

    st.write(f"Total Chunks : {len(chunks)}")

    # ------------------------------------
    # Embeddings
    # ------------------------------------
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=google_api_key
    )

    try:
        vector = embeddings.embed_query("Hello")

        st.write(f"Embedding Dimension : {len(vector)}")

    except Exception as e:
        st.exception(e)
        st.stop()

    # ------------------------------------
    # Create Vector Store
    # ------------------------------------
    try:

        vector_store = FAISS.from_texts(
            texts=chunks,
            embedding=embeddings
        )

        st.session_state.vector_store = vector_store
        st.session_state.pdf_uploaded = True

        st.success("Vector Store Created Successfully")

    except Exception as e:
        st.exception(e)
        st.stop()

# ------------------------------------
# Ask Questions
# ------------------------------------
if st.session_state.vector_store is not None:

    user_query = st.text_input("Ask a question about your PDF")

    if user_query:

        docs = st.session_state.vector_store.similarity_search(
            user_query,
            k=3
        )

        llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=google_api_key,
            temperature=0
        )

        prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful study assistant.

            Answer the question only using the provided context.

            Context:{context}

            Question:{question}
            """
        )

        chain = create_stuff_documents_chain(
            llm=llm,
            prompt=prompt
        )

        with st.spinner("Generating answer..."):

            try:

                # ----------------------------
                # New LangChain API
                # ----------------------------
                response = chain.invoke(
                    {
                        "context": docs,
                        "question": user_query
                    }
                )

                st.subheader("Answer")

                st.write(response)

                # ----------------------------
                # Old Deprecated API
                # ----------------------------

                # chain = load_qa_chain(
                #     llm,
                #     chain_type="stuff"
                # )

                # answer = chain.run(
                #     input_documents=docs,
                #     question=user_query
                # )

                # st.write(answer)

            except Exception as e:
                st.exception(e)

# ------------------------------------
# Reset
# ------------------------------------
st.divider()

if st.button("Upload New PDF"):

    st.session_state.vector_store = None
    st.session_state.chunks = None
    st.session_state.pdf_uploaded = False

    st.rerun()