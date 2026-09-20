import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

HERE = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.join(HERE, "data", "knowledge_base")
INDEX_DIR = os.path.join(HERE, "vectorstore", "faiss_index")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# split on markdown headers first so e.g. the whole "Fertilizer" section stays
# together, then size-split anything that's still too long
HEADERS_TO_SPLIT_ON = [("##", "section")]


def load_and_chunk():
    loader = DirectoryLoader(KB_DIR, glob="*.md", loader_cls=TextLoader)
    raw_docs = loader.load()

    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)
    size_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)

    chunks = []
    for doc in raw_docs:
        crop_name = os.path.basename(doc.metadata.get("source", "")).replace(".md", "")
        sections = header_splitter.split_text(doc.page_content)
        for section in sections:
            section.metadata["crop"] = crop_name
            sub_chunks = size_splitter.split_documents([section])
            chunks.extend(sub_chunks)

    print(f"Loaded {len(raw_docs)} documents -> {len(chunks)} chunks")
    return chunks


def main():
    chunks = load_and_chunk()

    print(f"Loading embedding model: {EMBEDDING_MODEL} (first run downloads ~90MB, cached after)")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(os.path.dirname(INDEX_DIR), exist_ok=True)
    vectorstore.save_local(INDEX_DIR)
    print(f"Saved FAISS index to {INDEX_DIR}")


if __name__ == "__main__":
    main()
