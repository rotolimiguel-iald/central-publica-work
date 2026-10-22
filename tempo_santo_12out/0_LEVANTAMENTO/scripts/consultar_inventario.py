"""Consulta SOMENTE-LEITURA ao inventario da bancada (INVENTARIO_BANCADA_CHATGPT.json) para os termos da trilha TEMPO.
Procura em 'unicos' (arquivo + declaracoes) e em 'documentos' (arquivo + titulo). Grava inventario_consultas.json.
Uso: python -I consultar_inventario.py"""
import hashlib
import json
import re

INV = r"C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.json"
TERMOS = {
    "pauli_teorema_tempo": r"time.?operator|operador.de.tempo|pauli.?(theorem|objection|teorema)|semibounded|semi.?bounded|bounded.?below|weyl.?pair|no_finite_weyl|stone.?von|canonical.?conjugate|ccr\b",
    "liouville_volume": r"liouville|phase.?space.?volume|volume.?preserv|measurePreserving|det_exp|exp_trace|symplectic",
    "tempo_termico_modular": r"thermal.?time|tempo.?termico|tempo térmico|rovelli|modular.?time|modularTime|modular_flow|modularFlow|sigma_t|modularConjugation",
    "kms": r"\bkms|KMSAt|KMSBody",
    "relogio": r"clock|relogio|relógio",
    "atrator_contracao": r"attract|atrator|contraction|contract_|strictContr|StrictComplementContraction|basin|bacia|lyapunov|spohn",
    "dissipacao_semigrupo": r"dissip|dephas|lindblad|gkls|semigroup|semigrupo|axiomFlow|diagFlow",
    "landauer_custo": r"landauer|erasure|apagamento|separation_is_not_free|cost_is|custo",
    "terceira_lei_tempo_finito": r"finite.?time|tempo.?finito|unreachable|never_lands|abismo|absolute_zero",
    "outer_inner_semifinito": r"\bouter|inner_autom|IsInner|semifinite|tracial|connes.?(spectrum|invariant)|crossed|crossedProduct|takesaki_dual|dual.?action|dualScaling|DualScalingData",
    "agora_instante": r"instantaneous|instante|\bnow\b|agora|present_moment",
    "santo_kadosh": r"kadosh|santo|sagrad|holy|sacred",
    "puro_amor_agape": r"agape|ágape|amor|love|doacao|doação|generos",
}


def main():
    raw = open(INV, "rb").read()
    d = json.loads(raw.decode("utf-8"))
    out = dict(inventario=INV, sha256=hashlib.sha256(raw).hexdigest(), gerado_em=d.get("gerado_em"),
               varredura_sha16=d.get("varredura_sha16"), numeros=d.get("numeros"), temas={})
    for tema, rx in TERMOS.items():
        r = re.compile(rx, re.I)
        hits_u = []
        for u in d["unicos"]:
            decls = [x for x in u.get("decls", []) if r.search(x)]
            if decls or r.search(u.get("arquivo", "")):
                hits_u.append(dict(arquivo=u["arquivo"], sha16=u["sha16"], n_decl=u.get("n_decl"), copias=u.get("copias"),
                                   temas=u.get("temas"), decls_casadas=decls[:40], n_casadas=len(decls)))
        hits_d = [dict(arquivo=x["arquivo"], sha16=x["sha16"], titulo=x.get("titulo"))
                  for x in d["documentos"] if r.search(x.get("arquivo", "")) or r.search(x.get("titulo") or "")]
        out["temas"][tema] = dict(regex=rx, n_lean=len(hits_u), n_docs=len(hits_d),
                                  n_decls=sum(h["n_casadas"] for h in hits_u), lean=hits_u, docs=hits_d)
    with open("inventario_consultas.json", "w", encoding="utf-8") as fo:
        json.dump(out, fo, ensure_ascii=False, indent=1)
    print("inventario sha16", out["sha256"][:16], "gerado_em", out["gerado_em"], out["numeros"])
    for t, v in out["temas"].items():
        print(f"{t:28s} lean={v['n_lean']:4d} decls={v['n_decls']:5d} docs={v['n_docs']:4d}")


if __name__ == "__main__":
    main()
