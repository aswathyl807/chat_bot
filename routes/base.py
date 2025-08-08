from langchain.embeddings import HuggingFaceEmbeddings

class Base:
  
  def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
