# -*- coding: utf-8 -*-
"""(1) Cria o AFERIDOR_v383.txt com o relatorio da AFERICAO DA v383 (o agente da 3a afericao da v382, so leitura), VERBATIM (da mensagem enfileirada), e as
disposicoes da gerencia. (2) Mapa: ERRATA ao lado do V1.4 (corrige 290: B-1 a proveniencia de alpha, B-2 o nome do campo do rotulo, B-6 a R6 inteira citada) e
ANOTACAO do exame. Hashes LIDOS dos arquivos."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
T = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
HDR = "# Aferição da v383 (candidato `3f62b37fe961141a`), só leitura"
found = None
with open(T, encoding="utf-8") as f:
    for line in f:
        if '"queue-operation"' not in line or "aa2b5030fb5e4aa4a" not in line:
            continue
        d = json.loads(line); c = d.get("content")
        if d.get("type") == "queue-operation" and isinstance(c, str) and '<agent-message from="aa2b5030fb5e4aa4a">' in c and HDR in c:
            found = c; break
assert found, "relatorio da afericao da v383 nao achado na fila"
k = found.find("  " + HDR); assert k >= 0
body = found[k:]; e = body.find("</agent-message>"); body = body[:e] if e > 0 else body
rep = "\n".join((l[2:] if l.startswith("  ") else l) for l in body.split("\n")).rstrip() + "\n"
assert "**Recomendação: CORRIGIR ANTES.**" in rep and "M-1" in rep
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
OLD = os.path.join(HERE, "um_v383_candidato_3f62b37fe961141a.py"); NEW = os.path.join(HERE, "um_v383_candidato.py")
E = json.load(open(os.path.join(HERE, "ESPERADOS_v383.json"), encoding="utf-8")); R = json.load(open(os.path.join(HERE, "ensaio_a_seco_v383.json"), encoding="utf-8"))
assert E["candidato_sha16"] == h16(NEW) == R["sha16"] and R["veredito"] == "TUDO PASSOU"
disp = """
--------------------------------------------------------------------------------
DISPOSICOES DA GERENCIA SOBRE A AFERICAO DA v383 (%s) -- recomendacao: CORRIGIR ANTES; acolhida. Cada ponto conferido no core e nos arquivos antes de acolher.
--------------------------------------------------------------------------------
M-1 (o artigo resumia as rotas sem os qualificadores do V1.4): ACOLHIDO -- o runtime le, para cada rota, o ROTULO PROPRIO da Fase 6 (fase6.veredito_principal /
emenda_v4.vereditos_todos / emenda_v5.vereditos_todos_DEC) e exige o mesmo estado; ECO_e le no core que a exclusao vem da emenda V4, NAO cega, e que o veredito V3 do
mesmo par e INCONCLUSIVE_SYSTEMATICS; ECO_g le que a clausula V5 esta no pre-registro, NAO foi aplicada pelo pipeline, e que o poder de R3 e < 5; as leis de maio
levam [INPUT, maio/2026] no V1.4. O artigo PT/EN imprime os dois qualificadores (so se as leituras do core passarem), o estatuto da lei de maio e a R6 so no
trecho que a rota usa, com a ligacao ao eco marcada [DERIVED de leitura, gerencia].
B-1 (a proveniencia de alpha no V1.4 e o um.py da v382): ACOLHIDO AO LADO -- o V1.4 nao se reescreve; ERRATA no mapa (corrige 290); o runtime confere que o beta do
V1.4 e o alpha do V1.4 vezes raiz de e (1e-15) e que o alpha do V1.4, o literal CODATA 2018, concorda com o alpha do core (calculado pelo motor da identidade) a 1e-9
relativo; nota ao lado no modulo. (A primeira tentativa usou o nome ALPHA_FINE_CODATA_2018 como global do modulo; ele so existe como texto de um script embutido,
e o teste em memoria reprovou -- corrigido antes do candidato.)
B-2 (o campo rotulo_da_fase6_citado e o token do modulo v380): ACOLHIDO AO LADO -- ERRATA no mapa; o runtime le e cita, ao lado, o rotulo proprio da Fase 6.
B-3 (a tabela de pedras mostra v382 sem nota): ACOLHIDO -- uma frase no paragrafo da v383 (PT/EN): as duas pedras aparecem como da v382, escritas e aferidas na
v382, que ficou so no Nos; publicas a partir desta versao. O registro de pedras nao muda (o texto das pedras diz v382).
B-4 (a docstring do conferidor dizia controle v381): ACOLHIDO -- o controle e o selo da v382 que esta no Nos.
B-5 (comentarios renomeados mecanicamente): ACOLHIDO -- instalar e rito voltam a «v382 (aferidor B1/C2)» e «aferidor v382 C1/C2»; o cabecalho do snippet diz «as
afericoes da v382 acolhidas».
B-6 (o V1.4 cita a R6 inteira, com o trecho «o custo nao esta nele», ja corrigido ao lado): ACOLHIDO AO LADO -- ERRATA no mapa; nota no modulo
(R6_in_the_routes); o artigo cita so o trecho que a rota usa.
A OBSERVACAO PARA O OPERADOR (o modulo, o paragrafo e a leitura do selo da v380, herdados e publicos, dizem FALSIFIED_AT_DELAY_LAW / PAIR_FALSIFIED_NOT_THE_THEORY):
levada a ele no relatorio da gerencia, antes de autorizar a custodia; o paragrafo da v383 diz, ao lado, que esse rotulo nomeia o par, nao a teoria.
Depois: candidato %s (era %s), ensaio a seco %s; ESPERADOS regenerado. PROVADA != CONFIRMADA; o gate nao se move.
""" % (time.strftime("%d/%m/%Y %H:%M"), h16(NEW), h16(OLD), R["veredito"])
p = os.path.join(HERE, "AFERIDOR_v383.txt")
if os.path.exists(p):
    print("AFERIDOR_v383.txt ja existe -- nada gravado")
else:
    head = ("=" * 80 + "\nAFERICAO DA v383 (o agente da 3a afericao da v382, so leitura, 02/10/2026, noite; recebido pela gerencia como mensagem do agente e gravado aqui VERBATIM, "
            "indentacao do harness removida)\n" + "=" * 80 + "\n\n")
    b = (head + rep + disp).encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
    print("AFERIDOR_v383.txt:", len(b), "B; sha16", hashlib.sha256(b).hexdigest()[:16])
regs = rotas._le()
if not any("afericao_v383" in str(r.get("titulo", "")) for r in regs):
    o = rotas.registrar([
        dict(tipo="ERRATA", corrige=290, rota_id="bancada.preregistro_dois_lados_delta_k", status="PROPOSTA", estatuto="REAL", olhou_dados=False,
             titulo="afericao_v383 (02/10, noite): ao lado do V1.4 -- (B-1) a proveniencia de alpha e o um.py do Nos no dia (a v382), o valor e o literal CODATA 2018, o mesmo da v381; (B-2) o campo rotulo_da_fase6_citado e o token do modulo v380 que le a Fase 6, nao o rotulo proprio da Fase 6; (B-6) o motivo das rotas cita a R6 inteira, inclusive o trecho «o custo nao esta nele», ja corrigido ao lado",
             resultado="o V1.4 nao se reescreve; o um.py v383 confere alpha/beta do V1.4 contra o core, le o rotulo proprio da Fase 6 ao lado e cita da R6 so o trecho que a rota usa",
             nao_refazer="nao reescrever o V1.4; a correcao vai ao lado", refs=["kernel.regra_matriz.cadeia_unica"]),
        dict(tipo="ANOTACAO", rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
             titulo="afericao_v383 (02/10, noite; o agente da 3a afericao da v382, so leitura): a decisao do operador cumprida exatamente (11 cobrancas campo a campo iguais ao V1.3; 9 rotas com os mesmos campos; motivos lidos das fontes; v382 so local; base v381); a moldura honesta (os dados excluem os pares e isso esta dito); 0 ALTO, 1 MEDIO (M-1: o artigo sem os qualificadores do V1.4), 6 BAIXOS; recomendacao CORRIGIR ANTES -- acolhida",
             metodo="o mapa 285-290; a memoria da suspensao; os backups da v381; os pre-registros V1-V1.4 e a diferenca dos geradores; o runtime v383 contra o v382 rodado em memoria sobre o core v381; a comparacao campo a campo das 11 cobrancas e das 9 rotas; as fontes dos motivos; o candidato contra a v382 do Nos e o kernel identico; o conferidor contra o controle v382; instalador, rito, ensaio e ESPERADOS; o dry PT/EN",
             resultado="corrigido antes do rito: os qualificadores de ECO_e e ECO_g lidos do core e impressos; o estatuto da lei de maio; a R6 so no trecho usado, com [DERIVED]; o rotulo proprio da Fase 6 lido ao lado; alpha/beta do V1.4 conferidos; a nota da tabela de pedras; o controle do conferidor; os comentarios historicos -- candidato %s" % h16(NEW),
             nao_refazer="o kernel da v383 e o da v382 (identico); o que segue e a conferencia da diferenca e o rito",
             proximo_passo="o mesmo agente confere a diferenca do candidato e a cadeia do selo v383; rito v383", artefatos=[p], refs=["bancada.preregistro_dois_lados_delta_k"])],
        "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
    print("mapa:", {k: o[k] for k in o if k != "registros"})
else:
    print("mapa: ja registrado")
