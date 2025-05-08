Gerador de Etiquetas
Este projeto é um Gerador de Etiquetas simples desenvolvido em Python com a biblioteca Tkinter para a interface gráfica e ReportLab para a criação de PDFs. O sistema permite a criação e visualização de etiquetas personalizadas com códigos de barras, seja de forma manual ou automática, e a exportação dessas etiquetas para um arquivo PDF. Também inclui um histórico de PDFs gerados, possibilitando o reprocessamento ou reabertura de arquivos anteriores.

Funcionalidades
Etiquetas Manuais: Criação de etiquetas com nome, ID, largura e altura personalizáveis.

Etiquetas Automáticas: Geração de etiquetas com base em um intervalo de IDs, usando o mesmo nome, largura e altura.

Visualização de Etiquetas: Exibição das etiquetas na interface para conferência antes da exportação.

Geração de PDF: As etiquetas podem ser exportadas como arquivos PDF, com layout otimizado para impressão.

Histórico de PDFs: Visualização e reabertura de PDFs gerados anteriormente.

Interface Intuitiva: Interface gráfica simples e fácil de usar, com menus para navegação entre as diferentes seções.

Tecnologias
Tkinter: Para a criação da interface gráfica.

ReportLab: Para a geração de arquivos PDF com etiquetas e códigos de barras.

Pillow: Para manipulação de imagens (se necessário para futuras melhorias).

Python 3.x: Linguagem de programação utilizada para o desenvolvimento.

Como Executar
Clone este repositório para o seu computador:
git clone https://github.com/seuusuario/gerador-etiquetas.git

Instale as dependências:
pip install -r requirements.txt

Execute o aplicativo:
python main.py
