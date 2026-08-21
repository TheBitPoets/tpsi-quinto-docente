import os
from fastapi import FastAPI
from sqlalchemy import create_engine

DATABASE_URL=os.getenv("FEISBUC_DATABASE_URL","sqlite:///./prod.db")
engine=create_engine(DATABASE_URL)
app=FastAPI()

@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.exec_driver_sql("select 1")
    return {"status":"ok","database":DATABASE_URL}

@app.get("/ready")
def ready():
    return {"status":"ok"}

# startup also creates schema here (omitted)
# production command: uvicorn app:app --reload --workers 4
