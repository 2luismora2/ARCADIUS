from database import SessionLocal, engine, test_connection

# Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if _name_ == "_main_":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)