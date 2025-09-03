from ..tools.createSQLengine import init_engine

engine, SessionDep = init_engine("sqlite:///database.db", {"check_same_thread": False})