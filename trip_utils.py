# Importa a biblioteca Streamlit, usada para construir interfaces web interativas em Python.
import streamlit as st

# Importa o módulo sys, que permite manipular o fluxo de entrada e saída padrão (stdin, stdout, stderr).
import sys

# Importa o decorador contextmanager, que permite criar funções que atuam como gerenciadores de contexto (`with`).
from contextlib import contextmanager

# Importa StringIO, que cria um buffer de texto em memória (como um arquivo, mas armazenado na RAM).
from io import StringIO

# Importa o módulo re (expressões regulares), usado para processar e limpar textos.
import re


# Define uma classe responsável por capturar e exibir saídas de processos no Streamlit.
class StreamlitProcessOutput:
    def __init__(self, container):
        # Armazena a referência ao container Streamlit (ex: `st.empty()` ou `st.container()`),
        # que será usado para exibir o texto dinamicamente.
        self.container = container

        # Guarda o texto acumulado que será exibido no app.
        self.output_text = ""

        # Mantém um conjunto (set) de linhas já vistas, para evitar repetições.
        self.seen_lines = set()

    def clean_text(self, text):
        """Limpa o texto removendo caracteres de controle e logs desnecessários."""
        # Cria uma expressão regular para capturar códigos ANSI (cores e formatações do terminal).
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

        # Remove esses códigos do texto.
        text = ansi_escape.sub('', text)

        # Ignora mensagens de debug específicas do LiteLLM.
        if text.strip().startswith('LiteLLM.Info:') or text.strip().startswith('Provider List:'):
            return None

        # Caso existam, poderia remover códigos de formatação específicos (comentado por enquanto).
        # text = text.replace('[1m', '').replace('[95m', '').replace('[92m', '').replace('[00m', '')

        # Retorna o texto limpo.
        return text

    def write(self, text):
        """Método chamado automaticamente quando algo é impresso (print) no terminal."""
        # Primeiro, limpa o texto.
        cleaned_text = self.clean_text(text)

        # Se o texto for nulo (ex: mensagem ignorada), não faz nada.
        if cleaned_text is None:
            return

        # Divide o texto em linhas para tratar cada uma separadamente.
        lines = cleaned_text.split('\n')
        new_lines = []

        # Percorre todas as linhas.
        for line in lines:
            # Remove espaços extras.
            line = line.strip()

            # Adiciona a linha apenas se for nova e não vazia.
            if line and line not in self.seen_lines:
                self.seen_lines.add(line)
                new_lines.append(line)

        # Se houver novas linhas, atualiza o texto exibido.
        if new_lines:
            # Junta as novas linhas em uma única string separada por quebras de linha.
            new_content = '\n'.join(new_lines)

            # Atualiza o conteúdo acumulado (mantendo histórico das mensagens anteriores).
            self.output_text = f"{self.output_text}\n{new_content}" if self.output_text else new_content

            # Atualiza o container Streamlit em tempo real com o texto novo.
            self.container.text(self.output_text)

    def flush(self):
        """Método obrigatório para compatibilidade com sys.stdout, mas não faz nada aqui."""
        pass


# Define um gerenciador de contexto para capturar saídas (prints) dentro de um bloco `with`.
@contextmanager
def capture_output(container):
    """Captura stdout e redireciona a saída para um container do Streamlit."""
    # Cria um buffer em memória para armazenar temporariamente o texto.
    string_io = StringIO()

    # Cria uma instância do manipulador de saída customizado.
    output_handler = StreamlitProcessOutput(container)

    # Guarda a saída padrão original (stdout original do Python).
    old_stdout = sys.stdout

    # Substitui stdout pelo manipulador customizado (redireciona os `print()`).
    sys.stdout = output_handler

    try:
        # Permite o uso de `with capture_output(container):` dentro do Streamlit.
        yield string_io
    finally:
        # Restaura a saída padrão ao final do bloco `with`, garantindo que o sistema volte ao normal.
        sys.stdout = old_stdout


# Define explicitamente quais símbolos são exportados ao importar este módulo.
# Assim, apenas `capture_output` ficará acessível se outro arquivo fizer `from arquivo import *`.
__all__ = ['capture_output']
