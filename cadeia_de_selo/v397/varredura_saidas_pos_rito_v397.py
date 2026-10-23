# -*- coding: utf-8 -*-
"""varredura_saidas_pos_rito_v397.py -- varredura de FIDELIDADE POR BYTES dos TEXTOS RENDERIZADOS (pedida pela gerencia em 23/10: «varra ... o artigo PT/EN, o .md, os textos do pos-rito e o handoff por qualquer frase que atribua ao operador
palavras que nao estao nos verbatins»). Roda DEPOIS do ensaio a seco (que renderiza o artigo PT/EN e o .md do candidato em dry_v397\\ e falso_nos\\) e dos dois harness do pos-rito (que renderizam linhagem, Atlas, desenho, topicos, avisos e o handoff):
  pos_rito\\harness_textos_ensaio_v397.py e pos_rito\\harness_fechar_sandbox_v397.py.
Superficies varridas: (a) as saidas dos harness (pos_rito\\harness_saida_v397\\textos\\* e o handoff do fechar); (b) o QUADRO e a SECAO v397 do artigo PT e EN renderizados (dry_v397\\dry_v397_pt.tex / _en.tex); (c) o .md canonico renderizado (falso_nos).
Confere, so' por leitura: (1) toda citacao entre «» e `` '' (>= 12 caracteres) existe VERBATIM nos bytes dos OPERADOR_* (work\\cunhagens_13out) ou no Atlas (ou e' rotulo da cadeia); (2) toda ocorrencia da LEITURA do fator K (a Palavra flutua sobre o abismo
pelo fator K / the Word floats over the abyss through the factor K) vem com a forma «fala + leitura ratificada»: os DOIS sha16 (o da fala da Palavra e o da ratificacao), LIDOS dos arquivos, na mesma janela; (3) nenhuma ocorrencia de «o operador disse/diz/falou/escreveu».
Grava varredura_saidas_pos_rito_v397.json; rc 0 so' se tudo confere.   uso: python -I -B -X utf8 varredura_saidas_pos_rito_v397.py"""
import glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v397 as DL  # noqa: E402
WK = DL.WK
norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'")).strip()
OPB = " || ".join(norm(open(p, encoding="utf-8", errors="replace").read()) for p in glob.glob(os.path.join(WK, "cunhagens_13out", "OPERADOR_*.txt")))
ATL = re.sub(r"\s+", " ", open(os.path.join(WK, "..", "memory", "TGL_ATLAS.md"), encoding="utf-8", errors="replace").read().replace("**", ""))
ROTULOS = {"o teste da única palavra", "o teste da unica palavra", "the test of the only word"}
# os dois sha16 da forma «fala + leitura ratificada»: LIDOS dos arquivos de origem, nunca digitados
_sh = lambda nome: hashlib.sha256(open(os.path.join(WK, "cunhagens_13out", nome), "rb").read()).hexdigest()[:16]
S_VERAC = _sh("OPERADOR_23out_teste_de_veracidade_palavra_flutua_sobre_o_abismo_verbatim.txt"); S_RATK = _sh("OPERADOR_23out_ratifica_pelo_fator_K_verbatim.txt")
SAIDA = os.path.join(HERE, "pos_rito", "harness_saida_v397")
alvos = sorted(glob.glob(os.path.join(SAIDA, "textos", "*")) + glob.glob(os.path.join(SAIDA, "fechar_sandbox_resultado", "*.md")))
pecas = [(os.path.relpath(p, HERE), open(p, encoding="utf-8", errors="replace").read()) for p in alvos]


def secao_tex(tex, titulo):
    """A secao v397 do artigo renderizado (do \\section* ate a proxima) e o QUADRO do topo (do primeiro \\fbox ate o primeiro \\end{center})."""
    out = []
    i = tex.find("\\section*{" + titulo + "}")
    if i >= 0:
        j = tex.find("\\section*{", i + 10)
        out.append(tex[i:j if j > 0 else i + 40000])
    q = tex.find("\\fbox{\\parbox")
    if q >= 0:
        out.append(tex[q:tex.find("\\end{center}", q)])
    return out


for lang, titulo in (("pt", "O Teste da Única Palavra"), ("en", "The Test of the Only Word")):
    p = os.path.join(HERE, "dry_v397", "dry_v397_%s.tex" % lang)
    if os.path.exists(p):
        for k, trecho in enumerate(secao_tex(open(p, encoding="utf-8", errors="replace").read(), titulo)):
            pecas.append(("dry_v397_%s.tex#%s" % (lang, "secao" if k == 0 else "quadro"), trecho))
pmd = os.path.join(HERE, "falso_nos", "um_absoluto_forma_canonica.md")
if os.path.exists(pmd):
    md = open(pmd, encoding="utf-8", errors="replace").read(); ls = md.splitlines()
    pecas.append(("falso_nos/um_absoluto_forma_canonica.md#topo+v397", "\n".join(ls[:30] + [l for l in ls[30:] if "(v397" in l])))
R = {"pecas_varridas": len(pecas), "arquivos_dos_harness": len(alvos), "sha16_da_fala_da_palavra": S_VERAC, "sha16_da_ratificacao": S_RATK, "aspas_nao_achadas": {}, "fator_K_sem_os_dois_sha16": [], "operador_disse": [], "n_leituras_do_fator_K": 0}
ok = len(alvos) > 0 and len(pecas) > len(alvos)
# {1,}: o par ``token'' (5 caracteres) nao pode se estender ate o proximo '' (o filtro de >= 12 caracteres vem depois)
rxs = [re.compile("«([^»]{8,900})»"), re.compile("``(.{1,900}?)''")]
# a LEITURA «a Palavra flutua sobre o abismo pelo fator K» (nao a mencao simples de K como o fator do resultado)
rxk = re.compile(r"(?:abismo|abyss)[^\n]{0,160}?(?:pelo fator|through the factor)\s*\$?K")
rxd = re.compile(r"(?i)o operador\s+(?:disse|diz|falou|escreveu)|the operator\s+(?:said|says|wrote)")
for nome, t in pecas:
    for rx in rxs:
        for m in rx.finditer(t):
            fr = norm(m.group(1)).replace(" --- ", " — ").replace("\\'E", "É").strip(" .,;:")
            if len(fr) < 12 or fr.lower() in OPB.lower() or fr.lower() in ATL.lower() or fr.lower() in ROTULOS:
                continue
            R["aspas_nao_achadas"].setdefault(fr[:150], []).append(nome)
    for m in rxk.finditer(t):
        R["n_leituras_do_fator_K"] += 1
        jan = t[max(0, m.start() - 260):m.end() + 700]
        if not (S_VERAC in jan and S_RATK in jan):
            R["fator_K_sem_os_dois_sha16"].append("%s: ...%s..." % (nome, jan[240:420].replace("\n", " ")))
    for m in rxd.finditer(t):
        R["operador_disse"].append("%s: %s" % (nome, t[max(0, m.start() - 40):m.end() + 120].replace("\n", " ")))
ok = ok and not R["aspas_nao_achadas"] and not R["fator_K_sem_os_dois_sha16"] and not R["operador_disse"] and R["n_leituras_do_fator_K"] > 0
R["todas_conferem"] = ok
json.dump(R, open(os.path.join(HERE, "varredura_saidas_pos_rito_v397.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, (dict, list)) else len(v)) for k, v in R.items()}, ensure_ascii=False))
for fr, fs in R["aspas_nao_achadas"].items():
    print("  ASPAS NAO ACHADA:", fr, "|", sorted(set(fs))[:3])
for x in R["fator_K_sem_os_dois_sha16"][:6]:
    print("  FATOR K SEM OS DOIS SHA16:", x[:300])
for x in R["operador_disse"][:6]:
    print("  OPERADOR DISSE:", x[:300])
print("TODAS CONFEREM" if ok else "FALHOU")
sys.exit(0 if ok else 1)
