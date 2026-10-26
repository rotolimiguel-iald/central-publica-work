# -*- coding: utf-8 -*-
"""gerar_registro_mapa_prep_v399.py -- monta registro_mapa_v399_prep.json (LISTA de registros, SO' com campos de `rotas.py modelo`) a partir dos artefatos da cadeia (numeros e hashes LIDOS; nada digitado) e VALIDA cada
registro com a MESMA funcao que o mapa usa (rotas._valida), SEM registrar: importa rotas.py (so' constantes e funcoes), le rotas.jsonl para os ids e seqs existentes, nao escreve no livro. O registro no mapa e' ato da gerencia
(`rotas.py registrar <json> --quem ...`). ESCRITO A MAO na v399 (a subida mecanica do gerador da v398 nao serve: a v399 tem UMA pedra, dois registros com funcao outros e o sidecar). Molde: gerar_registro_mapa_prep_v398.py.
uso: python -I -B -X utf8 gerar_registro_mapa_prep_v399.py   (roda DEPOIS de gerar_estado_v399.py: o ESTADO entra como artefato com o sha256 final)"""
import hashlib, importlib.util, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v399 as DL  # noqa: E402
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
CM = J("CANDIDATO_v399.json"); ESP = J("ESPERADOS_v399.json"); ENS = J("ensaio_a_seco_v399.json"); PIN = J("PINO_RECIBO_PRE_SELO_v399.json"); FJ = J("kernel", "FLAGS_v399.json"); KH = J("kernel", "KH_N1_v399.json")
HT = J("pos_rito", "HARNESS_TEXTOS_ENSAIO_v399.json"); HF = J("pos_rito", "HARNESS_FECHAR_SANDBOX_v399.json"); RM = J("RUNTIME_MONTAGEM_v399.json"); SERV = J("bancada_B3_servico", "DERIVACAO_SERVICO_v399.json")
CMP = J("COMPARACAO_V398_v399.json"); POSIT = J("conferencia_rito_v399_POSITIVO_FALSO_NOS.json"); NEG = J("conferencia_rito_v399_CONTROLE_NEGATIVO_PRE_RITO.json")
P = lambda *p: os.path.join(HERE, *p)
S16 = CM["sha16"]; esc = CM["escada"]; tot = KH["linha_TOTAL"]
S1 = DL.STONES[0]; P1 = CM["kernel"]["pedras"][S1["rel"]]
sar = ENS["selo_acom_registro"]; dcr = ENS["declaracao_registro"]; sc = ENS["sidecar"]
bn_atual = PIN["bancada_pina"]["deployment_id"]
v_banc = SERV["expectativa_do_B_n_da_v399"]["veredito_esperado_do_aplicar_da_v399"]
ROTA_NOVA = "umpy.v399.cadeia_de_selo_preparada_24out"
ROTA_TMN = "kernel.testemunho_v399_candidata_24out"; ROTA_SELO = "umpy.v399.selo_pela_propria_tecnologia_estudo_24out"; ROTA_DECL = "umpy.v399.declaracao_do_operador_operacao_quadratica_24out"
ROTA_BANC = "infra.bancada_um.sincronizacao_vnnn"; ROTA_V398 = "umpy.v398.sonico_e_afinacao_das_cordas_na_fractalizacao_do_um"; ROTA_CUST = "custodia.v398"
assert ROTA_NOVA not in ids, "a rota da cadeia v399 ja' existe no livro: acrescente RESULTADO/ANOTACAO em vez de ROTA"
art_prep = [P("ESTADO_V399.md"), P("CANDIDATO_v399.json"), P("ESPERADOS_v399.json"), P("ensaio_a_seco_v399.json"), P("kernel", "FLAGS_v399.json"), P("kernel", "KERNEL_RECIBO_v399.json"), P("kernel", "KH_N1_v399.json"), P("PINOS_BN_v399.json"),
            P("DIFF_KERNEL_v399.txt"), P("COMPARACAO_V398_v399.json"), P("RUNTIME_MONTAGEM_v399.json"), P("conferencia_rito_v399_CONTROLE_NEGATIVO_PRE_RITO.json"), P("conferencia_rito_v399_POSITIVO_FALSO_NOS.json"),
            P("EXAME_PONTOS_%s.json" % S16), P("SIMULACAO_ARVORE_NOS_%s.json" % S16), P("refazer_out_v399.txt"), P("pedra", "Testemunho.lean")]
refs = [x for x in (ROTA_TMN, ROTA_SELO, ROTA_DECL, ROTA_BANC, ROTA_V398, ROTA_CUST) if x in ids]
rec_rota = {
    "tipo": "ROTA", "rota_id": ROTA_NOVA, "dominio": "KERNEL_FORMAL", "status": "EM_CURSO", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "v399 PREPARADA (candidato %s): a pedra Testemunho (1 modulo, %d bandeiras), o selo pela propria tecnologia (ACOM Mirror Crypto embutido, perfil %s) e a declaracao do operador como registros com funcao, o sidecar, as quatro inscricoes de 24/10 e a secao do artigo; escada %d -> %d; ensaio a seco %s; nada instalado, nada selado; a instalacao aguarda a decisao [LEGAL] do operador" % (S16, FJ["n_flags"], sar["perfil"], esc[0], esc[1], ENS["veredito"]),
    "pergunta": "o candidato v399 sela, no ensaio a seco, com a pedra TGLExt/Testemunho no kernel (a composicao incondicional lida no kernel do proprio rito), o selo pela propria tecnologia (a segunda testemunha ao lado do SHA-256: reconstrucao exata do um.py, os 13 controles negativos recusados) e a declaracao do operador (a inscricao fundante por sha256), mais o sidecar um_absoluto_selo_acom.json e as quatro inscricoes de 24/10, sem mudar nenhum veredito da v398 fora da troca dita (so' numeros) e sem mexer no quadro do Teste da Unica Palavra?",
    "dados": ["nenhum dado novo e nenhum rito: a pedra cita termos que o kernel ja' tem; o selo reconstroi o proprio um.py a partir de tres partes (Psi, Theta, kappa); a declaracao do operador e' [DECLARACAO DO OPERADOR / INPUT]"],
    "metodo": "sandbox C:\\t\\k399c (copia de C:\\t\\k399, que ja' tem a pedra compilada isoladamente; raiz e Audit regerados com o import), lake build incremental e Audit; candidato DERIVADO por script da v398 selada (%d patches; comparacao AST: nada perdido); o runtime novo MONTADO por script dos insumos aprovados do estudo (%d edicoes de texto declaradas, cada uma com contagem exata; conferencias C1, C2, C3 e C9 do bloco embutido contra as seis fontes do operador); os dois registros sao FUNCOES chamadas no ponto real do main (logo depois da afinacao das cordas); ensaio a seco (verify real com os logs crus, vizinhos recomputados, fluxo principal, %d controles de unidade, selo, sidecar, artigo PT/EN com o quadro no topo, simular_arvore_do_nos, exame_pontos); conferidor com os 14 itens C1-C14 e o round trip byte a byte (controle negativo e caminho positivo emulado); recibo pre_selo do B(n) em modo ensaio, producao so' lida; harness do pos_rito sem a flag de ensaio" % (len(CM["patches"]), len(RM["edicoes_declaradas"]), len(ENS["unidade"])),
    "resultado": "selo_pela_propria_tecnologia_v399 (%d checagens, %d controles negativos recusados) e declaracao_do_operador_v399 (%d checagens) selam no ensaio | pedra Testemunho: %d bandeiras (a da composicao incondicional %s) | Audit %d constantes e %d teoremas, %d fora do trio | escada %d/%d | sidecar: %d objetos verificados | ensaio %s | conferidor: caminho positivo tudo_bate=%s (emulacao), controle negativo tudo_bate=%s | harness do pos_rito: textos tudo_passou=%s, fechar tudo_passou=%s | pre_selo %s (%d PASSA, %d FALHA) | comparacao com a v398: %d iguais, %d mudados, %d removidos, %d novos" % (
        len(sar["checks"]), len(sar["controles"]), len(dcr["checks"]), FJ["n_flags"], FJ["bandeira_do_teorema_incondicional"]["testemunho"], tot["decl"], tot["thm"], tot["fora_do_trio"], esc[1], esc[1], sum(1 for v in sc["verificacao"].values() if v is True), ENS["veredito"],
        str(POSIT["tudo_bate"]).lower(), str(NEG["tudo_bate"]).lower(), str(HT["tudo_passou"]).lower(), str(HF["tudo_passou"]).lower(), PIN["veredito"], PIN["contagens"]["passa"], PIN["contagens"]["falha"], CMP["iguais"], len(CMP["mudados"]), len(CMP["removidos"]), CMP["n_novos"]),
    "veredito": "selo_pela_propria_tecnologia_v399: %s | declaracao_do_operador_v399: %s" % (sar["verdict"], dcr["verdict"]),
    "defeito": "o rito real NAO rodou; instalar, rito e reverter (derivados), o pos_rito, os scripts de servico, o gerador, os registros e o runtime MONTADO sem revisao independente (o codigo do estudo teve exame independente [DECLARADO: EXAME_ESTUDO_V399.md, nao refeito aqui]; as edicoes de montagem nao); a Dobra pura nao e' exata em R (erro maximo %.4f): a exatidao exige o rint ao reticulado inteiro, que NAO e' da patente; o SHA-256 segue a primitiva de integridade e a segunda testemunha nao e' independente em forca criptografica; confidencialidade nao e' atestada; [LEGAL] embutir publica a implementacao (D2: decisao do operador com a agente de PI); a declaracao e' [INPUT] (o kernel nao a prova) e a leitura das duas faces e' [ONTO] da gerencia (D7); o build do sandbox e' incremental" % sar["erro_dobra_pura_recalculado_aqui"],
    "nao_refazer": "a pedra, os registros, o sidecar e o ensaio estao medidos para o candidato %s; refazer so' se a pedra, o runtime, os textos ou o kernel mudarem (sh refazer_candidato_v399.sh --regerar; sh refazer_sandbox_v399.sh se o kernel mudar); as tres rotas de estudo ja' estao no livro: %s, %s e %s" % (S16, ROTA_TMN, ROTA_SELO, ROTA_DECL),
    "proximo_passo": "decisao [LEGAL] do operador com a agente de PI (D2) e as demais D1 a D7; revisao independente do gerador, do runtime montado, dos registros e dos derivados; so' depois instalar e rodar o rito (ato da gerencia, com o recibo pre_selo pinado); pos-rito; B(n) SEM SALTO (a Bancada pina %s, logo o passo simples seguinte; a parada do servico e' ato do operador); README do espelho e site com os dois paragrafos prontos do handoff" % bn_atual,
    "onde": "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v399",
    "artefatos": art_prep,
    "refs": refs,
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 24/10/2026. Consultas ao mapa antes: v399, selo acom e testemunho -> as tres rotas de estudo (%s, %s e %s) e a %s; nenhuma rota de cadeia v399 existia. Validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move." % (ROTA_TMN, ROTA_SELO, ROTA_DECL, ROTA_CUST)}
rec_banc = {
    "tipo": "ANOTACAO", "rota_id": ROTA_BANC, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "Recibo pre_selo do B(n) da v399 (ensaio, producao so' lida): %s, pinado ANTES da instalacao" % PIN["veredito"],
    "resultado": "esboco R3.5, --versao v398 --fase pre_selo --modo ensaio; bateria %d PASSA, %d FALHA, %d NAO_EXECUTADO (T17 so' no pos_selo); utilizavel_como_recibo_pre_selo_do_B_n = %s; Bancada de producao (%d entradas) e Nos (%d) com listas iguais antes e depois; passo simples sem salto (pelo codigo do esboco o veredito do aplicar sera %s; lido, nao rodado); a Bancada pina %s" % (PIN["contagens"]["passa"], PIN["contagens"]["falha"], PIN["contagens"]["nao_executado"], str(PIN["utilizavel_como_recibo_pre_selo_do_B_n"]).lower(), PIN["escrita_na_producao"]["bancada_um"]["antes"], PIN["escrita_na_producao"]["nos"]["antes"], v_banc[:40], bn_atual),
    "artefatos": [P("PINO_RECIBO_PRE_SELO_v399.json"), PIN["path"], P("PROVA_PRODUCAO_INTACTA_v399_pre_selo.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente do recibo pre_selo), 24/10/2026. Limites: T12/T13/T14 medidos contra o um.py v398; o recibo fica obsoleto se a producao for repinada antes do B(n); o servico esta no ar (a parada e' ato do operador)."}
rec_tmn = {
    "tipo": "ANOTACAO", "rota_id": ROTA_TMN, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "A pedra Testemunho (nome provisorio) e' integrada no candidato v399 (preparado, nao instalado), com a composicao incondicional lida pelo registro da declaracao do operador",
    "resultado": "candidato %s: TGLExt/Testemunho.lean (sha16 %s) no kernel embutido; %d bandeiras ext_tmn399_NNNN, a da composicao incondicional %s; no sandbox a pedra entrou ja' compilada (Replayed) e o build recompilou a raiz e o Audit; %d declaracoes novas no Audit, axiomas no trio; o registro declaracao_do_operador_v399 le a pedra no kernel do rito (a ausencia recusa)" % (S16, P1["sha16"], FJ["n_flags"], FJ["bandeira_do_teorema_incondicional"]["testemunho"], FJ["decl_novas_dos_modulos"]),
    "artefatos": [P("ESTADO_V399.md"), P("pedra", "Testemunho.lean"), P("ensaio_a_seco_v399.json"), P("kernel", "FLAGS_v399.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 24/10/2026. Nenhum dado novo. A lei e' simetrica e a atribuicao dos papeis e' a declaracao do operador. Validade no kernel nao e' creditacao; o gate nao se move."}
rec_selo = {
    "tipo": "ANOTACAO", "rota_id": ROTA_SELO, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "O selo pela propria tecnologia e' integrado no candidato v399 (preparado, nao instalado): bloco ACOM embutido, registro com funcao, sidecar e conferidor C1-C14",
    "resultado": "candidato %s: runtime montado dos insumos aprovados do estudo (sha16 %s, %d edicoes de texto declaradas; conferencias C1, C2, C3 e C9 ok); o registro com FUNCAO selo_pela_propria_tecnologia_v399 sela no ensaio (%d checagens; perfil %s; %d controles negativos recusados; reconstrucao byte a byte; nenhuma parte isolada basta e Psi nao e' redundante); sidecar um_absoluto_selo_acom.json (%d objetos verificados; %d bytes no ensaio); o conferidor cobra C1 a C14 e o round trip do um.py instalado; decisoes da gerencia D3 (perfil C96/Q8; rint como adaptacao fora da patente), D4 (a recusa so' registra: AVISO, o SHA-256 segue soberano) e D5 (o sidecar entra na custodia)" % (
        S16, RM["runtime"]["sha256"][:16], len(RM["edicoes_declaradas"]), len(sar["checks"]), sar["perfil"], len(sar["controles"]), sum(1 for v in sc["verificacao"].values() if v is True), sc["bytes_do_sidecar"]),
    "artefatos": [P("ESTADO_V399.md"), P("runtime_v399.py"), P("RUNTIME_MONTAGEM_v399.json"), P("ensaio_a_seco_v399.json"), P("conferencia_rito_v399_POSITIVO_FALSO_NOS.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 24/10/2026. Nenhum dado novo. O SHA-256 segue a primitiva de integridade; nenhuma alegacao de confidencialidade; [LEGAL] publicar o bloco embutido e' decisao do operador com a agente de PI (D2). Validade no kernel nao e' creditacao; o gate nao se move."}
rec_decl = {
    "tipo": "ANOTACAO", "rota_id": ROTA_DECL, "estatuto": "INPUT", "olhou_dados": False,
    "titulo": "A declaracao do operador e' integrada no candidato v399 (preparado, nao instalado) com o estatuto [DECLARACAO DO OPERADOR / INPUT], ao lado da Tetelestai (v374) e da bancada (v86)",
    "resultado": "candidato %s: o registro com FUNCAO declaracao_do_operador_v399 sela no ensaio (%d checagens: a fala embutida == o arquivo do operador por sha256 %s; a trava EXECUTION_LOCKED_NOT_ONE no programa; %d ancoras do kernel no trio; a pedra Testemunho no kernel do rito); as quatro inscricoes de 24/10 embutidas por sha256 (cunhagens_v399), todas falas do operador; direcao: o operador testifica DA IALD, o um.py EM HASH, a IALD nao testifica do operador; o kernel nao prova a declaracao" % (
        S16, len(dcr["checks"]), dcr["verbatim_sha256"][:16], len(dcr["ancoras"])),
    "artefatos": [P("ESTADO_V399.md"), P("ensaio_a_seco_v399.json"), P("conferir_citacoes_v399.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 24/10/2026. Registrar nao e' provar. A leitura das duas faces e' [ONTO] da gerencia (D7), a ratificar pelo operador. O gate nao se move."}
reg = [rec_rota, rec_banc] + [r for r in (rec_tmn, rec_selo, rec_decl) if r["rota_id"] in ids]
for r in reg:   # anotacao em rota que nao existe: o mapa recusa; aqui o gerador recusa antes
    if r["tipo"] == "ANOTACAO":
        assert r["rota_id"] in ids, ("a rota a anotar nao existe no livro", r["rota_id"])
assert len(reg) == 5, ("esperava a rota nova e as quatro anotacoes", [r["rota_id"] for r in reg])
campos_modelo = set(rotas.MODELO)
saida = []
for r in reg:
    extras = sorted(set(r) - campos_modelo)
    assert not extras, ("campos fora do modelo", r["rota_id"], extras)
    v = rotas._valida(r, set(ids), seqs)   # a MESMA validacao do mapa (levanta ValueError se algo estiver errado); nao registra
    saida.append({"rota_id": v["rota_id"], "tipo": v["tipo"], "artefatos_n": len(v.get("artefatos", [])), "titulo_chars": len(v.get("titulo", ""))})
p = os.path.join(HERE, "registro_mapa_v399_prep.json"); b = (json.dumps(reg, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
if os.path.exists(p):
    open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_c1", "wb").write(open(p, "rb").read())
open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("VALIDO (rotas._valida, sem registrar):", json.dumps(saida, ensure_ascii=False)); print("registro_mapa_v399_prep.json", len(b), "bytes; sha16", hashlib.sha256(b).hexdigest()[:16])
