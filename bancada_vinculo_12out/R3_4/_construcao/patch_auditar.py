# -*- coding: utf-8 -*-
"""patch de construcao (R3.4): substitui, em ../sincronizar_bancada.py, a funcao auditar_fonte_de_auditoria (a 1a versao saiu com barras invertidas colapsadas por um heredoc)."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "sincronizar_bancada.py"
t = P.read_text(encoding="utf-8")
i = t.index("def auditar_fonte_de_auditoria(texto):")
j = t.index("CRITERIOS_TIPOS = dict(j1_declaracoes=int,")
NOVA = r'''def auditar_fonte_de_auditoria(texto):
    """R3.4 (M): a fonte de um modulo de auditoria (listado em modulos_de_auditoria do recibo do kernel) so pode ter comandos de auditoria: `import X`, `open X in`,
    `#print axioms X` e `run_cmd` (com o corpo indentado). Linha de topo de outra forma, indentada fora de um corpo de run_cmd, comentario de bloco, caractere de
    controle ou de formato, ou, no corpo, qualquer palavra da lista fechada RE_AUD_PROIBIDO (declaracao, escrita de ambiente, processo/arquivo, sorry): recusa.
    Exige ao menos um #print ou run_cmd (um modulo listado que nao audita nada e recusado). Devolve dict(ok, motivo, contagem). O corpo do run_cmd e codigo
    executado na compilacao: este script confere comandos de topo e a lista fechada; NAO prova a inocuidade semantica do corpo (residuo declarado)."""
    cont = dict(import_=0, open_=0, print_axioms=0, run_cmd=0, corpo=0, comentario=0, branco=0)
    for ch in texto:
        cat = unicodedata.category(ch)
        if (cat == "Cc" and ch not in "\n\r\t") or cat == "Cf":
            return dict(ok=False, motivo="caractere de controle ou de formato U+%04X" % ord(ch), contagem=cont)
    if "/-" in texto:
        return dict(ok=False, motivo="comentario de bloco (/-) nao se admite", contagem=cont)
    corpo = False
    for i, linha in enumerate(texto.replace("\r\n", "\n").replace("\r", "\n").split("\n"), 1):
        l_ = linha.rstrip(" \t")
        if not l_.strip():
            cont["branco"] += 1
            continue
        if l_.lstrip().startswith("--"):
            cont["comentario"] += 1
            continue
        if l_[0] in " \t":
            if not corpo:
                return dict(ok=False, motivo="l.%d: linha indentada fora de um corpo de run_cmd: %r" % (i, l_[:60]), contagem=cont)
            m = RE_AUD_PROIBIDO.search(l_)
            if m:
                return dict(ok=False, motivo="l.%d: palavra proibida no corpo do run_cmd: %r" % (i, m.group(0)), contagem=cont)
            cont["corpo"] += 1
            continue
        corpo = False
        if RE_AUD_IMPORT.match(l_):
            cont["import_"] += 1
        elif RE_AUD_OPEN.match(l_):
            cont["open_"] += 1
        elif RE_AUD_PRINT.match(l_):
            cont["print_axioms"] += 1
        elif RE_AUD_RUNCMD.match(l_):
            cont["run_cmd"] += 1
            corpo = True
        else:
            return dict(ok=False, motivo="l.%d: comando de topo fora da lista (import, open, #print axioms, run_cmd): %r" % (i, l_[:60]), contagem=cont)
    if cont["print_axioms"] + cont["run_cmd"] == 0:
        return dict(ok=False, motivo="nenhum #print axioms nem run_cmd: o modulo listado nao audita nada", contagem=cont)
    return dict(ok=True, motivo=None, contagem=cont)


'''
t = t[:i] + NOVA + t[j:]
P.write_text(t, encoding="utf-8", newline="")
print("ok")
