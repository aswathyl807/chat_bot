from fastapi import APIRouter, Request
from utils.rag_upload import RagPipeline
from utils.store_postgress import PostgresStore
import time

router = APIRouter()

rag_run = RagPipeline()

@router.post("/upload_pdf/")
async def upload_pdf(request: Request):

    start = time.time()

    try:
        data = await request.json()
        filepath = data['filepath']
        queryid = data['queryid']

        print(f"upload fun called with filepath: {filepath} and queryid: {queryid}")

        data, file_name = rag_run.load_documents(filepath)
        total_pages = rag_run.get_total_pages(data)
        chunks = rag_run.split_text(data)
        token_count, char_length, chunk_count = rag_run.save_to_chroma(chunks)

        print(f"file_name: {file_name}")
        print(f"Token Count: {token_count}")
        print(f"Char Length: {char_length}")
        print(f"Chunk Count: {chunk_count}")
        print(f"total_pages Count: {total_pages}")

        post_store = PostgresStore()
        post_store.store_to_postgres(file_name, total_pages, token_count, char_length, chunk_count)
        post_store.close_connection()
        print("postgress upload successful")

        end = time.time()
        total_time = end - start

        response_data = {
            "status_code": 200,
            "status_description": "Success",
            "remarks": "File uploaded to ChromaDB successfully.",
            "data": {
                "file_name": file_name,
                "query_id": queryid,
                "chunk_count": chunk_count,
                "token_count": token_count,
                "time_taken": total_time,
            }
        }
        return response_data
    
    except Exception as e:
        response_data = {
            "status_code": 500,
            "status_description": "Bad",
            "remarks": f"File uploaded failed, {e}",
            "data": {}
        }
        return response_data
