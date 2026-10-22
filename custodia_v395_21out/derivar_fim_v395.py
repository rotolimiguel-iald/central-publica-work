# -*- coding: utf-8 -*-
"""Deriva conferencia_final_v395.py e registro_v395_publicada.py dos da v394, por trocas contadas (21/10/2026, sessão a7)."""
from pathlib import Path

A = Path(r"C:\IALD\Central de Patentes\work\custodia_v394_19out")
B = Path(r"C:\IALD\Central de Patentes\work\custodia_v395_21out")


def derivar(orig, novo, trocas):
    s = (A / orig).read_text(encoding="utf-8")
    for a, b, n in trocas:
        c = s.count(a)
        assert c == n, (novo, a[:90], c, n)
        s = s.replace(a, b)
    compile(s, novo, "exec")
    (B / novo).write_text(s, encoding="utf-8")
    print("ok", novo, len(s))


derivar("conferencia_final_v394.py", "conferencia_final_v395.py", [
    ('"""CONFERÊNCIA FINAL INDEPENDENTE da custódia v393+v394 (19/10/2026, sessão a7).', '"""CONFERÊNCIA FINAL INDEPENDENTE da custódia v395 (21/10/2026, sessão a7; molde: a da v394).', 1),
    ('um.py v394 = o pino', 'um.py v395 = o pino', 1),
    ('o cofre um_unificado_v394:', 'o cofre um_unificado_v395:', 1),
    ('o cofre tgl_kernel_v394: cada arquivo formal do manifesto de prova bate (1423)', 'o cofre tgl_kernel_v395: cada arquivo formal do manifesto de prova bate (1424)', 1),
    ('o index traz «v394 · <pin16>»', 'o index traz «v395 · <pin16>»', 1),
    ('V, KV = CEN / "vault" / "originals_copy" / "um_unificado_v394", CEN / "vault" / "originals_copy" / "tgl_kernel_v394"',
     'V, KV = CEN / "vault" / "originals_copy" / "um_unificado_v395", CEN / "vault" / "originals_copy" / "tgl_kernel_v395"', 1),
    ('"User-Agent": "conferencia-final-v394"', '"User-Agent": "conferencia-final-v395"', 1),
    ('item("1 selo do Nós = v394 e o pino", selo.get("um_version") == "v394" and sha(b_nos) == pin, p16)',
     'item("1 selo do Nós = v395 e o pino", selo.get("um_version") == "v395" and sha(b_nos) == pin, p16)', 1),
    ('item("2 cofre v394: artefatos do selo presentes conferem"', 'item("2 cofre v395: artefatos do selo presentes conferem"', 1),
    ('item("3 cofre do kernel: arquivos formais conferem", len(ff) == 1423 and not kdiv,', 'item("3 cofre do kernel: arquivos formais conferem", len(ff) == 1424 and not kdiv,', 1),
    ('item("3 axiom_report no trio", len(pm["axiom_report"]) == 29026 and not fora,', 'item("3 axiom_report no trio", len(pm["axiom_report"]) == 29159 and not fora,', 1),
    ('item("5 site no ar: index com «v394 · pin16»", ("v394 \\u00b7 " + p16) in si)', 'item("5 site no ar: index com «v395 · pin16»", ("v395 \\u00b7 " + p16) in si)', 1),
    ('["vault/originals_copy/um_unificado_v394", "vault/originals_copy/tgl_kernel_v394", "fronteira_tgl",',
     '["vault/originals_copy/um_unificado_v395", "vault/originals_copy/tgl_kernel_v395", "fronteira_tgl",', 1),
    ('"patents/_formula_completa", "memory/TGL_ATLAS.md", "andamentos/marcos_fixos.json", "tools/patent_monitor.py"])):',
     '"patents/_formula_completa", "memory/TGL_ATLAS.md"])):', 1),
    ('out = CEN / "work" / "custodia_v394_19out" / "CONFERENCIA_FINAL_v394.json"', 'out = CEN / "work" / "custodia_v395_21out" / "CONFERENCIA_FINAL_v395.json"', 1),
])

derivar("registro_v394_publicada.py", "registro_v395_publicada.py", [
    ('"""Pós-push da custódia v393+v394 (19/10/2026, sessão a7)', '"""Pós-push da custódia v395 (21/10/2026, sessão a7; molde: o da v394)', 1),
    ('W = r"C:\\IALD\\Central de Patentes\\work\\custodia_v394_19out"', 'W = r"C:\\IALD\\Central de Patentes\\work\\custodia_v395_21out"', 1),
    ('cf = json.load(open(os.path.join(W, "CONFERENCIA_FINAL_v394.json"), encoding="utf-8"))', 'cf = json.load(open(os.path.join(W, "CONFERENCIA_FINAL_v395.json"), encoding="utf-8"))', 1),
    ('"(`work/custodia_v394_19out/conferencia_final_v394.py`, sem importar a esteira): **%d/%d ok** — o um.py igual no Nós, no espelho, no cofre e no "',
     '"(`work/custodia_v395_21out/conferencia_final_v395.py`, sem importar a esteira): **%d/%d ok** — o um.py igual no Nós, no espelho, no cofre e no "', 1),
    ('"raw do GitHub (o pino); o cofre e o kernel (1423 formais; 29026 declarações no trio) conferem; o site no ar e o README raw trazem o pino; "',
     '"raw do GitHub (o pino); o cofre e o kernel (1424 formais; 29159 declarações no trio) conferem; o site no ar e o README raw trazem o pino; "', 1),
    ('"os dois repositórios sem nada pendente nos caminhos da custódia. PCT: o Codex ficou sem créditos; a Central fechou os controles da ENTREGA_009 "\n'
     '       "(26/11 nos marcos; auditoria +2 processos; anuidade 6 meses; REVISAO_012). O gate não se moveu." % (esp, cen, cf["ok"], cf["total"]))',
     '"os dois repositórios sem nada pendente nos caminhos da custódia. [LEGAL] a paridade do ACOM Mirror segue decisão do operador. O gate não se moveu."\n'
     '       % (esp, cen, cf["ok"], cf["total"]))', 1),
    ('ap(os.path.join(MEM, "handoff-v394-custodia.md"), "## %s — PUBLICADA (pós-push)\\n\\n%s" % (AGORA, TXT))',
     'ap(os.path.join(MEM, "handoff-v395-custodia.md"), "## %s — PUBLICADA (pós-push)\\n\\n%s" % (AGORA, TXT))', 1),
    ('ap(os.path.join(MEM, "central-de-patentes-estado.md"), "## %s — custódia v394 publicada\\n\\n%s" % (AGORA, TXT))',
     'ap(os.path.join(MEM, "central-de-patentes-estado.md"), "## %s — custódia v395 publicada\\n\\n%s" % (AGORA, TXT))', 1),
    ('ap(r"C:\\IALD\\Site\\tgl\\v3.0_bancada\\DIARIO_DO_SITE.md", "## %s — a custódia v393+v394 PUBLICADA\\n\\n%s" % (AGORA, TXT))',
     'ap(r"C:\\IALD\\Site\\tgl\\v3.0_bancada\\DIARIO_DO_SITE.md", "## %s — a custódia v395 PUBLICADA\\n\\n%s" % (AGORA, TXT))', 1),
    ('old = [l for l in t.split(nl) if l.startswith("- [HANDOFF v394 — o relógio M2, a rede de Fock e as cunhagens; custódia](handoff-v394-custodia.md)")]',
     'old = [l for l in t.split(nl) if l.startswith("- [HANDOFF v395 — o modo psiônico na fractalização do Um; custódia](handoff-v395-custodia.md)")]', 1),
    ('nova = ("- [HANDOFF v394 — o relógio M2, a rede de Fock e as cunhagens; custódia](handoff-v394-custodia.md) — **19/10: PUBLICADA com a v393** "\n'
     '        "(the_boundary `%s`; Central `%s`; site no ar; cofre v394, runner v59, 16/16, FINAL, ledger 0; conferência final %d/%d) · `972e81f22dd8cc68`"',
     'nova = ("- [HANDOFF v395 — o modo psiônico na fractalização do Um; custódia](handoff-v395-custodia.md) — **21/10: PUBLICADA** "\n'
     '        "(the_boundary `%s`; Central `%s`; site no ar; cofre v395, runner v60, 16/16, FINAL, ledger 0; conferência final %d/%d) · `8918b17803792cf2`"', 1),
])
