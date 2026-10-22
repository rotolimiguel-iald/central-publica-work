# -*- coding: utf-8 -*-
"""derivar_passo10_r35.py (R3.5, 19/10/2026) -- RE-DERIVA o passo 10 (10, 10-bis-a/10a, 10-bis/10b, 10-ter/10c) do pos_rito/chain_pos_rito_v394.sh e o helper b3_recibo_v394.py pela §7 do RESULTADO_R3_4.md com a R3.5:
troca b3_prepara (pinos da R3.4/R3.5, bateria da v394 GERADA por script depois do selo, recibo do kernel R3_4), o passo 10 e o passo 10b (cadeia de selos, salto, esboco R3.5) e acrescenta um paragrafo ao cabecalho.
NAO roda derivar_cadeia_v394.py; NAO toca textos_v394.py, registrar_mapa_v394.py, fechar_v394.py; os passos 0-9, 10a, 10c, 11-14 ficam byte a byte. Backup de BYTES antes (.bak_<AAAAMMDD_HHMMSS> na mesma pasta);
escrita por temporario + os.replace. uso: python -I -B -X utf8 derivar_passo10_r35.py [--ensaio]"""
import argparse
import datetime
import hashlib
import os
import sys
sys.dont_write_bytecode = True
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
CH = AQUI.parent.parent / "cadeia_de_selo" / "v394" / "pos_rito" / "chain_pos_rito_v394.sh"
HLP = CH.with_name("b3_recibo_v394.py")
ap = argparse.ArgumentParser()
ap.add_argument("--ensaio", action="store_true")
a = ap.parse_args()
raw_ch, raw_h = CH.read_bytes(), HLP.read_bytes()
assert b"\r" not in raw_ch and b"\r" not in raw_h
t = raw_ch.decode("utf-8")
C = AQUI / "_construcao"
b_prep = (C / "bloco_b3_prepara_r35.sh.txt").read_text(encoding="utf-8")
b_10 = (C / "bloco_passo10_r35.sh.txt").read_text(encoding="utf-8")
b_10b = (C / "bloco_passo10b_r35.sh.txt").read_text(encoding="utf-8")
novo_h = (C / "b3_recibo_v394_r35.py.txt").read_text(encoding="utf-8")


def cortar(t, ini, fim, novo):
    assert t.count(ini) == 1 and t.count(fim) == 1, (ini[:60], t.count(ini), fim[:60], t.count(fim))
    i, j = t.index(ini), t.index(fim)
    assert i < j
    return t[:i] + novo + t[j:]


assert "esboco_R3_3" in t and "esboco_R3_5" not in t, "o chain ja foi re-derivado ou nao e o esperado"
t = cortar(t, "b3_prepara() {\n", "tem_pino() {", b_prep)
t = cortar(t, "if quer 10; then\n", "if quer 10a; then\n", b_10)
t = cortar(t, "if quer 10b; then\n", "if quer 10c; then\n", b_10b)
cab = ("# R3.5 (19/10/2026, depois da revisao independente EXAME_DELTA_E_R3_4.md): o PASSO 10 (10, 10a, 10b, 10c) e o helper b3_recibo_v394.py foram RE-DERIVADOS pela §7 do RESULTADO_R3_4.md com o esboco R3.5 (R3_5/_construcao/derivar_passo10_r35.py;\n"
       "# NAO se rodou derivar_cadeia_v394.py): o B(n) e' o SALTO v392 -> v394 (a Bancada de producao pina a v392; o elo da v393 nunca rodou). Os pinos vem de PINOS_BN_v394.json FUNDIDO com o que e' da R3.4/R3.5 (esboco_R3_5, cadeia_de_selos,\n"
       "# recibo_pre_selo 0d82d598 da R3.4, kernel_recibo R3_4 com modulos_de_auditoria, selo/manifesto do kernel da v393, gerador_bateria, driver_t12_t14, bateria_base_R2); a BATERIA da v394 e' GERADA por script no 10 (depois do selo; bateria por versao)\n"
       "# e pinada ao lado (bateria_pos_selo/PINOS_BATERIA_v394.json); o 10 e o 10b passam --cadeia-de-selos; o 10b exige o evento c1 que nomeia a v394. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como antes.\n")
alvo = 'PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v394"; SEL="$PK/pos_rito"\n'
assert t.count(alvo) == 1
t = t.replace(alvo, cab + alvo)
assert "esboco_R3_3" not in t.split("b3_prepara() {")[1].split("tem_pino() {")[0]
if a.ensaio:
    sys.stdout.write(t)
    sys.exit(0)
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
for p, raw in ((CH, raw_ch), (HLP, raw_h)):
    bak = p.with_name(p.name + ".bak_" + stamp)
    with open(bak, "xb") as f:
        f.write(raw)
    assert bak.read_bytes() == raw, "backup de bytes falhou: %s" % bak
    print("backup:", bak)
baks = {}
for p, raw in ((CH, raw_ch), (HLP, raw_h)):
    baks[p.name] = p.with_name(p.name + ".bak_" + stamp)
for p, novo, raw in ((CH, t.encode("utf-8"), raw_ch), (HLP, novo_h.encode("utf-8"), raw_h)):
    assert hashlib.sha256(p.read_bytes()).hexdigest() == hashlib.sha256(raw).hexdigest(), "o arquivo mudou durante a derivacao: %s" % p
    tmp = p.with_name(p.name + ".tmp_r35")
    with open(tmp, "xb") as f:
        f.write(novo)
    assert tmp.stat().st_size > 1000
    os.replace(tmp, p)
    print("escrito:", p, len(raw), "->", p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest()[:16])

import json
res = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), por="derivar_passo10_r35.py (R3.5)", chain=str(CH), chain_backup=str(baks[CH.name]), chain_sha256_antes=hashlib.sha256(raw_ch).hexdigest(),
           chain_sha256=hashlib.sha256(CH.read_bytes()).hexdigest(), helper=str(HLP), helper_backup=str(baks[HLP.name]), helper_sha256_antes=hashlib.sha256(raw_h).hexdigest(),
           helper_sha256=hashlib.sha256(HLP.read_bytes()).hexdigest(), nao_tocados=["textos_v394.py", "registrar_mapa_v394.py", "fechar_v394.py", "derivar_cadeia_v394.py"])
with open(AQUI / "evidencias" / "derivacao_passo10_r35.json", "xb") as f:
    f.write(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps(res, ensure_ascii=False))
