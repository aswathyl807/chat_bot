from langchain.llms import Ollama
from langchain.prompts import ChatPromptTemplate
import uuid
from langchain.vectorstores.chroma import Chroma  
from routes.base  import Base


class Inference(Base):


    def __init__(self, model="gemma3:4b",chroma_path="newchroma"):
        super().__init__()
        self.CHROMA_PATH = chroma_path
        self.model = model
        self.PROMPT_TEMPLATE = """Answer the question based on the context: {context} Question: {question}"""
        self.llm = Ollama(model=model)
        self.db = Chroma(persist_directory=self.CHROMA_PATH, embedding_function=self.embeddings)

    def query_rag(self,query_text):

        # Generate a unique query ID
        query_id = str(uuid.uuid4())  


        # Retrieving the context from the DB using similarity search
        results = self.db.similarity_search_with_relevance_scores(query_text, k=3)

        # Checking if there are any matching results or if the relevance score is too low
        if len(results) == 0 or results[0][1] < 0.7:
            print(f"Unable to find matching results.")

        # Combine context from matching documents
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        print(context_text)

        # Create prompt template using context and query text
        prompt_template = ChatPromptTemplate.from_template(self.PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)

        # Generate response text based on the prompt
        response_text = self.llm(prompt)

        # Get sources of the matching documents
        sources = [doc.metadata.get("source", None) for doc, _score in results]

        # Format and return response including generated text and sources
        formatted_response = f"Query ID: {query_id}\nAnswer: {response_text}\nSources: {sources}"
        return formatted_response, response_text, query_id













