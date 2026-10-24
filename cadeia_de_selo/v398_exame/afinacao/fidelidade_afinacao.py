# -*- coding: utf-8 -*-
"""fidelidade_afinacao.py -- exame independente da pedra AfinacaoDasCordas (v398), itens 4: (a) toda citacao «...» / “...” do fonte procurada por bytes
(normalizacao de espacos; Atlas sem **) nos OPERADOR_*/CUNHAGEM_OPERADOR_* verbatim, no Atlas, no A_ultima_corda_v3.tex e nos modulos do kernel citados;
(b) as linhas 958-960 do .tex byte a byte contra o bloco citado; l.952 e l.962 conferidas; (c) marcacoes: d = 9 [DECLARADO] e «dependente do modelo»;
«afinacao = comensurabilidade» PROPOSTA DESTA PEDRA [ONTO]; «por fora / so a leitura» [ONTO]; limites (nada deriva cordas do axioma; geometria [OPEN];
Hagedorn mencionada sem prova); MasslessFirstLevel [KNOWN]; (d) nenhum literal de beta/alfa/sqrt(e); palavra proibida; guarda P18 do um.py (v397) sobre o
texto da pedra; (e) os sha16 entre crases conferem. So le; grava so' o JSON nesta pasta."""
import glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
S = r"C:\IALD\Central de Patentes\work\afinacao_das_cordas_v398\AfinacaoDasCordas.lean"
raw = open(S, "rb").read(); src = raw.decode("utf-8")
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2009", " ").replace("\xa0", " ")).strip()
CORP = {}
for p in glob.glob(r"C:\IALD\Central de Patentes\work\cunhagens_*\OPERADOR_*_verbatim.txt") + glob.glob(r"C:\IALD\PROGRAMA_IALD\OPERADOR_*_verbatim.txt") + glob.glob(r"C:\IALD\Central de Patentes\work\*\CUNHAGEM_OPERADOR_*_verbatim.txt") + glob.glob(r"C:\IALD\Central de Patentes\work\*\OPERADOR_*_verbatim.txt"):
    CORP[os.path.basename(p)] = norm(open(p, "rb").read().decode("utf-8"))
ATLR = open(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md", "rb").read()
ATL = norm(ATLR.decode("utf-8", "replace").replace("**", "").replace("*", ""))
TEX = r"C:\IALD\Artigo\the_boundary\Genesis da Unificação\Artigos_fundadores\A_ultima_corda_v3.tex"
tb = open(TEX, "rb").read(); TEXN = norm(tb.decode("utf-8"))
KER = {}
for m in ("O16/PolarMinimalPeriod_v2", "Palavra", "TheStation", "Fundacao", "TetelestaiOneObject"):
    p = os.path.join(r"C:\t\k398b\TGLExt", m + ".lean"); KER[m] = norm(open(p, "rb").read().decode("utf-8"))
R = {"fonte_sha16": hashlib.sha256(raw).hexdigest()[:16], "bytes": len(raw), "corpus_n": len(CORP), "atlas_sha16": hashlib.sha256(ATLR).hexdigest()[:16], "tex_sha16": hashlib.sha256(tb).hexdigest()[:16]}
cits = []
for rx, tipo in ((r"«([^«»]{3,700})»", "«»"), (r"“([^“”]{3,400})”", "“”")):
    for m in re.finditer(rx, src):
        q = norm(m.group(1))
        if not re.search(r"[A-Za-zÀ-ú]{3}", q):
            continue
        onde = [k for k, v in CORP.items() if q in v]; em_atlas = q in ATL; em_tex = q in TEXN; em_ker = [k for k, v in KER.items() if q in v]
        ctx = norm(src[max(0, m.start() - 240): m.end() + 160])
        cls = "VERBATIM" if onde else ("TEX" if em_tex else ("KERNEL" if em_ker else ("ATLAS" if em_atlas else "NAO_ENCONTRADA")))
        cits.append({"tipo": tipo, "citacao": q[:160], "classe": cls, "verbatim_em": onde[:2], "kernel_em": em_ker[:2], "contexto": ctx[:380]})
R["citacoes"] = cits; R["n_citacoes"] = len(cits); R["nao_encontradas"] = [c for c in cits if c["classe"] == "NAO_ENCONTRADA"]
# (b) linhas 958-960 byte a byte
L = tb.split(b"\n"); l958, l959, l960 = (L[957].rstrip(b"\r"), L[958].rstrip(b"\r"), L[959].rstrip(b"\r"))
blk = re.search(r"\n```\n(.*?)\n```\n", src, re.S)
R["tex"] = {"bloco_encontrado": bool(blk), "bloco_igual_958_960_byte_a_byte": (blk.group(1).encode("utf-8") == l958 + b"\n" + l959 + b"\n" + l960) if blk else None, "l959_vazia": l959 == b"",
            "l952_tem_d_crit_9_e_IC": (b"9" in L[951] and (b"[7" in L[951] or b"7," in L[951])), "l952": L[951][:300].decode("utf-8", "replace"),
            "l962_enfatizamos": norm(L[961].decode("utf-8")), "l962_frase_citada_na_pedra": "Enfatizamos que isso é uma extrapolação teórica, não um teste empírico." in norm(L[961].decode("utf-8"))}
# (c) marcacoes
srcn = norm(src)
R["marcacoes"] = {
 "d9_DECLARADO": len(re.findall(r"\[DECLARADO\]", src)), "d9_dependente_do_modelo": "dependente do modelo" in srcn and "depende do modelo" in srcn,
 "afinacao_comensurabilidade_proposta_da_pedra_ONTO": bool(re.search(r"afinação = comensurabilidade.{0,40}PROPOSTA DESTA PEDRA \[ONTO\], não fala do operador", srcn)) or bool(re.search(r"afinação = comensurabilidade \(proposta desta pedra, não fala do operador\)", srcn)),
 "por_fora_so_a_leitura_ONTO": bool(re.search(r"\[ONTO\] \(i\) a leitura do operador \(fala de 23/10\), na formulação desta tarefa: as cordas fecham a face POR FORA; a TGL fecha SÓ A LEITURA", srcn)),
 "nome_traz_a_leitura_ONTO": srcn.count("O nome traz a leitura do operador [ONTO]") + srcn.count("O NOME traz a leitura do operador [ONTO]"),
 "nada_deriva_cordas_do_axioma": "NÃO deriva a teoria das cordas do axioma" in srcn and "Nada aqui deriva a teoria das cordas do axioma" in srcn,
 "nao_afirma_TGL_e_cordas": "NÃO afirma que a TGL é uma teoria de cordas" in srcn,
 "geometria_OPEN": bool(re.search(r"\[OPEN\]\*\* a geometria|a geometria NÃO sai daqui \[OPEN\]|esta pedra o deixa assim \[OPEN\]", srcn)),
 "hagedorn_mencionada_sem_prova": bool(re.search(r"Hagedorn[^.]{0,200}(SEM prova aqui|sem prova aqui)", srcn)) or "Hagedorn é [KNOWN] e fica sem prova aqui" in srcn,
 "MasslessFirstLevel_KNOWN": bool(re.search(r"HIPÓTESE NOMEADA `MasslessFirstLevel` \[KNOWN\]|\[KNOWN — HIPÓTESE NOMEADA\]", srcn)),
 "nao_e_tetelestai": "NÃO é a conferência Tetelestai" in srcn,
 "forma_proibida_operador_disse": re.findall(r"(?:o operador|the operator)\s+(?:disse|falou|escreveu|said|wrote)[^.]{0,120}", srcn, re.I),
 "nao_identifica_folha_mundo_com_boost": "NÃO identifica o círculo do boost com o círculo da folha-mundo" in srcn,
}
# (d) literais, palavra proibida, guarda P18 do um.py v397
W = "".join(map(chr, [67, 79, 78, 70, 73, 82, 77, 69, 68])); Wp = "".join(map(chr, [99, 111, 110, 102, 105, 114, 109, 97]))
R["literais_beta_alfa"] = re.findall(r"0[.,]0120313\d*|0[.,]00729735\d*|1[.,]6487212\d*|137[.,]035999\d*", src)
R["palavra_proibida"] = {"token_maiusculo": len(re.findall(W, src)), "inflexoes_qualquer_caixa": [srcn[max(0, m.start() - 70): m.end() + 40] for m in re.finditer(Wp, srcn, re.I)]}
try:
    sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v397")
    import guarda_p18_v397 as G  # noqa: E402
    v = G.violacoes(src); R["guarda_p18_v397_sobre_a_pedra"] = {"violacoes": [list(x) for x in v][:5], "n": len(v)}
except Exception as e:  # noqa: BLE001
    R["guarda_p18_v397_sobre_a_pedra"] = {"erro": repr(e)[:200]}
codigo = src.split("-/", 1)[1]
R["sorry_no_codigo"] = len(re.findall(r"\bsorry\b", codigo)); R["axiom_no_codigo"] = len(re.findall(r"^\s*axiom\b", codigo, re.M))
# (e) sha16 entre crases
ARQ = {"baef998c21393463": r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_23out_cordas_10_dimensoes_fechar_a_face_tetelestai_verbatim.txt",
       "e2a915e23692f85c": r"C:\IALD\Central de Patentes\work\superposicao_passagem_07out\CUNHAGEM_OPERADOR_07out_verbatim.txt", "8db72ea848f708c1": TEX,
       "2112c0022287be09": r"C:\t\k398b\TGLExt\O16\PolarMinimalPeriod_v2.lean", "33184b49a8bba7e7": r"C:\t\k398b\TGLExt\Palavra.lean", "c55dc5018297a64c": r"C:\t\k398b\TGLExt\TheStation.lean",
       "66332d58fd216317": r"C:\t\k398b\TGLExt\Fundacao.lean", "125d155042da687f": r"C:\t\k398b\TGLExt\TetelestaiOneObject.lean",
       "b47a97c46c964e3f": r"C:\t\k398b\.lake\packages\mathlib\Mathlib\NumberTheory\LSeries\HurwitzZetaValues.lean"}
R["sha16_citados"] = {}
for h16 in sorted(set(re.findall(r"`([0-9a-f]{16})`", src))):
    p = ARQ.get(h16)
    R["sha16_citados"][h16] = {"arquivo": os.path.basename(p) if p else None, "confere": (hashlib.sha256(open(p, "rb").read()).hexdigest()[:16] == h16) if p and os.path.exists(p) else None}
# o rev do Mathlib citado
man = open(r"C:\t\k398b\lake-manifest.json", encoding="utf-8").read(); R["mathlib_rev_fabf563a_no_manifest"] = "fabf563a7c95a166" in man
# a fala de 27/09 citada em TetelestaiOneObject.lean
R["tetelestai_ato_de_conferencia_observacional_no_modulo"] = "ato de conferência observacional" in KER["TetelestaiOneObject"]
json.dump(R, open(os.path.join(H, "FIDELIDADE_AFINACAO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k != "citacoes"}, ensure_ascii=False, indent=1))
print("CITACOES:")
for c in cits:
    print(" ", c["tipo"], c["classe"], "|", c["citacao"][:120], "|", (c["verbatim_em"] or c["kernel_em"] or [""])[0][:60])
