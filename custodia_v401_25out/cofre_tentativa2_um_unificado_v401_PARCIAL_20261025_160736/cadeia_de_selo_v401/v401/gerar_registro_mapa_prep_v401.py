# -*- coding: utf-8 -*-
"""gerar_registro_mapa_prep_v401.py -- monta registro_mapa_v401_prep.json (LISTA de registros, so' com campos de `rotas.py modelo`) a partir dos artefatos da cadeia (numeros e hashes LIDOS; nada digitado) e VALIDA cada
registro com a MESMA funcao que o mapa usa (rotas._valida), SEM registrar: importa rotas.py (so' constantes e funcoes), le rotas.jsonl para os ids e seqs existentes, nao escreve no livro. O registro no mapa e' ato da gerencia
(`rotas.py registrar <json> --quem ...`). Molde: gerar_registro_mapa_prep_v400.py.
uso: python -I -B -X utf8 gerar_registro_mapa_prep_v401.py   (roda DEPOIS de gerar_estado_v401.py: o ESTADO entra como artefato com o sha256 final)"""
import hashlib, importlib.util, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v401 as DL  # noqa: E402
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
J = lambda *p: json.load(open(os.path.join(HERE, *p), encoding="utf-8"))
P = lambda *p: os.path.join(HERE, *p)
CM = J("CANDIDATO_v401.json"); ESP = J("ESPERADOS_v401.json"); ENS = J("ensaio_a_seco_v401.json"); PIN = J("PINO_RECIBO_PRE_SELO_v401.json"); GU = J("GUARDAS_ESTATICAS_BANCADA_v401.json")
CMP = J("COMPARACAO_V400_v401.json"); POSIT = J("conferencia_rito_v401_POSITIVO_FALSO_NOS.json"); NEG = J("conferencia_rito_v401_CONTROLE_NEGATIVO_PRE_RITO.json")
SERV = J("bancada_B3_servico", "CONFERENCIA_EXIGENCIAS_SERVICO_v401.json"); KR = J("kernel", "KERNEL_RECIBO_v401.json")
S16 = CM["sha16"]; esc = CM["escada"]; fr = ENS["falsidade_registro"]; sc = ENS["sidecar"]
pedra = CM["kernel"]["pedras"]["TGLExt/FalsidadeDaInercia.lean"]
bn_atual = PIN["bancada_pina"]["deployment_id"]
nver = sum(1 for v in sc["verificacao"].values() if v is True)
ROTA_NOVA = "umpy.v401.cadeia_de_selo_preparada_25out"
ROTA_V400 = "umpy.v400.cadeia_de_selo_preparada_24out"; ROTA_BANC = "infra.bancada_um.sincronizacao_vnnn"; ROTA_PEDRA = "kernel.v401_falsidade_da_inercia"
assert ROTA_NOVA not in ids, "a rota da cadeia v401 ja' existe no livro: acrescente RESULTADO/ANOTACAO em vez de ROTA"
art_prep = [P("ESTADO_V401.md"), P("CANDIDATO_v401.json"), P("ESPERADOS_v401.json"), P("ensaio_a_seco_v401.json"), P("GUARDAS_ESTATICAS_BANCADA_v401.json"), P("COMPARACAO_V400_v401.json"),
            P("kernel", "KERNEL_RECIBO_v401.json"), P("PINOS_BN_v401.json"), P("PINO_RECIBO_PRE_SELO_v401.json"), P("PROVA_PRODUCAO_INTACTA_v401_pre_selo.json"), P("DIFF_KERNEL_v401.txt"),
            P("conferencia_rito_v401_CONTROLE_NEGATIVO_PRE_RITO.json"), P("conferencia_rito_v401_POSITIVO_FALSO_NOS.json"),
            P("EXAME_PONTOS_%s.json" % S16), P("SIMULACAO_ARVORE_NOS_%s.json" % S16), P("refazer_out_v401.txt"), P("pos_rito", "HARNESS_TEXTOS_ENSAIO_v401.json"), P("pos_rito", "HARNESS_FECHAR_SANDBOX_v401.json"), P("pedra_sha16_da_ordem.txt")]
art_prep = [x for x in art_prep if os.path.exists(x)]
refs = [x for x in (ROTA_V400, ROTA_BANC, ROTA_PEDRA) if x in ids]
rec_rota = {
    "tipo": "ROTA", "rota_id": ROTA_NOVA, "dominio": "SELO_UM_PY", "status": "EM_CURSO", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "v401 PREPARADA (candidato %s): a pedra «falsidade (simulacro) da inercia» (TGLExt.FalsidadeDaInercia, %d bandeiras) e o registro falsidade_da_inercia_v401; escada %d -> %d; ensaio a seco %s; nada instalado, nada selado" % (S16, pedra["bandeiras"], esc[0], esc[1], ENS["veredito"]),
    "pergunta": "o candidato v401, derivado por script da v400 selada, instala a pedra FalsidadeDaInercia (sha16 %s; a cadeia DERIVADA do axioma w(I)=1 e da lei de Takesaki [KNOWN]: nada que porte posto precede a impressao; a inercia nao e causa de si mesma; o zero e a consequencia da poda; a tensao projetada no atrator), o registro que a le a cada rito e a confere com o calculo no modelo oneScaling (beta = alfa . raiz de e em runtime), "
                "as seis inscricoes do operador de 25/10 e as ratificacoes, sela no ensaio a seco e passa as guardas estaticas da Bancada sobre o candidato?" % pedra["sha16"],
    "dados": ["nenhum dado novo e nenhum rito: a pedra compilada no sandbox (trio de axiomas, sem sorry), o kernel da v400 (byte a byte, mais o modulo novo) e as seis inscricoes do operador (sha256) sao so' lidos"],
    "metodo": "candidato DERIVADO por script da v400 selada (%d patches; comparacao AST: %d nos iguais, %d mudados, %d removidos, %d novos); kernel do sandbox k401c reconstruido (lake build incremental + Audit, recibo KERNEL_RECIBO_v401); guardas ESTATICAS da Bancada (a funcao ler_nos do esboco R3.5 pinado) sobre o candidato; "
              "ensaio a seco completo (kernel embutido == sandbox, exame dos pontos de chamada, simulacao da arvore do Nos, artigo PT/EN com pdflatex, .md, sidecar, quadro do topo); encanamento (instalar, reverter, rito, conferidor, ESPERADOS, citacoes, pos-rito, servico da Bancada) DERIVADO da v400 por motor com contagem exata por regra, nada executado" % (CM["n_patches"], CMP["iguais"] if isinstance(CMP["iguais"], int) else len(CMP["iguais"]), len(CMP["mudados"]), len(CMP["removidos"]), CMP["n_novos"]),
    "resultado": "falsidade_da_inercia_v401: %s | escada %d/%d | sidecar: %d objetos verificados | ensaio %s | conferidor: caminho positivo tudo_bate=%s (emulacao), controle negativo tudo_bate=%s | servico da Bancada: %d/%d condicoes estaticas | pre_selo %s (%d PASSA, %d FALHA; recibo refeito apos o reinicio do PC de 25/10, a Bancada ainda pina %s) | guardas estaticas: %s" % (
        fr.get("verdict", "?")[:90], esc[0], esc[1], nver, ENS["veredito"], str(POSIT["tudo_bate"]).lower(), str(NEG["tudo_bate"]).lower(), SERV["n_condicoes_ok"], SERV["n_condicoes"], PIN["veredito"], PIN["contagens"]["passa"], PIN["contagens"]["falha"], bn_atual, GU["veredito"]),
    "veredito": "falsidade_da_inercia_v401 (ensaio): %s | %s" % (fr.get("verdict", "?")[:120], GU["veredito"]),
    "defeito": "o rito real NAO rodou; instalar, rito e reverter (derivados), o pos_rito, os scripts de servico, o gerador, o runtime e os textos gerados sem revisao independente (quem construiu nao aprova) [DECLARADO]; a cadeia estendida e' [DERIVED] (axioma + lei de Takesaki [KNOWN] como campo da estrutura); "
               "a unica hipotese NOMEADA e' H_tau (tau e' a massa de Newton e a metrica de Einstein) [OPEN], que nenhum teorema usa; a ORDEM 025 ao Codex (sha16 3fd2b5a801071343, enfileirada) tenta tipa-la pela frente de luz de Bisognano-Wichmann: pendencia EXTERNA; E=mc2 [KNOWN, RS] nao e' termo do kernel; a RG e' o limite classico; "
               "a sexta inscricao e' um RECORTE DECLARADO da fala de 25/10 (a integra ficou em acervo privado, por decisao do operador); o recibo pre_selo vale enquanto a Bancada pinar %s; [LEGAL] publicar e' decisao do operador" % bn_atual,
    "nao_refazer": "a derivacao do candidato, a comparacao AST, as guardas estaticas e o ensaio estao medidos para o candidato %s; refazer so' se o runtime, os textos, o artigo ou o kernel mudarem (sh refazer_candidato_v401.sh); a pedra e a cadeia derivada nao se reprovam: estao compiladas (sha16 %s)" % (S16, pedra["sha16"]),
    "proximo_passo": "revisao independente do gerador, do runtime, dos derivados e dos textos gerados; so' depois instalar e rodar o rito (ato da gerencia, com o recibo pre_selo pinado e a Bancada ainda pinando %s); pos-rito; B(n) passo simples v400 -> v401 (parada e religamento do servico exigem V401_AUTORIZACAO_OPERADOR); custodia pela sessao do site" % bn_atual,
    "onde": "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v401",
    "artefatos": art_prep,
    "refs": refs,
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 25/10/2026. Consultas ao mapa antes: v401, inercia, falsidade -> a rota da pedra (%s, estudo da pedra com 12 teoremas, superada ao lado pela pedra de 20) e as rotas da v400 e do B(n). Validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move." % ROTA_PEDRA}
rec_pedra = {
    "tipo": "ANOTACAO", "rota_id": ROTA_PEDRA, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "A pedra FalsidadeDaInercia foi ESTENDIDA a 20 teoremas (sha16 %s): a cadeia e' [DERIVED]; a v401 a prepara (nao instalada)" % pedra["sha16"],
    "resultado": "a pedra de 12 teoremas (sha16 f9e4e877a5a9d688) foi superada ao lado pela de %d bandeiras (sha16 %s; trio de axiomas, sem sorry): nada que porte posto precede a impressao, a inercia nao e' causa de si mesma, o primeiro movimento e' a impressao, o zero e' a consequencia da poda, a tensao projetada no atrator; composicao falsidade_da_inercia_derivada; a unica hipotese NOMEADA e' H_tau [OPEN], que nenhum teorema usa (ORDEM 025 ao Codex, pendencia externa)" % (pedra["bandeiras"], pedra["sha16"]),
    "artefatos": [P("ESTADO_V401.md"), P("kernel", "KERNEL_RECIBO_v401.json"), P("pedra_sha16_da_ordem.txt")],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 25/10/2026. Validade no kernel nao e' creditacao; o gate nao se move."}
reg = [rec_rota] + [r for r in (rec_pedra,) if r["rota_id"] in ids]
for r in reg:
    if r["tipo"] == "ANOTACAO":
        assert r["rota_id"] in ids, ("a rota a anotar nao existe no livro", r["rota_id"])
assert len(reg) == 2, ("esperava a rota nova e a anotacao da pedra", [r["rota_id"] for r in reg])
campos_modelo = set(rotas.MODELO)
saida = []
for r in reg:
    extras = sorted(set(r) - campos_modelo)
    assert not extras, ("campos fora do modelo", r["rota_id"], extras)
    v = rotas._valida(r, set(ids), seqs)
    saida.append({"rota_id": v["rota_id"], "tipo": v["tipo"], "artefatos_n": len(v.get("artefatos", [])), "titulo_chars": len(v.get("titulo", ""))})
p = os.path.join(HERE, "registro_mapa_v401_prep.json"); b = (json.dumps(reg, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
if os.path.exists(p):
    open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_c1", "wb").write(open(p, "rb").read())
open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("VALIDO (rotas._valida, sem registrar):", json.dumps(saida, ensure_ascii=False)); print("registro_mapa_v401_prep.json", len(b), "bytes; sha16", hashlib.sha256(b).hexdigest()[:16])
