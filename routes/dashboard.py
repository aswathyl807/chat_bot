from fastapi import APIRouter, Response
from utils.store_postgress import PostgresStore
import time
import json

router = APIRouter()

@router.get("/dashboard/")
async def get_dashboard_data():

    start = time.time()
    
    try:
        post_store = PostgresStore()
        data = post_store.get_data()
        post_store.close_connection()

        end = time.time()
        total_time = end - start

        response_data = {
            "status_code": 200,
            "status_description": "Success",
            "remarks": "fetched from db.",
            "data": {
                "data": data,
                "time_taken": total_time,
            }
        }
        return response_data
    
    except Exception as e:
        response_data = {
            "status_code": 500,
            "status_description": "Bad",
            "remarks": str(e),
            "data": {}
        }
        return response_data
