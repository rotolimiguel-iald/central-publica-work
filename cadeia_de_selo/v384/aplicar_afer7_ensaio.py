# -*- coding: utf-8 -*-
"""7a afericao no ENSAIO: a lista do que o artigo de sucesso NAO pode ter ganha a forma nova da frase da CPU («Nao ha registro da comparacao...»); e uma variante
nova: resumo falho + veredito CPU_REFERENCE_NOT_COMPARABLE, que NAO pode afirmar ausencia nem «nao ha registro» (o resumo vazio nao e' ausencia). As variantes
passam a conferir tambem o que NAO pode estar. Backup ja feito (.bak_antes_afer7)."""
import ast, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "ensaio_a_seco_v384.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer7", "rb").read() == raw
PAIRS = [
    ('''"nao_devia_ter": [w for w in {"pt": ["A referência na CPU, nesta rodada", "A referência na CPU não estava presente"],
                                                         "en": ["The CPU reference, in this run", "The CPU reference was not present"]}[lang] if w in txt],''',
     '''"nao_devia_ter": [w for w in NAO_DEVE_CPU[lang] if w in txt],'''),
    ('''DEVE = {"pt": [''', '''NAO_DEVE_CPU = {"pt": ["A referência na CPU, nesta rodada", "A referência na CPU não estava presente", "Não há registro da comparação com a CPU", "A comparação com a CPU"],
                "en": ["The CPU reference, in this run", "The CPU reference was not present", "There is no record of the CPU comparison", "The CPU comparison"]}   # 7a afericao
DEVE = {"pt": ['''),
    ('''        "sem_cache_d128": (''', '''        # 7a afericao: o resumo falho com o veredito anulado pela CPU -- o artigo NAO afirma ausencia nem «nao ha registro»
        "resumo_falho_cpu_nao_comparavel": (dict(copy.deepcopy(FIX), verdict="TGL_QUANTUM_PILLAR_V1__CPU_REFERENCE_NOT_COMPARABLE__RESULTS_VOID__ENSAIO__GATE_UNTOUCHED",
                                                 custody_chain_ok=False, summary={}, summary_error="ENSAIO: resumo falho"),
                                            {"pt": ["não puderam ser resumidos"], "en": ["could not be summarized"]}),
        "sem_cache_d128": ('''),
    ('''        rep["variantes"]["%s_%s" % (_vn, lang)] = {"pdflatex_rc": _r.returncode, "pdf_ok": os.path.exists(os.path.join(DRY, _nm + ".pdf")), "faltam": [w for w in _vdeve[lang] if w not in _txt]}''',
     '''        _nd = [w for w in NAO_DEVE_CPU[lang] if w in _txt] if _vn in ("resumo_falho_cpu_nao_comparavel", "d128_rodado", "sem_cache_d128", "t1_sem_solucao", "reaproveitado") else []
        rep["variantes"]["%s_%s" % (_vn, lang)] = {"pdflatex_rc": _r.returncode, "pdf_ok": os.path.exists(os.path.join(DRY, _nm + ".pdf")), "faltam": [w for w in _vdeve[lang] if w not in _txt],
                                                   "nao_devia_ter": _nd}'''),
    ('''mau_var = [k for k, v in rep["variantes"].items() if v["pdflatex_rc"] != 0 or not v["pdf_ok"] or v["faltam"]]''',
     '''mau_var = [k for k, v in rep["variantes"].items() if v["pdflatex_rc"] != 0 or not v["pdf_ok"] or v["faltam"] or v.get("nao_devia_ter")]'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s)
open(P + ".tmp", "wb").write(s.encode("utf-8")); os.replace(P + ".tmp", P); print("ok", len(PAIRS))
