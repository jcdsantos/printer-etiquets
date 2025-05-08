import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
import subprocess
import sys
from etiqueta_generator import gerar_pdf

HISTORICO_DIR = "historico_pdfs"
os.makedirs(HISTORICO_DIR, exist_ok=True)

class EtiquetaApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerador de Etiquetas")

        self.etiquetas = []

        self.setup_layout()
        self.show_etiquetas_manuais()

    def setup_layout(self):
        self.sidebar = tk.Frame(self.master, width=150, bg="#eeeeee")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        btn_manuais = tk.Button(self.sidebar, text="Etiquetas Manuais", command=self.show_etiquetas_manuais)
        btn_manuais.pack(fill=tk.X, padx=10, pady=5)

        btn_automaticas = tk.Button(self.sidebar, text="Etiquetas Automáticas", command=self.show_etiquetas_automaticas)
        btn_automaticas.pack(fill=tk.X, padx=10, pady=5)

        btn_historico = tk.Button(self.sidebar, text="Histórico", command=self.show_historico)
        btn_historico.pack(fill=tk.X, padx=10, pady=5)

        # Adicionando o botão Sair
        btn_sair = tk.Button(self.sidebar, text="Sair", command=self.sair)
        btn_sair.pack(fill=tk.X, padx=10, pady=5)

    def show_etiquetas_manuais(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.setup_etiquetas_manuais()

    def show_etiquetas_automaticas(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.setup_etiquetas_automaticas()

    def setup_etiquetas_manuais(self):
        tk.Label(self.main_frame, text="Nome:").grid(row=0, column=0)
        self.nome_entry = tk.Entry(self.main_frame)
        self.nome_entry.grid(row=0, column=1)

        tk.Label(self.main_frame, text="ID:").grid(row=1, column=0)
        self.id_entry = tk.Entry(self.main_frame)
        self.id_entry.grid(row=1, column=1)

        tk.Label(self.main_frame, text="Largura (mm):").grid(row=2, column=0)
        self.largura_entry = tk.Entry(self.main_frame)
        self.largura_entry.insert(0, "60")
        self.largura_entry.grid(row=2, column=1)

        tk.Label(self.main_frame, text="Altura (mm):").grid(row=3, column=0)
        self.altura_entry = tk.Entry(self.main_frame)
        self.altura_entry.insert(0, "30")
        self.altura_entry.grid(row=3, column=1)

        tk.Button(self.main_frame, text="Adicionar Etiqueta", command=self.adicionar_etiqueta).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(self.main_frame, text="Gerar PDF", command=self.gerar_pdf).grid(row=5, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(self.main_frame, columns=("Nome", "ID", "Largura", "Altura"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Largura", text="Largura (mm)")
        self.tree.heading("Altura", text="Altura (mm)")
        self.tree.grid(row=6, column=0, columnspan=2, pady=10)

        tk.Button(self.main_frame, text="Remover Selecionada", command=self.remover_etiqueta).grid(row=7, column=0, columnspan=2)

    def setup_etiquetas_automaticas(self):
        tk.Label(self.main_frame, text="Nome:").grid(row=0, column=0)
        self.auto_nome_entry = tk.Entry(self.main_frame)
        self.auto_nome_entry.grid(row=0, column=1)

        tk.Label(self.main_frame, text="ID Início:").grid(row=1, column=0)
        self.auto_id_inicio_entry = tk.Entry(self.main_frame)
        self.auto_id_inicio_entry.grid(row=1, column=1)

        tk.Label(self.main_frame, text="ID Fim:").grid(row=2, column=0)
        self.auto_id_fim_entry = tk.Entry(self.main_frame)
        self.auto_id_fim_entry.grid(row=2, column=1)

        tk.Label(self.main_frame, text="Largura (mm):").grid(row=3, column=0)
        self.auto_largura_entry = tk.Entry(self.main_frame)
        self.auto_largura_entry.insert(0, "60")
        self.auto_largura_entry.grid(row=3, column=1)

        tk.Label(self.main_frame, text="Altura (mm):").grid(row=4, column=0)
        self.auto_altura_entry = tk.Entry(self.main_frame)
        self.auto_altura_entry.insert(0, "30")
        self.auto_altura_entry.grid(row=4, column=1)

        tk.Button(self.main_frame, text="Gerar Etiquetas", command=self.gerar_etiquetas_automaticas).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(self.main_frame, text="Gerar PDF", command=self.gerar_pdf).grid(row=6, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(self.main_frame, columns=("Nome", "ID", "Largura", "Altura"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Largura", text="Largura (mm)")
        self.tree.heading("Altura", text="Altura (mm)")
        self.tree.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(self.main_frame, text="Remover Selecionada", command=self.remover_etiqueta).grid(row=8, column=0, columnspan=2)

    def gerar_etiquetas_automaticas(self):
        nome = self.auto_nome_entry.get().strip()
        try:
            id_inicio = int(self.auto_id_inicio_entry.get())
            id_fim = int(self.auto_id_fim_entry.get())
            largura = float(self.auto_largura_entry.get())
            altura = float(self.auto_altura_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Verifique se todos os campos estão preenchidos corretamente.")
            return

        if id_fim < id_inicio:
            messagebox.showerror("Erro", "ID Fim deve ser maior ou igual ao ID Início.")
            return

        for i in range(id_inicio, id_fim + 1):
            codigo = str(i)
            self.etiquetas.append((nome, codigo, largura, altura))
            self.tree.insert("", "end", values=(nome, codigo, largura, altura))

    def adicionar_etiqueta(self):
        nome = self.nome_entry.get().strip()
        codigo = self.id_entry.get().strip()

        try:
            largura = float(self.largura_entry.get())
            altura = float(self.altura_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Largura e altura devem ser números.")
            return

        if not nome or not codigo:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        self.etiquetas.append((nome, codigo, largura, altura))
        self.tree.insert("", "end", values=(nome, codigo, largura, altura))

        self.nome_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)

    def remover_etiqueta(self):
        selected = self.tree.selection()
        if not selected:
            return
        for item in selected:
            index = self.tree.index(item)
            del self.etiquetas[index]
            self.tree.delete(item)

    def gerar_pdf(self):
        if not self.etiquetas:
            messagebox.showerror("Erro", "Nenhuma etiqueta adicionada.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        gerar_pdf(self.etiquetas, file_path)

        historico_nome = os.path.join(HISTORICO_DIR, os.path.basename(file_path))
        if not os.path.exists(historico_nome):
            try:
                with open(file_path, "rb") as original, open(historico_nome, "wb") as copia:
                    copia.write(original.read())
            except Exception as e:
                print("Erro ao salvar no histórico:", e)

        messagebox.showinfo("Sucesso", f"PDF gerado com sucesso!\nArquivo: {file_path}")
        self.etiquetas = []
        for i in self.tree.get_children():
            self.tree.delete(i)

    def show_historico(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Histórico de PDFs").pack(pady=10)

        self.historico_list = tk.Listbox(self.main_frame, width=60)
        self.historico_list.pack(padx=20, pady=10)

        for nome_arquivo in os.listdir(HISTORICO_DIR):
            self.historico_list.insert(tk.END, nome_arquivo)

        self.historico_list.bind("<Double-1>", self.abrir_pdf)

    def abrir_pdf(self, event):
        selecao = self.historico_list.curselection()
        if not selecao:
            return
        nome_arquivo = self.historico_list.get(selecao[0])
        caminho_pdf = os.path.abspath(os.path.join(HISTORICO_DIR, nome_arquivo))
        try:
            if sys.platform.startswith("win"):
                os.startfile(caminho_pdf)
            elif sys.platform == "darwin":
                subprocess.run(["open", caminho_pdf])
            else:
                subprocess.run(["xdg-open", caminho_pdf])
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o PDF:\n{e}")

    def sair(self):
        resposta = messagebox.askyesno("Sair", "Tem certeza que deseja sair?")
        if resposta:
            self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = EtiquetaApp(root)
    root.mainloop()
