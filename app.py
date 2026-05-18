import os
import streamlit as st

from dotenv import load_dotenv

from utils.transcript import (
    get_video_transcript,
    get_thumbnail_url,
    extract_video_title
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

from utils.reranker import (
    rerank_documents
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
    "🎥 Advanced YouTube RAG Chatbot"
)

st.markdown(
    """
Chat with YouTube videos using
Gemini AI + Advanced RAG.
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

if "transcript_text" not in st.session_state:

    st.session_state.transcript_text = ""


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

                # TITLE
                video_title = (
                    extract_video_title(
                        video_url
                    )
                )

                # THUMBNAIL
                thumbnail = (
                    get_thumbnail_url(
                        video_url
                    )
                )

                col1, col2 = st.columns(
                    [1, 2]
                )
                
                with col1:
                
                    st.image(
                        thumbnail,
                        use_container_width=True
                    )
                
                with col2:
                
                    st.subheader(
                        video_title
                    )
                
                    st.success(
                        "Video metadata extracted successfully."
                    )
                
                # TRANSCRIPT
                transcript_data = (
                    get_video_transcript(
                        video_url
                    )
                )

                transcript_text = " ".join(
                    [
                        item["text"]
                        for item
                        in transcript_data
                    ]
                )

                st.session_state.transcript_text = (
                    transcript_text
                )

                # CHUNKING
                documents = (
                    split_transcript(
                        transcript_data,
                        video_title
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
                            "k": 8
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

            st.error(
                    """
                Could not fetch transcript.
                
                Possible reasons:
                - Transcript disabled
                - No captions available
                - Private/restricted video
                - Invalid URL
                """
                )



# =========================
# DOWNLOAD TRANSCRIPT
# =========================

if st.session_state.transcript_text:

    st.download_button(
        label="📥 Download Transcript",
        data=st.session_state.transcript_text,
        file_name="transcript.txt",
        mime="text/plain"
    )


# =========================
# CHAT HISTORY
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
    "Ask questions about videos..."
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

            # RERANK
            reranked_docs = (
                rerank_documents(
                    query,
                    source_docs
                )
            )

        with st.chat_message(
            "assistant"
        ):

            st.write_stream(
                iter([answer])
            )

            with st.expander(
                "📚 Source Citations"
            ):

                for i, doc in enumerate(
                    reranked_docs[:4]
                ):

                    timestamp = int(
                        doc.metadata[
                            "timestamp"
                        ]
                    )

                    minutes = (
                        timestamp // 60
                    )

                    seconds = (
                        timestamp % 60
                    )

                    st.markdown(
                        f"""
### Citation {i+1}

🎥 Video:
{doc.metadata['video_title']}

⏱ Timestamp:
{minutes}:{seconds:02d}
"""
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

        
