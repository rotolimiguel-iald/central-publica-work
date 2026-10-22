# -*- coding: utf-8 -*-
"""patch de construcao (R3.4, parte 1): ../controles_negativos_r3_4.py (copia dos controles da R3.3) migrado para o estado de HOJE: a producao esta em B3/v392 e o Nos real em v393.
- os controles da familia b1 (a copia que pina o Nos REAL) passam de v391 para a versao do Nos real (VR = v393; VR_ERRADA = a seguinte); o b1 e derivado pelo montar_sandbox R3.4;
- os runs 1a (Nos real) e 1b (copia v391) usam a bateria POR VERSAO gerada por script (gerar_bateria_r3_4.py), porque o T12 da bateria R2 pina o um.py v391;
- o resto (b2, nos/, nos_v392/, decoys, kernel, eventos) e o da R3.3, byte a byte; o final confere a presenca dos 401 controles da R3.3."""
import re
import sys
sys.dont_write_bytecode = True
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "controles_negativos_r3_4.py"
t = P.read_text(encoding="utf-8")


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (t.count(old), old[:120])
    t = t.replace(old, new)


sub('"""controles_negativos_r3_3.py (R3.3, 13/10/2026) -- os 399 da R3.2', '"""controles_negativos_r3_4.py (R3.4, 19/10/2026) -- os 401 da R3.3 (nomes mantidos; os da familia b1 e os runs 1a/1b migrados para o estado de hoje: producao B3/v392, Nos real v393, '
    'bateria por versao) e os NOVOS (prefixos R34_S_ salto, R34_P_ bateria por versao, R34_M_ modulos de auditoria). Da R3.3: os 399 da R3.2', 1)
sub('"R3.3 (R31-1): rode com python -I -B -X utf8"', '"R3.4 (R31-1): rode com python -I -B -X utf8"')
sub('SBM = json.loads((RAIZ / "SANDBOX_MANIFEST_R3_2.json").read_text(encoding="utf-8"))',
    'SBM = json.loads((RAIZ / "SANDBOX_MANIFEST_R3_4.json").read_text(encoding="utf-8"))\n'
    'VR = SBM["nos_real"]["versao"]                       # R3.4: a versao do Nos REAL de hoje (v393): a familia b1 usa esta versao onde a R3.3 usava v391\n'
    'VR_ERRADA = "v%d" % (int(VR[1:]) + 1)                # uma versao que o Nos real nao tem\n'
    'R33 = AQUI.parent / "R3_3"')

# --- as baterias por versao, geradas por script, antes dos runs 1a e 1b
sub('# ================================================================ run 1a e 1b (a bateria inteira, pre_selo, ensaio)\n',
    '''# ================================================================ R3.4 (P): as baterias POR VERSAO, geradas por script (o T12 da R2 pina o um.py v391)
GEN_BAT = AQUI / "gerar_bateria_r3_4.py"
DRV_BAT = AQUI / "bateria_r3_4" / "t12_t14_atrator_r3_4.py"
PINOS_BN_REAL = WORK / "cadeia_de_selo" / VR / ("PINOS_BN_%s.json" % VR)


def gerar_bateria_r34(nome, versao, nos_dir, real=False, base=None):
    """roda gerar_bateria_r3_4.py (subprocesso, -I -B -X utf8): devolve (bateria, sha256, pino). real=True: pinos da cadeia (PINOS_BN) da versao instalada; senao, sandbox."""
    pino, saida = FX / ("PINO_UM_PY_%s.json" % nome), FX / ("BATERIA_R34_%s.json" % nome)
    base = base or BAT
    cmd = [PY, "-I", "-B", "-X", "utf8", str(GEN_BAT), "--base", str(base), "--base-sha256", sha(base), "--versao", versao, "--nos", str(nos_dir), "--driver", str(DRV_BAT),
           "--pino-saida", str(pino), "--saida", str(saida)] + (["--pinos-bn", str(PINOS_BN_REAL)] if real else ["--sandbox"])
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stdout + r.stderr
    return saida, sha(saida), pino


BAT_REAL, BAT_REAL_SHA, PINO_REAL = gerar_bateria_r34("real_" + VR, VR, NOS_REAL, real=True)
BAT_V391, BAT_V391_SHA, PINO_V391 = gerar_bateria_r34("v391_copia", "v391", NOS)

# ================================================================ run 1a e 1b (a bateria inteira, pre_selo, ensaio)
''')
sub('run("RUN_1a_pre_selo_b1_nos_real", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--modo", "ensaio", "--fase", "pre_selo"], 0,',
    'run("RUN_1a_pre_selo_b1_nos_real", ["--bancada", B1, "--versao", VR, "--bateria", BAT_REAL, "--bateria-sha256", BAT_REAL_SHA, "--modo", "ensaio", "--fase", "pre_selo"], 0,')
sub('rec["nos"]["um_py"]["sha256"] == SBM["nos"]["um_py"]["sha256"] and rec["manifesto_anterior"]["pina_o_nos_real"] is True and',
    'rec["nos"]["um_py"]["sha256"] == SBM["nos_real"]["um_py"]["sha256"] and rec["manifesto_anterior"]["pina_o_nos_real"] is True and')
sub('rec["nos"]["kernel"]["raiz_sha256"] == SBM["fx"]["kernel_v391"]["raiz_sha256"] and isolado(rec, S / "1a"))(recibo_de(j)),',
    'rec["nos"]["kernel"]["raiz_sha256"] == SBM["nos_real"]["kernel"]["raiz_sha256"] and isolado(rec, S / "1a")\n'
    '                           and rec["bateria"]["pinos_da_versao"]["conferidos_contra_o_nos_lido"] is True and rec["bateria"]["pinos_da_versao"]["versao"] == VR)(recibo_de(j)),')
sub('run("RUN_1b_pre_selo_b2_nos_copia", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--modo", "ensaio", "--fase", "pre_selo"], 0,',
    'run("RUN_1b_pre_selo_b2_nos_copia", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT_V391, "--bateria-sha256", BAT_V391_SHA, "--modo", "ensaio", "--fase", "pre_selo"], 0,')

# --- a familia b1 (o Nos real): v391 -> VR
n_b1 = len(re.findall(r'\["--bancada", (?:B1|jb1|b1x|b1t), "--versao", "v391",', t))
assert n_b1 == 12, n_b1          # B1 x7 (o RUN_1a ja foi trocado acima), jb1 x1, b1x x2, b1t x2
t = re.sub(r'\["--bancada", (B1|jb1|b1x|b1t), "--versao", "v391",', r'["--bancada", \1, "--versao", VR,', t)
sub('"\\\\\\\\?\\\\" + str(B1), "--versao", "v391",', '"\\\\\\\\?\\\\" + str(B1), "--versao", VR,')
sub('run("C1_versao_errada", ["--bancada", B1, "--versao", "v393",', 'run("C1_versao_errada", ["--bancada", B1, "--versao", VR_ERRADA,')
P.write_text(t, encoding="utf-8", newline="")
print("ok", n_b1)
