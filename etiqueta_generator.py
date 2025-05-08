from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.graphics.barcode import code128
from reportlab.graphics.barcode import code128, code39, code93

def gerar_pdf(etiquetas, nome_arquivo):
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    pagina_largura, pagina_altura = A4

    mm_para_pt = 2.83465  # Conversão de mm para pontos

    margem_superior = 20
    margem_lateral = 20
    espacamento_horizontal = 5
    espacamento_vertical = 5

    x = margem_lateral
    y = pagina_altura - margem_superior

    linha_altura = 0  # guarda a maior altura da linha atual

    for nome, codigo, largura_mm, altura_mm in etiquetas:
        largura = largura_mm * mm_para_pt
        altura = altura_mm * mm_para_pt

        # Se não couber na linha atual, vai para próxima linha
        if x + largura > pagina_largura - margem_lateral:
            x = margem_lateral
            y -= linha_altura + espacamento_vertical
            linha_altura = 0

        # Se não couber na página, inicia nova página
        if y - altura < margem_lateral:
            c.showPage()
            x = margem_lateral
            y = pagina_altura - margem_superior
            linha_altura = 0

        # Atualiza a maior altura da linha atual
        if altura > linha_altura:
            linha_altura = altura

        # Desenhar contorno da etiqueta
        c.rect(x, y - altura, largura, altura)

        # Nome centralizado no topo da etiqueta
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + largura / 2, y - 12, nome)

        # Código de barras centralizado
        try:
            bar_height = altura / 3
            barcode = code128.Code128(codigo, barHeight=bar_height, barWidth=0.5)
            barcode_width = barcode.width
            barcode_x = x + (largura - barcode_width) / 2
            barcode_y = y - altura / 2 - bar_height / 2
            barcode.drawOn(c, barcode_x, barcode_y)
        except Exception as e:
            c.setFont("Helvetica", 6)
            c.drawString(x + 5, y - altura / 2, f"Erro: {e}")

        # ID centralizado na parte inferior da etiqueta
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + largura / 2, y - altura + 5, codigo)

        x += largura + espacamento_horizontal  # Move para a direita

    c.save()
