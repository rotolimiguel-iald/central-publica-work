# -*- coding: utf-8 -*-
"""Arquiva o pacote v386, os dados da v386 e a cadeia v386_selo em C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v386 e \\v386_selo (molde: arquivar_v385.py).
v386: o pacote vive em scratchpad\\v386\\pacote e os dados em scratchpad\\v386\\ (os quatro arquivos do operador, o ramo B, o kernel do sandbox, as afericoes).
Arquivam-se: os arquivos de topo de v386\\ e de v386\\pacote\\ (filtrados), a copia de bytes do pilar anterior (pacote\\pilar_anterior_v385_*; o details.jsonl
de 6,8 MB fica dito como nao arquivado, > 5 MB), e as pastas-evidencia pequenas de v386\\ (kernel, ramo_b, afericao_kernel_v1, afericao_texto_citacoes,
auditoria_texto, critico, lean_viabilidade, lente_linhagem_verbo, lente_triade). Ficam FORA, ditos no manifesto com o tamanho: pacote\\dry_v386 (101 MB: o
ensaio a seco, com o kernel materializado e os PDFs) e afericao_codigo (170 MB). Nunca: candidatos > 5 MB, PDFs/tex/aux/toc, dotfiles de estado.
A CADEIA v386_selo vai por LISTA PERMITIDA, nunca por varredura: os scripts do topo (*.py, *.sh; sem .bak_/.tmp/.new), as saidas do topo (*_out.txt), o
manifesto e o JSON do mapa, e a pasta do CONFERIDOR desta cadeia (AMB['conf_dir']). As pastas de ensaio e os Nos sinteticos ficam FORA por construcao; e
qualquer arquivo da lista que venha de uma arvore marcada SINTETICO e' RECUSA VISIVEL, conferida ANTES da primeira copia.
Copia byte a byte conferida; MANIFESTO_ARQUIVO_v386.json com sha256. Rodar DEPOIS da cadeia pos-rito e ANTES do handoff (a guarda do handoff confere o
CONSTRUIR e o conferidor arquivados). Idempotente (substitui so se os bytes diferirem; nunca apaga).
Ensaio: com o Nos SINTETICO, o destino e' V386_ARQ_DEST (padrao v386_selo\\ensaio_arquivo) -- nunca o arquivo real."""
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v386 as A
AMB = A.ambiente()
DEST = AMB["arq_dest"]
EXCL_EXT = {".pdf", ".tex", ".aux", ".toc", ".pyc"}
MAX_B = 5 * 1024 * 1024
LONGO = chr(92) * 2 + "?" + chr(92)
PASTAS_DAT = ("kernel", "ramo_b", "afericao_kernel_v1", "afericao_texto_citacoes", "auditoria_texto", "critico", "lean_viabilidade", "lente_linhagem_verbo", "lente_triade")
PASTAS_PK = ("pilar_anterior_v385_",)
SEL_EXT = (".py", ".sh")
SEL_SAIDAS = ("v386_incorporacao_manifesto.json", "registro_mapa_v386.json")
man = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "destino": DEST, "sintetico": AMB["sint"], "arquivos": {}, "nao_arquivado": {}}


def aceita(fn):
    ext = os.path.splitext(fn)[1].lower()
    if fn.startswith(".") or "SINTETICO" in fn.upper():
        return False
    if ext in EXCL_EXT:
        return False
    return True


def de_arvore_sintetica(p, raiz):
    d = os.path.dirname(os.path.abspath(p)); r = os.path.normcase(os.path.abspath(raiz))
    rel_dir = os.path.relpath(d, raiz)
    if rel_dir != "." and "SINTETICO" in rel_dir.upper():
        return True
    while True:
        if os.path.exists(os.path.join(d, A.MARCA_SINT)):
            return True
        if os.path.normcase(d) == r or not os.path.normcase(d).startswith(r) or os.path.dirname(d) == d:
            return False
        d = os.path.dirname(d)


def copia(src, rel, sub):
    b = open(src, "rb").read()
    if len(b) > MAX_B:
        man["nao_arquivado"][sub + "/" + rel.replace("\\", "/")] = {"bytes": len(b), "porque": "> 5 MB"}; return
    q = A.pode_escrever(os.path.join(DEST, sub, rel), AMB); os.makedirs(os.path.dirname(q), exist_ok=True)
    if os.path.exists(q) and open(q, "rb").read() == b:
        estado = "igual"
    else:
        tmp = q + ".tmp"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, q); estado = "copiado"
    man["arquivos"][sub + "/" + rel.replace("\\", "/")] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b), "estado": estado}


def tamanho(p):
    tot, ileg = 0, 0
    for r_, _d, fs in os.walk(p):
        for f in fs:
            try:
                tot += os.path.getsize(LONGO + os.path.abspath(os.path.join(r_, f)))
            except OSError:
                ileg += 1
    return tot, ileg


# (0) a LISTA PERMITIDA da cadeia v386_selo, montada e conferida ANTES da primeira copia
LISTA_SEL = []
for fn in sorted(os.listdir(A.SEL)):
    p = os.path.join(A.SEL, fn)
    if not os.path.isfile(p):
        continue
    if ".bak_" in fn or ".tmp" in fn or fn.endswith(".new"):
        continue
    if fn.endswith(SEL_EXT) or fn.endswith("_out.txt") or fn in SEL_SAIDAS:
        if "SINTETICO" in fn.upper():
            man["nao_arquivado"]["v386_selo/" + fn] = {"bytes": os.path.getsize(p), "porque": "nome de ensaio (SINTETICO)"}; continue
        LISTA_SEL.append((p, fn))
_cd = AMB["conf_dir"]
if os.path.isdir(_cd):
    for fn in sorted(os.listdir(_cd)):
        p = os.path.join(_cd, fn)
        if os.path.isfile(p) and ".tmp" not in fn and ".bak_" not in fn:
            LISTA_SEL.append((p, "conferidor/" + fn))
else:
    man["nao_arquivado"]["v386_selo/conferidor/"] = {"bytes": 0, "porque": "a pasta do conferidor (%s) nao existe" % _cd}
_ruins = [p for p, _r in LISTA_SEL if de_arvore_sintetica(p, A.SEL)]
if _ruins:
    print("ARQUIVAR RECUSADO (falha visivel; NADA foi copiado): %d arquivo(s) da lista vem de arvore marcada SINTETICO: %s" % (len(_ruins), _ruins[:5])); sys.exit(3)
# (1) os dados da v386 (topo filtrado + as pastas-evidencia pequenas) e o pacote (topo filtrado + o pilar anterior)
for raiz, sub, pastas in ((A.DAT, "v386", PASTAS_DAT), (A.PK, "v386/pacote", PASTAS_PK)):
    for fn in sorted(os.listdir(raiz)):
        p = os.path.join(raiz, fn)
        if os.path.isfile(p):
            if aceita(fn):
                copia(p, fn, sub)
            else:
                man["nao_arquivado"][sub + "/" + fn] = {"bytes": os.path.getsize(p), "porque": "filtro (extensao/dotfile)"}
        elif os.path.isdir(p):
            if fn == "__pycache__" or (raiz == A.DAT and fn == "pacote"):
                continue
            if fn.startswith(pastas):
                for root, dirs, files in os.walk(p):
                    dirs[:] = [d for d in dirs if d != "__pycache__"]
                    for f in files:
                        if aceita(f) and not de_arvore_sintetica(os.path.join(root, f), raiz):
                            copia(os.path.join(root, f), os.path.relpath(os.path.join(root, f), raiz), sub)
            else:
                tot, ileg = tamanho(p)
                man["nao_arquivado"][sub + "/" + fn + "/"] = {"bytes": tot, "ilegiveis": ileg, "porque": "pasta de trabalho (ensaio a seco / afericao de codigo), fora do arquivo"}
# (2) a cadeia v386_selo: SO a lista permitida (conferida em (0))
for p, rel in LISTA_SEL:
    copia(p, rel, "v386_selo")
_fora = sorted(d for d in os.listdir(A.SEL) if os.path.isdir(os.path.join(A.SEL, d)) and os.path.normcase(os.path.join(A.SEL, d)) != os.path.normcase(_cd))
man["nao_arquivado"]["v386_selo/<pastas>"] = {"bytes": 0, "porque": "fora da lista permitida (ensaios, Nos sinteticos, copias): %s" % ", ".join(_fora)}
mp = A.pode_escrever(os.path.join(DEST, "v386_selo", "MANIFESTO_ARQUIVO_v386.json"), AMB); os.makedirs(os.path.dirname(mp), exist_ok=True)
open(mp + ".tmp", "wb").write(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8")); os.replace(mp + ".tmp", mp)
a = man["arquivos"]
print("arquivados:", sum(1 for v in a.values() if v["estado"] == "copiado"), "copiados;", sum(1 for v in a.values() if v["estado"] == "igual"), "iguais;",
      format(sum(v["bytes"] for v in a.values()), ","), "B; nao arquivados:", len(man["nao_arquivado"]), "itens,", format(sum(v["bytes"] for v in man["nao_arquivado"].values()), ","), "B;", mp)
print("da cadeia v386_selo (lista permitida): %d arquivo(s); nenhum de arvore SINTETICO" % len(LISTA_SEL))
for need in ("v386/CONSTRUIR_v386_resultado.json", "v386/VERBO_operador_05out.txt", "v386/RESPOSTAS_operador_05out.txt", "v386/RESPOSTAS_operador_05out.json",
             "v386/ramo_b/DECISAO_OPERADOR_RAMO_B_05out.json", "v386/ramo_b/ESPEC_RUNTIME_RAMO_B_v386_ERRATA.json", "v386/kernel/PEDRA_v386_pos_build.json",
             "v386/pacote/conferir_rito_v386.py", "v386/pacote/ESPERADOS_v386.json", "v386/pacote/CANDIDATO_v386.json", "v386/pacote/v386_pins.py", "v386/pacote/v386_runtime.py"):
    assert need in a, "faltou arquivar: " + need
