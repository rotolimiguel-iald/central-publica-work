# -*- coding: utf-8 -*-
"""_r6c_04_instrucoes_v410.py -- o CONSERTO UNICO da v410 (ESPEC_CONSERTO_R3_v2_FINAL), as INSTRUCOES que nao sao troca exata e que o construtor cumpre por script, cada uma pelo criterio do item:
 264: os comentarios e docstrings que repetiam a forma velha (runtime_aescala_v410.py: as duas ocorrencias; delta_v410.py: «os dados pela gerencia na R5» e os dois «38 ancoras»), com o texto que o item da';
 293: os quatro moldes de pos_rito/textos_v410.py (o paragrafo dos abertos, as pendencias, o paragrafo curto do README, a ordem de coleta) ganham DL_.FRASE_H0DN_PODER_COM_RETORNO_PT logo depois da oracao da abertura em versao futura,
      com a concatenacao DENTRO do parentese do molde, antes do operador de formato (a cola e' so' pontuacao: «; » onde a oracao termina em ponto e virgula, frase nova com a primeira letra em maiuscula onde termina em ponto);
 133: gerar_relatorio_v410.py: (a) o AVISO proprio do conserto, com o texto do item e os numeros por len(); (b) o AVISO da R1 passa a render o numero da R1 (os nomes novos das R3 e R4, lidos do recibo dos nomes); (c) o comentario velho da ratificacao_pendente;
  50: os dois controles OPCIONAIS: (b) _d108_artigo_ok em conferir_rito_v410.py (a frase da finura na secao A Escala do artigo, formas comparaveis; na v2 a segunda metade vai no artigo pelo nucleo da frase da secao 7, com a clausula do limite na secao);
      (c) em guardas_dos_textos do handoff, o README que traz a forma canonica do Clay traz a frase da finura, PT e EN.
Idempotente; backup de BYTES (<arquivo>.bak_<TS>_r6c4); fim de linha do arquivo (no misto, o da linha vizinha); temporario + os.replace; ast.parse.   uso: python -I -B -X utf8 _r6c_04_instrucoes_v410.py"""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")


class Arq:
    def __init__(self, rel):
        self.rel = rel; self.p = os.path.join(HERE, *rel.split("/")); self.b0 = open(self.p, "rb").read(); self.t = self.b0.decode("utf-8"); self.log = []

    def tr(self, a, b, n=1):
        c = self.t.count(a)
        if c == 0 and b in self.t:
            self.log.append("ja' feito: " + a[:50]); return
        assert c == n, (self.rel, "contagem", c, "esperado", n, a[:140])
        self.t = self.t.replace(a, b); self.log.append("trocado x%d: %s" % (c, a[:50]))

    def eol_depois_de(self, ancora):   # o fim de linha da linha que contem a ancora (para acrescentar linhas num arquivo misto ou CRLF)
        i = self.t.index(ancora); q = self.t.find("\n", i)
        return "\r\n" if (q > 0 and self.t[q - 1] == "\r") else "\n"

    def grava(self):
        b1 = self.t.encode("utf-8")
        if b1 != self.b0:
            ast.parse(self.t.replace("\r\n", "\n"))
            bak = self.p + ".bak_" + TS + "_r6c4"
            if not os.path.exists(bak):
                open(bak, "wb").write(self.b0); assert open(bak, "rb").read() == self.b0
            tmp = self.p + ".tmp_r6c"; open(tmp, "wb").write(b1); assert os.path.getsize(tmp) == len(b1) > 0
            os.replace(tmp, self.p); assert open(self.p, "rb").read() == b1
        print(self.rel + ":", "MUDOU" if b1 != self.b0 else "igual", self.log)


# ---------------------------------------------------------------- 264
A = Arq("runtime_aescala_v410.py")
A.tr("RATIFICADOS em 10/11 (D101), salvo os dois auxiliares da autoria, pendentes", "RATIFICADOS em 10/11 (D101), salvo o quarto teorema da clausula, NOMEADO pelo operador (D108), e os dois auxiliares da autoria, pendentes", n=2)
A.grava()
A = Arq("delta_v410.py")
A.tr("os dados pela gerencia na R5", "os tres apresentados ao operador antes da fala; o quarto, nomeado por ele (D108)")
A.tr("# (D86) as 38 ancoras da AEscala (os #print axioms da fonte)", "# (D86) as ancoras da AEscala (os #print axioms da fonte)")
A.tr("le as 38 ancoras, as bandeiras ext_aescala_410_*", "le as ancoras, as bandeiras ext_aescala_410_*")
A.grava()

# ---------------------------------------------------------------- 293
A = Arq("pos_rito/textos_v410.py"); X = "DL_.FRASE_H0DN_PODER_COM_RETORNO_PT"
if X not in A.t:
    # (1) o paragrafo dos abertos (_depois): os literais adjacentes passam a um grupo entre parenteses, e o operador de formato fica FORA dele
    A.tr('    return ("**O que vem depois destas superfícies:**', '    return (("**O que vem depois destas superfícies:**')
    A.tr('pina por sha256; "\n', 'pina por sha256; " + ' + X + ' + "; "\n')
    A.tr('o gate não se move."\n            % (bk["de"]', 'o gate não se move.")\n            % (bk["de"]')
    # (2) as pendencias (topico_novo): o molde ja' esta' entre parenteses antes do operador
    A.tr('e o vetor observado). Os nomes das declarações', 'e o vetor observado). " + DL_.costura_maiuscula(' + X + ') + ". Os nomes das declarações')
    # (3) o paragrafo curto do README e do site: o literal ganha o parentese proprio, antes do operador
    A.tr('          "> - **O teste H0DN × BG1** [REAL · DERIVED · DECLARADO · INPUT · OPEN]: %s (%s).', '          ("> - **O teste H0DN × BG1** [REAL · DERIVED · DECLARADO · INPUT · OPEN]: %s (%s).')
    A.tr('pode devolvê-la; a palavra do livro de cobranças (NOT_FALSIFIED) vai em campo próprio e nunca é a cabeça nem a palavra da creditação. Decisão do operador, em 09/11: %s." % (DL_.FRASE_H0DN_OBRIGATORIA_PT, DL_.FRASE_H0DN_ALCANCE_PT, hv["n_pinos"]',
         'pode devolvê-la; " + ' + X + ' + "; a palavra do livro de cobranças (NOT_FALSIFIED) vai em campo próprio e nunca é a cabeça nem a palavra da creditação. Decisão do operador, em 09/11: %s.") % (DL_.FRASE_H0DN_OBRIGATORIA_PT, DL_.FRASE_H0DN_ALCANCE_PT, hv["n_pinos"]')
    # (4) a ordem de coleta (secao_h0dn): o molde ja' esta' entre parenteses antes do operador
    A.tr('e o resultado dele é de versão futura. "\n', 'e o resultado dele é de versão futura. " + DL_.costura_maiuscula(' + X + ') + ". "\n')
    assert A.t.count(X) == 4
A.grava()

# ---------------------------------------------------------------- 133
A = Arq("gerar_relatorio_v410.py")
anc = "              % (_DL.ADENDO5_SHA16, _DL.ADENDO6_SHA16, _DL.N_FALAS_V410, len(_DL.NOMES_RATIFICADOS_D101_AESCALA), len(_DL.CAMPOS_RATIFICADOS_D101_AESCALA), len(_DL.NOMES_PENDENTES_AESCALA)))"
if "R6, ADENDO 7 (sha16 %s;" not in A.t:
    assert A.t.count(anc) == 1; e = A.eol_depois_de(anc)
    novo = (anc + e
            + "# (R6; item 133 a da ESPEC do conserto unico) o AVISO proprio do conserto, com os numeros por len()" + e
            + "AVISOS.append(\"R6, ADENDO 7 (sha16 %s; D106 a D109, D113 e D116 a D123; E38, E39 e E40): a revisao de terceiro R3 e o painel nao aprovaram o candidato; conserto unico; a fala da D101 ratifica %d nomes novos (nao 22) e 3 nomes da clausula do Tetelestai (nao 4); "
            + "o quarto teorema foi NOMEADO pelo operador (D108): ressurreicao_do_sinal; a pedra R6 traz a secao 7 (%d declaracoes novas, %d com o nome ratificado pelo operador, D117 e D123); seguem [DECLARADO pela autoria] %d nomes (os auxiliares da R5 e os da secao 7 que nao lhe foram mostrados); "
            + "as falas 29 a 40 entram nas congeladas (%d falas)\"" + e
            + "              % (_DL.ADENDO7_SHA16, len(_DL.NOMES_RATIFICADOS_D101_AESCALA), len(_DL.NOMES_NOVOS_R6_AESCALA), len(_DL.NOMES_RATIFICADOS_R6_AESCALA), len(_DL.NOMES_DECLARADOS_PELA_AUTORIA_AESCALA), _DL.N_FALAS_V410))")
    A.t = A.t.replace(anc, novo); A.log.append("AVISO da R6 acrescentado (fim de linha %r)" % e)
A.tr('_DL.H0DN_ORDEM02["sha256"][:16], len(_DL.NOMES_NOVOS_AESCALA), len(_DL.CAMPOS_NOVOS_AESCALA)))',
     '_DL.H0DN_ORDEM02["sha256"][:16], len(_DL._REC_AESC["nomes_novos_a_ratificar_r3"]) + len(_DL._REC_AESC["nomes_novos_a_ratificar_r4"]), len(_DL.CAMPOS_NOVOS_AESCALA)))   # (item 133 b: o numero e\' o da R1, os nomes novos das R3 e R4, lidos do recibo dos nomes; a frase e\' da R1)')
A.tr("# (R1/D92: os nomes e os campos novos da pedra R3, [DECLARADO], a ratificar pelo operador; os nomes anteriores foram ratificados na D87 («ratifico tudo»))",
     "# (D101 e D106: os dois lemas auxiliares da autoria da R5, [DECLARADO pela autoria]; os nomes novos das R3 e R4, os tres da clausula e os campos foram ratificados em 10/11 (D101); os nomes da secao 7 que seguem da autoria estao em NOMES_DECLARADOS_R6_AESCALA)")
A.grava()

# ---------------------------------------------------------------- 50 (b)
A = Arq("conferir_rito_v410.py")
if "_d108_artigo_ok" not in A.t:
    anc = 'r5_artigo_ok = bool(_r5_artigo_ok("pt") and _r5_artigo_ok("en"))\n'; assert A.t.count(anc) == 1
    A.t = A.t.replace(anc, anc
                      + "\n\ndef _d108_artigo_ok(l_):   # (D108; item 50 b da ESPEC do conserto unico, controle opcional) a frase da finura da leitura na secao A Escala do artigo, formas comparaveis: a primeira metade (o que os enunciados dizem) e, da segunda, o nucleo da frase da secao 7 (que o artigo traz no paragrafo da secao 7), com a clausula do limite na secao\n"
                      + "    sec_ = _secA[l_]; cs_ = DL.comparavel(sec_); pt_ = l_ == \"pt\"\n"
                      + "    return bool(sec_ and DL.comparavel(DL.FRASE_FINURA_REAL_PT if pt_ else DL.FRASE_FINURA_REAL_EN) in cs_ and DL.comparavel(DL.FRASE_ESCALA_UMA_NUCLEO_PT if pt_ else DL.FRASE_ESCALA_UMA_NUCLEO_EN) in cs_ and DL.comparavel(DL.CLAUSULA_Z_PT if pt_ else DL.CLAUSULA_Z_EN) in cs_)\n"
                      + "\n\nd108_artigo_ok = bool(_d108_artigo_ok(\"pt\") and _d108_artigo_ok(\"en\"))\n")
    A.tr("aescala_secao_ok = bool(r2_artigo_ok and r5_artigo_ok and ", "aescala_secao_ok = bool(r2_artigo_ok and r5_artigo_ok and d108_artigo_ok and ")
A.grava()

# ---------------------------------------------------------------- 50 (c)
A = Arq("pos_rito/textos_custodia_handoff_v410.py")
if "sem a frase da finura da leitura" not in A.t:
    anc = '            v3.append("%s: cita o ACOM Mirror sem [PILOTO][SIM] e sem dizer que nada ali valida fisica (D100)" % ident)'; assert A.t.count(anc) == 1; e = A.eol_depois_de(anc)
    A.t = A.t.replace(anc, anc + e
                      + "        if ident == \"README_EVIDENTE\" and CLAY_PT in t and not (FIN_PT in t and FIN_EN in t):   # (D108; item 50 c da ESPEC do conserto unico, controle opcional) o README que traz a forma canonica do Clay traz a frase da finura da leitura, PT e EN" + e
                      + "            v3.append(\"%s: traz a forma canonica do Clay sem a frase da finura da leitura, PT e EN (D108)\" % ident)")
    A.log.append("controle (c) acrescentado (fim de linha %r)" % e)
A.grava()
