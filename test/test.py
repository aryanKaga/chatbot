from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import SpacyTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

textloader=TextLoader(file_path='general.txt')

document=textloader.load()

textsplitter=SpacyTextSplitter(pipeline='en_core_web_sm')

documents=[document]

splitdocs=textsplitter.split_documents(document)

embedding= embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en",
        encode_kwargs={"normalize_embeddings": True}
    )

faiss_index=FAISS.from_documents(splitdocs,embedding=embedding)

query="whats the curriculum"
query_embedding=embedding.embed_query(query)
similar_docs_with_scores = faiss_index.similarity_search_with_score_by_vector(query_embedding, k=1)

for doc, score in similar_docs_with_scores:
    print("🔹 Document:", doc.page_content)
    print("🔸 L2 Distance Score:", score)
    print("🔸 Cosine Similarity (approx):", 1 - (score ** 2) / 2)
