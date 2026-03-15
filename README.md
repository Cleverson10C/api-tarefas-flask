# API de Tarefas

API REST simples para gerenciamento de tarefas usando **Flask** e **SQLite**.

## Tecnologias
- Python 3
- Flask
- SQLite (`sqlite3`, nativo do Python)

## Estrutura do Projeto
- `main.py`: inicializa a aplicação Flask e define as rotas CRUD.
- `banco.py`: cria conexão com banco e garante a criação da tabela `tarefas`.
- `tarefas.db`: banco SQLite gerado localmente.

## Modelo de Dados
Tabela `tarefas`:
- `id` (INTEGER, PK, AUTOINCREMENT)
- `titulo` (TEXT, obrigatório)
- `tempo_gasto` (INTEGER, padrão `0`)
- `dia_semana` (TEXT, obrigatório)
- `concluida` (INTEGER, padrão `0`)  

> Observação: o campo `concluida` está como inteiro (`0` ou `1`).

## Como Executar
1. Crie e ative um ambiente virtual (opcional, recomendado).
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute a API:

```bash
python main.py
```

A aplicação inicia em `http://127.0.0.1:5000` (modo `debug=True`).

## Endpoints

### 1. Página inicial
- **GET** `/`

Resposta (exemplo):

```json
{
  "mensagem": "Bem-vindo à API de Tarefas!",
  "como_criar_tarefa": {
    "metodo": "POST",
    "endpoint": "/tarefas",
    "headers": {
      "Content-Type": "application/json"
    },
    "body_exemplo": {
      "titulo": "Estudar Flask",
      "tempo_gasto": 60,
      "dia_semana": "segunda",
      "concluida": 0
    }
  }
}
```

### 2. Listar tarefas
- **GET** `/tarefas`

Resposta (exemplo):

```json
[
  {
    "id": 1,
    "titulo": "Estudar Flask",
    "tempo_gasto": 60,
    "dia_semana": "segunda",
    "concluida": 0
  }
]
```

### 3. Criar tarefa
- **POST** `/tarefas`

Body JSON:

```json
{
  "titulo": "Estudar Flask",
  "tempo_gasto": 60,
  "dia_semana": "segunda",
  "concluida": 0
}
```

Resposta:

```json
{
  "mensagem": "Tarefa criada com sucesso!"
}
```

### 4. Atualizar tarefa
- **PUT** `/tarefas/<id>`

Body JSON:

```json
{
  "titulo": "Estudar Flask avançado",
  "tempo_gasto": 90,
  "dia_semana": "terça",
  "concluida": 1
}
```

Resposta:

```json
{
  "mensagem": "Tarefa atualizada com sucesso!"
}
```

Se o `id` não for informado na URL (`PUT /tarefas`), resposta:

```json
{
  "mensagem": "Informe o ID na URL para atualizar. Exemplo: /tarefas/1"
}
```

### 5. Deletar tarefa
- **DELETE** `/tarefas/<id>`

Resposta:

```json
{
  "mensagem": "Tarefa deletada com sucesso!"
}
```

Se o `id` não for informado na URL (`DELETE /tarefas`), resposta:

```json
{
  "mensagem": "Informe o ID na URL para deletar. Exemplo: /tarefas/1"
}
```

## Exemplos com cURL

Criar tarefa:

```bash
curl -X POST http://127.0.0.1:5000/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Ler documentação","tempo_gasto":30,"dia_semana":"quarta","concluida":0}'
```

Listar tarefas:

```bash
curl http://127.0.0.1:5000/tarefas
```

Ver instruções na rota principal:

```bash
curl http://127.0.0.1:5000/
```

Atualizar tarefa (id 1):

```bash
curl -X PUT http://127.0.0.1:5000/tarefas/1 \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Ler documentação Flask","tempo_gasto":45,"dia_semana":"quarta","concluida":1}'
```

Deletar tarefa (id 1):

```bash
curl -X DELETE http://127.0.0.1:5000/tarefas/1
```

## Observações de Melhoria (análise do código)
- Ainda não há validação completa dos campos obrigatórios do JSON (`titulo`, `tempo_gasto`, `dia_semana`, `concluida`), então payload incompleto pode causar `KeyError`.
- As rotas `PUT`/`DELETE` não verificam se o `id` existe no banco antes de responder sucesso.
- Em produção, o ideal é desativar `debug=True`.
