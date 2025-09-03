from ..tools.createSQLengine import init_engine

# Create engine for SQL database and passing variable "SessionDep"
engine, SessionDep = init_engine("sqlite:///database.db", {"check_same_thread": False})
