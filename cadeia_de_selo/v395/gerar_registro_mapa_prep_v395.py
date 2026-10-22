# -*- coding: utf-8 -*-
"""gerar_registro_mapa_prep_v395.py -- monta registro_mapa_v395_prep.json (LISTA de registros, SO' com campos de `rotas.py modelo`) a partir dos artefatos da cadeia (numeros e hashes LIDOS; nada digitado) e VALIDA cada
registro com a MESMA funcao que o mapa usa (rotas._valida), SEM registrar: importa rotas.py (so' constantes e funcoes), le rotas.jsonl para os ids e seqs existentes, nao escreve no livro. O registro no mapa e' ato da gerencia
(`rotas.py registrar <json> --quem ...`). Molde: psibit_v395\\scripts\\valida_registro.py. uso: python -I -B -X utf8 gerar_registro_mapa_prep_v395.py"""
import hashlib, importlib.util, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v395 as DL  # noqa: E402
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
CM = J("CANDIDATO_v395.json"); ESP = J("ESPERADOS_v395.json"); ENS = J("ensaio_a_seco_v395.json"); PIN = J("PINO_RECIBO_PRE_SELO_v395.json"); FJ = J("kernel", "FLAGS_v395.json"); KH = J("kernel", "KH_N1_v395.json")
X = J("EXAME_PONTOS_%s.json" % CM["sha16"]); CMP = J("COMPARACAO_V394_v395.json")
P = lambda *p: os.path.join(HERE, *p)
S16 = CM["sha16"]; pv = ESP["psibit"]; esc = CM["escada"]
ROTA_PSIBIT = "kernel.psibit_v395_candidata_21out"
art_prep = [P("ESTADO_V395.md"), P("CANDIDATO_v395.json"), P("ESPERADOS_v395.json"), P("ensaio_a_seco_v395.json"), P("kernel", "FLAGS_v395.json"), P("kernel", "KERNEL_RECIBO_v395.json"), P("kernel", "KH_N1_v395.json"), P("PINOS_BN_v395.json"),
            P("DIFF_KERNEL_v395.txt"), P("COMPARACAO_V394_v395.json"), P("conferencia_rito_v395_CONTROLE_NEGATIVO_PRE_RITO.json"), P("conferencia_rito_v395_POSITIVO_FALSO_NOS.json"), P("EXAME_PONTOS_%s.json" % S16), P("SIMULACAO_ARVORE_NOS_%s.json" % S16)]
rec_rota = {
    "tipo": "ROTA", "rota_id": "umpy.v395.psibit_na_fractalizacao_preparo", "dominio": "KERNEL_FORMAL", "status": "EM_CURSO", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "v395 PREPARADA (candidato %s): a pedra Psibit (1 modulo, %d bandeiras), o registro psibit_v395 chamado na fractalizacao do Um e as quatro falas de 21/10; escada %d -> %d; ensaio a seco %s; nada instalado, nada selado" % (S16, FJ["n_flags"], esc[0], esc[1], ENS["veredito"]),
    "pergunta": "o candidato v395 sela, no ensaio a seco, com a pedra TGLExt/Psibit no kernel, o modo psionico calculado na fractalizacao do Um (beta = alfa CODATA x sqrt(e) em runtime) e as quatro falas do operador de 21/10 por sha256, sem mudar nenhum veredito da v394 fora da troca dita (so' numeros)?",
    "dados": ["nenhum dado observado: a mecanica da orbita do Um pela matriz-S em theta_M e' calculada e conferida contra os teoremas da pedra (replay documental e calculo)"],
    "metodo": "sandbox C:\\t\\k395c (copia de k395 + raiz e Audit com o import), lake build incremental e Audit; candidato DERIVADO por script da v394 selada (18 patches; comparacao AST: nada perdido); ensaio a seco (verify real com os logs crus, vizinhos recomputados, fluxo principal no ponto real do main, %d controles de unidade, selo, artigo PT/EN, simular_arvore_do_nos, exame_pontos); conferidor (controle negativo e caminho positivo emulado); recibo pre_selo do B(n) em modo ensaio, producao so' lida" % len(ENS["unidade"]),
    "resultado": "%s | psibit_v395: %d checagens da mecanica passam; theta_M = %.9f rad; codigo (%.9f, %+d, %+d), paridade %+d; conjuncao incondicional no kernel (%s), face do psion CONDICIONAL | Audit %d constantes e %d teoremas, 0 fora do trio | escada %d/%d | ensaio %s | pre_selo %s (%d PASSA, %d FALHA)" % (
        ESP["vereditos_novos_v395"]["psibit_v395"], pv["n_checks"], pv["values"]["theta_M_rad"], pv["values"]["code_weight"], pv["values"]["code_word"], pv["values"]["code_verb"], pv["values"]["parity"], pv["bandeira_incondicional"], KH["linha_TOTAL"]["decl"], KH["linha_TOTAL"]["thm"], esc[1], esc[1], ENS["veredito"], PIN["veredito"], PIN["contagens"]["passa"], PIN["contagens"]["falha"]),
    "veredito": ESP["vereditos_novos_v395"]["psibit_v395"],
    "defeito": "o rito real NAO rodou; instalar, rito e reverter (derivados) e o pos_rito (subagente) sem revisao independente; o build do sandbox e' incremental (a pedra Psibit ja estava compilada); ALPHA_FINE_CODATA_2018 nao e' global do um.py (o registro usa SEALED_CODATA_ALPHA, mesmo dado, dois nomes) e o beta do core difere do alfa x raiz de e em 5,4e-13 relativo (o registro compara a 1e-9); a face do psion e' CONDICIONAL a um certificado sem habitante exibido",
    "nao_refazer": "a pedra, o registro e o ensaio estao medidos para o candidato %s; refazer so' se a pedra, o runtime, os textos ou o kernel mudarem (sh refazer_candidato_v395.sh --regerar; sh refazer_sandbox_v395.sh se o kernel mudar)" % S16,
    "proximo_passo": "revisao independente do gerador, do registro e dos derivados; decisoes da gerencia (patch dos registros v394, politica de bandeiras, ponto de chamada, leitura do beta); instalar e rodar o rito (ato da gerencia, depois do recibo pre_selo pinado); pos-rito; B(n) SEM SALTO (a parada do servico da Bancada e' ato do operador); a divergencia da tabela da patente ACOM Mirror e' LEGAL, do operador",
    "onde": "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v395",
    "artefatos": art_prep,
    "refs": [ROTA_PSIBIT, "umpy.v394.fock_tempo_e_cunhagens", "infra.bancada_um.sincronizacao_vnnn", "kernel.criterio_binario_de_parada.ponto_fixo_v394_d19"],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 21/10/2026. Consultas ao mapa antes: v395 -> custodia v393+v394 (proximo passo de custodia, outro assunto); psibit -> a rota da pedra (%s) apareceu durante a preparacao. Validade no kernel nao e' creditacao; NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move." % ROTA_PSIBIT}
rec_psibit = {
    "tipo": "ANOTACAO", "rota_id": ROTA_PSIBIT, "estatuto": "REAL", "olhou_dados": False,
    "titulo": "A pedra Psibit entrou no candidato v395 %s: lida no kernel do rito (sandbox), bandeira %s da conjuncao incondicional, escada %d, e chamada na fractalizacao do Um" % (S16, pv["bandeira_incondicional"], esc[1]),
    "resultado": "kernel: %d modulo novo, %d declaracoes (%d teoremas), %d bandeiras so' de declaracao nomeada, 0 fora do trio; psibit_v395 selou no ensaio (ponto de chamada: linha %d do candidato, logo depois do principio da defasagem fractal); face do psion %s; as 4 falas de 21/10 embutidas por sha256" % (CM["kernel"]["modulos_novos"], FJ["decl_totais_modulo_novo"], KH["delta_vs_v394"]["thm"], FJ["n_flags"], X["ponto_psibit"]["linha"], pv["conditional"]["status"]),
    "artefatos": [P("ESTADO_V395.md"), P("ensaio_a_seco_v395.json"), P("kernel", "FLAGS_v395.json"), P("EXAME_PONTOS_%s.json" % S16)],
    "nota": "Em nome proprio da gerencia c1 (subagente de preparacao), 21/10/2026; o exame independente da 2a versao da pedra esta na rota; o gate nao se move."}
rec_banc = {
    "tipo": "ANOTACAO", "rota_id": "infra.bancada_um.sincronizacao_vnnn", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "Recibo pre_selo do B(n) da v395 (ensaio, producao so' lida): %s, pinado ANTES da instalacao" % PIN["veredito"],
    "resultado": "esboco R3.5, --versao v394 --fase pre_selo --modo ensaio; bateria %d PASSA, %d FALHA, %d NAO_EXECUTADO (T17 so' no pos_selo); utilizavel_como_recibo_pre_selo_do_B_n = %s; Bancada de producao (%d entradas) e Nos (%d) com listas iguais antes e depois; passo simples sem salto (pelo codigo do esboco os vereditos serao REPINADA_B5__...; lido, nao rodado)" % (PIN["contagens"]["passa"], PIN["contagens"]["falha"], PIN["contagens"]["nao_executado"], str(PIN["utilizavel_como_recibo_pre_selo_do_B_n"]).lower(), PIN["escrita_na_producao"]["bancada_um"]["antes"], PIN["escrita_na_producao"]["nos"]["antes"]),
    "artefatos": [P("PINO_RECIBO_PRE_SELO_v395.json"), PIN["path"], P("PROVA_PRODUCAO_INTACTA_v395_pre_selo.json")],
    "nota": "Em nome proprio da gerencia c1 (subagente do recibo pre_selo), 21/10/2026. Limites: T12/T13/T14 medidos contra o um.py v394; o recibo fica obsoleto se a producao for repinada antes do B(n); o servico esta no ar (a parada e' ato do operador)."}
reg = [rec_rota, rec_psibit, rec_banc]
campos_modelo = set(rotas.MODELO)
saida = []
for r in reg:
    extras = sorted(set(r) - campos_modelo)
    assert not extras, ("campos fora do modelo", r["rota_id"], extras)
    ids_ = set(ids)
    v = rotas._valida(r, ids_, seqs)   # a MESMA validacao do mapa (levanta ValueError se algo estiver errado); nao registra
    saida.append({"rota_id": v["rota_id"], "tipo": v["tipo"], "artefatos_n": len(v.get("artefatos", [])), "titulo_chars": len(v.get("titulo", ""))})
p = os.path.join(HERE, "registro_mapa_v395_prep.json"); b = (json.dumps(reg, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("VALIDO (rotas._valida, sem registrar):", json.dumps(saida, ensure_ascii=False)); print("registro_mapa_v395_prep.json", len(b), "bytes; sha16", hashlib.sha256(b).hexdigest()[:16])
