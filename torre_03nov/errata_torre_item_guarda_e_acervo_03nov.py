# -*- coding: utf-8 -*-
"""03/11/2026 10:3x, gerencia c1 (com o «vai» do operador para a Torre, verbatim sha16 57250bbbaca9fd39): (1) torre.py, memoria_missoes: a recusa do guarda de confidencialidade
(fonte de um registro que cita a outra casa) e' o guarda FUNCIONANDO, nao defasagem da Torre: vira INFO com a razao (errata AO LADO; o guarda nao muda); (2) build_acervo_index.py:
as duas pastas CLAUDE_memoria (Haja_Luz e Nativa) entram nas SOURCES, para que o historico movido continue indexado; (3) torre.py gerar (backup do TORRE_v406.json), quadro
remedido. Aplicado por patches.aplicar_em_arquivo (backup de bytes, py_compile). Escrito pelo Write."""
import json, shutil, subprocess, sys, time
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes"); sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import patches  # noqa: E402
PY = r"C:\Python314\python.exe"; TORRE = Path(r"C:\IALD\TORRE_IALD\torre.py"); ACV = Path(r"C:\IALD\projetos_pyhton\IALD\build_acervo_index.py"); TS = time.strftime("%Y%m%d_%H%M%S")
O1 = ('            else:\n'
      '                item("Memória ACOM", "missão %s projetável" % nome, "projeção OK", e["estado"] + " — " + str(e.get("erro"))[:100], False)\n')
N1 = ('            elif e["estado"] == "RECUSADO_PELO_GUARDA":\n'
      '                # AO LADO (03/11/2026, gerência c1, com o «vai» do operador): a recusa do guarda de confidencialidade (fonte de um registro que cita a outra casa)\n'
      '                # é o guarda FUNCIONANDO, não defasagem da Torre: fica INFO com a razão. O original (abaixo, intacto) a contava como DEFASADO. O guarda não muda.\n'
      '                #     item("Memória ACOM", "missão %s projetável" % nome, "projeção OK", e["estado"] + " — " + str(e.get("erro"))[:100], False)\n'
      '                info("Memória ACOM", "missão %s: projeção recusada pelo guarda (o guarda funcionou)" % nome, str(e.get("erro"))[:140])\n'
      '            else:\n'
      '                item("Memória ACOM", "missão %s projetável" % nome, "projeção OK", e["estado"] + " — " + str(e.get("erro"))[:100], False)\n')


def f_torre(s):
    assert s.count(O1) == 1 and "o guarda funcionou" not in s
    return s.replace(O1, N1), ["1 memoria_missoes: recusa do guarda vira INFO (ao lado)"]


r1 = patches.aplicar_em_arquivo(TORRE, f_torre, "v406_guarda_info"); print("torre.py:", json.dumps(r1, ensure_ascii=False)[:200]); assert r1["estado"] == "aplicado"
O2 = '    (r"C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um", (".md", ".tex"), False),\n'
N2 = (O2 + '    # AO LADO (03/11/2026, gerência c1): o histórico dos dois CLAUDE.md foi movido para CLAUDE_memoria (sem perda; prova em work\\torre_03nov): segue indexado\n'
      '    (r"C:\\IALD\\Artigo\\Haja_Luz\\CLAUDE_memoria", (".md",), False),\n'
      '    (r"C:\\IALD\\projetos_pyhton\\IALD\\CLAUDE_memoria", (".md",), False),\n')


def f_acv(s):
    assert s.count(O2) == 1 and "CLAUDE_memoria" not in s
    return s.replace(O2, N2), ["1 SOURCES: CLAUDE_memoria (Haja_Luz e Nativa)"]


r2 = patches.aplicar_em_arquivo(ACV, f_acv, "claude_memoria"); print("build_acervo_index.py:", json.dumps(r2, ensure_ascii=False)[:200]); assert r2["estado"] == "aplicado"
# Torre e quadro
tj = Path(r"C:\IALD\TORRE_IALD\TORRE_v406.json"); shutil.copy2(tj, tj.with_name(tj.name + ".bak_" + TS + "_c1"))
q = subprocess.run([PY, "-X", "utf8", str(TORRE), "gerar"], cwd=str(TORRE.parent), capture_output=True, timeout=600); print("torre gerar rc", q.returncode, q.stdout.decode("utf-8", "replace")[-300:].replace("\n", " | "))
q2 = subprocess.run([PY, "-X", "utf8", str(CEN / "tools" / "estado_do_organismo.py")], cwd=str(CEN), capture_output=True, timeout=600); print("quadro rc", q2.returncode)
d = json.loads((CEN / "organismo" / "ESTADO_DO_ORGANISMO.json").read_text(encoding="utf-8")); print("quadro", d.get("medido_em"), json.dumps(d.get("resumo"), ensure_ascii=False))
for i in d["itens"]:
    if i["estado"] in ("DEFASADO", "FALHA"): print("  ", i["estado"], "|", i["superficie"][:34], "|", i["item"][:72])
