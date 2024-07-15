import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from .config import *

class RagPipeline:
    def __init__(self):
        # setting environment variables
        load_dotenv()
        os.environ["HUGGINFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    def rag_pipeline(self, query, prompt=None, rag_query=None):

        # laoading model
        llm = HuggingFaceEndpoint(repo_id=mistral_repo, temperature=0.7, max_length=128)

        if rag_query:
            # creating embeddings 
            hf_embedding = HuggingFaceEmbeddings()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            documents = text_splitter.split_text(text)

            # storing into vector db and creting retriever
            chroma_db = Chroma.from_documents(documents, hf_embedding, persist_directory="vecotr_db")
            retriever = chroma_db.as_retriever(search_type="similarity", search_kwargs={"k": top_k})

            prompt = hub.pull("rlm/rag-prompt")
           
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            # creating retrieval chain
            rag_chain = ({
                "context": retriever | format_docs,
                "question": RunnablePassthrough()} 
                | prompt | llm | StrOutputParser()
            )

            response = rag_chain.invoke(query)

        
        else:
            response = llm.invoke(query)
        
        return response