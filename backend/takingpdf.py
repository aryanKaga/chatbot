import os
from glob import glob
from langchain_community.document_loaders import (
    UnstructuredWordDocumentLoader,
    UnstructuredPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import spacy
from langchain.text_splitter import SpacyTextSplitter


def load_document_by_type(filepath):
    ext = filepath.lower().split(".")[-1]
    if ext == "docx":
        return UnstructuredWordDocumentLoader(filepath).load()
    elif ext == "pdf":
        return UnstructuredPDFLoader(filepath).load()
    elif ext == "txt":
        return TextLoader(filepath).load()
    elif ext == "md":
        return UnstructuredMarkdownLoader(filepath).load()
    else:
        print(f"⚠️ Skipping unsupported file: {filepath}")
        return []

def add_all_files_to_vectorstore(folder_path: str = "./data", persist_dir: str = "rag_db"):
    supported_extensions = ("*.docx", "*.pdf", "*.txt", "*.md")
    all_documents = []

    # Collect all supported files
    all_files = []
    for ext in supported_extensions:
        all_files.extend(glob(os.path.join(folder_path, ext)))

    if not all_files:
        print("❌ No supported files found in folder.")
        return

    for filepath in all_files:
        print(f"📄 Loading {os.path.basename(filepath)}")
        docs = load_document_by_type(filepath)
        all_documents.extend(docs)

    # Split text
    text_splitter=SpacyTextSplitter(pipeline="en_core_web_sm")
    split_docs = text_splitter.split_documents(all_documents)

    # Embeddings
    embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en",
        encode_kwargs={"normalize_embeddings": True}
    )

    # FAISS vector store
    faiss_index = FAISS.from_documents(split_docs, embedding_model)

    # Save
    faiss_index.save_local(persist_dir)

    print(f"✅ Embedded and saved {len(all_files)} file(s) to vector store at '{persist_dir}'!")

# Run this
if __name__ == "__main__":
    add_all_files_to_vectorstore("./data", "rag_db")
