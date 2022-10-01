from sqlmodel import SQLModel, Session, create_engine
try:
    from . import models
except:
    import models


sqlite_filename = 'database.db'
sqlite_url = f"sqlite:///{sqlite_filename}"


engine = create_engine(sqlite_url, echo=True)
session = Session(bind=engine)

if __name__ == '__main__':
    SQLModel.metadata.create_all(engine)