# -*- coding: utf-8 -*-
"""varredura_fock_omega_v409.py -- (claude-construtor-v409, 05/11/2026 ~22h50; pedido da gerencia apos a R2 do Sonnet) VARREDURA, SO' LEITURA, de TODOS os textos que saem da preparacao da v409:
o core e o selo do ensaio, o .md canonico e os artigos PT/EN rendidos (dry_v409), os textos do pos-rito rendidos pelo harness (C:\\t\\h409\\harness_saida_v409: handoff, paragrafo do README/site, superficies, linhagem,
X), o rascunho do X, o relatorio, o plano, o deposito da fila e as fontes (delta, registros, runtime, artigos, textos do pos-rito, gerador, relatorio). Procura, no MESMO trecho (separado por . ; | quebra de linha, aspas
e o ponto mediano do grupo de estatuto), (a) «Fock» com OPEN/aberto/abert/pendente/«ainda nao»/«por fazer»/v410/v411 e (b) «Omega/Ω» com «uniforme» e OPEN/aberto. Classifica cada achado: HISTORICO (cita a E21,
a v407/v408 selada, «deixou», «dizia», «ficava», «era»; ou e' texto selado/herdado de versao anterior dentro do um.py) ou NOVO (a corrigir). Grava VARREDURA_FOCK_OMEGA_v409.json; rc 1 se ha' achado NOVO.
uso: python -I -B -X utf8 varredura_fock_omega_v409.py"""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
H = os.path.join("C:" + os.sep, "t", "h409", "harness_saida_v409")
ARQ = [os.path.join(HERE, "dry_v409", n_) for n_ in ("core_ensaio.json", "selo_ensaio.json", "um_absoluto_forma_canonica.md", "dry_v409_pt.txt", "dry_v409_en.txt")]
ARQ += sorted(p_ for p_ in glob.glob(os.path.join(H, "**", "*"), recursive=True) if os.path.isfile(p_) and p_.lower().endswith((".md", ".txt", ".json")) and os.path.getsize(p_) < 8 * 1024 * 1024 and "nos_emulado" + os.sep + "tgl_kernel" not in p_)
ARQ += [os.path.join(HERE, "pos_rito", "CUSTODIA_v409_RASCUNHO.txt"), os.path.join(HERE, "RELATORIO_PREPARACAO_v409.md"), os.path.join(HERE, "PLANO_v409.md"), os.path.join(HERE, "DEPOSITO_CONSTRUTOR_v409.md")]
ARQ += [os.path.join(HERE, n_) for n_ in ("delta_v409.py", "registros_v409.py", "runtime_v409.py", "artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "gerar_candidato_v409.py", "gerar_relatorio_v409.py", "depositar_construtor_v409.py",
                                          "fechar_preparacao_v409.py", "acom_inscrever_prep_v409.py", "guarda_frases_v409.py")]
ARQ += [os.path.join(HERE, "pos_rito", n_) for n_ in ("textos_v409_novo.pysnip", "textos_v409.py", "registrar_mapa_v409.py", "textos_custodia_handoff_v409.py", "gerar_x_custodia_v409.py", "leitura_v409.py")]
ARQ += sorted(glob.glob(os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "depositos", "claude-construtor-v409", "*.md")))[-1:]
ABERTO = re.compile(r"\bOPEN\b|\baberto\b|\baberta\b|\bem\s+abert|\bpendente|ainda\s+n[ãa]o|por\s+fazer|\bv41[0-9]\b|\bopen\b|\bpending\b|not\s+yet", re.I)
FOCK = re.compile(r"face\s+de\s+fock|par\s+de\s+fock|fock\s+face|parnafacedefock|par\s+(?:de\s+ps[ií]ons\s+)?no\s+fock|pair\s+(?:of\s+psions\s+)?on\s+the\s+fock", re.I)
OMEGA = re.compile(r"(?:ω|omega)[^.;]{0,80}?uniform", re.I)
HIST = ("e21", "v407", "v408", "deixou", "dizia", "ficava", "selad", "sealed", "historic", "histórico", "registro da época", "era [open]", "fecha como construcao", "fecha como construção", "fechou",
        "f41", "f40", "f42", "dito em aberto", "no mesmo trecho", "proibid", "forbidden", "_p409", "sonda", "probe", "reprova", "podad", "pruned", "inscri", "nao e' termo", "não é termo")
SEP = re.compile(r"[.;|\n\"«»·]")
# o que e' texto SELADO/HERDADO dentro do core/um.py (nao e' texto novo da v409): as chaves dos registros anteriores
CHAVES_V409 = ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409")


_BASE = os.path.join(HERE, "base_v408")
_NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N" + chr(243) + "s")
_HCORP = chr(10).join(open(p_, encoding="utf-8", errors="replace").read() for p_ in (os.path.join(_BASE, "um.py"), os.path.join(_BASE, "um_absoluto.json"), os.path.join(_BASE, "um_absoluto_selo.json"),
                                                                                    os.path.join(_NOS, "rodada_v408_stdout.txt")) if os.path.isfile(p_))
_HCORP_N = re.sub(r"\s+", " ", _HCORP)


def herdado(trecho_):
    t_ = re.sub(r"\s+", " ", trecho_.strip())
    return len(t_) >= 12 and t_ in _HCORP_N


def segmentos(t_):
    return [s_ for s_ in SEP.split(t_) if s_.strip()]


def varre_texto(t_):
    out_ = []
    for s_ in segmentos(t_):
        sl_ = s_.lower()
        f_ = bool(FOCK.search(sl_)) and bool(ABERTO.search(s_))
        o_ = bool(OMEGA.search(sl_)) and bool(ABERTO.search(s_))
        if f_ or o_:
            out_.append({"tipo": "fock" if f_ else "omega", "trecho": s_.strip()[:240], "historico": any(h_ in sl_ for h_ in HIST) or herdado(s_)})
    return out_


R = {"arquivos": 0, "achados": [], "recorte": "texto NOVO da v409: no core e no selo, so' as chaves da v409; no .md canonico, so' a linha da v409; nos artigos rendidos, so' a secao da v409; nas superficies do harness, so' o acrescimo sobre o .bak; o resto inteiro"}
for p_ in ARQ:
    if not os.path.isfile(p_) or ".bak_" in os.path.basename(p_) or (os.sep + "ensaio_superficies_limite" + os.sep) in p_:
        continue
    R["arquivos"] += 1
    t_ = open(p_, encoding="utf-8", errors="replace").read()
    b_ = os.path.basename(p_)
    if b_ in ("core_ensaio.json", "selo_ensaio.json") or (b_.startswith("um_absoluto") and b_.endswith(".json")):
        try:
            c_ = json.loads(t_)
        except ValueError:
            c_ = {}
        for k_ in [k_ for k_ in (c_ if isinstance(c_, dict) else {}) if "v409" in k_]:
            for a_ in varre_texto(json.dumps(c_.get(k_), ensure_ascii=False)):
                R["achados"].append(dict(a_, arquivo=p_ + "::" + k_))
        continue
    linhas_ = t_.split(chr(10)); idx_ = list(range(len(linhas_)))
    if b_.startswith("um_absoluto_forma_canonica") or b_.startswith("um_absoluto_manifest"):
        idx_ = [i_ for i_ in idx_ if "v409" in linhas_[i_]]
    elif (b_.startswith("dry_v409_") or b_.startswith("um_absoluto_")) and b_.endswith(".txt"):
        i0_ = next((i_ for i_ in idx_ if "05/11/2026" in linhas_[i_]), None)
        i1_ = next((i_ for i_ in idx_ if i0_ is not None and i_ > i0_ and "04/11/2026" in linhas_[i_]), len(linhas_))
        idx_ = list(range(max(0, i0_ - 3), i1_)) if i0_ is not None else []
    else:
        baks_ = sorted(glob.glob(p_ + ".bak_*"))
        if baks_:
            velhas_ = set(open(baks_[0], encoding="utf-8", errors="replace").read().split(chr(10)))
            if b_ == "MEMORY_2.md":   # a linha velha do MEMORY.md movida VERBATIM ao MEMORY_2.md e' historica
                for bk_ in sorted(glob.glob(os.path.join(os.path.dirname(p_), "MEMORY.md.bak_*")))[:1]:
                    velhas_ |= set(open(bk_, encoding="utf-8", errors="replace").read().split(chr(10)))
            idx_ = [i_ for i_ in idx_ if linhas_[i_] not in velhas_]
    if b_ == "guarda_frases_v409.py":   # META: as listas PROIBIDAS e LIMPAS sao a definicao da guarda (o controle negativo dela as testa)
        idx_ = []
    for i_ in idx_:
        for a_ in varre_texto(linhas_[i_]):
            R["achados"].append(dict(a_, arquivo="%s:%d" % (p_, i_ + 1)))
novos = [a_ for a_ in R["achados"] if not a_["historico"]]
R["n_achados"] = len(R["achados"]); R["n_novos"] = len(novos); R["n_historicos"] = R["n_achados"] - len(novos)
open(os.path.join(HERE, "VARREDURA_FOCK_OMEGA_v409.json"), "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1))
print("arquivos varridos:", R["arquivos"], "| achados:", R["n_achados"], "| historicos/citacao:", R["n_historicos"], "| NOVOS a corrigir:", len(novos))
for a_ in novos:
    print("NOVO", a_["tipo"], "|", a_["arquivo"].replace(HERE, "v409"), "|", a_["trecho"][:200])
sys.exit(1 if novos else 0)
