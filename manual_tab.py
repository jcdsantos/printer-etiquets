import tkinter as tk
from tkinter import messagebox
from etiqueta_generator import gerar_pdf

class ManualEtiquetaFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.etiquetas = []

        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Nome:").grid(row=0, column=0)
        self.nome_entry = tk.Entry(self)
        self.nome_entry.grid(row=0, column=1)

        tk.Label(self, text="ID:").grid(row=1, column=0)
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=1, column=1)

        tk.Label(self, text="Largura (mm):").grid(row=2, column=0)
        self.largura_entry = tk.Entry(self)
        self.largura_entry.insert(0, "60")
        self.largura_entry.grid(row=2, column=1)

        tk.Label(self, text="Altura (mm):").grid(row=3, column=0)
        self.altura_entry = tk.Entry(self)
        self.altura_entry.insert(0, "30")
        self.altura_entry.grid(row=3, column=1)

        tk.Button(self, text="Adicionar Etiqueta", command=self.adicionar_etiqueta).grid(row=4, column=0, columnspan=2)
        tk.Button(self, text="Gerar PDF", command=self.gerar_pdf).grid(row=5, column=0, columnspan=2)

        self.canvas = tk.Canvas(self, width=595, height=842, bg="white")
        self.canvas.grid(row=0, column=2, rowspan=10, padx=10)

    def adicionar_etiqueta(self):
        nome = self.nome_entry.get().strip()
        codigo = self.id_entry.get().strip()

        if not nome or not codigo:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        try:
            largura = float(self.largura_entry.get())
            altura = float(self.altura_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Largura e altura devem ser números.")
            return

        self.etiquetas.append((nome, codigo, largura, altura))
        self.nome_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self._atualizar_canvas()

    def _atualizar_canvas(self):
        self.canvas.delete("all")
        x, y = 10, 10
        for nome, codigo, largura_mm, altura_mm in self.etiquetas:
            largura = largura_mm * 2.83465
            altura = altura_mm * 2.83465
            if x + largura > 595:
                x = 10
                y += altura + 10
            if y + altura > 842:
                break
            self.canvas.create_rectangle(x, y, x + largura, y + altura, outline="black")
            self.canvas.create_text(x + largura / 2, y + 12, text=nome)
            self.canvas.create_text(x + largura / 2, y + altura - 12, text=codigo)
            x += largura + 10

    def gerar_pdf(self):
        if not self.etiquetas:
            messagebox.showerror("Erro", "Nenhuma etiqueta adicionada.")
            return
        gerar_pdf(self.etiquetas, "etiquetas.pdf")
        messagebox.showinfo("Sucesso", "PDF gerado com sucesso! Arquivo: etiquetas.pdf")
        self.etiquetas = []
        self._atualizar_canvas()
