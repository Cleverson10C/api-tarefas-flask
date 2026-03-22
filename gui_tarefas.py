import customtkinter as ctk
import tkinter.messagebox as messagebox
import requests
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TarefasApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Tarefas")
        self.geometry("600x600")
        self.criar_interface()

    def criar_interface(self):
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True)

        self.label_titulo = ctk.CTkLabel(self.frame_principal, text="Gerenciador de Tarefas", font=("Arial", 20))
        self.entrada_id = ctk.CTkEntry(self.frame_principal, placeholder_text="ID da tarefa (para atualizar/deletar)")
        self.entrada_titulo = ctk.CTkEntry(self.frame_principal, placeholder_text="Digite o título da tarefa")
        self.entrada_tempo = ctk.CTkEntry(self.frame_principal, placeholder_text="Tempo gasto (minutos)")
        self.entrada_dia = ctk.CTkEntry(self.frame_principal, placeholder_text="Dia da semana")
        self.checkbox_concluida = ctk.CTkCheckBox(self.frame_principal, text="Concluída")

        self.botao_adicionar = ctk.CTkButton(self.frame_principal, text="Adicionar Tarefa", command=self.adicionar_tarefa)
        self.botao_listar = ctk.CTkButton(self.frame_principal, text="Listar Tarefas", command=self.listar_tarefas)
        self.botao_atualizar = ctk.CTkButton(self.frame_principal, text="Atualizar Tarefa", command=self.atualizar_tarefa)
        self.botao_deletar = ctk.CTkButton(self.frame_principal, text="Deletar Tarefa", command=self.deletar_tarefa)

        self.texto_resultados = ctk.CTkTextbox(self.frame_principal, width=600, height=250, font=("Arial", 16))

        self.label_titulo.grid(row=0, column=0, columnspan=2, pady=10)
        self.entrada_id.grid(row=1, column=0, columnspan=2, pady=5)
        self.entrada_titulo.grid(row=2, column=0, columnspan=2, pady=5)
        self.entrada_tempo.grid(row=3, column=0, columnspan=2, pady=5)
        self.entrada_dia.grid(row=4, column=0, columnspan=2, pady=5)
        self.checkbox_concluida.grid(row=5, column=0, columnspan=2, pady=5)
        self.botao_adicionar.grid(row=6, column=0, pady=10)
        self.botao_listar.grid(row=6, column=1, pady=10)
        self.botao_atualizar.grid(row=7, column=0, pady=10)
        self.botao_deletar.grid(row=7, column=1, pady=10)
        self.texto_resultados.grid(row=8, column=0, columnspan=2, pady=10)

    def preparar_dados(self):
        titulo = self.entrada_titulo.get()
        tempo_gasto_str = self.entrada_tempo.get()
        dia_semana = self.entrada_dia.get()
        concluida = 1 if self.checkbox_concluida.get() else 0

        if not titulo or not tempo_gasto_str or not dia_semana:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return None

        try:
            tempo_gasto = int(tempo_gasto_str)
        except ValueError:
            messagebox.showerror("Erro", "Tempo gasto deve ser um número inteiro!")
            return None

        return {
            "titulo": titulo,
            "tempo_gasto": tempo_gasto,
            "dia_semana": dia_semana,
            "concluida": concluida
        }

    def adicionar_tarefa(self):
        dados = self.preparar_dados()
        if dados:
            threading.Thread(target=self._enviar_requisicao, args=("POST", "http://127.0.0.1:5000/tarefas", dados)).start()

    def listar_tarefas(self):
        threading.Thread(target=self._enviar_requisicao, args=("GET", "http://127.0.0.1:5000/tarefas")).start()

    def atualizar_tarefa(self):
        id_str = self.entrada_id.get()
        if not id_str:
            messagebox.showerror("Erro", "Informe o ID da tarefa!")
            return
        try:
            id_tarefa = int(id_str)
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número!")
            return

        dados = self.preparar_dados()
        if dados:
            url = f"http://127.0.0.1:5000/tarefas/{id_tarefa}"
            threading.Thread(target=self._enviar_requisicao, args=("PUT", url, dados)).start()

    def deletar_tarefa(self):
        id_str = self.entrada_id.get()
        if not id_str:
            messagebox.showerror("Erro", "Informe o ID da tarefa!")
            return
        try:
            id_tarefa = int(id_str)
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número!")
            return

        url = f"http://127.0.0.1:5000/tarefas/{id_tarefa}"
        threading.Thread(target=self._enviar_requisicao, args=("DELETE", url)).start()

    def _enviar_requisicao(self, metodo, url, dados=None):
        try:
            if metodo == "GET":
                resposta = requests.get(url)
            elif metodo == "POST":
                resposta = requests.post(url, json=dados)
            elif metodo == "PUT":
                resposta = requests.put(url, json=dados)
            elif metodo == "DELETE":
                resposta = requests.delete(url)
            self.after(0, lambda: self._atualizar_resultados(resposta))
        except requests.RequestException as erro:
            self.after(0, lambda: self._atualizar_resultados(None, str(erro)))

    def _atualizar_resultados(self, resposta, erro=None):
        self.texto_resultados.delete("0.0", "end")
        if erro:
            self.texto_resultados.insert("0.0", f"Erro: {erro}")
            return

        if resposta is None:
            self.texto_resultados.insert("0.0", "Erro desconhecido: resposta vazia")
            return

        # Tenta extrair JSON sempre
        dados = None
        mensagem = None
        try:
            dados = resposta.json()
            if isinstance(dados, dict):
                mensagem = dados.get("mensagem")
        except ValueError:
            pass

        if resposta.status_code in [200, 201]:
            if isinstance(dados, list):
                for item in dados:
                    self.texto_resultados.insert("end", f"ID: {item.get('id')}, Título: {item.get('titulo')}, Tempo: {item.get('tempo_gasto')}, Dia: {item.get('dia_semana')}, Concluída: {item.get('concluida')}\n")
            elif mensagem:
                self.texto_resultados.insert("0.0", f"Sucesso: {mensagem}")
            elif dados is not None:
                self.texto_resultados.insert("0.0", f"Sucesso: {dados}")
            else:
                self.texto_resultados.insert("0.0", resposta.text)
            return

        # Tratamento de erros (404/400/outros)
        if mensagem:
            self.texto_resultados.insert("0.0", f"Erro {resposta.status_code}: {mensagem}")
        elif dados is not None:
            self.texto_resultados.insert("0.0", f"Erro {resposta.status_code}: {dados}")
        else:
            self.texto_resultados.insert("0.0", f"Erro {resposta.status_code}: {resposta.text}")         

if __name__ == "__main__":
    app = TarefasApp()
    app.mainloop()      