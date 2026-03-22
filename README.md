# API de Tarefas com Interface Gráfica

API REST completa para gerenciamento de tarefas usando **Flask**, **SQLite** e interface gráfica com **CustomTkinter**.

## Tecnologias
- **Backend**: Python 3, Flask, SQLite
- **Frontend**: CustomTkinter (interface gráfica moderna)
- **Comunicação**: Requests para integração API-GUI

## Estrutura do Projeto
- `main.py`: API Flask com endpoints REST
- `banco.py`: Conexão e criação do banco SQLite
- `gui_tarefas.py`: Interface gráfica para gerenciamento de tarefas
- `test_api.py`: Script de teste automatizado da API
- `tarefas.db`: Banco SQLite gerado localmente
- `requirements.txt`: Dependências do projeto

## Modelo de Dados
Tabela `tarefas`:
- `id` (INTEGER, PK, AUTOINCREMENT)
- `titulo` (TEXT, obrigatório)
- `tempo_gasto` (INTEGER, padrão `0`)
- `dia_semana` (TEXT, obrigatório)
- `concluida` (INTEGER, padrão `0` - 0=não, 1=sim)

## Como Executar

### 1. Preparação
```bash
# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Executar API
```bash
python main.py
```
A API inicia em `http://127.0.0.1:5000` (modo debug ativado).

### 3. Executar Interface Gráfica (em outro terminal)
```bash
# Manter a API rodando no terminal anterior
python gui_tarefas.py
```

## Funcionalidades

### API REST Endpoints

#### 1. Página Inicial
- **GET** `/`
- Retorna informações sobre a API e exemplo de uso

#### 2. Listar Tarefas
- **GET** `/tarefas`
- Retorna lista de todas as tarefas ou mensagem "Nenhuma tarefa encontrada" (404)

#### 3. Criar Tarefa
- **POST** `/tarefas`
- Body JSON obrigatório com: titulo, tempo_gasto, dia_semana, concluida
- Retorna confirmação com ID da tarefa criada

#### 4. Atualizar Tarefa
- **PUT** `/tarefas/<id>`
- Body JSON com campos a atualizar
- Requer ID na URL

#### 5. Deletar Tarefa
- **DELETE** `/tarefas/<id>`
- Remove tarefa pelo ID

### Interface Gráfica (GUI)

A GUI oferece interface intuitiva para todas as operações:

#### Campos da Interface:
- **ID da tarefa**: Para operações de atualização/deleção
- **Título da tarefa**: Campo obrigatório
- **Tempo gasto (minutos)**: Campo obrigatório, deve ser número
- **Dia da semana**: Campo obrigatório
- **Concluída**: Checkbox para marcar tarefa como concluída

#### Botões Disponíveis:
- **Adicionar Tarefa**: Cria nova tarefa
- **Listar Tarefas**: Mostra todas as tarefas no banco
- **Atualizar Tarefa**: Modifica tarefa existente (requer ID)
- **Deletar Tarefa**: Remove tarefa (requer ID)

#### Área de Resultados:
- Exibe mensagens de sucesso/erro
- Mostra lista de tarefas quando solicitada
- Tratamento inteligente de respostas da API

## Exemplos de Uso

### Via API (cURL)

Criar tarefa:
```bash
curl -X POST http://127.0.0.1:5000/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Estudar Python","tempo_gasto":120,"dia_semana":"segunda","concluida":0}'
```

Listar tarefas:
```bash
curl http://127.0.0.1:5000/tarefas
```

Atualizar tarefa (ID 1):
```bash
curl -X PUT http://127.0.0.1:5000/tarefas/1 \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Estudar Python Avançado","tempo_gasto":180,"concluida":1}'
```

Deletar tarefa (ID 1):
```bash
curl -X DELETE http://127.0.0.1:5000/tarefas/1
```

### Via Interface Gráfica

1. **Adicionar tarefa**:
   - Preencher título, tempo, dia da semana
   - Marcar "Concluída" se necessário
   - Clicar "Adicionar Tarefa"

2. **Listar tarefas**:
   - Clicar "Listar Tarefas"
   - Ver lista na área de resultados

3. **Atualizar tarefa**:
   - Inserir ID da tarefa
   - Preencher novos dados
   - Clicar "Atualizar Tarefa"

4. **Deletar tarefa**:
   - Inserir ID da tarefa
   - Clicar "Deletar Tarefa"

## Testes Automatizados

Execute testes da API:
```bash
python test_api.py
```

O script testa automaticamente:
- Criação de tarefa
- Listagem de tarefas
- Atualização de tarefa
- Deleção de tarefa
- Verificação final

## Tratamento de Erros

### API:
- Campos obrigatórios não preenchidos → 400 Bad Request
- ID não encontrado → 404 Not Found
- Lista vazia → 404 com mensagem personalizada

### GUI:
- Campos vazios → Alerta popup
- Tempo não numérico → Alerta popup
- ID inválido → Alerta popup
- Erros da API → Mensagem clara na interface

## Observações Técnicas

- **Banco de dados**: SQLite com autoincrement (IDs não são reutilizados após deleção)
- **Threading**: GUI usa threads para não bloquear interface durante requisições
- **Validação**: Tanto API quanto GUI validam dados antes de enviar
- **Debug**: API roda em modo debug para desenvolvimento

## Melhorias Futuras

- Autenticação de usuários
- Categorias de tarefas
- Filtros e busca avançada
- Interface responsiva
- Deploy em produção
- Testes unitários completos

---

**Desenvolvido com ❤️ para aprendizado e demonstração de APIs REST com interface gráfica.**
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

## Testes Automatizados

Execute testes da API:
```bash
python test_api.py
```

O script testa automaticamente:
- Criação de tarefa
- Listagem de tarefas
- Atualização de tarefa
- Deleção de tarefa
- Verificação final

## Tratamento de Erros

### API:
- Campos obrigatórios não preenchidos → 400 Bad Request
- ID não encontrado → 404 Not Found
- Lista vazia → 404 com mensagem personalizada

### GUI:
- Campos vazios → Alerta popup
- Tempo não numérico → Alerta popup
- ID inválido → Alerta popup
- Erros da API → Mensagem clara na interface

## Observações Técnicas

- **Banco de dados**: SQLite com autoincrement (IDs não são reutilizados após deleção)
- **Threading**: GUI usa threads para não bloquear interface durante requisições
- **Validação**: Tanto API quanto GUI validam dados antes de enviar
- **Debug**: API roda em modo debug para desenvolvimento

## Melhorias Futuras

- Autenticação de usuários
- Categorias de tarefas
- Filtros e busca avançada
- Interface responsiva
- Deploy em produção
- Testes unitários completos

---

**Desenvolvido com ❤️ para aprendizado e demonstração de APIs REST com interface gráfica.**
