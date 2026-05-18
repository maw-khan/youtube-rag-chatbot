from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain.docstore.document import (
    Document
)


def split_transcript(
    transcript_data,
    video_title
):

    full_text = ""

    timestamps = []

    for item in transcript_data:

        full_text += item["text"] + " "

        timestamps.append(
            item["start"]
        )

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    )

    chunks = splitter.split_text(
        full_text
    )

    documents = []

    for i, chunk in enumerate(chunks):

        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "video_title": video_title,
                    "chunk_id": i + 1,
                    "timestamp": (
                        timestamps[
                            min(
                                i,
                                len(timestamps)-1
                            )
                        ]
                    )
                }
            )
        )

    return documents
