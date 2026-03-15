import sqlite3

def inicializar_banco():
    return sqlite3.connect('tarefas.db')

def criar_tabela():
    conexao = inicializar_banco()
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   
        titulo TEXT NOT NULL,
        tempo_gasto INTEGER DEFAULT 0,
        dia_semana TEXT NOT NULL,
        concluida INTEGER DEFAULT 0
    )'''
    )
    conexao.commit()
    conexao.close()
    
