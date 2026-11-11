# -*- coding: utf-8 -*-
"""Revisor v410 R1: varredura INDEPENDENTE (sondas do revisor) de frases proibidas/obrigatorias nos textos RENDIDOS e nas fontes de texto novas. Nao usa a guarda do construtor.
Imprime cada ocorrencia com contexto para classificacao manual; separa ocorrencias DENTRO de definicoes de guarda (padroes proibidos listados) das ocorrencias em texto publico."""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
rd = lambda p: open(p, "rb").read().decode("utf-8", "replace")
norm = lambda s: re.sub(r"\s+", " ", s)
fontes = {}
for p in (R + "revisao_terceiro/novo_pt.txt", R + "revisao_terceiro/novo_en.txt", R + "revisao_terceiro/novo_md.txt"): fontes["RENDIDO_NOVO:" + os.path.basename(p)] = rd(p)
pass
for p in sorted(glob.glob("C:/t/h410/harness_saida_v410/textos/*.txt")): fontes["HARNESS:" + os.path.basename(p)] = rd(p)
for f in ("pos_rito/textos_v410.semente", "pos_rito/textos_custodia_handoff_v410.py", "pos_rito/CUSTODIA_v410_RASCUNHO.txt", "artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip",
          "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip", "delta_v410.py", "registros_v410.py", "registros_h0dn_v410.py", "registros_aescala_v410.py", "registros_hms13_v410.py"):
    if os.path.exists(R + f): fontes["FONTE:" + f] = rd(R + f)
for p in (R + "insumos/AEscala.lean", R + "insumos/IALD2.lean"): fontes["PEDRA:" + os.path.basename(p)] = rd(p)
lit = json.load(open(R + "revisao_terceiro/literais_v410.json", encoding="utf-8"))


def strs(o, acc):
    if isinstance(o, str): acc.append(o)
    elif isinstance(o, dict):
        for v in o.values(): strs(v, acc)
    elif isinstance(o, (list, tuple)):
        for v in o: strs(v, acc)


for nm, v in lit.items():
    if nm.endswith("INSUMOS"): continue
    acc = []; strs(v, acc); fontes["REG:" + nm] = "\n".join(acc)
PADROES = {
    "clay_resolvido_seco": r"(?i)clay[^.\n]{0,40}(resolvid[oa]|resolved|solved)|resolveu[^.\n]{0,30}clay|clay_solved",
    "tgl_resolve_milenio": r"(?i)(TGL|IALD)[^.\n]{0,30}(resolve|resolves|solves|resolved)[^.\n]{0,40}(milên|milen|millennium)",
    "tautologia": r"(?i)tautolog",
    "nao_resolve": r"(?i)n[ãa]o resolve|does not resolve|does not solve",
    "nao_afirma_prova_pnp": r"(?i)(n[ãa]o\s+(afirma|prova|decide)|does not (claim|prove|assert|decide))[^.\n]{0,60}P\s*=\s*n?N?P",
    "CONFIRMED": r"CONFIRMED(?!_)(?!\s*\))",
    "PROVED_BY": r"PROVED_BY",
    "5sigma_atingido": r"(?i)5\s*(σ|sigma)\s*(atingid|observad|reached|observed)|FIVE_SIGMA_OBSERVED|H0DN_CONFIRMS|\bDETECTED\b",
    "covariancia_fechada_afirma": r"(?i)(covari[âa]ncia\s+f[íi]sica\s+(est[áa]\s+)?fechada|physical covariance (is\s+)?closed)(?!\s*(n[ãa]o|False|\\textsf\{False))",
    "abertura_permitida": r"(?i)abertura\s+permitida|opening[_ ]allowed\W{0,4}true|full_HMS_admitted\W{0,4}true|physical_covariance_closed\W{0,4}true",
    "PROVED_IN_NATURE": r"PROVED_IN_NATURE",
    "provado_na_natureza": r"(?i)provado na natureza|proved in nature|proven in nature",
}
for pn, rx in PADROES.items():
    print("\n######", pn)
    tot = 0
    for k, t in fontes.items():
        tn = norm(t)
        ms = list(re.finditer(rx, tn))
        if not ms: continue
        tot += len(ms)
        print("  [%s] %d" % (k, len(ms)))
        seen = set()
        for m in ms[:4]:
            c = tn[max(0, m.start() - 110):m.end() + 130]
            if c in seen: continue
            seen.add(c); print("      ...", c)
    print("  total", tot)
