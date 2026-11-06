# -*- coding: utf-8 -*-
"""_adapt_util_v409.py -- o utilitario dos adaptadores da v409 (claude-construtor-v409, 05/11/2026): troca de texto com CONTAGEM EXATA (aborta se nao casar o numero esperado),
sobre o texto com fim de linha normalizado (LF) e regravado no fim de linha ORIGINAL do arquivo (CRLF preservado; nunca sed -i), com backup de BYTES (.bak_<ts>) antes de gravar,
temporario -> conferencia de tamanho -> substituicao, e a marca `[A ADAPTAR v409]` trocada pela marca `[ADAPTADO v409, ...]` (o p00 recusa arquivo com a marca A ADAPTAR).
Uso (num adaptador): from _adapt_util_v409 import Arq; a = Arq("arquivo.py"); a.troca(velho, novo, n=1); a.marca("o que mudou"); a.grava()"""
import ast
import datetime
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
RX_MARCA = re.compile(r"^# \[A ADAPTAR v409\][^\n]*\n", re.M)


class Arq:
    def __init__(self, rel):
        self.p = rel if os.path.isabs(rel) else os.path.join(HERE, *rel.replace("\\", "/").split("/"))
        self.raw = open(self.p, "rb").read()
        t = self.raw.decode("utf-8")
        self.crlf = "\r\n" in t
        assert not self.crlf or t.count("\r") == t.count("\r\n"), ("CR solto", self.p)
        self.t = t.replace("\r\n", "\n")
        self.t0 = self.t
        self.log = []

    def troca(self, velho, novo, n=1):
        c = self.t.count(velho)
        assert c == n, ("TROCA NAO CASOU %d vez(es) (casou %d) em %s" % (n, c, os.path.basename(self.p)), velho[:160])
        self.t = self.t.replace(velho, novo)
        self.log.append((velho[:60], c))
        return self

    def troca_re(self, padrao, novo, n=1, flags=re.M):
        t2, c = re.subn(padrao, lambda m_: novo, self.t, flags=flags)
        assert c == n, ("TROCA_RE NAO CASOU %d vez(es) (casou %d) em %s" % (n, c, os.path.basename(self.p)), padrao[:160])
        self.t = t2
        self.log.append((padrao[:60], c))
        return self

    def tem(self, s):
        return s in self.t

    def marca(self, oque):
        m = RX_MARCA.findall(self.t)
        assert len(m) == 1, ("a marca [A ADAPTAR v409] nao esta' uma vez", os.path.basename(self.p), len(m))
        self.t = RX_MARCA.sub(lambda _m: "# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] %s\n" % oque.replace("\n", " "), self.t, count=1)
        return self

    def grava(self):
        assert not RX_MARCA.search(self.t), ("a marca ainda esta' no arquivo (linha que comeca por # [A ADAPTAR v409]; a marca CITADA num texto, como no p00 que a recusa, nao conta)", os.path.basename(self.p))
        out = (self.t.replace("\n", "\r\n") if self.crlf else self.t).encode("utf-8")
        if self.p.endswith(".py"):
            ast.parse(self.t)
        elif self.p.endswith(".sh"):
            r = subprocess.run(["sh", "-n"], input=self.t.encode("utf-8"), capture_output=True)
            assert r.returncode == 0, (self.p, r.stderr[:300])
        if out == self.raw:
            print("igual:", os.path.basename(self.p))
            return False
        bak = self.p + ".bak_" + TS + "_adapt"
        if not os.path.exists(bak):
            open(bak, "wb").write(self.raw)
            assert open(bak, "rb").read() == self.raw
        open(self.p + ".tmp", "wb").write(out)
        assert os.path.getsize(self.p + ".tmp") == len(out)
        os.replace(self.p + ".tmp", self.p)
        print("gravado:", os.path.basename(self.p), len(self.raw), "->", len(out), "bytes;", len(self.log), "trocas")
        return True


def so_marca(rel, oque):
    """arquivo que a subida mecanica ja' deixou certo (conferido pelo diff do bump): so' a marca muda."""
    a = Arq(rel)
    a.marca(oque)
    a.grava()
    return a
