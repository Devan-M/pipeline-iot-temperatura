
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================================
# CONFIGURAÇÃO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "IOT-temp.csv"

load_dotenv(BASE_DIR / ".env")

COLUNAS_LEITURA = [
    "reading_id",
    "room_id",
    "reading_timestamp",
    "temperature",
    "location",
]


# ============================================================
# BANCO DE DADOS
# ============================================================

def create_database_engine():
    """Cria a conexão com o PostgreSQL."""

    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    port = os.getenv("POSTGRES_PORT", "5432")

    if not all([database, user, password]):
        raise ValueError(
            "Variáveis de conexão com o PostgreSQL não configuradas."
        )

    database_url = (
        f"postgresql+psycopg2://"
        f"{user}:{password}"
        f"@localhost:{port}/{database}"
    )

    return create_engine(database_url)


# ============================================================
# LEITURA E TRATAMENTO DO DATASET
# ============================================================

def load_data() -> pd.DataFrame:
    """Carrega e prepara o dataset para processamento."""

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo CSV não encontrado: {CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    df = df.rename(
        columns={
            "id": "reading_id",
            "room_id/id": "room_id",
            "noted_date": "reading_timestamp",
            "temp": "temperature",
            "out/in": "location",
        }
    )

    colunas_ausentes = set(COLUNAS_LEITURA) - set(df.columns)

    if colunas_ausentes:
        raise ValueError(
            f"Colunas ausentes no CSV: {sorted(colunas_ausentes)}"
        )

    df["reading_timestamp"] = pd.to_datetime(
        df["reading_timestamp"],
        format="%d-%m-%Y %H:%M",
        errors="coerce",
    )

    df["temperature"] = pd.to_numeric(
        df["temperature"],
        errors="coerce",
    )

    df = df.dropna(subset=COLUNAS_LEITURA)

    # Mantém apenas uma ocorrência de linhas totalmente idênticas
    # dentro do próprio arquivo.
    df = df.drop_duplicates(subset=COLUNAS_LEITURA)

    # A tabela de destino utiliza INTEGER para temperatura.
    if not (df["temperature"] % 1 == 0).all():
        raise ValueError(
            "Existem temperaturas não inteiras incompatíveis com a tabela."
        )

    df["temperature"] = df["temperature"].astype("int64")

    return df[COLUNAS_LEITURA].copy()


# ============================================================
# CARGA IDEMPOTENTE
# ============================================================

def load_into_database(df: pd.DataFrame, engine) -> int:
    """
    Insere somente leituras que ainda não existem no banco.

    A comparação usa os cinco campos da leitura, sem pressupor
    que reading_id seja único.
    """

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TEMPORARY TABLE temperature_readings_stage (
                    reading_id VARCHAR(100) NOT NULL,
                    room_id VARCHAR(100) NOT NULL,
                    reading_timestamp TIMESTAMP NOT NULL,
                    temperature INTEGER NOT NULL,
                    location VARCHAR(10) NOT NULL
                ) ON COMMIT DROP
                """
            )
        )

        df.to_sql(
            "temperature_readings_stage",
            con=connection,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )

        result = connection.execute(
            text(
                """
                INSERT INTO temperature_readings (
                    reading_id,
                    room_id,
                    reading_timestamp,
                    temperature,
                    location
                )
                SELECT DISTINCT
                    stage.reading_id,
                    stage.room_id,
                    stage.reading_timestamp,
                    stage.temperature,
                    stage.location
                FROM temperature_readings_stage AS stage
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM temperature_readings AS existing
                    WHERE existing.reading_id = stage.reading_id
                      AND existing.room_id = stage.room_id
                      AND existing.reading_timestamp =
                          stage.reading_timestamp
                      AND existing.temperature = stage.temperature
                      AND existing.location = stage.location
                )
                """
            )
        )

        return result.rowcount


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    df = load_data()

    print(f"Arquivo carregado: {CSV_PATH}")
    print(f"Leituras válidas e únicas no CSV: {len(df)}")

    engine = create_database_engine()

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Conexão com PostgreSQL validada.")
        print("Iniciando carga idempotente...")

        inseridos = load_into_database(df, engine)

        print("Carga concluída.")
        print(f"Novas leituras inseridas: {inseridos}")
        print(f"Leituras já existentes ou repetidas ignoradas: "
              f"{len(df) - inseridos}")

    finally:
        engine.dispose()
