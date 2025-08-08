from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
import tiktoken
from langchain_community.document_loaders import PyPDFLoader
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from langchain.embeddings import HuggingFaceEmbeddings
import os



class RagPipeline:


    def __init__(self, chroma_path="newchroma"):
        self.CHROMA_PATH = chroma_path
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def get_token_count(self, text: str) -> int:
        encoding = tiktoken.encoding_for_model("text-embedding-ada-002")
        return len(encoding.encode(text))

    def get_total_pages(self, data):
        total_pages = data[0].metadata['total_pages']
        return total_pages

    def load_documents(self, pdf_path):
        """Load PDF documents from the specified file using PyPDFLoader."""
        document_loader = PyPDFLoader(pdf_path)
        data = document_loader.load()
        file_name = os.path.basename(data[0].metadata['source'])
        return data, file_name

    
    def split_text(self, documents: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,  # Size of each chunk in characters
            chunk_overlap=100,  # Overlap between consecutive chunks
            length_function=len,  # Function to compute the length of the text
            add_start_index=True,  # Flag to add start index to each chunk
        )
        chunks = text_splitter.split_documents(documents)
        return chunks

    def save_to_chroma(self, chunks: list):
        db = Chroma.from_documents(
            chunks,
            self.embeddings,
            persist_directory=self.CHROMA_PATH
        )
        db.persist()
        token_count = sum(self.get_token_count(chunk.page_content) for chunk in chunks)
        char_length = sum(len(chunk.page_content) for chunk in chunks)
        chunk_count = len(chunks)
        return token_count, char_length, chunk_count






# data_path=r"C:/Users/aswat/Downloads/hulk.pdf"

# chroma_path="newchroma2"

# rag_run=Ragpipeline(data_path,chroma_path)

# data,file_name=rag_run.load_documents()
# total_pages=rag_run.get_total_pages(data)

# chunks=rag_run.split_text(data)
# token_count,char_length,chunk_count=rag_run.save_to_chroma(chunks)



# print(f"Token Count: {token_count}")
# print(f"Char Length: {char_length}")
# print(f"Chunk Count: {chunk_count}")








