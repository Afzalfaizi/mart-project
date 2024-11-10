from sqlmodel import SQLModel, Session, create_engine
from app import settings

#database connection
connection_string=str(settings.DATABASE_URL)
print(connection_string)
engine = create_engine(connection_string, echo=True, pool_pre_ping=True)
print(engine)
def create_tables():
    SQLModel.metadata.create_all(engine)
# Dependency to get the session
def get_session():
    with Session(engine) as session:
        yield session