# -*- coding: utf-8 -*-
"""03/11/2026 15:1x, gerencia c1 (ordem do operador, verbatim sha16 484af3b204b1be9e: «monte você mesmo a v407, não delegue a outro modelo»): as CORRECOES DA GERENCIA (R2) sobre o
rascunho da preparacao, a partir dos nove BAIXOS da revisao de terceiro R1 (revisao_terceiro/REVISAO_TERCEIRO_v407.md) e da leitura da propria gerencia. Tudo por substituicao
EXATA (assert count == 1), com backup de BYTES `.bak_<ts>_c1_r2` ao lado de cada arquivo tocado; temporario -> os.replace. Nada toca o Nos, o kernel canonico, o selo ou o gate.
O que muda e por que:
 (1) PsionCantoR1.lean (fonte): citacao exata «virar essa chave de conjectura para provado» (BAIXO 3); escopo do lema dito (BAIXO 6); «nome provisorio» fora do docstring do teorema (BAIXO 8).
 (2) OParDePsionsR1.lean (fonte): «em theta = pi a polarizacao e+ do setor TT volta a si» (BAIXO 1); [KNOWN/ONTO] -> [ONTO] (BAIXO 8); «nome provisorio» -> «conjuncao, nao identificacao» (BAIXO 8).
 (3) OUmInscritoCandidata.lean (fonte): a cunhagem de 02/11 verbatim, com acento e sha16 (BAIXO 3); a frase «o unico autovetor do boost e' o zero», que esta' na lista de frases proibidas da casa
     e e' imprecisa (o zero nao e' autovetor), reescrita como «nenhum vetor nao nulo e' autovetor do boost; so' o zero satisfaz a condicao» (BAIXO 2, decisao da gerencia).
 (4) OIgualCandidata.lean e APonteDoAtritoCandidata.lean (fontes): citacoes exatas com acento, pontuacao do original e sha16; a cadeia «tensao -> ... -> magnetismo» sem aspas (BAIXO 3).
 (5) delta_v407.py: RESSALVAS_V407[0] (escopo do lema, BAIXO 6), [3] e E19 (sem aspas em parafrase, BAIXO 3), [4] (as nove relidas na R1, as correcoes vao a R2), [7] (abaixo de 5 sigma: parede medida, BAIXO 7);
     TESTEMUNHA.sha16_da_ordem e preparar_bundle PEDRAS.sha16_da_ordem = o sha16 NOVO da fonte da PsionCanto (lido depois da edicao).
 (6) runtime_v407.py c16: a checagem varre o core por qualquer chave de resultado do teste D (BAIXO 5).
 (7) gerar_candidato_v407.py: o campo fock_face.reading da testemunha ramifica pela chave lida (BAIXO 4).
 (8) artigo_pt/en_v407.pysnip: OUmInscrito no Fock concreto [KNOWN, a conferir] e «Um inscrito = vacuo» [ONTO] (BAIXO 2); escopo do lema (BAIXO 6); teste D abaixo de 5 sigma (BAIXO 7); as nove relidas (ressalva 4).
 (9) orquestrador/pos_treino_v407.py s1b: confere tambem os `arquivos_revisados` contra o disco (BAIXO 9).
 (10) pedra/<Nome>.lean e pedra/origem/<fonte> das pedras alteradas vao para pedra/antes_de_<ts>/ (o preparar_bundle recusa duravel divergente).
Depois deste script: preparar_bundle_v407_03nov.py -> construir_kernel (lake build incremental + Audit) -> pos_build -> copiar_insumos -> refazer_candidato --regerar -> R2 do revisor -> fechar. Escrito pelo Write."""
import hashlib, os, re, shutil, time
from pathlib import Path
TS = time.strftime("%Y%m%d_%H%M%S"); W = Path(r"C:\IALD\Central de Patentes\work"); V7 = W / "cadeia_de_selo" / "v407"; P3 = W / "pedras_candidatas_03nov"
sha16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]  # noqa: E731
LOG = []


def troca(p, pares, rot):
    """substituicoes EXATAS em bytes (utf-8), cada 'old' presente UMA vez; backup de bytes; temporario -> os.replace."""
    p = Path(p); b = p.read_bytes(); s = b.decode("utf-8"); novo = s
    for old, new in pares:
        assert novo.count(old) == 1, ("trecho nao esta' UMA vez (%d) em %s: %r" % (novo.count(old), p.name, old[:90]))
        novo = novo.replace(old, new)
    assert novo != s
    bak = p.with_name(p.name + ".bak_" + TS + "_c1_r2"); open(bak, "xb").write(b); assert bak.read_bytes() == b
    tmp = p.with_name(p.name + ".tmp_" + TS); open(tmp, "xb").write(novo.encode("utf-8")); os.replace(tmp, p); assert p.read_bytes() == novo.encode("utf-8")
    LOG.append("%s: %d trocas; %d -> %d B; backup %s" % (p.name, len(pares), len(b), len(novo.encode("utf-8")), bak.name)); print(LOG[-1])


# ---------------------------------------------------------------- (1) PsionCantoR1.lean (fonte)
troca(P3 / "PsionCantoR1.lean", [
    ("que, no kernel, «vira a chave de conjectura para provado» — como VALIDADE", "que, no kernel, «virar essa chave de conjectura para provado» — como VALIDADE"),
    ("  ESTRUTURA (a mesma construção «canto escalar de um vetor de norma 1», os mesmos invariantes, a mesma leitura comprimida), não de vetores.\n* NÃO deriva que `psionFlow`",
     "  ESTRUTURA (a mesma construção «canto escalar de um vetor de norma 1», os mesmos invariantes, a mesma leitura comprimida), não de vetores.\n"
     "* O resultado sob compressão decorre de `Ω` ser fixo pela luz e de o canto ser projeção de posto 1: vale para QUALQUER vetor unitário fixo pelo fluxo;\n"
     "  o lema NÃO relaciona as duas faces por uma aplicação entre os espaços; o que ele diz é que a mesma construção, com os mesmos invariantes, vive nas duas.\n"
     "* NÃO deriva que `psionFlow`"),
    ("/-- ★★★ O LEMA QUE LIGA AS DUAS FACES DO PSÍON (nome provisório). Nas duas faces o psíon é o vetor de norma 1 cujo canto é o projetor",
     "/-- ★★★ O LEMA QUE LIGA AS DUAS FACES DO PSÍON (elo de estrutura; o nome `PsionCanto` foi aceito pelo operador em 03/11/2026). Nas duas faces o psíon é o vetor de norma 1 cujo canto é o projetor"),
], "psion")
# ---------------------------------------------------------------- (2) OParDePsionsR1.lean (fonte)
troca(P3 / "OParDePsionsR1.lean", [
    ("  e o RETORNO DE FASE é a meia-volta: em θ = π o par volta a si (`cos 2π = 1`, `sin 2π = 0`).",
     "  e o RETORNO DE FASE é a meia-volta: em θ = π a polarização `e₊` do setor TT volta a si (`cos 2π = 1`, `sin 2π = 0`) — a face de helicidade do kernel,\n"
     "  lida AO LADO da face ligada; não é uma propriedade provada do projetor de Bell (os dois espaços são distintos; ver «O que esta pedra NÃO afirma»)."),
    ("por construção, `canonicalGravitonShadow`, e prova as duas hélices no setor TT, `qgPhysicsCertificate_helicities`; o elo entre os dois é [KNOWN/ONTO]).",
     "por construção, `canonicalGravitonShadow`, e prova as duas hélices no setor TT, `qgPhysicsCertificate_helicities`; o elo entre os dois é [ONTO] até haver citação)."),
    ("/-- ★★★ A CUNHAGEM COMPOSTA (nome provisório): ligado, nunca cancelado, lido pela fase e pelo retorno de fase, no canto 4×4. -/",
     "/-- ★★★ A CUNHAGEM COMPOSTA (conjunção, não identificação): ligado, nunca cancelado, lido pela fase e pelo retorno de fase, no canto 4×4. -/"),
], "par")
# ---------------------------------------------------------------- (3) OUmInscritoCandidata.lean (fonte): a cunhagem verbatim (sha16 25010b04c17e8ce1) e a frase proibida reescrita
troca(W / "fechamento_02nov" / "OUmInscritoCandidata.lean", [
    ("Cunhagem do operador (02/11/2026): «a luz tem autovetor: a inscricao do um absoluto, que e na essencia ela mesma, ou seja,\n"
     "identidade; o um absoluto inscrito e a identidade da luz; por isso o par, inclusive dela mesma; sem par somente o zero\n"
     "absoluto, que e o abstrato inominado».",
     "Cunhagem do operador (02/11/2026, verbatim sha16 25010b04c17e8ce1, em work\\cunhagens_13out): «a luz tem autovetor a inscrição do um absoluto que é na essência ela mesma, ou seja, identidade o um absoluto inscrito é a identidade da luz, por isso o par, inclusive dela mesma, sem par somente o zero absoluto que é o abstrato inominado»."),
    ("* `B0_no_eigen`: em UMA particula, o unico autovetor do boost e o zero — o abstrato inominado, sem par.",
     "* `B0_no_eigen`: em UMA particula nenhum vetor nao nulo e autovetor do boost (so o zero satisfaz a condicao) — sem par, o que resta e o zero, o abstrato inominado."),
    ("/-- em uma particula, sem par: o unico autovetor do boost e o zero, o abstrato inominado (apelido de `B0_no_eigen`, PAGO\npela bancada). -/",
     "/-- em uma particula, sem par: nenhum vetor nao nulo e autovetor do boost; so o zero satisfaz a condicao — o abstrato inominado (apelido de `B0_no_eigen`, PAGO\npela bancada). -/"),
], "um_inscrito")
# ---------------------------------------------------------------- (4) OIgual e APonteDoAtrito (fontes): citacoes exatas
troca(W / "rota_RE_dualidade_02nov" / "OIgualCandidata.lean", [
    ("«agora o K me pareceu fazer a função do próprio gráviton (que antes eu disse ser o operador \"=\", aquele que criva)»",
     "«É isso mesmo, mas agora o K me pareceu fazer a função do próprio gráviton ( que antes eu disse ser o operador “=“, aquele que criva)» (02/11/2026, verbatim sha16 1c05c03070544839, em work\\cunhagens_13out)"),
], "o_igual")
troca(W / "beta_calor_02nov" / "APonteDoAtritoCandidata.lean", [
    ("Pergunta do operador (02/11/2026): «Consegue derivar a ponte agora?» — a ponte atrito → temperatura da cadeia dele\n"
     "«tensao → atrito → temperatura → magnetismo» (registrada em `MassaTensaoPura`), com a leitura dele:\n"
     "«[parcela que mantem o balanco fechado a cada observacao ciclica] = equilibrio … o atrito constante gera a viscosidade,\n"
     "que impede o zero absoluto, porque seu efeito e calor e isso fractaliza o Um absoluto pelo decaimento de seu expoente».",
     "Pergunta do operador (02/11/2026, verbatim sha16 e36df7f1245c7f16, em work\\cunhagens_13out): «Consegue derivar a ponte agora?» — a ponte atrito → temperatura da cadeia dele,\n"
     "tensao → atrito → temperatura → magnetismo (registrada em `MassaTensaoPura`, sem aspas: e a sequencia, nao uma frase dele), com a leitura dele, verbatim:\n"
     "«[parcela que mantém o balanço fechado a cada observação cíclica]=equilíbrio» e «o Atrito constante gera a viscosidade, que impede o zero absoluto, porque seu efeito é calor e isso\n"
     "fractaliza o Um absoluto pelo decaimento de seu expoente»."),
], "ponte_do_atrito")
NOVO_SHA_PSION = sha16(P3 / "PsionCantoR1.lean"); print("sha16 novo da fonte PsionCantoR1:", NOVO_SHA_PSION)
# ---------------------------------------------------------------- (5) delta_v407.py
troca(V7 / "delta_v407.py", [
    ('"sha16_da_ordem": "ae74b8334c3c0c8e", "theorem": ANCORA_LEMA', '"sha16_da_ordem": "%s", "theorem": ANCORA_LEMA' % NOVO_SHA_PSION),
    ("a chave linked_to_the_corner_by_a_lemma le True nesse sentido e SO' nesse\",",
     "a chave linked_to_the_corner_by_a_lemma le True nesse sentido e SO' nesse; o resultado sob compressao decorre de Omega ser fixo pela luz e de o canto ser projecao de posto 1 (vale para qualquer vetor unitario fixo pelo fluxo); o lema NAO relaciona as duas faces por uma aplicacao entre os espacos\","),
    ("o texto do ACOM/INPI de 2025 («psi+ psi- cancelado = vacuo») e a frase da Fronteira de 02/2026 («|G> como produto nao emaranhado») ficam superados pela cunhagem de 03/11/2026 (E19), nao reescritos\",",
     "o texto do ACOM/INPI de 2025 (que dava o par psi+ psi- como cancelado, igual ao vacuo) e a frase da Fronteira de 02/2026 (que dava |G> como produto nao emaranhado), ambos resumidos pelo agente de leitura do acervo [DECLARADO], ficam superados pela cunhagem de 03/11/2026 (E19), nao reescritos\","),
    ("AChaveDaGuarda, OGuarda, LeituraPreservada e OIgual NAO tiveram revisao de terceiro ate' esta preparacao;",
     "as nove pedras foram relidas inteiras pelo revisor de terceiro desta preparacao em 03/11/2026 (R1 do Sonnet: 0 alto, 0 medio, 9 baixo; as correcoes da gerencia foram a R2);"),
    ("pela opcao (c) do operador o teste so' entra no um.py se tiver poder\",",
     "pela opcao (c) do operador o teste so' entra no um.py se tiver poder; os dois intervalos ficam ABAIXO de 5 sigma: parede medida, nao falsificacao; por (c) o resultado nao entra; entra so' a citacao do pre-registro\","),
    ("o texto do ACOM/INPI de 2025 («psi+ psi- cancelado = vacuo», o graviton = psi+ psi+) e a frase da Fronteira de 02/2026 («|G> como produto nao emaranhado») ficam SUPERADOS",
     "o texto do ACOM/INPI de 2025 (que dava o par psi+ psi- como cancelado, igual ao vacuo, e o graviton como psi+ psi+) e a frase da Fronteira de 02/2026 (que dava |G> como produto nao emaranhado), resumidos pelo agente de leitura [DECLARADO], ficam SUPERADOS"),
], "delta")
troca(V7 / "preparar_bundle_v407_03nov.py", [
    ('"tipo": "03nov_nome_aceito", "sha16_da_ordem": "ae74b8334c3c0c8e"}', '"tipo": "03nov_nome_aceito", "sha16_da_ordem": "%s"}   # R2 da gerencia (03/11, 15h): fonte corrigida (BAIXOS 3, 6, 8)' % NOVO_SHA_PSION),
], "bundle")
# ---------------------------------------------------------------- (6) runtime c16
troca(V7 / "runtime_v407.py", [
    ('{"id": "c16", "descricao": "o teste (d) so\' consta por CITACAO do pre-registro V1.1 (manifesto pinado por sha256; nenhum resultado no um.py)", "ok": td_.get("so_citado") is True and td_.get("resultado_no_um_py") is None and fd_.get("sha256") == td_["manifesto_sha256"] and td_["manifesto_sha256"].startswith(td_["manifesto_sha16"])},',
     '{"id": "c16", "descricao": "o teste (d) so\' consta por CITACAO do pre-registro V1.1 (manifesto pinado por sha256); nenhum resultado no um.py: nenhuma chave do core com conjunto_d, teste_d_ ou ramo_b_resultado/veredito", "ok": td_.get("so_citado") is True and td_.get("resultado_no_um_py") is None and fd_.get("sha256") == td_["manifesto_sha256"] and td_["manifesto_sha256"].startswith(td_["manifesto_sha16"]) and not any(("conjunto_d" in str(k_).lower() or "teste_d_" in str(k_).lower() or ("ramo_b" in str(k_).lower() and ("resultado" in str(k_).lower() or "veredito" in str(k_).lower()))) for k_ in core_)},'),
], "runtime")
# ---------------------------------------------------------------- (7) gerar_candidato: o reading da testemunha ramifica pela chave lida
GC = V7 / "gerar_candidato_v407.py"; s_gc = GC.read_text(encoding="utf-8")
ANC = 'replace_unique(OLD_TE, NEW_TE, "C19_testemunha_linked_vira_leitura", "G_CHAVES",'
assert s_gc.count(ANC) == 1
troca(GC, [
    (ANC,
     'OLD_RD = \'             "reading": ("the Fock face of the psion (psion C = C.Omega, fixed by the light) is a statement for every Fock certificate, declared in the Psibit module; since v406\'\n'
     'NEW_RD = \'             "reading": (("since v407 the lemma of the two faces is a term of the kernel of the rite (TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces; a link of structure, not of vectors; errata E18): the sentence that follows is the reading of v396 to v406, kept as record: " if _v407_elo_lido(kf_) else "") + "the Fock face of the psion (psion C = C.Omega, fixed by the light) is a statement for every Fock certificate, declared in the Psibit module; since v406\'\n'
     'replace_unique(OLD_RD, NEW_RD, "C19b_testemunha_reading_ramifica", "G_CHAVES", "testemunha_estatica_v396: o campo fock_face.reading ramifica pela chave lida (v407: o lema e\' termo; a frase antiga fica como registro de v396-v406). BAIXO 4 da R1.")\n'
     + ANC),
], "gerar_candidato")
# ---------------------------------------------------------------- (8) artigos
troca(V7 / "artigo_pt_v407.pysnip", [
    ("O Um inscrito é o único vetor \\emph{fixo} da luz sob a hipótese nomeada; autovetor com fase não é excluído por termo.",
     "O Um inscrito é o único vetor \\emph{fixo} da luz no Fock concreto, com $B_0$ lido como o boost da luz [KNOWN, a conferir]; autovetor com fase não é excluído por termo; «Um inscrito = vácuo» é leitura do operador [ONTO]."),
    ("o que o kernel entrega é a validade desses termos, não um teste com a natureza.\")",
     "o que o kernel entrega é a validade desses termos, não um teste com a natureza. \\textsf{[REAL, escopo]} O resultado decorre de $\\Omega$ ser fixo pela luz e de o canto ser projeção de posto~1: vale para qualquer vetor unitário fixo pelo fluxo; o lema não relaciona as duas faces por uma aplicação entre os espaços.\")"),
    ("nenhum resultado, nenhuma execução em dado real. O app e o contrato do JEV",
     "nenhum resultado, nenhuma execução em dado real. O poder de planejamento (3,7 a 3,9$\\sigma$ com dez eventos; 2,1 a 3,2$\\sigma$ com a incerteza do viés do aparelho) fica abaixo de $5\\sigma$: parede medida, não falsificação. O app e o contrato do JEV"),
    ("as outras quatro não tiveram revisão de terceiro até esta preparação.\")",
     "as nove foram relidas inteiras pelo revisor de terceiro desta preparação em 03/11 (R1: 0 alto, 0 médio, 9 baixo; as correções da gerência foram à R2).\")"),
], "artigo_pt")
troca(V7 / "artigo_en_v407.pysnip", [
    ("The inscribed One is the only \\emph{fixed} vector of the light under the named hypothesis; an eigenvector with a phase is not excluded by a term.",
     "The inscribed One is the only \\emph{fixed} vector of the light in the concrete Fock space, with $B_0$ read as the boost of the light [KNOWN, to be checked]; an eigenvector with a phase is not excluded by a term; ``inscribed One = vacuum'' is the operator's reading [ONTO]."),
    ("what the kernel delivers is the validity of those terms, not a test against nature.\")",
     "what the kernel delivers is the validity of those terms, not a test against nature. \\textsf{[REAL, scope]} The result follows from $\\Omega$ being fixed by the light and from the corner being a rank-one projection: it holds for any unit vector fixed by the flow; the lemma does not relate the two faces by a map between the spaces.\")"),
    ("no result, no run on real data. The app and the JEV contract",
     "no result, no run on real data. The planning power (3.7 to 3.9$\\sigma$ with ten events; 2.1 to 3.2$\\sigma$ with the uncertainty of the apparatus bias) stays below $5\\sigma$: a measured wall, not a falsification. The app and the JEV contract"),
    ("the other four had no third-party review up to this preparation.\")",
     "all nine were re-read in full by the third-party reviewer of this preparation on 03/11 (R1: 0 high, 0 medium, 9 low; the management's corrections went to R2).\")"),
], "artigo_en")
# ---------------------------------------------------------------- (9) orquestrador s1b: arquivos_revisados contra o disco
troca(V7 / "orquestrador" / "pos_treino_v407.py", [
    ('            if j.get("aprovada") is True and j.get("candidato_sha16") == cand:\n'
     '                marcar(e, "S1b_revisao", True, sha16=sha16(REV), revisor=j.get("revisor"), candidato=cand, ressalvas=j.get("ressalvas")); return True\n',
     '            ruins = [k for k, v in (j.get("arquivos_revisados") or {}).items() if (PK / k).is_file() and sha16(PK / k) != v]   # [R2, 03/11] BAIXO 9: os arquivos revisados (pos_rito, orquestrador...) tem de ser os do disco\n'
     '            if j.get("aprovada") is True and j.get("candidato_sha16") == cand and not ruins:\n'
     '                marcar(e, "S1b_revisao", True, sha16=sha16(REV), revisor=j.get("revisor"), candidato=cand, ressalvas=j.get("ressalvas"), arquivos_revisados=len(j.get("arquivos_revisados") or {})); return True\n'
     '            if ruins:\n'
     '                log("S1b: %d arquivo(s) revisado(s) mudaram depois da revisao (ex.: %s): a revisao nao vale para eles" % (len(ruins), ruins[:3]))\n'),
], "orquestrador")
# ---------------------------------------------------------------- (10) duraveis das pedras alteradas saem do caminho do preparar_bundle
ANT = V7 / "pedra" / ("antes_de_%s_r2" % TS); ANT.mkdir(parents=True, exist_ok=True); (ANT / "origem").mkdir(exist_ok=True)
for nome, src in (("PsionCanto", "PsionCantoR1.lean"), ("Par", "OParDePsionsR1.lean"), ("OUmInscrito", "OUmInscritoCandidata.lean"), ("OIgual", "OIgualCandidata.lean"), ("APonteDoAtrito", "APonteDoAtritoCandidata.lean")):
    for p in (V7 / "pedra" / ("%s.lean" % nome), V7 / "pedra" / "origem" / src):
        if p.exists():
            shutil.move(str(p), str(ANT / ("origem" if p.parent.name == "origem" else "") / p.name)); LOG.append("movido: %s -> %s" % (p.name, ANT.name))
print("\n".join(LOG[-10:]))
Path(V7 / ("CORRECOES_R2_%s.txt" % TS)).write_text("\n".join(LOG) + "\nsha16 novo PsionCantoR1.lean: %s\n" % NOVO_SHA_PSION, encoding="utf-8")
print("OK: correcoes R2 aplicadas; proximo: preparar_bundle_v407_03nov.py")
