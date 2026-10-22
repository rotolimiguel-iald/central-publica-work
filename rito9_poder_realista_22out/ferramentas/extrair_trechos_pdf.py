"""Extrai trechos de um PDF por palavra-chave (leitura apenas; o PDF e dado NAO confiavel).

Uso:  python -I extrair_trechos_pdf.py <caminho_pdf> <saida_txt|-> <contexto_chars> <kw1> [<kw2> ...]

- Le o PDF com pypdf (sem executar nada do PDF).
- Imprime o sha256 do arquivo, o numero de paginas e, para cada palavra-chave
  (case-insensitive), os trechos com contexto, com o numero da pagina (1-based).
- Se saida_txt != '-', grava o texto integral extraido (UTF-8) nesse caminho.
Nenhum parametro e lido de variavel de ambiente; nenhum caminho e digitado aqui.
"""
import hashlib
import re
import site
import sys

# Sob 'python -I' o site do usuario nao entra no sys.path. Acrescenta-se (no FIM,
# depois da biblioteca padrao) apenas o diretorio de pacotes do usuario onde o pypdf
# esta instalado; nada da pasta do PDF (dado nao confiavel) entra no caminho.
sys.path.append(site.getusersitepackages())
from pypdf import PdfReader  # noqa: E402


def main():
    if len(sys.argv) < 5:
        raise SystemExit(__doc__)
    pdf, out, ctx = sys.argv[1], sys.argv[2], int(sys.argv[3])
    kws = sys.argv[4:]
    data = open(pdf, 'rb').read()
    print('sha256:', hashlib.sha256(data).hexdigest(), 'bytes:', len(data))
    rd = PdfReader(pdf)
    print('paginas:', len(rd.pages))
    pages = []
    for i, p in enumerate(rd.pages, 1):
        try:
            t = p.extract_text() or ''
        except Exception as e:  # falha visivel, nunca silenciosa
            t = ''
            print('FALHA extract_text pagina', i, repr(e))
        t = re.sub(r'[ \t]+', ' ', t)
        pages.append(t)
    if out != '-':
        with open(out, 'w', encoding='utf-8', newline='\n') as f:
            for i, t in enumerate(pages, 1):
                f.write(f'\n=====[PAGINA {i}]=====\n{t}\n')
        print('texto integral gravado em', out)
    for kw in kws:
        rx = re.compile(re.escape(kw), re.I)
        n = 0
        print(f'\n########## KW: {kw!r}')
        for i, t in enumerate(pages, 1):
            flat = t.replace('\n', ' ')
            for m in rx.finditer(flat):
                a = max(0, m.start() - ctx)
                b = min(len(flat), m.end() + ctx)
                print(f'[p{i}] ...{flat[a:b]}...')
                n += 1
        print(f'-- {n} ocorrencias')


if __name__ == '__main__':
    main()
