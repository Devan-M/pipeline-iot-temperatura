import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Carrega as variáveis do arquivo .env
load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"
)


# Cria a conexão com o PostgreSQL
engine = create_engine(DATABASE_URL)


# Testa a conexão
with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))
    version = result.scalar()

    print("Conexão com PostgreSQL realizada com sucesso!")
    print(f"Versão: {version}")
