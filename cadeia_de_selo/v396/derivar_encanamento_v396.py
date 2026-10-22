# -*- coding: utf-8 -*-
"""derivar_encanamento_v396.py -- DERIVA POR SCRIPT, SEM EXECUTAR, os scripts de ENCANAMENTO da cadeia v396 a partir dos da v395 (cadeia_de_selo\\v395\\, a que foi USADA no rito real da v395):
(1) o mapa mecanico das versoes numa passada so, com fronteira de digitos: 394 -> 395 e 395 -> 396 (v394/V394/k394/E394 -> v395/V395/k395/E395; v395/V395/k395/psb395 -> v396/V396/k396/...);
(2) edicoes SEMANTICAS nomeadas, cada uma com a contagem exata (o script ABORTA se a regra nao casar o numero esperado de vezes); os padroes estao escritos como o texto fica DEPOIS do mapa;
(3) ast.parse de cada saida .py (so' compila, NAO executa); relatorio JSON com sha256 de entrada e de saida e a lista das palavras de CONTEUDO ESPECIFICO que ainda restam (psibit, psion, 21/10...), para a conferencia.
Nada aqui e' digitado de memoria: hashes e numeros do conteudo vem dos arquivos que os scripts derivados leem. Escreve so' em v396\\ (arquivos derivados; reexecutavel: reescreve os derivados, nunca toca v395).
uso: python -I -B -X utf8 derivar_encanamento_v396.py [--so NOME ...]"""
import ast, hashlib, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V5 = os.path.join(os.path.dirname(HERE), "v395")
sha = lambda b: hashlib.sha256(b).hexdigest()
RX_V = re.compile(r"(?<![0-9])39([45])(?![0-9])")
bump = lambda t: RX_V.sub(lambda m: "39" + str(int(m.group(1)) + 1), t)
FLAGGED = re.compile(r"[Pp]sibit|PSIBIT|psion|Psion|PSION|21/10|2026-10-21|20261021|psb39|quatro|four |21 Oct|v39[0-4]_|V39[0-4]_")

# (origem relativa a v395, destino relativo a v396, [(antigo_depois_do_mapa, novo, contagem)])
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
    exec(open(os.path.join(HERE, "derivar_encanamento_v396_regras.py"), encoding="utf-8").read(), globals())
    rel = []
    for src, dst, regras in ENTRADAS:
        if so and os.path.basename(dst) not in so and dst not in so:
            continue
        r = aplicar(src, dst, regras); rel.append(r)
        print("%-46s %s regras=%d restam=%s" % (dst, r["destino_sha256"][:12], len(regras), r["palavras_de_conteudo_restantes"][:6]))
    if not so:
        json.dump({"contrato": "DERIVACAO_ENCANAMENTO_v396", "executado": False, "mapa": "394->395, 395->396 com fronteira de digitos", "arquivos": rel}, open(os.path.join(HERE, "DERIVACAO_ENCANAMENTO_v396.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
