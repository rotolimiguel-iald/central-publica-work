# -*- coding: utf-8 -*-
"""(1) Acrescenta ao AFERIDOR_v382.txt a CONFERENCIA FINAL antes da instalacao (o mesmo agente, so leitura), VERBATIM (da mensagem enfileirada do agente), e a
disposicao da gerencia sobre o unico BAIXO cosmetico, com os hashes LIDOS dos arquivos e a troca unica PROVADA por script. (2) Mapa: ANOTACAO do exame."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
ST = time.strftime("%Y%m%d_%H%M%S")
T = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
HDR = "# Conferência final antes da instalação"
MARCA = "conferencia_final_v382"
found = None
with open(T, encoding="utf-8") as f:
    for line in f:
        if '"queue-operation"' not in line or "aa2b5030fb5e4aa4a" not in line:
            continue
        d = json.loads(line); c = d.get("content")
        if d.get("type") == "queue-operation" and isinstance(c, str) and '<agent-message from="aa2b5030fb5e4aa4a">' in c and HDR in c:
            found = c; break
assert found, "conferencia final nao achada na fila"
k = found.find("  " + HDR); assert k >= 0
body = found[k:]; e = body.find("</agent-message>"); body = body[:e] if e > 0 else body
rep = "\n".join((l[2:] if l.startswith("  ") else l) for l in body.split("\n")).rstrip() + "\n"
assert "**Recomendação: INSTALAR.**" in rep
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
OLDP = os.path.join(HERE, "um_v382_candidato_c6f68e9bf3759a18.py"); NEWP = os.path.join(HERE, "um_v382_candidato.py")
old, new = open(OLDP, "rb").read(), open(NEWP, "rb").read()
a, b = "|z| lido".encode(), "z lido".encode()
assert old.count(a) == 1 and old.replace(a, b, 1) == new, "a troca unica nao se prova"
E = json.load(open(os.path.join(HERE, "ESPERADOS_v382.json"), encoding="utf-8")); R = json.load(open(os.path.join(HERE, "ensaio_a_seco_v382.json"), encoding="utf-8"))
assert E["candidato_sha16"] == h16(NEWP) == R["sha16"] and R["veredito"] == "TUDO PASSOU"
disp = """
--------------------------------------------------------------------------------
DISPOSICAO DA GERENCIA SOBRE A CONFERENCIA FINAL (%s) -- recomendacao: INSTALAR; acolhida.
--------------------------------------------------------------------------------
O unico BAIXO cosmetico (o rotulo «|z| lido» do check do R3 imprime o z com sinal): ACOLHIDO -- o rotulo passa a «z lido». O candidato novo (%s, %d B) e o conferido
(%s, %d B) com UMA troca de bytes, PROVADA por script (o rotulo velho ocorria uma vez; anterior.replace(velho, novo, 1) == novo). Ensaio a seco do candidato novo:
%s; ESPERADOS mudou so em candidato_sha16 e candidato_bytes. Segue a instalacao e o rito. PROVADA != CONFIRMADA; o gate nao se move.
""" % (time.strftime("%d/%m/%Y %H:%M"), h16(NEWP), len(new), h16(OLDP), len(old), R["veredito"])
p = os.path.join(HERE, "AFERIDOR_v382.txt"); raw = open(p, "rb").read()
if HDR in raw.decode("utf-8", errors="replace"):
    print("AFERIDOR_v382.txt: a conferencia final ja esta")
else:
    bak = p + ".bak_" + ST; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    head = ("\n\n" + "=" * 80 + "\n5a PASSADA -- CONFERENCIA FINAL ANTES DA INSTALACAO -- v382 (o mesmo agente, so leitura, 02/10/2026; recebido pela gerencia como mensagem do agente "
            "e gravado aqui VERBATIM, indentacao do harness removida)\n" + "=" * 80 + "\n\n")
    novo = raw + (head + rep + disp).encode("utf-8"); tmp = p + ".tmp"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo) > len(raw); os.replace(tmp, p)
    assert open(p, "rb").read()[:len(raw)] == raw
    print("AFERIDOR_v382.txt:", len(raw), "->", len(novo), "B; sha16", hashlib.sha256(novo).hexdigest()[:16])
regs = rotas._le()
if not any(MARCA in str(r.get("titulo", "")) for r in regs):
    o = rotas.registrar([
        dict(tipo="ANOTACAO", rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
             titulo="%s (02/10, o mesmo agente, só leitura): a diferença entre os candidatos corresponde só às disposições; os checks novos dizem só o que conferem; nenhum campo sem chave nos scripts da cadeia; a errata do R-1 com os dois nomes lidos; 0 ALTO, 0 MÉDIO, 1 BAIXO cosmético (o rótulo do z do R3), corrigido por uma troca provada por script; recomendação INSTALAR -- acolhida" % MARCA,
             resultado="candidato %s (ensaio a seco %s); segue a instalação e o rito" % (h16(NEWP), R["veredito"]),
             nao_refazer="o candidato passou por três aferições, a verificação das disposições e a conferência final da diferença",
             proximo_passo="instalação e rito v382", artefatos=[p], refs=["bancada.preregistro_dois_lados_delta_k"])],
        "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
    print("mapa:", {k: o[k] for k in o if k != "registros"})
else:
    print("mapa: ja registrado")
