from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import SpacyTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

textloader=TextLoader(file_path='./data/general.txt')

document=textloader.load()

textsplitter=SpacyTextSplitter(pipeline='en_core_web_sm')

documents=[document]

splitdocs=textsplitter.split_documents(document)

embedding= embedding_model = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en",
        encode_kwargs={"normalize_embeddings": True}
    )

faiss_index=FAISS.from_documents(splitdocs,embedding=embedding)





def check_similarity(query:str):
    query_embedding=embedding.embed_query(query)
    similar_docs_with_scores = faiss_index.similarity_search_with_score_by_vector(query_embedding, k=1)

    for doc, score in similar_docs_with_scores:
        print(doc.page_content)
        print(score)
        cosine_similarity=1 - (score ** 2) / 2

        if(cosine_similarity>0.925):
            return True

        
    return False
