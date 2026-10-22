# -*- coding: utf-8 -*-
"""controles_negativos.py -- prova que o sincronizar_bancada.py FALHA FECHADO (cada recusa esperada acontece e nada e gravado na Bancada-copia).
Roda so no sandbox; a producao e nomeada uma vez (C6) apenas para mostrar a guarda, que recusa ANTES de ler qualquer byte dela."""
import hashlib, json, subprocess, sys, datetime, shutil
from pathlib import Path
AQUI = Path(__file__).resolve().parent
SB = AQUI / "sandbox"
OUT = SB / "controles_negativos"
PY = sys.executable
SYNC = AQUI / "sincronizar_bancada.py"
BAT = AQUI / "BATERIA_VINCULO.json"
COPIA = SB / "bancada_copia"
NSIN = SB / "nos_sintetico"
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(nome, args, esperado_rc, esperado_recusa=None):
    saida = OUT / nome
    cmd = [PY, "-B", "-X", "utf8", str(SYNC), "--saida", str(saida), "--bateria", str(BAT)] + args
    antes = sha(COPIA / "canonical_contracts.json")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    depois = sha(COPIA / "canonical_contracts.json")
    ult = (r.stdout.strip().splitlines() or [""])[-1]
    try:
        j = json.loads(ult)
    except ValueError:
        j = dict(veredito=None, recusa=None, bruto=ult[:400], stderr=r.stderr[-800:])
    ok = (r.returncode == esperado_rc) and (esperado_recusa is None or str(j.get("recusa") or "").startswith(esperado_recusa)) and antes == depois
    return dict(controle=nome, comando=cmd[5:], rc=r.returncode, rc_esperado=esperado_rc, recusa=j.get("recusa"), recusa_esperada=esperado_recusa,
                veredito=j.get("veredito"), manifesto_da_copia_intocado=(antes == depois), passa=ok)


OUT.mkdir(parents=True, exist_ok=False)
res = []
# C1: a versao alvo nao e a do selo
res.append(run("C1_versao_errada", ["--bancada", str(COPIA), "--versao", "v393", "--sem-bateria"], 2, "SELO_VERSAO_DIFERENTE"))
# C2: deriva de CODIGO numa copia da Bancada (um byte de motor.py trocado): nao e sincronizacao
drift = SB / "bancada_copia_drift"
shutil.copytree(COPIA, drift)
p = drift / "bancada" / "motor.py"
b = p.read_bytes()
p.write_bytes(b[:-1] + bytes([b[-1] ^ 1]))
res.append(run("C2_code_drift", ["--bancada", str(drift), "--versao", "v392", "--nos", str(NSIN), "--sandbox", "--sem-bateria"], 2, "CODE_DRIFT_NAO_E_SINCRONIZACAO"))
shutil.rmtree(drift)
# C3: aplicar sem evento c1
res.append(run("C3_aplicar_sem_evento", ["--bancada", str(COPIA), "--versao", "v392", "--nos", str(NSIN), "--sandbox", "--modo", "aplicar"], 2, "EVENTO_C1_AUSENTE"))
# C4: aplicar com um evento real do quadro que NAO nomeia a gravacao (seq 1); o recibo pre-selo do run 1 e passado para que a recusa
# chegue a porta do evento (sem ele, a porta anterior RECIBO_PRE_SELO_AUSENTE ja recusa -- tambem fail-closed, mas nao e o que C4 testa)
R1 = sorted((SB / "saida_1_pre_selo_v391").glob("RECIBO_SINCRONIZACAO_*.json"))[-1]
res.append(run("C4_evento_nao_nomeia", ["--bancada", str(COPIA), "--versao", "v392", "--nos", str(NSIN), "--modo", "aplicar", "--evento", "1", "--recibo-pre-selo", str(R1)], 2, "EVENTO_"))
# C5: Nos fora do caminho pinado SEM --sandbox
res.append(run("C5_nos_diferente_sem_sandbox", ["--bancada", str(COPIA), "--versao", "v392", "--nos", str(NSIN), "--sem-bateria"], 2, "NOS_DIFERENTE_DO_PINADO"))
# C6: a producao sem --producao (a guarda recusa antes de ler qualquer byte da producao)
res.append(run("C6_producao_sem_flag", ["--bancada", r"C:\IALD\Bancada_Um", "--versao", "v391", "--sem-bateria"], 2, "PRODUCAO_SEM_FLAG"))
# C7: bateria com um teste que FALHA, em modo aplicar com evento sandbox: nada se grava
bat_falha = OUT / "BATERIA_FALHA.json"
bj = json.loads(BAT.read_bytes())
bj["testes"] = [dict(id="T00_FALHA_INJETADA", teste="controle: um teste que falha de proposito", fontes=[], comando=["{py}", "-c", "import sys; print('falha injetada'); sys.exit(1)"],
                     cwd="{raiz}", verificacao=dict(tipo="exit0"), fases=["pre_selo", "pos_selo"], obrigatorio_em=["ensaio", "aplicar"], timeout_s=60)]
bj["copias"] = []
bat_falha.write_text(json.dumps(bj), encoding="utf-8")
saida = OUT / "C7_bateria_falha"
cmd = [PY, "-B", "-X", "utf8", str(SYNC), "--saida", str(saida), "--bateria", str(bat_falha), "--bancada", str(COPIA), "--versao", "v392", "--nos", str(NSIN),
       "--sandbox", "--modo", "aplicar", "--evento", "SANDBOX:controle C7"]
antes = sha(COPIA / "canonical_contracts.json")
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
depois = sha(COPIA / "canonical_contracts.json")
j = json.loads((r.stdout.strip().splitlines() or ["{}"])[-1])
res.append(dict(controle="C7_bateria_falha_em_aplicar", comando=cmd[5:], rc=r.returncode, rc_esperado=3, veredito=j.get("veredito"), recusa=j.get("recusa"),
                manifesto_da_copia_intocado=(antes == depois), contrato_B3_nao_gravado=not (COPIA / "CONTRATO_CANONICO_B3.md").exists(),
                passa=(r.returncode == 3 and antes == depois and "BATERIA_FALHOU" in str(j.get("veredito")) and not (COPIA / "CONTRATO_CANONICO_B3.md").exists())))
out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), script_sha256=sha(SYNC), n=len(res), passam=sum(1 for x in res if x["passa"]), controles=res,
           veredito=("TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO" if all(x["passa"] for x in res) else "ALGUM_CONTROLE_NAO_RECUSOU"))
(OUT / "CONTROLES_NEGATIVOS.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for x in res:
    print(("PASSA" if x["passa"] else "FALHA"), x["controle"], "rc=%s" % x["rc"], x.get("recusa") or x.get("veredito"))
print(out["veredito"])
