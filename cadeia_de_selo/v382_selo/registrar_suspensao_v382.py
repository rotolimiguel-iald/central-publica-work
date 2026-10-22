# -*- coding: utf-8 -*-
"""A v382 rodou limpa SO no Nos; a custodia fica SUSPENSA ate o operador decidir como a TGL publica os pares do eco excluidos.
(1) memoria-topico `v382-custodia-suspensa.md` + linha no MEMORY.md (backup de BYTES; tmp -> conferir -> replace; limite 24 000 B);
(2) mapa: ANOTACAO (EM_CURSO). Tudo LIDO dos artefatos (conferidor, um.py, stdout do rito); nada digitado."""
import os, re, sys, json, time, hashlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
UMEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
ST = time.strftime("%Y%m%d_%H%M%S")
VERB = ("eu não quero publicar nada que seja resultado de falsificação, preciso entender isso, porque o que foi falsificado foi alguma rota, "
        "alguma aplicação equivocada da teoria, alguma interpretação que carece de ajuste")
C = json.load(open(os.path.join(HERE, "conferidor", "conferencia_rito_v382.json"), encoding="utf-8"))
assert C.get("tudo_bate") is True
dm, npm = C.get("deve_mudar") or {}, C.get("nao_pode_mudar") or {}
s16 = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
assert C.get("um_py_sha16") == s16
out = open(os.path.join(NOS, "rodada_v382_stdout.txt"), encoding="utf-8", errors="replace").read()
teor = re.search(r"teoremas limpos: (\d+)/(\d+)", out).group(0)
rc = re.findall(r"^RITO_RC=(\d+)", out, re.M)[-1]
assert rc == "0" and "FAIL_CLOSED_SELFTEST_PASSED" in out
conf = "TUDO BATE (%d/%d deve mudar; %d/%d não pode mudar)" % (sum(1 for v in dm.values() if v), len(dm), sum(1 for v in npm.values() if v), len(npm))
corpo = """---
name: v382-custodia-suspensa
description: "v382 selada SÓ no Nós (02/10, noite): custódia SUSPENSA até o operador decidir como a TGL publica os pares do eco excluídos; a sessão do site NÃO custodia a v382"
metadata:
  type: project
---

**02/10/2026, noite.** O rito da v382 rodou limpo no Nós: `um.py` `%(s16)s`, RITO_RC=%(rc)s, %(teor)s, autoteste fail-closed aprovado; conferidor %(conf)s. Tudo lido dos artefatos por script.

**O operador, verbatim (02/10, depois do rito lançado):** «%(verb)s».

**Suspenso pela gerência até a decisão dele:** a cadeia pós-rito (superfícies, árvore, índice, Atlas), o handoff para a sessão do site e o registro do resultado. **A sessão do site NÃO custodia a v382.** Os scripts estão prontos em `scratchpad\\v382_selo\\` (chain_pos_rito_v382.sh, handoff_v382.py, registrar_resultado_v382.py, arquivar_v382.py).

**O que foi excluído e por quê (a resposta dada a ele):** cinco versões do modelo «o eco como cópia atrasada do ringdown» (amplitude √β ou sin 2θ × atraso KMS, dezembro ou maio), excluídas pelos dados do LIGO/Virgo; o objeto é o PAR (leitura de amplitude × lei de atraso), não a TGL: a amplitude do eco = |R| é [ONTO]; sin 2θ é [CONJECTURE]; o atraso KMS usa uma largura em tempo imaginário como atraso real (GWECO-05); a lei de dezembro é [DECLARADO], derivada por IA, não do axioma, e põe a massa do remanescente no atraso (contra a R6 ratificada); na v381 o operador pôs o eco como cópia fora da cadeia. Também a partição P2 dos relógios ficou excluída na leitura. As cinco exclusões já são públicas desde a custódia da v380 (02/10) e seguem na v381.

**A decisão pendente (do operador):** (a) recomendação da gerência — tirar do livro de cobranças os nove pares do eco (cinco excluídos, quatro inconclusivos), que não são cobranças da teoria, e publicá-los como rotas examinadas e excluídas, com os números e o motivo; pede pré-registro V1.4 e uma v383; a v382 fica selada só localmente; (b) custodiar a v382 como está, com o motivo de cada exclusão escrito ao lado.

Ver [[handoff-v381-custodia]], [[fase6-eco-radical-01out]], [[beta-e-a-regra-matriz-02out]], [[mapa-de-rotas]].
""" % dict(s16=s16, rc=rc, teor=teor, conf=conf, verb=VERB)
p = os.path.join(UMEM, "v382-custodia-suspensa.md")
if os.path.exists(p):
    print("memoria ja existe:", p)
else:
    open(p + ".tmp", "wb").write(corpo.encode("utf-8")); assert os.path.getsize(p + ".tmp") == len(corpo.encode("utf-8")); os.replace(p + ".tmp", p)
    print("OK", p, len(corpo.encode("utf-8")), "B")
linha = ("- [v382 SELADA SÓ NO NÓS; CUSTÓDIA SUSPENSA (02/10)](v382-custodia-suspensa.md) — **a sessão do site NÃO custodia a v382** até o operador decidir como "
         "publicar os pares do eco excluídos (o par, não a teoria); `%s`" % s16)
idx = os.path.join(UMEM, "MEMORY.md"); raw = open(idx, "rb").read(); assert b"\r\n" not in raw
if b"v382-custodia-suspensa.md" in raw:
    print("indice: ja tem a linha")
else:
    txt = raw.decode("utf-8"); anc = "- [HANDOFF v381 — A REGRA MATRIZ no kernel; custódia](handoff-v381-custodia.md)"
    assert txt.count(anc) == 1
    novo = txt.replace(anc, linha + "\n" + anc).encode("utf-8"); assert len(novo) <= 24000, len(novo)
    bak = idx + ".bak_" + ST + "_susp382"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(idx + ".tmp", "wb").write(novo); assert os.path.getsize(idx + ".tmp") == len(novo) > len(raw)
    assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
    print("OK MEMORY.md", len(raw), "->", len(novo), "B")
regs = rotas._le()
if not any("v382_custodia_suspensa" in str(r.get("titulo", "")) for r in regs):
    o = rotas.registrar([dict(tipo="ANOTACAO", rota_id="kernel.regra_matriz.cadeia_unica", status="EM_CURSO", estatuto="REAL", olhou_dados=False,
        titulo="v382_custodia_suspensa (02/10, noite): a v382 rodou limpa só no Nós (um.py %s; RITO_RC=%s; %s; conferidor %s); a custódia fica SUSPENSA até o operador decidir como a TGL publica os pares do eco excluídos; a sessão do site NÃO custodia a v382" % (s16, rc, teor, conf),
        resultado="o operador, verbatim: «%s». Suspensos: a cadeia pós-rito, o handoff e o registro do resultado" % VERB,
        nao_refazer="não custodiar a v382 sem a decisão do operador; o que caiu foi o PAR (leitura de amplitude × lei de atraso), não a teoria",
        proximo_passo="decisão do operador: (a) tirar do livro os nove pares do eco e publicá-los como rotas excluídas (pré-registro V1.4 + v383) ou (b) custodiar a v382 com o motivo ao lado",
        artefatos=[os.path.join(NOS, "rodada_v382_stdout.txt"), os.path.join(NOS, "um_absoluto_selo.json"), os.path.join(HERE, "conferidor", "conferencia_rito_v382.json")],
        refs=["bancada.preregistro_dois_lados_delta_k"])], "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
    print("mapa:", {k: o[k] for k in o if k != "registros"})
else:
    print("mapa: ja registrado")
