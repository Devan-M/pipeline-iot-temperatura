# 🌡️ Pipeline IoT de Temperatura

Pipeline de dados em Python que importa, valida, trata e armazena leituras de temperatura em um banco **PostgreSQL**. O projeto também oferece um **dashboard interativo** para explorar os dados processados.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Docker-4169E1?logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)

## 📊 Dashboard de Temperaturas IoT

O projeto conta com um dashboard interativo desenvolvido com **Streamlit** e **Plotly**, integrado ao PostgreSQL, que permite acompanhar os principais indicadores e explorar as leituras de temperatura dos dispositivos IoT.

### 1. Visão geral e principais indicadores

Apresenta uma visão consolidada dos dados processados, destacando os principais indicadores do conjunto de leituras. Essa visualização permite compreender rapidamente o volume de dados e as informações gerais monitoradas pelo sistema.

![Gráfico 1 - Visão geral e principais indicadores](docs/images/Grafico 1.png)

### 2. Evolução das temperaturas ao longo do tempo

Apresenta a evolução das temperaturas registradas ao longo do período disponível no conjunto de dados, permitindo observar variações e identificar tendências temporais.

![Gráfico 2 - Evolução das temperaturas ao longo do tempo](docs/images/grafico-2.png)

### 3. Temperaturas médias e distribuição por hora

Reúne visualizações para analisar as temperaturas médias e a distribuição das leituras por hora do dia. Essa análise auxilia na identificação de diferenças entre as localizações monitoradas e dos horários com maior concentração de registros.

![Gráfico 3 - Temperaturas médias e distribuição por hora](docs/images/grafico-3.png)

---

## 📑 Sumário

- [Objetivos](#-objetivos)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Arquitetura do projeto](#-arquitetura-do-projeto)
- [Estrutura de diretórios](#-estrutura-de-diretórios)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração do ambiente](#-configuração-do-ambiente)
- [Execução do projeto](#-execução-do-projeto)
- [Consultas analíticas](#-consultas-analíticas)
- [Testes automatizados](#-testes-automatizados)
- [Validação dos dados](#-validação-dos-dados)
- [Encerramento do ambiente](#-encerramento-do-ambiente)
- [Segurança](#-segurança)
- [Licença](#-licença)

---

## 🎯 Objetivos

- Processar dados de sensores de temperatura a partir de um arquivo CSV.
- Validar e padronizar os registros antes da carga.
- Remover registros duplicados durante o processamento.
- Armazenar os dados em um banco PostgreSQL.
- Evitar a reinserção de leituras já existentes em execuções posteriores.
- Disponibilizar consultas analíticas por meio de views SQL.
- Visualizar os resultados em um dashboard interativo.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso no projeto |
|---|---|
| **Python** | Processamento e validação dos dados |
| **Pandas e NumPy** | Manipulação e análise de dados |
| **PostgreSQL** | Armazenamento dos registros |
| **Docker Compose** | Execução do banco de dados em container |
| **SQLAlchemy e psycopg2** | Conexão e operações com o PostgreSQL |
| **Streamlit** | Aplicação do dashboard |
| **Plotly** | Visualizações interativas |
| **python-dotenv** | Leitura das variáveis de ambiente |

---

## 🏗️ Arquitetura do projeto

O fluxo de processamento segue estas etapas:

1. Leitura do arquivo CSV.
2. Validação das colunas e dos valores.
3. Conversão dos campos para os tipos esperados.
4. Remoção de registros inválidos e duplicados.
5. Conexão com o PostgreSQL.
6. Carga dos registros ainda não existentes.
7. Consulta dos dados por meio de views SQL.
8. Apresentação dos indicadores no dashboard.

```text
CSV → Validação → Tratamento → PostgreSQL → Views SQL → Dashboard
```

---

## 📁 Estrutura de diretórios

```text
pipeline-iot-temperatura/
├── data/
│   └── IOT-temp.csv
├── sql/
│   ├── create_table.sql
│   └── views.sql
├── src/
│   ├── dashboard.py
│   ├── process_data.py
│   └── test_connection.py
├── tests/
│   ├── test_process_data.py
│   ├── test_database_load.py
│   └── test_database_integration.py
├── .env
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

### Principais arquivos

| Arquivo | Responsabilidade |
|---|---|
| `data/IOT-temp.csv` | Conjunto de dados de entrada |
| `sql/create_table.sql` | Criação da tabela de leituras |
| `sql/views.sql` | Criação das views analíticas |
| `src/process_data.py` | Validação, transformação e carga dos dados |
| `src/test_connection.py` | Verificação da conexão com o PostgreSQL |
| `tests/test_process_data.py` | Testes unitários do processamento dos dados |
| `tests/test_database_load.py` | Testes da lógica de carga com mocks |
| `tests/test_database_integration.py` | Testes de integração com PostgreSQL |
| `requirements-dev.txt` | Dependências de desenvolvimento e testes |
| `src/dashboard.py` | Dashboard interativo |
| `docker-compose.yml` | Configuração do container PostgreSQL |
| `requirements.txt` | Dependências Python |
| `.env` | Configurações e credenciais locais |

---

## ✅ Pré-requisitos

Antes de executar o projeto, tenha instalado:

- Git
- Python 3 e `venv`
- Docker
- Docker Compose

> Os comandos deste documento consideram um ambiente **Linux**, como Ubuntu.

---

## ⚙️ Configuração do ambiente

### 1. Clonar o repositório

```bash
git clone git@github.com:Devan-M/pipeline-iot-temperatura.git
cd pipeline-iot-temperatura
```

Se preferir, o repositório também pode ser clonado por HTTPS.

### 2. Criar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto, utilizando valores próprios para o seu ambiente:

```env
POSTGRES_DB=nome_do_banco
POSTGRES_USER=usuario_do_banco
POSTGRES_PASSWORD=sua_senha
POSTGRES_PORT=5432
```

Os valores acima são apenas exemplos. O banco, o usuário e a senha precisam ser consistentes com a configuração utilizada pelo Docker Compose.

> ⚠️ **Importante:** não publique o arquivo `.env` nem inclua senhas reais no repositório. Ele deve permanecer protegido pelo `.gitignore`.

---

## 🚀 Execução do projeto

### 1. Iniciar o PostgreSQL

Na raiz do projeto, execute:

```bash
docker compose up -d
```

Confira o estado do container:

```bash
docker compose ps
```

Aguarde o PostgreSQL ficar saudável antes de executar os próximos passos.

### 2. Criar a tabela de leituras

O script SQL cria a tabela `temperature_readings`. No terminal Bash, carregue as variáveis do arquivo `.env` e execute o script:

```bash
set -a
source .env
set +a

docker compose exec -T postgres \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  < sql/create_table.sql
```

> O comando pressupõe que o serviço do PostgreSQL no Compose se chama `postgres`, conforme a configuração do projeto.

### 3. Processar e carregar os dados

Com o ambiente virtual ativado, execute:

```bash
python src/process_data.py
```

O script lê o CSV, valida e transforma os registros e insere no PostgreSQL as leituras que ainda não existem na tabela.

A carga foi implementada para permitir novas execuções sem reinserir os registros já encontrados, considerando a comparação dos campos da leitura.

### 4. Criar as views analíticas

```bash
docker compose exec -T postgres \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  < sql/views.sql
```

As views podem ser recriadas a qualquer momento, pois o script utiliza `CREATE OR REPLACE VIEW`.

### 5. Testar a conexão com o banco

```bash
python src/test_connection.py
```

O script verifica se a aplicação consegue estabelecer uma conexão com o PostgreSQL.

### 6. Iniciar o dashboard

```bash
streamlit run src/dashboard.py --server.address 0.0.0.0
```

O Streamlit informa no terminal o endereço para acessar a aplicação. Em um servidor remoto, utilize o endereço IP ou o nome do servidor e a porta informada, considerando as regras de firewall e de rede aplicáveis.

Para encerrar o dashboard, pressione `Ctrl+C` no terminal em que ele está em execução.

---

## 📊 Consultas analíticas

O arquivo `sql/views.sql` disponibiliza três views.

### 1. Temperatura média por localização

**View:** `avg_temp_por_localizacao`

Apresenta a temperatura média e a quantidade de leituras agrupadas pela localização do registro.

```sql
SELECT *
FROM avg_temp_por_localizacao;
```

### 2. Quantidade de leituras por hora

**View:** `leituras_por_hora`

Agrupa os registros pela hora do dia, permitindo observar a distribuição temporal das leituras.

```sql
SELECT *
FROM leituras_por_hora
ORDER BY hora;
```

### 3. Temperaturas mínima, máxima e média por dia

**View:** `temp_max_min_por_dia`

Apresenta estatísticas diárias de temperatura.

```sql
SELECT *
FROM temp_max_min_por_dia
ORDER BY data;
```

---

## 🧪 Testes automatizados

Os testes automatizados verificam o processamento dos dados, a lógica de carga
e a integração com o PostgreSQL.

### Instalar as dependências de desenvolvimento

Na raiz do projeto, com o ambiente virtual ativado:

```bash
pip install -r requirements-dev.txt
```

Esse arquivo instala as dependências da aplicação e o pytest.

### Executar os testes unitários

```bash
python -m pytest -v tests/test_process_data.py tests/test_database_load.py
```

Esses testes verificam as transformações dos dados e a lógica de carga,
utilizando mocks quando não é necessário acessar um banco real.

### Executar a suíte completa

```bash
python -m pytest -v
```

Sem a variável `TEST_DATABASE_URL`, os testes de integração são ignorados
automaticamente. Os testes unitários continuam sendo executados.

### Executar os testes de integração com PostgreSQL

Os testes de integração precisam de um banco exclusivo para testes. Não use
o banco principal do projeto nem as credenciais do arquivo `.env`.

Crie um contêiner PostgreSQL temporário, usando uma porta local dedicada:

```bash
docker run -d --name postgres-iot-test \
  -p 127.0.0.1:55432:5432 \
  -e POSTGRES_DB=iot_test \
  -e POSTGRES_USER=iot_test_user \
  -e POSTGRES_PASSWORD=test_only_password \
  postgres:16-alpine
```

Aguarde o banco ficar pronto:

```bash
until docker exec postgres-iot-test \
  pg_isready -U iot_test_user -d iot_test
do
  sleep 1
done
```

Crie a tabela e o índice necessários aos testes:

```bash
docker exec -i postgres-iot-test \
  psql -U iot_test_user -d iot_test < sql/create_table.sql
```

Execute os testes de integração:

```bash
TEST_DATABASE_URL='postgresql+psycopg2://iot_test_user:test_only_password@127.0.0.1:55432/iot_test' \
  python -m pytest -v tests/test_database_integration.py
```

Para executar todos os testes, incluindo os de integração:

```bash
TEST_DATABASE_URL='postgresql+psycopg2://iot_test_user:test_only_password@127.0.0.1:55432/iot_test' \
  python -m pytest -v
```

Os testes de integração limpam a tabela de teste antes e depois de cada caso.
Use essas credenciais somente no contêiner descartável descrito nesta seção.

Após concluir os testes, remova apenas o contêiner de teste:

```bash
docker rm -f postgres-iot-test
```

Esse comando não remove o contêiner principal `postgres-iot`.

---

## 🔍 Validação dos dados

O pipeline contempla verificações durante o processamento, incluindo:

- Presença das colunas necessárias.
- Conversão de data e hora para o formato esperado.
- Conversão de temperatura para valor numérico inteiro.
- Descarte de registros com campos obrigatórios inválidos.
- Remoção de registros duplicados no conjunto de dados processado.
- Verificação da conexão com o PostgreSQL antes da carga.

A estratégia de carga idempotente evita reinserções em execuções repetidas. Uma restrição de unicidade no PostgreSQL protege a integridade dos dados, inclusive contra tentativas de inserção duplicada.

---

## 🛑 Encerramento do ambiente

Para interromper e remover o container do projeto:

```bash
docker compose down
```

Os dados persistidos no volume nomeado do PostgreSQL são mantidos.

> ⚠️ Para remover também o volume e os dados armazenados, seria necessário usar `docker compose down -v`. Esse comando é **destrutivo** e não deve ser executado se você quiser preservar o banco.

---

## 🔒 Segurança

- Não versionar o arquivo `.env`.
- Não publicar credenciais ou senhas.
- Manter as dependências registradas em `requirements.txt`.
- Evitar expor a porta do banco de dados a redes não confiáveis.
- Utilizar backups adequados para preservar os dados importantes.

---

## 📄 Licença

À ser definida!
