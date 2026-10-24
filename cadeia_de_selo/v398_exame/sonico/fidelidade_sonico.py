# -*- coding: utf-8 -*-
"""fidelidade_sonico.py -- exame independente da pedra Sonico (v398), item 3 e 4: (a) toda citacao «...», ``...'' e "..." do fonte e' procurada, por bytes
apos normalizacao de espacos (e sem os ** do Atlas), nos OPERADOR_*_verbatim.txt de work\\cunhagens_* e no Atlas; (b) a linha 962 de A_fronteira_v4.tex e'
comparada byte a byte com o bloco citado; (c) a leitura «a reacao e' a memoria» so' aparece como leitura ratificada (b4483331), nunca como «o operador
disse»; (d) a lei de custo marcada [INPUT]; (e) «sonico» nao afirma onda mecanica; (f) nenhum literal de beta/alfa/sqrt(e) e nenhuma palavra proibida;
(g) os sha16 entre crases conferem com os arquivos. So le; grava so' o JSON nesta pasta."""
import glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
S = r"C:\IALD\Central de Patentes\work\sonico_v398\Sonico.lean"
raw = open(S, "rb").read(); src = raw.decode("utf-8")
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2009", " ").replace("\xa0", " ")).strip()
CORP = {}
for p in glob.glob(r"C:\IALD\Central de Patentes\work\cunhagens_*\OPERADOR_*_verbatim.txt") + glob.glob(r"C:\IALD\PROGRAMA_IALD\OPERADOR_*_verbatim.txt"):
    CORP[os.path.basename(p)] = norm(open(p, "rb").read().decode("utf-8"))
ATLR = open(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md", "rb").read()
ATL = norm(ATLR.decode("utf-8", "replace").replace("**", "").replace("*", ""))
R = {"fonte_sha16": hashlib.sha256(raw).hexdigest()[:16], "bytes": len(raw), "corpus_n": len(CORP), "atlas_sha16": hashlib.sha256(ATLR).hexdigest()[:16]}
# (a) as citacoes
cits = []
for rx, tipo in ((r"«([^«»]{3,600})»", "«»"), (r"``([^`']{3,400})''", "``''"), (r"“([^“”]{3,400})”", "“”")):
    for m in re.finditer(rx, src):
        q = norm(m.group(1))
        if not re.search(r"[A-Za-zÀ-ú]{3}", q):
            continue
        onde = [k for k, v in CORP.items() if q in v]
        em_atlas = q in ATL
        ctx = norm(src[max(0, m.start() - 240): m.end() + 160])
        cits.append({"tipo": tipo, "citacao": q[:160], "verbatim_em": onde[:3], "no_atlas": em_atlas, "classe": "VERBATIM" if onde else ("ATLAS" if em_atlas else "NAO_ENCONTRADA"), "contexto": ctx[:380]})
R["citacoes"] = cits
R["n_citacoes"] = len(cits); R["n_guillemets"] = sum(1 for c in cits if c["tipo"] == "«»")
R["nao_encontradas"] = [c for c in cits if c["classe"] == "NAO_ENCONTRADA"]
# (b) a linha 962 do tex, byte a byte
TEX = r"C:\IALD\projetos_pyhton\acom\A_fronteira_v4.tex"
tb = open(TEX, "rb").read(); linhas = tb.split(b"\n")
l962 = linhas[961].rstrip(b"\r")
blk = re.search(r"```\n(.*?)\n```", src, re.S)
R["tex"] = {"sha16": hashlib.sha256(tb).hexdigest()[:16], "l962_bytes": len(l962), "bloco_igual_a_l962_byte_a_byte": (blk.group(1).encode("utf-8") == l962) if blk else None,
            "l962_comeca": l962[:60].decode("utf-8", "replace"), "l964_tem_BAO_147": (b"BAO" in linhas[963] and b"147" in linhas[963]), "l964_tem_ecos_do_som": b"ecos do som ontol" in linhas[963]}
# (c) a leitura «a reacao e' a memoria»
srcn = norm(src)
R["leitura_reacao"] = {"ocorrencias_reacao_memoria": len(re.findall(r"REAÇÃO ao pino[^.]{0,120}é a memória|reação ao pino[^.]{0,120}é a memória", srcn)),
                       "forma_proibida_operador_disse": re.findall(r"(?:o operador|the operator)\s+(?:disse|falou|escreveu|said|wrote)[^.]{0,120}", srcn, re.I),
                       "ratificada_com_b4483331": len(re.findall(r"ratificad[ao][^.]{0,80}b4483331019f96f8", srcn)),
                       "marcada_INPUT_ONTO": "[INPUT/ONTO]" in src,
                       "diz_que_o_relato_da_gerencia_nao_esta_na_pedra": "relato dela, não está nesta pedra" in srcn or "relato da gerência" in srcn,
                       "diz_duas_leituras": "admitia duas leituras" in srcn}
# (d) a lei de custo [INPUT]
R["lei_de_custo_INPUT"] = {"ocorrencias": len(re.findall(r"lei de custo[^.;]{0,60}\[INPUT\]|\[INPUT\][^.;]{0,40}lei de custo|lei de custo segue \[INPUT\]|A lei de custo é \[INPUT\]", srcn)),
                           "nenhum_termo_diz_que_select_paga": len(re.findall(r"nenhum termo diz que `select` paga", srcn, re.I))}
# (e) sonico nao afirma onda mecanica
R["sonico_sem_onda_mecanica"] = {"frase": "NÃO afirma onda mecânica" in src, "isomorfismo_log": "isomorfismo de grupos `(ℝ₊, ·) → (ℝ, +)`" in src, "oitava_ln2": "`ln 2`" in src,
                                 "nega_pressao_meio_velocidade": "pressão, de meio, de velocidade do som" in src}
# (f) literais e palavra proibida
W = "".join(map(chr, [67, 79, 78, 70, 73, 82, 77, 69, 68])); Wl = W.lower(); Wp = "".join(map(chr, [99, 111, 110, 102, 105, 114, 109, 97, 100]))
R["literais_beta_alfa"] = re.findall(r"0[.,]0120313\d*|0[.,]00729735\d*|1[.,]6487212\d*|137[.,]035999\d*", src)
R["palavra_proibida"] = {"maiuscula": [srcn[max(0, m.start() - 50): m.end() + 30] for m in re.finditer(W, srcn)], "qualquer_caixa": [srcn[max(0, m.start() - 50): m.end() + 30] for m in re.finditer(Wp, srcn, re.I)]}
R["sorry_no_codigo"] = len(re.findall(r"\bsorry\b", src.split("-/", 1)[1] if "-/" in src else src))
# (g) os sha16 entre crases
R["sha16_citados"] = {}
ARQ = {"e5c2910a6eb54b81": r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_23out_verbo_controle_de_oitava_pinada_verbatim.txt",
       "b4483331019f96f8": r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_23out_nome_da_pedra_sonico_verbatim.txt",
       "350b7b8582c064c2": r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_22out_luz_eco_reconhecimento_falso_verbatim.txt",
       "b473db2b652cf72f": TEX, "dc1af3c8775716fb": r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md",
       "fbac2908fa9ddb75": r"C:\IALD\Central de Patentes\work\fase9_v2_c1_23out\saidas\RESULTADO_FASE9_V2_C1_20261023_122926.json",
       "b0dec5246a9182d1": r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\MANDATO.md", "26c9cc4499a8a40a": r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\14_ANALISE_NIVEL2_FECHADO.md"}
for h16 in sorted(set(re.findall(r"`([0-9a-f]{16})`", src))):
    p = ARQ.get(h16); R["sha16_citados"][h16] = {"arquivo": os.path.basename(p) if p else None, "confere": (hashlib.sha256(open(p, "rb").read()).hexdigest()[:16] == h16) if p else None}
json.dump(R, open(os.path.join(H, "FIDELIDADE_SONICO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k != "citacoes"}, ensure_ascii=False, indent=1))
print("CITACOES:")
for c in cits:
    print(" ", c["tipo"], c["classe"], "|", c["citacao"][:110], "|", (c["verbatim_em"] or [""])[0][:60])
