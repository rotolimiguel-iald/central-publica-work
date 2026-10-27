# -*- coding: utf-8 -*-
"""derivar_v402_motor.py -- o MOTOR da derivacao dos scripts da cadeia v402 a partir dos da cadeia v401 (a que foi USADA no rito real de 25/10), sem executar nada: o mapa mecanico das versoes, o PROTEGIDO e as regras com contagem exata.
Molde: derivar_v401_motor.py (cadeia_de_selo/v401). Uma ORIGEM so': "v401" (o arquivo da cadeia v401 FINAL, com as licoes de v399, v400 e v401 ja' dentro); o mapa sobe 400 -> 401 (a base selada) e 401 -> 402 (esta rodada); o 399 NAO sobe (os nomes e rotulos
de 399 sao historicos: a pedra Testemunho, os registros selo_pela_propria_tecnologia_v399 etc.).
 - O PROTEGIDO (nomes que NASCERAM no um.py e por isso NAO sobem: o um.py v402 os traz com o nome da v399/v400/v401): todo identificador com 399/400/401 que existe no TEXTO da base v401 selada (lido do disco, nao digitado) + PROT_EXTRA do arquivo.
   Palavras nuas (v400, v401, E401, V401...) NAO sao protegidas: sao o rotulo da versao e sobem.
 - As REGRAS: (antigo_depois_do_mapa, novo, contagem) ou funcoes (texto -> texto) que ASSERTAM a propria contagem; o motor ABORTA se uma regra nao casar o numero esperado de vezes.
 - ast.parse de cada saida .py; sha256 de entrada e de saida de cada arquivo no relatorio. NUNCA executa o derivado. Nao sobrescreve um derivado que ja' existe e difere (autoral editado depois) sem --refazer."""
import ast, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.dirname(HERE)                                        # ...\cadeia_de_selo
ORIGENS = {"v401": os.path.join(CH, "v401")}
sha = lambda b: hashlib.sha256(b).hexdigest()
NUM3 = re.compile(r"(?<![0-9])(399|400|401)(?![0-9])")
RX_WORD = re.compile(r"[A-Za-z0-9_]+")
HEXLONGO = re.compile(r"[0-9a-fA-F]{8,}")
MAPAS = {"v401": {"400": "401", "401": "402"}}
_PROT_UM = None
_UMBLOB = None
_CACHE = {}


def prot_um():
    """Os identificadores de 399/400/401 que existem no um.py base (v401 selada): nascidos no programa, nao sobem."""
    global _PROT_UM, _UMBLOB
    if _PROT_UM is None:
        _pb = os.path.join(HERE, "base_v401", "um.py")
        if not os.path.exists(_pb):    # antes de copiar_base_v402.py: o um.py do Nos (a v401 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)
            _pb = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "um.py")
        t = open(_pb, "rb").read().decode("utf-8")
        ws = set(RX_WORD.findall(t))
        _PROT_UM = {w for w in ws if NUM3.search(w) and not re.fullmatch(r"[A-Za-z]?(399|400|401)", w) and not HEXLONGO.fullmatch(w)}
        _UMBLOB = "\n" + "\n".join(sorted(_PROT_UM)) + "\n"
    return _PROT_UM


def protegida(w):
    """w (palavra com 399/400/401) nasceu no um.py: e' um identificador dele OU um pedaco (prefixo/sufixo/miolo) de um identificador dele."""
    if w in _CACHE:
        return _CACHE[w]
    prot_um()
    r = (w in _PROT_UM) or (not re.fullmatch(r"[A-Za-z]?(399|400|401)", w) and len(w) >= 10 and (w in _UMBLOB))
    _CACHE[w] = r
    return r


def bump(t, prot_extra=(), origem="v401"):
    prot_um()
    extra = set(prot_extra)
    mapa = MAPAS[origem]
    rx_mapeado = re.compile(r"(?<![0-9])(%s)(?![0-9])" % "|".join(mapa))
    sub = lambda s: rx_mapeado.sub(lambda m: mapa[m.group(1)], s)

    def fw(m):
        w = m.group(0)
        if not rx_mapeado.search(w) or HEXLONGO.fullmatch(w) or w in extra:
            return w
        # a ETIQUETA de stdout `[v399]` (ou `\[v399\]` num regex) que o um.py imprime (nasceu nele): nao sobe
        if m.start() > 0 and t[m.start() - 1] == "[" and (t[m.end():m.end() + 1] == "]" or t[m.end():m.end() + 2] == "\\]") and re.fullmatch(r"v(399|400|401)", w):
            return w
        if w.startswith("registros_v39") or w.startswith("registros_v40"):     # a CHAVE do core/selo (nascida no um.py) NAO sobe; o MODULO da cadeia (registros_v39x.py / import registros_v39x) sobe
            seg_ant = t[max(0, m.start() - 30):m.start()]
            if t[m.end():m.end() + 3] == ".py" or re.search(r"import\s+$", seg_ant):
                return sub(w)
            return w
        if re.match(r"\.(?:py|json|sh|pysnip|lean|txt|md|log)(?![A-Za-z0-9_])", t[m.end():m.end() + 9]):    # NOME DE ARQUIVO da cadeia (runtime_v399.py, ESPERADOS_v400.json...): sobe; o programa so' o MENCIONA em texto
            return sub(w)
        if protegida(w):
            return w
        return sub(w)
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


def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v401"):
    """src: caminho relativo a pasta da origem (v401); dst: relativo a v402. Devolve o relatorio. As regras vem DEPOIS do mapa (os padroes estao escritos como o texto fica depois do mapa)."""
    ps, pd = os.path.join(ORIGENS[origem], *src.split("/")), os.path.join(HERE, *dst.split("/"))
    raw = open(ps, "rb").read(); t = raw.decode("utf-8")
    t2 = bump(t, prot_extra, origem) if com_bump else t
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
    return {"origem": ps, "origem_sha256": sha(raw), "destino": pd, "destino_sha256": sha(novo), "estado": estado, "regras": aplic, "mapa_de_origem": origem}


def linhas_com(dst, padrao=r"39[9]|40[012]"):
    """as linhas do derivado que carregam um rotulo de versao (para a conferencia visual da gerencia)"""
    t = open(os.path.join(HERE, *dst.split("/")), "rb").read().decode("utf-8")
    return [(i + 1, l.strip()[:170]) for i, l in enumerate(t.splitlines()) if re.search(padrao, l)]


def _opcodes(a_txt, b_txt):
    import difflib
    A, B = a_txt.splitlines(True), b_txt.splitlines(True)
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    return A, B, [op for op in sm.get_opcodes() if op[0] != "equal"]


def lista_hunks(a_rel, b_rel, origem_a="v401", origem_b="v401", ancho=170):
    """lista (indice, tag, linhas_a, linhas_b, trecho) dos hunks entre o arquivo da origem A (subido) e o da origem B (subido): serve para ESCOLHER quais licoes da cadeia B entram."""
    a = bump(open(os.path.join(ORIGENS[origem_a], a_rel), encoding="utf-8").read(), (), origem_a)
    b = bump(open(os.path.join(ORIGENS[origem_b], b_rel), encoding="utf-8").read(), (), origem_b)
    A, B, ops = _opcodes(a, b)
    out = []
    for k, (tag, i1, i2, j1, j2) in enumerate(ops):
        out.append((k, tag, (i1 + 1, i2), (j1 + 1, j2), (("".join(B[j1:j2]) or "".join(A[i1:i2]))[:ancho]).replace("\n", " | ")))
    return out


def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v401", origem_b="v401"):
    """regra por FUNCAO: o texto `t` (o arquivo da origem A, ja' subido) recebe os hunks de indice `indices` do diff A -> B (B = o arquivo da origem B, subido). Assevera que `t` e' o A esperado."""
    def fn(t):
        b = bump(open(os.path.join(ORIGENS[origem_b], b_rel), encoding="utf-8").read(), (), origem_b)
        A, B, ops = _opcodes(t, b)
        assert max(indices) < len(ops), ("indice de hunk fora do intervalo", indices, len(ops))
        out, pos = [], 0
        for k, (tag, i1, i2, j1, j2) in enumerate(ops):
            out.append("".join(A[pos:i1]))
            out.append("".join(B[j1:j2]) if k in indices else "".join(A[i1:i2]))
            pos = i2
        out.append("".join(A[pos:]))
        return "".join(out)
    return (fn, "hunks %s de %s" % (list(indices), b_rel), 1)
