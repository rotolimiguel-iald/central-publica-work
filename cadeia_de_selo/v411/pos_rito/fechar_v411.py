# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-sonnet-posrito-L-v411, a servico do claude-construtor-v411] ao DESENHO_v411 e aos AO LADO de 12/11: o teste H0DN x BG1 ABERTO UMA VEZ (D169) e o resultado RECALCULADO no rito; NENHUM modulo novo de kernel (o bundle e' vazio; o kernel e a escada sao os da v410); UM registro com funcao (h0dn_bg1_v411, 16 checagens: V['fecho'])
# e dois por spec (cunhagens_v411, kh_n1_cobertura_v411); os QUATRO registros com funcao da v410 e os dois por spec da v410 sao RECRIADOS e selados (V['reg410_recriados']). O fechar exige, ANTES de escrever qualquer coisa, V['fecho'] selado com as duas linhas (o primario e as Cefeidas livres), as sete ressalvas e o que o teste nao decide; os recriados selados; V['n_pedras'] == 0.
# O manifesto ganha registros_v411 (os tres novos), registros_v410 (os seis recriados), registros_funcao_v411 (h0dn_bg1_v411), registros_funcao_v410 (os quatro da v410) e h0dn_bg1_v411_resumo (lido do core selado; nada digitado); as chaves de V mudaram de sentido com o deslocamento de versao (V['ancoras410'] e V['bundle410'] sao os da v410; V['ancoras409'] e V['bundle409'], os da traducao).
# O handoff vem de textos_v411.handoff(V, k) (SEM os blocos da custodia: NOTA_EN_v411, README_*, ESTATUTO_P2_*, que textos_custodia_handoff_v411.py anexa depois): o fechar recusa o que nao diga o registro com funcao, os da v410 recriados, as sete ressalvas por rotulo e o que o teste nao decide, ou que traga a frase velha da v410 («pre-registrado; nenhum dado observado lido»), um token proibido ou o que a D65 deixa fora.
"""fechar_v411.py -- DEPOIS da cadeia pos-rito e do elo B(n) (molde: fechar_v410.py FINAL): (1) o manifesto de incorporacao v411 -> pos_rito e a pasta das ferramentas;
(2) o ARQUIVO: o indice por sha256 de tudo o que esta na pasta da cadeia (work\\cadeia_de_selo\\v411 -- aqui o pacote JA mora na casa duravel, nao ha copia do pacote), a copia de pos_rito -> work\\cadeia_de_selo\\v411_selo, A COPIA DO SIDECAR um_absoluto_selo_acom.json (reescrito pelo rito) E DO SELO PRIMARIO para a mesma pasta,
e do kernel (work\\cadeia_de_selo\\v411\\kernel e, se existir, work\\v411_kernel; a v411 nao tem modulo novo: so' a raiz e o Audit, que sao os da v410) -> work\\cadeia_de_selo\\v411_kernel;
(3) os DOIS DIFFS para o auditor independente: DIFF_v410_v411.diff (um.py da base x o selado, GNU diff -U2) e DIFF_KERNEL_v411.txt (o kernel embutido: nenhum modulo novo; a raiz e o Audit iguais);
(4) o HANDOFF (memory\\handoff-v411-custodia.md + Nos\\HANDOFF_v411_CUSTODIA.md) para a sessao de custodia, que TRAZ PRONTOS PARA COLAR OS DOIS PARAGRAFOS do README do espelho e do site: (a) o do QUADRO «O Teste da Unica Palavra» (v397, intocado), gerado pelas MESMAS funcoes do quadro do artigo (quadro_v397.paragrafo_pronto_readme)
sobre o core SELADO do Nos, mesmos numeros e estatutos; (b) o NOVO, o paragrafo da v411 (o teste decisivo: a razao de Hubble, H0DN x BG1, aberta uma vez), gerado do registro selado h0dn_bg1_v411 (numeros LIDOS do core; as duas linhas juntas; as sete ressalvas; o que o teste nao decide; as falas do operador de 12/11 verbatim; as quatro obrigacoes da guarda no mesmo bloco).
GUARDAS: a leitura sem problema (inclui o sidecar); o PARAGRAFO DO QUADRO passa nas verificacoes do quadro contra o resultado pinado (quadro_v397.confere_md e a regra da ordem: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item; frase do operador verbatim; numeros iguais aos do resultado); o PARAGRAFO NOVO passa na verificacao propria
(T.verificar_paragrafo_v411: numeros == o registro do core; sem o 4,44; estatutos; limites; citacoes verbatim das falas do operador; sem alegacao de seguranca criptografica; D65; guarda P18 e guarda das frases); se QUALQUER um nao passar, o fechar RECUSA (rc 2) ANTES de escrever qualquer coisa e o handoff nao nasce; os tres RECIBOS do B(n) (o RECIBO_SINCRONIZACAO_v411_*.json do 10-bis,
o recibo da PARADA do servico e o do RELIGAMENTO) -- sem eles o fechar RECUSA; a guarda de texto P18 e a guarda das frases no handoff; D169 (12/11): V['fecho'] selado, aberto uma vez, com as duas linhas; o handoff dizendo o registro e os recriados, sem a frase velha da v410; D65: o handoff nao traz o que a fala do nome do algoritmo deixa fora.
v411 (FILA DA MEMORIA): o diretorio de memoria e' parametrizado por V411_MEMORIA_DIR (padrao: o REAL; no ensaio, uma COPIA); o manifesto REGISTRA (so' informa, nao recusa) o estado da fila ao fechar: sha256 do memoria.py, do MEMORY.md e do PINO_MEMORY.json, se o pino confere com o indice, se a pausa do vigia sumiu.
Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""
import glob, hashlib, json, os, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v411 as L
import textos_v411 as T
from guarda_p18_v411 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V411"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v411 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
V, PROB = L.ler()
if PROB:
    print("FECHAR RECUSADO:", PROB); sys.exit(2)
# ---------------------------------------------------------------- (0') v411 (12/11/2026, D169): o UNICO registro com FUNCAO, h0dn_bg1_v411 (o teste H0DN x BG1 aberto uma vez, RECALCULADO no rito): a leitura o selou (V['fecho']), com as DUAS linhas, as sete ressalvas e as 16 checagens; os registros da v410 (os quatro com funcao e os dois por spec) estao RECRIADOS e selados
# (V['reg410_recriados']); NENHUM modulo novo (V['n_pedras'] == 0, bundle vazio, escada igual); o resumo que o manifesto leva e' LIDO do core selado do Nos; sem isso, RECUSA (rc 2) ANTES de escrever qualquer coisa
_core_ = json.load(open(os.path.join(L.NOS, "um_absoluto.json"), encoding="utf-8")).get("core") or {}
import delta_v411 as DLR   # os nomes dos registros vem de delta_v411 (REGISTROS_FUNCAO == [h0dn_bg1_v411]; REGISTROS_FUNCAO_V410 = os quatro com funcao da v410)
_H = V.get("fecho") or {}; _hc = _core_.get(DLR.FECHO_REGISTRO) or {}; _hv = _hc.get("values") or {}; _hp = _hv.get("primario") or {}; _hcl = _hv.get("cefeidas_livres") or {}
if not (list(L.REG_FUNCAO) == list(DLR.REGISTROS_FUNCAO) == [DLR.FECHO_REGISTRO] and isinstance(V.get("fecho"), dict) and isinstance(V.get("reg410_recriados"), dict)):
    print("FECHAR RECUSADO: a leitura nao traz o registro com funcao da v411 (V['fecho']) e os recriados da v410 (V['reg410_recriados']; delta_v411.REGISTROS_FUNCAO):", list(DLR.REGISTROS_FUNCAO)); sys.exit(2)
if not (_H.get("sealed") is True and _H.get("ok") is True and _H.get("opened_once") is True and _H.get("observed_vector_read") is True and _hc.get("all_verified") is True and _hc.get("opened_once") is True and _hc.get("runtime_executed") is True and _hc.get("does_not_gate_core") is True
        and (_hc.get("mechanics") or {}).get("n_checks") == DLR.N_CHECKS_FECHO and _hp and _hcl and len(_hc.get("ressalvas_secao8") or []) == 7 and len(_hc.get("o_que_o_teste_nao_decide") or []) == 5 and _hc.get("cabeca_do_teste") == _hp.get("cabeca_do_teste")):
    print("FECHAR RECUSADO: o registro h0dn_bg1_v411 (o teste H0DN x BG1 aberto uma vez, D169; as duas linhas, as sete ressalvas, o que o teste nao decide) nao esta selado na leitura (V['fecho']) ou no core do Nos, ou nao diz que foi aberto uma vez, ou nao traz as duas linhas:", {k_: _H.get(k_) for k_ in ("sealed", "ok", "opened_once", "stdout_ok", "selo_ok", "guarda_ok", "ressalvas_ok", "duas_linhas_ok", "gate_ok", "emenda_ok")}); sys.exit(2)
if not (V.get("n_pedras") == 0 and not V.get("pedras") and V.get("escada_antes") == V.get("escada_depois") and all(((V["reg410_recriados"].get(n_) or {}).get("sealed") is True) for n_ in L.REG_RECRIADOS_V410) and all(V.get(k_, {}).get("ok") is True for k_ in ("bundle410", "bundle409", "bundle408", "bundle407", "bundle406"))):
    print("FECHAR RECUSADO: a v411 nao tem modulo novo de kernel (V['n_pedras'] = 0, escada igual) e os seis registros da v410 (quatro com funcao e dois por spec) tem de estar RECRIADOS e selados, com os bundles anteriores no kernel:", {n_: (V["reg410_recriados"].get(n_) or {}).get("sealed") for n_ in L.REG_RECRIADOS_V410}); sys.exit(2)
H0DN_RESUMO = {"registro": DLR.FECHO_REGISTRO, "verdict": _hc.get("verdict"), "outcome": _hc.get("outcome"), "cabeca_do_teste_sha16": hashlib.sha256(str(_hc.get("cabeca_do_teste")).encode("utf-8")).hexdigest()[:16], "opened_once": _hc.get("opened_once"), "observed_vector_read": _hc.get("observed_vector_read"), "n_checks": (_hc.get("mechanics") or {}).get("n_checks"),
               "primario": {k_: _hp.get(k_) for k_ in ("modelo", "t", "z_null", "z_tgl", "D", "p_unilateral", "ramo", "outcome")}, "cefeidas_livres": {k_: _hcl.get(k_) for k_ in ("modelo", "t", "z_null", "z_tgl", "D", "ramo", "outcome")}, "lei_em_km_s_Mpc": _hv.get("lei_em_km_s_Mpc"), "atos": _hv.get("atos"),
               "n_ressalvas": len(_hc.get("ressalvas_secao8") or []), "rotulos_das_ressalvas": _hc.get("rotulos_das_sete_ressalvas"), "o_que_o_teste_nao_decide": _hc.get("o_que_o_teste_nao_decide"), "insumos_sha16": {k_: str((v_ or {}).get("sha256"))[:16] for k_, v_ in (_hc.get("insumos_pinados") or {}).items()},
               "contratos_de_registro_fora_da_escada": _hc.get("contratos_de_registro_fora_da_escada"), "gate_verdict": _hv.get("gate_verdict"), "escada": _hv.get("escada"),
               "nota": "lido do core selado do Nos (nada digitado); o teste foi aberto uma vez, depois do commit publico do pre-registro; sob o modelo de erros publicado, com a linha das Cefeidas livres ao lado; retrodicao sem ajuste, teste nao cego; validade, nao creditacao; o gate nao se move"}
# ---------------------------------------------------------------- (0) os PARAGRAFOS PRONTOS do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO), as MESMAS funcoes do quadro do artigo sobre o core SELADO do Nos; (2) o paragrafo NOVO da v411 (a IALD2), gerado dos registros selados e verificado contra o core e contra ESPERADOS (sem o 4,44; citacoes verbatim das falas do operador ou do kernel embutido; sem alegacao de seguranca criptografica); os do testemunho de dois (v399), da falsidade (v401), da v402, da v403, da v404 e os da v405 a v410 SEGUEM COMO ESTAO e nao sao regenerados;
# sem passar nas verificacoes, RECUSA (rc 2) ANTES de escrever qualquer coisa
try:
    PAR, PAR_INFO = T.paragrafo_readme()
    PAR_F, PAR_F_INFO = T.paragrafo_v411()   # (o handoff de textos_v411 o recebe como readme_paragrafo_v411)
except BaseException as e_:   # noqa: BLE001
    print("FECHAR RECUSADO: um dos paragrafos prontos do README e do site (o quadro O Teste da Unica Palavra, v397, ou o da v411: a IALD2) nao passou nas verificacoes (regra da ordem do 4,44; frase verbatim; numeros iguais aos do resultado pinado e aos de ESPERADOS; citacoes verbatim; sem alegacao de seguranca criptografica):", repr(e_)[:700]); sys.exit(2)
# o SIDECAR (arquivo NOVO da custodia, D5): a leitura ja' o conferiu (existe, JSON valido, selado, tres objetos com o SHA-256 dos arquivos do Nos); aqui so' o resumo que o manifesto e o handoff levam
if not (V["sidecar"]["ok"] is True and os.path.isfile(os.path.join(L.NOS, "um_absoluto_selo_acom.json"))):
    print("FECHAR RECUSADO: o sidecar um_absoluto_selo_acom.json nao esta selado ou nao existe no Nos:", V["sidecar"].get("erro")); sys.exit(2)
SC_INFO = {"arquivo": "um_absoluto_selo_acom.json", "sha256": V["sidecar"]["sha256"], "bytes": V["sidecar"]["bytes"], "veredito": V["sidecar"]["veredito"], "esquema": V["sidecar"]["esquema"], "recusas": V["sidecar"]["recusas"],
           "objetos": {n_: {"bytes": o_["bytes"], "sha256": o_["sha256"]} for n_, o_ in V["sidecar"]["objetos"].items()}}
NOS = L.NOS; WK = os.path.dirname(os.path.dirname(PK)); TOOLS = os.path.join(WK, "cadeia_de_selo")
MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
UMEM = os.path.abspath(os.environ.get("V411_MEMORIA_DIR", "").strip() or MEM_REAL)   # v411 (fila da memoria): a pasta de memoria e' parametrizada por V411_MEMORIA_DIR (padrao: a REAL; no ensaio, uma COPIA)
ST = time.strftime("%Y%m%d_%H%M%S"); s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]; s64 = lambda b: hashlib.sha256(b).hexdigest()
DIRS_B3 = os.path.join(PK, "bancada_B3"); DIRS_SERV = os.path.join(PK, "bancada_B3_servico")


def _j(p):
    return json.load(open(p, encoding="utf-8"))


# ---------------------------------------------------------------- 0. os tres recibos do B(3): sem eles, nao fecha
def recibos_b3():
    prob = []; out = {}
    # a pasta do aplicar e' nova a cada tentativa (bancada_B3, bancada_B3_2, ...); o ensaio (bancada_B3_ensaio_*) NAO conta
    ap = sorted(glob.glob(os.path.join(DIRS_B3, "RECIBO_SINCRONIZACAO_v411_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v411_*.json")), key=os.path.getmtime)
    if not ap:
        prob.append("sem o RECIBO_SINCRONIZACAO_v411_*.json do 10-bis em %s (nem em bancada_B3_<n>)" % DIRS_B3)
    else:
        r = _j(ap[-1])
        if not (str(r.get("veredito") or "").startswith("REPINADA_B") and "__SALTO_" not in str(r.get("veredito") or "") and r.get("salto") in (None, {}) and r.get("modo") == "aplicar" and r.get("fase") == "pos_selo" and r.get("versao_alvo") == "v411"
                and (r.get("bateria_resultado") or {}).get("veredito") == "BATERIA_PASSA" and r.get("aplicacao")):
            prob.append("o recibo do 10-bis nao e' de uma aplicacao pos_selo v411 com a bateria passando: %s" % os.path.basename(ap[-1]))
        out["aplicar"] = {"path": ap[-1], "sha256": s64(open(ap[-1], "rb").read()), "veredito": r.get("veredito"), "manifesto_novo_sha256": (r.get("manifesto_novo") or {}).get("sha256"),
                          "evento": ((r.get("evento_c1") or {}).get("evento")), "bateria": (r.get("bateria_resultado") or {}).get("veredito")}
    pp = os.path.join(DIRS_SERV, "RECIBO_PARADA_v411.json"); rp = os.path.join(DIRS_SERV, "RECIBO_RELIGAMENTO_v411.json")
    if not os.path.exists(pp):
        prob.append("sem o recibo da PARADA do servico (10-bis-a): %s" % pp)
    else:
        d = _j(pp); pid = d.get("pid") or d.get("pids") or d.get("PID"); fech = d.get("porta_fechada") or d.get("fechada"); hora = d.get("hora") or d.get("quando")
        if not (pid and fech is True and d.get("porta") == 18777 and hora):
            prob.append("o recibo da parada nao traz pid, porta 18777, porta_fechada true e hora")
        out["parada"] = {"path": pp, "sha256": s64(open(pp, "rb").read()), "hora": hora, "pid": pid}
    if not os.path.exists(rp):
        prob.append("sem o recibo do RELIGAMENTO do servico (10-ter): %s" % rp)
    else:
        d = _j(rp); vs = d.get("versao_servida") or d.get("versao"); msha = d.get("manifesto_sha256")
        esperado = (out.get("aplicar") or {}).get("manifesto_novo_sha256")
        if not (vs == "v411" and msha and esperado and msha == esperado and (d.get("pid") or d.get("PID")) and (d.get("hora") or d.get("quando"))):
            prob.append("o recibo do religamento nao traz versao servida v411, o sha do manifesto novo do recibo do 10-bis, pid e hora")
        out["religamento"] = {"path": rp, "sha256": s64(open(rp, "rb").read()), "versao_servida": vs, "manifesto_sha256": msha}
    return out, prob


B3, PB3 = recibos_b3()
if PB3:
    print("FECHAR RECUSADO -- o elo B(3) da Bancada nao esta completo (R3, Remissao 4):")
    for x in PB3:
        print("  -", x)
    print("  (a cadeia para em AGUARDA_OPERADOR ate a palavra do operador para a B3; depois rodar a cadeia a partir do passo 11)"); sys.exit(2)


def grava(p, b):
    if os.path.exists(p):
        if open(p, "rb").read() == b:
            print("  igual:", p); return
        raw = open(p, "rb").read(); bk = p + ".bak_" + ST + "_f407"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp_f411_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b; print("  gravado:", p, len(b), "B")


# ---------------------------------------------------------------- (3) os dois diffs (antes do manifesto, para entrarem nele)
def carregar_embutido(path):
    import ast
    text = open(path, "rb").read().decode("utf-8"); lines = text.splitlines(keepends=True)
    i0 = [i for i, l in enumerate(lines) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]; assert len(i0) == 1, i0
    j = i0[0] + 1
    while lines[j].rstrip("\r\n") != "}":
        j += 1
    return ast.literal_eval("".join(lines[i0[0]:j + 1]).split("=", 1)[1].strip())


um = os.path.join(NOS, "um.py"); base = V["base_backup"]
assert os.path.exists(base) and s16(base) == V["base16"], "o backup da base (APLICADO_AO_CANONICO) nao e' a v410 selada: " + base
print("(3) diffs")
exe = shutil.which("diff")
if exe:
    r = subprocess.run([exe, "-U", "2", "--label", "um.py v410 %s" % V["base16"], "--label", "um.py v411 %s" % V["s16"], base, um], capture_output=True)
    assert r.returncode == 1, "diff rc=%s: %s" % (r.returncode, r.stderr[:200])
    dd = r.stdout
else:
    import difflib
    a = open(base, "r", encoding="utf-8", newline="").read().splitlines(); b = open(um, "r", encoding="utf-8", newline="").read().splitlines()
    dd = ("\n".join(difflib.unified_diff(a, b, "um.py v410 %s" % V["base16"], "um.py v411 %s" % V["s16"], lineterm="", n=2)) + "\n").encode("utf-8")
grava(os.path.join(PK, "DIFF_v410_v411.diff"), dd)
import difflib
E0 = carregar_embutido(base); E1 = carregar_embutido(um)
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v410 (%s) -> v411 (%s)" % (V["base16"], V["s16"]), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, s64(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
for k in mudados:
    a_, b_ = E0[k].splitlines(), E1[k].splitlines(); d_ = list(difflib.unified_diff(a_, b_, "v410/" + k, "v411/" + k, lineterm="", n=0))
    out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, s64(E0[k].encode())[:16], s64(E1[k].encode())[:16], sum(1 for l in d_ if l.startswith("+") and not l.startswith("+++")),
                                                         sum(1 for l in d_ if l.startswith("-") and not l.startswith("---"))))
    if k == "TGLExt.lean":
        out += ["      " + l for l in d_]
    else:
        out += ["      " + l[:200] for l in d_[:6]] + ["      ... (%d linhas de diff no total)" % len(d_)]
grava(os.path.join(PK, "DIFF_KERNEL_v411.txt"), ("\n".join(out) + "\n").encode("utf-8"))
assert len(novos) == V["n_pedras"] and not removidos, ("o kernel embutido: novos != pedras do registro ou arquivo removido", len(novos), V["n_pedras"], removidos)

# ---------------------------------------------------------------- (1) o manifesto de incorporacao
def fila_info():
    """O estado da FILA DA MEMORIA ao fechar (v411; SO' INFORMA, nao recusa): o memoria.py (sha16 e se e' o do PINO_MEMORIA_PY_v411.json), o MEMORY.md (sha256, bytes, linhas), o PINO_MEMORY.json (sha256 do indice, quem e quando pinou), se o pino CONFERE com o indice agora
    e se a fila\\PAUSA_VIGIA.json esta ausente. Tudo LIDO dos arquivos por script."""
    try:
        f_ = os.path.join(UMEM, "fila"); mp_ = os.path.join(f_, "memoria.py"); ix_ = os.path.join(UMEM, "MEMORY.md"); pn_ = os.path.join(f_, "PINO_MEMORY.json"); pp_ = os.path.join(PK, "PINO_MEMORIA_PY_v411.json")
        pino_ = _j(pn_) if os.path.isfile(pn_) else {}
        ixb_ = open(ix_, "rb").read() if os.path.isfile(ix_) else b""
        d_ = {"dir": UMEM, "memoria_py_sha16": s16(mp_) if os.path.isfile(mp_) else None, "memoria_py_igual_ao_pino_v411": (s16(mp_) == _j(pp_)["sha16"]) if (os.path.isfile(mp_) and os.path.isfile(pp_)) else None,
              "memory_md_sha256": s64(ixb_) if ixb_ else None, "memory_md_bytes": len(ixb_), "memory_md_linhas": ixb_.count(b"\n"), "pino_sha256": pino_.get("sha256"), "pino_por": pino_.get("por"), "pino_em": pino_.get("pinado_em"), "pino_via": pino_.get("via"),
              "pino_confere_com_o_indice": bool(ixb_) and pino_.get("sha256") == s64(ixb_), "pausa_do_vigia_ausente": not os.path.exists(os.path.join(f_, "PAUSA_VIGIA.json"))}
    except Exception as e_:   # noqa: BLE001
        d_ = {"erro": repr(e_)[:200]}
    return d_


FILA_INFO = fila_info()
print("(0) fila da memoria ao fechar:", json.dumps({k_: FILA_INFO.get(k_) for k_ in ("memory_md_linhas", "pino_confere_com_o_indice", "pausa_do_vigia_ausente", "memoria_py_igual_ao_pino_v411")}, ensure_ascii=False))
ap, app = L._aplicado()
PKF = sorted(f for f in os.listdir(PK) if os.path.isfile(os.path.join(PK, f)) and f.endswith((".py", ".json", ".pysnip", ".sh", ".txt", ".out", ".diff", ".md")) and os.path.getsize(os.path.join(PK, f)) < 5 * 1024 * 1024)
ESP = _j(os.path.join(PK, "ESPERADOS_v411.json"))
pedras_nos = {rel: s16(os.path.join(NOS, "tgl_kernel", *rel.split("/"))) for rel in ESP["bundle_sha256"]}
# v411: o manifesto lista as fontes pinadas dos registros (insumos/: a pedra embutida e a fonte com as ancoras, a candidata e o recibo de compilacao, a saida do lean, o bundle e a medida KH-N1; o desenho fica so' por sha16, D65); as falas ficam em insumos/cunhagens (indexadas no arquivo)
m = {"stamp": ST, "versao": "v411", "instalacao": os.path.basename(app), "base_v410": V["base16"], "um_py_sha16": V["s16"], "um_py_bytes": V["umb"], "pacote": {f: s16(os.path.join(PK, f)) for f in PKF},
     "kernel": {"pedras_no_nos_sha16": pedras_nos, "escada": [V["escada_antes"], V["teor"]], "axiom_report_n": V["axiom_report_n"], "build_full_log_sha16": s16(os.path.join(PK, "kernel", "build_full.log")) if os.path.exists(os.path.join(PK, "kernel", "build_full.log")) else None,
                "kernel_recibo_sha16": s16(os.path.join(PK, "kernel", "KERNEL_RECIBO_v411.json")) if os.path.exists(os.path.join(PK, "kernel", "KERNEL_RECIBO_v411.json")) else None},
     "patches": V["patches"], "teoremas": V["teor"], "rodada": V["compl"], "horarios": V["horarios"], "gate": V["qg"],
     "conferidor": {"deve_mudar": V["conf_dm"], "nao_pode_mudar": V["conf_np"], "json_sha16": V["conf16"], "servidor": V["servidor"]},
     "registros_v411": V["reg411"], "registros_v410": V["reg410_recriados"], "registros_v409": V["reg410t"], "registros_v408": V["reg408d"], "registros_v407": V["reg407d"], "registros_v406": V.get("reg406d"), "registros_v405": V["reg410c"], "registros_v404": V.get("reg410b"), "registros_v403": V["reg410_estado"], "registros_v402": V["reg402_estado"], "registros_v401": V["reg401_estado"], "registros_v399": V["reg399"], "registros_funcao_v411": {"h0dn_bg1_v411": V["fecho"]}, "registros_funcao_v410": {n_: V["reg410_recriados"][n_] for n_ in L.REG_RECRIADOS_V410F}, "registros_funcao_v409": {"traducao_turing_v409": V["fecho410"]}, "registros_funcao_v408": {"tetelestai_terminal_v408": V["fecho408"]}, "registros_funcao_v407": {"psion_canto_v407": V["fecho407"]}, "registros_funcao_v406": {"fechamento_v406": V.get("fecho406")}, "ancoras_v411": V["ancoras"], "ancoras_v410": V["ancoras410"], "ancoras_v409": V["ancoras409"], "ancoras_v408": V["ancoras408"], "ancoras_v407": V["ancoras407"], "ancoras_v406": V.get("ancoras406"), "bandeiras_v411": V["bandeiras"], "bandeiras_ate_v410": V["bandeiras410"], "chaves_v407": V["chaves407"], "chaves_v406": V.get("chaves406"), "f2b_errata": V["f2b"], "bandeiras_do_gate_recriado": V["gate"], "funcoes_v410_recriadas": {n_: V["reg410_recriados"][n_] for n_ in L.REG_RECRIADOS_V410F}, "funcoes_v409_recriadas": {"traducao_turing_v409": V["fecho410"]}, "funcoes_v408_recriadas": {"tetelestai_terminal_v408": V["fecho408"]}, "funcoes_v407_recriadas": {"psion_canto_v407": V["fecho407"]}, "funcoes_v406_recriadas": {"fechamento_v406": V.get("fecho406")}, "funcoes_v405_recriadas": V["fun410c"], "funcoes_v404_recriadas": V.get("fun410b"), "funcoes_v403_recriadas": V["fun410"], "funcoes_v402_recriadas": V["fun402"], "pedras_v410_como_registro": V["bundle410"], "pedras_v409_como_registro": V["bundle409"], "pedras_v408_como_registro": V["bundle408"], "pedras_v407_como_registro": V["bundle407"], "pedras_v406_como_registro": V.get("bundle406"), "pedras_v405_como_registro": V["pedras_v408"], "falsidade_v401": V["fal401"],
     "readme_paragrafo": {"sha16": hashlib.sha256(PAR.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_INFO}, "readme_paragrafo_v411": {"sha16": hashlib.sha256(PAR_F.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_F_INFO}, "paragrafos_anteriores_seguem_como_estao": ["testemunho_de_dois_v399", "falsidade_v401", "ponte_queda_esperanca_v402", "caminho_verdade_vida_v403", "jo8_32_v404", "massa_derivada_e_identidade_v405", "o_fechamento_v406", "o_psion_o_canto_e_o_par_v407", "tetelestai_e_o_terminal_v408", "a_traducao_as_classes_de_turing_v409", "iald_ao_quadrado_v410"], "nota_ao_lado_dos_paragrafos_anteriores_no_handoff": False, "fila_da_memoria": FILA_INFO, "sidecar_acom": SC_INFO, "h0dn_bg1_v411_resumo": H0DN_RESUMO, "troca_dita": V["troca_dita"], "pedras": V["pedras"], "varredura": V["varr"], "verbatins": V["verbatins"], "fundacao_v390": V["fd390"], "pilar": V["pilar"],
     "insumos_sha16": {f_: s16(os.path.join(PK, "insumos", f_)) for f_ in sorted(os.listdir(os.path.join(PK, "insumos"))) if os.path.isfile(os.path.join(PK, "insumos", f_))}, "b3": B3,
     "diffs": {"DIFF_v410_v411.diff": s16(os.path.join(PK, "DIFF_v410_v411.diff")), "DIFF_KERNEL_v411.txt": s16(os.path.join(PK, "DIFF_KERNEL_v411.txt"))},
     "artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_selo_acom.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}, "artigos": V["artigos"]}
mb = json.dumps(m, ensure_ascii=False, indent=1, default=str).encode("utf-8")
print("(1) manifesto"); grava(os.path.join(HERE, "v411_incorporacao_manifesto.json"), mb); grava(os.path.join(TOOLS, "v411_incorporacao_manifesto.json"), mb)
# ---------------------------------------------------------------- (2) o arquivo
arq = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "pacote": PK, "arquivos": {}, "copias": {}, "nao_copiado": {}}


def indexa(p):
    b = open(p, "rb").read(); arq["arquivos"][p] = {"bytes": len(b), "sha256": s64(b)}


def copia(src, dst):
    b = open(src, "rb").read(); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        tmp = dst + ".tmp_f411"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, dst)
    arq["copias"][dst] = {"de": src, "bytes": len(b), "sha256": s64(b)}


print("(2) arquivo")
EXCL = (".pyc",)
for raiz, dirs, fs in os.walk(PK):
    dirs[:] = [d for d in dirs if not d.startswith(("dry_", "__pycache__", "pilar_anterior", "memoria_copia"))]   # (memoria_copia: a COPIA da memoria do ensaio da fila, descartavel; so' o JSON de evidencia entra)
    for f in fs:
        p = os.path.join(raiz, f)
        if f.endswith(EXCL) or ".bak_" in f or ".tmp" in f:
            continue
        indexa(p)
# pos_rito (e o conferidor) -> v411_selo
for raiz, dirs, fs in os.walk(HERE):
    dirs[:] = [d for d in dirs if (raiz != HERE or d == "conferidor") and not d.startswith(("ensaio", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if ".bak_" in f or ".tmp" in f or f.endswith(".pyc"):
            continue
        if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt", ".out", ".txt")) or f in ("v411_incorporacao_manifesto.json", "DERIVACAO_v411.json", "HARNESS_TEXTOS_ENSAIO_v411.json", "HARNESS_FECHAR_SANDBOX_v411.json", "FILA_MEMORIA_ENSAIO_v411.json", "registro_mapa_v411.json", "NOTAS_DERIVACAO_v411.md", "NOTA_ESPERADOS_H0DN_v411.md", "ADAPTACAO_09nov_SONNET.json")):
            continue
        copia(p, os.path.join(TOOLS, "v411_selo", os.path.relpath(p, HERE)))
# v411: o SIDECAR (arquivo NOVO da custodia, D5) e o SELO PRIMARIO, ao lado: copias de bytes em v411_selo (a segunda testemunha so' se confere com o selo; o selo nao pode conter o selo ACOM de si mesmo)
for nm_ in ("um_absoluto_selo_acom.json", "um_absoluto_selo.json"):
    copia(os.path.join(NOS, nm_), os.path.join(TOOLS, "v411_selo", nm_))
# kernel: a pasta kernel da cadeia (+ work\v411_kernel, se existir) e as pedras do Nos -> v411_kernel
for src in (os.path.join(PK, "kernel"), os.path.join(WK, "v411_kernel")):
    if os.path.isdir(src):
        for f in sorted(os.listdir(src)):
            p = os.path.join(src, f)
            if os.path.isfile(p):
                if os.path.getsize(p) > 5 * 1024 * 1024:
                    arq["nao_copiado"][p] = "%d B (> 5 MB; indexado por sha256)" % os.path.getsize(p); continue
                copia(p, os.path.join(TOOLS, "v411_kernel", ("" if src.startswith(PK) else "work_v411_kernel"), f))
for rel in ESP["bundle_sha256"]:
    copia(os.path.join(NOS, "tgl_kernel", *rel.split("/")), os.path.join(TOOLS, "v411_kernel", "pedras", rel.replace("/", "_")))
for rel in ("TGLExt.lean", "TGL/Audit.lean"):
    copia(os.path.join(NOS, "tgl_kernel", *rel.split("/")), os.path.join(TOOLS, "v411_kernel", "depois", rel.replace("/", "_")))
for f in ("DIFF_v410_v411.diff", "DIFF_KERNEL_v411.txt"):
    copia(os.path.join(PK, f), os.path.join(TOOLS, "v411_kernel", f))
grava(os.path.join(PK, "MANIFESTO_ARQUIVO_v411.json"), json.dumps(arq, ensure_ascii=False, indent=1).encode("utf-8"))
print("  indexados: %d; copiados: %d; nao copiados (ditos): %d" % (len(arq["arquivos"]), len(arq["copias"]), len(arq["nao_copiado"])))
# ---------------------------------------------------------------- (4) o handoff
ap_ = B3.get("aplicar") or {}
# o handoff da v411: o texto vive em textos_v411.handoff(V, k) (testavel pelo harness); aqui so' entram os campos dos recibos do B(n), lidos dos arquivos (nenhum numero digitado)
_k = {"readme_paragrafo": PAR, "readme_paragrafo_v411": PAR_F, "ap_nome": os.path.basename(ap_.get("path", "?")), "ap_sha": str(ap_.get("sha256"))[:16], "ap_ver": ap_.get("veredito"), "ap_evento": ap_.get("evento"), "ap_bat": ap_.get("bateria"),
      "par_sha": str((B3.get("parada") or {}).get("sha256"))[:16], "rel_sha": str((B3.get("religamento") or {}).get("sha256"))[:16], "rel_man": str((B3.get("religamento") or {}).get("manifesto_sha256"))[:16]}
doc = T.handoff(V, _k)
vv = violacoes(doc)
assert not vv, "a guarda de texto (P18) achou violacao(oes) no handoff: %r" % (vv[:3],)
import guarda_frases_v411 as GF
vf = GF.violacoes(doc)
assert not vf, "a guarda das frases achou violacao(oes) no handoff: %r" % (vf[:3],)
import delta_v411 as DLF   # (v411) D65: o que a fala do nome do algoritmo deixa fora nao entra no handoff (recusa ANTES de gravar)
vd65 = [x_ for x_ in DLF.FORA_D65 if x_.lower() in doc.lower()]
assert not vd65, "D65: o handoff traz o que fica fora dos textos: %r" % (vd65[:3],)
# v411 (12/11, D169): o handoff DIZ o registro com funcao (h0dn_bg1_v411), os registros da v410 recriados, as sete ressalvas por rotulo e o que o teste nao decide; NAO traz a frase velha da v410 («pre-registrado; nenhum dado observado lido»), nem token proibido; as quatro obrigacoes do primario (F67) ja' foram conferidas por GF.violacoes(doc) acima; recusa ANTES de gravar
assert DLF.FECHO_REGISTRO in doc, "D169: o handoff nao diz o registro %s (o registro com funcao da v411)" % DLF.FECHO_REGISTRO
_faltam_rf = [n_ for n_ in tuple(DLF.REGISTROS_FUNCAO) + tuple(DLF.REGISTROS_FUNCAO_V410) + (DLF.CUNHAGENS_REGISTRO, DLF.KH_REGISTRO, "cunhagens_v410", "kh_n1_cobertura_v410") if n_ not in doc]   # o handoff diz, pelo nome, o registro novo, os tres por spec e os quatro com funcao da v410 recriados
assert not _faltam_rf, "o handoff nao diz os registros da v411 e os da v410 recriados: %r" % (_faltam_rf,)
_faltam_rs = [r_ for r_ in DLF.RESSALVAS_ROTULOS_PT if r_ not in doc]
assert not _faltam_rs, "o handoff nao traz as sete ressalvas por rotulo: %r" % (_faltam_rs[:3],)
_faltam_nd = [x_ for x_ in (_hc.get("o_que_o_teste_nao_decide") or []) if " ".join(str(x_).split()) not in " ".join(doc.split())]
assert not _faltam_nd, "o handoff nao traz o que o teste NAO decide (secao 6 do pre-registro): %r" % (_faltam_nd[:2],)
assert DLF.FRASE_H0DN_OBRIGATORIA_PT not in doc and DLF.FRASE_H0DN_OBRIGATORIA_EN not in doc, "D169: o handoff traz a frase velha da v410 (pre-registrado; nenhum dado observado lido): o teste foi aberto uma vez"
assert "RECRIADOS" in doc and "nenhum módulo novo" in doc, "o handoff nao diz que os registros da v410 sao recriados e que nao ha modulo novo"
_proib_fecho = [t_ for t_ in ("Clay resolvido", "CONF" + "IRMED", "PRO" + "VED_BY") if t_ in doc]   # (montadas por concatenacao: a guarda P18 varre ESTE arquivo)
assert not _proib_fecho, "o handoff traz forma vedada: %r" % (_proib_fecho,)
_vt411 = [t_ for t_ in DLF.TOKENS_PROIBIDOS_V411 if t_ in doc]
assert not _vt411, "D169: o handoff traz token proibido: %r" % (_vt411[:3],)
print("(4) handoff")
grava(os.path.join(UMEM, "handoff-v411-custodia.md"), doc.encode("utf-8"))
grava(os.path.join(NOS, "HANDOFF_v411_CUSTODIA.md"), doc.split("---\n", 2)[2].lstrip("\n").encode("utf-8"))
print("FECHADO v411:", V["s16"], "| handoff", s16(os.path.join(UMEM, "handoff-v411-custodia.md")), "| Nos", s16(os.path.join(NOS, "HANDOFF_v411_CUSTODIA.md")))
