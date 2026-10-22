# -*- coding: utf-8 -*-
"""registrar_mapa_v392.py -- MONTA (nao registra) o registro da v392 no mapa de rotas e imprime o comando (molde: registrar_mapa_v391.py). Rodar DEPOIS do fechar (handoff gravado).
Diferenca para a v391: o molde registrou UMA rota; a v392 tem de fechar o proximo passo das 8 rotas que esperam por ela (levantamento, 5.4) -- uma ANOTACAO em cada, dizendo o que o selo
FECHOU e o que NAO fechou (cada afirmacao e' testada contra o core/selo lidos por script: o registro novo existe? a pedra esta nas 'pedras_v392'?) -- e anotar a R3 (perito oficial = JUNO)
na rota neutrinos.m2.normalizacao. Mais a ROTA nova umpy.v392.pedras_e_barreiras. Fail-closed: o selo tem de ser a v392; as rotas citadas tem de existir no livro (leitura); a nova nao pode existir.
SAIDA: pos_rito\\registro_mapa_v392.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa)."""
import glob, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v392 as L
from guarda_p18_v392 import violacoes
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS"); PROG = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD")
V, PROB = L.ler()
if PROB:
    print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); sys.exit(2)
NOS = L.NOS
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo.get("um_version") == "v392", "o selo nao e a v392"
R = set(V["registros_novos"]); MODS = {p["modulo"].split(".")[-1] for p in V["pedras"]}
S = V["s16"]
# --- o livro do mapa (so leitura): as rotas existem; a nova nao
ids = set()
for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("tipo") == "ROTA":
        ids.add(d.get("rota_id"))
NOVA = "umpy.v392.pedras_e_barreiras"
assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
# --- as R3 do neutrino: lidas do consolidado do critico (CR-05), nunca digitadas
cr = json.load(open(os.path.join(PROG, "exame_12out", "J_SINTESE", "R2", "medidas", "CR_itens_consolidado.json"), encoding="utf-8"))["CR-05"]["o_que_resolveria"]
for t in ("2,21σ", "JUNO", "2,95σ", "2,44σ"):
    assert t in cr, "o texto do CR-05 nao traz %s" % t
b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v392_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v392_*.json")), key=os.path.getmtime)
arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(PK, "ESPERADOS_v392.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v392.json"),
        os.path.join(PK, "DIFF_KERNEL_v392.txt"), os.path.join(PK, "DIFF_v391_v392.diff"), os.path.join(NOS, "HANDOFF_v392_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v392.json")] + b3[-1:]
arts = [a for a in arts if os.path.exists(a)]


def sim(cond, fechado, aberto):
    return fechado if cond else aberto


def anot(rota_id, titulo, resultado, proximo, refs=None, nota=None, estatuto="REAL"):
    d = {"tipo": "ANOTACAO", "rota_id": rota_id, "estatuto": estatuto, "olhou_dados": False, "titulo": titulo, "resultado": resultado, "proximo_passo": proximo, "refs": [NOVA] + (refs or [])}
    if nota:
        d["nota"] = nota
    return d


T8 = []
c = "kh_n1_cobertura_v392" in R
T8.append(anot("kernel.auditoria.cobertura_axiomas_73_modulos", "v392 SELADA %s: o proximo passo «acrescentar a auditoria ao kernel e a checagem de cobertura» %s" % (S, sim(c, "esta FECHADO", "NAO esta fechado")),
               sim(c, "o registro kh_n1_cobertura_v392 esta no core selado (veredito: %s)." % (V["registros"].get("kh_n1_cobertura_v392") or {}).get("verdict"),
                   "o registro kh_n1_cobertura_v392 NAO esta no core selado: o axiom_report cobre so os #print axioms do Audit (%d declaracoes)." % V["axiom_report_n"]),
               sim(c, "auditoria independente do desenho da cobertura (quem construiu nao aprova).", "KH-N1 segue aberto: o desenho (a) run_cmd no Audit foi decidido em 13/10 mas nao entrou neste selo.")))
p = "Palavra" in MODS
T8.append(anot("kernel.leitura_cria_o_objeto_07out", "v392 SELADA %s: a pedra PALAVRA %s" % (S, sim(p, "esta INSTALADA no kernel", "NAO esta no kernel")),
               sim(p, "TGLExt.Palavra consta de pedras_v392 (bandeiras e declaracoes no trio, lidas do core). Registro palavra_v392: %s." % sim("palavra_v392" in R, "presente", "ausente"),
                   "TGLExt.Palavra nao consta de pedras_v392."),
               "o proximo passo «instalar TGLExt.Palavra, o registro e a secao do artigo» %s; a errata de nome «palavra aniquiladora» -> «letra» no artigo: conferir no .txt PT/EN (nao conferida por este script)." % sim(p and "palavra_v392" in R, "esta cumprido", "esta cumprido so em parte")))
c = "final_step_name_adopted_v392" in R
T8.append(anot("kernel.livro_de_cobrancas.otica", "v392 SELADA %s: o registro do nome do degrau final (Axioma) %s" % (S, sim(c, "esta no core selado", "NAO esta no core selado")),
               sim(c, "final_step_name_adopted_v392: %s." % (V["registros"].get("final_step_name_adopted_v392") or {}).get("verdict"), "o registro final_step_name_adopted_v392 nao veio no candidato selado."),
               sim(c, "FECHADO: a cunhagem definitiva do nome do degrau final consta do core e do artigo (conferir o artigo PT/EN).", "segue aberto: registrar final_step_name_adopted_v392 numa proxima versao.")))
c = {"V351DualScalingBridge", "AgapeNonVacuity"} <= MODS
T8.append(anot("programa.auditoria.f1_2_ponte_v351_07out", "v392 SELADA %s: a ponte V351 e a Agape nao vacua %s" % (S, sim(c, "estao INSTALADAS no kernel", "NAO estao (ambas) no kernel")),
               "pedras presentes em pedras_v392: V351DualScalingBridge=%s, AgapeNonVacuity=%s." % ("V351DualScalingBridge" in MODS, "AgapeNonVacuity" in MODS),
               sim(c, "FECHADO: a gerencia instalou na v392 o que a gerente TGL entregou; auditoria independente do selo.", "segue aberto: instalar as pedras que faltam.")))
c = {"LiganteLeiCampoCurvo", "LiganteLeiCampoCurvoTestemunha"} <= MODS
T8.append(anot("formal.f2_3.curved_field_ligand", "v392 SELADA %s: o ligante da lei de campo curva e a testemunha S7/S8 %s" % (S, sim(c, "estao INSTALADOS no kernel", "NAO estao (ambos) no kernel")),
               "pedras em pedras_v392: LiganteLeiCampoCurvo=%s, LiganteLeiCampoCurvoTestemunha=%s. O ligante e' CONDICIONAL ao H3 nomeado; ramo C e Temperatura ficam fora (F0.5 (l))." % ("LiganteLeiCampoCurvo" in MODS, "LiganteLeiCampoCurvoTestemunha" in MODS),
               sim(c, "FECHADO para a v392; seguem abertos o antecedente H3 em toda tela e direcao ([KNOWN] Jacobson 1995) e a familia de cunhas de Lorentz.", "segue aberto: instalar o que falta.")))
T8.append(anot("programa.qg_o_que_falta_07out", "v392 SELADA %s: «v392 (F0.5) com as erratas e a fiacao» -- cumprido em parte, dito item a item",
               "pedras: %s; registros novos alem dos dois fixos: %s; erratas ao lado nas superficies (CR-08, a ressalva do estatuto, a atribuicao de Coulomb, CR-02 na arvore) pela cadeia pos-rito." % (", ".join(sorted(MODS)), ", ".join(sorted(k for k in R if k not in L.REG_FIXOS)) or "nenhum"),
               "o que a v392 NAO fecha: a F8.1 (bandeiras do gate recalculadas), o antecedente H3, a familia de cunhas, e as decisoes do operador na lista unica."))
c = "beta_escala_errata_v392" in R
T8.append(anot("umpy.v388.selo_beta_corre_e_fase9_aberta", "v392 SELADA %s: a errata ao lado do token WHICH_MU_PER_RITE_OPEN %s" % (S, sim(c, "esta no core selado (beta_escala_errata_v392)", "NAO veio no candidato selado")),
               sim(c, "beta_escala_errata_v392: %s." % (V["registros"].get("beta_escala_errata_v392") or {}).get("verdict"), "o registro beta_escala_errata_v392 nao esta no core selado."),
               sim(c, "FECHADO para a escala; seguem abertas as fontes dos leitores locais por sha256 (regra 1 do V1).", "segue aberto: a errata ao lado do token numa proxima versao.")))
T8.append(anot("iald.ordem019.f0_3.memoria_v391", "v392 SELADA %s: destrava a F0.3 (a memoria comum no selo corrente)",
               "o selo corrente e' a v392 (um.py %s); a fonte do Jev passa ao selo corrente depois do aviso de selo. Esta anotacao NAO fecha o recibo do MCP da F0.3 (X17) nem a F0.3.SN1." % S,
               "gerencia: o aviso de selo a coordenadora (molde msg_v391_selada_coordenadora.md); coordenadora: release da memoria canonica da fila sobre a v392 e o status no cliente MCP do Codex."))
# --- R3 do neutrino
T8.append(anot("neutrinos.m2.normalizacao", "R3 (leitura ratificada pelo operador em 02/10): a entrada global do m2 e' a determinacao direta -- perito oficial = JUNO, 2,21σ; 2,95σ (NuFIT) e 2,44σ (Capozzi) sao reflexos globais, ao lado",
               "[DECLARADO -- lido do consolidado do critico CR-05, que cita o ledger do core da v391] a face e' a determinacao direta (JUNO autonomo, 2,21σ, σ do lado da previsao); NuFIT 2,95σ e Capozzi 2,44σ ficam ao lado com a diferenca dita. A v392 anota; NAO muda nenhuma conta.",
               "natureza em AGUARDA (a regra de morte pede duas determinacoes independentes >= 5σ); errata ao lado nas superficies que ainda dao 2,95σ como entrada: pendente (nao feita por esta cadeia).",
               estatuto="DECLARADO"))
for d in T8:
    assert d["rota_id"] in ids, "a rota %s nao existe no mapa" % d["rota_id"]
ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
        "titulo": "v392 SELADA %s: %d pedras novas no kernel (%s), escada %s -> %s, varredura lexical recursiva e detector de sorry; o gate nao se move" % (S, V["n_pedras"], ", ".join(sorted(MODS)), V["escada_antes"], V["teor"].split("/")[0]),
        "pergunta": "o candidato v392 selou com as pedras, a escada nova e os dois consertos de barreira, sem mudar nenhum veredito fora da troca dita?",
        "dados": ["nenhum dado novo: leitura dos registros do core v392"],
        "metodo": "ensaio a seco do candidato; rito completo; conferidor (deve mudar / nao pode mudar); leitura da rodada; superficies com a regra da linhagem completa; elo B(3) da Bancada (recibos)",
        "resultado": "%s | %s | conferidor %s e %s | %d vereditos fora da troca dita mudaram (exigido 0)" % (V["pedras_verdict"], V["varr_verdict"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"]),
        "defeito": "a F8.1 (as bandeiras do gate recalculadas) NAO e' fechada pela v392; o ligante da lei de campo curva e' condicional ao H3 nomeado; a hipotese BGL entra como tipo sem habitante; Verdade e' a projecao do posto e' leitura do operador sobre o termo",
        "nao_refazer": "a instalacao das pedras e a escada 6893 estao medidas; repetir so com kernel novo",
        "proximo_passo": "auditoria independente (quem construiu nao aprova); custodia pela sessao do site; commit/push (operador)",
        "onde": PK, "artefatos": arts, "refs": sorted(d["rota_id"] for d in T8),
        "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move"}
REG = [ROTA] + T8
bad = [(d["rota_id"], violacoes(json.dumps(d, ensure_ascii=False))[:2]) for d in REG if violacoes(json.dumps(d, ensure_ascii=False))]
assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
J = os.path.join(HERE, "registro_mapa_v392.json"); json.dump(REG, open(J, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
quem = "claude-c1 (gerência), cadeia v392"
print("registro MONTADO (NAO registrado): %d registro(s) -> %s" % (len(REG), J))
print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
