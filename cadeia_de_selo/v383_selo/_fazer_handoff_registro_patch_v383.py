# -*- coding: utf-8 -*-
"""Fabrica handoff_v383.py, registrar_resultado_v383.py e patch_arvore_indice_v383.py a partir dos da v382 (v382 -> v383 nos nomes; depois as trocas de
CONTEUDO, count conferido): o livro de onze; os nove pares do eco fora do livro (decisao do operador); a base v381; a v382 selada so no Nos (NAO custodiar;
o seu stdout e os pre-registros V1-V1.3 ficam locais); a linha da suspensao no indice marcada DECIDIDO."""
import os, ast
HERE = os.path.dirname(os.path.abspath(__file__)); V2 = os.path.join(os.path.dirname(HERE), "v382_selo")
rd = lambda n: open(os.path.join(V2, n), encoding="utf-8", newline="").read().replace("v382", "v383").replace("V382", "V383")


def wr(n, s):
    ast.parse(s)
    p = os.path.join(HERE, n); assert not os.path.exists(p), p
    open(p, "w", encoding="utf-8", newline="").write(s); print("ok", n)


def subs(s, pares):
    for a, b, n in pares:
        assert s.count(a) == n, (a[:110], s.count(a), n); s = s.replace(a, b)
    return s


# ---- handoff
s = rd("handoff_v382.py")
i = s.index("Aferidores independentes ANTES do rito"); j = s.index("com os resíduos baixos também dispostos).", i) + len("com os resíduos baixos também dispostos).")
s = s[:i] + ("A v383 foi aferida antes do rito (relatório verbatim e disposições em `scratchpad\\\\v383\\\\AFERIDOR_v383.txt`); as aferições da v382 — três, a verificação das "
             "disposições e a conferência final — valem para as pedras e para o livro (`scratchpad\\\\v382\\\\AFERIDOR_v382.txt`).") + s[j:]
s = subs(s, [
    ('description: "HANDOFF v383 (%(data)s): O LIVRO DE COBRANÇAS (a TGL é ótica: lê a face e o custo; nenhum desfecho move a regra; o gate não lê o livro, pelos probes do runtime) + ψ com norma 1 e a viscosidade (duas pedras, %(kf_n)s declarações); o pré-registro dos dois lados do estimando δ⟨K_∂⟩ por hash; o nome do degrau final proposto ao lado; gate intocado; para a sessão do site custodiar"',
     'description: "HANDOFF v383 (%(data)s): O LIVRO DE COBRANÇAS (onze cobranças; a TGL é ótica: lê a face e o custo; nenhum desfecho move a regra; os nove pares do eco FORA do livro, como rotas examinadas, por decisão do operador) + ψ com norma 1 e a viscosidade (duas pedras, %(kf_n)s declarações); o pré-registro V1.4 por hash; a v382 selada só no Nós, NÃO custodiar; gate intocado; para a sessão do site custodiar"', 1),
    ("gate intocado (`%(qg)s`).** Sobre a v381 `%(base16)s`. Kernel novo:",
     "gate intocado (`%(qg)s`).** Sobre a v381 `%(base_build16)s`, no lugar da v382 `%(base16)s` (selada só no Nós em 02/10 e NÃO custodiada, por decisão do operador). Kernel novo (o mesmo da v382):", 1),
    ("a ratificação de R1–R6 e a correção «a TGL não é semi ela é ótica, ela lê tanto a face como o custo» [INPUT/ONTO], tipadas:",
     "a ratificação de R1–R6 e a correção «a TGL não é semi ela é ótica, ela lê tanto a face como o custo» [INPUT/ONTO], e a decisão (02/10, noite: «eu não quero publicar nada que seja "
     "resultado de falsificação, preciso entender isso, porque o que foi falsificado foi alguma rota, alguma aplicação equivocada da teoria, alguma interpretação que carece de ajuste» e, "
     "sobre a opção da gerência, «prefiro a primeira opção»: os nove pares do eco não são cobranças da teoria), tipadas:", 1),
    ("supersede %(pr_super)s pelos achados das aferições, antes de qualquer estimador ou dado novo; publicado na Bancada; mapa seq %(pr_seq)s); R2 sem poder (Γ(100 Hz) = %(r2_gamma)s s⁻¹).",
     "supersede %(pr_super)s pela decisão do operador, antes de qualquer estimador ou dado novo; publicado na Bancada; mapa seq %(pr_seq)s); R2 sem poder (Γ(100 Hz) = %(r2_gamma)s s⁻¹). "
     "Fora do livro, as %(rot_n)s rotas examinadas do eco como cópia atrasada, que não são cobranças da teoria: %(rot_ids)s — %(rot_exc)s excluídas pelos dados, %(rot_inc)s inconclusivas; "
     "o estado de cada uma é o rótulo da Fase 6 lido do core, e o motivo está no pré-registro.", 1),
    ("dos %(eco_n)s pares do eco como cópia atrasada, %(eco_ext)s estão extintos e %(eco_inc)s inconclusivos (nenhum move a regra);",
     "os nove pares do eco como cópia atrasada não são cobranças da teoria: são rotas examinadas fora do livro (%(rot_exc)s excluídas pelos dados, %(rot_inc)s inconclusivas), por decisão do operador;", 1),
    ("`rodada_v383_stdout.txt` em `rodadas\\\\`), regenerar as PORTAs por script, README/llms.txt, CITATION.cff, e o `MEMORIA_DA_LINHAGEM.md` do espelho.",
     "`rodada_v383_stdout.txt` em `rodadas\\\\`), regenerar as PORTAs por script, README/llms.txt, CITATION.cff, e o `MEMORIA_DA_LINHAGEM.md` do espelho. **NÃO espelhar "
     "`rodada_v382_stdout.txt`**: a v382 foi selada só no Nós e não é custodiada, por decisão do operador; a linhagem diz o que ela foi.", 1),
    ("O pré-registro dos dois lados (`C:\\\\IALD\\\\Bancada_Um\\\\investigacao\\\\preregistro_dois_lados_02out\\\\`) é lido por hash pelo um.py: vai junto com o cache da Bancada se o espelho o carregar.",
     "Do pré-registro dos dois lados (`C:\\\\IALD\\\\Bancada_Um\\\\investigacao\\\\preregistro_dois_lados_02out\\\\`), só o %(pr_label)s (`PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.json` e `.md`) "
     "é lido por hash pelo um.py e vai junto com o cache da Bancada se o espelho o carregar; os V1 a V1.3 ficam locais (traziam os pares do eco no livro).", 1),
    ("Ver [[beta-e-a-regra-matriz-02out]], [[regra-dos-dois-regimes]], [[handoff-v381-custodia]],", "Ver [[beta-e-a-regra-matriz-02out]], [[regra-dos-dois-regimes]], [[v382-custodia-suspensa]], [[handoff-v381-custodia]],", 1),
    ('linha = ("- [HANDOFF v383 — O LIVRO DE COBRANÇAS no kernel; custódia](handoff-v383-custodia.md) — **%s, para a sessão do site**: a TGL é ótica (lê a face e o custo); nenhum desfecho move a regra; ψ com norma 1 e a viscosidade; o pré-registro dos dois lados por hash; o nome do degrau final proposto ao lado; `%s`" % (V["data"][:5], V["s16"]))',
     'linha = ("- [HANDOFF v383 — O LIVRO DE COBRANÇAS no kernel; o eco fora do livro; custódia](handoff-v383-custodia.md) — **%s, para a sessão do site**: onze cobranças; os nove pares do eco fora do livro (decisão do operador); a v382 só no Nós, NÃO custodiar; ψ com norma 1 e a viscosidade; o pré-registro V1.4 por hash; `%s`" % (V["data"][:5], V["s16"]))', 1),
])
assert "eco_n" not in s and "eco_ext" not in s
s += '''
# v383: a linha da SUSPENSAO no indice ganha o marcador DECIDIDO (a v383 supera a v382); backup de bytes; tmp -> conferir -> replace; limite 24 000 B
raw = open(idx, "rb").read(); txt = raw.decode("utf-8")
ks = [k for k, l in enumerate(txt.split("\\n")) if "(v382-custodia-suspensa.md)" in l]
if len(ks) == 1 and "DECIDIDO" not in txt.split("\\n")[ks[0]]:
    L_ = txt.split("\\n"); L_[ks[0]] = L_[ks[0]] + " · **%s: DECIDIDO — a v383 `%s` supera; a v382 fica só no Nós**" % (V["data"][:5], V["s16"])
    novo2 = "\\n".join(L_).encode("utf-8")
    if len(novo2) <= 24000:
        bak2 = idx + ".bak_" + STAMP + "_handoff383_susp"; open(bak2, "wb").write(raw); assert open(bak2, "rb").read() == raw
        open(idx + ".tmp", "wb").write(novo2); assert os.path.getsize(idx + ".tmp") == len(novo2) > len(raw); os.replace(idx + ".tmp", idx)
        print("OK MEMORY.md: a linha da suspensao marcada DECIDIDO", len(raw), "->", len(novo2), "B")
    else:
        print("MEMORY.md: a marca DECIDIDO ficaria acima de 24 000 B (%d) -- nao gravo; a memoria-topico da suspensao ja diz a decisao" % len(novo2))
else:
    print("MEMORY.md: a linha da suspensao ja marcada (ou ausente):", len(ks))
'''
wr("handoff_v383.py", s)

# ---- registrar
s = rd("registrar_resultado_v382.py")
s = subs(s, [
    ("psi com norma 1 e a viscosidade -- TGLExt.TheLedgerOfCharges (%s) + TGLExt.ThePsionAndTheViscosity (%s), %s/%s no trio, sem sorry; o pre-registro dos dois lados lido por hash;",
     "psi com norma 1 e a viscosidade -- TGLExt.TheLedgerOfCharges (%s) + TGLExt.ThePsionAndTheViscosity (%s), %s/%s no trio, sem sorry; onze cobrancas; os nove pares do eco FORA do livro (rotas examinadas, nao cobrancas da teoria), por decisao do operador; a v382 selada so no Nos (nao custodiada); o pre-registro dos dois lados lido por hash;", 1),
    ('% (V["s16"], format(V["umb"], ","), V["base16"], V["teor"],', '% (V["s16"], format(V["umb"], ","), V["base_build16"], V["teor"],', 1),
    ('''nao_refazer="nenhum lado e cego (a TGL e otica); nenhum desfecho move beta; dos %s pares do eco como copia atrasada, %s estao extintos e %s inconclusivos (nenhum move a regra); o R4 nao tem FALSIFIED no conjunto congelado (a mesma fonte do degrau experimental do gate);" % (V["eco_n"], V["eco_ext"], V["eco_inc"])''',
     '''nao_refazer="nenhum lado e cego (a TGL e otica); nenhum desfecho move beta; os nove pares do eco como copia atrasada NAO sao cobrancas da teoria (decisao do operador): rotas examinadas fora do livro, %s excluidas pelos dados e %s inconclusivas; nao custodiar a v382; o R4 nao tem FALSIFIED no conjunto congelado (a mesma fonte do degrau experimental do gate);" % (V["rot_exc"], V["rot_inc"])''', 1),
    ('nota="proximo: o estimador da dissipacao na propagacao (R2), com o poder dito antes de abrir o banco de GW; nenhum dado novo olhado",',
     'nota="as %s rotas do eco fora do livro conferidas contra o V1.4 (estado lido do rotulo da Fase 6); proximo: o estimador da dissipacao na propagacao (R2), com o poder dito antes de abrir o banco de GW; nenhum dado novo olhado" % V["rot_n"],', 1),
])
s = subs(s, [('            artefatos=[os.path.join(NOS, "um_absoluto.json")], refs=["kernel.livro_de_cobrancas.otica"])]',
              '            artefatos=[os.path.join(NOS, "um_absoluto.json")], refs=["kernel.livro_de_cobrancas.otica"]),\n'
              '       dict(tipo="ANOTACAO", rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,\n'
              '            titulo="v383 SELADA (%s): a suspensao da v382 se resolve pela decisao do operador -- a sessao do site custodia a v383, NAO a v382 (%s); o stdout da v382 e os pre-registros V1-V1.3 ficam locais" % (V["s16"], V["v382_16"]),\n'
              '            nao_refazer="nao custodiar a v382; nao contar os pares do eco como cobrancas da teoria", refs=["kernel.livro_de_cobrancas.otica", "bancada.preregistro_dois_lados_delta_k"])]', 1)])
wr("registrar_resultado_v383.py", s)

# ---- patch arvore/indice: o titulo do verbete diz o eco fora do livro
s = rd("patch_arvore_indice_v382.py")
s = subs(s, [("o pré-registro dos dois lados \" + V['pr_label'] + \" do estimando δ⟨K_∂⟩ por hash; o nome do degrau final pelo pagamento proposto ao lado (v383)', _V383TXT),\")",
              "o pré-registro dos dois lados \" + V['pr_label'] + \" do estimando δ⟨K_∂⟩ por hash; os nove pares do eco fora do livro, como rotas examinadas (decisão do operador); o nome do degrau final pelo pagamento proposto ao lado (v383)', _V383TXT),\")", 1)])
wr("patch_arvore_indice_v383.py", s)
print("FABRICADOS handoff, registrar, patch (v383)")
