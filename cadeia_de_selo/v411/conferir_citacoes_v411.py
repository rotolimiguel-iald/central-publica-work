# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] REESCRITO para a v411 (o corpo da v410 subido por rotulo fica em conferir_citacoes_v411.py.bak_*_corpo_v410_bump e em bump\)
"""conferir_citacoes_v411.py -- confere que TODA citacao entre « » nos textos NOVOS da v411 e' VERBATIM de uma fala do operador: as 9 falas de 11 e 12/11 (VERBATIM_CONGELADO_v411.json, lidas por bytes) ou, se a
citacao for de fala anterior ja' selada, as falas embutidas na v410 (v410\\insumos\\cunhagens, lidas por bytes). Regra da casa: «» so' para fala verbatim do operador; frase da gerencia vai entre “ ”. Os textos novos:
delta_v411, registros_h0dn_v411, registros_v411, runtime_h0dn_v411, quadro_v411, gerar_candidato_v411 (o bloco do main, a linha UM_VERSION), os pysnips/os textos do pos-rito quando existirem, a proposta do topo do DESENHO
(5.1 b, entre “ ”: nao e' fala) e, se existir, o TOPO_RATIFICADO_v411.json; com --candidato, tambem o bloco v411 do candidato (v411_pins.py). Nao corrige texto: aponta. Grava conferir_citacoes_v411.json; rc 1 se alguma
citacao nao for verbatim. uso: python -B -X utf8 conferir_citacoes_v411.py [--candidato]"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
FALAS = {f_["nome"]: f_["text"] for f_ in DL.FALAS_V411}
ANT = {}
for p_ in glob.glob(os.path.join(DL.V410, "insumos", "cunhagens", "*.txt")):
    ANT[os.path.basename(p_)] = open(p_, "rb").read().decode("utf-8", "replace")
for p_ in glob.glob(os.path.join(DL.CUN, "OPERADOR_*_verbatim.txt")):   # (o acervo das falas do operador, so' leitura: uma citacao antiga reconhecida e' verbatim de um arquivo dele)
    ANT.setdefault(os.path.basename(p_), open(p_, "rb").read().decode("utf-8", "replace"))
_nrm = lambda s_: " ".join(str(s_).replace("\r\n", "\n").split())
# (escopo b, ORDEM da gerencia c1 de 12/11: a regra (g) da v410, portada) so' os arquivos de TEXTO do pos-rito; testes e harnesses ficam FORA da varredura, como na v410
ARQS_POS_RITO = [os.path.join("pos_rito", n_) for n_ in ("textos_v411.py", "registrar_mapa_v411.py", "fechar_v411.py", "leitura_v411.py", "superficies_v411.py", "textos_custodia_handoff_v411.py", "blocos_custodia_v411.py", "textos_v411_novo.pysnip")]
ARQS = ["delta_v411.py", "registros_h0dn_v411.py", "registros_v411.py", "runtime_h0dn_v411.py", "quadro_v411.py", "gerar_candidato_v411.py"]   # (escopo a, o do um.py: ESTRITO, as falas da lista congelada e as ja' seladas)
if os.path.exists(DL.TOPO_RATIFICADO_ARQ):
    ARQS.append(os.path.basename(DL.TOPO_RATIFICADO_ARQ))
if "--candidato" in sys.argv and os.path.exists(DL.PINS_ARQ):   # (pedido do fork B: os pinos DA RODADA -- no ensaio do topo proposto, os do artefato de ensaio)
    ARQS.append(DL.PINS_ARQ)
_MARCA = "[A ADAPTAR v" + "411]"
NAO_ADAPTADOS = [a_ for a_ in ARQS if os.path.exists(os.path.join(HERE, a_)) and _MARCA in open(os.path.join(HERE, a_), "rb").read().decode("utf-8", "replace")]
ARQS = [a_ for a_ in ARQS if a_ not in NAO_ADAPTADOS]   # (o corpo ainda e' o da v410, subido por rotulo: a citacao dele se confere quando o arquivo for adaptado; a lista vai dita no JSON)
out = {"contrato": "CONFERIR_CITACOES_v411", "n_falas_v411": len(FALAS), "n_falas_anteriores": len(ANT), "arquivos": {}, "nao_verbatim": [], "nao_conferidos_corpo_da_v410_a_adaptar": NAO_ADAPTADOS}
for a_ in ARQS:
    p_ = a_ if os.path.isabs(a_) else os.path.join(HERE, a_)
    if not os.path.exists(p_):
        continue
    t_ = open(p_, "rb").read().decode("utf-8", "replace")
    cits_ = re.findall(r"«([^«»]{3,})»", t_)
    rel_ = []
    for c_ in cits_:
        cn_ = _nrm(c_)
        de_ = [n_ for n_, f_ in FALAS.items() if cn_ in _nrm(f_)] or [n_ for n_, f_ in ANT.items() if cn_ in _nrm(f_)]
        rel_.append({"citacao": c_[:120], "verbatim_de": de_[:2], "ok": bool(de_)})
        if not de_:
            out["nao_verbatim"].append({"arquivo": a_, "citacao": c_[:200]})
    out["arquivos"][a_] = {"n_citacoes": len(cits_), "n_ok": sum(1 for r_ in rel_ if r_["ok"]), "citacoes": rel_}
_prop = re.findall(r"^> (?:PT|EN) — “(.+)”$", DL._S5, re.M)
out["proposta_do_topo"] = {"n": len(_prop), "entre_aspas_curvas": True, "citacoes_angulares_dentro": sum(len(re.findall("«[^»]+»", x_)) for x_ in _prop), "nota": "a proposta e' texto da GERENCIA (entre “ ”), nao fala do operador"}
# ---- (escopo b) A REGRA (g) DA v410, PORTADA (ordem da gerencia c1, 12/11/2026): o corpus LARGO e os rotulos da cadeia
_SRC410 = open(os.path.join(DL.V410, "conferir_citacoes_v410.py"), encoding="utf-8").read(); _TR410 = __import__("ast").parse(_SRC410)
_NS410 = {"re": re}
for _n410 in _TR410.body:   # (a normalizacao e a limpeza da v410, LIDAS do arquivo da v410, nao redigitadas)
    if isinstance(_n410, __import__("ast").Assign) and getattr(_n410.targets[0], "id", None) in ("_norm", "_limpa"):
        exec(compile(__import__("ast").get_source_segment(_SRC410, _n410), "<conferir_citacoes_v410>", "exec"), _NS410)
_norm, _limpa = _NS410["_norm"], _NS410["_limpa"]
_ROT410 = [__import__("ast").literal_eval(_n410.value) for _n410 in _TR410.body if isinstance(_n410, __import__("ast").Assign) and getattr(_n410.targets[0], "id", None) == "_ROTULOS" and isinstance(_n410.value, __import__("ast").Set)]
assert len(_ROT410) == 1 and len(_ROT410[0]) > 100, "a lista _ROTULOS da v410 nao foi lida"
# os rotulos da v411, ACRESCENTADOS um a um, cada um com o porque (titulo de secao, rotulo de linha, frase de regra da guarda, traducao seguida do original): nenhum e' fala de ninguem
ROTULOS_V411 = {
    "O teste decisivo: a razão de Hubble local/fundo (H0DN × BG1), a emenda e a abertura": "titulo de secao do artigo (DESENHO_v411 5.2), PT",
    "O teste decisivo: a razao de Hubble local/fundo (H0DN x BG1), a emenda e a abertura": "o mesmo titulo de secao, na forma ASCII dos docstrings do pos-rito",
    "The decisive test: the local/background Hubble ratio (H0DN × BG1), the amendment and the opening": "titulo de secao do artigo (DESENHO_v411 5.2), EN",
    "README: o que fica evidente": "titulo da secao do HANDOFF que leva os blocos do README (rotulo da cadeia de custodia)",
    "o recibo HMS/13 da v410 e' cobertura de fontes": "frase de REGRA do leitor das superficies (a forma da v411 que a guarda aceita, do texto do registro h0dn_bg1_v411), nao fala",
    "covariancia fisica ... aberta": "frase de REGRA do leitor das superficies (a forma da v411 que a guarda aceita, com elisao), nao fala",
}
_ROTULOS = {x_.lower() for x_ in _ROT410[0]} | {x_.lower() for x_ in ROTULOS_V411}
_DIRS410 = ("cunhagens_13out", "cinco_sigma_fora_da_cosmologia_27out", "projecao_transversal_28out", "transicao_para_a_massa_28out", "experimento_espelho_30out", "e0_cadeia_31out", "observador_terminal_31out")
_OPB = " || ".join(_norm(open(p_, encoding="utf-8", errors="replace").read()) for p_ in sum([glob.glob(os.path.join(DL.WK, d_, "*OPERADOR_*.txt")) for d_ in _DIRS410]
                                                                                  + [glob.glob(os.path.join(DL.V410, "insumos", "cunhagens", "*OPERADOR_*.txt")), glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*OPERADOR_*.txt"))], []))
_ATLAS = os.path.join(DL.CENTRAL, "memory", "TGL_ATLAS.md"); _ATL = re.sub(r"\s+", " ", open(_ATLAS, encoding="utf-8", errors="replace").read().replace("**", "")) if os.path.exists(_ATLAS) else ""
_base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()
_KERN = _norm(re.sub(r"\s--\s+", " ", _base.replace("**", "").replace("`", "").replace("\\n", " ")))
_ADENDO = _norm(open(DL.D10.ADENDO_ARQ, encoding="utf-8").read().replace("**", "").replace("`", ""))
_PEDRAS = _norm(" ".join(open(p_["src"], encoding="utf-8").read() for p_ in DL.D10.PEDRAS_V410 if os.path.exists(p_.get("src") or "")).replace("**", "").replace("`", ""))
_CASA = _norm(open(os.path.join("C:" + os.sep, "IALD", "CLAUDE.md"), encoding="utf-8", errors="replace").read().replace("**", ""))
_corpus_um = lambda fr: (fr.lower() in _OPB.lower() or fr.lower() in _ATL.lower() or fr.lower() in _ROTULOS or fr.lower() in _KERN.lower() or fr.lower() in _ADENDO.lower() or fr.lower() in _PEDRAS.lower() or fr.lower() in _CASA.lower())
_corpus_ok = lambda fr: _corpus_um(fr) or (re.search("…|" + re.escape("[...]"), fr) is not None and all(_corpus_um(x_.strip(" .,;:")) for x_ in re.split("…|" + re.escape("[...]"), fr) if len(x_.strip(" .,;:")) >= 8))
_rxs = [re.compile("«([^»]{8,700})»"), re.compile(r"``(.{8,700}?)''")]
out["nao_verbatim_do_um_py"] = list(out["nao_verbatim"])
out["nao_verbatim_do_pos_rito"] = []; out["pos_rito_saltados"] = {"concatenacao_ou_molde": 0, "curtos_ou_nomes_de_constante": 0}; out["pos_rito_arquivos"] = {}
for a_ in ARQS_POS_RITO:
    p_ = os.path.join(HERE, a_)
    if not os.path.exists(p_):
        out["pos_rito_arquivos"][a_] = "ausente"; continue
    t_ = open(p_, encoding="utf-8", errors="replace").read(); n_ok_ = n_tot_ = 0
    for rx_ in _rxs:
        for m_ in rx_.finditer(t_):
            fr_ = _limpa(m_.group(1))
            if "+" in fr_ or "%s" in fr_:   # (concatenacao que, em execucao, cerca um trecho VERBATIM lido do arquivo por sha256, ou molde de formatacao: conferido onde e' lido; como na v410)
                out["pos_rito_saltados"]["concatenacao_ou_molde"] += 1; continue
            if len(fr_) < 12 or "_V410_" in fr_ or "_V411_" in fr_:
                out["pos_rito_saltados"]["curtos_ou_nomes_de_constante"] += 1; continue
            n_tot_ += 1
            if _corpus_ok(fr_):
                n_ok_ += 1; continue
            lin_ = t_.count("\n", 0, m_.start()) + 1; l_ = t_.splitlines()[lin_ - 1]
            out["nao_verbatim_do_pos_rito"].append({"arquivo": a_, "linha": lin_, "citacao": fr_[:200], "onde": "comentario" if "#" in l_[:max(0, l_.find(m_.group(0)[:20]))] else "texto ou string do codigo"})
    out["pos_rito_arquivos"][a_] = {"n_citacoes_conferidas": n_tot_, "n_no_corpus_ou_rotulo": n_ok_}
out["regra_do_pos_rito"] = "a regra (g) da v410, portada (ordem da gerencia c1, 12/11): os arquivos de texto do pos-rito; regex de 8 a 700 caracteres; o corpus largo (falas, Atlas, um.py da base, adendo, pedras, CLAUDE.md); os rotulos da v410 herdados e os da v411 acrescentados com o porque"
out["n_rotulos"] = {"v410": len(_ROT410[0]), "v411": len(ROTULOS_V411)}
out["nao_verbatim"] = out["nao_verbatim_do_um_py"] + out["nao_verbatim_do_pos_rito"]
out["ok_do_um_py"] = not out["nao_verbatim_do_um_py"]
out["ok_do_pos_rito"] = not out["nao_verbatim_do_pos_rito"]
out["escopos"] = {"um_py": "os textos que entram no candidato (delta, registros, runtime, quadro, gerador, o TOPO_RATIFICADO e os pinos da rodada)", "pos_rito": "os scripts da frente pos-rito (nao entram no candidato): a correcao e' da outra frente (PEDIDOS_ENTRE_FRENTES_v411.md)"}
out["ok"] = not out["nao_verbatim"]
out.update(DL.MARCA_ENSAIO)
p = DL.saida("conferir_citacoes_v411.json")
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
print("citacoes « »:", sum(v_["n_citacoes"] for v_ in out["arquivos"].values()), "| verbatim:", sum(v_["n_ok"] for v_ in out["arquivos"].values()), "| NAO verbatim:", len(out["nao_verbatim"]))
for x_ in out["nao_verbatim"][:10]:
    print("  NAO VERBATIM:", x_)
sys.exit(0 if out["ok"] else (2 if out["ok_do_um_py"] else 1))   # (rc 2: so' o escopo do pos-rito reprova -- o candidato esta' limpo; o pedido e' da outra frente)
