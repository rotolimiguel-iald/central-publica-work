# -*- coding: utf-8 -*-
"""Extrai, do texto que os geradores do espelho produzem HOJE, os trechos que dizem que β_TGL na natureza a 5σ é o fator decisivo aberto
(12/11/2026, claude-site-custodia; de acordo da gerência c1). Nada é digitado: cada trecho sai do `ler()` do estatuto_tres_apoios.py e das
linhas-fonte do gerar_estado_atual.py, e tem de aparecer UMA vez. Grava:
  - tools/custodia_g1/h0dn_trechos_estatuto.json (o que a G1 usa no E04 para remendar os dois geradores);
  - work/custodia_v411_preparo_12nov/ESTATUTO_TRECHOS_PARA_O_HANDOFF_v411.md (para quem escreve os onze marcadores: o trecho e o contexto).
Só lê o espelho; não escreve nele."""
import ast, hashlib, importlib.util, json, re, sys, time
from pathlib import Path

TB = Path(r"C:\IALD\Artigo\the_boundary")
CEN = Path(r"C:\IALD\Central de Patentes")
SAI_JSON = CEN / "tools" / "custodia_g1" / "h0dn_trechos_estatuto.json"
SAI_MD = CEN / "work" / "custodia_v411_preparo_12nov" / "ESTATUTO_TRECHOS_PARA_O_HANDOFF_v411.md"
EST = TB / "tools" / "estatuto_tres_apoios.py"
GEA = TB / "tools" / "gerar_estado_atual.py"

PADROES = {
    "linha_en": r"What nature decides is not proved: the decisive open factor is \*\*β_TGL itself in nature at ≥ 5σ\*\*\.",
    "linha_06_en": r"what nature decides is not proved: the decisive open factor is \*\*β_TGL in nature at ≥ 5σ\*\*\.",
    "linha_06_pt": r"o que a natureza decide não se prova: o fator decisivo aberto é \*\*β_TGL na natureza a 5σ\*\*\.",
    "curto_en": r"What nature decides is not proved: the decisive open factor is beta_TGL itself in nature at 5 sigma\.",
    "curto_pt_ascii": r"O que a natureza decide nao se prova: o fator decisivo aberto e' beta_TGL na natureza a 5 sigma\.",
    "p2_en": r"\*\*What nature decides is not proved — the decisive open factor is β_TGL itself in nature at ≥ 5σ \(P2, `P2_NOT_DETERMINED`\)\.\*\* "
             r"No channel discriminates GR at the available sensitivity, in either direction:",
    "secao_md": r"O que a natureza decide não se prova: o fator decisivo aberto é \*\*β_TGL na natureza a 5σ\*\*",
    "linha_curta_en": r"What nature decides is not proved: the decisive open factor is \*\*β_TGL itself in nature at ≥ 5σ\*\*\.",
    "p_curto_en": r"\*\*What nature decides is not proved:\*\* the decisive open factor is β_TGL itself at ≥ 5σ \(P2\)",
}

spec = importlib.util.spec_from_file_location("estatuto_tres_apoios_leitura", EST)
mod = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(EST.parent))
spec.loader.exec_module(mod)
E = mod.ler(TB)
trechos, md = {}, []
for k, rx in PADROES.items():
    t = E.get(k)
    assert isinstance(t, str), "chave ausente no estatuto: " + k
    ms = list(re.finditer(rx, t))
    assert len(ms) == 1, "o trecho de %s aparece %d vez(es)" % (k, len(ms))
    m = ms[0]
    trechos[k] = m.group(0)
    md.append("### `ESTATUTO_%s_v411` — substitui, dentro da chave `%s`, exatamente:\n\n> %s\n\n*Contexto (o que fica antes e depois, gerado com números do core):* "
              "…%s **[o trecho]** %s…\n\n*ASCII só:* %s\n" % (k.upper(), k, m.group(0), t[max(0, m.start() - 140):m.start()].replace("\n", " "),
                                                              t[m.end():m.end() + 160].replace("\n", " "), "sim (a chave inteira é ASCII)" if t.isascii() else "não"))
src = GEA.read_bytes().decode("utf-8")
linhas = {}
for k, chave in (("p2_en_estado", "is the decisive open factor.*\")"), ("p2_pt_estado", "é o fator decisivo aberto.*\")")):
    ls = [ln for ln in src.split("\r\n") if ln.endswith(chave)]
    assert len(ls) == 1, "a linha %s aparece %d vez(es) no gerar_estado_atual.py" % (k, len(ls))
    linhas[k] = ls[0]
    texto = ast.literal_eval(ls[0].strip()[len("L.append("):-1])   # a string Python da própria linha, só como literal
    md.append("### `ESTATUTO_%s_v411` — substitui a linha inteira do gerar_estado_atual.py (seção «What is NOT proved»):\n\n> %s\n"
              % ("P2_ESTADO_EN" if k == "p2_en_estado" else "P2_ESTADO_PT", texto))
d = {"schema": "H0DN_TRECHOS_ESTATUTO_V1", "gerado": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "por": "claude-site-custodia (work/custodia_v411_preparo_12nov/extrair_trechos_estatuto_12nov.py)",
     "fontes": {"estatuto_tres_apoios.py": hashlib.sha256(EST.read_bytes()).hexdigest(), "gerar_estado_atual.py": hashlib.sha256(GEA.read_bytes()).hexdigest(),
                "selo_versao": E.get("versao") or json.loads((TB / mod.A3 / "um_absoluto_selo.json").read_text(encoding="utf-8")).get("um_version")},
     "estatuto": trechos, "estado_linhas": linhas,
     # AO LADO (12/11/2026, a mesma sessao): ESTATUTO_P2_EN colidia com a chave p2_en do estatuto; as duas linhas do estado viram ESTATUTO_P2_ESTADO_EN/PT
     "marcadores": {**{"ESTATUTO_" + k.upper(): k for k in trechos}, "ESTATUTO_P2_ESTADO_EN": "p2_en_estado", "ESTATUTO_P2_ESTADO_PT": "p2_pt_estado"}}
for p, b in ((SAI_JSON, (json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8")),
             (SAI_MD, ("# Os onze trechos do estatuto que o H0DN aberto substitui (v411)\n\n*Gerado por script em %s do texto que os geradores do espelho produzem hoje "
                       "(selo %s). Cada marcador do handoff substitui SÓ o trecho citado, na sintaxe da chave; o resto da chave (números do core) continua gerado. "
                       "Uma linha só, sem quebra; a chave ASCII pede texto ASCII. Os textos passam pela F67, pelos números e pela cabeça contra o registro e pelo portão.*\n\n"
                       % (d["gerado"], d["fontes"]["selo_versao"]) + "\n".join(md)).encode("utf-8"))):
    if p.exists():
        p.with_name(p.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(p.read_bytes())
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_bytes(b)
    tmp.replace(p)
    print("gravado:", p, len(b), "bytes, sha16", hashlib.sha256(b).hexdigest()[:16])

assert len(d["marcadores"]) == 11, "os marcadores colidiram: %d" % len(d["marcadores"])
