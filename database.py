from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:223344@localhost:5432/taskdb"

# postgresql://postgres:223344@localhost:5432/react_fastapi

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

def get_db():
    print("Getting database session")
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        print("Closing database session")
        db.close()
