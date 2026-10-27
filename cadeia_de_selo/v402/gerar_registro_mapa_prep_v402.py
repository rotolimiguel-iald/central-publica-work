# -*- coding: utf-8 -*-
"""gerar_registro_mapa_prep_v402.py -- monta registro_mapa_v402_prep.json (LISTA de registros, so' com campos de `rotas.py modelo`) a partir dos artefatos da cadeia (numeros e hashes LIDOS; nada digitado) e VALIDA cada
registro com a MESMA funcao que o mapa usa (rotas._valida), SEM registrar: importa rotas.py (so' constantes e funcoes), le rotas.jsonl para os ids e seqs existentes, nao escreve no livro. O registro no mapa e' ato da gerencia
(`rotas.py registrar <json> --quem ...`). Molde: gerar_registro_mapa_prep_v401.py (que rodou na v401), com o delta da v402: TRES pedras (a ponte da escala dual, a queda sem geometria, a esperanca condicional), tres registros com funcao.
A rota e' a de PREPARACAO (umpy.v402.cadeia_de_selo_preparada_26out): o que foi examinado, o que foi testado e passou e o que NAO foi feito (nada instalado, rito nao rodado). O registro da v402 SELADA (a rota nova, as anotacoes e as erratas E1 a E4)
e' o de pos_rito\\registrar_mapa_v402.py, depois do rito.
Tolera arquivo ainda ausente (diz 'AUSENTE' no texto e nao lista o artefato); so' o CANDIDATO, o ESPERADOS e o ensaio a seco sao exigidos.
uso: python -I -B -X utf8 gerar_registro_mapa_prep_v402.py   (roda DEPOIS de gerar_estado_v402.py: o ESTADO entra como artefato com o sha256 final)"""
import hashlib, importlib.util, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
spec = importlib.util.spec_from_file_location("rotas_ro", os.path.join(MAPA, "rotas.py")); rotas = importlib.util.module_from_spec(spec); spec.loader.exec_module(rotas)
ids, seqs = set(), set()
for ln in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
    ln = ln.strip()
    if ln:
        r = json.loads(ln)
        if "rota_id" in r:
            ids.add(r["rota_id"])
        if isinstance(r.get("seq"), int):
            seqs.add(r["seq"])
P = lambda *p: os.path.join(HERE, *p)
sha256 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()


def J(*p):
    """JSON da pasta da cadeia, ou None se o arquivo estiver ausente/ilegivel (o texto diz AUSENTE; nunca falha por isso)."""
    try:
        return json.load(open(P(*p), encoding="utf-8"))
    except (OSError, ValueError):
        return None


def exigir(*p):
    d = J(*p)
    assert d is not None, "arquivo exigido ausente ou ilegivel: " + os.path.join(*p)
    return d


def mais_antigo_que_o_pos_rito(*p):
    """True se o arquivo existe e e' mais antigo que algum .py/.sh de pos_rito (um artefato 'velho' precisa ser regerado antes do registro)."""
    f = P(*p)
    if not os.path.exists(f):
        return False
    novo = max([os.path.getmtime(os.path.join(HERE, "pos_rito", n)) for n in os.listdir(P("pos_rito")) if n.endswith((".py", ".sh"))] or [0])
    return os.path.getmtime(f) < novo


CM = exigir("CANDIDATO_v402.json"); ESP = exigir("ESPERADOS_v402.json"); ENS = exigir("ensaio_a_seco_v402.json")
PIN = J("PINO_RECIBO_PRE_SELO_v402.json"); GU = J("GUARDAS_ESTATICAS_BANCADA_v402.json"); CMP = J("COMPARACAO_V401_v402.json")
POSIT = J("conferencia_rito_v402_POSITIVO_FALSO_NOS.json"); NEG = J("conferencia_rito_v402_CONTROLE_NEGATIVO_PRE_RITO.json")
SERV = J("bancada_B3_servico", "CONFERENCIA_EXIGENCIAS_SERVICO_v402.json"); KR = J("kernel", "KERNEL_RECIBO_v402.json"); PRE = J("PRECONDICOES_v402.json"); MEM = J("PINO_MEMORIA_PY_v402.json")
CONFPS = J("bateria_pre_selo", "conferencia_pelo_esboco_v402.json"); PROVA = J("PROVA_PRODUCAO_INTACTA_v402_pre_selo.json")
S16 = CM["sha16"]; esc = ESP["escada_v401_e_v402"]; NF = ESP["n_bandeiras_novas"]
assert S16 == ESP["candidato_sha16"] == ENS["sha16"], "o candidato de CANDIDATO, ESPERADOS e ensaio nao e' um so'"
assert esc[1] - esc[0] == NF == sum(ESP["n_bandeiras_por_grupo"].values()), "a escada nao fecha com as bandeiras novas"
assert hashlib.sha256(open(P("um_v402_candidato.py"), "rb").read()).hexdigest()[:16] == S16, "o arquivo do candidato != o sha16 de CANDIDATO_v402.json"
GR = ("ponte", "queda", "esperanca")
NOMES_REG = {"ponte": "ponte_da_escala_dual_v402", "queda": "queda_sem_geometria_v402", "esperanca": "esperanca_condicional_v402"}
reg = ENS["v402_registros"]
assert set(reg) == set(GR) and all(reg[g]["all_verified"] is True for g in GR), "algum dos tres registros nao selou no ensaio a seco"
MOD = {g: ESP["teoremas_das_pedras"][g].split(".")[1] for g in GR}                      # PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional
PED = {g: ESP["pedras"]["TGLExt/%s.lean" % MOD[g]] for g in GR}
pins_ordem = exigir("pedras_sha16_da_ordem.json")
assert all(PED[g]["sha16"] == pins_ordem[g] for g in GR), "o sha16 de uma pedra != o pino da ordem da gerencia"
assert all(sha256(P("pedra", MOD[g] + ".lean")) == PED[g]["sha256"] for g in GR), "uma pedra em pedra\\ != o sha256 de ESPERADOS"
nver = sum(1 for v in (ENS["sidecar"].get("verificacao") or {}).values() if v is True)
bn_atual = (PIN or {}).get("bancada_pina", {}).get("deployment_id", "AUSENTE")
ROTA_NOVA = "umpy.v402.cadeia_de_selo_preparada_26out"
ROTA_V401 = "umpy.v401.selada_falsidade_da_inercia_25out"; ROTA_PREP401 = "umpy.v401.cadeia_de_selo_preparada_25out"; ROTA_BANC = "infra.bancada_um.sincronizacao_vnnn"
ROTA_PONTE = "kernel.ordem025.ponte_escala_dual"; ROTA_QUEDA = "kernel.v402_queda_sem_geometria"; ROTA_ESPER = "kernel.v402_esperanca_condicional_e_nome"; ROTA_PEDRA401 = "kernel.v401_falsidade_da_inercia"
ROTA_DE = {"ponte": ROTA_PONTE, "queda": ROTA_QUEDA, "esperanca": ROTA_ESPER}
assert ROTA_NOVA not in ids, "a rota da cadeia v402 ja' existe no livro: acrescente RESULTADO/ANOTACAO em vez de ROTA"
for rr in (ROTA_V401, ROTA_PREP401, ROTA_BANC, ROTA_PONTE, ROTA_QUEDA, ROTA_ESPER, ROTA_PEDRA401):
    assert rr in ids, "a rota citada nao existe no livro: " + rr
art_prep = [P("ESTADO_V402.md"), P("CANDIDATO_v402.json"), P("um_v402_candidato.py"), P("ESPERADOS_v402.json"), P("ensaio_a_seco_v402.json"), P("GUARDAS_ESTATICAS_BANCADA_v402.json"), P("COMPARACAO_V401_v402.json"),
            P("kernel", "KERNEL_RECIBO_v402.json"), P("PINOS_BN_v402.json"), P("PINO_RECIBO_PRE_SELO_v402.json"), P("PROVA_PRODUCAO_INTACTA_v402_pre_selo.json"), P("DIFF_KERNEL_v402.txt"),
            P("conferencia_rito_v402_CONTROLE_NEGATIVO_PRE_RITO.json"), P("conferencia_rito_v402_POSITIVO_FALSO_NOS.json"), P("PRECONDICOES_v402.json"), P("PINO_MEMORIA_PY_v402.json"),
            P("EXAME_PONTOS_%s.json" % S16), P("SIMULACAO_ARVORE_NOS_%s.json" % S16), P("refazer_out_v402.txt"), P("pos_rito", "HARNESS_TEXTOS_ENSAIO_v402.json"), P("pos_rito", "HARNESS_FECHAR_SANDBOX_v402.json"),
            P("pedras_sha16_da_ordem.json")] + [P("pedra", MOD[g] + ".lean") for g in GR]
ausentes = [os.path.basename(x) for x in art_prep if not os.path.exists(x)]
art_prep = [x for x in art_prep if os.path.exists(x)]
refs = [x for x in (ROTA_V401, ROTA_PREP401, ROTA_BANC, ROTA_PONTE, ROTA_QUEDA, ROTA_ESPER, ROTA_PEDRA401) if x in ids]
B = lambda x: "sim" if x else "NAO"
tf = lambda x: "AUSENTE" if x is None else str(bool(x)).lower()


def txt_pre():
    if PRE is None:
        return "pre-condicoes (p00): AUSENTE"
    falhas = [c["checagem"][:60] for c in PRE["checagens"] if not c["ok"]]
    vel = " (o arquivo e' mais antigo que arquivos de pos_rito: precisa ser regerado)" if mais_antigo_que_o_pos_rito("PRECONDICOES_v402.json") else ""
    return "pre-condicoes (p00): %s (%d checagens%s)%s" % ("TODAS OK" if PRE["ok"] else "FALHARAM", len(PRE["checagens"]), "" if PRE["ok"] else ": " + "; ".join(falhas), vel)


rot_resumo = " | ".join("%s: %s… (%d checagens)" % (NOMES_REG[g], reg[g]["verdict"][:90], reg[g]["n_checks"]) for g in GR)
rec_rota = {
    "tipo": "ROTA", "rota_id": ROTA_NOVA, "dominio": "SELO_UM_PY", "status": "EM_CURSO", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "v402 PREPARADA (candidato %s): a ponte da escala dual, a queda sem geometria e a esperanca condicional (TGLExt.%s, %s e %s, %d bandeiras; nomes provisorios) e os registros com funcao %s, %s e %s; escada %d -> %d; ensaio a seco %s; nada instalado, nada selado" % (
        S16, MOD["ponte"], MOD["queda"], MOD["esperanca"], NF, NOMES_REG["ponte"], NOMES_REG["queda"], NOMES_REG["esperanca"], esc[0], esc[1], ENS["veredito"]),
    "pergunta": "o candidato v402, derivado por script da v401 selada, instala as TRES pedras (sha16 %s, %s e %s: a ponte do Codex, ORDEM 025, copia de bytes; a queda sem geometria; a esperanca condicional = o Nome), os tres registros que as leem a cada rito e as conferem com o calculo "
                "(beta = alfa x raiz de e em runtime), cunhagens_v402 (as tres inscricoes do operador de 26/10 por sha256, as decisoes D11 a D16 e as erratas E1 a E4 da integracao da ponte) e kh_n1_cobertura_v402, sela no ensaio a seco e passa as guardas estaticas da Bancada sobre o candidato?" % (
                    PED["ponte"]["sha16"], PED["queda"]["sha16"], PED["esperanca"]["sha16"]),
    "dados": ["nenhum dado novo e nenhum rito: as pedras compiladas no sandbox (trio de axiomas, sem sorry), o kernel da v401 (byte a byte, mais os tres modulos novos) e as tres inscricoes do operador (sha256) sao so' lidos"],
    "metodo": "candidato DERIVADO por script da v401 selada (%d patches%s); kernel do sandbox k402c reconstruido (lake build incremental + Audit, recibo KERNEL_RECIBO_v402%s); guardas ESTATICAS da Bancada (a funcao ler_nos do esboco R3.5 pinado) sobre o candidato; "
              "ensaio a seco completo (kernel embutido == sandbox, exame dos pontos de chamada, simulacao da arvore do Nos, artigo PT/EN com pdflatex, .md, sidecar, quadro do topo); encanamento (instalar, reverter, rito, conferidor, ESPERADOS, citacoes, pos-rito, servico da Bancada) DERIVADO da v401 por motor com contagem exata por regra, nada executado" % (
                  CM["n_patches"], "" if CMP is None else "; comparacao AST: %s nos iguais, %d mudados, %d removidos, %d novos" % (CMP["iguais"] if isinstance(CMP["iguais"], int) else len(CMP["iguais"]), len(CMP["mudados"]) if not isinstance(CMP["mudados"], int) else CMP["mudados"], len(CMP["removidos"]) if not isinstance(CMP["removidos"], int) else CMP["removidos"], CMP["n_novos"]),
                  "" if KR is None else ", rc %s, sorry %s" % (KR["rc"], KR["sorry"])),
    "resultado": "%s | escada %d -> %d (teoremas limpos %d/%d) | sidecar: %d objetos verificados | ensaio %s (%d verificacoes de unidade) | conferidor: caminho positivo tudo_bate=%s (emulacao), controle negativo tudo_bate=%s (esperado: o Nos ainda e' a v401) | servico da Bancada: %s | pre_selo %s | guardas estaticas: %s | %s" % (
        rot_resumo, esc[0], esc[1], ENS["escada"][0], ENS["escada"][1], nver, ENS["veredito"], len(ENS["unidade"]), tf(POSIT and POSIT["tudo_bate"]), tf(NEG and NEG["tudo_bate"]),
        "AUSENTE" if SERV is None else "%d/%d condicoes estaticas" % (SERV["n_condicoes_ok"], SERV["n_condicoes"]),
        "AUSENTE" if PIN is None else "%s (%s PASSA, %s FALHA; Bancada pina %s; utilizavel como recibo do B(n): %s)" % (PIN["veredito"], PIN["contagens"]["passa"], PIN["contagens"]["falha"], bn_atual, tf(PIN["utilizavel_como_recibo_pre_selo_do_B_n"])),
        "AUSENTE" if GU is None else GU["veredito"], txt_pre()),
    "veredito": "ensaio a seco: %s | %s" % (ENS["veredito"], "AUSENTE" if GU is None else GU["veredito"]),
    "defeito": "o rito real NAO rodou; instalar, rito e reverter (derivados), o pos_rito, os scripts de servico, o gerador, o runtime e os textos gerados sem revisao independente (quem construiu nao aprova) [DECLARADO]; as pedras compoem por citacao: a lei de escala de Takesaki e' dado (campo de DualScalingData, [KNOWN]) e os registros CONFEREM os teoremas, nao os provam; "
               "as erratas E1 a E4 (H_tau na forma literal REFUTADA no kernel; Inertial = vetor zero; rest_energy_eq_mc2 nao e' E = mc^2 composta da escala; a proveniencia da entrega do Codex) estao ditas ao lado no candidato, em nome proprio da gerencia c1, e entram no mapa DEPOIS do selo; as pendencias H_BW, H_cal, H3, a assinatura (4,0) x (1,3) e rank c = 4 seguem [OPEN]; "
               "IsotropicPost e' hipotese nomeada e a dimensao 3 nao e' provada; o indice 1/beta do Nome e' condicional e sem instancia; os nomes dos tres modulos e dos registros sao provisorios (o operador nomeia, D16); a pergunta e a resposta de 26/10 sao [DECLARADO]; "
               "o recibo pre_selo vale enquanto a Bancada pinar %s; [LEGAL] publicar e' decisao do operador%s" % (bn_atual, "" if not ausentes else "; artefatos ainda AUSENTES na hora desta geracao: " + ", ".join(ausentes)),
    "nao_refazer": "a derivacao do candidato, a comparacao AST, as guardas estaticas e o ensaio estao medidos para o candidato %s; refazer so' se o runtime, os textos, o artigo ou o kernel mudarem (sh refazer_candidato_v402.sh); as pedras nao se reprovam: estao compiladas (sha16 %s, %s e %s)" % (
        S16, PED["ponte"]["sha16"], PED["queda"]["sha16"], PED["esperanca"]["sha16"]),
    "proximo_passo": "revisao independente do gerador, do runtime, dos derivados e dos textos gerados; so' depois instalar e rodar o rito (ato da gerencia, com o recibo pre_selo pinado e a Bancada ainda pinando %s); pos-rito; B(n) passo simples v401 -> v402 (parada e religamento do servico exigem V402_AUTORIZACAO_OPERADOR); custodia pela sessao do site; o operador nomeia as pedras" % bn_atual,
    "onde": "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v402",
    "artefatos": art_prep,
    "refs": refs,
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao, A2), 26/10/2026. Consultas ao mapa antes: v402, ponte da escala dual, queda sem geometria, esperanca condicional, ordem025 -> as rotas das tres pedras (%s, %s e %s), a da pedra anterior (%s) e a da v401 selada; "
            "a rota da ponte so' aparece por «ordem025» (o consultar «ponte da escala dual» nao devolve nada). Validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move." % (ROTA_PONTE, ROTA_QUEDA, ROTA_ESPER, ROTA_PEDRA401)}


def anot_pedra(g):
    r = reg[g]; p = PED[g]
    extra = (" As erratas E1 a E4 da integracao estao ditas ao lado no candidato (registro cunhagens_v402, artigo e handoff), em nome proprio da gerencia c1; a forma literal de H_tau e' REFUTADA no kernel (lift_mass_not_selected, positive_weight_cannot_be_invariant_mass); o mapa recebe as erratas com o seq do registro corrigido DEPOIS do selo." if g == "ponte" else "")
    return {"tipo": "ANOTACAO", "rota_id": ROTA_DE[g], "estatuto": "REAL", "olhou_dados": False,
            "titulo": "A pedra %s esta no candidato v402 (%s): a v402 a prepara (nao instalada, nao selada)" % (MOD[g], S16),
            "resultado": "pedra %s (sha16 %s, %d bandeiras novas; composicao %s, estrela %s) no kernel embutido do candidato; o registro %s selou no ensaio a seco com %d checagens do calculo (beta = alfa x raiz de e em runtime); escada %d -> %d; "
                         "o rito real nao rodou e nada foi instalado no Nos (o um.py do Nos segue %s, a v401 selada).%s" % (MOD[g], p["sha16"], p["bandeiras"], ESP["teoremas_das_pedras"][g].split(".")[-1], ESP["estrelas_v402"][g]["teorema"].split(".")[-1], NOMES_REG[g], r["n_checks"], esc[0], esc[1], ESP["origem_sha16"], extra),
            "proximo_passo": "revisao independente do candidato e da cadeia; o operador nomeia o modulo (nome provisorio, D16) e decide instalar e rodar o rito; o selo (se vier) e' registrado depois por registrar_mapa_v402.py.",
            "refs": [ROTA_NOVA],
            "artefatos": [x for x in (P("pedra", MOD[g] + ".lean"), P("kernel", "KERNEL_RECIBO_v402.json"), P("ESTADO_V402.md")) if os.path.exists(x)],
            "nota": "Em nome proprio da gerencia c1 (subagente de preparacao, A2), 26/10/2026. Validade no kernel nao e' creditacao; o gate nao se move."}


reg_final = [rec_rota] + [anot_pedra(g) for g in GR]
for r in reg_final:
    if r["tipo"] == "ANOTACAO":
        assert r["rota_id"] in ids, ("a rota a anotar nao existe no livro", r["rota_id"])
campos_modelo = set(rotas.MODELO)
saida = []
for r in reg_final:
    extras = sorted(set(r) - campos_modelo)
    assert not extras, ("campos fora do modelo", r["rota_id"], extras)
    v = rotas._valida(json.loads(json.dumps(r)), set(ids), seqs)
    saida.append({"rota_id": v["rota_id"], "tipo": v["tipo"], "artefatos_n": len(v.get("artefatos", [])), "titulo_chars": len(v.get("titulo", ""))})
# a guarda de palavras recusadas (P18) sobre o texto gerado
spg = importlib.util.spec_from_file_location("guarda_p18_v402", P("guarda_p18_v402.py")); gp = importlib.util.module_from_spec(spg); spg.loader.exec_module(gp)
viol = [(r["rota_id"], gp.violacoes(json.dumps(r, ensure_ascii=False))[:2]) for r in reg_final if gp.violacoes(json.dumps(r, ensure_ascii=False))]
assert not viol, ("a guarda de texto (P18) achou violacao(oes)", viol)
p = P("registro_mapa_v402_prep.json"); b = (json.dumps(reg_final, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
if os.path.exists(p) and open(p, "rb").read() != b:
    open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_a2", "wb").write(open(p, "rb").read())
open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("VALIDO (rotas._valida, sem registrar):", json.dumps(saida, ensure_ascii=False)); print("registro_mapa_v402_prep.json", len(b), "bytes; sha16", hashlib.sha256(b).hexdigest()[:16])
print("artefatos listados: %d; AUSENTES nesta geracao: %s" % (len(art_prep), ausentes or "nenhum"))
