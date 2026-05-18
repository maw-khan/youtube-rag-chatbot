from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain.docstore.document import (
    Document
)


def split_transcript(text):

    document = Document(
        page_content=text
    )

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    )

    chunks = splitter.split_documents(
        [document]
    )

    return chunks
