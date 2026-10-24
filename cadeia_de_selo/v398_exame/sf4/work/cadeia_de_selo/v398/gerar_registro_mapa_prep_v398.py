# -*- coding: utf-8 -*-
"""gerar_registro_mapa_prep_v398.py -- monta registro_mapa_v398_prep.json (LISTA de registros, SO' com campos de `rotas.py modelo`) a partir dos artefatos da cadeia (numeros e hashes LIDOS; nada digitado) e VALIDA cada
registro com a MESMA funcao que o mapa usa (rotas._valida), SEM registrar: importa rotas.py (so' constantes e funcoes), le rotas.jsonl para os ids e seqs existentes, nao escreve no livro. O registro no mapa e' ato da gerencia
(`rotas.py registrar <json> --quem ...`). Molde: gerar_registro_mapa_prep_v397.py. uso: python -I -B -X utf8 gerar_registro_mapa_prep_v398.py   (roda DEPOIS de gerar_estado_v398.py: o ESTADO entra como artefato com o sha256 final)"""
import hashlib, importlib.util, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v398 as DL  # noqa: E402
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
CM = J("CANDIDATO_v398.json"); ESP = J("ESPERADOS_v398.json"); ENS = J("ensaio_a_seco_v398.json"); PIN = J("PINO_RECIBO_PRE_SELO_v398.json"); FJ = J("kernel", "FLAGS_v398.json"); KH = J("kernel", "KH_N1_v398.json")
HT = J("pos_rito", "HARNESS_TEXTOS_ENSAIO_v398.json"); HF = J("pos_rito", "HARNESS_FECHAR_SANDBOX_v398.json")
CMP = J("COMPARACAO_V397_v398.json")
P = lambda *p: os.path.join(HERE, *p)
S16 = CM["sha16"]; esc = CM["escada"]; sr = ENS["sonico_registro"]; ar_ = ENS["afinacao_registro"]; tot = KH["linha_TOTAL"]
S1, S2 = DL.STONES; P1, P2 = CM["kernel"]["pedras"][S1["rel"]], CM["kernel"]["pedras"][S2["rel"]]
ROTA_SON = "kernel.sonico_v398_candidata_23out"; ROTA_AFI = "kernel.afinacao_das_cordas_v398_candidata_23out"; ROTA_BANC = "infra.bancada_um.sincronizacao_vnnn"
ROTA_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"; ROTA_TESTEMUNHA = "umpy.v396.testemunha_estatica_na_fractalizacao_do_um"
art_prep = [P("ESTADO_V398.md"), P("CANDIDATO_v398.json"), P("ESPERADOS_v398.json"), P("ensaio_a_seco_v398.json"), P("kernel", "FLAGS_v398.json"), P("kernel", "KERNEL_RECIBO_v398.json"), P("kernel", "KH_N1_v398.json"), P("PINOS_BN_v398.json"),
            P("DIFF_KERNEL_v398.txt"), P("COMPARACAO_V397_v398.json"), P("conferencia_rito_v398_CONTROLE_NEGATIVO_PRE_RITO.json"), P("conferencia_rito_v398_POSITIVO_FALSO_NOS.json"), P("EXAME_PONTOS_%s.json" % S16), P("SIMULACAO_ARVORE_NOS_%s.json" % S16),
            P("refazer_out_v398.txt"), P("pedra", "Sonico.lean"), P("pedra", "AfinacaoDasCordas.lean")]
refs = [x for x in (ROTA_SON, ROTA_AFI, ROTA_BANC, ROTA_QUADRO, ROTA_TESTEMUNHA) if x in ids]
rec_rota = {
    "tipo": "ROTA", "rota_id": "umpy.v398.sonico_e_afinacao_preparo", "dominio": "KERNEL_FORMAL", "status": "EM_CURSO", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "v398 PREPARADA (candidato %s): as pedras Sonico e AfinacaoDasCordas (%d modulos, %d bandeiras), os registros com funcao sonico_v398 e afinacao_das_cordas_v398 na fractalizacao do Um, as seis inscricoes de 23/10 e a secao do artigo; escada %d -> %d; ensaio a seco %s; nada instalado, nada selado" % (S16, CM["kernel"]["modulos_novos"], FJ["n_flags"], esc[0], esc[1], ENS["veredito"]),
    "pergunta": "o candidato v398 sela, no ensaio a seco, com as pedras TGLExt/Sonico e TGLExt/AfinacaoDasCordas no kernel (cada composicao incondicional lida no kernel do proprio rito), os dois registros com funcao no ponto da fractalizacao do Um (logo depois da testemunha estatica), as seis inscricoes de 23/10 por sha256 e a secao do artigo, sem mudar nenhum veredito da v397 fora da troca dita (so' numeros) e sem mexer no quadro do Teste da Unica Palavra?",
    "dados": ["nenhum dado novo e nenhum rito: as pedras citam termos que o kernel ja' tem; os registros recalculam aritmetica (ln 2, e^(ln 2) = 2 e a entropia do colapso em theta_M com beta = alfa CODATA 2018 x sqrt(e) calculado no rito; a torre n kappa com kappa de teste; zeta(-1) = -1/12 e zeta(-1, 1/2) = 1/24 por numeros de Bernoulli)"],
    "metodo": "sandbox C:\\t\\k398c (copia de k398b, que ja' tem as duas pedras compiladas isoladamente; raiz e Audit regerados com os imports), lake build e Audit; candidato DERIVADO por script da v397 selada (%d patches; comparacao AST: nada perdido); os dois registros sao FUNCOES (padrao da testemunha_estatica_v396) chamadas no ponto real do main (o sonico logo depois da testemunha estatica, a afinacao logo depois do sonico); ensaio a seco (verify real com os logs crus, vizinhos recomputados, fluxo principal, %d controles de unidade, selo, artigo PT/EN com o quadro no topo, simular_arvore_do_nos, exame_pontos); conferidor (controle negativo e caminho positivo emulado); recibo pre_selo do B(n) em modo ensaio, producao so' lida; harness do pos_rito sem a flag de ensaio" % (len(CM["patches"]), len(ENS["unidade"])),
    "resultado": "sonico_v398 (%d checagens) e afinacao_das_cordas_v398 (%d) selam no ensaio | Audit %d constantes e %d teoremas, %d fora do trio | escada %d/%d | %d bandeiras (%d + %d) | ensaio %s | harness do pos_rito: textos tudo_passou=%s, fechar tudo_passou=%s | pre_selo %s (%d PASSA, %d FALHA) | comparacao com a v397: %d iguais, %d mudados, %d removidos, %d novos" % (
        sr["n_checks"], ar_["n_checks"], tot["decl"], tot["thm"], tot["fora_do_trio"], esc[1], esc[1], FJ["n_flags"], FJ["por_grupo_bandeiras"]["sonico"], FJ["por_grupo_bandeiras"]["afinacao"], ENS["veredito"], str(HT["tudo_passou"]).lower(), str(HF["tudo_passou"]).lower(),
        PIN["veredito"], PIN["contagens"]["passa"], PIN["contagens"]["falha"], CMP["iguais"], len(CMP["mudados"]), len(CMP["removidos"]), CMP["n_novos"]),
    "veredito": "sonico_v398: %s | afinacao_das_cordas_v398: %s" % (sr["verdict"], ar_["verdict"]),
    "defeito": "o rito real NAO rodou; instalar, rito e reverter (derivados), o pos_rito, os scripts de servico e o codigo novo (registros_v398, runtime_pedras_v398, ensaio) sem revisao independente; as duas pedras tiveram revisao independente [DECLARADO: pelo mapa, nao refeita aqui]; o kappa do boost nao esta no core (a afinacao confere a forma da torre com kappa de teste); MasslessFirstLevel e' hipotese nomeada [KNOWN], a geometria das cordas segue [OPEN] e o d = 9 da casa e' [DECLARADO]; a lei de custo do sonico e' [INPUT]; o build do sandbox e' incremental (as pedras entraram ja' compiladas)",
    "nao_refazer": "as pedras, os registros e o ensaio estao medidos para o candidato %s; refazer so' se a pedra, o runtime, os textos ou o kernel mudarem (sh refazer_candidato_v398.sh --regerar; sh refazer_sandbox_v398.sh se o kernel mudar); as pedras ja' estao registradas nas rotas %s e %s" % (S16, ROTA_SON, ROTA_AFI),
    "proximo_passo": "revisao independente do gerador, dos registros, do runtime novo e dos derivados; decisoes da gerencia (patch dos contratos dos registros anteriores, ponto de chamada, registros como funcao); o operador nomeia os dois registros (nomes provisorios) e decide se entram no um.py (ordem de 22/10: sem gordura); instalar e rodar o rito (ato da gerencia, com o recibo pre_selo pinado); pos-rito; B(n) SEM SALTO (a Bancada pina %s, logo B8; a parada do servico e' ato do operador); README do espelho e site com os dois paragrafos prontos do handoff" % PIN["bancada_pina"]["deployment_id"],
    "onde": "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v398",
    "artefatos": art_prep,
    "refs": refs,
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 23/10/2026. Consultas ao mapa antes: sonico e afinacao das cordas -> as duas rotas candidatas kernel.* (pedras compiladas, revisao independente PEDRA_APROVADA, ratificadas pelo operador); v398 -> so' essas duas, nenhuma rota de cadeia; sincronizacao_vnnn -> a rota da Bancada e as cadeias v395 e v396. Validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move."}
rec_banc = {
    "tipo": "ANOTACAO", "rota_id": ROTA_BANC, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "Recibo pre_selo do B(n) da v398 (ensaio, producao so' lida): %s, pinado ANTES da instalacao" % PIN["veredito"],
    "resultado": "esboco R3.5, --versao v397 --fase pre_selo --modo ensaio; bateria %d PASSA, %d FALHA, %d NAO_EXECUTADO (T17 so' no pos_selo); utilizavel_como_recibo_pre_selo_do_B_n = %s; Bancada de producao (%d entradas) e Nos (%d) com listas iguais antes e depois; passo simples sem salto (pelo codigo do esboco os vereditos serao REPINADA_B8__...; lido, nao rodado); a Bancada pina %s" % (PIN["contagens"]["passa"], PIN["contagens"]["falha"], PIN["contagens"]["nao_executado"], str(PIN["utilizavel_como_recibo_pre_selo_do_B_n"]).lower(), PIN["escrita_na_producao"]["bancada_um"]["antes"], PIN["escrita_na_producao"]["nos"]["antes"], PIN["bancada_pina"]["deployment_id"]),
    "artefatos": [P("PINO_RECIBO_PRE_SELO_v398.json"), PIN["path"], P("PROVA_PRODUCAO_INTACTA_v398_pre_selo.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente do recibo pre_selo), 23/10/2026. Limites: T12/T13/T14 medidos contra o um.py v397; o recibo fica obsoleto se a producao for repinada antes do B(n); o servico esta no ar (a parada e' ato do operador)."}
rec_son = {
    "tipo": "ANOTACAO", "rota_id": ROTA_SON, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "A pedra Sonico e' integrada no candidato v398 (preparado, nao instalado), com o registro com funcao sonico_v398 lido na fractalizacao do Um",
    "resultado": "candidato %s: TGLExt/Sonico.lean (sha16 %s) no kernel embutido; %d bandeiras ext_son398_NNNN, a da composicao incondicional %s; o registro sonico_v398 sela no ensaio (%d checagens: composicao e termos no kernel do rito, axiomas no trio, ln 2, e^(ln 2) = 2, aditividade, idempotencia do seletor, entropia do colapso em theta_M como numero derivado do rito); a lei de custo segue [INPUT]" % (S16, P1["sha16"], FJ["por_grupo_bandeiras"]["sonico"], FJ["bandeira_do_teorema_incondicional"]["sonico"], sr["n_checks"]),
    "artefatos": [P("ESTADO_V398.md"), P("pedra", "Sonico.lean"), P("ensaio_a_seco_v398.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 23/10/2026. Nenhum dado novo. Validade no kernel nao e' creditacao; o gate nao se move."}
rec_afi = {
    "tipo": "ANOTACAO", "rota_id": ROTA_AFI, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "A pedra AfinacaoDasCordas e' integrada no candidato v398 (preparado, nao instalado), com o registro com funcao afinacao_das_cordas_v398 lido na fractalizacao do Um",
    "resultado": "candidato %s: TGLExt/AfinacaoDasCordas.lean (sha16 %s) no kernel embutido; %d bandeiras ext_afi398_NNNN (%d auxiliares do compilador fora), a da composicao incondicional %s; o registro afinacao_das_cordas_v398 sela no ensaio (%d checagens: composicao e termos no kernel do rito, axiomas no trio, torre n kappa com kappa de teste, zeta(-1) = %s e zeta(-1, 1/2) = %s por Bernoulli, D = 26 e D = 10 sob a hipotese nomeada); MasslessFirstLevel segue [KNOWN], a geometria [OPEN]" % (S16, P2["sha16"], FJ["por_grupo_bandeiras"]["afinacao"], FJ["excluidas_auxiliares"]["n"], FJ["bandeira_do_teorema_incondicional"]["afinacao"], ar_["n_checks"], ar_["values"]["zeta_minus_one"], ar_["values"]["hurwitz_zeta_minus_one_half"]),
    "artefatos": [P("ESTADO_V398.md"), P("pedra", "AfinacaoDasCordas.lean"), P("ensaio_a_seco_v398.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 23/10/2026. Nenhum dado novo. Nada aqui deriva a teoria das cordas do axioma. Validade no kernel nao e' creditacao; o gate nao se move."}
rec_quadro = {
    "tipo": "ANOTACAO", "rota_id": ROTA_QUADRO, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "O quadro do Teste da Unica Palavra segue INTOCADO no topo do artigo PT/EN e do .md no candidato v398",
    "resultado": "candidato %s (preparado, nao instalado): runtime_quadro_v397 e quadro_v397 copiados sem mudanca (so' o import do delta); o conferidor e o harness do pos_rito conferem de novo o quadro contra o resultado pinado (sha256 %s) e a regra da ordem (o numero do z_disc nunca sem o p calibrado e sem a linha dos 5 sigma); o registro teste_de_veracidade_fase9_v397 segue selando (%d checagens)" % (S16, ESP["veracidade"]["resultado"]["sha256"][:16], ENS["mainflow"]["veracidade_n_checks"]),
    "artefatos": [P("ESTADO_V398.md"), P("ensaio_a_seco_v398.json"), P("conferencia_rito_v398_POSITIVO_FALSO_NOS.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 23/10/2026. Nenhuma abertura nova. NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move."}
reg = [rec_rota, rec_banc, rec_son, rec_afi] + ([rec_quadro] if ROTA_QUADRO in ids else [])
for r in reg:   # anotacao em rota que nao existe: o mapa recusa; aqui o gerador recusa antes
    if r["tipo"] == "ANOTACAO":
        assert r["rota_id"] in ids, ("a rota a anotar nao existe no livro", r["rota_id"])
campos_modelo = set(rotas.MODELO)
saida = []
for r in reg:
    extras = sorted(set(r) - campos_modelo)
    assert not extras, ("campos fora do modelo", r["rota_id"], extras)
    v = rotas._valida(r, set(ids), seqs)   # a MESMA validacao do mapa (levanta ValueError se algo estiver errado); nao registra
    saida.append({"rota_id": v["rota_id"], "tipo": v["tipo"], "artefatos_n": len(v.get("artefatos", [])), "titulo_chars": len(v.get("titulo", ""))})
p = os.path.join(HERE, "registro_mapa_v398_prep.json"); b = (json.dumps(reg, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
if os.path.exists(p):
    open(p + ".bak_" + __import__("time").strftime("%Y%m%d_%H%M%S") + "_c1", "wb").write(open(p, "rb").read())
open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("VALIDO (rotas._valida, sem registrar):", json.dumps(saida, ensure_ascii=False)); print("registro_mapa_v398_prep.json", len(b), "bytes; sha16", hashlib.sha256(b).hexdigest()[:16])
