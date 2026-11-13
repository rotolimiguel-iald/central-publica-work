# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] REESCRITO para a v411 (o corpo da v410, subido por rotulo, fica em p00_precondicoes_v411.py.bak_20261112_085148_corpo_v410_bump e em bump\): uma versao sem modulo novo, com UM registro com funcao
"""p00_precondicoes_v411.py -- confere, SO LENDO, as pre-condicoes de bytes da v411 ANTES do candidato e antes de instalar. Nada e' escrito fora de PRECONDICOES_v411.json (nesta pasta). Os pinos sao LIDOS dos arquivos, nunca digitados.
Fail-closed: rc 1 se algo FALHA; rc 3 se NENHUMA FALHA mas ha' PENDENTES (o que so' passa a existir depois de outro passo da cadeia, ou e' ato da gerencia); rc 0 so' com TODAS PASSARAM. Uma checagem que levanta excecao vira FALHA visivel.
O que confere (DESENHO_v411 e as licoes D133/D135 da v410): (1) a base v410 selada; (2) o kernel do sandbox k411c (o da v410: fontes, raiz, Audit, log do Audit e linha TOTAL iguais; nenhuma bandeira nova); (3) os 18 insumos embutidos, os 7 citados,
os 5 textos da gerencia e as 9 falas: as copias duraveis em insumos\\ == as origens == o sha16 do DESENHO; (4) A GUARDA DE MATERIAL PRIVADO da E03 da G1 sobre TODOS os insumos pinados e as copias (D133: insumo que traga material privado
so' entra por copia limpa; aqui e' FALHA); (5) o veto: nenhum insumo nem citado vem da pasta do Kimi; (6) os ensaios da preparacao (o registro h0dn_bg1_v411 offline 16/16 com os controles negativos; a guarda de frases; o quadro e a secao
renderizados; o pre-voo do gerador); (7) D135: nenhum .tmp nesta pasta e nenhuma copia do kernel por rodada (imp_*, dry_*, falso_nos, arvore_simulada_*) dentro de work\\; (8) a marca de copia mecanica de rotulo (a de adaptar, com a versao entre colchetes; montada em partes mais abaixo, para o proprio p00 nao a trazer por extenso, o que paralisaria o passo 14 da cadeia) em arquivo da cadeia e' FALHA (copia
mecanica de rotulo nunca adaptada); (9) PENDENTES ditos: TOPO_RATIFICADO_v411.json (gerencia), o candidato e o que vem depois dele (ensaio, esperados, conferidores, citacoes, B20 pre-selo, harnesses), o pino do memoria.py e a folga do MEMORY.md
(gerencia). uso: python -B -X utf8 p00_precondicoes_v411.py"""
import datetime, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
res = []; ok_all = True; PEND = []


def chk(nome, cond, det=None):
    global ok_all
    ok_ = bool(cond); ok_all = ok_all and ok_
    res.append({"checagem": nome, "ok": ok_, "detalhe": det}); print(("OK   " if ok_ else "FALHA"), nome, ("" if ok_ else "| %s" % (str(det)[:300])))


def pend(nome, motivo):
    PEND.append({"checagem": nome, "motivo": motivo}); res.append({"checagem": nome, "ok": None, "pendente": motivo}); print("PEND ", nome, "|", motivo[:200])


def J(p):
    p = os.path.join(HERE, p)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def tenta(nome, fn):
    try:
        r_ = fn()
        chk(nome, r_[0] if isinstance(r_, tuple) else r_, r_[1] if isinstance(r_, tuple) else None)
    except Exception as e_:   # noqa: BLE001
        chk(nome, False, "excecao: %r" % (e_,))


# (1) a base
BC = J("BASE_V410_COPIA.json")
tenta("base_v410 = a v410 selada do DESENHO (copia de bytes conferida)", lambda: (BC is not None and BC["base_sha16"] == DL.BASE_SHA16_DA_ORDEM and sha(os.path.join(HERE, DL.BASE_DIR, "um.py"))[:16] == DL.BASE_SHA16_DA_ORDEM, BC and BC.get("base_sha16")))
# (2) o kernel
POS = J(os.path.join("kernel", "POS_BUILD_v411.json")); REC = J(os.path.join("kernel", "KERNEL_RECIBO_v411.json")); FL = J(os.path.join("kernel", "FLAGS_v411.json")); CF = J("CONFERENCIA_FONTES_K411C_v411.json")
tenta("kernel k411c: build incremental e Audit rc 0, nenhum modulo compilado, log do Audit com os bytes da v410, linha TOTAL da v410", lambda: (POS is not None and POS["ok"] is True and all(POS["criterios"].values()), POS and POS.get("criterios")))
tenta("kernel k411c: fontes identicas as do Nos v410 selado (nada so' num lado)", lambda: (CF is not None and CF["identico"] is True and CF["selo_um_version"] == "v410", CF and {k_: CF[k_] for k_ in ("n_comuns", "n_diferentes")}))
tenta("kernel: recibo rc 0, sem sorry e sem erro; nenhuma bandeira nova; escada = a da base", lambda: (REC is not None and REC["rc"] == 0 and REC["sorry"] == 0 and REC["erros"] == 0 and FL["n_flags"] == 0 and POS["escada"][0] == POS["escada"][1] == POS["E410"], (POS or {}).get("escada")))
# (3) os insumos e as copias
MI = J("MANIFESTO_INSUMOS_v411.json")
_NCOP = len(DL.INSUMOS_V411) + len(DL.CITADOS_V411) + len(DL.TEXTOS_DA_GERENCIA_CITADOS) + len(DL.FALAS_V411)   # (12/11: 18 + 7 + 6 + 11, lidas do delta)
tenta("as %d copias duraveis em insumos\\ == as origens (sha256), com os sha16 do DESENHO e do AO LADO de 12/11" % _NCOP, lambda: (MI is not None and MI["n"] == _NCOP and all(os.path.exists(c_["copia"]) and sha(c_["copia"]) == c_["sha256"] == sha(c_["origem"]) for c_ in MI["copias"]), MI and MI["n"]))
tenta("os 18 insumos do DESENHO existem e tem o sha16 dele (delta_v411, lido da tabela)", lambda: (len(DL.INSUMOS_V411) == 18 and all(sha(i_["arquivo"]) == i_["sha256"] for i_ in DL.INSUMOS_V411), len(DL.INSUMOS_V411)))
CG = J("VERBATIM_CONGELADO_v411.json")
tenta("a lista congelada das falas: %d (9 do DESENHO + 2 do AO LADO de 12/11), cada uma com o sha256 do arquivo" % DL.N_FALAS_V411, lambda: (CG is not None and CG["n"] == DL.N_FALAS_V411 == len(CG["registro"]) and all(sha(r_["arquivo"]) == r_["sha256"] for r_ in CG["registro"]), CG and CG["n"]))
# (4) a guarda de material privado (E03 da G1), sobre TODOS os insumos pinados e as copias
try:
    import guarda_material_privado_v411 as GMP
    _g = GMP.varrer(GMP.insumos_pinados())
    chk("GUARDA DE MATERIAL PRIVADO (a da E03 da G1: os termos da casa + o conjunto privado de marcadores) sobre os %d insumos pinados e copias: nenhum traz material privado (D133)" % _g["n_arquivos"], _g["limpo"] and _g["n_marcadores_privados"] > 0 and not _g["ilegiveis"],
        {"com_material_privado": _g["com_material_privado"], "n_marcadores": _g["n_marcadores_privados"]})
    _txt = sorted(glob.glob(os.path.join(HERE, "*.py")) + glob.glob(os.path.join(HERE, "*.md")) + glob.glob(os.path.join(HERE, "*.json")) + glob.glob(os.path.join(HERE, "pos_rito", "*.py")) + glob.glob(os.path.join(HERE, "orquestrador", "*.py")))
    _txt = [p_ for p_ in _txt if ".bak_" not in p_ and not p_.endswith(".tmp") and os.path.normcase(os.path.abspath(p_)) != os.path.normcase(os.path.abspath(DL.CANDIDATO_ARQ))]
    if os.path.exists(DL.CANDIDATO_ARQ):   # (o candidato herda as ocorrencias do um.py selado da v410: a checagem e' que NENHUMA e' nova; so' contagens, nada impresso)
        _oc = lambda p__: sum(int(a__.get("ocorrencias") or 0) for a__ in (GMP.varrer([p__]).get("arquivos") or []))
        _ob, _occ = _oc(os.path.join(HERE, DL.BASE_DIR, "um.py")), _oc(DL.CANDIDATO_ARQ)
        chk("a guarda de material privado sobre o CANDIDATO: nenhuma ocorrencia a mais que no um.py da v410 selada (o texto novo da v411 e' varrido limpo abaixo, em v411_pins.py e nos scripts)", _occ == _ob, {"base": _ob, "candidato": _occ})
    _g2 = GMP.varrer(_txt)
    chk("a mesma guarda sobre os %d scripts, textos e recibos desta pasta (registro da gerencia que possa virar insumo nao nomeia os confidenciais: D135 (5))" % _g2["n_arquivos"], _g2["limpo"], {"com_material_privado": _g2["com_material_privado"]})
except Exception as e_:   # noqa: BLE001
    chk("GUARDA DE MATERIAL PRIVADO carregada (a guarda de 7 termos sozinha e' fraca)", False, "excecao: %r" % (e_,))
# (5) o veto
tenta("VETO: nenhum insumo embutido nem citado vem de work\\h0dn_bg1_v410_09nov\\kimi\\", lambda: (not any(os.path.normcase(x_["arquivo"]).startswith(os.path.normcase(DL.H0DN_PASTA_VEDADA_V410)) for x_ in DL.INSUMOS_V411 + DL.CITADOS_V411), DL.H0DN_PASTA_VEDADA_V410))
# (6) os ensaios da preparacao
TO = J("TESTE_H0DN_OFFLINE_v411.json"); GFJ = J("GUARDA_FRASES_v411.json"); TQ = J("TESTE_QUADRO_v411.json"); PV = J("PREVOO_GERADOR_v411.json")
tenta("o registro h0dn_bg1_v411 offline: 16/16, o recalculo identico ao resultado da abertura, e cada controle negativo recusa", lambda: (TO is not None and TO["TUDO_PASSOU"] is True and TO["n_ok"] == DL.N_CHECKS_FECHO and all(v_.get("recusou") for k_, v_ in TO["controles_negativos"].items() if k_ != "guarda_de_frases_controle"),
                                                                                                                                 TO and {"n_ok": TO["n_ok"], "c6_max_dif": TO["c6_max_dif"]}))
tenta("a guarda de frases da v411: controle negativo (as proibidas reprovam, as certas passam, a fala do operador so' pela excecao)", lambda: (GFJ is not None and GFJ["controle_negativo"]["ok"] is True, GFJ and GFJ["n_proibidas"]))
tenta("o quadro, a remissao, a secao e o .md renderizados: sem n/d, sem unicode no LaTeX, as duas guardas limpas linha a linha; tirar as Cefeidas livres reprova", lambda: (TQ is not None and TQ["TUDO_PASSOU"] is True, None))
tenta("o pre-voo do gerador (todas as assercoes, as ancoras unicas, as guardas sobre o texto novo e o renderizado; nenhum candidato gravado)", lambda: (PV is not None and PV.get("ok") is True and not PV["guarda_frases"]["violacoes_no_texto_renderizado"] and PV["escada"] == [POS["E410"], POS["E410"]], PV and PV.get("sha16")))
# (7) D135: os .tmp e as copias do kernel por rodada fora de work\
_tmps = [p_ for p_ in glob.glob(os.path.join(HERE, "**", "*.tmp"), recursive=True)]
chk("D135 (3): nenhum .tmp na pasta da cadeia", not _tmps, _tmps[:5])
_copias = [d_ for d_ in os.listdir(HERE) if re.match(r"^(imp_|dry_|falso_nos|arvore_simulada_|sim_)", d_) and os.path.isdir(os.path.join(HERE, d_))]
chk("D135 (2): nenhuma copia do kernel por rodada (imp_*, dry_*, falso_nos, arvore_simulada_*, sim_*) dentro de work\\ (elas ficam em C:\\t\\k411c)", not _copias, _copias)
# (8) a marca de copia mecanica de rotulo (montada em partes, abaixo: o literal nao pode estar neste arquivo, porque o passo da cadeia que o roda PARA se o achar no script)
_marca = "[A ADAPTAR v" + "411]"
_marcados = sorted(os.path.relpath(p_, HERE) for p_ in glob.glob(os.path.join(HERE, "**", "*"), recursive=True) if os.path.isfile(p_) and ".bak_" not in p_ and os.sep + "bump" + os.sep not in p_ and not p_.endswith((".json", ".txt", ".diff", ".log", ".npz", ".lean", ".md"))
                    and os.path.basename(p_) not in ("_bump_copia_v411.py", "p00_precondicoes_v411.py") and _marca in open(p_, "rb").read().decode("utf-8", "replace"))
chk("nenhum arquivo da cadeia com a marca %s (copia mecanica de rotulo nunca adaptada)" % _marca, not _marcados, {"n": len(_marcados), "arquivos": _marcados})
# (8b) (R1, C-01) a checagem ESTATICA da cadeia do pos-rito: nenhum teste exercia o chain_pos_rito_v411.sh, e uma lista com um nome que nao existe so' apareceria DEPOIS do selo (o passo 0 PARARIA com a cadeia inteira por fazer). Confere, sem rodar nada:
# (a) `sh -n` passa no chain_pos_rito_v411.sh e no rito_v411.sh; (b) todo $PK/<arquivo> e $SEL/<arquivo> literal da lista do passo 0 e do laco do passo 1 existe em disco; (c) todo script Python ou shell que o chain invoca (com $PK/ ou $SEL/, fora do que ele proprio
# guarda com `[ -f ]` por ser opcional) existe e COMPILA (py_compile em memoria: nenhum .pyc e' gravado). Controle negativo: uma copia do script com um nome inexistente na lista do passo 0, outra no laco do passo 1 e outra com erro de sintaxe sao recusadas.
def _chain_estatico(chain_txt_, chain_path_=None):
    import shutil, subprocess, tempfile
    sh_ = shutil.which("sh") or r"C:\Program Files\Git\usr\bin\sh.exe"
    pk_ = HERE; sel_ = os.path.join(HERE, "pos_rito"); falhas_ = []
    def _sh_n(p_):
        return subprocess.run([sh_, "-n", p_], capture_output=True).returncode == 0
    with tempfile.TemporaryDirectory() as td_:
        pc_ = os.path.join(td_, "chain.sh"); open(pc_, "w", encoding="utf-8", newline="\n").write(chain_txt_.replace("\r\n", "\n"))
        if not _sh_n(pc_):
            falhas_.append("sh -n recusa o chain")
    m0_ = re.search(r'for f in (.*?); do\s*\n\s*\[ -f "\$f" \] \|\| parar "ferramenta/superficie ausente', chain_txt_, re.S)
    m1_ = re.search(r'for q in (.*?); do\s*\n\s*cp -p "\$PK/\$q"', chain_txt_, re.S)
    if not m0_ or not m1_:
        return False, ["a lista do passo 0 ou o laco do passo 1 nao foram achados no chain"]
    lst0_ = re.findall(r'"\$(PK|SEL)/([^"]+)"', m0_.group(1)); lst1_ = [("PK", q_) for q_ in m1_.group(1).split()]
    base_ = lambda v_: pk_ if v_ == "PK" else sel_
    for v_, rel_ in lst0_ + lst1_:
        if not os.path.exists(os.path.join(base_(v_), *rel_.split("/"))):
            falhas_.append("lista obrigatoria: $%s/%s nao existe" % (v_, rel_))
    opc_ = {(v_, r_) for v_, r_ in re.findall(r'\[ -f "\$(PK|SEL)/([^"]+)" \]', chain_txt_)}
    for v_, rel_ in sorted(set(re.findall(r'\$(PK|SEL)/([A-Za-z0-9_./-]+\.(?:py|sh))', chain_txt_)) | set(x_ for x_ in lst1_ if x_[1].endswith((".py", ".sh")))):
        p_ = os.path.join(base_(v_), *rel_.split("/"))
        if not os.path.exists(p_):
            if (v_, rel_) not in opc_:
                falhas_.append("script invocado: $%s/%s nao existe" % (v_, rel_))
            continue
        if rel_.endswith(".py"):
            try:
                compile(open(p_, "rb").read(), p_, "exec")
            except SyntaxError as e_:
                falhas_.append("script nao compila: $%s/%s (%s)" % (v_, rel_, e_.msg))
        elif not _sh_n(p_):
            falhas_.append("sh -n recusa: $%s/%s" % (v_, rel_))
    return not falhas_, falhas_


try:
    _ch_p = os.path.join(HERE, "pos_rito", "chain_pos_rito_v411.sh"); _ch_t = open(_ch_p, "rb").read().decode("utf-8")
    _ok_c1, _f_c1 = _chain_estatico(_ch_t, _ch_p)
    chk("(C-01) o chain_pos_rito_v411.sh: sh -n passa; todo $PK/ e $SEL/ da lista do passo 0 e do laco do passo 1 existe; todo script que ele invoca existe e compila", _ok_c1, _f_c1[:6])
    import tempfile as _tf, shutil as _sh_, subprocess as _sp
    _m0 = re.search(r'for f in (.*?); do\s*\n\s*\[ -f "\$f" \] \|\| parar', _ch_t, re.S); _m1 = re.search(r'for q in (.*?); do\s*\n\s*cp -p "\$PK/\$q"', _ch_t, re.S)
    _v0 = _ch_t.replace(_m0.group(1), _m0.group(1) + ' "$PK/runtime_v411_inexistente.py"', 1); _v1 = _ch_t.replace(_m1.group(1), _m1.group(1) + " runtime_v411_inexistente.py", 1); _v2 = _ch_t + "\nfi\n"
    _neg = {"nome_inexistente_na_lista_do_passo_0": _chain_estatico(_v0)[0], "nome_inexistente_no_laco_do_passo_1": _chain_estatico(_v1)[0], "erro_de_sintaxe_sh_n": _chain_estatico(_v2)[0]}
    chk("(C-01) controle negativo da checagem estatica do chain: uma copia com um nome inexistente na lista do passo 0, outra no laco do passo 1 e outra com erro de sintaxe sao RECUSADAS", all(v_ is False for v_ in _neg.values()) and _ok_c1, _neg)
    _sh = _sh_.which("sh") or r"C:\Program Files\Git\usr\bin\sh.exe"
    chk("(C-01) sh -n passa no rito_v411.sh", _sp.run([_sh, "-n", os.path.join(HERE, "rito_v411.sh")], capture_output=True).returncode == 0)
except Exception as e_:   # noqa: BLE001
    chk("(C-01) a checagem estatica do chain_pos_rito_v411.sh", False, "excecao: %r" % (e_,))
# (9) o topo ratificado, o candidato e o que vem depois dele (conferidos QUANDO existem; senao, PENDENTE com o passo que os produz)
_sha = lambda p_: sha(p_) if os.path.exists(p_) else None
if os.path.exists(DL.TOPO_RATIFICADO_ARQ) and not DL.ENSAIO_TOPO_PROPOSTO:
    tenta("TOPO_RATIFICADO_v411.json (a palavra do operador, D172/D173): o sha256 do arquivo == o lido pelo delta (a fonte unica do topo, 12 marcadores)", lambda: (sha(DL.TOPO_RATIFICADO_ARQ) == DL.TOPO_SHA256 and len(DL.MARCADORES_V411 or {}) == 12, DL.TOPO_SHA256))
elif not DL.ENSAIO_TOPO_PROPOSTO:
    pend("TOPO_RATIFICADO_v411.json (o texto do topo do resumo, com a palavra do operador; DESENHO 5.1 b e secao 8)", "ato da GERENCIA: sem ele o candidato nao e' gerado")
if not os.path.exists(DL.CANDIDATO_ARQ):
    pend("o candidato um_v411_candidato.py e o que vem depois dele (comparacao com a v410, ensaio a seco, ESPERADOS, conferidores, citacoes, diff e pinos, conferir_instalar_rito, fim_de_cadeia com o B20 pre-selo, harnesses)", "gerar_candidato_v411.py (so' depois do TOPO_RATIFICADO_v411.json)")
else:
    _c16 = sha(DL.CANDIDATO_ARQ)[:16]; CMJ = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8")) if os.path.exists(DL.MANIFESTO_ARQ) else {}
    tenta("o candidato e o manifesto dele: o sha16 do arquivo == o do manifesto; escada 12308 sem bandeira nova; o topo do manifesto e' o ratificado (sha256)", lambda: (CMJ.get("sha16") == _c16 and CMJ.get("escada") == [POS["E410"], POS["E410"]] and CMJ.get("n_bandeiras") == 0
                                                                                                                                                                and (DL.ENSAIO_TOPO_PROPOSTO or (CMJ.get("topo") or {}).get("sha256") == DL.TOPO_SHA256), {"sha16": _c16, "manifesto": CMJ.get("sha16")}))
    # (R1, 12/11 noite, D181) a GUARDA DA CONVERSA sobre o candidato: as 11 falas da casa (o texto inteiro, cada linha de 24 caracteres ou mais, as linhas curtas alem da base v410, os nomes dos arquivos) tem 0 ocorrencias no fonte;
    # controle negativo dos dois lados (uma copia com linha plantada, com nome plantado e com linha curta alem da base e' recusada; o candidato limpo passa). Os textos das falas sao lidos da casa so' aqui, na preparacao.
    try:
        import guarda_conversa_v411 as GC
        _al = {"um_py": open(DL.CANDIDATO_ARQ, "rb").read()}
        _gv = GC.verificar(_al); _gn = GC.controle_negativo(_al, limpo_=_gv)
        _gj = {"contrato": "GUARDA_CONVERSA_v411", "modo": "p00 (o fonte do candidato)", "candidato_sha16": _c16, "ok": bool(_gv["ok"] and _gn["ok"]), "limpo": bool(_gv["ok"]), "n_achados": len(_gv["achados"]), "achados": _gv["achados"][:20], "informativo": _gv["informativo"][:20],
               "controle_negativo": _gn, "n_agulhas": _gv["n_agulhas"], "alvos": _gv["alvos"], "nota": "nenhum texto de fala neste arquivo: so' indice, sha16 da linha, tamanho, alvo e contagem; os insumos pinados em base64 (a pre-registro publicado e os recibos) trazem nomes de arquivo por dentro e nao sao varridos aqui"}
        open(DL.saida("GUARDA_CONVERSA_v411.json") + ".tmp", "w", encoding="utf-8").write(json.dumps(_gj, ensure_ascii=False, indent=1)); os.replace(DL.saida("GUARDA_CONVERSA_v411.json") + ".tmp", DL.saida("GUARDA_CONVERSA_v411.json"))
        chk("(D181) a GUARDA DA CONVERSA sobre o CANDIDATO: as 11 falas da casa tem 0 ocorrencias no fonte (texto inteiro e linhas de 24+), as linhas curtas nao passam da base v410, os nomes dos arquivos tem 0; controle negativo dos dois lados", _gj["ok"], {"n_achados": _gj["n_achados"], "controle_negativo_ok": _gn.get("ok")})
    except Exception as e_:   # noqa: BLE001
        chk("(D181) a GUARDA DA CONVERSA sobre o CANDIDATO", False, "excecao: %r" % (e_,))
    _DEPOIS = [("ensaio_a_seco_v411.json", "ensaio_a_seco_v411.py", lambda j_: j_.get("veredito") == "TUDO PASSOU" and j_.get("sha16") == _c16),
               ("ESPERADOS_v411.json", "gerar_esperados_v411.py", lambda j_: j_.get("candidato_sha16") == _c16),
               ("conferencia_rito_v411_CONTROLE_NEGATIVO_PRE_RITO.json", "conferir_rito_v411.py --controle-negativo", lambda j_: j_.get("tudo_bate") is False),
               ("conferencia_rito_v411_POSITIVO_FALSO_NOS.json", "teste_conferidor_positivo_v411.py", lambda j_: j_.get("tudo_bate") is True and j_.get("um_py_sha16") == _c16),
               ("conferir_citacoes_v411.json", "conferir_citacoes_v411.py --candidato", lambda j_: j_.get("ok_do_um_py") is True),
               ("DERIVACAO_v411.json", "conferir_instalar_rito_v411.py", lambda j_: not j_.get("falhas")),
               ("PINOS_BN_v411.json", "diff_e_pinos_v411.py", lambda j_: ((j_.get("candidato") or {}).get("sha256") or "")[:16] == _c16)]
    for _arq, _passo, _ok in _DEPOIS:
        _p = DL.saida(_arq)
        if os.path.exists(_p):
            tenta("%s (de %s) e' deste candidato e passou" % (_arq, _passo), (lambda p__=_p, ok__=_ok: (bool(ok__(json.load(open(p__, encoding="utf-8")))), os.path.basename(p__))))
        else:
            pend("%s (o passo %s ainda nao rodou para este candidato)" % (_arq, _passo), "passo da cadeia (cadeia_v411.sh)")
    _cj = DL.saida("conferir_citacoes_v411.json")
    if os.path.exists(_cj) and json.load(open(_cj, encoding="utf-8")).get("ok_do_pos_rito") is False:
        pend("as citacoes em «» do escopo do pos-rito (pos_rito\\*_v411*: a outra frente) nao sao todas fala verbatim do operador", "pedido a frente pos-rito em PEDIDOS_ENTRE_FRENTES_v411.md (o escopo do um.py esta' limpo; o relatorio final exige os dois)")
if not os.path.exists(os.path.join(HERE, "PINO_MEMORIA_PY_v411.json")):
    pend("PINO_MEMORIA_PY_v411.json (o pino do memoria.py)", "ato da GERENCIA (pino_memoria_py_v411.py)")
# (G1, integracao de 12/11) a folga e o pino do MEMORY.md deixam de ser pendente INCONDICIONAL e viram CONFERENCIA (so' leitura; nada e' escrito na pasta de memoria): OK se (i) `memoria.py verificar` (MEMORIA_GERENCIA=claude-c1, diretorio corrente = fila, rc 0 e "ok": true) e (ii) o indice, depois da troca da linha da missao e da linha nova do handoff
# como pos_rito\superficies_v411.py as monta (as MESMAS funcoes do textos_v411: marca_missao e linha_handoff), fica em ate 24.000 B e 195 quebras de linha; senao PENDENTE com os numeros medidos (a gerencia decide o que sai do indice).
def _memory_md_conferido(idx_override=None):
    import subprocess, importlib.util as _ilu
    mem = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory"); fila = os.path.join(mem, "fila"); idx = os.path.join(mem, "MEMORY.md")
    idx = idx_override or idx   # (R1, C-05: o controle negativo aponta uma COPIA do indice; nada e' escrito)
    env = dict(os.environ); env["MEMORIA_GERENCIA"] = "claude-c1"
    r = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(fila, "memoria.py"), "verificar"], cwd=fila, env=env, capture_output=True, timeout=300)
    try:
        vj = json.loads(r.stdout.decode("utf-8"))
    except Exception:   # noqa: BLE001
        vj = {}
    ver_ok = bool(r.returncode == 0 and vj.get("ok") is True) or bool(idx_override)   # (no controle so' o limite do indice e' exercitado)
    raw = open(idx, "rb").read()
    if b"\r\n" in raw:
        return False, {"verificar_rc": r.returncode, "motivo": "MEMORY.md com CRLF: o molde das superficies espera LF"}
    sp = _ilu.spec_from_file_location("textos_v411_p00", os.path.join(HERE, "pos_rito", "textos_v411.py")); T = _ilu.module_from_spec(sp); sp.loader.exec_module(T)
    s16_ = sha(DL.CANDIDATO_ARQ)[:16] if os.path.exists(DL.CANDIDATO_ARQ) else "0" * 16
    Vx = {"data": datetime.date.today().strftime("%d/%m/%Y"), "s16": s16_, "teor": "%d/%d" % (POS["E410"], POS["E410"])}
    lines = raw.decode("utf-8").split("\n")
    if any(("v411 SELADA" in l_ and Vx["s16"] in l_) for l_ in lines):
        novo = raw; ja = True   # o indice ja traz a linha da v411 (idempotente, como a superficie)
    else:
        ja = False
        k_ = [i_ for i_, l_ in enumerate(lines) if "(missao-ultima-flag-um-py.md)" in l_ and l_.startswith("- [")]
        h_ = [i_ for i_, l_ in enumerate(lines) if "(handoff-v410-custodia.md)" in l_ and l_.startswith("- [")]
        assert len(k_) == 1 and len(h_) == 1, ("ancoras do indice (missao, handoff da v410)", len(k_), len(h_))
        lines[k_[0]] = "- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — " + T.marca_missao(Vx) + "íntegra anterior no MEMORY_2.md (movida %s)" % Vx["data"][:5]
        lines.insert(h_[0], T.linha_handoff(Vx))
        novo = "\n".join(lines).encode("utf-8")
    med = {"verificar_rc": r.returncode, "verificar_ok": vj.get("ok"), "verificar_violacoes": vj.get("violacoes"), "indice_hoje_linhas_bytes": [raw.count(b"\n"), len(raw)], "indice_projetado_linhas_bytes": [novo.count(b"\n"), len(novo)], "limites_linhas_bytes": [195, 24000], "ja_tem_a_linha_da_v411": ja}
    return bool(ver_ok and len(novo) <= 24000 and novo.count(b"\n") <= 195), med


try:
    _mm_ok, _mm = _memory_md_conferido()
except Exception as e_:   # noqa: BLE001
    _mm_ok, _mm = False, {"excecao": repr(e_)}
if _mm_ok:
    chk("a folga do MEMORY.md para a linha do handoff da v411 e o pino do MEMORY.md (CONFERIDOS: memoria.py verificar ok; o indice projetado cabe em 24000 B e 195 linhas)", True, _mm)
else:
    pend("a folga do MEMORY.md para a linha do handoff da v411 e o pino do MEMORY.md (a conferencia nao deu OK: medido %s)" % json.dumps(_mm, ensure_ascii=False), "ato da GERENCIA (a fila da memoria; so' a c1 escreve o indice): abrir a folga ou refazer o pino e rodar de novo")
# (R1, C-05) o controle negativo da conferencia do MEMORY.md: uma COPIA do indice com 196 linhas ou mais tem de dar PENDENTE (o limite e' 195 linhas e 24.000 B); nada e' escrito no indice
try:
    import tempfile as _tf2
    _raw_idx = open(os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md"), "rb").read()
    with _tf2.TemporaryDirectory() as _td2:
        _p196 = os.path.join(_td2, "MEMORY.md"); open(_p196, "wb").write(_raw_idx + b"- linha de controle (copia do indice; nada e' escrito no real)\n" * (max(0, 196 - _raw_idx.count(b"\n")) + 8))
        _c05_ok, _c05_med = _memory_md_conferido(_p196)
    chk("(C-05) controle negativo da conferencia do MEMORY.md: uma COPIA do indice com 196 linhas ou mais da PENDENTE (o limite e' 195 linhas e 24.000 B)", _c05_ok is False, {"indice_projetado_linhas_bytes": _c05_med.get("indice_projetado_linhas_bytes")})
except Exception as e_:   # noqa: BLE001
    chk("(C-05) controle negativo da conferencia do MEMORY.md", False, "excecao: %r" % (e_,))
_v = "TODAS PASSARAM" if (ok_all and not PEND) else ("NENHUMA FALHA, %d PENDENTE(S)" % len(PEND) if ok_all else "FALHOU")
out = {"contrato": "PRECONDICOES_v411", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "veredito": _v, "n_checagens": len(res), "n_ok": sum(1 for r_ in res if r_.get("ok") is True),
       "n_falhas": sum(1 for r_ in res if r_.get("ok") is False), "n_pendentes": len(PEND), "pendentes": PEND, "checagens": res}
out.update(DL.MARCA_ENSAIO)
p = DL.saida("PRECONDICOES_v411.json")   # (pedido do fork B: no ensaio do topo proposto, na pasta de ensaio)
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
print(_v, "| %d ok, %d falha(s), %d pendente(s)" % (out["n_ok"], out["n_falhas"], out["n_pendentes"]))
sys.exit(0 if _v == "TODAS PASSARAM" else (3 if ok_all else 1))
