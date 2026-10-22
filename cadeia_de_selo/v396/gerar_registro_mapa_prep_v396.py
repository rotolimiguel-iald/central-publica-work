# -*- coding: utf-8 -*-
"""gerar_registro_mapa_prep_v396.py -- monta registro_mapa_v396_prep.json (LISTA de registros, SO' com campos de `rotas.py modelo`) a partir dos artefatos da cadeia (numeros e hashes LIDOS; nada digitado) e VALIDA cada
registro com a MESMA funcao que o mapa usa (rotas._valida), SEM registrar: importa rotas.py (so' constantes e funcoes), le rotas.jsonl para os ids e seqs existentes, nao escreve no livro. O registro no mapa e' ato da gerencia
(`rotas.py registrar <json> --quem ...`). Molde: gerar_registro_mapa_prep_v395.py. uso: python -I -B -X utf8 gerar_registro_mapa_prep_v396.py   (roda DEPOIS de gerar_estado_v396.py: o ESTADO entra como artefato com o sha256 final)"""
import hashlib, importlib.util, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v396 as DL  # noqa: E402
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
CM = J("CANDIDATO_v396.json"); ESP = J("ESPERADOS_v396.json"); ENS = J("ensaio_a_seco_v396.json"); PIN = J("PINO_RECIBO_PRE_SELO_v396.json"); FJ = J("kernel", "FLAGS_v396.json"); KH = J("kernel", "KH_N1_v396.json")
X = J("EXAME_PONTOS_%s.json" % CM["sha16"]); CMP = J("COMPARACAO_V395_v396.json")
P = lambda *p: os.path.join(HERE, *p)
S16 = CM["sha16"]; tv = ESP["testemunha"]; esc = CM["escada"]
ROTA_PEDRA = "kernel.testemunha_estatica_v396_candidata_22out"   # a ROTA que o construtor da pedra preparou (registro_mapa_testemunha_estatica.json); so' entra nas refs/anotacoes se JA estiver no livro
ROTA_PSIBIT = "kernel.psibit_v395_candidata_21out"
art_prep = [P("ESTADO_V396.md"), P("CANDIDATO_v396.json"), P("ESPERADOS_v396.json"), P("ensaio_a_seco_v396.json"), P("kernel", "FLAGS_v396.json"), P("kernel", "KERNEL_RECIBO_v396.json"), P("kernel", "KH_N1_v396.json"), P("PINOS_BN_v396.json"),
            P("DIFF_KERNEL_v396.txt"), P("COMPARACAO_V395_v396.json"), P("conferencia_rito_v396_CONTROLE_NEGATIVO_PRE_RITO.json"), P("conferencia_rito_v396_POSITIVO_FALSO_NOS.json"), P("EXAME_PONTOS_%s.json" % S16), P("SIMULACAO_ARVORE_NOS_%s.json" % S16)]
refs = [x for x in (ROTA_PEDRA, ROTA_PSIBIT, "umpy.v395.psibit_na_fractalizacao_do_um", "infra.bancada_um.sincronizacao_vnnn", "kernel.v385_axioma_e_testemunha_falsa") if x in ids or x == ROTA_PEDRA]
reat = FJ.get("reatribuidas_a_pedra") or {}
rec_rota = {
    "tipo": "ROTA", "rota_id": "umpy.v396.testemunha_estatica_preparo", "dominio": "KERNEL_FORMAL", "status": "EM_CURSO", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "v396 PREPARADA (candidato %s): a pedra TestemunhaEstatica (1 modulo, %d bandeiras), o registro testemunha_estatica_v396 chamado junto do psibit na fractalizacao do Um e as tres falas de 22/10; escada %d -> %d; ensaio a seco %s; nada instalado, nada selado" % (S16, FJ["n_flags"], esc[0], esc[1], ENS["veredito"]),
    "pergunta": "o candidato v396 sela, no ensaio a seco, com a pedra TGLExt/TestemunhaEstatica no kernel, a mecanica do canto do psion, da reducao a um sitio, do fluxo construido e do colapso calculada na fractalizacao do Um (beta = alfa CODATA x sqrt(e) em runtime) e as tres falas do operador de 22/10 por sha256, sem mudar nenhum veredito da v395 fora da troca dita (so' numeros)?",
    "dados": ["nenhum dado observado: a mecanica (projetor de Bell 4x4, reducao a um sitio, fluxo F_t = P + exp(-t beta g)(1 - P), colapso P y P) e' calculada e conferida contra os teoremas da pedra (replay documental e calculo)"],
    "metodo": "sandbox C:\\t\\k396c (copia de k396 + pedra, raiz e Audit com o import), lake build incremental e Audit; candidato DERIVADO por script da v395 selada (%d patches; comparacao AST: nada perdido); ensaio a seco (verify real com os logs crus, vizinhos recomputados, fluxo principal no ponto real do main, %d controles de unidade, selo, artigo PT/EN, simular_arvore_do_nos, exame_pontos); conferidor (controle negativo e caminho positivo emulado); recibo pre_selo do B(n) em modo ensaio, producao so' lida" % (len(CM["patches"]), len(ENS["unidade"])),
    "resultado": "%s | testemunha_estatica_v396: %d checagens da mecanica passam (par puro, individuo (1/2) I que nao ecoa, entropia de von Neumann %.9f = ln 2, fluxo fixa so' a reta do psion, testemunha global falsa, colapso idempotente e nao injetivo); composicao incondicional no kernel (%s); face de Fock CONDICIONAL e declarada em %s | Audit %d constantes e %d teoremas, 0 fora do trio | escada %d/%d | ensaio %s | pre_selo %s (%d PASSA, %d FALHA)" % (
        ESP["vereditos_novos_v396"]["testemunha_estatica_v396"], tv["n_checks"], tv["values"]["von_neumann_entropy"], tv["bandeira_incondicional"], tv["fock_face_declarada_em"], KH["linha_TOTAL"]["decl"], KH["linha_TOTAL"]["thm"], esc[1], esc[1], ENS["veredito"], PIN["veredito"], PIN["contagens"]["passa"], PIN["contagens"]["falha"]),
    "veredito": ESP["vereditos_novos_v396"]["testemunha_estatica_v396"],
    "defeito": "o rito real NAO rodou; instalar, rito e reverter (derivados) e o pos_rito (subagente) sem revisao independente; o build do sandbox e' incremental (a pedra ja estava compilada); a proveniencia do compilador atribui a pedra %d declaracoes e so' %d sao novas (a auxiliar TGLExt.diagFlow.eq_1 muda de modulo: %s); a ponte e' CONSTRUIDA, nao derivada; a face de Fock segue CONDICIONAL a um certificado sem habitante exibido" % (FJ["decl_totais_modulo_novo"], KH["decl_novas_do_modulo"], ", ".join("%s -> %s" % (v["antes"], v["agora"]) for v in reat.values()) or "nenhuma"),
    "nao_refazer": "a pedra, o registro e o ensaio estao medidos para o candidato %s; refazer so' se a pedra, o runtime, os textos ou o kernel mudarem (sh refazer_candidato_v396.sh --regerar; sh refazer_sandbox_v396.sh se o kernel mudar)" % S16,
    "proximo_passo": "revisao independente do gerador, do registro e dos derivados; decisoes da gerencia (patch dos registros anteriores incluindo o contrato do psibit_v395, politica de bandeiras e a reatribuicao de diagFlow.eq_1, ponto de chamada); o operador nomeia a pedra e decide se ela entra no um.py (ordem de 22/10: sem gordura); instalar e rodar o rito (ato da gerencia, depois do recibo pre_selo pinado); pos-rito; B(n) SEM SALTO (a parada do servico da Bancada e' ato do operador)",
    "onde": "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v396",
    "artefatos": art_prep,
    "refs": refs,
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 22/10/2026. Consultas ao mapa antes: v396 -> a custodia da v395 (outro assunto); testemunha estatica -> a origem do full_static_witness_exists (v385). A ROTA da pedra (%s), preparada pelo construtor em work\\testemunha_estatica_v396\\registro_mapa_testemunha_estatica.json, %s. Validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move." % (ROTA_PEDRA, "ja esta no livro" if ROTA_PEDRA in ids else "AINDA NAO esta no livro (ato da gerencia: registre-a antes; ela entra nas refs desta rota)")}
rec_banc = {
    "tipo": "ANOTACAO", "rota_id": "infra.bancada_um.sincronizacao_vnnn", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "Recibo pre_selo do B(n) da v396 (ensaio, producao so' lida): %s, pinado ANTES da instalacao" % PIN["veredito"],
    "resultado": "esboco R3.5, --versao v395 --fase pre_selo --modo ensaio; bateria %d PASSA, %d FALHA, %d NAO_EXECUTADO (T17 so' no pos_selo); utilizavel_como_recibo_pre_selo_do_B_n = %s; Bancada de producao (%d entradas) e Nos (%d) com listas iguais antes e depois; passo simples sem salto (pelo codigo do esboco os vereditos serao REPINADA_B6__...; lido, nao rodado); a Bancada pina %s" % (PIN["contagens"]["passa"], PIN["contagens"]["falha"], PIN["contagens"]["nao_executado"], str(PIN["utilizavel_como_recibo_pre_selo_do_B_n"]).lower(), PIN["escrita_na_producao"]["bancada_um"]["antes"], PIN["escrita_na_producao"]["nos"]["antes"], PIN["bancada_pina"]["deployment_id"]),
    "artefatos": [P("PINO_RECIBO_PRE_SELO_v396.json"), PIN["path"], P("PROVA_PRODUCAO_INTACTA_v396_pre_selo.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente do recibo pre_selo), 22/10/2026. Limites: T12/T13/T14 medidos contra o um.py v395; o recibo fica obsoleto se a producao for repinada antes do B(n); o servico esta no ar (a parada e' ato do operador)."}
reg = [rec_rota, rec_banc]
campos_modelo = set(rotas.MODELO)
saida = []
for r in reg:
    extras = sorted(set(r) - campos_modelo)
    assert not extras, ("campos fora do modelo", r["rota_id"], extras)
    v = rotas._valida(r, set(ids), seqs)   # a MESMA validacao do mapa (levanta ValueError se algo estiver errado); nao registra
    saida.append({"rota_id": v["rota_id"], "tipo": v["tipo"], "artefatos_n": len(v.get("artefatos", [])), "titulo_chars": len(v.get("titulo", ""))})
p = os.path.join(HERE, "registro_mapa_v396_prep.json"); b = (json.dumps(reg, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("VALIDO (rotas._valida, sem registrar):", json.dumps(saida, ensure_ascii=False)); print("registro_mapa_v396_prep.json", len(b), "bytes; sha16", hashlib.sha256(b).hexdigest()[:16])
