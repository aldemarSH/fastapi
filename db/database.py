from sqlmodel import SQLModel, create_engine, Session

try:
    from . import models
except:
    import models


sqlite_file_name = "database2.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
session = Session(bind=engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()