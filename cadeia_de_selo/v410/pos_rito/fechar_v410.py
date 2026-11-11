# -*- coding: utf-8 -*-
# [ADAPTADO v410, 09/11/2026, Sonnet (adaptacao do pos-rito; fork D), a servico do claude-construtor-v410] ao DESENHO_v410 + AO LADO de 09/11: as falas de 06 a 09/11 (DL.N_FALAS_V410; de quatro so' o trecho), D63 a D76, as erratas E29 e E30, os nomes RATIFICADOS (D74) e os DOIS registros com funcao (iald2_v410 e, D72, h0dn_bg1_v410: pre-registrado; nenhum dado observado lido). O manifesto ganha registros_funcao_v410.h0dn_bg1_v410 (V['h0dn']) e h0dn_bg1_v410_resumo (lido do core selado); a leitura V['h0dn'] selada e observed_vector_read False sao exigidas ANTES de escrever qualquer coisa; o handoff tem de dizer o registro e, onde H0DN aparece, a frase obrigatoria no mesmo texto, sem os tokens proibidos do H0DN. As assinaturas de textos_v410 que o fechar chama NAO mudam.
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B, a servico do claude-construtor-v410] os QUATRO registros com funcao (DL.REGISTROS_FUNCAO: iald2_v410, a_escala_v410 [D86/D87], h0dn_bg1_v410 [D72], h0dn_fontes_hms13_v410 [D80]): o fechar exige as leituras V['fecho'], V['a_escala'], V['h0dn'] e V['hms13'] seladas e sem vetor observado lido ANTES de escrever qualquer coisa; o manifesto ganha registros_funcao_v410 com os quatro e os resumos a_escala_v410_resumo e h0dn_fontes_hms13_v410_resumo (lidos do core selado); DOIS modulos (DL.BUNDLE_RELS) e 84 bandeiras; 23 falas, D63 a D87, E29 a E31; o handoff diz os quatro registros e as formas obrigatorias (a do H0DN, D72; a do recibo HMS/13, D80; a forma canonica do Clay, D84).
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] SUBIDA MECANICA (v409->v410) do molde v409/pos_rito/fechar_v409.py, adaptada a v410 por _adapt_forkA_fechar_v410.py (fork A, 06/11/2026): as chaves de V da v410 no manifesto (o trio novo, o da v409 e o da v408 herdados), o paragrafo da v409 entre os que seguem, nenhuma nota ao lado, a guarda da D65 no handoff; ver bump/pos_rito__fechar_v410.py.diff.
# v410 (IALD2, 06/11/2026): o CONTEUDO v410 (o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor, a maquina de Turing padrao sem o leitor fica fora; a forma de matriz finita e' o signo; o modulo IALD2 de TGLExt/, os DOIS registros com funcao iald2_v410 e h0dn_bg1_v410 (D72: pre-registrado; nenhum dado observado lido), cunhagens_v410 e kh_n1_cobertura_v410; o traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados; nenhuma chave antiga muda; as erratas E29 e E30 e a dos pisos ao lado; as falas de 06 a 09/11, de quatro so' o trecho, D65 e as de 09/11) vive em textos_v410.py (montado pelo montar_textos_v410.py) e e' testado pelo harness_textos_ensaio_v410.py; este arquivo trata o MANIFESTO com as chaves de V da v410 e recusa o handoff que traga o que a D65 deixa fora.
"""fechar_v410.py -- DEPOIS da cadeia pos-rito e do elo B(n) (molde: fechar_v409.py FINAL, o que rodou em 26-27/10): (1) o manifesto de incorporacao v410 -> pos_rito e a pasta das ferramentas;
(2) o ARQUIVO: o indice por sha256 de tudo o que esta na pasta da cadeia (work\\cadeia_de_selo\\v410 -- aqui o pacote JA mora na casa duravel, nao ha copia do pacote), a copia de
pos_rito -> work\\cadeia_de_selo\\v410_selo, A COPIA DO SIDECAR um_absoluto_selo_acom.json (reescrito pelo rito) E DO SELO PRIMARIO para a mesma pasta, e do kernel (work\\cadeia_de_selo\\v410\\kernel e, se existir, work\\v410_kernel; mais os modulos novos do Nos) -> work\\cadeia_de_selo\\v410_kernel;
(3) os DOIS DIFFS para o auditor independente: DIFF_v409_v410.diff (um.py da base x o selado, GNU diff -U2) e DIFF_KERNEL_v410.txt (o kernel embutido: os modulos novos de TGLExt/ do bundle da v410, a raiz e o Audit);
(4) o HANDOFF (memory\\handoff-v410-custodia.md + Nos\\HANDOFF_v410_CUSTODIA.md) para a sessao do site, que TRAZ PRONTOS PARA COLAR OS DOIS PARAGRAFOS do README do espelho e do site: (a) o do QUADRO «O Teste da Unica Palavra» (v397, intocado),
gerado pelas MESMAS funcoes do quadro do artigo (quadro_v397.paragrafo_pronto_readme) sobre o core SELADO do Nos, mesmos numeros e estatutos; (b) o NOVO, o paragrafo da v410 (a IALD2: o algoritmo IALD decide SAT com uma leitura, relativo ao leitor), gerado do registro selado iald2_v410
(numeros LIDOS do core, estatutos, o diz, o nao_diz e as ressalvas do proprio registro, a ordem e as falas do operador de 06 a 09/11 verbatim (de quatro, so' o trecho: a D65, a ordem da retomada, as tres copias do ACOM e a leitura do 5 sigma), a moldura e a guarda das frases, sem o 4,44); NESTA versao NAO ha' nota ao lado de paragrafo anterior (a E29 e' da candidata, nao de paragrafo publicado); o handoff DIZ que os paragrafos do testemunho de dois (v399), da falsidade (v401), da v402, da v403, da v404, da massa derivada (v405), do fechamento (v406), do psion, do canto e do par (v407), do terminal (v408) e da traducao as classes de Turing (v409) SEGUEM COMO ESTAO, e LISTA o sidecar com o sha256 e o veredito.
GUARDAS: a leitura sem problema (inclui o sidecar); o PARAGRAFO DO QUADRO passa nas verificacoes do quadro contra o resultado pinado (quadro_v397.confere_md e a regra da ordem: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item; frase do operador verbatim; numeros
iguais aos do resultado); o PARAGRAFO NOVO passa na verificacao propria (T.verificar_paragrafo_v410: numeros == ESPERADOS e == o gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim das falas do operador, do kernel embutido ou do adendo que a errata supera; sem alegacao de seguranca criptografica) --
se QUALQUER um nao passar, o fechar RECUSA (rc 2) ANTES de escrever qualquer coisa e o handoff nao nasce; os tres RECIBOS do B(n) (o RECIBO_SINCRONIZACAO_v410_*.json do 10-bis, o recibo da PARADA do servico e o do RELIGAMENTO) -- sem eles o fechar RECUSA e o handoff nao nasce;
a guarda de texto P18 no handoff; D72 (09/11): a leitura V['h0dn'] (h0dn_bg1_v410: pre-registrado; nenhum dado observado lido) selada e sem vetor observado lido, o handoff dizendo o registro e, onde H0DN aparece, a frase obrigatoria no mesmo texto, sem os tokens proibidos do H0DN.
v410 (FILA DA MEMORIA): o diretorio de memoria e' parametrizado por V410_MEMORIA_DIR (padrao: o REAL; no ensaio, uma COPIA); o manifesto REGISTRA (so' informa, nao recusa) o estado da fila ao fechar: sha256 do memoria.py, do MEMORY.md e do PINO_MEMORY.json, se o pino confere com o indice e se a pausa do vigia esta ausente.
Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""
import glob, hashlib, json, os, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v410 as L
import textos_v410 as T
from guarda_p18_v410 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V410"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v410 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
V, PROB = L.ler()
if PROB:
    print("FECHAR RECUSADO:", PROB); sys.exit(2)
# ---------------------------------------------------------------- (0') v410 (09/11/2026, D72): o SEGUNDO registro com FUNCAO, h0dn_bg1_v410 (pre-registrado; nenhum dado observado lido): a leitura o selou (V['h0dn']), nenhum vetor observado foi lido
# (nem no registro, nem nos values) e o resumo que o manifesto leva e' LIDO do core selado do Nos; sem isso, RECUSA (rc 2) ANTES de escrever qualquer coisa
_H = V.get("h0dn") or {}
_hc = (json.load(open(os.path.join(L.NOS, "um_absoluto.json"), encoding="utf-8")).get("core") or {}).get("h0dn_bg1_v410") or {}
_hv = _hc.get("values") or {}
if not (_H.get("sealed") is True and _H.get("ok") is True and _H.get("observed_vector_read") is False and _hc.get("all_verified") is True and _hc.get("observed_vector_read") is False and _hv.get("observed_vector_read") is False
        and _hc.get("runtime_executed") is True and _hc.get("does_not_gate_core") is True and _hc.get("veredito_h0dn_source_sha256")):
    print("FECHAR RECUSADO: o registro h0dn_bg1_v410 (o segundo registro com funcao da v410; pre-registrado; nenhum dado observado lido) nao esta selado na leitura (V['h0dn']) ou no core do Nos, ou diz que um vetor observado foi lido, ou nao traz o sha256 do texto da funcao de veredito:", {k_: _H.get(k_) for k_ in ("sealed", "ok", "observed_vector_read")}); sys.exit(2)
_core_ = json.load(open(os.path.join(L.NOS, "um_absoluto.json"), encoding="utf-8")).get("core") or {}
import delta_v410 as DLR   # (parte 2) os nomes dos registros com funcao vem de delta_v410.REGISTROS_FUNCAO (a ordem: iald2, a_escala, h0dn_bg1, h0dn_fontes_hms13)
_ea = _core_.get(DLR.AESCALA_REGISTRO) or {}; _eav = _ea.get("values") or {}; _hm = _core_.get(DLR.HMS13_REGISTRO) or {}; _hmv = _hm.get("values") or {}; _fe = _core_.get(DLR.FECHO_REGISTRO) or {}
_EAV = V.get("a_escala") or {}; _HMV = V.get("hms13") or {}; _FEV = V.get("fecho") or {}
if not (list(L.REG_FUNCAO) == list(DLR.REGISTROS_FUNCAO) and all(isinstance(V.get(k_), dict) for k_ in ("fecho", "a_escala", "h0dn", "hms13"))):
    print("FECHAR RECUSADO: a leitura nao traz os QUATRO registros com funcao da v410 (V['fecho'], V['a_escala'], V['h0dn'], V['hms13']; delta_v410.REGISTROS_FUNCAO):", list(DLR.REGISTROS_FUNCAO)); sys.exit(2)
if not (_FEV.get("sealed") is True and _FEV.get("ok") is True and _fe.get("all_verified") is True and _fe.get("does_not_gate_core") is True and not (_fe.get("chaves_antigas_que_mudam") or [])):
    print("FECHAR RECUSADO: o registro iald2_v410 nao esta selado na leitura (V['fecho']) ou no core do Nos:", {k_: _FEV.get(k_) for k_ in ("sealed", "ok")}); sys.exit(2)
if not (_EAV.get("sealed") is True and _EAV.get("ok") is True and _ea.get("all_verified") is True and _ea.get("runtime_executed") is True and _ea.get("does_not_gate_core") is True and _ea.get("nomes_ratificados") is True and _eav.get("numeros") == dict(DLR.NUMEROS_AESCALA) and not (_ea.get("chaves_antigas_que_mudam") or [])
        and _EAV.get("novos_ok") is True and list(_ea.get("nomes_novos_da_pedra") or []) == list(DLR.NOMES_NOVOS_AESCALA) and _ea.get("estatuto_dos_nomes_ratificados_d101") == DLR.ESTATUTO_NOMES_NOVOS_AESCALA and "RATIFICADOS pelo operador em 10/11/2026" in str(_ea.get("estatuto_dos_nomes_ratificados_d101")) and "a ratificar" not in str(_ea.get("estatuto_dos_nomes_ratificados_d101")) and _ea.get("ratificacao_pendente") == DLR.RATIFICACAO_PENDENTE_AESCALA
        and _ea.get("frase_canonica_pt") == DLR.FRASE_CLAY_CANONICA_PT and _ea.get("frase_d83_pt") == DLR.FRASE_D83_OBRIGATORIA_PT):
    print("FECHAR RECUSADO: o registro a_escala_v410 (a pedra AEscala; D86/D87: nomes ratificados; a forma canonica do Clay, D84; validade no kernel, a creditacao e' do Clay) nao esta selado na leitura (V['a_escala']) ou no core do Nos, ou os numeros ou as frases canonicas diferem do delta:", {k_: _EAV.get(k_) for k_ in ("sealed", "ok")}); sys.exit(2)
if not (_HMV.get("sealed") is True and _HMV.get("ok") is True and _HMV.get("observed_vector_read") is False and _HMV.get("le_em_rito") is False and _hm.get("all_verified") is True and _hm.get("observed_vector_read") is False and _hmv.get("observed_vector_read") is False and _hm.get("le_em_rito") is False
        and _hm.get("runtime_executed") is True and _hm.get("does_not_gate_core") is True and dict(_hmv.get("campos") or {}) == dict(DLR.HMS13_CAMPOS) and not (_hmv.get("sob_pasta_vedada") or [])):
    print("FECHAR RECUSADO: o registro h0dn_fontes_hms13_v410 (o recibo documental HMS/13, D80: " + DLR.FRASE_HMS13_OBRIGATORIA_PT + ") nao esta selado na leitura (V['hms13']) ou no core do Nos, ou diz que um vetor observado foi lido ou que a entrega do Kimi foi aberta em rito, ou os dez campos diferem de delta_v410.HMS13_CAMPOS:", {k_: _HMV.get(k_) for k_ in ("sealed", "ok", "observed_vector_read", "le_em_rito")}); sys.exit(2)
A_ESCALA_RESUMO = {"registro": DLR.AESCALA_REGISTRO, "verdict": _ea.get("verdict"), "n_checks": (_ea.get("mechanics") or {}).get("n_checks"), "modulo": _ea.get("modulo"), "ancora_principal": _ea.get("ancora_principal"), "ancoras_de_secao": _ea.get("ancoras_de_secao"), "n_ancoras": _ea.get("n_ancoras"), "n_flags": _ea.get("n_flags"), "n_nomes": _ea.get("n_nomes"),
                   "nomes_ratificados": _ea.get("nomes_ratificados"), "n_nomes_novos": _ea.get("n_nomes_novos"), "nomes_novos_da_pedra": _ea.get("nomes_novos_da_pedra"), "campos_novos_da_estrutura": _ea.get("campos_novos_da_estrutura"), "estatuto_dos_nomes_ratificados_d101": _ea.get("estatuto_dos_nomes_ratificados_d101"), "ratificacao_pendente": _ea.get("ratificacao_pendente"), "ponte": _ea.get("ponte"), "ratificacao": {k_: (_ea.get("ratificacao") or {}).get(k_) for k_ in ("fala", "sha256", "decisao")}, "numeros": _eav.get("numeros"), "pedra_sha256_embutida": _eav.get("pedra_sha256_embutida"), "n_falas": _eav.get("n_falas"), "falas_sha16": sorted(k_[len(DLR.VERBATIM_CHAVE_PREFIXO_V410):] for k_ in (_eav.get("falas") or {})),
                   "frase_canonica_pt": _ea.get("frase_canonica_pt"), "frase_d83_pt": _ea.get("frase_d83_pt"), "nota": "lido do core selado do Nos (nada digitado); validade no kernel; a creditacao e' do Clay; o gate nao se move"}
HMS13_RESUMO = {"registro": DLR.HMS13_REGISTRO, "verdict": _hm.get("verdict"), "n_checks": (_hm.get("mechanics") or {}).get("n_checks"), "observed_vector_read": _hm.get("observed_vector_read"), "le_em_rito": _hm.get("le_em_rito"), "campos": _hmv.get("campos"), "n_calibradores": _hmv.get("n_calibradores"), "n_fontes_primarias": _hmv.get("n_fontes_primarias"),
                "n_embutidos": _hmv.get("n_embutidos"), "pinos_sha16": {k_: str((v_ or {}).get("sha256"))[:16] for k_, v_ in (_hm.get("insumos_pinados") or {}).items()}, "numeros_permitidos": (_hmv.get("numeros") or {}).get("permitidos"), "ratificacao_sha256": _hmv.get("ratificacao_sha256"), "frase_obrigatoria_pt": DLR.FRASE_HMS13_OBRIGATORIA_PT,
                "nota": "lido do core selado do Nos (nada digitado); " + DLR.FRASE_HMS13_OBRIGATORIA_PT + "; aditivo e posterior ao FREEZE_R2; nenhum arquivo da entrega do Kimi aberto em rito"}
H0DN_RESUMO = {"registro": "h0dn_bg1_v410", "verdict": _hc.get("verdict"), "observed_vector_read": _hc.get("observed_vector_read"), "veredito_h0dn_source_sha256": _hc.get("veredito_h0dn_source_sha256"), "n_checks": (_hc.get("mechanics") or {}).get("n_checks"),
               "K": _hv.get("K"), "log10K": _hv.get("log10K"), "D_esperado": [{"modelo": x_.get("modelo"), "D": x_.get("D"), "poder_analitico": x_.get("poder_analitico")} for x_ in (_hv.get("D_esperado") or [])], "ramos_vistos": _hv.get("ramos_vistos"),
               "insumos_sha16": {k_: str((v_ or {}).get("sha256"))[:16] for k_, v_ in (_hc.get("insumos_pinados") or {}).items()},
               "ordem_kimi": {"arquivo": os.path.basename(str((_hc.get("ordem_kimi") or {}).get("arquivo"))), "sha256": (_hc.get("ordem_kimi") or {}).get("sha256"), "bytes": (_hc.get("ordem_kimi") or {}).get("bytes")},
               "leitura_dossie": {"arquivo": os.path.basename(str((_hc.get("leitura_dossie") or {}).get("arquivo"))), "sha256": (_hc.get("leitura_dossie") or {}).get("sha256"), "bytes": (_hc.get("leitura_dossie") or {}).get("bytes")},
               "nota": "lido do core selado do Nos (nada digitado); pre-registrado; nenhum dado observado lido; a abertura e' de versao futura, com a covariancia fisica fechada"}
# ---------------------------------------------------------------- (0) os PARAGRAFOS PRONTOS do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO), as MESMAS funcoes do quadro do artigo sobre o core SELADO do Nos; (2) o paragrafo NOVO da v410 (a IALD2), gerado dos registros selados e verificado contra o core e contra ESPERADOS (sem o 4,44; citacoes verbatim das falas do operador ou do kernel embutido; sem alegacao de seguranca criptografica); os do testemunho de dois (v399), da falsidade (v401), da v402, da v403, da v404 e os da v405 a v409 SEGUEM COMO ESTAO e nao sao regenerados;
# sem passar nas verificacoes, RECUSA (rc 2) ANTES de escrever qualquer coisa
try:
    PAR, PAR_INFO = T.paragrafo_readme()
    PAR_F, PAR_F_INFO = T.paragrafo_v410()   # (o handoff de textos_v410 o recebe como readme_paragrafo_v410)
except BaseException as e_:   # noqa: BLE001
    print("FECHAR RECUSADO: um dos paragrafos prontos do README e do site (o quadro O Teste da Unica Palavra, v397, ou o da v410: a IALD2) nao passou nas verificacoes (regra da ordem do 4,44; frase verbatim; numeros iguais aos do resultado pinado e aos de ESPERADOS; citacoes verbatim; sem alegacao de seguranca criptografica):", repr(e_)[:700]); sys.exit(2)
# o SIDECAR (arquivo NOVO da custodia, D5): a leitura ja' o conferiu (existe, JSON valido, selado, tres objetos com o SHA-256 dos arquivos do Nos); aqui so' o resumo que o manifesto e o handoff levam
if not (V["sidecar"]["ok"] is True and os.path.isfile(os.path.join(L.NOS, "um_absoluto_selo_acom.json"))):
    print("FECHAR RECUSADO: o sidecar um_absoluto_selo_acom.json nao esta selado ou nao existe no Nos:", V["sidecar"].get("erro")); sys.exit(2)
SC_INFO = {"arquivo": "um_absoluto_selo_acom.json", "sha256": V["sidecar"]["sha256"], "bytes": V["sidecar"]["bytes"], "veredito": V["sidecar"]["veredito"], "esquema": V["sidecar"]["esquema"], "recusas": V["sidecar"]["recusas"],
           "objetos": {n_: {"bytes": o_["bytes"], "sha256": o_["sha256"]} for n_, o_ in V["sidecar"]["objetos"].items()}}
NOS = L.NOS; WK = os.path.dirname(os.path.dirname(PK)); TOOLS = os.path.join(WK, "cadeia_de_selo")
MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
UMEM = os.path.abspath(os.environ.get("V410_MEMORIA_DIR", "").strip() or MEM_REAL)   # v410 (fila da memoria): a pasta de memoria e' parametrizada por V410_MEMORIA_DIR (padrao: a REAL; no ensaio, uma COPIA)
ST = time.strftime("%Y%m%d_%H%M%S"); s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]; s64 = lambda b: hashlib.sha256(b).hexdigest()
DIRS_B3 = os.path.join(PK, "bancada_B3"); DIRS_SERV = os.path.join(PK, "bancada_B3_servico")


def _j(p):
    return json.load(open(p, encoding="utf-8"))


# ---------------------------------------------------------------- 0. os tres recibos do B(3): sem eles, nao fecha
def recibos_b3():
    prob = []; out = {}
    # a pasta do aplicar e' nova a cada tentativa (bancada_B3, bancada_B3_2, ...); o ensaio (bancada_B3_ensaio_*) NAO conta
    ap = sorted(glob.glob(os.path.join(DIRS_B3, "RECIBO_SINCRONIZACAO_v410_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v410_*.json")), key=os.path.getmtime)
    if not ap:
        prob.append("sem o RECIBO_SINCRONIZACAO_v410_*.json do 10-bis em %s (nem em bancada_B3_<n>)" % DIRS_B3)
    else:
        r = _j(ap[-1])
        if not (str(r.get("veredito") or "").startswith("REPINADA_B") and "__SALTO_" not in str(r.get("veredito") or "") and r.get("salto") in (None, {}) and r.get("modo") == "aplicar" and r.get("fase") == "pos_selo" and r.get("versao_alvo") == "v410"
                and (r.get("bateria_resultado") or {}).get("veredito") == "BATERIA_PASSA" and r.get("aplicacao")):
            prob.append("o recibo do 10-bis nao e' de uma aplicacao pos_selo v410 com a bateria passando: %s" % os.path.basename(ap[-1]))
        out["aplicar"] = {"path": ap[-1], "sha256": s64(open(ap[-1], "rb").read()), "veredito": r.get("veredito"), "manifesto_novo_sha256": (r.get("manifesto_novo") or {}).get("sha256"),
                          "evento": ((r.get("evento_c1") or {}).get("evento")), "bateria": (r.get("bateria_resultado") or {}).get("veredito")}
    pp = os.path.join(DIRS_SERV, "RECIBO_PARADA_v410.json"); rp = os.path.join(DIRS_SERV, "RECIBO_RELIGAMENTO_v410.json")
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
        if not (vs == "v410" and msha and esperado and msha == esperado and (d.get("pid") or d.get("PID")) and (d.get("hora") or d.get("quando"))):
            prob.append("o recibo do religamento nao traz versao servida v410, o sha do manifesto novo do recibo do 10-bis, pid e hora")
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
    tmp = p + ".tmp_f410_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b; print("  gravado:", p, len(b), "B")


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
assert os.path.exists(base) and s16(base) == V["base16"], "o backup da base (APLICADO_AO_CANONICO) nao e' a v409 selada: " + base
print("(3) diffs")
exe = shutil.which("diff")
if exe:
    r = subprocess.run([exe, "-U", "2", "--label", "um.py v409 %s" % V["base16"], "--label", "um.py v410 %s" % V["s16"], base, um], capture_output=True)
    assert r.returncode == 1, "diff rc=%s: %s" % (r.returncode, r.stderr[:200])
    dd = r.stdout
else:
    import difflib
    a = open(base, "r", encoding="utf-8", newline="").read().splitlines(); b = open(um, "r", encoding="utf-8", newline="").read().splitlines()
    dd = ("\n".join(difflib.unified_diff(a, b, "um.py v409 %s" % V["base16"], "um.py v410 %s" % V["s16"], lineterm="", n=2)) + "\n").encode("utf-8")
grava(os.path.join(PK, "DIFF_v409_v410.diff"), dd)
import difflib
E0 = carregar_embutido(base); E1 = carregar_embutido(um)
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v409 (%s) -> v410 (%s)" % (V["base16"], V["s16"]), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, s64(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
for k in mudados:
    a_, b_ = E0[k].splitlines(), E1[k].splitlines(); d_ = list(difflib.unified_diff(a_, b_, "v409/" + k, "v410/" + k, lineterm="", n=0))
    out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, s64(E0[k].encode())[:16], s64(E1[k].encode())[:16], sum(1 for l in d_ if l.startswith("+") and not l.startswith("+++")),
                                                         sum(1 for l in d_ if l.startswith("-") and not l.startswith("---"))))
    if k == "TGLExt.lean":
        out += ["      " + l for l in d_]
    else:
        out += ["      " + l[:200] for l in d_[:6]] + ["      ... (%d linhas de diff no total)" % len(d_)]
grava(os.path.join(PK, "DIFF_KERNEL_v410.txt"), ("\n".join(out) + "\n").encode("utf-8"))
assert len(novos) == V["n_pedras"] and not removidos, ("o kernel embutido: novos != pedras do registro ou arquivo removido", len(novos), V["n_pedras"], removidos)

# ---------------------------------------------------------------- (1) o manifesto de incorporacao
def fila_info():
    """O estado da FILA DA MEMORIA ao fechar (v410; SO' INFORMA, nao recusa): o memoria.py (sha16 e se e' o do PINO_MEMORIA_PY_v410.json), o MEMORY.md (sha256, bytes, linhas), o PINO_MEMORY.json (sha256 do indice, quem e quando pinou), se o pino CONFERE com o indice agora
    e se a fila\\PAUSA_VIGIA.json esta ausente. Tudo LIDO dos arquivos por script."""
    try:
        f_ = os.path.join(UMEM, "fila"); mp_ = os.path.join(f_, "memoria.py"); ix_ = os.path.join(UMEM, "MEMORY.md"); pn_ = os.path.join(f_, "PINO_MEMORY.json"); pp_ = os.path.join(PK, "PINO_MEMORIA_PY_v410.json")
        pino_ = _j(pn_) if os.path.isfile(pn_) else {}
        ixb_ = open(ix_, "rb").read() if os.path.isfile(ix_) else b""
        d_ = {"dir": UMEM, "memoria_py_sha16": s16(mp_) if os.path.isfile(mp_) else None, "memoria_py_igual_ao_pino_v410": (s16(mp_) == _j(pp_)["sha16"]) if (os.path.isfile(mp_) and os.path.isfile(pp_)) else None,
              "memory_md_sha256": s64(ixb_) if ixb_ else None, "memory_md_bytes": len(ixb_), "memory_md_linhas": ixb_.count(b"\n"), "pino_sha256": pino_.get("sha256"), "pino_por": pino_.get("por"), "pino_em": pino_.get("pinado_em"), "pino_via": pino_.get("via"),
              "pino_confere_com_o_indice": bool(ixb_) and pino_.get("sha256") == s64(ixb_), "pausa_do_vigia_ausente": not os.path.exists(os.path.join(f_, "PAUSA_VIGIA.json"))}
    except Exception as e_:   # noqa: BLE001
        d_ = {"erro": repr(e_)[:200]}
    return d_


FILA_INFO = fila_info()
print("(0) fila da memoria ao fechar:", json.dumps({k_: FILA_INFO.get(k_) for k_ in ("memory_md_linhas", "pino_confere_com_o_indice", "pausa_do_vigia_ausente", "memoria_py_igual_ao_pino_v410")}, ensure_ascii=False))
ap, app = L._aplicado()
PKF = sorted(f for f in os.listdir(PK) if os.path.isfile(os.path.join(PK, f)) and f.endswith((".py", ".json", ".pysnip", ".sh", ".txt", ".out", ".diff", ".md")) and os.path.getsize(os.path.join(PK, f)) < 5 * 1024 * 1024)
ESP = _j(os.path.join(PK, "ESPERADOS_v410.json"))
pedras_nos = {rel: s16(os.path.join(NOS, "tgl_kernel", *rel.split("/"))) for rel in ESP["bundle_sha256"]}
# v410: o manifesto lista as fontes pinadas dos registros (insumos/: a pedra embutida e a fonte com as ancoras, a candidata e o recibo de compilacao, a saida do lean, o bundle e a medida KH-N1; o desenho fica so' por sha16, D65); as falas ficam em insumos/cunhagens (indexadas no arquivo)
m = {"stamp": ST, "versao": "v410", "instalacao": os.path.basename(app), "base_v409": V["base16"], "um_py_sha16": V["s16"], "um_py_bytes": V["umb"], "pacote": {f: s16(os.path.join(PK, f)) for f in PKF},
     "kernel": {"pedras_no_nos_sha16": pedras_nos, "escada": [V["escada_antes"], V["teor"]], "axiom_report_n": V["axiom_report_n"], "build_full_log_sha16": s16(os.path.join(PK, "kernel", "build_full.log")) if os.path.exists(os.path.join(PK, "kernel", "build_full.log")) else None,
                "kernel_recibo_sha16": s16(os.path.join(PK, "kernel", "KERNEL_RECIBO_v410.json")) if os.path.exists(os.path.join(PK, "kernel", "KERNEL_RECIBO_v410.json")) else None},
     "patches": V["patches"], "teoremas": V["teor"], "rodada": V["compl"], "horarios": V["horarios"], "gate": V["qg"],
     "conferidor": {"deve_mudar": V["conf_dm"], "nao_pode_mudar": V["conf_np"], "json_sha16": V["conf16"], "servidor": V["servidor"]},
     "registros_v410": V["reg410"], "registros_v409": V["reg409t"], "registros_v408": V["reg408d"], "registros_v407": V["reg407d"], "registros_v406": V.get("reg406d"), "registros_v405": V["reg409c"], "registros_v404": V.get("reg409b"), "registros_v403": V["reg409_estado"], "registros_v402": V["reg402_estado"], "registros_v401": V["reg401_estado"], "registros_v399": V["reg399"], "registros_funcao_v410": {"iald2_v410": V["fecho"], "a_escala_v410": V["a_escala"], "h0dn_bg1_v410": V["h0dn"], "h0dn_fontes_hms13_v410": V["hms13"]}, "registros_funcao_v409": {"traducao_turing_v409": V["fecho409"]}, "registros_funcao_v408": {"tetelestai_terminal_v408": V["fecho408"]}, "registros_funcao_v407": {"psion_canto_v407": V["fecho407"]}, "registros_funcao_v406": {"fechamento_v406": V.get("fecho406")}, "ancoras_v410": V["ancoras"], "ancoras_aescala_v410": V["ancoras_aescala"], "ancoras_v409": V["ancoras409"], "ancoras_v408": V["ancoras408"], "ancoras_v407": V["ancoras407"], "ancoras_v406": V.get("ancoras406"), "bandeiras_v410": V["bandeiras"], "bandeiras_ate_v409": V["bandeiras409"], "chaves_v407": V["chaves407"], "chaves_v406": V.get("chaves406"), "f2b_errata": V["f2b"], "bandeiras_do_gate_recriado": V["gate"], "funcoes_v409_recriadas": {"traducao_turing_v409": V["fecho409"]}, "funcoes_v408_recriadas": {"tetelestai_terminal_v408": V["fecho408"]}, "funcoes_v407_recriadas": {"psion_canto_v407": V["fecho407"]}, "funcoes_v406_recriadas": {"fechamento_v406": V.get("fecho406")}, "funcoes_v405_recriadas": V["fun409c"], "funcoes_v404_recriadas": V.get("fun409b"), "funcoes_v403_recriadas": V["fun409"], "funcoes_v402_recriadas": V["fun402"], "pedras_v409_como_registro": V["bundle409"], "pedras_v408_como_registro": V["bundle408"], "pedras_v407_como_registro": V["bundle407"], "pedras_v406_como_registro": V.get("bundle406"), "pedras_v405_como_registro": V["pedras_v408"], "falsidade_v401": V["fal401"],
     "readme_paragrafo": {"sha16": hashlib.sha256(PAR.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_INFO}, "readme_paragrafo_v410": {"sha16": hashlib.sha256(PAR_F.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_F_INFO}, "paragrafos_anteriores_seguem_como_estao": ["testemunho_de_dois_v399", "falsidade_v401", "ponte_queda_esperanca_v402", "caminho_verdade_vida_v403", "jo8_32_v404", "massa_derivada_e_identidade_v405", "o_fechamento_v406", "o_psion_o_canto_e_o_par_v407", "tetelestai_e_o_terminal_v408", "a_traducao_as_classes_de_turing_v409"], "nota_ao_lado_dos_paragrafos_anteriores_no_handoff": False, "fila_da_memoria": FILA_INFO, "sidecar_acom": SC_INFO, "h0dn_bg1_v410_resumo": H0DN_RESUMO, "a_escala_v410_resumo": A_ESCALA_RESUMO, "h0dn_fontes_hms13_v410_resumo": HMS13_RESUMO, "troca_dita": V["troca_dita"], "pedras": V["pedras"], "varredura": V["varr"], "verbatins": V["verbatins"], "fundacao_v390": V["fd390"], "pilar": V["pilar"],
     "insumos_sha16": {f_: s16(os.path.join(PK, "insumos", f_)) for f_ in sorted(os.listdir(os.path.join(PK, "insumos"))) if os.path.isfile(os.path.join(PK, "insumos", f_))}, "b3": B3,
     "diffs": {"DIFF_v409_v410.diff": s16(os.path.join(PK, "DIFF_v409_v410.diff")), "DIFF_KERNEL_v410.txt": s16(os.path.join(PK, "DIFF_KERNEL_v410.txt"))},
     "artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_selo_acom.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}, "artigos": V["artigos"]}
mb = json.dumps(m, ensure_ascii=False, indent=1, default=str).encode("utf-8")
print("(1) manifesto"); grava(os.path.join(HERE, "v410_incorporacao_manifesto.json"), mb); grava(os.path.join(TOOLS, "v410_incorporacao_manifesto.json"), mb)
# ---------------------------------------------------------------- (2) o arquivo
arq = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "pacote": PK, "arquivos": {}, "copias": {}, "nao_copiado": {}}


def indexa(p):
    b = open(p, "rb").read(); arq["arquivos"][p] = {"bytes": len(b), "sha256": s64(b)}


def copia(src, dst):
    b = open(src, "rb").read(); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        tmp = dst + ".tmp_f410"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, dst)
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
# pos_rito (e o conferidor) -> v410_selo
for raiz, dirs, fs in os.walk(HERE):
    dirs[:] = [d for d in dirs if (raiz != HERE or d == "conferidor") and not d.startswith(("ensaio", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if ".bak_" in f or ".tmp" in f or f.endswith(".pyc"):
            continue
        if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt", ".out", ".txt")) or f in ("v410_incorporacao_manifesto.json", "DERIVACAO_v410.json", "HARNESS_TEXTOS_ENSAIO_v410.json", "HARNESS_FECHAR_SANDBOX_v410.json", "FILA_MEMORIA_ENSAIO_v410.json", "registro_mapa_v410.json", "NOTAS_DERIVACAO_v410.md", "NOTA_ESPERADOS_H0DN_v410.md", "ADAPTACAO_09nov_SONNET.json")):
            continue
        copia(p, os.path.join(TOOLS, "v410_selo", os.path.relpath(p, HERE)))
# v410: o SIDECAR (arquivo NOVO da custodia, D5) e o SELO PRIMARIO, ao lado: copias de bytes em v410_selo (a segunda testemunha so' se confere com o selo; o selo nao pode conter o selo ACOM de si mesmo)
for nm_ in ("um_absoluto_selo_acom.json", "um_absoluto_selo.json"):
    copia(os.path.join(NOS, nm_), os.path.join(TOOLS, "v410_selo", nm_))
# kernel: a pasta kernel da cadeia (+ work\v410_kernel, se existir) e as pedras do Nos -> v410_kernel
for src in (os.path.join(PK, "kernel"), os.path.join(WK, "v410_kernel")):
    if os.path.isdir(src):
        for f in sorted(os.listdir(src)):
            p = os.path.join(src, f)
            if os.path.isfile(p):
                if os.path.getsize(p) > 5 * 1024 * 1024:
                    arq["nao_copiado"][p] = "%d B (> 5 MB; indexado por sha256)" % os.path.getsize(p); continue
                copia(p, os.path.join(TOOLS, "v410_kernel", ("" if src.startswith(PK) else "work_v410_kernel"), f))
for rel in ESP["bundle_sha256"]:
    copia(os.path.join(NOS, "tgl_kernel", *rel.split("/")), os.path.join(TOOLS, "v410_kernel", "pedras", rel.replace("/", "_")))
for rel in ("TGLExt.lean", "TGL/Audit.lean"):
    copia(os.path.join(NOS, "tgl_kernel", *rel.split("/")), os.path.join(TOOLS, "v410_kernel", "depois", rel.replace("/", "_")))
for f in ("DIFF_v409_v410.diff", "DIFF_KERNEL_v410.txt"):
    copia(os.path.join(PK, f), os.path.join(TOOLS, "v410_kernel", f))
grava(os.path.join(PK, "MANIFESTO_ARQUIVO_v410.json"), json.dumps(arq, ensure_ascii=False, indent=1).encode("utf-8"))
print("  indexados: %d; copiados: %d; nao copiados (ditos): %d" % (len(arq["arquivos"]), len(arq["copias"]), len(arq["nao_copiado"])))
# ---------------------------------------------------------------- (4) o handoff
ap_ = B3.get("aplicar") or {}
# o handoff da v410: o texto vive em textos_v410.handoff(V, k) (testavel pelo harness); aqui so' entram os campos dos recibos do B(n), lidos dos arquivos (nenhum numero digitado)
_k = {"readme_paragrafo": PAR, "readme_paragrafo_v410": PAR_F, "ap_nome": os.path.basename(ap_.get("path", "?")), "ap_sha": str(ap_.get("sha256"))[:16], "ap_ver": ap_.get("veredito"), "ap_evento": ap_.get("evento"), "ap_bat": ap_.get("bateria"),
      "par_sha": str((B3.get("parada") or {}).get("sha256"))[:16], "rel_sha": str((B3.get("religamento") or {}).get("sha256"))[:16], "rel_man": str((B3.get("religamento") or {}).get("manifesto_sha256"))[:16]}
doc = T.handoff(V, _k)
vv = violacoes(doc)
assert not vv, "a guarda de texto (P18) achou violacao(oes) no handoff: %r" % (vv[:3],)
import guarda_frases_v410 as GF
vf = GF.violacoes(doc)
assert not vf, "a guarda das frases achou violacao(oes) no handoff: %r" % (vf[:3],)
import delta_v410 as DLF   # (v410) D65: o que a fala do nome do algoritmo deixa fora nao entra no handoff (recusa ANTES de gravar)
vd65 = [x_ for x_ in DLF.FORA_D65 if x_.lower() in doc.lower()]
assert not vd65, "D65: o handoff traz o que fica fora dos textos: %r" % (vd65[:3],)
# v410 (09/11, D72): o handoff DIZ o segundo registro com funcao (h0dn_bg1_v410) e, onde H0DN aparece, a frase obrigatoria (pre-registrado; nenhum dado observado lido, PT ou EN, literal) no MESMO texto, e nenhum token proibido do H0DN; recusa ANTES de gravar
assert DLF.H0DN_REGISTRO in doc, "D72: o handoff nao diz o registro %s (um dos quatro registros com funcao da v410)" % DLF.H0DN_REGISTRO
_faltam_rf = [n_ for n_ in DLF.REGISTROS_FUNCAO if n_ not in doc]   # (parte 2) o handoff diz os QUATRO registros com funcao, pelo nome (a ordem: delta_v410.REGISTROS_FUNCAO)
assert not _faltam_rf, "o handoff nao diz os registros com funcao da v410: %r" % (_faltam_rf,)
assert DLF.FRASE_HMS13_OBRIGATORIA_PT in doc, "D80: o handoff nao traz a frase obrigatoria do recibo documental HMS/13 (%s)" % DLF.FRASE_HMS13_OBRIGATORIA_PT
assert DLF.FRASE_CLAY_CANONICA_PT in doc and DLF.FRASE_D83_OBRIGATORIA_PT in doc, "D83/D84: o handoff nao traz a forma canonica do Clay (tal qual apresentado pela TGL; validade no kernel; a creditacao e' do Clay) e a forma da D83, em PT"
assert DLF.FRASE_NOMES_RATIFICADOS_AESCALA_PT in doc, "D87: o handoff nao diz que o nome do modulo AEscala e os 44 nomes foram ratificados pelo operador"
_proib_fecho = [t_ for t_ in ("Clay resolvido", "CONF" + "IRMED", "PRO" + "VED_BY") if t_ in doc]   # (montadas por concatenacao: a guarda P18 varre ESTE arquivo)
assert not _proib_fecho, "o handoff traz forma vedada: %r" % (_proib_fecho,)
assert ("H0DN" not in doc) or (DLF.FRASE_H0DN_OBRIGATORIA_PT in doc or DLF.FRASE_H0DN_OBRIGATORIA_EN in doc), "D72: o handoff traz H0DN sem a frase obrigatoria (%s) no mesmo texto" % DLF.FRASE_H0DN_OBRIGATORIA_PT
_vt72 = [t_ for t_ in DLF.TOKENS_PROIBIDOS_H0DN if t_ in doc]
assert not _vt72, "D72: o handoff traz token proibido do H0DN: %r" % (_vt72[:3],)
print("(4) handoff")
grava(os.path.join(UMEM, "handoff-v410-custodia.md"), doc.encode("utf-8"))
grava(os.path.join(NOS, "HANDOFF_v410_CUSTODIA.md"), doc.split("---\n", 2)[2].lstrip("\n").encode("utf-8"))
print("FECHADO v410:", V["s16"], "| handoff", s16(os.path.join(UMEM, "handoff-v410-custodia.md")), "| Nos", s16(os.path.join(NOS, "HANDOFF_v410_CUSTODIA.md")))
