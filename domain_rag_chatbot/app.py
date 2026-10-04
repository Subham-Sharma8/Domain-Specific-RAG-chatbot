import os
import streamlit as st
from dotenv import load_dotenv
from rag_pipeline import RAGPipeline

load_dotenv()

st.set_page_config(
    page_title="Domain-Specific RAG Chatbot",
    page_icon="📚",
    layout="wide",
)

@st.cache_resource(show_spinner=False)
def get_pipeline():
    return RAGPipeline()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pipeline_ready" not in st.session_state:
    st.session_state.pipeline_ready = False

pipeline = get_pipeline()

st.title("📚 Domain-Specific RAG Chatbot")
st.caption("Ask questions from uploaded PDF documents. Answers are grounded in retrieved document passages.")

with st.sidebar:
    st.header("Documents")
    uploaded_files = st.file_uploader(
        "Upload one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload documents that belong to the selected domain."
    )

    st.info("Recommended: 2–5 related documents for a domain-specific knowledge base.")

    if st.button("Process Documents", use_container_width=True, type="primary"):
        if not uploaded_files:
            st.warning("Please upload at least one PDF.")
        else:
            with st.spinner("Extracting, chunking, embedding and indexing documents..."):
                try:
                    result = pipeline.process_uploaded_files(uploaded_files)
                    st.session_state.pipeline_ready = True
                    st.session_state.messages = []
                    st.success(
                        f"Processed {result['documents']} document(s), "
                        f"{result['pages']} page(s), and {result['chunks']} chunk(s)."
                    )
                except Exception as exc:
                    st.error(f"Processing failed: {exc}")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []

    st.divider()
    st.subheader("System status")
    status = pipeline.status()
    st.write(f"**Indexed:** {'Yes' if status['ready'] else 'No'}")
    st.write(f"**Chunks:** {status['chunks']}")
    st.write(f"**Embedding model:** {pipeline.embedding_model_name}")
    st.write(f"**LLM:** {pipeline.llm_name}")

    st.divider()
    st.caption("For high-stakes information, verify the answer against the original document.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            st.markdown("**Sources**")
            for source in message["sources"]:
                st.write(
                    f"• {source['document']} — page {source['page']} "
                    f"(similarity: {source['score']:.3f})"
                )

if not st.session_state.pipeline_ready and not pipeline.status()["ready"]:
    st.info("Upload PDF documents in the sidebar and click **Process Documents** to begin.")

question = st.chat_input("Ask a question about the uploaded documents...")

if question:
    if not pipeline.status()["ready"]:
        st.warning("Please upload and process at least one PDF first.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving relevant passages and generating a grounded answer..."):
                try:
                    result = pipeline.ask(question)
                    st.markdown(result["answer"])
                    st.markdown("**Sources**")
                    for source in result["sources"]:
                        st.write(
                            f"• {source['document']} — page {source['page']} "
                            f"(similarity: {source['score']:.3f})"
                        )
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["sources"],
                    })
                except Exception as exc:
                    error_message = (
                        "The question could not be answered because the language-model "
                        f"request failed: {exc}"
                    )
                    st.error(error_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message,
                        "sources": [],
                    })
