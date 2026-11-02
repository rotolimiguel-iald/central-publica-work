# -*- coding: utf-8 -*-
"""Statutes and append-only ledger. Sidak arithmetic is exploratory only;
shared families do not establish calibrated global significance. Posterior
mass is not passed to frequentist correction. No physical confirmation."""
import hashlib
from contextlib import contextmanager
import json
import math
import numbers
import re
import sqlite3
import threading
import time

PROIBIDO = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED|CONSCIOUSNESS_PROVED|\bconfirmad[oa]s?\b", re.I)

ESTATUTOS = {
    "DIAGNOSTICO_DE_AVALIACAO": "avaliação de um ponto do modelo contra os dados: não é ajuste nem inferência",
    "AJUSTE_DE_MAXIMA_VEROSSIMILHANCA": "melhor ajuste por mínimos quadrados; σ pela matriz JᵀJ (aproximação gaussiana local)",
    "COMPARACAO_DE_MODELOS_DELTA_CHI2": "Δχ² entre ajustes aninhados; aproximação local de Wilks não calibrada; sem significância global certificada",
    "POSTERIOR_CONDICIONAL_AO_MODELO_E_AOS_DADOS": "posterior diagnóstico uniforme no suporte instrumental explícito; sem evidência sobre o prior amplo",
}


def numero_finito(value, name="numero"):
    """Reject booleans, strings, NaN and infinity before coercion."""
    if isinstance(value, bool) or not isinstance(value, numbers.Real) or not math.isfinite(float(value)):
        raise ValueError("%s deve ser número finito não booleano" % name)
    return float(value)


def inteiro(value, name, lo, hi):
    n = numero_finito(value, name)
    if not n.is_integer() or not lo <= n <= hi:
        raise ValueError("%s deve ser inteiro em [%s,%s]" % (name, lo, hi))
    return int(n)


def booleano(value, name):
    if type(value) is not bool:
        raise ValueError("%s deve ser booleano" % name)
    return value


def guarda(obj):
    """Recusa (exceção) qualquer saída que contenha palavra proibida pela régua."""
    s = json.dumps(obj, ensure_ascii=False, default=str, allow_nan=False)
    m = PROIBIDO.search(s)
    if m:
        raise ValueError("REGUA: saída recusada por palavra proibida: %r" % m.group(0))
    return obj


def z_de_p(p):
    """z bilateral de um p (p pequeno: expansão assintótica estável)."""
    p = numero_finito(p, "p")
    if not 0 <= p <= 1:
        raise ValueError("p fora de [0,1]")
    if p == 0:
        return None  # numerical underflow is not measured infinite significance
    if p >= 1:
        return 0.0
    from scipy.stats import norm
    return float(norm.isf(p / 2.0))


def p_de_z(z):
    z = numero_finito(z, "z")
    from scipy.stats import norm
    return float(2.0 * norm.sf(abs(z)))


class Livro:
    """O livro de consultas: SQLite só de acréscimo em estado/livro.sqlite3."""

    def __init__(self, caminho):
        self.caminho = caminho
        self.lock = threading.Lock()
        with self._con() as c:
            c.execute("CREATE TABLE IF NOT EXISTS consultas (id INTEGER PRIMARY KEY, ts TEXT, cliente TEXT, operacao TEXT, familia TEXT, "
                      "conjuntos TEXT, modelo TEXT, pedido TEXT, resultado_sha TEXT, estatuto TEXT, estatistica REAL, p_local REAL)")

    @contextmanager
    def _con(self):
        connection = sqlite3.connect(self.caminho, timeout=30)
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    @staticmethod
    def familia(operacao, conjuntos, modelo):
        chave = json.dumps([operacao, sorted(conjuntos), modelo], sort_keys=True)
        return hashlib.sha256(chave.encode()).hexdigest()[:16]

    def registra(self, cliente, operacao, conjuntos, modelo, pedido, resultado, estatuto, estatistica=None, p_local=None):
        guarda(resultado)
        if estatistica is not None:
            numero_finito(estatistica, "estatistica")
        if p_local is not None:
            p_local = numero_finito(p_local, "p_local")
            if not 0 <= p_local <= 1:
                raise ValueError("p_local fora de [0,1]")
        sha = hashlib.sha256(json.dumps(resultado, sort_keys=True, default=str, allow_nan=False).encode()).hexdigest()
        with self.lock, self._con() as c:
            c.execute("INSERT INTO consultas (ts, cliente, operacao, familia, conjuntos, modelo, pedido, resultado_sha, estatuto, estatistica, p_local) "
                      "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                      (time.strftime("%Y-%m-%dT%H:%M:%S"), cliente, operacao, self.familia(operacao, conjuntos, modelo), json.dumps(sorted(conjuntos)),
                       json.dumps(modelo, sort_keys=True), json.dumps(pedido, sort_keys=True, default=str), sha, estatuto, estatistica, p_local))
        return sha

    def n_familias_de_teste(self, incluir=None):
        """Famílias distintas de teste no livro; `incluir` soma a família do teste corrente se ela ainda não estiver lá."""
        with self._con() as c:
            fams = {r[0] for r in c.execute("SELECT DISTINCT familia FROM consultas WHERE p_local IS NOT NULL")}
        if incluir:
            fams.add(incluir)
        return len(fams)

    def corrige(self, p_local, familia=None):
        """Sidak arithmetic, explicitly exploratory; no certified global p-value."""
        n = max(1, self.n_familias_de_teste(incluir=familia))
        p_local = numero_finito(p_local, "p_local")
        if not 0 <= p_local <= 1:
            raise ValueError("p_local fora de [0,1]")
        if n * p_local < 1e-10:
            pg = n * p_local                                    # primeira ordem exata a 1e-10
        else:
            pg = -math.expm1(n * math.log1p(-p_local)) if p_local < 1.0 else 1.0
        return dict(p_local=p_local, z_local_aproximado=z_de_p(p_local), n_familias=n,
                    p_sidak_exploratorio=pg, z_sidak_exploratorio=z_de_p(pg),
                    p_global=None, z_global=None, global_certificado=False,
                    estatuto="DIAGNOSTICO_EXPLORATORIO_NAO_CALIBRADO",
                    metodo="Šidák ilustrativo; independência não estabelecida; sem controle FWER certificado")

    def resumo(self, n=30):
        with self._con() as c:
            tot = c.execute("SELECT COUNT(*) FROM consultas").fetchone()[0]
            ult = c.execute("SELECT ts, cliente, operacao, conjuntos, modelo, estatuto, estatistica, p_local, resultado_sha FROM consultas "
                            "ORDER BY id DESC LIMIT ?", (n,)).fetchall()
        return dict(total=int(tot), familias_de_teste=self.n_familias_de_teste(),
                    ultimas=[dict(ts=a, cliente=b, operacao=o, conjuntos=json.loads(cj), modelo=json.loads(mo), estatuto=e, estatistica=s,
                                  p_local=p, resultado_sha=h[:16]) for a, b, o, cj, mo, e, s, p, h in ult])
