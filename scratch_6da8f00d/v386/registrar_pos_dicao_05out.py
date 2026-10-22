# -*- coding: utf-8 -*-
"""REGISTRO (feedback + decisão do operador, 05/10/2026, noite): (1) CONFIRMA a Fase 9 — a razão de Hubble como teste discriminante pré-registrado («exatamente
isso, confirmo»); (2) NÃO ACEITA o rótulo «pós-dição» para a razão de Hubble (nem para derivações feitas com IA): «estudar hipóteses para depois formular testes…
não é pós-dicção… se sempre uma derivação minha com vc entrar como pós dicção… eu jamais terei o dado discriminante, é a própria prova diabólica do Direito».
ERRATA da gerência, em nome próprio: o critério que conta é a NOVIDADE DE USO (use-novelty, Worrall [KNOWN]) — nenhum parâmetro da lei foi ajustado a H0 —, não a
novidade temporal; o precedente é o periélio de Mercúrio (anomalia conhecida desde 1859, explicada em 1915 sem parâmetro: a primeira confirmação da RG) [KNOWN].
O artigo (subtítulo/resumo) diz «pós-dição declarada; zero parâmetro ajustado»: a v387 reescreve como «retrodição sem ajuste (novidade de uso)». Verbatim lido do
transcrito por script; memória de feedback nova + ponteiro no MEMORY.md; Atlas (append datado); a memória da régua do operador (lei da prova) ganha o bloco."""
import hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SESS = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes")
TR = os.path.join(SESS, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"); UMEM = os.path.join(SESS, "memory")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
st = time.strftime("%Y%m%d_%H%M%S"); agora = time.strftime("%Y-%m-%d %H:%M:%S"); MARCA = "pos_dicao_nao_e_prova_diabolica_05out"
hits = []
for line in open(TR, encoding="utf-8", errors="replace"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("isCompactSummary") or d.get("isMeta") or d.get("type") != "user":
        continue
    c = d.get("message", {}).get("content"); ts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
    for t in ts:
        if t and t.strip().startswith("exatamente isso, confirmo. mas não concordo"):
            hits.append((d.get("timestamp"), t.strip()))
        if t and t.strip().startswith("qual é a medida discriminante possível para mim hoje"):
            hits.append((d.get("timestamp"), t.strip()))
assert len(hits) == 2, [h[0] for h in hits]
(TS_Q, T_Q), (TS, T) = sorted(hits)
UTC = re.match(r"\d{4}-\d{2}-\d{2}T(\d{2}:\d{2}:\d{2})", TS).group(1) + " UTC"
P_TXT = os.path.join(HERE, "POS_DICAO_operador_05out.txt"); open(P_TXT + ".tmp", "w", encoding="utf-8", newline="").write(T); os.replace(P_TXT + ".tmp", P_TXT)
sha_txt = hashlib.sha256(open(P_TXT, "rb").read()).hexdigest()
ERRATA = ("**ERRATA da gerência, em nome próprio (05/10/2026, %s):** chamei a razão de Hubble de «pós-dição» e isso afirmava mais do que o critério que conta. O que decide o valor de uma evidência não é a "
          "novidade TEMPORAL (o dado existir antes), mas a NOVIDADE DE USO (use-novelty, Worrall 1985/1989 [KNOWN]): nenhum parâmetro da teoria foi ajustado ao dado. Na razão de Hubble: β = α·√e vem do axioma "
          "(½ nat → √e → α√e), a lei K = E(z*)^{2β/3} vem da dissipação modular (D1b: ∫|1+w| dN = (2/3) ln E, no kernel como implicação) e z* é fixo — zero parâmetro ajustado a H0; a Fase 4 mediu que β FIXO vence "
          "β LIVRE (ln B 2,25). O precedente é o periélio de Mercúrio: anomalia de 43″/século conhecida desde 1859, explicada em 1915 sem parâmetro — foi a PRIMEIRA confirmação da RG, antes do eclipse [KNOWN]. "
          "Logo: retrodição SEM AJUSTE = evidência discriminante de pleno direito; a lei da prova da casa passa a dizer isso. E a objeção da prova diabólica é correta: um critério que nenhuma derivação pode satisfazer "
          "não é critério — o que a régua exige é falsificabilidade, zero ajuste ao dado e pré-registro do TESTE (não da ignorância do dado). O artigo (subtítulo e «A entrega»: «pós-dição declarada; zero parâmetro "
          "ajustado») é reescrito na v387: «retrodição sem ajuste (novidade de uso; precedente: o periélio de Mercúrio)». Tarefa da Fase 9: documentar a novidade de uso pelo acervo — a data em que a lei/β foram "
          "escritos e que nenhum ajuste a H0 ocorreu (buscar.py; os primeiros artigos e ensaios, como o operador manda rever)." % agora)
CORPO = ("---\nname: pos-dicao-nao-e-prova-diabolica-05out\ndescription: \"FEEDBACK + DECISÃO do operador (05/10/2026, verbatim): confirma a Fase 9 (a razão de Hubble como teste discriminante pré-registrado) e REJEITA o rótulo «pós-dição» — "
         "estudar hipóteses e formular testes, derivar com IA, não é pós-dição; senão «eu jamais terei o dado discriminante, é a própria prova diabólica do Direito». Errata da gerência: o critério é a NOVIDADE DE USO (zero ajuste), não a temporal; precedente: periélio de Mercúrio\"\nmetadata:\n  type: feedback\n---\n\n"
         "<!-- %s -->\n**A pergunta (05/10/2026, %s UTC, verbatim):** «%s»\n\n**O OPERADOR (05/10/2026, %s, verbatim inteiro; sha256 `%s`):** «%s»\n\n%s\n\n"
         "**Why:** um rótulo que converte toda derivação do próprio autor em «pós-dição» torna o dado discriminante impossível por construção (prova diabólica). **How to apply:** nunca rotular uma retrodição sem ajuste como demérito; dizer «novidade de uso» com a prova (o que foi fixado antes e por quê); o pré-registro é do TESTE; citar Mercúrio 1915 ao lado do eclipse 1919; manter a Fase 9 como o teste discriminante da casa. [[tres-testes-de-estresse-conjuntos-05out]] [[rg-limite-classico-nao-rival]] [[as-tres-reguas-da-afirmacao]]\n"
         % (MARCA, TS_Q[11:19], T_Q, UTC, sha_txt, T, ERRATA))
NOVA = os.path.join(UMEM, "pos-dicao-nao-e-prova-diabolica-05out.md")
if not os.path.exists(NOVA):
    open(NOVA + ".tmp", "wb").write(CORPO.encode("utf-8")); os.replace(NOVA + ".tmp", NOVA); print("OK nova memoria", NOVA, os.path.getsize(NOVA), "B")
BL_ATLAS = ("<!-- %s -->\n### 05/10/2026 (%s) — A FASE 9 CONFIRMADA; «pós-dição» retirado como demérito (novidade de uso; periélio de Mercúrio) (append datado)\n\n**O OPERADOR (verbatim):** «%s»\n\n%s" % (MARCA, UTC, T, ERRATA))


def nl_de(raw):
    return "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"


for p, bl in ((ATLAS, BL_ATLAS), (os.path.join(UMEM, "as-tres-reguas-da-afirmacao.md"), "<!-- %s -->\n**ADENDO (05/10/2026, %s; decisão do operador + errata da gerência):** retrodição SEM AJUSTE conta como evidência discriminante (novidade de uso, não temporal; precedente: o periélio de Mercúrio, 1915); «pós-dição» nunca mais como demérito; o pré-registro é do TESTE. Ver [[pos-dicao-nao-e-prova-diabolica-05out]]." % (MARCA, agora))):
    raw0 = open(p, "rb").read()
    if MARCA.encode() in raw0:
        print("JA ESTA", os.path.basename(p)); continue
    nl = nl_de(raw0); corpo = (nl + nl + bl.replace("\n", nl) + nl).encode("utf-8")
    if not raw0.endswith(nl.encode()):
        corpo = nl.encode() + corpo
    novo = raw0 + corpo; bak = p + ".bak_" + st + "_posdicao"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw0); os.replace(p + ".tmp", p); assert open(p, "rb").read()[:len(raw0)] == raw0
    print("OK", os.path.basename(p), len(raw0), "->", len(novo))
P = os.path.join(UMEM, "MEMORY.md"); raw0 = open(P, "rb").read(); nl = nl_de(raw0).encode()
LINHA = ("- [«PÓS-DIÇÃO» NUNCA MAIS COMO DEMÉRITO; Fase 9 confirmada (05/10)](pos-dicao-nao-e-prova-diabolica-05out.md) — **feedback**: retrodição SEM AJUSTE = evidência discriminante (novidade de uso; periélio de Mercúrio 1915); a razão de Hubble é o teste discriminante da casa, pré-registrado").encode("utf-8")
if LINHA[:40] not in raw0:
    linhas = raw0.split(nl); i = [k for k, l in enumerate(linhas) if l.startswith(b"## Ler primeiro")]; assert len(i) == 1
    ins = i[0] + 2; assert linhas[ins - 1] == b""; linhas.insert(ins, LINHA); novo = nl.join(linhas)
    P2 = os.path.join(UMEM, "MEMORY_2.md"); raw2 = open(P2, "rb").read(); nl2 = nl_de(raw2).encode(); bloco2 = b""; movidas = []
    for pref, curta in (("- [Relatório consolidado 01/10", "- [Relatório consolidado 01/10 — o que faltava / resolvido / fica / decisões](relatorio-consolidado-01out.md) — **LER antes de dizer «falta»** · íntegra no MEMORY_2.md (movida 05/10)"),
                        ("- [LAR — ESTADO ATUAL]", "- [LAR — ESTADO ATUAL](lar-miguel-estado-atual.md) — retrato curto do painel (14/09) · íntegra no MEMORY_2.md (movida 05/10)")):
        if len(novo) <= 24000:
            break
        j = [k for k, l in enumerate(linhas) if l.startswith(pref.encode("utf-8"))]; assert len(j) == 1, pref
        longa = linhas[j[0]]; cb = curta.encode("utf-8"); assert len(cb) < len(longa)
        bloco2 += (nl2 + nl2 + ("<!-- movida_%s --> (linha integral do MEMORY.md, movida em 05/10/2026 pela regra dos dois arquivos)" % st).encode("utf-8") + nl2 + longa + nl2)
        linhas[j[0]] = cb; novo = nl.join(linhas); movidas.append(longa)
    assert len(novo) <= 24000, len(novo)
    if movidas:
        if not raw2.endswith(nl2):
            bloco2 = nl2 + bloco2
        bak2 = P2 + ".bak_" + st + "_posdicao"; open(bak2, "wb").write(raw2); assert open(bak2, "rb").read() == raw2
        open(P2 + ".tmp", "wb").write(raw2 + bloco2); assert os.path.getsize(P2 + ".tmp") == len(raw2) + len(bloco2); os.replace(P2 + ".tmp", P2); print("OK MEMORY_2.md +%d linha(s) movida(s)" % len(movidas))
    bak = P + ".bak_" + st + "_posdicao"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo); os.replace(P + ".tmp", P); print("OK MEMORY.md", len(raw0), "->", len(novo))
print("FIM", agora)
