import os
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings,ChatCohere
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_pinecone.vectorstores import PineconeVectorStore
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document
from pinecone import Pinecone
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import TextLoader
from utils import pdf_to_text,get_papers_from_query,get_pdf_to_text,get_template,check_index,extract_pdf_links
from langchain.globals import set_verbose
import time
set_verbose(True) 

class RAG_Chain:
    def __init__(self,option="default"):
        # Load environment variables
        load_dotenv()
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        os.environ['COHERE_API_KEY']  = os.getenv("COHERE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        
        # Initialize embeddings and vector store
        self.embeddings = CohereEmbeddings(model="embed-english-v3.0")
        pc = Pinecone(api_key=self.pinecone_api_key)
        # checking if the index exists or not
        Indexs=check_index(pc)
        if self.index_name not in Indexs:
            pc.create_index(name=self.index_name,dimension=1024)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.index = pc.Index(self.index_name)
        self.vectorstore = PineconeVectorStore(index = self.index, pinecone_api_key = self.pinecone_api_key,embedding = self.embeddings)

        self.update_vectorstore_with_files()
        # Initialize LLM and components for RAG chain 
        # model is chosen cause of high context 
        self.llm = ChatCohere(model='command-r')
        self.reranker = CohereRerank(model='rerank-english-v3.0')
        self.change_template(option)
        
        
    def update_vectorstore_with_files(self,file=None):
        """Update the vector store with the PDFs uploaded by the user"""
        if file:
            text = pdf_to_text(file=file)
            text_chunks = self.text_splitter.split_text(text)
            documents = [Document(page_content=chunk) for chunk in text_chunks]
            if not documents:
                return
            self.vectorstore.add_documents(documents=documents)
        else:
            # added this part as it is scalable to be able to connect to your device it will get all the files
            # and upload them in the vectorstore so they can be retrieved when a query related to them is asked!
            if self.folder_path==None:
                return
            text_loader_kwargs = {"autodetect_encoding": True}
            loader = DirectoryLoader(path = self.folder_path,loader_cls=TextLoader,loader_kwargs=text_loader_kwargs)
            directory = loader.load()
            documents = []
            for file in directory:
                file_path = file.metadata.get('source')
                text=pdf_to_text(file_path=file_path)
                splits = self.text_splitter.split_text(text)  # Splits text into chunks
                text_chunks = [Document(page_content=chunk) for chunk in splits]
                documents.extend(text_chunks)
                
            self.vectorstore.add_documents(documents=documents)

    def update_vector_store_with_research_papers(self,query):
        """updating the vectorstore with the research papers we get"""
        source,papers = get_papers_from_query(query)
        papers_with_pdf = extract_pdf_links(papers)
        documents = []
        for paper in papers_with_pdf:
            if len(documents) >100:
                continue
            link = paper['link']
            text=get_pdf_to_text(pdf_url=link,source=source)
            if text is not None:
                splits = self.text_splitter.split_text(text)
                text_chunks = [Document(page_content=chunk) for chunk in splits]
                documents.extend(text_chunks)
        self.vectorstore.add_documents(documents=documents)
        return papers_with_pdf
    
    def update_vector_store_with_youtube(self,link):
        """updating the vectorstore with the youtube video link we get"""
        loader = YoutubeLoader.from_youtube_url(
                youtube_url=link, 
                add_video_info=False,
                language=["en", "en-US"],
                translation="en"
            )
        
        documents=loader.load()
        self.vectorstore.add_documents(documents=documents)
        
    def get_rag_chain(self):
        """Return the RAG chain."""
        return self.chain
    
    def change_template(self,option):
        
        self.template = get_template(option)
        self.prompt = PromptTemplate.from_template(self.template)
        self.compression_retriever = ContextualCompressionRetriever(
            base_retriever=self.vectorstore.as_retriever(),
            base_compressor = self.reranker
        )
        
        question_answer_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=self.prompt
        )
        
        self.chain = create_retrieval_chain(
            retriever=self.compression_retriever,
            combine_docs_chain= question_answer_chain
        )

