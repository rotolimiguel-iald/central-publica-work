# -*- coding: utf-8 -*-
"""gerar_registro_mapa_prep_v397.py -- monta registro_mapa_v397_prep.json (LISTA de registros, SO' com campos de `rotas.py modelo`) a partir dos artefatos da cadeia (numeros e hashes LIDOS; nada digitado) e VALIDA cada
registro com a MESMA funcao que o mapa usa (rotas._valida), SEM registrar: importa rotas.py (so' constantes e funcoes), le rotas.jsonl para os ids e seqs existentes, nao escreve no livro. O registro no mapa e' ato da gerencia
(`rotas.py registrar <json> --quem ...`). Molde: gerar_registro_mapa_prep_v396.py. uso: python -I -B -X utf8 gerar_registro_mapa_prep_v397.py   (roda DEPOIS de gerar_estado_v397.py: o ESTADO entra como artefato com o sha256 final)"""
import hashlib, importlib.util, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v397 as DL  # noqa: E402
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
CM = J("CANDIDATO_v397.json"); ESP = J("ESPERADOS_v397.json"); ENS = J("ensaio_a_seco_v397.json"); PIN = J("PINO_RECIBO_PRE_SELO_v397.json"); FJ = J("kernel", "FLAGS_v397.json"); KH = J("kernel", "KH_N1_v397.json")
X = J("EXAME_PONTOS_%s.json" % CM["sha16"]); CMP = J("COMPARACAO_V396_v397.json")
P = lambda *p: os.path.join(HERE, *p)
S16 = CM["sha16"]; ev = ESP["veracidade"]; esc = CM["escada"]; nm_ = ev["numeros_do_resultado"]
ROTA_RESULTADO = "d1.fase9.v2_c1_a_unica_palavra_23out"   # a rota da ABERTURA (claude-c1, 23/10): o resultado e' dela; esta preparacao so' o LE por hash
ROTA_TESTEMUNHA = "umpy.v396.testemunha_estatica_na_fractalizacao_do_um"
art_prep = [P("ESTADO_V397.md"), P("CANDIDATO_v397.json"), P("ESPERADOS_v397.json"), P("ensaio_a_seco_v397.json"), P("kernel", "FLAGS_v397.json"), P("kernel", "KERNEL_RECIBO_v397.json"), P("kernel", "KH_N1_v397.json"), P("PINOS_BN_v397.json"),
            P("DIFF_KERNEL_v397.txt"), P("COMPARACAO_V396_v397.json"), P("conferencia_rito_v397_CONTROLE_NEGATIVO_PRE_RITO.json"), P("conferencia_rito_v397_POSITIVO_FALSO_NOS.json"), P("EXAME_PONTOS_%s.json" % S16), P("SIMULACAO_ARVORE_NOS_%s.json" % S16),
            P("insumos", "fase9", "RESULTADO_FASE9_V2_C1_20261023_122926.json"), P("pedra", "Token.lean")]
refs = [x for x in (ROTA_RESULTADO, ROTA_TESTEMUNHA, "kernel.testemunha_estatica_v396_candidata_22out", "infra.bancada_um.sincronizacao_vnnn") if x in ids]
rec_rota = {
    "tipo": "ROTA", "rota_id": "umpy.v397.token_e_veracidade_preparo", "dominio": "KERNEL_FORMAL", "status": "EM_CURSO", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "v397 PREPARADA (candidato %s): a pedra Token (1 modulo, %d bandeira; o nome e' do operador), o registro teste_de_veracidade_fase9_v397 (o resultado do Teste da Unica Palavra lido por hash, ao lado do V1; nenhum sigma novo), as quatro falas de 23/10 e o QUADRO no topo do artigo e do .md; escada %d -> %d; ensaio a seco %s; nada instalado, nada selado" % (S16, FJ["n_flags"], esc[0], esc[1], ENS["veredito"]),
    "pergunta": "o candidato v397 sela, no ensaio a seco, com a pedra TGLExt/Token no kernel (a conjuncao de psibit_is_the_mode_of_the_reader e the_psion_inhabits_the_static_witness), o resultado do Teste da Unica Palavra e os tres recibos lidos por sha256 no ponto do V1 (beta = alfa CODATA x sqrt(e) em runtime conferido contra o do resultado), as quatro falas do operador de 23/10 por sha256 e o quadro «O Teste da Unica Palavra» no topo do artigo PT/EN e do .md com os numeros == os do resultado pinado, sem mudar nenhum veredito da v396 fora da troca dita (so' numeros)?",
    "dados": ["nenhum dado novo: o registro LE o resultado ja' aberto UMA vez em 23/10 (rota %s) e os tres recibos; os numeros (z_disc calibrado %.4f, p unilateral %.3e, z_delta calibrado %.4f, p bilateral %.4f, poder previo %.4f, lnB(TGL/LCDM) %.4f, lnB(TGL/beta livre) %.4f, K %.6f) sao os do resultado; nenhum sigma, p ou lnB e' calculado" % (
        ROTA_RESULTADO, nm_["z_disc_calibrado"], nm_["p_disc_unilateral"], nm_["z_delta_calibrado"], nm_["p_delta_bilateral"], nm_["poder_previo"], nm_["lnB_lcdm"], nm_["lnB_beta_livre"], nm_["K"])],
    "metodo": "sandbox C:\\t\\k397c (copia de k396c + a pedra Token, raiz e Audit com o import), lake build incremental e Audit; candidato DERIVADO por script da v396 selada (%d patches; comparacao AST: nada perdido); o registro de veracidade e' SPEC (motor _v392_registro) chamado no ponto real do main logo depois do bloco do V1; ensaio a seco (verify real com os logs crus, vizinhos recomputados, fluxo principal, %d controles de unidade incluindo sha errado, recibo ausente e numero adulterado com sha repinado, selo, artigo PT/EN e o quadro no topo, simular_arvore_do_nos, exame_pontos); conferidor (controle negativo e caminho positivo emulado, com o quadro conferido contra o resultado pinado); recibo pre_selo do B(n) em modo ensaio, producao so' lida" % (len(CM["patches"]), len(ENS["unidade"])),
    "resultado": "%s | Audit %d constantes e %d teoremas, 0 fora do trio | escada %d/%d | %d checagens do registro de veracidade passam, as quatro fontes pinadas conferem | quadro no topo do artigo PT/EN e do .md: %s | ensaio %s | pre_selo %s (%d PASSA, %d FALHA)" % (
        ev["verdict"], KH["linha_TOTAL"]["decl"], KH["linha_TOTAL"]["thm"], esc[1], esc[1], ev["n_checks"], ENS["quadro"]["ok"], ENS["veredito"], PIN["veredito"], PIN["contagens"]["passa"], PIN["contagens"]["falha"]),
    "veredito": ev["verdict"],
    "defeito": "o rito real NAO rodou; instalar, rito e reverter (derivados), o pos_rito (subagente) e o codigo novo (registros_v397, runtime_quadro_v397, quadro_v397, ensaio) sem revisao independente; a pedra Token nao teve exame independente (compoe por citacao; compilou no sandbox); o build do sandbox e' incremental; o teste nao foi cego (centros publicos, dito no token do veredito); a discriminacao a 5 sigma (o degrau da creditacao) NAO foi alcancada (o z_disc calibrado e' menor que 5)",
    "nao_refazer": "a pedra, o registro e o ensaio estao medidos para o candidato %s; refazer so' se a pedra, o runtime, os textos ou o kernel mudarem (sh refazer_candidato_v397.sh --regerar; sh refazer_sandbox_v397.sh se o kernel mudar); a abertura do Teste da Unica Palavra esta CONSUMIDA (rota %s): nao reabrir" % (S16, ROTA_RESULTADO),
    "proximo_passo": "revisao independente do gerador, do registro, do quadro e dos derivados; decisoes da gerencia (patch dos registros anteriores incluindo o contrato da testemunha_estatica_v396, ponto de chamada ao lado do V1); o operador nomeia o registro de veracidade (nome provisorio) e decide se a pedra e o registro entram no um.py (ordem de 22/10: sem gordura); instalar e rodar o rito (ato da gerencia, depois do recibo pre_selo pinado); pos-rito; B(n) SEM SALTO (a parada do servico da Bancada e' ato do operador); README do espelho e site com o paragrafo pronto do handoff",
    "onde": "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v397",
    "artefatos": art_prep,
    "refs": refs,
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 23/10/2026. Consultas ao mapa antes: v397 -> a custodia da v396, o incremental da Central publica e a camada IA do acervo (outros assuntos); token -> rotas de tokens de modelo; fase9 -> a rota da abertura (%s). A discriminacao a 5 sigma e' o degrau da creditacao e nao foi alcancada; validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move." % ROTA_RESULTADO}
rec_banc = {
    "tipo": "ANOTACAO", "rota_id": "infra.bancada_um.sincronizacao_vnnn", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "Recibo pre_selo do B(n) da v397 (ensaio, producao so' lida): %s, pinado ANTES da instalacao" % PIN["veredito"],
    "resultado": "esboco R3.5, --versao v396 --fase pre_selo --modo ensaio; bateria %d PASSA, %d FALHA, %d NAO_EXECUTADO (T17 so' no pos_selo); utilizavel_como_recibo_pre_selo_do_B_n = %s; Bancada de producao (%d entradas) e Nos (%d) com listas iguais antes e depois; passo simples sem salto (pelo codigo do esboco os vereditos serao REPINADA_B7__...; lido, nao rodado); a Bancada pina %s" % (PIN["contagens"]["passa"], PIN["contagens"]["falha"], PIN["contagens"]["nao_executado"], str(PIN["utilizavel_como_recibo_pre_selo_do_B_n"]).lower(), PIN["escrita_na_producao"]["bancada_um"]["antes"], PIN["escrita_na_producao"]["nos"]["antes"], PIN["bancada_pina"]["deployment_id"]),
    "artefatos": [P("PINO_RECIBO_PRE_SELO_v397.json"), PIN["path"], P("PROVA_PRODUCAO_INTACTA_v397_pre_selo.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente do recibo pre_selo), 23/10/2026. Limites: T12/T13/T14 medidos contra o um.py v396; o recibo fica obsoleto se a producao for repinada antes do B(n); o servico esta no ar (a parada e' ato do operador)."}
rec_res = {
    "tipo": "ANOTACAO", "rota_id": ROTA_RESULTADO, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "O resultado do Teste da Unica Palavra passa a ser LIDO por hash pelo um.py v397 (registro teste_de_veracidade_fase9_v397, ao lado do V1), com o quadro no topo do artigo e do .md",
    "resultado": "candidato %s (preparado, nao instalado): o registro le o resultado (sha256 %s) e os tres recibos, confere a cadeia congelamento -> abertura -> consumida e o beta contra alfa CODATA x sqrt(e), e compoe a leitura binaria do operador sem calcular sigma novo; z_disc calibrado %.4f (p unilateral %.3e) abaixo de 5 sigma: o degrau da creditacao nao foi alcancado" % (S16, DL.F9_RESULTADO_SHA256_DA_ORDEM[:16], nm_["z_disc_calibrado"], nm_["p_disc_unilateral"]),
    "artefatos": [P("ESTADO_V397.md"), P("insumos", "fase9", "RESULTADO_FASE9_V2_C1_20261023_122926.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 23/10/2026. Nenhuma abertura nova: a abertura esta consumida. NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move."}
reg = [rec_rota, rec_banc] + ([rec_res] if ROTA_RESULTADO in ids else [])
campos_modelo = set(rotas.MODELO)
saida = []
for r in reg:
    extras = sorted(set(r) - campos_modelo)
    assert not extras, ("campos fora do modelo", r["rota_id"], extras)
    v = rotas._valida(r, set(ids), seqs)   # a MESMA validacao do mapa (levanta ValueError se algo estiver errado); nao registra
    saida.append({"rota_id": v["rota_id"], "tipo": v["tipo"], "artefatos_n": len(v.get("artefatos", [])), "titulo_chars": len(v.get("titulo", ""))})
p = os.path.join(HERE, "registro_mapa_v397_prep.json"); b = (json.dumps(reg, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("VALIDO (rotas._valida, sem registrar):", json.dumps(saida, ensure_ascii=False)); print("registro_mapa_v397_prep.json", len(b), "bytes; sha16", hashlib.sha256(b).hexdigest()[:16])
