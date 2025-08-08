from django.shortcuts import render
from django.http import JsonResponse
import shutil
from django.views.decorators.csrf import csrf_exempt
from fastapi import FastAPI
import os
import uvicorn
from utils.store_postgress import PostgresStore
# from utils.inference import Inference
from routes import rag_upload,inference,dashboard

app = FastAPI()

# Include routers
app.include_router(rag_upload.router)
app.include_router(dashboard.router)
app.include_router(inference.router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000,reload=False)
    


