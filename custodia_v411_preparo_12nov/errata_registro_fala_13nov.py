# -*- coding: utf-8 -*-
"""A frase do autor de 02/11 CITADA no REGISTRO_FASE9_V2.md (13/11/2026, claude-site-custodia; decisão da gerência c1 de 12/11, opção (b)).

A regra do operador de 12/11/2026 (verbatim em work\\cunhagens_13out, sha16 lido do disco em runtime): conversa entre os autores não se
transcreve no programa nem no artigo; cita-se por data e sha256. O REGISTRO_FASE9_V2.md nasce na custódia da v411, logo a regra vale para ele.
Edição por bytes de UM arquivo, readme_pinado.py (LF):
  - registro_fase9_v2 passa a usar _hubble_pt_registro (o b_hubble_pt com a linha da fala trocada pela citação por data e sha16);
    b_hubble_pt fica INTACTA; a linha PT dos números fica igual;
  - o cabeçalho do registro deixa de dizer «verbatim»: igual, exceto a frase do autor, citada pela regra de 12/11 (sha16 do arquivo dela);
  - o portão do registro no --gerar conhece o sha16 da regra (lido do disco por _regra_fala).
Backup de bytes antes de tocar; gravação por temporário; compilação conferida; o arquivo tem de crescer.
Uso: python -X utf8 errata_registro_fala_13nov.py [PASTA_DA_G1]   (padrão: a G1 real; o ensaio passa uma cópia)
SÓ DEPOIS DO HANDOFF DA v411 (congelamento C-06 da gerência c1 até lá)."""
import os, sys, time

G1 = sys.argv[1] if len(sys.argv) > 1 else r"C:\IALD\Central de Patentes\tools\custodia_g1"
STAMP = time.strftime("%Y%m%d_%H%M%S")

VELHO_REG = r'''def registro_fase9_v2(C):
    """O painel inteiro da Fase 9 V2 e a frase do autor de 02/11, como estiveram no topo do README (as MESMAS funcoes, os MESMOS itens do PRIMORDIAL)."""
    s = b_primordial(C)
    if s.count(_ANCORA_HUBBLE) != 1:
        raise Falha("H0DN aberto: a ancora do painel da Fase 9 V2 nao esta uma vez no b_primordial")
    hub = "> **Hubble-ratio test**" + s[s.index(_ANCORA_HUBBLE) + len(_ANCORA_HUBBLE):]
    return ("# Record \u00b7 registro: the Phase 9 V2 panel (Hubble ratio, opened once on %s)\n\n"
            "<!-- PINADO por tools/custodia_g1/readme_pinado.py \u00b7 fonte PRIMORDIAL.json sha16 %s \u00b7 pino PINO_README.json \u00b7 n\u00e3o editar \u00e0 m\u00e3o -->\n\n"
            "*This panel stood at the top of the README until the custody of %s, when the H0DN \u00d7 BG1 test, opened once (registry `%s`), took the top; "
            "it moved here verbatim, from the same generator and the same PRIMORDIAL items. It stays true about that test.*\n\n"
            % (C.v("hubble.data_abertura"), C.prim_sha16, C.v("selo.versao"), C.v("h0dn.registro")) + hub + "\n" + b_hubble_pt(C))
'''

NOVO_REG = r'''# AO LADO (13/11/2026, claude-site-custodia; decisao da gerencia c1 de 12/11, opcao (b)): a regra do operador de 12/11/2026 (conversa entre os
# autores nao se transcreve no programa nem no artigo; cita-se por data e sha256) vale para o que se escreve de novo, e este registro nasce na
# custodia da v411. A frase do autor de 02/11 entra CITADA por data e sha16, nao transcrita; b_hubble_pt fica INTACTA (o caminho sem o H0DN
# aberto e o registro do que foi publicado); a linha PT dos numeros da Fase 9 V2 fica igual, com todos os companheiros do z_disc; o cabecalho
# deixa de dizer verbatim. Sem o arquivo da regra em disco, ou sem a frase uma vez no fim do b_hubble_pt, PARA (nunca a transcricao como saida).
# A funcao anterior (que descia o painel verbatim COM a frase, de acordo da gerencia de 12/11 anterior a regra) fica no backup .bak_*_registro_fala.
REGRA_FALA_12NOV = ("OPERADOR_12nov_nao_precisa_transcrever_esse_tipo_de_fala_pra_dentro_do_programa_nunca_verbatim.txt", "12/11/2026")


def _regra_fala():
    """(data, sha16) da regra do operador de 12/11/2026, o sha16 lido do arquivo verbatim em disco (nunca de memoria)."""
    p = Path(Caminhos().CEN) / "work" / "cunhagens_13out" / REGRA_FALA_12NOV[0]
    if not p.is_file():
        raise Falha("a regra do operador de %s (nao transcrever fala dos autores) nao esta em disco: %s" % (REGRA_FALA_12NOV[1], p))
    return REGRA_FALA_12NOV[1], hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def _hubble_pt_registro(C):
    """O b_hubble_pt com a linha da frase do autor de 02/11 trocada pela citacao por data e sha16; o resto, byte a byte."""
    s = b_hubble_pt(C)
    fala = ("> *\u00ab%s\u00bb* \u2014 the author, %s (verbatim, sha16 `%s`) `[INPUT: the author\u2019s judgement, not a claim of the program]`\n"
            % (C.v("operador.frase_4_44_sic"), C.v("operador.data"), C.f("operador_verbatim", "sha16")))
    if s.count(fala) != 1 or not s.endswith(fala):
        raise Falha("H0DN aberto: a frase do autor de 02/11 nao esta uma vez, no fim, do b_hubble_pt (o registro nao se monta)")
    cit = ("> *The author\u2019s judgement of %s on this result is cited by date and sha256, not transcribed (verbatim file sha16 `%s`).* "
           "`[INPUT: the author\u2019s judgement, not a claim of the program]`\n" % (C.v("operador.data"), C.f("operador_verbatim", "sha16")))
    return s[:-len(fala)] + cit


def registro_fase9_v2(C):
    """O painel inteiro da Fase 9 V2, como esteve no topo do README (as MESMAS funcoes, os MESMOS itens do PRIMORDIAL), exceto a frase do autor de 02/11, citada por data e sha16."""
    s = b_primordial(C)
    if s.count(_ANCORA_HUBBLE) != 1:
        raise Falha("H0DN aberto: a ancora do painel da Fase 9 V2 nao esta uma vez no b_primordial")
    hub = "> **Hubble-ratio test**" + s[s.index(_ANCORA_HUBBLE) + len(_ANCORA_HUBBLE):]
    d_regra, sha_regra = _regra_fala()
    return ("# Record \u00b7 registro: the Phase 9 V2 panel (Hubble ratio, opened once on %s)\n\n"
            "<!-- PINADO por tools/custodia_g1/readme_pinado.py \u00b7 fonte PRIMORDIAL.json sha16 %s \u00b7 pino PINO_README.json \u00b7 n\u00e3o editar \u00e0 m\u00e3o -->\n\n"
            "*This panel stood at the top of the README until the custody of %s, when the H0DN \u00d7 BG1 test, opened once (registry `%s`), took the top; "
            "it moved here from the same generator and the same PRIMORDIAL items, unchanged except for the author\u2019s sentence of %s, which is now cited "
            "by date and sha256 instead of transcribed, under the author\u2019s rule of %s (verbatim file sha16 `%s`). It stays true about that test.*\n\n"
            % (C.v("hubble.data_abertura"), C.prim_sha16, C.v("selo.versao"), C.v("h0dn.registro"), C.v("operador.data"), d_regra, sha_regra)
            + hub + "\n" + _hubble_pt_registro(C))
'''

VELHO_PORTAO = r'''        viol_h = textos.portao(_neutraliza(reg_txt), conhecidos_de(prim_bytes.decode("utf-8")) | {C.prim_sha16}, rotulo=REGISTRO_FASE9_V2) + regra_444(reg_txt, C.P)
'''
NOVO_PORTAO = r'''        # AO LADO (13/11/2026, claude-site-custodia; decisao da gerencia c1): o sha16 da regra de 12/11, citado no cabecalho do registro, lido do disco
        viol_h = textos.portao(_neutraliza(reg_txt), conhecidos_de(prim_bytes.decode("utf-8")) | {C.prim_sha16, _regra_fala()[1]}, rotulo=REGISTRO_FASE9_V2) + regra_444(reg_txt, C.P)
'''

README = [(VELHO_REG, NOVO_REG), (VELHO_PORTAO, NOVO_PORTAO)]


def aplicar(nome, eds):
    P = os.path.join(G1, nome)
    b = open(P, "rb").read()
    assert b.count(b"\r\n") == 0, "fim de linha inesperado em %s (o readme_pinado.py e LF)" % nome
    pares = [(a.encode("utf-8"), d.encode("utf-8")) for a, d in eds]
    for a, _ in pares:
        assert b.count(a) == 1, "o trecho mudou em %s - PARAR: %r" % (nome, a[:90])
    for nec in (b"\nimport hashlib\n", b"Caminhos"):
        assert nec in b, "%s sem %r - PARAR" % (nome, nec)
    bak = P + ".bak_%s_registro_fala" % STAMP
    open(bak, "wb").write(b)
    assert open(bak, "rb").read() == b
    novo = b
    for a, d in pares:
        novo = novo.replace(a, d)
    compile(novo.decode("utf-8"), P, "exec")
    assert novo.count(b"\r\n") == 0, "CRLF entrou em %s" % nome
    t = P + ".tmp_errata"
    open(t, "wb").write(novo)
    assert os.path.getsize(t) == len(novo) > len(b)
    os.replace(t, P)
    print("ok:", nome, len(b), "->", len(novo), "| backup", os.path.basename(bak))


aplicar("readme_pinado.py", README)
