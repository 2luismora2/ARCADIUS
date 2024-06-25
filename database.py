from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:toor@localhost/libros"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Connection to the database was successful.")
    except OperationalError:
        print("Connection to the database failed.")

if __name__ == "__main__":
    test_connection()