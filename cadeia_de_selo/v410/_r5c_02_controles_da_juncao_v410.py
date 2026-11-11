# -*- coding: utf-8 -*-
"""_r5c_02_controles_da_juncao_v410.py -- a REVISAO DO CONSTRUTOR, parte 2 (10/11/2026): a juncao «FRASE (CLAUSULA); RECONSTRUCAO» vira UMA constante do delta (ANUNCIO_TETELESTAI_PT/EN), usada pelo registro e por todos os controles (nada de juncao digitada em dois lugares);
a linha do .md passa a trazer a clausula do limite DUAS vezes (ao lado do limiar de um pixel, D99, e logo depois da clausula de 1 - beta, D100): os controles que exigiam uma ocorrencia passam a exigir as duas e o composto exato. Idempotente; backup de BYTES; temporario + os.replace; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")


class Arq:
    def __init__(self, rel):
        self.rel = rel; self.p = os.path.join(HERE, *rel.split("/")); self.b0 = open(self.p, "rb").read(); self.t = self.b0.decode("utf-8"); self.log = []

    def tr(self, a, b, n=1):
        c = self.t.count(a)
        if c == 0 and b in self.t:
            self.log.append("ja' feito: " + a[:60]); return
        assert c == n, (self.rel, "contagem", c, "esperado", n, a[:140])
        self.t = self.t.replace(a, b); self.log.append("trocado x%d: %s" % (c, a[:60]))

    def grava(self):
        b1 = self.t.encode("utf-8")
        if b1 != self.b0:
            if self.p.endswith(".py"):
                ast.parse(self.t)
            bak = self.p + ".bak_" + TS + "_r5c2"
            if not os.path.exists(bak):
                open(bak, "wb").write(self.b0); assert open(bak, "rb").read() == self.b0
            tmp = self.p + ".tmp_r5c"; open(tmp, "wb").write(b1); assert os.path.getsize(tmp) == len(b1) > 0
            os.replace(tmp, self.p); assert open(self.p, "rb").read() == b1
        print(self.rel + ":", "MUDOU" if b1 != self.b0 else "igual", self.log)


JP = 'DL.FRASE_TETELESTAI_PT + " " + DL.CLAUSULA_Z_PT + " " + DL.FRASE_RECONSTROI_PT'; JE = JP.replace("_PT", "_EN")

A = Arq("delta_v410.py")
A.tr("# a ratificacao D101 (PT e EN): quantos nomes,",
     "# (revisao do construtor, R5) o ANUNCIO da clausula de 1 - beta: a FRASE, a CLAUSULA do limite entre parenteses logo depois dela, e a RECONSTRUCAO -- UMA constante, usada pelo registro e por todos os controles\n"
     "ANUNCIO_TETELESTAI_PT = FRASE_TETELESTAI_PT + \" (\" + CLAUSULA_Z_PT + \"); \" + FRASE_RECONSTROI_PT\n"
     "ANUNCIO_TETELESTAI_EN = FRASE_TETELESTAI_EN + \" (\" + CLAUSULA_Z_EN + \"); \" + FRASE_RECONSTROI_EN\n"
     "# a ratificacao D101 (PT e EN): quantos nomes,")
A.tr('+ FRASE_TETELESTAI_PT + " (" + CLAUSULA_Z_PT + "); "\n             + FRASE_RECONSTROI_PT + ". O limiar', '+ ANUNCIO_TETELESTAI_PT + ". O limiar')
A.grava()

A = Arq("registros_aescala_v410.py")
A.tr('ANUNCIO_PT = DL.FRASE_TETELESTAI_PT + " (" + DL.CLAUSULA_Z_PT + "); " + DL.FRASE_RECONSTROI_PT', 'ANUNCIO_PT = DL.ANUNCIO_TETELESTAI_PT')
A.tr('ANUNCIO_EN = DL.FRASE_TETELESTAI_EN + " (" + DL.CLAUSULA_Z_EN + "); " + DL.FRASE_RECONSTROI_EN', 'ANUNCIO_EN = DL.ANUNCIO_TETELESTAI_EN')
A.grava()

A = Arq("conferir_rito_v410.py")
A.tr(JP, "DL.ANUNCIO_TETELESTAI_PT")
A.tr('.count(DL.CLAUSULA_Z_PT) == 1 and DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) in fc', '.count(DL.CLAUSULA_Z_PT) == 2 and DL.ANUNCIO_TETELESTAI_PT in fc[fc.find(ESP["md_aescala"]):].split("\\n", 1)[0] and DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) in fc')
A.grava()

A = Arq("ensaio_a_seco_v410.py")
A.tr(JP, "DL.ANUNCIO_TETELESTAI_PT"); A.tr(JE, "DL.ANUNCIO_TETELESTAI_EN")
A.tr('DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) in ln_ and ln_.count(DL.CLAUSULA_Z_PT) == 1))', 'DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) in ln_ and ln_.count(DL.CLAUSULA_Z_PT) == 2))')
A.tr('DL.FRASE_NOMES_RATIFICADOS_D101_PT[1:] in ln_ and ln_.count(DL.CLAUSULA_Z_PT) == 1', 'DL.FRASE_NOMES_RATIFICADOS_D101_PT[1:] in ln_ and ln_.count(DL.CLAUSULA_Z_PT) == 2')
A.tr('and ln_.find(DL.CLAUSULA_Z_PT) < ln_.find(DL.FRASE_TETELESTAI_PT) and "[PILOTO][SIM]" in ln_', 'and ln_.find(DL.CLAUSULA_Z_PT) < ln_.find(DL.FRASE_TETELESTAI_PT) and DL.ANUNCIO_TETELESTAI_PT in ln_ and "[PILOTO][SIM]" in ln_')
A.grava()

A = Arq("guarda_frases_v410.py")
A.tr(JP, "DL.ANUNCIO_TETELESTAI_PT"); A.tr(JE, "DL.ANUNCIO_TETELESTAI_EN")
A.grava()

A = Arq("pos_rito/teste_textos_custodia_sem_candidato_v410.py")
A.tr('DL.FRASE_TETELESTAI_PT + ". " + DL.CLAUSULA_Z_PT in R and DL.FRASE_TETELESTAI_EN + ". " + DL.CLAUSULA_Z_EN in _en5', 'DL.FRASE_TETELESTAI_PT + " (" + DL.CLAUSULA_Z_PT + ")" in R and DL.FRASE_TETELESTAI_EN + " (" + DL.CLAUSULA_Z_EN + ")" in _en5')
A.tr('R.replace(DL.FRASE_TETELESTAI_PT + ". " + DL.CLAUSULA_Z_PT, DL.FRASE_TETELESTAI_PT + ". (retirada)")', 'R.replace(DL.FRASE_TETELESTAI_PT + " (" + DL.CLAUSULA_Z_PT + ")", DL.FRASE_TETELESTAI_PT + " (retirada)")')
A.tr('r_ = bool(DL.FRASE_TETELESTAI_PT + ". " + DL.CLAUSULA_Z_PT in txt_ and', 'r_ = bool(DL.FRASE_TETELESTAI_PT + " (" + DL.CLAUSULA_Z_PT + ")" in txt_ and')
A.grava()
