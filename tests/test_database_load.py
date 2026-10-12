from unittest.mock import MagicMock, call

import pandas as pd

from src import process_data


def criar_dataframe():
    return pd.DataFrame(
        [
            {
                "reading_id": "leitura-001",
                "room_id": "Room Admin",
                "reading_timestamp": pd.Timestamp("2018-07-28 07:06"),
                "temperature": 25,
                "location": "In",
            },
            {
                "reading_id": "leitura-002",
                "room_id": "Room Admin",
                "reading_timestamp": pd.Timestamp("2018-07-28 08:06"),
                "temperature": 30,
                "location": "Out",
            },
        ],
        columns=process_data.COLUNAS_LEITURA,
    )


def test_carga_cria_tabela_temporaria_e_retorna_inseridos(
    monkeypatch,
):
    df = criar_dataframe()

    connection = MagicMock()
    resultado_insert = MagicMock()
    resultado_insert.rowcount = 2
    connection.execute.return_value = resultado_insert

    engine = MagicMock()
    engine.begin.return_value.__enter__.return_value = connection

    to_sql_mock = MagicMock()
    monkeypatch.setattr(pd.DataFrame, "to_sql", to_sql_mock)

    inseridos = process_data.load_into_database(df, engine)

    assert inseridos == 2
    assert connection.execute.call_count == 2

    sql_criacao = str(connection.execute.call_args_list[0].args[0])
    sql_insert = str(connection.execute.call_args_list[1].args[0])

    assert "CREATE TEMPORARY TABLE temperature_readings_stage" in sql_criacao
    assert "ON COMMIT DROP" in sql_criacao
    assert "ON CONFLICT" in sql_insert
    assert "DO NOTHING" in sql_insert

    to_sql_mock.assert_called_once_with(
        "temperature_readings_stage",
        con=connection,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )


def test_carga_retorna_zero_quando_nenhuma_linha_e_inserida(
    monkeypatch,
):
    df = criar_dataframe()

    connection = MagicMock()
    resultado_insert = MagicMock()
    resultado_insert.rowcount = 0
    connection.execute.return_value = resultado_insert

    engine = MagicMock()
    engine.begin.return_value.__enter__.return_value = connection

    monkeypatch.setattr(
        pd.DataFrame,
        "to_sql",
        MagicMock(),
    )

    inseridos = process_data.load_into_database(df, engine)

    assert inseridos == 0


def test_carga_propaga_erro_ao_falhar_execucao_sql(monkeypatch):
    df = criar_dataframe()

    connection = MagicMock()
    connection.execute.side_effect = RuntimeError("falha simulada")

    engine = MagicMock()
    engine.begin.return_value.__enter__.return_value = connection

    monkeypatch.setattr(
        pd.DataFrame,
        "to_sql",
        MagicMock(),
    )

    import pytest

    with pytest.raises(RuntimeError, match="falha simulada"):
        process_data.load_into_database(df, engine)


def test_carga_propaga_erro_ao_falhar_execucao_sql(monkeypatch):
    df = criar_dataframe()

    connection = MagicMock()
    connection.execute.side_effect = RuntimeError("falha simulada")

    engine = MagicMock()
    engine.begin.return_value.__enter__.return_value = connection

    monkeypatch.setattr(
        pd.DataFrame,
        "to_sql",
        MagicMock(),
    )

    import pytest

    with pytest.raises(RuntimeError, match="falha simulada"):
        process_data.load_into_database(df, engine)
