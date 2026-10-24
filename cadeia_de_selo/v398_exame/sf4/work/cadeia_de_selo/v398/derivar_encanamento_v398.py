# -*- coding: utf-8 -*-
"""derivar_encanamento_v398.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os scripts de ENCANAMENTO da cadeia v398 a partir dos da v397 (cadeia_de_selo\\v397\\, a que foi USADA no rito real da v397 em 23/10):
(1) o mapa mecanico das versoes numa passada so', com fronteira de digitos e PROTECAO dos nomes que nasceram no um.py (e por isso NAO sobem): 396 -> 397 e 397 -> 398 em tudo, menos nos identificadores protegidos
    (testemunha_estatica_v396, teste_de_veracidade_fase9_v397, cunhagens_v39x, kh_n1_cobertura_v39x, registros_v39x [como chave do core/selo], _V39x_*, _v39x_*, v39x_cun_*, ext_*39x_*); o que sobrar de nome nascido no um.py e subir sozinho vira um nome
    inexistente e o derivador RECUSA (FANTASMAS); nenhum nome da v398 pode existir no texto de PARTIDA (FANT_PRE);
(2) edicoes SEMANTICAS nomeadas, cada uma com a contagem exata (o script ABORTA se a regra nao casar o numero esperado de vezes); os padroes estao escritos como o texto fica DEPOIS do mapa;
(3) ast.parse de cada saida .py (so' compila, NAO executa); relatorio JSON com sha256 de entrada e de saida e a lista das palavras de CONTEUDO ESPECIFICO que ainda restam (token, veracidade, 4,44, quadro, seis...), para a conferencia.
Nada aqui e' digitado de memoria: hashes e numeros do conteudo vem dos arquivos que os scripts derivados leem. Escreve so' em v398\\ (arquivos derivados). NAO sobrescreve um derivado que ja' existe e difere (os autorais, editados depois da subida, ficam como estao) a menos que
--refazer. uso: python -I -B -X utf8 derivar_encanamento_v398.py [--so NOME ...] [--refazer] [--saida PASTA]"""
import ast, hashlib, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V5 = os.path.join(os.path.dirname(HERE), "v397")
sha = lambda b: hashlib.sha256(b).hexdigest()
RX39 = re.compile(r"(?<![0-9])39([67])(?![0-9])")
RX_WORD = re.compile(r"[A-Za-z0-9_]+")
# nomes que NASCERAM no um.py (v393 a v397) e referem-se a objetos que continuam com esse nome: NAO sobem
PROT = re.compile(r"(?:(?:testemunha_estatica|cunhagens|kh_n1_cobertura|psibit|kh_n1|teste_de_veracidade_fase9)_v39[67]\w*|_[vV]39[67]_\w*|v39[67]_cun_[0-9a-f]+|v396_static_witness_mechanics|ext_[a-z]+39[67]_\d+|REG_V39[67]\w*|TGL_\w*_V39[67]\w*)")   # TGL_<...>_V39x<...>: os VEREDITOS nascidos no um.py (prefixos como TGL_FASE9_VERACIDADE_V397__...) NAO sobem
# nomes fantasma: o que o mapa NAO pode produzir (objetos do um.py que nao existem na v398); se sobrar, e' erro
FANTASMAS = re.compile(r"testemunha_estatica_v397|psibit_v396|_[vV]397_(?:TESTEMUNHA|PSIBIT)\w*|ext_tes397|ext_tok398|ext_psb396|teste_de_veracidade_fase9_v398|v396_static_witness_mechanics_v397")
# a partida (v397) nao pode trazer nenhum nome da v398: se trouxer, a protecao falhou antes de comecar
FANT_PRE = re.compile(r"cunhagens_v398|kh_n1_cobertura_v398|sonico_v398|afinacao_das_cordas_v398|teste_de_veracidade_fase9_v398|_[vV]398_\w*|ext_[a-z]+398_\d+")
FLAGGED = re.compile(r"[Tt]oken|TOKEN|veracidade|VERACIDADE|4,44|4\.44|[Qq]uadro|QUADRO|Unica Palavra|[Úú]nica Palavra|seis |six |fase9|F9|tok397|23/10|2026-10-23|20261023|0b6a58e7|testemunha_estatica|psibit")


def bump(t):
    def fw(m):
        w = m.group(0)
        if not RX39.search(w):
            return w
        if PROT.fullmatch(w):
            return w
        if w.startswith("registros_v39"):   # a CHAVE do core/selo (nascida no um.py) NAO sobe; o MODULO da cadeia (registros_v39x.py / import) sobe
            seg_ant = t[max(0, m.start() - 30):m.start()]
            if t[m.end():m.end() + 3] == ".py" or re.search(r"import\s+$", seg_ant):
                return RX39.sub(lambda k: "39" + str(int(k.group(1)) + 1), w)
            return w
        return RX39.sub(lambda k: "39" + str(int(k.group(1)) + 1), w)
    return RX_WORD.sub(fw, t)


# (origem relativa a v397, destino relativo a v398, [(antigo_depois_do_mapa, novo, contagem)], bump?)
ENTRADAS = []


def entrada(src, dst=None, regras=(), com_bump=True, autoral=False):
    ENTRADAS.append((src, dst or (bump(src) if com_bump else src), list(regras), com_bump, autoral))


def aplicar(src, dst, regras, com_bump, saida, refazer):
    ps, pd = os.path.join(V5, *src.split("/")), os.path.join(saida, *dst.split("/"))
    raw = open(ps, "rb").read(); t = raw.decode("utf-8")
    if com_bump:
        fp = sorted({m.group(0) for m in FANT_PRE.finditer(t)})
        if fp:
            raise SystemExit("A PARTIDA %s traz nome da v398 (a protecao falhou): %s" % (src, fp[:6]))
    t2 = bump(t) if com_bump else t; aplic = []
    for old, new, n in regras:
        c = t2.count(old)
        if c != n:
            raise SystemExit("REGRA NAO CASOU %d vez(es) (casou %d) em %s: %r" % (n, c, src, old[:120]))
        t2 = t2.replace(old, new); aplic.append({"regra": old[:70], "casou": c})
    fant = sorted({m.group(0) for m in FANTASMAS.finditer(t2)})
    if fant:
        raise SystemExit("NOME FANTASMA em %s (objeto do um.py que nao existe na v398): %s" % (dst, fant[:6]))
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
    resto = sorted({m.group(0) for m in FLAGGED.finditer(t2)})
    return {"origem": ps, "origem_sha256": sha(raw), "destino": pd, "destino_sha256": sha(novo), "estado": estado, "regras": aplic, "palavras_de_conteudo_restantes": resto}


def main():
    args = sys.argv[1:]
    refazer = "--refazer" in args
    saida = HERE
    if "--saida" in args:
        saida = os.path.abspath(args[args.index("--saida") + 1])
    so = None
    if "--so" in args:
        i = args.index("--so"); so = set(a for a in args[i + 1:] if not a.startswith("--"))
    for rf in sorted(f for f in os.listdir(HERE) if re.fullmatch(r"derivar_encanamento_v398_regras(_[A-Z])?\.py", f)):   # lotes de regras (exec no escopo deste arquivo)
        exec(open(os.path.join(HERE, rf), encoding="utf-8").read(), globals())
    rel = []
    for src, dst, regras, com_bump, autoral in ENTRADAS:
        if so and os.path.basename(dst) not in so and dst not in so:
            continue
        r = aplicar(src, dst, regras, com_bump, saida, refazer); r["autoral_depois_da_subida"] = autoral; rel.append(r)
        print("%-46s %-12s %s regras=%d restam=%s" % (dst, r["estado"][:12], r["destino_sha256"][:12], len(regras), r["palavras_de_conteudo_restantes"][:6]))
    if not so and saida == HERE:
        json.dump({"contrato": "DERIVACAO_ENCANAMENTO_v398", "executado": False, "mapa": "396->397, 397->398 com fronteira de digitos e protecao dos nomes nascidos no um.py", "arquivos": rel},
                  open(os.path.join(HERE, "DERIVACAO_ENCANAMENTO_v398.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
