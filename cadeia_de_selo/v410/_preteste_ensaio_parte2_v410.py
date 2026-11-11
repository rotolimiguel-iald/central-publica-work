# -*- coding: utf-8 -*-
"""_preteste_ensaio_parte2_v410.py -- PRE-TESTE PARCIAL do ensaio a seco adaptado a parte 2 (D80 a D87), ANTES da cadeia inteira (que roda UMA vez): executa o PROPRIO texto do ensaio_a_seco_v410.py do comeco ate' o fim do bloco (6p-d)
(o kernel pelo verify com o lake simulado, os vizinhos, o fluxo, a ordem de chamada, os registros com funcao e os controles negativos), numa pasta dry_pre410 propria, e depois so' o que e' NOVO no artigo: um pdflatex (uma passada) do artigo PT e EN
(os titulos e subtitulos novos, o indice, nenhum n/d na secao nova) e as variantes em que faltam o a_escala, o recibo HMS/13 e todos os registros da v410 (as frases de guarda), mais as quatro linhas do .md.
NAO e' o ensaio a seco (nao grava ensaio_a_seco_v410.json, nao roda simular_arvore, exame_pontos nem as guardas da Bancada) e NAO e' o rito. Grava PRETESTE_ENSAIO_PARTE2_v410.json.   uso: python -B -X utf8 _preteste_ensaio_parte2_v410.py"""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); ENS = os.path.join(HERE, "ensaio_a_seco_v410.py"); T0 = time.time()
src = open(ENS, encoding="utf-8").read()
i8 = src.index("# (8) o artigo\n"); iq = src.index('rep["quadro"] = {}\n'); i9 = src.index("# (9) md e manifesto\n"); i9b = src.index('rep["quadro"]["md"] = ')
p1 = src[:i8]; p8 = src[i8:iq]; p9 = src[i9:i9b]
sys.argv = [ENS, "um_v410_candidato.py", "pre410"]
g = {"__name__": "__preteste__", "__file__": ENS}
J = {"contrato": "PRETESTE_ENSAIO_PARTE2_v410", "nota": "pre-teste PARCIAL dos blocos novos do ensaio; nao e' o ensaio a seco nem o rito", "ensaio_sha16": __import__("hashlib").sha256(open(ENS, "rb").read()).hexdigest()[:16]}


def grava(ok):
    J["ok"] = bool(ok); J["segundos"] = round(time.time() - T0, 1)
    p = os.path.join(HERE, "PRETESTE_ENSAIO_PARTE2_v410.json"); open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(J, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)


try:
    exec(compile(p1, ENS, "exec"), g)
except SystemExit as e:
    J["erro"] = "o ensaio saiu antes do bloco (8): %r" % (e,); grava(False); raise
except BaseException as e:   # noqa: BLE001
    import traceback
    J["erro"] = traceback.format_exc()[-3000:]; grava(False); print(J["erro"]); sys.exit(2)
U = g["U"]; rep = g["rep"]
J["candidato_sha16"] = rep.get("sha16"); J["unidade_falsas"] = sorted(k for k, v in U.items() if not v); J["unidade_n"] = len(U); J["fluxo_ok"] = bool(g.get("mf_ok")); J["vizinhos_ok"] = bool(g.get("viz_ok")); J["fluxo_erro"] = (rep.get("mainflow") or {}).get("erro"); J["chaves_novas"] = (rep.get("mainflow") or {}).get("chaves_novas")
J["partes_falsas"] = {k: [a for a, b in (rep.get(k) or {}).items() if not b] for k in ("a_escala_v410_partes", "a_escala_v410_partes_do_texto", "a_escala_v410_partes_dos_numeros", "h0dn_fontes_hms13_v410_partes", "h0dn_fontes_hms13_v410_partes_do_texto", "h0dn_fontes_hms13_v410_partes_dos_numeros")}
J["checagens_negadas_ruins"] = {k: {a: b for a, b in (rep.get(k) or {}).items() if not b.get("ok")} for k in ("a_escala_v410_checagens_negadas", "h0dn_fontes_hms13_v410_checagens_negadas", "h0dn_bg1_v410_checagens_negadas")}
J["ordem_de_chamada"] = {k: (rep.get(k) or {}).get("real", {}).get("ok") for k in ("ordem_de_chamada_iald2_v410", "ordem_de_chamada_a_escala_v410", "ordem_de_chamada_h0dn_bg1_v410", "ordem_de_chamada_h0dn_fontes_hms13_v410")}
print("\n[pre-teste] unidade: %d checagens, falsas: %s" % (len(U), J["unidade_falsas"])); print("[pre-teste] fluxo:", J["fluxo_ok"], "| vizinhos:", J["vizinhos_ok"], "| partes falsas:", J["partes_falsas"], "| negadas ruins:", J["checagens_negadas_ruins"], "| %.0f s" % (time.time() - T0))
grava(False)   # (parcial: se o artigo cair, o que ja' foi medido fica no disco)
# ---- o artigo: so' o que e' NOVO (uma passada do pdflatex)
exec(compile("\n" * p1.count("\n") + p8, ENS, "exec"), g)
TAIL = r'''
import re as _re_p
_GA_ = {"pt": "o registro da AEscala NÃO selou", "en": "the AEscala record did NOT seal"}; _GH_ = {"pt": "o registro do H0DN NÃO selou", "en": "the H0DN record did NOT seal"}; _GI_ = {"pt": "NÃO selaram todos", "en": "did NOT all seal"}
_GF_ = {"pt": _re_p.compile(r"o recibo documental HMS\W{0,3}13 NÃO selou"), "en": _re_p.compile(r"the documentary HMS\W{0,3}13 receipt did NOT seal")}
_cva = dict(copy.deepcopy(c)); _cva.pop("a_escala_v410", None)
_cvf = dict(copy.deepcopy(c)); _cvf.pop("h0dn_fontes_hms13_v410", None)
_cvv = dict(copy.deepcopy(c)); [_cvv.pop(k, None) for k in list(um._V410_REGISTROS_FUNCAO) + list(um._V410_NOMES_REGISTROS)]
_PRE = {}
for lang in ("pt", "en"):
    tex, txt, rcs, log = compilar(c, "pre_%s" % lang, lang, duas=False); flat = re.sub(r"\s+", " ", txt)
    h0 = TI410 if lang == "pt" else TI410E; h1 = TN409 if lang == "pt" else TN409E
    iq_ = flat.find("O coração:" if lang == "pt" else "The heart:"); a = flat.find(h0.replace(chr(92) + "beta", "β"), iq_ + 5); bb = flat.find(h1, a + 10)
    sec = flat[a:bb] if (a >= 0 and bb > a) else ""
    tp = os.path.join(DRY, "pre_%s.toc" % lang); toc = re.sub(r"(\\[A-Za-z]+) (?=[$}0-9])", r"\1", open(tp, encoding="utf-8", errors="replace").read().replace("\n", "")) if os.path.exists(tp) else ""
    _nd = [sec[max(0, m_.start() - 90):m_.start() + 30] for m_ in re.finditer(r"n/d|n/a", sec)][:6]
    d = {"pdflatex_rc": rcs, "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6], "faltam": [w for w in DEVE[lang] if w not in flat.replace("_ ", "_") and w not in tex], "nd_na_secao": sec.count("n/d") + sec.count("n/a"), "nd_contexto": _nd, "secao_chars": len(sec),
         "guarda": [m_.group(0) for m_ in GUARDA.finditer(sec.replace("_ ", "_"))], "toc_faltam": [w for w in TOC[lang] if w not in toc], "frases_de_guarda_ausentes_no_texto_completo": (_GA_[lang] not in flat) and (_GH_[lang] not in flat) and (_GI_[lang] not in flat) and not _GF_[lang].search(flat)}
    _ta, _xa, _ra, _la = compilar(_cva, "pre_var_a_%s" % lang, lang, duas=False); fla = re.sub(r"\s+", " ", _xa)
    _tf, _xf, _rf, _lf = compilar(_cvf, "pre_var_f_%s" % lang, lang, duas=False); flf = re.sub(r"\s+", " ", _xf)
    _tv, _xv, _rv, _lv = compilar(_cvv, "pre_var_v_%s" % lang, lang, duas=False); flv = re.sub(r"\s+", " ", _xv)
    d["variantes"] = {"rc_a_escala": _ra, "erros_a_escala": [l for l in _la.splitlines() if l.startswith("! ")][:4], "frase_guarda_a_escala": _GA_[lang] in fla, "so_a_guarda_da_aescala": (_GI_[lang] not in fla) and (_GH_[lang] not in fla) and not _GF_[lang].search(fla),
                      "rc_hms13": _rf, "erros_hms13": [l for l in _lf.splitlines() if l.startswith("! ")][:4], "frase_guarda_hms13": bool(_GF_[lang].search(flf)), "so_a_guarda_do_hms13": (_GI_[lang] not in flf) and (_GH_[lang] not in flf) and (_GA_[lang] not in flf),
                      "rc_todos": _rv, "erros_todos": [l for l in _lv.splitlines() if l.startswith("! ")][:4], "todas_as_quatro_guardas_quando_todos_faltam": (_GI_[lang] in flv) and (_GH_[lang] in flv) and (_GA_[lang] in flv) and bool(_GF_[lang].search(flv))}
    d["ok"] = bool(rcs == [0] and not d["latex_errors"] and not d["faltam"] and not d["nd_na_secao"] and d["secao_chars"] >= 1800 and not d["guarda"] and not d["toc_faltam"] and d["frases_de_guarda_ausentes_no_texto_completo"]
                   and _ra == [0] and _rf == [0] and _rv == [0] and d["variantes"]["frase_guarda_a_escala"] and d["variantes"]["so_a_guarda_da_aescala"] and d["variantes"]["frase_guarda_hms13"] and d["variantes"]["so_a_guarda_do_hms13"] and d["variantes"]["todas_as_quatro_guardas_quando_todos_faltam"])
    _PRE[lang] = d
    print("[pre-teste] artigo", lang, json.dumps(d, ensure_ascii=False))
'''
try:
    exec(compile(TAIL, "<preteste:artigo>", "exec"), g)
    exec(compile("\n" * src[:i9].count("\n") + p9, ENS, "exec"), g)
except BaseException as e:   # noqa: BLE001
    import traceback
    J["erro_artigo"] = traceback.format_exc()[-3000:]; grava(False); print(J["erro_artigo"]); sys.exit(3)
J["artigo"] = g["_PRE"]; J["markdown_falsas"] = sorted(k for k, v in g["rep"]["markdown"].items() if not v); J["markdown_n"] = len(g["rep"]["markdown"])
ok = bool(not J["unidade_falsas"] and J["fluxo_ok"] and J["vizinhos_ok"] and all(v for v in J["ordem_de_chamada"].values()) and not any(J["partes_falsas"].values()) and not any(J["checagens_negadas_ruins"].values()) and all(d["ok"] for d in J["artigo"].values()) and not J["markdown_falsas"])
grava(ok)
print("[pre-teste] md falsas:", J["markdown_falsas"], "de", J["markdown_n"]); print("\nPRE-TESTE DA PARTE 2: %s | %.0f s" % ("TUDO PASSOU" if ok else "FALHOU", time.time() - T0)); sys.exit(0 if ok else 1)
