>> alembic init migrations
modificar migrations - script.py.mako:
    import sqlmodel  # en la linea 10
modificar migrations - env.py
    from sqlmodel import SQLModel # linea 5
    from db.models import *   # linea 6
    target_metadata = SQLModel.metadata # linea 23
modificar alembic.ini 
    sqlalchemy.url = sqlite:///database.db #linea 58
>> alembic revision --autogenerate -m "init"
aplicar las migraciones
>> alembic upgrade head

>> alembic revision -m "Add a column"