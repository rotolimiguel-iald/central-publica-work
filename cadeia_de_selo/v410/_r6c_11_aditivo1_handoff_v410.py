# -*- coding: utf-8 -*-
"""_r6c_11_aditivo1_handoff_v410.py -- ADITIVO 1 a ordem do conserto unico (gerencia c1, 10/11/2026; a custodia da v410 e' automatica), parte A, FORA do candidato: no gerador do handoff
(pos_rito\\textos_custodia_handoff_v410.py), dentro da secao «README: o que fica evidente», depois do README_EVIDENTE, os dois blocos novos, que passam pelas MESMAS guardas e pelo portao do G1 que os sete textos:
 A1. README_FRENTE: o texto PRONTO, EN e depois PT, para a frente do README do espelho; as formas ratificadas entram SO' pelas constantes que o gerador ja' tem (D81_EN, D81_PT, CLAY_EN, CLAY_PT, UMH_EN, UMH_PT, OBR_EN, OBR_PT);
     os conectores literais sao os da ordem, letra por letra; as tres frases da escala foram conferidas contra os enunciados da pedra R6 (sem_escala_nao_ha_fita; a_constante_da_luz_e_a_escala_do_tempo; o_nome_e_a_singularidade_da_informacao);
 A2. README_O_QUE_SAI: o texto literal da ordem.
Os dois vao ao handoff entre marcadores proprios (README_FRENTE_v410 e README_O_QUE_SAI_v410; o parser do G1 so' publica os PARAGRAFO_*), sao relidos pelo parser do G1 e conferidos contra o escrito, e o recibo do S6d
(RECIBO_TEXTOS_CUSTODIA_HANDOFF_v410.json) ganha os dois textos e os bytes do README_FRENTE rendido em UTF-8. Idempotente; backup de BYTES; CRLF como o arquivo; temporario + os.replace; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")
p = os.path.join(HERE, "pos_rito", "textos_custodia_handoff_v410.py"); b0 = open(p, "rb").read(); t = b0.decode("utf-8")
assert t.count("\r\n") == t.count("\n") > 0, "o gerador do handoff deixou de ser CRLF"
t = t.replace("\r\n", "\n"); log = []


def tr(a, b, n=1):
    global t
    c = t.count(a)
    if c == 0 and b in t:
        log.append("ja' feito: " + a[:50]); return
    assert c == n, ("contagem", c, "esperado", n, a[:140])
    t = t.replace(a, b); log.append("trocado x%d: %s" % (c, a[:50]))


BLOCO = r'''# ------------------------------------------------------------------ (ADITIVO 1 a ordem do conserto unico, gerencia c1, 10/11/2026: a custodia da v410 e' automatica) os DOIS BLOCOS do README, dentro da secao «README: o que fica evidente», depois do README_EVIDENTE
# README_FRENTE: o texto PRONTO, EN e depois PT, para a frente do README do espelho, no lugar do bloco de hoje «P = nP — a theorem in the kernel» (v408–v409). As formas ratificadas entram SO' pelas constantes (D81, a forma canonica do Clay, o habitante unico, a obrigacao do H0DN);
# os conectores sao os da ordem, letra por letra. As tres frases da escala sao os tres fatos da FRASE_ESCALA_UMA sem o limiar (por isso o bloco NAO anuncia limiar e nao leva a clausula do limite); conferidas contra os enunciados da pedra R6:
# sem_escala_nao_ha_fita (com [Nonempty X]: para todo k e t, leitorComConstante 0 k t = 1; e leituraComConstante 0 cc s = 1 para toda instancia cc); a_constante_da_luz_e_a_escala_do_tempo (leitorComConstante c k s = leitorComConstante 1 k (c * s) = iald.brilho k (c * s));
# o_nome_e_a_singularidade_da_informacao ((∃! x, P x) ↔ ∃ a, ∀ x, (P x ↔ x = a)). A linha «Start here · comece aqui» do README de hoje fica como esta' (e' da custodia).
README_FRENTE = ("## P = nP and the Clay question, in the kernel · no kernel `[PROVED = validity · v408–v410]`\n\n"
                 "**P = nP of Turing, in the form of D81:** " + D81_EN + ".\n\n"
                 "**The Clay question, in the canonical form:** " + CLAY_EN + "\n\n"
                 "**The scope, said with it:** " + UMH_EN + ".\n\n"
                 "**The scale (v410, `TGLExt.AEscala`), three theorems of the kernel, kernel validity and not creditation:** with the constant of the scale equal to 0 every pixel has brightness 1 at every time and, given at least one pixel, every instance reads 1 (`sem_escala_nao_ha_fita`); "
                 "the reader of constant c at the time s is the reader of constant 1, the IALD, at the time c·s (`a_constante_da_luz_e_a_escala_do_tempo`); and a property holds of exactly one thing if and only if holding it is being one designated thing (`o_nome_e_a_singularidade_da_informacao`). The names were given or ratified by the operator.\n\n"
                 "**The H0DN × BG1 test:** " + OBR_EN + "; it was not opened: the power certificate was refused (declared by the executor, read by the management), a test without discriminating predictive power is not opened, and the opening belongs to a future version.\n\n"
                 "*PT — " + D81_PT + ". " + CLAY_PT + " " + UMH_PT + ". A escala (v410, `TGLExt.AEscala`; teoremas do kernel: validade, não creditação): com a constante da escala igual a 0 todo pixel brilha 1 em todo tempo e, havendo ao menos um pixel, toda instância lê 1 (`sem_escala_nao_ha_fita`); "
                 "o leitor de constante c no tempo s é o leitor de constante 1, a IALD, no tempo c·s (`a_constante_da_luz_e_a_escala_do_tempo`); e uma propriedade vale de exatamente uma coisa se e só se tê-la é ser uma coisa designada (`o_nome_e_a_singularidade_da_informacao`); os nomes foram dados ou ratificados pelo operador. "
                 "O teste H0DN × BG1: " + OBR_PT + "; não foi aberto: o certificado de poder foi recusado (declarado pelo executor, lido pela gerência), teste sem poder preditivo discriminante não se abre, e a abertura é de versão futura.*")
# README_O_QUE_SAI: o texto LITERAL da ordem (o que sai do README para caber no teto; decisao estrutural da gerencia c1)
README_O_QUE_SAI = ("**O que sai do README para caber no teto de 40.960 bytes (L01): decisão estrutural da gerência c1, de 10/11/2026.** (1) O bloco de hoje “P = nP — a theorem in the kernel” é SUBSTITUÍDO pelo bloco pronto acima; a linha “Start here · comece aqui” fica. "
                    "(2) A seção “Abstract” SAI da frente do README e vai, por cópia de bytes, para `ABSTRACT.md` na raiz do espelho (a origem dela é o livro-razão, que não muda); no README fica o título com uma linha de ponteiro para o arquivo; com ela sai a nota “Read the Abstract below under the current ruler” do bloco “What changed in this version”. "
                    "(3) Se ainda assim o README passar do teto, sai “Citing This Work” inteiro para o `CITING.md`, ficando uma linha de ponteiro. Fora disso a custódia não corta nada sem voltar à gerência. Precedente: em 06/11 o BibTeX saiu do README para o `CITING.md`. A porta da raiz ganha o arquivo novo, por script.")
README_BLOCOS = [("README_FRENTE", README_FRENTE), ("README_O_QUE_SAI", README_O_QUE_SAI)]
_RF_NOMES = ("sem_escala_nao_ha_fita", "a_constante_da_luz_e_a_escala_do_tempo", "o_nome_e_a_singularidade_da_informacao")
assert all(x_ in README_FRENTE for x_ in (D81_EN, D81_PT, CLAY_EN, CLAY_PT, UMH_EN, UMH_PT, OBR_EN, OBR_PT)), "o README_FRENTE nao traz uma das formas ratificadas pela constante"
assert set(_RF_NOMES) <= set(DL.NOMES_RATIFICADOS_R6_AESCALA) and all(README_FRENTE.count("`" + n_ + "`") == 2 for n_ in _RF_NOMES), "os tres teoremas da escala do README_FRENTE nao sao nomes da secao 7 ratificados pelo operador (ou nao estao uma vez no EN e uma no PT)"
assert not re.search(r"limiar|threshold|ln 2", README_FRENTE) and DL.CLAUSULA_Z_PT not in README_FRENTE and DL.CLAUSULA_Z_EN not in README_FRENTE, "o README_FRENTE nao anuncia limiar (por isso nao leva a clausula do limite)"
assert README_FRENTE.startswith("## P = nP and the Clay question, in the kernel") and README_FRENTE.count("\n\n") == 6 and README_FRENTE.endswith("versão futura.*") and "%" not in README_FRENTE, "o README_FRENTE mudou de forma (titulo, cinco paragrafos em ingles e o paragrafo em portugues)"
assert README_O_QUE_SAI.startswith("**O que sai do README para caber no teto de 40.960 bytes (L01)") and all(x_ in README_O_QUE_SAI for x_ in ("`ABSTRACT.md`", "`CITING.md`", "(1) ", "(2) ", "(3) ")), "o README_O_QUE_SAI mudou de forma"


def montar_blocos(textos, readme_evidente, readme_blocos, v):
    """O que vai ao handoff, depois do cabecalho: os sete textos, cada um entre os seus marcadores; a secao README (D85), em paragrafo proprio; e, DENTRO dela, depois do README_EVIDENTE, os dois blocos do README (ADITIVO 1), cada um entre os seus marcadores."""
    marc_ = lambda i_, t_: "\n<!-- INICIO_%s_%s -->\n%s\n<!-- FIM_%s_%s -->\n" % (i_, v, t_, i_, v)
    return "".join(marc_(i_, t_) for i_, t_ in textos) + "\n" + readme_evidente + "\n" + "".join(marc_(i_, t_) for i_, t_ in readme_blocos)


'''
ANC_TEXTOS = 'TEXTOS = [("TITULO_EN", TITULO_EN), ("ENTROU_EN", ENTROU_EN), ("KERNEL_LEITURA_EN", KERNEL_LEITURA_EN), ("ABERTOS_EN", ABERTOS_EN), ("ARCO_EN", ARCO_EN), ("ARCO_PT", ARCO_PT), ("COMMIT", COMMIT)]\n'
if "README_FRENTE = (" not in t:
    assert t.count(ANC_TEXTOS) == 1
    t = t.replace(ANC_TEXTOS, ANC_TEXTOS + BLOCO); log.append("os dois blocos e montar_blocos acrescentados depois de TEXTOS")
tr('guardas, falhas = guardas_dos_textos(TEXTOS + [("README_EVIDENTE", README_EVIDENTE)], conhecidos)', 'guardas, falhas = guardas_dos_textos(TEXTOS + [("README_EVIDENTE", README_EVIDENTE)] + README_BLOCOS, conhecidos)   # (ADITIVO 1) os dois blocos do README passam pelas MESMAS guardas e pelo portao do G1')
tr('for ident, _ in TEXTOS:\n    assert ("INICIO_%s_%s" % (ident, V)) not in h_txt, "marcador %s ja existe no handoff" % ident', 'for ident, _ in TEXTOS + README_BLOCOS:\n    assert ("INICIO_%s_%s" % (ident, V)) not in h_txt, "marcador %s ja existe no handoff" % ident')
tr('print("guardas: os sete textos e a secao README (D85) passaram (guarda de frases v410, portao do G1, forma do ARCO/COMMIT, sem 4,44, D59, D65)")',
   'print("guardas: os sete textos, a secao README (D85) e os dois blocos do README (README_FRENTE, %d bytes em UTF-8; README_O_QUE_SAI) passaram (guarda de frases v410, portao do G1, forma do ARCO/COMMIT, sem 4,44, D59, D65)" % len(README_FRENTE.encode("utf-8")))')
tr('blocos = "".join("\\n<!-- INICIO_%s_%s -->\\n%s\\n<!-- FIM_%s_%s -->\\n" % (i, V, t, i, V) for i, t in TEXTOS) + "\\n" + README_EVIDENTE + "\\n"', 'blocos = montar_blocos(TEXTOS, README_EVIDENTE, README_BLOCOS, V)')
tr('assert h.o_que_e and h.o_que_e.pin16 == PIN and h.o_que_e.versao == V, "o «O que é» do handoff deixou de ser lido"',
   'assert h.o_que_e and h.o_que_e.pin16 == PIN and h.o_que_e.versao == V, "o «O que é» do handoff deixou de ser lido"\n'
   'for i, t in README_BLOCOS:   # (ADITIVO 1) os dois blocos do README, relidos entre os marcadores pelo parser do G1: iguais aos escritos\n'
   '    assert h.corpos.get("%s_%s" % (i, V), "").strip("\\n") == t, "bloco do README lido difere do escrito: " + i\n'
   'assert "**README: o que fica evidente**" in hpath.read_text(encoding="utf-8"), "a secao README (D85) nao esta\' no handoff"\n'
   'print("parser do G1: os dois blocos do README lidos entre os marcadores, iguais aos escritos; README_FRENTE: %d bytes em UTF-8, sha256 %s" % (len(README_FRENTE.encode("utf-8")), hashlib.sha256(README_FRENTE.encode("utf-8")).hexdigest()))')
tr('"textos": dict(TEXTOS), "readme_evidente": README_EVIDENTE, "guardas": guardas,',
   '"textos": dict(TEXTOS), "readme_evidente": README_EVIDENTE, "readme_frente": README_FRENTE, "readme_frente_bytes_utf8": len(README_FRENTE.encode("utf-8")), "readme_frente_sha256": hashlib.sha256(README_FRENTE.encode("utf-8")).hexdigest(), "readme_o_que_sai": README_O_QUE_SAI, "guardas": guardas,')
ast.parse(t)
b1 = t.replace("\n", "\r\n").encode("utf-8")
if b1 != b0:
    bak = p + ".bak_" + TS + "_aditivo1"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
    tmp = p + ".tmp_r6c"; open(tmp, "wb").write(b1); assert os.path.getsize(tmp) == len(b1) > len(b0); os.replace(tmp, p); assert open(p, "rb").read() == b1
print("pos_rito/textos_custodia_handoff_v410.py:", "MUDOU" if b1 != b0 else "igual", log)
