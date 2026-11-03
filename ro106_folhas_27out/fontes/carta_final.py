# -*- coding: utf-8 -*-
# Cartas FINAIS da Regra 26.4 (02/11/2026), a partir das cartas ACEITAS, por decisao do operador: as folhas nao mudam. Diferencas, e so estas:
# (1) sai a nota de minuta; (2) local e data preenchidos; (3) bloco do requerente, com a assinatura eletronica do envio pelo ePCT;
# (4) MQC, item 3(c): a frase passa a dizer o que foi medido, igual a do Aprendizado. Arquivos novos *_FINAL; as cartas aceitas ficam intactas.
import copy
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import carta

W = carta.W
DATA = 'Goiânia, 4 de novembro de 2026'
NOME = 'ROTOLI MIGUEL, Luiz Antonio — Requerente'
ELETR = 'Assinado eletronicamente no envio pelo ePCT.'
MQC = copy.deepcopy(carta.MQC)
MQC['comum_c'] = carta.APR['comum_c']


SUBS = (('a requerente apresenta', 'o requerente apresenta'), ('letras com haste com altura', 'letras com haste ascendente com altura'))  # r2: observacoes O1 e O2 da revisao


def frases(t):
    for x, y in SUBS:
        assert t.count(x) == 1, x
        t = t.replace(x, y)
    return t


def final_md(d):
    t = frases(carta.md(d))
    t, n = re.subn(r'(?m)^> \*\*Minuta preparada.*\n\n?', '', t)
    assert n == 1
    assert t.count('[local], [data]') == 1 and t.count('[ASSINATURA E IDENTIFICAÇÃO — a preencher pelo operador]') == 1
    return t.replace('[local], [data]', DATA).replace('[ASSINATURA E IDENTIFICAÇÃO — a preencher pelo operador]', NOME + '  \n' + ELETR)


def final_tex(d):
    t = frases(carta.tex(d))
    t, n = re.subn(r'(?m)^\{\\small\\itshape Minuta preparada.*\n\n', '', t)
    assert n == 1
    a = 'Termos em que, pede deferimento.\n\n' + r'\vspace{1.2cm}[ASSINATURA E IDENTIFICAÇÃO --- a preencher pelo operador]'
    b = (r'\begin{minipage}{\linewidth}Termos em que, pede deferimento.' + '\n\n' + r'\vspace{1.2cm}' + NOME.replace('—', '---') + r'\\ ' + ELETR + r'\end{minipage}')
    assert t.count('[local], [data]') == 1 and t.count(a) == 1
    return t.replace('[local], [data]', DATA).replace(a, b)


for d in (carta.APR, MQC):
    nome = d['nome'] + '_FINAL'
    alvo = W / (nome + '.pdf')
    assert not alvo.exists(), alvo
    (W / (nome + '.md')).write_text(final_md(d), encoding='utf-8')
    t = W / '_tmp' / nome
    t.mkdir(parents=True, exist_ok=True)
    (t / (nome + '.tex')).write_text(final_tex(d), encoding='utf-8')
    for _ in range(2):
        r = subprocess.run(['xelatex', '--disable-installer', '-interaction=nonstopmode', nome + '.tex'], cwd=t, capture_output=True, text=True)
    log = (t / (nome + '.log')).read_text(encoding='utf-8', errors='replace')
    erros = re.findall(r'^! .*$', log, flags=re.M)
    print(nome, 'erros TeX:', erros[:5])
    assert not erros
    shutil.copy(t / (nome + '.pdf'), alvo)
