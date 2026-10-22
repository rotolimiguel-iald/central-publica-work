# -*- coding: utf-8 -*-
"""registrar_mapa_v394.py -- MONTA (nao registra) o registro da v394 no mapa de rotas e imprime o comando (molde: registrar_mapa_v393.py). Rodar DEPOIS do fechar (handoff gravado).
A v394 traz UMA rota nova, umpy.v394.fock_tempo_e_cunhagens (o relogio M2, a regra quadratica, a rede de Fock, Takesaki e Maxwell do Codex e as cunhagens de 14 a 19/10), mais tres ANOTACOES nas rotas que esperavam por ela
(o tempo e a leitura de 15/10, a cinematica bosonica concreta da rede e a prova do contrato da regra), cada afirmacao testada contra o core/selo lidos por script (o registro existe? selou? o que NAO fechou fica dito).
Fail-closed: o selo tem de ser a v394; as rotas anotadas e as citadas em refs tem de existir no livro (leitura); a nova nao pode existir.
SAIDA: pos_rito\\registro_mapa_v394.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa)."""
import glob, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v394 as L
from guarda_p18_v394 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V394"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) de narrativa da v393 marcado(s) para reescrever na v394 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
V, PROB = L.ler()
if PROB:
    print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); sys.exit(2)
NOS = L.NOS
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo.get("um_version") == "v394", "o selo nao e a v394"
R = set(V["registros_novos"]); MODS = {p["modulo"].split(".")[-1] for p in V["pedras"]}
S = V["s16"]
_tol = lambda V: ("%g" % V["cons"]["tol"]) if V["cons"].get("tol") is not None else "n/d"
# --- o livro do mapa (so leitura): as rotas anotadas existem; a nova nao
ids = set()
for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("tipo") == "ROTA":
        ids.add(d.get("rota_id"))
NOVA = "umpy.v394.fock_tempo_e_cunhagens"
assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v394_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v394_*.json")), key=os.path.getmtime)
arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(PK, "ESPERADOS_v394.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v394.json"),
        os.path.join(PK, "DIFF_KERNEL_v394.txt"), os.path.join(PK, "DIFF_v393_v394.diff"), os.path.join(NOS, "HANDOFF_v394_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v394.json")] + b3[-1:]
arts = [a for a in arts if os.path.exists(a)]


def sim(cond, fechado, aberto):
    return fechado if cond else aberto


def anot(rota_id, titulo, resultado, proximo, refs=None, nota=None, estatuto="REAL"):
    d = {"tipo": "ANOTACAO", "rota_id": rota_id, "estatuto": estatuto, "olhou_dados": False, "titulo": titulo, "resultado": resultado, "proximo_passo": proximo, "refs": [NOVA] + (refs or [])}
    if nota:
        d["nota"] = nota
    return d


def selou(k):
    r = core.get(k) or {}
    return r.get("all_verified") is True


# as tres ANOTACOES (rotas que esperavam por esta versao), cada afirmacao testada contra o core lido: o registro existe? selou? o que NAO fechou fica dito (reescrito pela gerencia c1 em 19/10/2026)
NF = json.load(open(os.path.join(PK, "ESPERADOS_v394.json"), encoding="utf-8"))["n_formais"]
RF = core.get("rede_fock_v394") or {}
N_TG = sum(1 for p in V["pedras"] if p["modulo"].startswith("TGLExt.TimeGraviton")); N_F1 = sum(1 for p in V["pedras"] if p["modulo"].startswith("TGLExt.F1Fecho394."))
N_OUT = V["n_pedras"] - N_TG - N_F1 - 1   # modulo de outro grupo (se um delta acrescentar): dito no titulo, nunca escondido
assert N_OUT >= 0 and N_F1 == NF["rede_fontes"], "os modulos novos nao cobrem relogio M2, regra quadratica e rede de Fock"
T3 = []
c = selou("tempo_frequencia_v394") and selou("cunhagens_v394")
T3.append(anot("formal.tempo_consumacao_leitura_15out", "v394 SELADA %s: o tempo e a frequencia (modelo M2) %s" % (S, sim(c, "entram no selo, no escopo dito", "NAO selaram no rito")),
               "tempo_frequencia_v394 selou=%s (%s); %d teoremas de contrato; derivado no modelo M2 (2x2), com hipoteses fisicas nomeadas; a passagem de M2 ao setor modular, a rede e ao dispositivo NAO e' consequencia automatica. "
               "As leituras do operador (retorno de fase, dobra no nivel de c^3, a resposta antes da emissao) seguem [INPUT/ONTO]; o relatorio do Codex nao da' segundos universais nem propagador avancado para informacao controlavel." % (
                   selou("tempo_frequencia_v394"), V["reg394"]["tempo_frequencia_v394"]["verdict"], NF["tempo"]),
               sim(c, "ligar o relogio de M2 a uma identificacao fisica do dispositivo e do relogio (item aberto do contrato conjunto); a ponte material OH-modos fica adiada por ordem do operador; auditoria independente (quem construiu nao aprova).",
                   "segue aberto: integrar o que falta numa proxima versao.")))
c = selou("rede_fock_v394") and RF.get("whole_certificate_inhabited") is False
T3.append(anot("formal.f1_rede.concrete_bosonic_kinematics", "v394 SELADA %s: a cadeia de Fock, Takesaki e Maxwell (%d modulos) %s" % (S, N_F1, sim(c, "entra no selo, com o contrato conjunto ABERTO", "NAO selou no rito")),
               "rede_fock_v394 selou=%s (%s); %d declaracoes de contrato e %d fontes por sha256; %d componentes construidos sobre a mesma Fock canonica; whole_certificate_inhabited=%s: o contrato conjunto NAO foi habitado; abertos: %s." % (
                   selou("rede_fock_v394"), V["reg394"]["rede_fock_v394"]["verdict"], NF["rede"], NF["rede_fontes"], len(RF.get("constructed_components") or []), RF.get("whole_certificate_inhabited"), "; ".join(RF.get("open_joint_contract") or [])),
               sim(c, "habitar o contrato conjunto (CanonicalNetInput e os 21 campos restantes); nao chamar de rede global o que e' componente construido; H3 segue OPEN em toda direcao nula.",
                   "segue aberto: integrar o que falta numa proxima versao.")))
c = selou("regra_quadratica_v394")
T3.append(anot("conceitual.regra.prova_contrato", "v394 SELADA %s: a regra quadratica (RuleQuadraticResidual) %s" % (S, sim(c, "entra no selo", "NAO selou no rito")),
               "regra_quadratica_v394 selou=%s (%s); %d teoremas de contrato: o residuo quadratico da leitura contra uma ancora fixada antes da avaliacao e' nulo se e somente se a leitura e' a ancora, e' invariante no fluxo e e' positivo para ancora impossivel; "
               "construcao em M2, e ler isso como regra e' a representacao explicita do RuleTruthContract. A fala de 15/10 (a mentira como leitura sem ancora) esta tipada; a de 17/10 (a Palavra Falsa, o Nome Proprio sem referente) "
               "ainda nao foi cruzada com o residuo [DERIVED de leitura]." % (selou("regra_quadratica_v394"), V["reg394"]["regra_quadratica_v394"]["verdict"], NF["quadratica"]),
               sim(c, "cruzar a fala de 17/10 com o residuo; ligar a regra a um consumidor com dado observado (etapa posterior); auditoria independente (quem construiu nao aprova).",
                   "segue aberto: integrar o que falta numa proxima versao.")))
for d in T3:
    assert d["rota_id"] in ids, "a rota %s nao existe no mapa" % d["rota_id"]
ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
        "titulo": "v394 SELADA %s: o relogio M2 (%d modulos), a regra quadratica (1) e a rede de Fock, Takesaki e Maxwell do Codex (%d)%s; %d cunhagens de 14 a 19/10 por sha256; escada %s -> %s; o gate nao se move" % (
            S, N_TG, N_F1, (" e mais %d modulo(s) de outro grupo" % N_OUT) if N_OUT else "", len(V["verbatins"]), V["escada_antes"], V["teor"].split("/")[0]),
        "pergunta": "o candidato v394 selou com os %d modulos novos (relogio M2, regra quadratica, rede de Fock, Takesaki e Maxwell) e as cunhagens de 14 a 19/10 embutidas por sha256, sem mudar nenhum veredito fora da troca dita?" % V["n_pedras"],
        "dados": ["nenhum dado novo: leitura dos registros do core v394 (consumidores sinteticos)"],
        "metodo": "ensaio a seco do candidato; um lake build e um Audit no sandbox; rito completo; conferidor (deve mudar / nao pode mudar); leitura da rodada; superficies com a regra da linhagem completa; elo B(n) da Bancada (recibos)",
        "resultado": "%s | %s | %s | %s | %s | conferidor %s e %s | %d vereditos fora da troca dita mudaram (exigido 0)" % (
            V["reg394"]["tempo_frequencia_v394"]["verdict"], V["reg394"]["regra_quadratica_v394"]["verdict"], V["reg394"]["rede_fock_v394"]["verdict"], V["reg394"]["cunhagens_v394"]["verdict"], V["reg394"]["kh_n1_cobertura_v394"]["verdict"],
            V["conf_dm"], V["conf_np"], V["n_ver_mudaram"]),
        "defeito": "o relogio e' derivado no modelo M2 (2x2), com hipoteses fisicas nomeadas, e a passagem a setor modular, rede e dispositivo nao e' consequencia automatica; o contrato conjunto da rede nao foi habitado (whole_certificate_inhabited false); "
                   "H3 segue OPEN em toda direcao nula; beta so' se identifica no canal do dispositivo com uma taxa Gamma independente (R64, R65, R70); o selo gravitacional segue FORM_VERIFIED_CHI_FROM_CODATA; "
                   "os registros kh_n1_cobertura_v392 e kh_n1_cobertura_v393 foram corrigidos ao lado (k5 e h5 passam a <= 4; h2 e h3 viram pisos), porque a v394 quebra as igualdades que eles cobravam; as provas do Codex foram recompiladas no sandbox, nao refeitas",
        "nao_refazer": "a integracao dos %d modulos novos e a escada %s estao medidas; as provas do Codex foram recompiladas, nao refeitas; repetir so' com kernel novo" % (V["n_pedras"], V["teor"].split("/")[0]),
        "proximo_passo": "revisao independente do candidato e da cadeia (quem construiu nao aprova); o elo B(n) da Bancada Um (palavra do operador); custodia pela sessao do site; commit/push (operador)",
        "onde": PK, "artefatos": arts, "refs": sorted(d["rota_id"] for d in T3) + ["umpy.v392.pedras_e_barreiras", "formal.regra.integracao_v393", "formal.tempo_santo_fluxo_e_dissipacao",
                                                                               "formal.f1_takesaki.modular_identity_to_scaling", "formal.f1_rede.canonical_spectral_realization", "formal.f1_rede.geometric_identification"],
        "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move"}
for r in ROTA["refs"]:
    assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
REG = [ROTA] + T3
bad = [(d["rota_id"], violacoes(json.dumps(d, ensure_ascii=False))[:2]) for d in REG if violacoes(json.dumps(d, ensure_ascii=False))]
assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
J = os.path.join(HERE, "registro_mapa_v394.json"); json.dump(REG, open(J, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
quem = "claude-c1 (gerência), cadeia v394"
print("registro MONTADO (NAO registrado): %d registro(s) -> %s" % (len(REG), J))
print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
