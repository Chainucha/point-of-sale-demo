from typing import Annotated
from sqlmodel import SQLModel, Session, create_engine
from fastapi import Depends

# Create engine once
def init_engine(db_url: str, connect_args: dict | None = None):
    engine = create_engine(db_url, connect_args=connect_args)

    # Dependency for FastAPI
    def get_session():
        with Session(engine) as session:
            yield session

    # Annotated type for convenience
    SessionDep = Annotated[Session, Depends(get_session)]

    return engine, SessionDep
