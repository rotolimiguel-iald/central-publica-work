# -*- coding: utf-8 -*-
"""limpar_sandbox_vb16.py -- apaga o sandbox curto C:\\t\\vb16 (so' o que a preparacao da v399 criou: fotografias, copias adulteradas do conferidor, scripts de leitura), DEPOIS de provar
que nao ha juncao nem link simbolico dentro dele (um rmtree seguiria uma juncao para fora). Confere que a pasta-mae C:\\t nao perde nenhum outro filho. Grava LIMPEZA_SANDBOX_vb16.json ao lado.
Recusa (SystemExit) se o caminho nao for exatamente C:\\t\\vb16, se achar qualquer juncao/link, ou se a pasta-mae mudar. uso: python -I -B -X utf8 limpar_sandbox_vb16.py"""
import json
import os
import shutil
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join("C:" + os.sep, "t", "vb16")
PAI = os.path.dirname(ALVO)
assert ALVO == r"C:\t\vb16", ALVO
dest = os.path.join(HERE, "LIMPEZA_SANDBOX_vb16.json")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
if not os.path.isdir(ALVO):
    raise SystemExit("o sandbox nao existe: " + ALVO)
irmaos_antes = sorted(x for x in os.listdir(PAI) if x != "vb16")
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
irmaos_depois = sorted(x for x in os.listdir(PAI) if x != "vb16")
rec = {"contrato": "LIMPEZA_SANDBOX_vb16", "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "alvo": ALVO, "arquivos": n_arq, "pastas": n_dir, "bytes": n_bytes, "juncoes_ou_links_antes_de_apagar": len(reparse),
       "existe_depois": os.path.exists(ALVO), "irmaos_de_C_t_antes": len(irmaos_antes), "irmaos_de_C_t_depois": len(irmaos_depois), "irmaos_iguais": irmaos_antes == irmaos_depois,
       "nota": "as fotografias e as listas que valem como prova estao copiadas em v399\\bateria_pre_selo\\prova_producao\\ (gerar_pino_recibo_pre_selo_v399.py); o resto do sandbox era descartavel"}
assert rec["existe_depois"] is False and rec["irmaos_iguais"] is True
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print(json.dumps(rec, ensure_ascii=False))
