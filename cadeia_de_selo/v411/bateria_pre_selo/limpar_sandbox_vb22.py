# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] apaga so' C:\t\vb22 depois de provar que nao ha juncao nem link (nao depende de versao); o recibo da limpeza em OUTB (no ensaio do topo proposto, a pasta de ensaio)
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] apaga so' C:\t\vb21 depois de provar que nao ha juncao nem link; nao depende de versao; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v410 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos; na v411, adaptado em 12/11/2026 pelo fork B do claude-construtor-v411, retomada) molde v410/bateria_pre_selo/limpar_sandbox_vb22.py (rotulos subidos por _bump_copia_v411.py; diff em bump/); conferido em 04/11/2026: o corpo nao depende de modulos nem de versao: apaga so' C:\t\vb22, depois de provar que nao ha juncao nem link
"""limpar_sandbox_vb22.py -- apaga o sandbox curto C:\\t\\vb22 (so' o que a preparacao da v411 criou: fotografias, copias adulteradas do conferidor, scripts de leitura), DEPOIS de provar
que nao ha juncao nem link simbolico dentro dele (um rmtree seguiria uma juncao para fora). Confere que a pasta-mae C:\\t nao perde nenhum outro filho. Grava LIMPEZA_SANDBOX_vb22.json ao lado.
Recusa (SystemExit) se o caminho nao for exatamente C:\\t\\vb22, se achar qualquer juncao/link, ou se a pasta-mae mudar. uso: python -I -B -X utf8 limpar_sandbox_vb22.py"""
import json
import os
import shutil
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
def _saida_pre_selo():
    """(v411) onde a bateria grava: no ensaio do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1, lido pelo delta_v411) a pasta de ensaio, fora de work; no real, esta pasta e v411\\ (como na v410)."""
    import importlib.util as _u
    _s = _u.spec_from_file_location("delta_v411_pre_selo", os.path.join(V, "delta_v411.py")); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
    return (os.path.join(_m.SAIDA, "bateria_pre_selo") if _m.ENSAIO_TOPO_PROPOSTO else HERE), _m.SAIDA, _m


OUTB, OUTV, _DLM = _saida_pre_selo()
os.makedirs(OUTB, exist_ok=True)
ALVO = os.path.join("C:" + os.sep, "t", "vb22")
PAI = os.path.dirname(ALVO)
assert ALVO == r"C:\t\vb22", ALVO
dest = os.path.join(OUTB, "LIMPEZA_SANDBOX_vb22.json")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
if not os.path.isdir(ALVO):
    raise SystemExit("o sandbox nao existe: " + ALVO)
irmaos_antes = sorted(x for x in os.listdir(PAI) if x != "vb22")
n_arq = n_dir = n_bytes = 0
reparse = []
pilha = [ALVO]
while pilha:
    p = pilha.pop()
    with os.scandir(p) as it:
        for e in it:
            if e.is_junction() or e.is_symlink():
                reparse.append(e.path)
                continue
            if e.is_dir(follow_symlinks=False):
                n_dir += 1
                pilha.append(e.path)
            else:
                n_arq += 1
                n_bytes += e.stat(follow_symlinks=False).st_size
if reparse:
    raise SystemExit("juncao ou link dentro do sandbox, nao apago: %r" % reparse)
shutil.rmtree(ALVO)
irmaos_depois = sorted(x for x in os.listdir(PAI) if x != "vb22")
rec = {"contrato": "LIMPEZA_SANDBOX_vb22", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "alvo": ALVO, "arquivos": n_arq, "pastas": n_dir, "bytes": n_bytes, "juncoes_ou_links_antes_de_apagar": len(reparse),
       "existe_depois": os.path.exists(ALVO), "irmaos_de_C_t_antes": len(irmaos_antes), "irmaos_de_C_t_depois": len(irmaos_depois), "irmaos_iguais": irmaos_antes == irmaos_depois,
       "nota": "as fotografias e as listas que valem como prova estao copiadas em %s (gerar_pino_recibo_pre_selo_v411.py); o resto do sandbox era descartavel" % os.path.join(OUTB, "prova_producao"), **_DLM.MARCA_ENSAIO}
assert rec["existe_depois"] is False and rec["irmaos_iguais"] is True
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print(json.dumps(rec, ensure_ascii=False))
