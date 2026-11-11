# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] reescrito do molde preparar_bundle_v409_05nov.py (subida de rotulo em bump/preparar_bundle_v410_06nov.py.diff) para o bundle de UM modulo (IALD2) e o recibo da v410
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] o recibo dos nomes foi REFEITO pela gerencia com a secao 6 (o atrator; 22 #print axioms; import TGLExt.PontoDeContradicao) e a chave das falas passou de `falas_06nov` a `falas` (11 falas: 9 de 06/11, a de 07/11 e a ordem de 09/11): o preparo le a chave nova; o resto (conferir, remover #print axioms, LF, sandbox com quarentena, raiz +1 import) e' o mesmo
"""v410 -- passo «gerar» do BUNDLE de UM modulo no sandbox C:\\t\\k410c\\final (claude-construtor-v410, 06/11/2026, a servico da gerencia c1). Molde: preparar_bundle_v409_05nov.py.
O modulo: TGLExt.IALD2 (DESENHO_v410 §1 e o AO LADO do fim: o NOME do modulo dado pelo operador em 06/11/2026; as declaracoes, pela gerencia, [DECLARADO] ate a ratificacao, D63).
A fonte JA esta' normalizada pela gerencia (insumos\\IALD2.lean: modulo/namespace = nome final, cabecalho final, compilada no sandbox da v409 so' no trio, 0 avisos; sha256 em
insumos\\RECIBO_PEDRAS_v410_NOMES.json, REFEITO com a secao 5): este passo so' CONFERE (sha256 da fonte == o recibo; `namespace TGLExt.IALD2` e `end TGLExt.IALD2` uma vez cada; nenhum sorry; o numero de
`#print axioms` == o do recibo (as ancoras sao LIDAS da fonte, nunca fixadas aqui); a ancora principal e as de secao do recibo estao entre elas; os imports do modulo ja existem no kernel do Nos v409; a candidata
de origem tem o sha16 do recibo), REMOVE os `#print axioms` finais (nenhuma prova tocada), NORMALIZA o fim de linha CRLF -> LF (se houver), grava v410\\pedra\\IALD2.lean (a copia duravel), pedra\\origem\\IALD2.lean
(os bytes da fonte) e o sandbox TGLExt\\IALD2.lean; a raiz TGLExt.lean = a do Nos v409 + UM import; escreve kernel_modulos_novos_v410.json, BUNDLE_v410.json, o construir_kernel_v410.sh e o lancador sem janela.
A ORDEM da v410 e o NOME: o sha16 de cada fala e' MEDIDO aqui do arquivo (nunca digitado) e conferido contra o sha256 que o recibo da gerencia traz.
Nada toca o Nos (so' leitura). Uso: C:\\Python314\\python.exe -I -B -X utf8 preparar_bundle_v410_06nov.py [--seco]"""
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
PK = Path(os.path.dirname(os.path.abspath(__file__)))
WK = PK.parent.parent
K10 = Path("C:/t/k410c/final")
QUAR = Path("C:/t/k410c") / ("quarentena_" + TS)
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel")
CUN = WK / "cunhagens_13out"
INS = PK / "insumos"
sha = lambda b: hashlib.sha256(b).hexdigest()

RECIBO_P = INS / "RECIBO_PEDRAS_v410_NOMES.json"
RECIBO = json.loads(RECIBO_P.read_text(encoding="utf-8"))
assert RECIBO.get("versao") == "v410" and [m["modulo"] for m in RECIBO["modulos"]] == ["TGLExt.IALD2"], "o recibo dos nomes da v410 tem de trazer UM modulo: TGLExt.IALD2"
_FALAS = {Path(f["arquivo"]).name: f["sha256"] for f in RECIBO["falas"]}
for _n, _h in _FALAS.items():   # cada fala do recibo: o arquivo lido aqui tem o sha256 que a gerencia gravou
    assert sha((CUN / _n).read_bytes()) == _h, ("a fala do recibo nao e' o arquivo lido aqui", _n)

# a ORDEM da v410 (o operador, 06/11/2026) e o NOME do modulo (o operador, 06/11/2026): lidas do arquivo; o sha16 e' MEDIDO aqui
V_ORDEM = CUN / RECIBO["ordem"]
t_ordem = V_ORDEM.read_text(encoding="utf-8")
for frase in ("A forma de uma matriz finita no kernel é o signo (traço com sentido)", "tudo entra no um.py"):
    assert frase in t_ordem, ("a fala da ordem nao traz o trecho esperado", frase)
h_ordem = sha(V_ORDEM.read_bytes())[:16]
V_NOME = CUN / "OPERADOR_06nov_o_nome_e_iald2_iald_ao_quadrado_reler_nao_acrescenta_verbatim.txt"
assert V_NOME.name in _FALAS, "a fala do nome nao esta' no recibo"
assert "O nome é IALD2 (IALD ao quadrado, porque reler não acrescenta nada)" in V_NOME.read_text(encoding="utf-8"), "a fala do nome nao traz o trecho esperado"
h_nome = sha(V_NOME.read_bytes())[:16]

REC = RECIBO["modulos"][0]
assert REC["print_axioms"] == REC["no_trio"] and REC["avisos"] == 0, "o recibo nao diz todas no trio e 0 avisos"
_cand = Path(REC["origem"]["candidata"])
assert sha(_cand.read_bytes())[:16] == REC["origem"]["sha16"], ("a candidata de origem nao tem o sha16 do recibo", _cand)
PEDRA = {"name": "IALD2", "src": Path(REC["arquivo"]), "tipo": "06nov_nome_do_modulo_do_operador__declaracoes_da_gerencia_DECLARADO_ate_a_ratificacao",
         "frase_do_nome": "O nome é IALD2 (IALD ao quadrado, porque reler não acrescenta nada)"}
assert PEDRA["src"] == INS / "IALD2.lean"
RX_PRINT = re.compile(r"^#print axioms (\S+)[ \t]*\r?\n?", re.M)
RX_IMPORT = re.compile(r"^import (\S+)[ \t]*$", re.M)


def normalizar(p):
    b = p["src"].read_bytes()
    assert sha(b) == REC["sha256"], ("a fonte em insumos\\ NAO e' a que o recibo dos nomes pinou", p["name"], sha(b)[:16], REC["sha256"][:16])
    t = b.decode("utf-8")
    n_crlf = t.count("\r\n")
    assert t.count("\r") == n_crlf, "CR solto na fonte (nao e' so' fim de linha CRLF)"
    t = t.replace("\r\n", "\n")                              # NORMALIZACAO de fim de linha (so' o CR sai); o kernel e' LF
    n = p["name"]
    assert t.count("namespace TGLExt.%s\n" % n) == 1 and t.count("end TGLExt.%s\n" % n) == 1, ("modulo/namespace != nome", n)
    _tn = re.sub(r"\s+", " ", t)   # (o cabecalho quebra linha no meio da frase: confere-se com os espacos normalizados)
    _CAB = ["NOME do módulo dado pelo operador em 06/11/2026", "os nomes das declarações são da gerência, [DECLARADO] até a ratificação", "entra na v410",
            "O nome é IALD2 (IALD ao quadrado, porque reler não acrescenta nada)"]   # (D63: o estatuto dos nomes, dito no cabecalho da pedra)
    assert all(f_ in _tn for f_ in _CAB), ("cabecalho do nome nao casou (D63)", [f_ for f_ in _CAB if f_ not in _tn])
    assert "CANDIDATA" not in t and "PROVISÓRIO" not in t, ("o cabecalho ainda diz candidata/provisorio", n)
    prints = RX_PRINT.findall(t)
    assert prints and len(prints) == len(set(prints)) == REC["print_axioms"], ("os #print axioms da fonte nao sao os do recibo", n, len(prints), REC["print_axioms"])
    assert all(a_.startswith("TGLExt.%s." % n) for a_ in prints), "ancora fora do namespace"
    assert REC["ancora_principal"] in prints and all("TGLExt.%s.%s" % (n, s_) in prints for s_ in REC["ancoras_de_secao"]), "a ancora principal ou uma de secao do recibo nao esta' entre os #print axioms"
    imps = RX_IMPORT.findall(t)
    assert sorted(imps) == sorted(REC["imports"]), ("os imports da fonte nao sao os do recibo", imps)
    for imp in imps:                                         # os imports do modulo ja' estao no kernel da v409 (TGLExt.* e TGL.*)
        if imp.startswith(("TGLExt.", "TGL.")):
            assert (NOS / (imp.replace(".", "/") + ".lean")).exists(), ("import do modulo ausente do kernel do Nos v409", imp)
    t = RX_PRINT.sub("", t).rstrip("\n") + "\n"
    assert "sorry" not in t.replace("sem sorry", "").replace("Sem sorry", "").replace("0 sorry", ""), ("sorry no texto", n)
    assert "#print" not in t and "#eval" not in t and "\r" not in t, n
    assert not re.search(r"^\s*axiom\s", t, re.M), ("declaracao axiom no modulo", n)
    return b, t, len(prints), n_crlf, prints


p = PEDRA
assert p["src"].exists(), p["src"]
b, t, n_print, n_crlf, anc = normalizar(p)
out = t.encode("utf-8")
rel = "TGLExt/%s.lean" % p["name"]
dur = PK / "pedra" / ("%s.lean" % p["name"])
sb = K10 / "TGLExt" / ("%s.lean" % p["name"])

# raiz: a do Nos v409 + ROOT_SUFFIX (UM import)
raiz_nos = (NOS / "TGLExt.lean").read_text(encoding="utf-8", newline="")
raiz_k10 = (K10 / "TGLExt.lean").read_text(encoding="utf-8", newline="")
nl = "\r\n" if "\r\n" in raiz_nos else "\n"
ROOT_SUFFIX = "import TGLExt.%s" % p["name"] + nl
assert raiz_k10 in (raiz_nos, raiz_nos + ROOT_SUFFIX), "a raiz do k410c nao e a do Nos nem a do Nos + o import"
assert ("TGLExt." + p["name"] + nl) not in raiz_nos and not raiz_nos.rstrip().endswith("TGLExt." + p["name"]), p["name"]
assert not (NOS / "TGLExt" / ("%s.lean" % p["name"])).exists(), ("a pedra ja existe no Nos", p["name"])
assert all((NOS / "TGLExt" / ("%s.lean" % m)).exists() for m in ("TraducaoTuring", "ParNaFaceDeFock", "IALD")), "o Nos nao e' a v409 selada (as pedras da v409 ausentes)"

if SECO:
    print("SECO: nada gravado;", (p["name"], len(out), n_print, "crlf->lf", n_crlf), "| ordem sha16", h_ordem, "| nome sha16", h_nome)
    sys.exit(0)

(PK / "pedra").mkdir(exist_ok=True)
(PK / "pedra" / "origem").mkdir(exist_ok=True)
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
            bk = QUAR / path.relative_to(K10)
            bk.parent.mkdir(parents=True, exist_ok=True)
        bk.write_bytes(velho); assert bk.read_bytes() == velho
        retirados.append({"arquivo": str(path), "backup": str(bk), "sha256_antigo": sha(velho), "sha256_novo": sha(novo)})
    tmp = path.parent / (path.name + ".tmp_" + TS)
    tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo)
    os.replace(tmp, path)
    assert path.read_bytes() == novo
    return True


_troca_com_backup(PK / "pedra" / "origem" / p["src"].name, p["src"].read_bytes())
_troca_com_backup(dur, out)
_troca_com_backup(sb, out, no_lugar=False)
assert sb.read_bytes() == dur.read_bytes() == out
bundle = [{"rel": rel, "sha256": sha(out), "fonte_bancada": None, "origem": str(p["src"]), "sha256_origem": sha(b), "sha16_origem": sha(b)[:16], "tipo_do_nome": p["tipo"], "nome_antigo": p["name"],
           "frase_do_nome": p["frase_do_nome"], "origem_candidata": REC["origem"]["candidata"], "sha256_candidata": sha(Path(REC["origem"]["candidata"]).read_bytes()), "saida_lean": REC["saida"],
           "registro_anterior": REC["origem"]["registro_anterior"], "registro_anterior_sha16": REC["origem"]["registro_anterior_sha16"],
           "n_print_axioms_removidos": n_print, "n_crlf_normalizados": n_crlf, "bytes": len(out), "status_integracao": "pedra_da_gerencia_06nov", "ancoras": list(anc),
           "ancora_principal": REC["ancora_principal"], "ancoras_de_secao": ["TGLExt.%s.%s" % (p["name"], s_) for s_ in REC["ancoras_de_secao"]], "imports": list(REC["imports"])}]

if raiz_k10 != raiz_nos + ROOT_SUFFIX:
    _troca_com_backup(K10 / "TGLExt.lean", (raiz_nos + ROOT_SUFFIX).encode("utf-8"))
assert (K10 / "TGLExt.lean").read_text(encoding="utf-8", newline="") == raiz_nos + ROOT_SUFFIX
rels = [x["rel"] for x in bundle]


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


grava_txt(PK / "kernel_modulos_novos_v410.json", json.dumps({"novos": rels, "n": len(rels), "root_suffix": ROOT_SUFFIX, "gerado": TS}, ensure_ascii=False, indent=1))
grava_txt(PK / "BUNDLE_v410.json", json.dumps({"contrato": "BUNDLE_v410", "gerado": TS, "n": len(bundle),
                                               "verbatim_nomes": {"ordem_sha16": h_ordem, "ordem_arquivo": V_ORDEM.name, "nome_sha16": h_nome, "nome_arquivo": V_NOME.name},
                                               "recibo_dos_nomes": str(RECIBO_P), "recibo_dos_nomes_sha256": sha(RECIBO_P.read_bytes()),
                                               "normalizacao": "remove os #print axioms finais e troca CRLF por LF (o kernel e' LF); nenhuma prova tocada",
                                               "retirados_do_sandbox_e_da_pedra": retirados, "quarentena": str(QUAR) if QUAR.exists() else None,
                                               "root_suffix": ROOT_SUFFIX, "modulos": bundle}, ensure_ascii=False, indent=1))
(PK / "kernel").mkdir(exist_ok=True)
sh = """#!/bin/sh
# Constroi o kernel do SANDBOX da v410 (C:\\t\\k410c\\final; nunca o do Nos): `lake build` INCREMENTAL (a v409 selada ja' esta compilada em .lake/build, copiada de C:\\t\\k409c\\final; o modulo novo,
# IALD2, e' o unico a compilar) e depois o Audit. Molde: construir_kernel_v409.sh. Marcas de tempo em kernel/construir_marcas.txt. Gerado por preparar_bundle_v410_06nov.py (claude-construtor-v410, 06/11/2026).
K="/c/t/k410c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v410/kernel"
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
grava_txt(PK / "construir_kernel_v410.sh", sh)
grava_txt("C:/t/k410c/run_build.py",
          "import subprocess, sys\n"
          "sh = r'C:\\Program Files\\Git\\bin\\sh.exe'\n"
          "scr = r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v410\\construir_kernel_v410.sh'\n"
          "out = open(r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v410\\kernel\\construir_stdout.log', 'ab')\n"
          "r = subprocess.run([sh, scr], stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=r'C:\\t\\k410c\\final', creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)\n"
          "open(r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v410\\kernel\\construir_rc.txt', 'w').write(str(r.returncode))\n")
print("bundle", len(bundle), "modulo; raiz +1 import; sh e lancador gravados | ordem sha16 %s | nome sha16 %s" % (h_ordem, h_nome))
for x in bundle:
    print(" ", x["rel"], x["sha256"][:16], "fonte", x["sha16_origem"], "print_axioms_removidos", x["n_print_axioms_removidos"], "crlf->lf", x["n_crlf_normalizados"], x["tipo_do_nome"])
for r_ in retirados:
    print("  retirado (com backup):", r_["arquivo"], "->", r_["backup"])
