# -*- coding: utf-8 -*-
"""v409 -- passo «gerar» do BUNDLE de DOIS módulos no sandbox C:\\t\\k409c\\final (claude-construtor-v409, 05/11/2026, a serviço da gerência c1).
Molde: preparar_bundle_v408_04nov.py. A v409 era UM módulo; pela ordem do operador de 05/11 («eu quero que entre tudo na versão 409 não deixar nada para a v410»; DESENHO_v409, AO LADO de ~18h)
passa a DOIS, nesta ordem: TraducaoTuring (o insumo REFEITO da R9: + a inscrição no psíon, + a fórmula é a fita, + a E28 no cabeçalho) e ParNaFaceDeFock (NOVO: a ligação do par na face de Fock).
As fontes JÁ estão normalizadas pela gerência (insumos\\<nome>.lean: módulo/namespace = nome final, cabeçalho final, compiladas no sandbox da v408 só no trio, 0 avisos; sha256 em
insumos\\RECIBO_PEDRAS_v409_NOMES.json, revisto às 16:53): este passo só CONFERE (sha256 de cada fonte == o recibo; `namespace TGLExt.<nome>` e `end TGLExt.<nome>` uma vez cada; nenhum sorry;
os `#print axioms` de cada fonte == as âncoras do recibo daquele módulo, na ordem; os imports do módulo já existem no kernel do Nós v408), REMOVE os `#print axioms` finais (nenhuma prova tocada),
NORMALIZA o fim de linha CRLF -> LF, grava v409\\pedra\\<nome>.lean (a cópia durável), pedra\\origem\\<nome>.lean (os bytes da fonte) e o sandbox TGLExt\\<nome>.lean; a raiz TGLExt.lean = a do Nós v408 + os DOIS imports;
escreve kernel_modulos_novos_v409.json e BUNDLE_v409.json e o construir_kernel_v409.sh + o lançador sem janela.
A TraducaoTuring ANTIGA (a da R8, 62 âncoras) sai do sandbox pelo mecanismo deste preparo: a cópia de bytes vai para C:\\t\\k409c\\quarentena_<ts>\\ (fora da árvore de fontes) e o arquivo é substituído
pelo novo; a cópia durável antiga em pedra\\ e a origem antiga em pedra\\origem\\ ganham backup de bytes (.bak_<ts>) ANTES de serem substituídas. A raiz antiga (um import) ganha backup.
Nada toca o Nós (só leitura). Uso: C:\\Python314\\python.exe -I -B -X utf8 preparar_bundle_v409_05nov.py [--seco]"""
import datetime
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PK9 = Path(os.path.dirname(os.path.abspath(__file__)))
WK = PK9.parent.parent
K9 = Path("C:/t/k409c/final")
QUAR = Path("C:/t/k409c") / ("quarentena_" + TS)
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel")
CUN = WK / "cunhagens_13out"
INS = PK9 / "insumos"
sha = lambda b: hashlib.sha256(b).hexdigest()

# a ORDEM da v409 e a ratificação dos nomes (05/11/2026): lida do arquivo; o sha16 e' MEDIDO aqui e gravado no BUNDLE (nunca digitado); e a ordem «tudo na v409» (05/11, ~18h)
V_ORDEM = CUN / "OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes_verbatim.txt"
t_ordem = V_ORDEM.read_text(encoding="utf-8")
for frase in ("Prossigamos para a próxima verão do um.py", "concordo com todos os nomes que foram dados"):
    assert frase in t_ordem, ("a fala da ordem/nomes nao traz o trecho esperado", frase)
h_ordem = sha(V_ORDEM.read_bytes())[:16]

RECIBO_P = INS / "RECIBO_PEDRAS_v409_NOMES.json"
RECIBO = json.loads(RECIBO_P.read_text(encoding="utf-8"))
assert RECIBO.get("versao") == "v409" and [m["modulo"] for m in RECIBO["modulos"]] == ["TGLExt.TraducaoTuring", "TGLExt.ParNaFaceDeFock"], "o recibo dos nomes (revisto) tem de trazer os DOIS modulos, nesta ordem"
V_TUDO = Path(RECIBO["ordem_tudo_na_v409"]["arquivo"])
assert V_TUDO.parent == CUN and sha(V_TUDO.read_bytes()) == RECIBO["ordem_tudo_na_v409"]["sha256"], "a ordem «tudo na v409» do recibo nao e' o arquivo lido aqui"
assert "eu quero que entre tudo na versão 409" in V_TUDO.read_text(encoding="utf-8"), "a fala da ordem «tudo na v409» nao traz o trecho esperado"
h_tudo = sha(V_TUDO.read_bytes())[:16]
REC_POR_NOME = {m["modulo"].split(".")[-1]: m for m in RECIBO["modulos"]}
assert sum(m["declaracoes_print_axioms"] for m in RECIBO["modulos"]) == len(RECIBO["ancoras"]) and all(m["declaracoes_print_axioms"] == m["no_trio"] and m["avisos"] == 0 for m in RECIBO["modulos"]), "o recibo nao diz todas no trio e 0 avisos"

PEDRAS = [{"name": "TraducaoTuring", "src": INS / "TraducaoTuring.lean", "old": "TraducaoTuring", "tipo": "05nov_nome_da_gerencia_ratificado_R1_a_R8__acrescimos_da_R9_DECLARADO",
           "frase_do_nome": "concordo com todos os nomes que foram dados"},
          {"name": "ParNaFaceDeFock", "src": INS / "ParNaFaceDeFock.lean", "old": "ParNaFaceDeFock", "tipo": "05nov_nome_da_gerencia_DECLARADO_ate_a_ratificacao",
           "frase_do_nome": "concordo com todos os nomes que foram dados"}]
RX_PRINT = re.compile(r"^#print axioms (\S+)[ \t]*\r?\n?", re.M)
RX_IMPORT = re.compile(r"^import (\S+)[ \t]*$", re.M)


def normalizar(p):
    rec = REC_POR_NOME[p["name"]]
    b = p["src"].read_bytes()
    assert sha(b) == rec["sha256"] and Path(rec["arquivo"]) == p["src"], ("a fonte em insumos\\ NAO e' a que o recibo dos nomes pinou", p["name"], sha(b)[:16])
    t = b.decode("utf-8")
    n_crlf = t.count("\r\n")
    assert t.count("\r") == n_crlf, "CR solto na fonte (nao e' so' fim de linha CRLF)"
    t = t.replace("\r\n", "\n")                              # NORMALIZACAO de fim de linha (so' o CR sai); o kernel e' LF
    n, old = p["name"], p["old"]
    assert old == n, "v409: a fonte ja' esta' normalizada; nada se renomeia"
    assert t.count("namespace TGLExt.%s\n" % n) == 1 and t.count("end TGLExt.%s\n" % n) == 1, ("modulo/namespace != nome", n)
    _tn = re.sub(r"\s+", " ", t)   # (o cabecalho quebra linha no meio da frase: confere-se com os espacos normalizados)
    _CAB = {"TraducaoTuring": ["o nome `TraducaoTuring` e os nomes das declarações das rodadas R1–R8 foram dados pela gerência e RATIFICADOS pelo operador em 05/11/2026",
                               "os nomes acrescentados depois dessa fala (a inscrição no psíon e a fórmula SAT) são da gerência e ficam [DECLARADO] até a ratificação", "entra na v409"],
            "ParNaFaceDeFock": ["o nome `ParNaFaceDeFock` e os nomes das declarações são da gerência e ficam [DECLARADO] até a ratificação", "entra na v409, por ordem do operador"]}   # (o estatuto do recibo revisto de 05/11 ~19h30)
    assert all(f_ in _tn for f_ in _CAB[n]), ("cabecalho do nome nao casou (o estatuto do recibo revisto)", n, [f_ for f_ in _CAB[n] if f_ not in _tn])
    assert "CANDIDATA" not in t and "candidata à v409" not in t and "PROVISÓRIO" not in t, ("o cabecalho ainda diz candidata/provisorio", n)
    prints = RX_PRINT.findall(t)
    esperadas = [a_ for a_ in RECIBO["ancoras"] if a_.startswith("TGLExt.%s." % n)]
    assert prints == esperadas and len(prints) == rec["declaracoes_print_axioms"], ("os #print axioms da fonte nao sao as ancoras do recibo, na ordem", n, len(prints), len(esperadas))
    for imp in RX_IMPORT.findall(t):                         # os imports do modulo ja' estao no kernel da v408 (TGLExt.* e TGL.*)
        if imp.startswith(("TGLExt.", "TGL.")):
            assert (NOS / (imp.replace(".", "/") + ".lean")).exists(), ("import do modulo ausente do kernel do Nos v408", imp)
    t = RX_PRINT.sub("", t).rstrip("\n") + "\n"
    assert "sorry" not in t.replace("sem sorry", "").replace("Sem sorry", "").replace("0 sorry", ""), ("sorry no texto", n)
    assert "#print" not in t and "#eval" not in t and "\r" not in t, n
    assert not re.search(r"^\s*axiom\s", t, re.M), ("declaracao axiom no modulo", n)
    return b, t, len(prints), n_crlf, rec, esperadas


saida = []
bundle = []
for p in PEDRAS:
    assert p["src"].exists(), p["src"]
    b, t, n_print, n_crlf, rec, anc = normalizar(p)
    out = t.encode("utf-8")
    rel = "TGLExt/%s.lean" % p["name"]
    dur = PK9 / "pedra" / ("%s.lean" % p["name"])
    sb = K9 / "TGLExt" / ("%s.lean" % p["name"])
    saida.append((p, out, rel, dur, sb, sha(b), n_print, len(b), n_crlf, rec, anc))

# raiz: a do Nós v408 + ROOT_SUFFIX (os DOIS imports, na ordem do bundle)
raiz_nos = (NOS / "TGLExt.lean").read_text(encoding="utf-8", newline="")
raiz_k9 = (K9 / "TGLExt.lean").read_text(encoding="utf-8", newline="")
nl = "\r\n" if "\r\n" in raiz_nos else "\n"
ROOT_SUFFIX = nl.join("import TGLExt.%s" % p["name"] for p in PEDRAS) + nl
SUFIXO_ANTIGO = "import TGLExt.TraducaoTuring" + nl                # (a raiz do bundle de UM modulo, antes da ordem «tudo na v409»)
assert raiz_k9 in (raiz_nos, raiz_nos + SUFIXO_ANTIGO, raiz_nos + ROOT_SUFFIX), "a raiz do k409c nao e a do Nos, nem a do Nos + o import antigo, nem a do Nos + os dois imports"
for p in PEDRAS:
    assert ("TGLExt." + p["name"]) not in raiz_nos, p["name"]
    assert not (NOS / "TGLExt" / ("%s.lean" % p["name"])).exists(), ("a pedra ja existe no Nos", p["name"])
assert all((NOS / "TGLExt" / ("%s.lean" % m)).exists() for m in ("TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP")), "o Nos nao e' a v408 selada (as quatro pedras da v408 ausentes)"

if SECO:
    print("SECO: nada gravado;", [(s[0]["name"], len(s[1]), s[6], "crlf->lf", s[8]) for s in saida], "| ordem/nomes sha16", h_ordem, "| tudo na v409 sha16", h_tudo)
    sys.exit(0)

(PK9 / "pedra").mkdir(exist_ok=True)
(PK9 / "pedra" / "origem").mkdir(exist_ok=True)
retirados = []


def _troca_com_backup(path, novo, no_lugar=True):
    """grava `novo` em `path`; se `path` existe e difere: backup de bytes ANTES (no lugar: .bak_<ts>; fora: na quarentena), conferido; nada se perde."""
    path = Path(path)
    if path.exists():
        velho = path.read_bytes()
        if velho == novo:
            return None
        if no_lugar:
            bk = path.parent / (path.name + ".bak_" + TS)
        else:
            bk = QUAR / path.relative_to(K9)
            bk.parent.mkdir(parents=True, exist_ok=True)
        bk.write_bytes(velho); assert bk.read_bytes() == velho
        retirados.append({"arquivo": str(path), "backup": str(bk), "sha256_antigo": sha(velho), "sha256_novo": sha(novo)})
    tmp = path.parent / (path.name + ".tmp_" + TS)
    tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo)
    os.replace(tmp, path)
    assert path.read_bytes() == novo
    return True


for p, out, rel, dur, sb, h_src, n_print, nb, n_crlf, rec, anc in saida:
    _troca_com_backup(PK9 / "pedra" / "origem" / p["src"].name, p["src"].read_bytes())
    _troca_com_backup(dur, out)
    _troca_com_backup(sb, out, no_lugar=False)                 # o modulo antigo do sandbox sai para a quarentena (fora da arvore de fontes do lake)
    assert sb.read_bytes() == dur.read_bytes() == out
    bundle.append({"rel": rel, "sha256": sha(out), "fonte_bancada": None, "origem": str(p["src"]), "sha256_origem": h_src, "sha16_origem": h_src[:16], "tipo_do_nome": p["tipo"], "nome_antigo": p["old"],
                   "frase_do_nome": p["frase_do_nome"], "origem_candidata": rec["origem"], "sha256_candidata": rec["origem_sha256"], "saida_lean": rec["saida"],
                   "n_print_axioms_removidos": n_print, "n_crlf_normalizados": n_crlf, "bytes": len(out), "status_integracao": "pedra_da_gerencia_05nov", "ancoras": list(anc)})

if raiz_k9 != raiz_nos + ROOT_SUFFIX:
    _troca_com_backup(K9 / "TGLExt.lean", (raiz_nos + ROOT_SUFFIX).encode("utf-8"))
assert (K9 / "TGLExt.lean").read_text(encoding="utf-8", newline="") == raiz_nos + ROOT_SUFFIX
rels = [b["rel"] for b in bundle]


def grava_txt(path, txt):
    path = Path(path)
    if path.exists():
        if path.read_bytes() == txt.encode("utf-8"):
            return
        (path.parent / (path.name + ".bak_" + TS)).write_bytes(path.read_bytes())
    tmp = path.parent / (path.name + ".tmp")
    tmp.write_bytes(txt.encode("utf-8"))
    assert tmp.stat().st_size == len(txt.encode("utf-8"))
    os.replace(tmp, path)


grava_txt(PK9 / "kernel_modulos_novos_v409.json", json.dumps({"novos": rels, "n": len(rels), "root_suffix": ROOT_SUFFIX, "gerado": TS}, ensure_ascii=False, indent=1))
grava_txt(PK9 / "BUNDLE_v409.json", json.dumps({"contrato": "BUNDLE_v409", "gerado": TS, "n": len(bundle),
                                                "verbatim_nomes": {"nomes_sha16": h_ordem, "ordem_sha16": h_ordem, "nomes_arquivo": V_ORDEM.name, "ordem_arquivo": V_ORDEM.name, "tudo_na_v409_sha16": h_tudo, "tudo_na_v409_arquivo": V_TUDO.name},
                                                "recibo_dos_nomes": str(RECIBO_P), "recibo_dos_nomes_sha256": sha(RECIBO_P.read_bytes()),
                                                "normalizacao": "remove os #print axioms finais e troca CRLF por LF (o kernel e' LF); nenhuma prova tocada",
                                                "retirados_do_sandbox_e_da_pedra": retirados, "quarentena": str(QUAR) if QUAR.exists() else None,
                                                "root_suffix": ROOT_SUFFIX, "modulos": bundle}, ensure_ascii=False, indent=1))
(PK9 / "kernel").mkdir(exist_ok=True)
sh = """#!/bin/sh
# Constroi o kernel do SANDBOX da v409 (C:\\t\\k409c\\final; nunca o do Nos): `lake build` INCREMENTAL (a v408 selada ja' esta compilada em .lake/build, copiada de C:\\t\\k408c\\final; os DOIS modulos novos,
# TraducaoTuring e ParNaFaceDeFock, sao os unicos a compilar) e depois o Audit. Molde: construir_kernel_v408.sh. Marcas de tempo em kernel/construir_marcas.txt. Gerado por preparar_bundle_v409_05nov.py (claude-construtor-v409, 05/11/2026).
K="/c/t/k409c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v409/kernel"
mkdir -p "$D"
for f in lake_build.log audit.log build_full.log; do [ -f "$D/$f" ] && cp -p "$D/$f" "$D/$f.bak_$(date +%Y%m%d_%H%M%S)"; done
cd "$K" || exit 9
echo "inicio $(date '+%Y-%m-%d %H:%M:%S')" > "$D/construir_marcas.txt"
echo "epoch_inicio=$(date +%s)" >> "$D/construir_marcas.txt"
/c/Users/rotol/.elan/bin/lake build > "$D/lake_build.log" 2>&1; rb=$?
echo "rc_build=$rb $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_build_fim=$(date +%s)" >> "$D/construir_marcas.txt"
/c/Users/rotol/.elan/bin/lake env lean TGL/Audit.lean > "$D/audit.log" 2>&1; ra=$?
echo "rc_audit=$ra $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_audit_fim=$(date +%s)" >> "$D/construir_marcas.txt"
if [ "$rb" = "0" ] && [ "$ra" = "0" ]; then echo "rc=0" >> "$D/construir_marcas.txt"; else echo "rc=1" >> "$D/construir_marcas.txt"; fi
echo "fim $(date '+%Y-%m-%d %H:%M:%S')" >> "$D/construir_marcas.txt"
cat "$D/construir_marcas.txt"
"""
grava_txt(PK9 / "construir_kernel_v409.sh", sh)
grava_txt("C:/t/k409c/run_build.py",
          "import subprocess, sys\n"
          "sh = r'C:\\Program Files\\Git\\bin\\sh.exe'\n"
          "scr = r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v409\\construir_kernel_v409.sh'\n"
          "out = open(r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v409\\kernel\\construir_stdout.log', 'ab')\n"
          "r = subprocess.run([sh, scr], stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=r'C:\\t\\k409c\\final', creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)\n"
          "open(r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v409\\kernel\\construir_rc.txt', 'w').write(str(r.returncode))\n")
print("bundle", len(bundle), "modulos; raiz +%d imports; sh e lancador gravados | ordem/nomes sha16 %s | tudo na v409 sha16 %s" % (len(PEDRAS), h_ordem, h_tudo))
for b in bundle:
    print(" ", b["rel"], b["sha256"][:16], "fonte", b["sha16_origem"], "print_axioms_removidos", b["n_print_axioms_removidos"], "crlf->lf", b["n_crlf_normalizados"], b["tipo_do_nome"])
for r_ in retirados:
    print("  retirado (com backup):", r_["arquivo"], "->", r_["backup"])
