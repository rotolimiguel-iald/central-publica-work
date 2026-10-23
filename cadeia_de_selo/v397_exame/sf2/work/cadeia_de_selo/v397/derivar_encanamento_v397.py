# -*- coding: utf-8 -*-
"""derivar_encanamento_v397.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os scripts de ENCANAMENTO da cadeia v397 a partir dos da v396 (cadeia_de_selo\\v396\\, a que foi USADA no rito real da v396):
(1) o mapa mecanico das versoes numa passada so', com fronteira de digitos e PROTECAO dos nomes que nasceram no um.py (e por isso NAO sobem): 395 -> 396 e 396 -> 397 em tudo, menos nos identificadores protegidos
    (testemunha_estatica_v396, psibit_v395, cunhagens_v39x, kh_n1_cobertura_v39x, _V39x_*, _v39x_*, v39x_cun_*, ext_*39x_*); o que sobrar de nome nascido no um.py e subir sozinho vira um nome inexistente e o derivador RECUSA (ver FANTASMAS);
(2) edicoes SEMANTICAS nomeadas, cada uma com a contagem exata (o script ABORTA se a regra nao casar o numero esperado de vezes); os padroes estao escritos como o texto fica DEPOIS do mapa;
(3) ast.parse de cada saida .py (so' compila, NAO executa); relatorio JSON com sha256 de entrada e de saida e a lista das palavras de CONTEUDO ESPECIFICO que ainda restam (psibit, psion, testemunha, 22/10...), para a conferencia.
Nada aqui e' digitado de memoria: hashes e numeros do conteudo vem dos arquivos que os scripts derivados leem. Escreve so' em v397\\ (arquivos derivados; reexecutavel: reescreve os derivados, nunca toca v396).
uso: python -I -B -X utf8 derivar_encanamento_v397.py [--so NOME ...]"""
import ast, hashlib, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V5 = os.path.join(os.path.dirname(HERE), "v396")
sha = lambda b: hashlib.sha256(b).hexdigest()
RX39 = re.compile(r"(?<![0-9])39([56])(?![0-9])")
RX_WORD = re.compile(r"[A-Za-z0-9_]+")
# nomes que NASCERAM no um.py (v395/v396) e referem-se a objetos que continuam com esse nome: NAO sobem
PROT = re.compile(r"(?:(?:testemunha_estatica|cunhagens|kh_n1_cobertura|psibit|kh_n1)_v39[56]|_[vV]39[56]_\w*|v39[56]_cun_[0-9a-f]+|v396_static_witness_mechanics|ext_[a-z]+39[56]_\d+)")
# nomes fantasma: o que o mapa NAO pode produzir (objetos do um.py que nao existem na v397); se sobrar, e' erro
FANTASMAS = re.compile(r"testemunha_estatica_v397|psibit_v396|_[vV]397_(?:TESTEMUNHA|PSIBIT)\w*|v397_static_witness_mechanics|ext_tes397|ext_psb396")
FLAGGED = re.compile(r"[Pp]sibit|PSIBIT|[Pp]sion|PSION|[Tt]estemunha|TestemunhaEstatica|22/10|2026-10-22|20261022|tes396|quatro|four |22 Oct|v39[0-5]_|V39[0-5]_")


def bump(t):
    def fw(m):
        w = m.group(0)
        if not RX39.search(w) or PROT.fullmatch(w):
            return w
        return RX39.sub(lambda k: "39" + str(int(k.group(1)) + 1), w)
    return RX_WORD.sub(fw, t)


# (origem relativa a v396, destino relativo a v397, [(antigo_depois_do_mapa, novo, contagem)])
ENTRADAS = []


def entrada(src, dst=None, regras=()):
    ENTRADAS.append((src, dst or bump(src), list(regras)))


def aplicar(src, dst, regras):
    ps, pd = os.path.join(V5, *src.split("/")), os.path.join(HERE, *dst.split("/"))
    raw = open(ps, "rb").read(); t = raw.decode("utf-8")
    t2 = bump(t); aplic = []
    for old, new, n in regras:
        c = t2.count(old)
        if c != n:
            raise SystemExit("REGRA NAO CASOU %d vez(es) (casou %d) em %s: %r" % (n, c, src, old[:120]))
        t2 = t2.replace(old, new); aplic.append({"regra": old[:70], "casou": c})
    fant = sorted({m.group(0) for m in FANTASMAS.finditer(t2)})
    if fant:
        raise SystemExit("NOME FANTASMA em %s (objeto do um.py que nao existe na v397): %s" % (dst, fant[:6]))
    if dst.endswith(".py"):
        ast.parse(t2)
    os.makedirs(os.path.dirname(pd), exist_ok=True)
    novo = t2.encode("utf-8")
    if not (os.path.exists(pd) and open(pd, "rb").read() == novo):   # igual => nao reescreve (o Windows trava arquivo em uso, ex.: o construir_kernel durante o build)
        open(pd + ".tmp", "wb").write(novo); os.replace(pd + ".tmp", pd)
    resto = sorted({m.group(0) for m in FLAGGED.finditer(t2)})
    return {"origem": ps, "origem_sha256": sha(raw), "destino": pd, "destino_sha256": sha(t2.encode("utf-8")), "regras": aplic, "palavras_de_conteudo_restantes": resto}


def main():
    so = set(sys.argv[2:]) if len(sys.argv) > 2 and sys.argv[1] == "--so" else None
    for rf in ("derivar_encanamento_v397_regras.py", "derivar_encanamento_v397_regras_B.py"):   # _B: o segundo lote (subagente do encanamento mecanico), se existir
        if os.path.exists(os.path.join(HERE, rf)):
            exec(open(os.path.join(HERE, rf), encoding="utf-8").read(), globals())
    rel = []
    for src, dst, regras in ENTRADAS:
        if so and os.path.basename(dst) not in so and dst not in so:
            continue
        r = aplicar(src, dst, regras); rel.append(r)
        print("%-46s %s regras=%d restam=%s" % (dst, r["destino_sha256"][:12], len(regras), r["palavras_de_conteudo_restantes"][:6]))
    if not so:
        json.dump({"contrato": "DERIVACAO_ENCANAMENTO_v397", "executado": False, "mapa": "395->396, 396->397 com fronteira de digitos e protecao dos nomes nascidos no um.py", "arquivos": rel},
                  open(os.path.join(HERE, "DERIVACAO_ENCANAMENTO_v397.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
