import os
import streamlit as st

from dotenv import load_dotenv

from utils.transcript import (
    get_video_transcript
)

from utils.chunking import (
    split_transcript
)

from utils.embeddings import (
    load_embedding_model
)

from utils.vectorstore import (
    create_vector_store
)

from utils.rag_chain import (
    create_rag_chain
)


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="YouTube RAG Chatbot",
    page_icon="🎥",
    layout="wide"
)

st.title(
    "🎥 YouTube Video RAG Chatbot"
)

st.markdown(
    """
Chat with YouTube videos using
Gemini AI + RAG.
"""
)


# =========================
# LOAD ENV
# =========================

load_dotenv()


# =========================
# SIDEBAR
# =========================

st.sidebar.title("⚙ Settings")

GOOGLE_API_KEY = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password"
)

if GOOGLE_API_KEY:

    os.environ[
        "GOOGLE_API_KEY"
    ] = GOOGLE_API_KEY


# =========================
# SESSION STATE
# =========================

if "qa_chain" not in st.session_state:

    st.session_state.qa_chain = None

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# =========================
# INPUT
# =========================

video_url = st.text_input(
    "Enter YouTube Video URL"
)


# =========================
# PROCESS VIDEO
# =========================

if st.button("Process Video"):

    if not GOOGLE_API_KEY:

        st.warning(
            "Please enter Gemini API Key"
        )

    elif not video_url:

        st.warning(
            "Please enter YouTube URL"
        )

    else:

        try:

            with st.spinner(
                "Processing video..."
            ):

                # GET TRANSCRIPT
                transcript = (
                    get_video_transcript(
                        video_url
                    )
                )

                # SPLIT
                documents = (
                    split_transcript(
                        transcript
                    )
                )

                # EMBEDDINGS
                embedding_model = (
                    load_embedding_model()
                )

                # VECTOR STORE
                vector_store = (
                    create_vector_store(
                        documents,
                        embedding_model
                    )
                )

                # RETRIEVER
                retriever = (
                    vector_store.as_retriever(
                        search_type="mmr",
                        search_kwargs={
                            "k": 4
                        }
                    )
                )

                # QA CHAIN
                qa_chain = (
                    create_rag_chain(
                        retriever
                    )
                )

                st.session_state.qa_chain = (
                    qa_chain
                )

                st.success(
                    "Video processed successfully!"
                )

        except Exception as e:

            st.error(str(e))


# =========================
# DISPLAY CHAT HISTORY
# =========================

for role, message in (
    st.session_state.chat_history
):

    with st.chat_message(role):

        st.markdown(message)


# =========================
# CHAT INPUT
# =========================

query = st.chat_input(
    "Ask questions about the video..."
)


# =========================
# GENERATE RESPONSE
# =========================

if query and st.session_state.qa_chain:

    with st.chat_message("user"):

        st.markdown(query)

    try:

        with st.spinner(
            "Generating response..."
        ):

            response = (
                st.session_state.qa_chain.invoke(
                    {"question": query}
                )
            )

            answer = response["answer"]

            source_docs = response[
                "source_documents"
            ]

        with st.chat_message(
            "assistant"
        ):

            st.markdown(answer)

            with st.expander(
                "📚 Source Chunks"
            ):

                for i, doc in enumerate(
                    source_docs
                ):

                    st.markdown(
                        f"### Chunk {i+1}"
                    )

                    st.write(
                        doc.page_content[:500]
                        + "..."
                    )

        st.session_state.chat_history.append(
            ("user", query)
        )

        st.session_state.chat_history.append(
            ("assistant", answer)
        )

    except Exception as e:

        st.error(str(e))
