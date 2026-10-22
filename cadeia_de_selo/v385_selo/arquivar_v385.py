# -*- coding: utf-8 -*-
"""Arquiva o pacote v385 e a cadeia v385_selo em C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v385 e \\v385_selo (molde: arquivar_v384.py).
O pacote v385 tem ~3 GB (as pastas de afericao, os candidatos de 33 MB, os ensaios): arquivam-se SO os arquivos de topo (filtrados) e as pastas que sao
evidencia pequena e direta (a fumaca, as conferencias do congelamento, os rascunhos v13 apresentados, a 11a afericao); o resto fica dito no manifesto
(nao_arquivado, com o tamanho). Nunca: candidatos > 5 MB, PDFs/tex/aux, dotfiles de estado (.rito_v385.pid, .servidor_parado_pelo_rito, .vigia_ativo).
A CADEIA v385_selo vai por LISTA PERMITIDA (2o achado da revisao de 04/10), nunca por varredura: os scripts do topo (*.py, *.sh; sem .bak_/.tmp/.new),
as saidas do topo (*_out.txt), o manifesto e o JSON do mapa, e a pasta do CONFERIDOR desta cadeia (AMB['conf_dir']). As pastas de ensaio, de revisao
(revisao_*), do corretor e os Nos sinteticos ficam FORA por construcao; e qualquer arquivo da lista que venha de uma arvore marcada SINTETICO (a marca
SINTETICO_ENSAIO_V385.txt num diretorio acima dele, ou 'SINTETICO' num diretorio do caminho) e' RECUSA VISIVEL, conferida ANTES da primeira copia (nada e'
copiado). Copia byte a byte conferida; MANIFESTO_ARQUIVO_v385.json com sha256. Rodar DEPOIS da cadeia pos-rito e ANTES do handoff (a guarda do handoff
confere o AFERIDOR arquivado). Idempotente (substitui so se os bytes diferirem; nunca apaga).
Ensaio: com o Nos SINTETICO, o destino e' V385_ARQ_DEST (padrao v385_selo\\ensaio_arquivo) -- nunca o arquivo real."""
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v385 as A
AMB = A.ambiente()
DEST = AMB["arq_dest"]
EXCL_EXT = {".pdf", ".tex", ".aux", ".out", ".toc", ".pyc"}
LOG_OK = ("rito_servidor_v385.log", "build_full.log")   # v385: o log da construcao do kernel no sandbox (4 MB) e' evidencia da escada
MAX_B = 5 * 1024 * 1024
LONGO = chr(92) * 2 + "?" + chr(92)   # o prefixo de caminho longo do Windows
PASTAS_PK = ("kernel", "afericao_codigo", "afericao_texto", "pilar_anterior_v384_")   # v385: os relatorios do kernel do sandbox, as duas afericoes, o pilar anterior (copia de bytes)
SEL_EXT = (".py", ".sh")
SEL_SAIDAS = ("v385_incorporacao_manifesto.json", "registro_mapa_v385.json")
man = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "destino": DEST, "sintetico": AMB["sint"], "arquivos": {}, "nao_arquivado": {}}


def aceita(fn, b=None):
    ext = os.path.splitext(fn)[1].lower()
    if fn.startswith(".") or "SINTETICO" in fn.upper():
        return False
    if ext in EXCL_EXT:
        return False
    if ext == ".log" and not fn.startswith(LOG_OK):
        return False
    if ext == ".txt" and not ("stdout" in fn or "_out" in fn or fn.startswith(("AFERIDOR_", "rito_horarios_", "rito_v385_sinal", "diff_"))):
        return False
    return True


def de_arvore_sintetica(p, raiz):
    """True se o arquivo vem de uma arvore marcada SINTETICO: um diretorio do caminho (relativo a raiz) com 'SINTETICO' no nome, ou a marca
    SINTETICO_ENSAIO_V385.txt em qualquer diretorio entre o do arquivo e a raiz (inclusive)."""
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


# (0) a LISTA PERMITIDA da cadeia v385_selo, montada e conferida ANTES da primeira copia
LISTA_SEL = []
for fn in sorted(os.listdir(A.SEL)):
    p = os.path.join(A.SEL, fn)
    if not os.path.isfile(p):
        continue
    if ".bak_" in fn or ".tmp" in fn or fn.endswith(".new"):
        continue
    if fn.endswith(SEL_EXT) or fn.endswith("_out.txt") or fn in SEL_SAIDAS:
        if "SINTETICO" in fn.upper():
            man["nao_arquivado"]["v385_selo/" + fn] = {"bytes": os.path.getsize(p), "porque": "nome de ensaio (SINTETICO)"}; continue
        LISTA_SEL.append((p, fn))
_cd = AMB["conf_dir"]
if os.path.isdir(_cd):
    for fn in sorted(os.listdir(_cd)):
        p = os.path.join(_cd, fn)
        if os.path.isfile(p) and ".tmp" not in fn and ".bak_" not in fn:
            LISTA_SEL.append((p, "conferidor/" + fn))
else:
    man["nao_arquivado"]["v385_selo/conferidor/"] = {"bytes": 0, "porque": "a pasta do conferidor (%s) nao existe" % _cd}
_ruins = [p for p, _r in LISTA_SEL if de_arvore_sintetica(p, A.SEL)]
if _ruins:
    print("ARQUIVAR RECUSADO (falha visivel; NADA foi copiado): %d arquivo(s) da lista vem de arvore marcada SINTETICO: %s" % (len(_ruins), _ruins[:5])); sys.exit(3)
# (1) o pacote v385: topo filtrado + as pastas-evidencia pequenas
for fn in sorted(os.listdir(A.PK)):
    p = os.path.join(A.PK, fn)
    if os.path.isfile(p):
        if aceita(fn):
            copia(p, fn, "v385")
        else:
            man["nao_arquivado"]["v385/" + fn] = {"bytes": os.path.getsize(p), "porque": "filtro (extensao/dotfile/txt)"}
    elif os.path.isdir(p):
        if fn.startswith(PASTAS_PK):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                for f in files:
                    if aceita(f) and not de_arvore_sintetica(os.path.join(root, f), A.PK):
                        copia(os.path.join(root, f), os.path.relpath(os.path.join(root, f), A.PK), "v385")
        else:
            tot, ileg = 0, 0
            for r_, _d, fs in os.walk(p):
                for f in fs:
                    try:
                        tot += os.path.getsize(LONGO + os.path.abspath(os.path.join(r_, f)))   # caminho longo (> 260) no Windows
                    except OSError:
                        ileg += 1
            man["nao_arquivado"]["v385/" + fn + "/"] = {"bytes": tot, "ilegiveis": ileg, "porque": "pasta de trabalho (afericao/ensaio/teste), fora do arquivo"}
# (2) a cadeia v385_selo: SO a lista permitida (conferida em (0))
for p, rel in LISTA_SEL:
    copia(p, rel, "v385_selo")
_fora = sorted(d for d in os.listdir(A.SEL) if os.path.isdir(os.path.join(A.SEL, d)) and os.path.normcase(os.path.join(A.SEL, d)) != os.path.normcase(_cd))
man["nao_arquivado"]["v385_selo/<pastas>"] = {"bytes": 0, "porque": "fora da lista permitida (ensaios, revisoes, Nos sinteticos, copias): %s" % ", ".join(_fora)}
mp = A.pode_escrever(os.path.join(DEST, "v385_selo", "MANIFESTO_ARQUIVO_v385.json"), AMB); os.makedirs(os.path.dirname(mp), exist_ok=True)
open(mp + ".tmp", "wb").write(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8")); os.replace(mp + ".tmp", mp)
a = man["arquivos"]
print("arquivados:", sum(1 for v in a.values() if v["estado"] == "copiado"), "copiados;", sum(1 for v in a.values() if v["estado"] == "igual"), "iguais;",
      format(sum(v["bytes"] for v in a.values()), ","), "B; nao arquivados:", len(man["nao_arquivado"]), "itens,", format(sum(v["bytes"] for v in man["nao_arquivado"].values()), ","), "B;", mp)
print("da cadeia v385_selo (lista permitida): %d arquivo(s); nenhum de arvore SINTETICO" % len(LISTA_SEL))
for need in ("v385/AFERIDOR_v385.txt", "v385/disposicoes_afericoes_v385.json", "v385/conferir_rito_v385.py", "v385/ESPERADOS_v385.json"):
    assert need in a, "faltou arquivar: " + need
