import pandas as pd
import pytest

from src import process_data


def criar_csv(tmp_path, dados):
    """Cria um CSV temporário para os testes."""
    caminho = tmp_path / "dados_teste.csv"
    pd.DataFrame(dados).to_csv(caminho, index=False)
    return caminho


def registro_valido(**alteracoes):
    """Retorna uma leitura válida no formato original do dataset."""
    registro = {
        "id": "leitura-001",
        "room_id/id": "Room Admin",
        "noted_date": "28-07-2018 07:06",
        "temp": 25,
        "out/in": "In",
    }
    registro.update(alteracoes)
    return registro


def test_load_data_renomeia_colunas_e_converte_tipos(
    tmp_path, monkeypatch
):
    caminho = criar_csv(
        tmp_path,
        [
            registro_valido(),
            registro_valido(
                id="leitura-002",
                noted_date="29-07-2018 08:30",
                temp=30,
                **{"out/in": "Out"},
            ),
        ],
    )
    monkeypatch.setattr(process_data, "CSV_PATH", caminho)

    df = process_data.load_data()

    assert list(df.columns) == process_data.COLUNAS_LEITURA
    assert len(df) == 2
    assert pd.api.types.is_datetime64_any_dtype(
        df["reading_timestamp"]
    )
    assert pd.api.types.is_integer_dtype(df["temperature"])
    assert df["temperature"].tolist() == [25, 30]
    assert df["location"].tolist() == ["In", "Out"]


def test_load_data_remove_registros_invalidos_e_duplicados(
    tmp_path, monkeypatch
):
    caminho = criar_csv(
        tmp_path,
        [
            registro_valido(),
            registro_valido(),  # Duplicata exata
            registro_valido(
                id="data-invalida",
                noted_date="31-02-2018 12:00",
            ),
            registro_valido(
                id="temperatura-invalida",
                temp="abc",
            ),
            registro_valido(
                id="local-ausente",
                **{"out/in": None},
            ),
        ],
    )
    monkeypatch.setattr(process_data, "CSV_PATH", caminho)

    df = process_data.load_data()

    assert len(df) == 1
    assert df.iloc[0]["reading_id"] == "leitura-001"


def test_load_data_rejeita_colunas_obrigatorias_ausentes(
    tmp_path, monkeypatch
):
    caminho = criar_csv(
        tmp_path,
        [
            {
                "id": "leitura-001",
                "room_id/id": "Room Admin",
                "noted_date": "28-07-2018 07:06",
                "out/in": "In",
            }
        ],
    )
    monkeypatch.setattr(process_data, "CSV_PATH", caminho)

    with pytest.raises(ValueError, match="Colunas ausentes no CSV"):
        process_data.load_data()


def test_load_data_rejeita_temperatura_fracionaria(
    tmp_path, monkeypatch
):
    caminho = criar_csv(
        tmp_path,
        [registro_valido(temp=25.5)],
    )
    monkeypatch.setattr(process_data, "CSV_PATH", caminho)

    with pytest.raises(
        ValueError,
        match="temperaturas não inteiras",
    ):
        process_data.load_data()


def test_load_data_informa_quando_arquivo_nao_existe(
    tmp_path, monkeypatch
):
    caminho = tmp_path / "inexistente.csv"
    monkeypatch.setattr(process_data, "CSV_PATH", caminho)

    with pytest.raises(FileNotFoundError, match="Arquivo CSV não encontrado"):
        process_data.load_data()
