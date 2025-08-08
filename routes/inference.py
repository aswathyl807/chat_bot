from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.inference import Inference
import time


router = APIRouter()
infer = Inference()


class QueryRequest(BaseModel):
    query: str
    queryid: str

@router.post("/inference/")
async def query(query_request: QueryRequest):

    start = time.time()

    try:

        formatted_response, response_text, query_id = infer.query_rag(query_request.query)

        end = time.time()
        total_time = end - start

        data = {
            "status_code": 200,
            "status_description": "Success",
            "remarks": "Query processed success.",
            "data": {
                "response": formatted_response,
                "query_id": query_request.queryid,
                "time_taken": total_time,
            }
        }
        return data
    except Exception as e:
        data = {
            "status_code": 500,
            "status_description": "Bad",
            "remarks": "Query processing failed",
            "data": {},
            "error": str(e)
        }
        return data



