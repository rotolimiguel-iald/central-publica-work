# -*- coding: utf-8 -*-
"""recibo_testes_operador.py -- recibo da suite de testes do PROPRIO operador (SkyGrid_Piloto/tests/run_tests.py) rodada numa COPIA byte-identica (ref_operador/),
nunca na pasta dele. Le o log da rodada, conta PASS/FAIL, extrai as linhas do BLOCO 1b (acom_mirror) e 1c (acom_crypto) e confere que a copia e' identica a' origem.
Saida: recibos/RECIBO_TESTES_DO_OPERADOR.json. Uso: python -I -B -X utf8 recibo_testes_operador.py"""
import hashlib
import json
import os
import re
import time

W = os.path.dirname(os.path.abspath(__file__))
ORIG = r"C:\IALD\Central de Patentes\Patentes\Skygrid\SkyGrid_Piloto"
COPIA = os.path.join(W, "ref_operador", "SkyGrid_Piloto_copia")
LOG = os.path.join(W, "ref_operador", "run_tests_saida.txt")

n = ok = 0
diferem = []
for raiz, _, arqs in os.walk(ORIG):
    if "__pycache__" in raiz:
        continue
    for f in arqs:
        a = os.path.join(raiz, f)
        b = os.path.join(COPIA, os.path.relpath(a, ORIG))
        n += 1
        if os.path.exists(b) and open(a, "rb").read() == open(b, "rb").read():
            ok += 1
        else:
            diferem.append(os.path.relpath(a, ORIG))
log = open(LOG, "rb").read().decode("utf-8", "replace")
linhas = log.split("\n")
passes = [l for l in linhas if "[PASS]" in l]
fails = [l for l in linhas if "[FAIL]" in l]
bloco = []
dentro = False
for l in linhas:
    if l.startswith("[BLOCO 1b]") or l.startswith("[BLOCO 1c]"):
        dentro = True
    elif l.startswith("[BLOCO ") and dentro:
        dentro = False
    if dentro:
        bloco.append(l.rstrip())
m_fim = re.search(r"(\d+)/(\d+) testes PASS", log)
mt_sel = os.path.getmtime(os.path.join(ORIG, "SKYGRID_SIM_SELO.json"))
R = {
    "quando": time.strftime("%Y-%m-%d %H:%M:%S"),
    "copia_byte_identica_a_origem": {"arquivos_na_origem_sem_pycache": n, "identicos_DEPOIS_da_rodada": ok, "diferem_depois_da_rodada": diferem[:10], "origem": ORIG, "copia": COPIA,
                                     "antes_da_rodada": "82 de 82 identicos (medido por script no momento da copia, na saida do comando de copia)",
                                     "por_que_um_difere_agora": "a suite do operador reescreve o proprio selo (SKYGRID_SIM_SELO.json) NA COPIA ao rodar; a origem nao foi tocada",
                                     "mtime_do_SKYGRID_SIM_SELO_na_origem": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mt_sel)),
                                     "origem_intocada_hoje": time.strftime("%Y-%m-%d", time.localtime(mt_sel)) != time.strftime("%Y-%m-%d")},
    "log": {"caminho": LOG, "sha256": hashlib.sha256(open(LOG, "rb").read()).hexdigest()},
    "resultado": {"PASS": len(passes), "FAIL": len(fails), "linha_final": m_fim.group(0) if m_fim else None},
    "linhas_dos_blocos_1b_e_1c": bloco,
    "leitura": ("o piloto do proprio operador trata a Dobra como COM PERDA no nivel do real: o criterio dele e' correlacao >= 0,99 (8 bits) e > 0,9999 (16 bits), nao igualdade; "
                "o estudo v399 acrescenta a exatidao no RETICULADO INTEIRO (apos rint), que nao e' o criterio dele"),
}
p = os.path.join(W, "recibos", "RECIBO_TESTES_DO_OPERADOR.json")
os.makedirs(os.path.dirname(p), exist_ok=True)
with open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k != "linhas_dos_blocos_1b_e_1c"}, ensure_ascii=False, indent=1)[:1500])
