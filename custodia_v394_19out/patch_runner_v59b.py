# -*- coding: utf-8 -*-
"""Runner da Fronteira v59b (custódia v394, 19/10/2026, sessão a7): ERRATA AO LADO nas pedras v48-v53 (arco v369-v375, o todo e um v376,
lei da dissipação v377, lei com contraste v378, razão elementar v379, fases 5-6-7 v380). Elas liam o cofre CORRENTE (CUSTODY_DIR) e,
pelas erratas v49/v50, aceitavam o registro crescer desde que nenhum veredito antigo mudasse. A v394 mudou um veredito antigo de forma
DECLARADA (o índice da IALD, `the_iald_index`, passa a THE_IALD_INDEX_QUALIFIED_COMPILER_PROVENANCE_VERIFIED — handoff v394, mudança não
numérica), e as famílias de bandeiras do arco v369-v375 cresceram. A correção é a lição da v55-v58: cada pedra lê o PRÓPRIO cofre pelo
nome (um_unificado_v375 ... v380), exata para sempre; o que vale no cofre corrente é medido pela pedra da versão corrente (v43)."""
import os, subprocess, sys
from datetime import datetime
R = r"C:\IALD\Central de Patentes\fronteira_tgl\runner\one_fronteira.py"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(R, "rb").read(); s = raw.decode("utf-8"); nl = "\r\n" if "\r\n" in s else "\n"
if "ERRATA v394 (runner v59b" in s: raise SystemExit("ja aplicado")
open(R + ".bak_v59b_" + TS, "wb").write(raw)

PEDRAS = (("_medir_v375_arco_v369_v375", "v375", "v368"), ("_medir_v376_o_todo_e_um", "v376", "v375"),
          ("_medir_v377_lei_da_dissipacao", "v377", "v376"), ("_medir_v378_lei_com_contraste", "v378", "v377"),
          ("_medir_v379_razao_elementar", "v379", "v378"), ("_medir_v380_fases_5_6_7", "v380", "v379"))
for fn, ver, ant in PEDRAS:
    i = s.index("def %s():" % fn)
    j = s.index("\ndef ", i + 10)
    corpo = s[i:j]
    velho = ('''        can = json.loads((CUSTODY_DIR / "um_absoluto.json").read_text(encoding="utf-8"))
        sl = json.loads((CUSTODY_DIR / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        mf = json.loads((CUSTODY_DIR / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
        pt = (CUSTODY_DIR / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        en = (CUSTODY_DIR / "um_absoluto_en.txt").read_text(encoding="utf-8", errors="replace")
        ant = CUSTODY_DIR.parent / ("um_unificado_" + "%s")
''' % ant).replace("\n", nl)
    novo = ('''        # ERRATA v394 (runner v59b, AO LADO): as cinco leituras abaixo eram do cofre CORRENTE (CUSTODY_DIR); a v394 mudou um veredito
        # antigo de forma declarada (the_iald_index) e o cofre corrente deixou de ser o lugar do que esta pedra afirma. Ela afirma a %s
        # contra a %s: le-se o COFRE %s pelo nome (estavel para sempre); o cofre corrente e' medido pela pedra da versao corrente.
        _c%s = CUSTODY_DIR.parent / ("um_unificado_" + "%s")
        can = json.loads((_c%s / "um_absoluto.json").read_text(encoding="utf-8"))
        sl = json.loads((_c%s / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        mf = json.loads((_c%s / "tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
        pt = (_c%s / "um_absoluto_pt.txt").read_text(encoding="utf-8", errors="replace")
        en = (_c%s / "um_absoluto_en.txt").read_text(encoding="utf-8", errors="replace")
        ant = CUSTODY_DIR.parent / ("um_unificado_" + "%s")
''' % (ver, ant, ver, ver[1:], ver, ver[1:], ver[1:], ver[1:], ver[1:], ver[1:], ant)).replace("\n", nl)
    assert corpo.count(velho) == 1, (fn, corpo.count(velho))
    s = s[:i] + corpo.replace(velho, novo) + s[j:]
    print("  ok  errata %s: le o cofre %s" % (fn, ver))
tmp = R + ".tmp_v59b"; open(tmp, "wb").write(s.encode("utf-8"))
r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
if r.returncode != 0:
    os.remove(tmp); raise SystemExit("SINTAXE INVALIDA — nada trocado:\n" + (r.stderr or "")[:1500])
os.replace(tmp, R); print("runner v59b: %d -> %d bytes | py_compile OK | backup .bak_v59b_%s" % (len(raw), os.path.getsize(R), TS))
