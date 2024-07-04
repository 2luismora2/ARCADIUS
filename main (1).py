from database import SessionLocal, engine, test_connection
from api import *



if __name__ == "_main_":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)