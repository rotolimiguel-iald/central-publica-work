# -*- coding: utf-8 -*-
"""Acrescenta ao AFERIDOR_v383.txt a 2a PASSADA (a diferenca do candidato e a cadeia do selo), VERBATIM, e as disposicoes; mapa: ANOTACAO. Hashes lidos."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
T = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
HDR = "# Duas conferências (só leitura): a diferença do candidato e a cadeia do selo da v383"
found = None
with open(T, encoding="utf-8") as f:
    for line in f:
        if '"queue-operation"' not in line or "aa2b5030fb5e4aa4a" not in line:
            continue
        d = json.loads(line); c = d.get("content")
        if d.get("type") == "queue-operation" and isinstance(c, str) and '<agent-message from="aa2b5030fb5e4aa4a">' in c and HDR in c:
            found = c; break
assert found, "relatorio nao achado na fila"
k = found.find("  " + HDR); body = found[k:]; e = body.find("</agent-message>"); body = body[:e] if e > 0 else body
rep = "\n".join((l[2:] if l.startswith("  ") else l) for l in body.split("\n")).rstrip() + "\n"
assert "INSTALAR" in rep and "B-M1" in rep and "B-M2" in rep
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
NEW = os.path.join(HERE, "um_v383_candidato.py"); OLD = os.path.join(HERE, "um_v383_candidato_b425fe335f61e134.py")
disp = """
--------------------------------------------------------------------------------
DISPOSICOES DA GERENCIA SOBRE A 2a PASSADA (%s) -- (A) INSTALAR, acolhida, com os dois BAIXOS corrigidos ANTES de instalar (nada selado com residuo);
(B) os dois MEDIOS e os sete BAIXOS corrigidos ANTES da cadeia.
--------------------------------------------------------------------------------
O DESVIO DO AFERIDOR, dito por ele: um diff gravou por engano C:\\Users\\rotol\\AppData\\Local\\Temp\\_never_written (21 018 B) e ele o removeu; fica registrado.
A-1 (o rotulo do alpha dizia «o literal CODATA 2018» e so conferia 1e-9): ACOLHIDO -- a conferencia passa a exigir alpha do V1.4 == SEALED_CODATA_ALPHA do programa
(o literal CODATA 2018, global em um.py:95), exato; o rotulo e a nota ao lado o dizem.
A-2 (o maximo |z| dos controles de ECO_e nao estava no artigo): ACOLHIDO -- o qualificador de ECO_e imprime «controles com |z| maximo de 4,81, abaixo de 5», lido do core.
O candidato novo (%s) e o conferido (%s) com EXATAMENTE as cinco trocas (tres no runtime, uma em cada snippet), provado por script; ensaio a seco TUDO PASSOU;
ESPERADOS regenerado; instalado as 20:04 (origem a v382 do Nos) e o rito lancado.
B-M1 (a folga do indice): ACOLHIDO -- cinco linhas do MEMORY.md (o handoff v381 superado, o v381 CUSTODIADO, a linha do β, a da suspensao e a da v384) foram INTEIRAS,
verbatim, para o fim do MEMORY_2.md, ficando ponteiros curtos (23 695 -> 23 160 B; regra dos dois arquivos); e o DECIDIDO que nao couber falha A VISTA (sys.exit 3).
B-M2 (a prova das afericoes no scratchpad): ACOLHIDO -- o arquivar inclui v382 e v382_selo (o AFERIDOR e o APLICADO da v382) e o diff do candidato; o handoff aponta
para C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v38x\\AFERIDOR_v38x.txt (o arquivar roda antes do handoff).
b1 marcas de backup _sup383/_p383/_handoff383; b2 _i383p/_i383; b3 os comentarios historicos da espera voltam a v382; b4 «nucleo da rodada v383, base v381»;
b5 as contagens lidas de V (n_ledger, rot_n, pr_label) nos textos, no handoff, nas superficies, no registro e no patch; b6 «os V1 a V1.3 ficam locais» marcado
[DERIVED de leitura, gerencia; a confirmar pelo operador] -- e levado a ele; b7 o comentario «marcador v376» e o diff no arquivo. Testes: as 13 funcoes de texto, o corpo
e a linha do handoff, as frases do registro e das superficies, com um dicionario de teste; nenhuma chave sobrando; todos compilam. PROVADA != CONFIRMADA.
""" % (time.strftime("%d/%m/%Y %H:%M"), h16(NEW), h16(OLD))
p = os.path.join(HERE, "AFERIDOR_v383.txt"); raw = open(p, "rb").read()
if HDR in raw.decode("utf-8", errors="replace"):
    print("AFERIDOR_v383.txt: a 2a passada ja esta")
else:
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    head = "\n\n" + "=" * 80 + "\n2a PASSADA -- A DIFERENCA DO CANDIDATO E A CADEIA DO SELO -- v383 (o mesmo agente, so leitura, 02/10/2026, noite; VERBATIM, indentacao do harness removida)\n" + "=" * 80 + "\n\n"
    novo = raw + (head + rep + disp).encode("utf-8"); open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw); os.replace(p + ".tmp", p)
    assert open(p, "rb").read()[:len(raw)] == raw
    print("AFERIDOR_v383.txt:", len(raw), "->", len(novo), "B; sha16", hashlib.sha256(novo).hexdigest()[:16])
regs = rotas._le()
if not any("afericao2_v383" in str(r.get("titulo", "")) for r in regs):
    o = rotas.registrar([dict(tipo="ANOTACAO", rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
        titulo="afericao2_v383 (02/10, noite; o mesmo agente): (A) o candidato INSTALAR, 2 BAIXOS (o rotulo do alpha; o maximo |z| dos controles de ECO_e) corrigidos antes; (B) a cadeia do selo: 2 MEDIOS (a folga do indice; a prova das afericoes no scratchpad) e 7 BAIXOS, corrigidos antes da cadeia; o agente registrou e desfez uma escrita acidental (um arquivo de diff no Temp)",
        resultado="candidato %s (o conferido + exatamente cinco trocas, provado por script), instalado; o indice 23 695 -> 23 160 B pela regra dos dois arquivos; o arquivar inclui a v382" % h16(NEW),
        nao_refazer="nao deixar a prova das afericoes so no scratchpad; nao digitar contagens nos textos da cadeia",
        proximo_passo="o mesmo agente confere as correcoes da cadeia durante o rito; depois a cadeia, o arquivar, o handoff e o registro",
        artefatos=[p], refs=["kernel.livro_de_cobrancas.otica"])], "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
    print("mapa:", {k: o[k] for k in o if k != "registros"})
else:
    print("mapa: ja registrado")
