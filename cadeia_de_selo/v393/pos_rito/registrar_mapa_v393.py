# -*- coding: utf-8 -*-
"""registrar_mapa_v393.py -- MONTA (nao registra) o registro da v393 no mapa de rotas e imprime o comando (molde: registrar_mapa_v392.py). Rodar DEPOIS do fechar (handoff gravado).
A v393 e' menor que a v392: UMA rota nova, umpy.v393.regra_e_coracao, mais tres ANOTACOES nas rotas que esperavam por ela (a integracao da regra, o motor continuo e a forma de alfa), cada afirmacao
testada contra o core/selo lidos por script (o registro existe? selou? o que NAO fechou fica dito). Fail-closed: o selo tem de ser a v393; as rotas anotadas tem de existir no livro (leitura); a nova nao pode existir.
SAIDA: pos_rito\\registro_mapa_v393.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa)."""
import glob, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v393 as L
from guarda_p18_v393 import violacoes
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
V, PROB = L.ler()
if PROB:
    print("REGISTRO RECUSADO -- a leitura da rodada tem problema(s):", PROB); sys.exit(2)
NOS = L.NOS
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo.get("um_version") == "v393", "o selo nao e a v393"
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
NOVA = "umpy.v393.regra_e_coracao"
assert NOVA not in ids, "a rota %s ja existe no mapa" % NOVA
b3 = sorted(glob.glob(os.path.join(PK, "bancada_B3", "RECIBO_SINCRONIZACAO_v393_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v393_*.json")), key=os.path.getmtime)
arts = [os.path.join(NOS, "um.py"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(PK, "ESPERADOS_v393.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v393.json"),
        os.path.join(PK, "DIFF_KERNEL_v393.txt"), os.path.join(PK, "DIFF_v392_v393.diff"), os.path.join(NOS, "HANDOFF_v393_CUSTODIA.md"), os.path.join(PK, "MANIFESTO_ARQUIVO_v393.json")] + b3[-1:]
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


T3 = []
c = selou("pedras_v393") and selou("regra_consumidor_v393")
T3.append(anot("formal.regra.integracao_v393", "v393 SELADA %s: a integracao da regra no um.py %s" % (S, sim(c, "esta FEITA no selo", "NAO esta feita no selo")),
               "pedras_v393 selou=%s (%s); regra_consumidor_v393 selou=%s (%s); cunhagens_regra_v393 selou=%s. As quatro cunhagens do operador entram por sha256 (%s)." % (
                   selou("pedras_v393"), V["pedras_verdict"], selou("regra_consumidor_v393"), V["cons"]["verdict"], selou("cunhagens_regra_v393"), ", ".join("%s %s" % (k, v["sha16"]) for k, v in V["verbatins"].items())),
               sim(c, "auditoria independente (quem construiu nao aprova); a completude relativa ao alvo segue hipotese declarada [INPUT/ONTO]; as leituras filosofica e juridica sao do operador.",
                   "segue aberto: integrar o que falta numa proxima versao.")))
c = selou("regra_consumidor_v393")
T3.append(anot("formal.regra_motor_continuo", "v393 SELADA %s: o motor continuo com a regra %s" % (S, sim(c, "esta ligado e EXECUTADO no rito", "NAO selou no rito")),
               "regra_consumidor_v393: %s pontos, %s verificacoes; satisfacao admitida para o alvo correto e recusada para o incompativel; criterio exato (kernel) distinto da tolerancia numerica (%s; igualdade exata NAO afirmada); "
               "espaco fixo de dimensao complexa %s; replica do Codex (informativa) com hash final igual=%s." % (V["cons"]["pontos"], V["cons"]["verificacoes"], _tol(V), V["cons"]["dimfix"], V["cons"]["replica_hash_igual"]),
               "o consumidor e' sintetico (nenhum dado observado) e a unicidade do criterio vale para o alvo dado, nao para todo estado fixo; ligar a regra a um consumidor com dado observado e' etapa posterior.",
               estatuto="REAL"))
c = selou("coracao_e_selo_gravitacional_v393")
T3.append(anot("outro.alfa_laboratorio", "v393 SELADA %s: o coracao e o selo gravitacional %s" % (S, sim(c, "selaram no rito, com o limite dito", "NAO selaram no rito")),
               "coracao_e_selo_gravitacional_v393: %s. A FORMA de alfa e' derivada (1 = q^2 + alfa^2); o VALOR de alfa e' a leitura do CODATA, previsao independente=%s; G derivado=%s; evidencia espectral independente: %s. "
               "A v393 NAO deriva alfa do 1 e NAO prediz alfa: documenta o limite." % (V["cora"]["verdict"], V["cora"]["prev"], V["cora"]["G"], V["cora"]["espectral_hoje"]),
               "o que fecharia: uma cadeia espectral PINADA independente do CODATA (artefatos relidos por sha256); hoje ausente. Afirmacoes de laboratorio sobre a forma de alfa seguem fora deste selo.",
               estatuto="REAL"))
for d in T3:
    assert d["rota_id"] in ids, "a rota %s nao existe no mapa" % d["rota_id"]
ROTA = {"tipo": "ROTA", "rota_id": NOVA, "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
        "titulo": "v393 SELADA %s: a regra (%d pedras: %s) e o coracao; escada %s -> %s; o gate nao se move" % (S, V["n_pedras"], ", ".join(sorted(MODS)), V["escada_antes"], V["teor"].split("/")[0]),
        "pergunta": "o candidato v393 selou com as tres pedras da regra, o consumidor numerico que a consome e o selo do coracao, sem mudar nenhum veredito fora da troca dita?",
        "dados": ["nenhum dado novo: leitura dos registros do core v393 (consumidor sintetico)"],
        "metodo": "ensaio a seco do candidato; rito completo; conferidor (deve mudar / nao pode mudar); leitura da rodada; superficies com a regra da linhagem completa; elo B(3) da Bancada (recibos)",
        "resultado": "%s | %s | %s | conferidor %s e %s | %d vereditos fora da troca dita mudaram (exigido 0)" % (V["pedras_verdict"], V["cons"]["verdict"], V["cora"]["verdict"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"]),
        "defeito": "a completude relativa ao alvo e' hipotese declarada, nao teorema extraido do nome; a tolerancia numerica nao e' igualdade exata; o valor de alfa e' a leitura do CODATA (sem previsao independente) e G nao e' derivado; "
                   "o registro kh_n1_cobertura_v392 foi re-pinado a uma copia (o arquivo foi regravado pelo pos_build da v392 depois do rito) e as suas igualdades viraram pisos, com errata ao lado",
        "nao_refazer": "a integracao das tres pedras da regra e a escada 7045 estao medidas; repetir so com kernel novo",
        "proximo_passo": "auditoria independente (quem construiu nao aprova); custodia pela sessao do site; commit/push (operador)",
        "onde": PK, "artefatos": arts, "refs": sorted(d["rota_id"] for d in T3) + ["umpy.v392.pedras_e_barreiras", "conceitual.regra.negatividade_juridica", "conceitual.regra.prova_contrato"],
        "nota": "validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move"}
for r in ROTA["refs"]:
    assert r in ids, "a rota citada em refs nao existe no mapa: %s" % r
REG = [ROTA] + T3
bad = [(d["rota_id"], violacoes(json.dumps(d, ensure_ascii=False))[:2]) for d in REG if violacoes(json.dumps(d, ensure_ascii=False))]
assert not bad, "a guarda de texto (P18) achou violacao(oes): %r" % bad
J = os.path.join(HERE, "registro_mapa_v393.json"); json.dump(REG, open(J, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
quem = "claude-c1 (gerência), cadeia v393"
print("registro MONTADO (NAO registrado): %d registro(s) -> %s" % (len(REG), J))
print("COMANDO (ato da gerencia): python %s registrar \"%s\" --quem \"%s\"" % (os.path.join(MAPA, "rotas.py"), J, quem))
print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")
