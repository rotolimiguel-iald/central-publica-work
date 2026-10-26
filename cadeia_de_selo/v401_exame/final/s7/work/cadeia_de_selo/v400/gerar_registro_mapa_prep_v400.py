# -*- coding: utf-8 -*-
"""gerar_registro_mapa_prep_v400.py -- monta registro_mapa_v400_prep.json (LISTA de registros, SO' com campos de `rotas.py modelo`) a partir dos artefatos da cadeia (numeros e hashes LIDOS; nada digitado) e VALIDA cada
registro com a MESMA funcao que o mapa usa (rotas._valida), SEM registrar: importa rotas.py (so' constantes e funcoes), le rotas.jsonl para os ids e seqs existentes, nao escreve no livro. O registro no mapa e' ato da gerencia
(`rotas.py registrar <json> --quem ...`). ESCRITO A MAO na v400 (a v400 e' uma CORRECAO: nenhuma pedra, nenhum registro novo). Molde: gerar_registro_mapa_prep_v399.py.
uso: python -I -B -X utf8 gerar_registro_mapa_prep_v400.py   (roda DEPOIS de gerar_estado_v400.py: o ESTADO entra como artefato com o sha256 final)"""
import hashlib, importlib.util, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
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
CM = J("CANDIDATO_v400.json"); ESP = J("ESPERADOS_v400.json"); ENS = J("ensaio_a_seco_v400.json"); PIN = J("PINO_RECIBO_PRE_SELO_v400.json"); GU = J("GUARDAS_ESTATICAS_BANCADA_v400.json"); SAL = J("salto_r3_4", "SALTO_R3_4_MEDIDO_v400.json")
RM = J("RUNTIME_MONTAGEM_v400.json"); CMP = J("COMPARACAO_V399_v400.json"); POSIT = J("conferencia_rito_v400_POSITIVO_FALSO_NOS.json"); NEG = J("conferencia_rito_v400_CONTROLE_NEGATIVO_PRE_RITO.json")
HT = J("pos_rito", "HARNESS_TEXTOS_ENSAIO_v400.json"); HF = J("pos_rito", "HARNESS_FECHAR_SANDBOX_v400.json"); SERV = J("bancada_B3_servico", "CONFERENCIA_EXIGENCIAS_SERVICO_v400.json"); KR = J("kernel", "KERNEL_RECIBO_v400.json")
P = lambda *p: os.path.join(HERE, *p)
S16 = CM["sha16"]; esc = CM["escada"]; co = CM["guarda_alpha_unica_da_bancada"]
sar = ENS["selo_acom_registro"]; dcr = ENS["declaracao_registro"]; sc = ENS["sidecar"]
bn_atual = PIN["bancada_pina"]["deployment_id"]
ROTA_NOVA = "umpy.v400.cadeia_de_selo_preparada_24out"
ROTA_V399 = "umpy.v399.cadeia_de_selo_preparada_24out"; ROTA_BANC = "infra.bancada_um.sincronizacao_vnnn"; ROTA_SELO = "umpy.v399.selo_pela_propria_tecnologia_estudo_24out"
assert ROTA_NOVA not in ids, "a rota da cadeia v400 ja' existe no livro: acrescente RESULTADO/ANOTACAO em vez de ROTA"
art_prep = [P("ESTADO_V400.md"), P("CANDIDATO_v400.json"), P("ESPERADOS_v400.json"), P("ensaio_a_seco_v400.json"), P("GUARDAS_ESTATICAS_BANCADA_v400.json"), P("salto_r3_4", "SALTO_R3_4_MEDIDO_v400.json"), P("COMPARACAO_V399_v400.json"), P("RUNTIME_MONTAGEM_v400.json"),
            P("kernel", "KERNEL_RECIBO_v400.json"), P("PINOS_BN_v400.json"), P("PINO_RECIBO_PRE_SELO_v400.json"), P("DIFF_KERNEL_v400.txt"), P("conferencia_rito_v400_CONTROLE_NEGATIVO_PRE_RITO.json"), P("conferencia_rito_v400_POSITIVO_FALSO_NOS.json"),
            P("EXAME_PONTOS_%s.json" % S16), P("SIMULACAO_ARVORE_NOS_%s.json" % S16), P("refazer_out_v400.txt"), P("pos_rito", "HARNESS_TEXTOS_ENSAIO_v400.json"), P("pos_rito", "HARNESS_FECHAR_SANDBOX_v400.json")]
art_prep = [x for x in art_prep if os.path.exists(x)]
refs = [x for x in (ROTA_V399, ROTA_BANC, ROTA_SELO, "umpy.v398.sonico_e_afinacao_das_cordas_na_fractalizacao_do_um") if x in ids]
rec_rota = {
    "tipo": "ROTA", "rota_id": ROTA_NOVA, "dominio": "SELO_UM_PY", "status": "EM_CURSO", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "v400 PREPARADA (candidato %s): a CORRECAO da v399 -- o alfa de uma linha so' (a Bancada Um recusara a v399 por ALPHA_LINHA_NAO_UNICA) e o beta do registro do selo ACOM conferido contra o core; nenhum modulo novo, nenhum registro novo, nenhuma inscricao nova; escada %d -> %d; ensaio a seco %s; nada instalado, nada selado" % (S16, esc[0], esc[1], ENS["veredito"]),
    "pergunta": "o candidato v400, derivado por script da v399 selada com UMA correcao -- a secao do selo ACOM deixa de redeclarar o alfa (le o SEALED_CODATA_ALPHA do programa; uma so' linha de alfa no um.py, a de numero %d) e a checagem do beta do registro confronta o beta do runtime com o beta do core a 1e-9 (a da v399 era uma tautologia) -- "
                "sela no ensaio a seco e passa, ANTES de instalar, as guardas estaticas do contrato da Bancada (a funcao ler_nos do esboco R3.5 pinado), sem mudar o kernel, sem mudar nenhum veredito da v399 fora do hash proprio no estatuto da prova e sem mexer no quadro do topo?" % co["linha_do_alfa"],
    "dados": ["nenhum dado novo e nenhum rito: o kernel e' o da v399 (byte a byte); o bloco embutido do operador NAO mudou (hash %s); o recibo da recusa da Bancada a v399 e o esboco R3.5 pinado sao so' lidos" % RM["bloco_embutido_sha256"][:16]],
    "metodo": "o runtime novo MONTADO por script do runtime da v399 (%d edicoes de texto declaradas, cada uma com contagem exata; conferencias C1, C2, C3, C9, C3', C10 e C11 ok; bloco do operador intocado); candidato DERIVADO por script da v399 selada (%d patches; comparacao AST: %d nos iguais, %d mudados, %d removido, %d novos); "
              "guardas ESTATICAS da Bancada (a FUNCAO ler_nos do esboco R3.5 pinado) sobre o candidato -- a v399 selada REPRODUZ a recusa do recibo da Bancada e 9 controles negativos recusam --; ensaio a seco completo (kernel embutido == sandbox, exame dos pontos de chamada, simulacao da arvore do Nos, artigo PT/EN com pdflatex, .md, sidecar, quadro do topo); "
              "o encanamento (instalar, reverter, rito, conferidor, ESPERADOS, citacoes, pos-rito, servico da Bancada) DERIVADO da v399 por motor com contagem exata por regra, nada executado" % (len(RM["edicoes_declaradas"]), CM["n_patches"], CMP["iguais"], len(CMP["mudados"]), len(CMP["removidos"]), CMP["n_novos"]),
    "resultado": "selo_pela_propria_tecnologia_v399 (%d checagens, %d controles negativos recusados) e declaracao_do_operador_v399 (%d checagens) selam no ensaio | alfa: %d linha col0 (linha %d), %d indentadas; versao: %d linha | guardas estaticas da Bancada: candidato PASSA, v399 recusada com a mesma mensagem do recibo (%s) | "
                 "kernel: nenhum modulo novo, escada %d/%d | sidecar: %d objetos verificados | ensaio %s | conferidor: caminho positivo tudo_bate=%s (emulacao), controle negativo tudo_bate=%s | harness do pos_rito: textos tudo_passou=%s, fechar tudo_passou=%s | servico da Bancada: %d/%d condicoes estaticas | "
                 "pre_selo %s (%d PASSA, %d FALHA; o recibo da cadeia v399, reconferido pelo esboco) | B(n): %s" % (
        len(sar["checks"]), len(sar["controles"]), len(dcr["checks"]), co["candidato_v400"]["alfa_col0"], co["linha_do_alfa"], co["candidato_v400"]["alfa_indentada"], co["candidato_v400"]["versao_col0"], GU["v399_selada_o_defeito_real"]["recusa"], esc[1], esc[1],
        sum(1 for v in sc["verificacao"].values() if v is True), ENS["veredito"], str(POSIT["tudo_bate"]).lower(), str(NEG["tudo_bate"]).lower(), str(HT["tudo_passou"]).lower(), str(HF["tudo_passou"]).lower(), SERV["n_condicoes_ok"], SERV["n_condicoes"],
        PIN["veredito"], PIN["contagens"]["passa"], PIN["contagens"]["falha"], SAL["veredito"]),
    "veredito": "selo_pela_propria_tecnologia_v399: %s | declaracao_do_operador_v399: %s | %s" % (sar["verdict"], dcr["verdict"], GU["veredito"]),
    "defeito": "o rito real NAO rodou; instalar, rito e reverter (derivados), o pos_rito, os scripts de servico, o gerador, o runtime MONTADO e os textos GERADOS sem revisao independente (quem construiu nao aprova) [DECLARADO]; o salto declarado do R3.4 pelo elo da v399 foi MEDIDO impossivel com o esboco R3.5 (o esboco recusa o elo por alfa nao unico, e o diff do kernel "
               "entre a v399 e a v400 e vazio, o que o T17 recusaria): o B(n) preparado e' o passo SIMPLES v398 -> v400, nao um salto declarado; o recibo pre_selo e' o da cadeia v399 (sobre o um.py v398 que a Bancada pina), reconferido e nao regerado: um novo pre_selo exigiria o Nos na versao que a Bancada pina; "
               "o ensaio restaura ao valor da v399 selada o instantaneo de contagens de three_stress_tests_v387 (o rito o computa no ponto do main; so' as contagens diferem no ensaio); a Dobra pura nao e' exata em R e o rint ao reticulado inteiro NAO e' da patente; o SHA-256 segue a primitiva de integridade; [LEGAL] publicar o bloco embutido e' decisao do operador com a agente de PI",
    "nao_refazer": "a correcao, a comparacao AST, as guardas estaticas da Bancada e o ensaio estao medidos para o candidato %s; refazer so' se o runtime, os textos, o artigo ou o kernel mudarem (sh refazer_candidato_v400.sh); o salto do R3.4 pelo elo da v399 nao se refaz: esta medido impossivel (salto_r3_4\\SALTO_R3_4_MEDIDO_v400.json)" % S16,
    "proximo_passo": "revisao independente do gerador, do runtime montado, dos derivados e dos textos gerados; so' depois instalar e rodar o rito (ato da gerencia, com o recibo pre_selo pinado: %s e a Bancada ainda pinando %s); pos-rito; B(n) passo simples v398 -> v400 (parada e religamento do servico sao ato do operador); custodia CONJUNTA v399 + v400 pela sessao do site" % (PIN["path"].split(os.sep)[-1], bn_atual),
    "onde": "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v400",
    "artefatos": art_prep,
    "refs": refs,
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 24/10/2026. Consultas ao mapa antes: v400, alpha linha unica e salto -> nenhuma rota; a rota da cadeia v399 (%s), a do B(n) (%s) e as tres rotas de estudo da v399 existiam. Validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move." % (ROTA_V399, ROTA_BANC)}
rec_v399 = {
    "tipo": "ANOTACAO", "rota_id": ROTA_V399, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "A v399 foi RECUSADA pela Bancada Um no ensaio do B(n) (ALPHA_LINHA_NAO_UNICA): a v400 a corrige (preparada, nao instalada)",
    "resultado": "a Bancada recusou a v399 (%s) por %s; a v400 (candidato %s) a corrige sem modulo novo: o alfa tem uma so' linha (a de numero %d) e a checagem do beta do registro do selo ACOM confronta o core; a v399 nunca foi sincronizada com a Bancada, que segue pinando %s; a custodia da v399 e da v400 sera conjunta" % (
        GU["v399_selada_o_defeito_real"]["recusa"], "duas linhas de alfa na coluna 0 (a do programa e a que a secao do selo ACOM embutida redeclarava)", S16, co["linha_do_alfa"], bn_atual),
    "artefatos": [P("ESTADO_V400.md"), P("GUARDAS_ESTATICAS_BANCADA_v400.json"), P("COMPARACAO_V399_v400.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 24/10/2026. O bloco do operador embutido nao mudou: o alfa redeclarado estava na adaptacao da gerencia. Validade no kernel nao e' creditacao; o gate nao se move."}
rec_banc = {
    "tipo": "ANOTACAO", "rota_id": ROTA_BANC, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "B(n) da v400: o salto declarado do R3.4 pelo elo da v399 foi MEDIDO impossivel; o passo preparado e' simples v398 -> v400, com o recibo pre_selo da cadeia v399 reconferido",
    "resultado": "esboco R3.5: %s; a cadeia de selos v398 -> v399 e recusada (%s); o ler_nos sobre a v399 selada recusa com a mesma mensagem do recibo da Bancada; o diff do kernel entre a v399 e a v400 e vazio (o T17 recusaria `pedras vazias` num B(n) cujo ANTES fosse a v399); no passo simples v398 -> v400 o diff e' a pedra Testemunho; "
                 "o recibo pre_selo (%s; esboco: %d condicoes e %d controles) e utilizavel; a Bancada de producao segue pinando %s" % (
        SAL["veredito"], SAL["cadeia_v398_v399"]["recusa"][:60], PIN["veredito"], int(str(SAL["passo_simples_v398_v400"]["condicoes"]).split("/")[0]), int(str(SAL["passo_simples_v398_v400"]["controles"]).split("/")[0]), bn_atual),
    "artefatos": [P("salto_r3_4", "SALTO_R3_4_MEDIDO_v400.json"), P("PINO_RECIBO_PRE_SELO_v400.json"), P("PINOS_BN_v400.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 24/10/2026. T17 lido do codigo do esboco, nao executado (precisa do selo e do manifesto reais). A producao foi so' lida."}
rec_selo = {
    "tipo": "ANOTACAO", "rota_id": ROTA_SELO, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "O selo pela propria tecnologia: a v400 corrige a adaptacao em volta do bloco (alfa unico; beta conferido contra o core), preparada e nao instalada",
    "resultado": "candidato %s: o runtime foi MONTADO do runtime da v399 com %d edicoes de texto declaradas; o hash do bloco do operador (%s) NAO mudou; o registro com FUNCAO selo_pela_propria_tecnologia_v399 sela no ensaio (%d checagens, a do beta agora contra o core; %d controles negativos recusados); testes de unidade novos: o alfa do programa adulterado e' pego pela checagem do beta" % (
        S16, len(RM["edicoes_declaradas"]), RM["bloco_embutido_sha256"][:16], len(sar["checks"]), len(sar["controles"])),
    "artefatos": [P("ESTADO_V400.md"), P("runtime_v400.py"), P("RUNTIME_MONTAGEM_v400.json"), P("ensaio_a_seco_v400.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 24/10/2026. O SHA-256 segue a primitiva de integridade; nenhuma alegacao de confidencialidade; [LEGAL] publicar o bloco embutido e' decisao do operador com a agente de PI (D2). Validade no kernel nao e' creditacao; o gate nao se move."}
reg = [rec_rota] + [r for r in (rec_v399, rec_banc, rec_selo) if r["rota_id"] in ids]
for r in reg:   # anotacao em rota que nao existe: o mapa recusa; aqui o gerador recusa antes
    if r["tipo"] == "ANOTACAO":
        assert r["rota_id"] in ids, ("a rota a anotar nao existe no livro", r["rota_id"])
assert len(reg) == 4, ("esperava a rota nova e as tres anotacoes", [r["rota_id"] for r in reg])
campos_modelo = set(rotas.MODELO)
saida = []
for r in reg:
    extras = sorted(set(r) - campos_modelo)
    assert not extras, ("campos fora do modelo", r["rota_id"], extras)
    v = rotas._valida(r, set(ids), seqs)   # a MESMA validacao do mapa (levanta ValueError se algo estiver errado); nao registra
    saida.append({"rota_id": v["rota_id"], "tipo": v["tipo"], "artefatos_n": len(v.get("artefatos", [])), "titulo_chars": len(v.get("titulo", ""))})
p = os.path.join(HERE, "registro_mapa_v400_prep.json"); b = (json.dumps(reg, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
if os.path.exists(p):
    open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_c1", "wb").write(open(p, "rb").read())
open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("VALIDO (rotas._valida, sem registrar):", json.dumps(saida, ensure_ascii=False)); print("registro_mapa_v400_prep.json", len(b), "bytes; sha16", hashlib.sha256(b).hexdigest()[:16])
