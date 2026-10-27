# -*- coding: utf-8 -*-
"""derivar_v400_motor.py -- o MOTOR da derivacao dos scripts da cadeia v400 a partir dos da v399 (a cadeia que RODOU em 24/10), sem executar nada: o mapa mecanico das versoes, o PROTEGIDO e as regras com contagem exata.
 - O MAPA: 398 -> 399 e 399 -> 400, palavra a palavra, com fronteira de digitos (a versao ANTERIOR da cadeia sobe um, a versao DESTA cadeia sobe um); hash hexadecimal longo nunca e' tocado.
 - O PROTEGIDO (nomes que NASCERAM no um.py e por isso NAO sobem: o um.py v400 os traz com o nome da v398/v399): todo identificador de 398/399 que existe no TEXTO da base v399 selada (lido do disco, nao digitado) + PROT_EXTRA do arquivo.
   Palavras nuas (v398, v399, E398, V399...) NAO sao protegidas: sao o rotulo da versao e sobem.
 - As REGRAS: (antigo_depois_do_mapa, novo, contagem) ou funcoes (texto -> texto) que ASSERTAM a propria contagem; o motor ABORTA se uma regra nao casar o numero esperado de vezes.
 - ast.parse de cada saida .py; sha256 de entrada e de saida de cada arquivo no relatorio. NUNCA executa o derivado. Nao sobrescreve um derivado que ja' existe e difere (autoral editado depois) sem --refazer.
Molde: derivar_encanamento_v399.py."""
import ast, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
V9 = os.path.join(os.path.dirname(HERE), "v399")
sha = lambda b: hashlib.sha256(b).hexdigest()
NUM = re.compile(r"(?<![0-9])(398|399)(?![0-9])")
RX_WORD = re.compile(r"[A-Za-z0-9_]+")
HEXLONGO = re.compile(r"[0-9a-fA-F]{8,}")
NU = lambda m: str(int(m.group(1)) + 1)
_PROT_UM = None
_UMBLOB = None
_CACHE = {}


def prot_um():
    """Os identificadores de 398/399 que existem no um.py base (v399 selada): nascidos no programa, nao sobem."""
    global _PROT_UM, _UMBLOB
    if _PROT_UM is None:
        t = open(os.path.join(HERE, "base_v399", "um.py"), "rb").read().decode("utf-8")
        ws = set(RX_WORD.findall(t))
        _PROT_UM = {w for w in ws if NUM.search(w) and not re.fullmatch(r"[A-Za-z]?(398|399)", w) and not HEXLONGO.fullmatch(w)}
        _UMBLOB = "\n" + "\n".join(sorted(_PROT_UM)) + "\n"
    return _PROT_UM


def protegida(w):
    """w (palavra com 398/399) nasceu no um.py: e' um identificador dele OU um pedaco (prefixo/sufixo/miolo) de um identificador dele (ex.: o veredito TGL_..._V399__ de um token maior)."""
    if w in _CACHE:
        return _CACHE[w]
    prot_um()
    r = (w in _PROT_UM) or (not re.fullmatch(r"[A-Za-z]?(398|399)", w) and len(w) >= 10 and (w in _UMBLOB))
    _CACHE[w] = r
    return r


def bump(t, prot_extra=()):
    prot_um()
    extra = set(prot_extra)

    def fw(m):
        w = m.group(0)
        if not NUM.search(w) or HEXLONGO.fullmatch(w) or w in extra:
            return w
        if m.start() > 0 and t[m.start() - 1] == "[" and (t[m.end():m.end() + 1] == "]" or t[m.end():m.end() + 2] == "\\]") and re.fullmatch(r"v39[89]", w):   # a ETIQUETA de stdout `[v399]` (ou `\[v399\]` num regex) que o um.py imprime (nasceu nele): nao sobe
            return w
        if w.startswith("registros_v39"):     # a CHAVE do core/selo (nascida no um.py) NAO sobe; o MODULO da cadeia (registros_v39x.py / import registros_v39x) sobe
            seg_ant = t[max(0, m.start() - 30):m.start()]
            if t[m.end():m.end() + 3] == ".py" or re.search(r"import\s+$", seg_ant):
                return NUM.sub(NU, w)
            return w
        if re.match(r"\.(?:py|json|sh|pysnip|lean|txt|md|log)(?![A-Za-z0-9_])", t[m.end():m.end() + 9]):    # NOME DE ARQUIVO da cadeia (runtime_v399.py, ESPERADOS_v399.json...): sobe; o programa so' o MENCIONA em texto
            return NUM.sub(NU, w)
        if protegida(w):
            return w
        return NUM.sub(NU, w)
    return RX_WORD.sub(fw, t)


def entre(inicio, fim, novo, nome):
    """regra por FUNCAO: troca o trecho que comeca em `inicio` (unico) e vai ate o comeco de `fim` (depois de `inicio`) por `novo`; ASSERTA as ancoras."""
    def fn(t):
        assert t.count(inicio) == 1, ("ancora inicial nao unica", nome, inicio[:70], t.count(inicio))
        i = t.index(inicio)
        assert t.count(fim, i + len(inicio)) >= 1, ("ancora final ausente", nome, fim[:70])
        j = t.index(fim, i + len(inicio))
        return t[:i] + novo + t[j:]
    return (fn, nome, 1)


def sub_n(pat, rep, n, nome=None, flags=0):
    def fn(t):
        t2, c = re.subn(pat, lambda m_: rep, t, flags=flags)      # o novo e' texto LITERAL (barras invertidas nao sao escapes de modelo)
        assert c == n, ("regra sub_n casou %d (esperado %d)" % (c, n), pat[:80])
        return t2
    return (fn, nome or ("sub_n:" + pat[:50]), n)


def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None):
    """src: caminho relativo a v399; dst: relativo a v400. Devolve o relatorio. As regras vem DEPOIS do mapa (os padroes estao escritos como o texto fica depois do mapa)."""
    ps, pd = os.path.join(V9, *src.split("/")), os.path.join(HERE, *dst.split("/"))
    raw = open(ps, "rb").read(); t = raw.decode("utf-8")
    t2 = bump(t, prot_extra) if com_bump else t
    aplic = []
    for old, new, n in regras:
        if callable(old):
            t2 = old(t2); aplic.append({"regra": "fn:" + str(new)[:66], "casou": n}); continue
        c = t2.count(old)
        if c != n:
            raise SystemExit("REGRA NAO CASOU %d vez(es) (casou %d) em %s: %r" % (n, c, src, old[:140]))
        t2 = t2.replace(old, new); aplic.append({"regra": old[:70], "casou": c})
    if fantasmas:
        fant = sorted({m.group(0) for m in re.finditer(fantasmas, t2)})
        if fant:
            raise SystemExit("NOME FANTASMA em %s: %s" % (dst, fant[:6]))
    if dst.endswith(".py"):
        ast.parse(t2)
    os.makedirs(os.path.dirname(pd), exist_ok=True)
    novo = t2.encode("utf-8")
    estado = "gravado"
    if os.path.exists(pd):
        atual = open(pd, "rb").read()
        if atual == novo:
            estado = "igual"
        elif not refazer:
            estado = "EXISTE_E_DIFERE__nao_sobrescrevi"
    if estado == "gravado":
        open(pd + ".tmp", "wb").write(novo); os.replace(pd + ".tmp", pd)
    return {"origem": ps, "origem_sha256": sha(raw), "destino": pd, "destino_sha256": sha(novo), "estado": estado, "regras": aplic}


def linhas_com(dst, padrao=r"39[89]|400"):
    """as linhas do derivado que carregam um rotulo de versao (para a conferencia visual da gerencia)"""
    t = open(os.path.join(HERE, *dst.split("/")), "rb").read().decode("utf-8")
    return [(i + 1, l.strip()[:170]) for i, l in enumerate(t.splitlines()) if re.search(padrao, l)]
