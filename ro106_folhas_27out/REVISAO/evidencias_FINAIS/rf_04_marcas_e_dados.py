# -*- coding: utf-8 -*-
# C2 (marcas de rascunho), C6 (dados pessoais) e parte de C7 (termos internos) nos PDFs FINAIS (e, por contraste, nos aceitos).
import json, pathlib, re, collections, unicodedata
import fitz

K = pathlib.Path("C:/IALD/Central de Patentes/work/ro106_folhas_27out")
E = K / "REVISAO" / "evidencias_FINAIS"
ALVOS = {
    "576_final": "CARTA_REGRA_26_4_050576_FINAL.pdf",
    "579_final": "CARTA_REGRA_26_4_050579_FINAL.pdf",
    "576_aceita": "CARTA_REGRA_26_4_050576.pdf",
    "579_aceita": "CARTA_REGRA_26_4_050579.pdf",
}
MARCAS = [
    r"minuta", r"n[aã]o enviada", r"a preencher", r"\[LEGAL\]", r"\[local\]", r"\[data\]", r"\[ASSINATURA", r"rascunho",
    r"\bTODO\b", r"\bXXX+\b", r"\?\?\?", r"\bTBD\b", r"lorem", r"placeholder", r"preench", r"liberação do operador", r"\boperador\b",
]
INTERNOS = [
    r"Central de Patentes", r"\bIALD\b", r"Claude", r"Codex", r"Kimi", r"ChatGPT", r"Gemini", r"DeepSeek", r"MiMo", r"Qwen",
    r"gerência", r"gerencia", r"revis[aã]o", r"rodada", r"script", r"\.py\b", r"\.tex\b", r"conferência", r"kit\b",
    r"sha256", r"sha16", r"hash", r"\bB4\b", r"\bR2-1\b", r"work[\\/]", r"C:\\", r"/IALD", r"TikZ", r"matplotlib", r"xelatex", r"XeTeX", r"MiKTeX",
    r"DECLARADO", r"\[DERIVED\]", r"\[REAL\]", r"\[INPUT\]", r"\[ONTO\]", r"\[KNOWN\]",
]
PESSOAIS = {
    "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{11}\b",
    "CNPJ": r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b|\b\d{14}\b",
    "EMAIL": r"[\w.+-]+@[\w-]+(\.[\w-]+)+",
    "TELEFONE": r"(\+?55\s?)?\(?\b\d{2}\)?[\s.-]?9?\d{4}[\s.-]\d{4}\b",
    "CEP": r"\b\d{2}\.?\d{3}-\d{3}\b",
    "URL": r"https?://\S+|www\.\S+",
    "RG/OAB/CREA": r"\bRG\b|\bOAB\b|\bCREA\b|\bCRM\b",
    "ORCID": r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dX]\b",
    "Logradouro (rua/av.)": r"\b(Rua|Av\.?|Avenida|Alameda|Travessa|Rodovia|Pra[cç]a)\s+[A-ZÁÉÍÓÚ][\w .,'ºª-]*",
    "Cidade/UF": r"\b(Goi[aâ]nia|GO\b|Rio de Janeiro|RJ\b|São Paulo|SP\b|Bras[ií]lia|DF\b)",
}
out = {}
for tag, nome in ALVOS.items():
    d = fitz.open(K / nome)
    texto = "\n".join(p.get_text("text") for p in d)
    t = unicodedata.normalize("NFC", texto)
    flat = re.sub(r"\s+", " ", re.sub(r"(?<=\w)-\n(?=\w)", "", t))
    r = {"marcas": {}, "internos": {}, "pessoais": {}, "colchetes": [], "palavras_com_underscore_ou_chaves": []}
    for pat in MARCAS:
        m = [x.group(0) for x in re.finditer(pat, flat, flags=re.I)]
        r["marcas"][pat] = m
    for pat in INTERNOS:
        m = [x.group(0) for x in re.finditer(pat, flat, flags=re.I)]
        r["internos"][pat] = m
    for k, pat in PESSOAIS.items():
        m = [x.group(0) for x in re.finditer(pat, flat)]
        r["pessoais"][k] = m
    # todos os colchetes e conteudos
    cols = re.findall(r"\[[^\]\n]{0,80}\]", flat)
    r["colchetes"] = dict(collections.Counter(cols))
    # colchete aberto sem fechar ou vice-versa, chaves, <>
    r["desbalanceio"] = {"[": flat.count("["), "]": flat.count("]"), "{": flat.count("{"), "}": flat.count("}"), "<": flat.count("<"), ">": flat.count(">")}
    r["underscore_chaves"] = re.findall(r"\S*[_{}\\]\S*", flat)[:50]
    # texto de anotacoes, links e anexos
    r["annots"] = [[a.type[1], a.info.get("content", "")] for p in d for a in (p.annots() or [])]
    r["links"] = [l for p in d for l in p.get_links()]
    r["embfiles"] = d.embfile_names()
    # texto invisivel (render_mode 3) ou fora da pagina: varrer spans via rawdict seria caro; checar por textpage com flags de invisivel
    inv = 0
    fora = 0
    for p in d:
        rect = p.rect
        for b in p.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    x0, y0, x1, y1 = sp["bbox"]
                    if x1 < rect.x0 or x0 > rect.x1 or y1 < rect.y0 or y0 > rect.y1:
                        fora += 1
                    if sp.get("alpha", 255) == 0 or (sp.get("size", 1) < 1.0):
                        inv += 1
    r["spans_invisiveis"] = inv
    r["spans_fora_da_pagina"] = fora
    out[tag] = r
    print("=" * 90)
    print(tag, nome)
    print("  marcas de rascunho encontradas:", {k: v for k, v in r["marcas"].items() if v})
    print("  termos internos encontrados:", {k: v for k, v in r["internos"].items() if v})
    print("  dados pessoais (padroes):", {k: v for k, v in r["pessoais"].items() if v})
    print("  colchetes:", r["colchetes"])
    print("  desbalanceio:", r["desbalanceio"])
    print("  underscore/chaves/barra:", r["underscore_chaves"])
    print("  annots:", r["annots"], "| links:", len(r["links"]), "| embfiles:", r["embfiles"], "| spans invisiveis:", inv, "| fora da pagina:", fora)
(E / "rf_04_marcas_e_dados.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
