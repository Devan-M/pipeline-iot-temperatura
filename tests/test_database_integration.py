import os

import pandas as pd
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from src.process_data import load_into_database


@pytest.fixture
def test_engine():
    database_url = os.getenv("TEST_DATABASE_URL")

    if not database_url:
        pytest.skip("Defina TEST_DATABASE_URL para executar a integração.")

    url = make_url(database_url)

    # Proteção contra execução acidental no banco principal.
    if (
        url.database != "iot_test"
        or url.host not in {"127.0.0.1", "localhost"}
        or url.port != 55432
    ):
        pytest.fail(
            "Por segurança, os testes exigem o banco iot_test "
            "em localhost:55432."
        )

    engine = create_engine(database_url)

    try:
        with engine.begin() as connection:
            connection.execute(
                text("TRUNCATE TABLE temperature_readings RESTART IDENTITY")
            )

        yield engine

    finally:
        with engine.begin() as connection:
            connection.execute(
                text("TRUNCATE TABLE temperature_readings RESTART IDENTITY")
            )
        engine.dispose()


def criar_leituras():
    return pd.DataFrame(
        [
            {
                "reading_id": "teste-001",
                "room_id": "Room Test",
                "reading_timestamp": pd.Timestamp("2026-01-01 10:00:00"),
                "temperature": 25,
                "location": "In",
            },
            {
                "reading_id": "teste-002",
                "room_id": "Room Test",
                "reading_timestamp": pd.Timestamp("2026-01-01 11:00:00"),
                "temperature": 30,
                "location": "Out",
            },
        ],
        columns=[
            "reading_id",
            "room_id",
            "reading_timestamp",
            "temperature",
            "location",
        ],
    )


def test_carga_repetida_nao_insere_duplicatas(test_engine):
    df = criar_leituras()

    primeira_carga = load_into_database(df, test_engine)
    segunda_carga = load_into_database(df, test_engine)

    with test_engine.connect() as connection:
        total = connection.execute(
            text("SELECT COUNT(*) FROM temperature_readings")
        ).scalar_one()

    assert primeira_carga == 2
    assert segunda_carga == 0
    assert total == 2


def test_carga_insere_somente_novas_leituras(test_engine):
    df = criar_leituras()

    primeira_carga = load_into_database(df, test_engine)

    leitura_nova = pd.DataFrame(
        [
            {
                "reading_id": "teste-003",
                "room_id": "Room Test",
                "reading_timestamp": pd.Timestamp("2026-01-01 12:00:00"),
                "temperature": 28,
                "location": "In",
            }
        ]
    )

    segunda_carga = load_into_database(
        pd.concat([df.iloc[[0]], leitura_nova], ignore_index=True),
        test_engine,
    )

    with test_engine.connect() as connection:
        total = connection.execute(
            text("SELECT COUNT(*) FROM temperature_readings")
        ).scalar_one()

    assert primeira_carga == 2
    assert segunda_carga == 1
    assert total == 3
