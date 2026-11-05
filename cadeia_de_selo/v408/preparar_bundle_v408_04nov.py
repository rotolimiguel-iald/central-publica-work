# -*- coding: utf-8 -*-
"""v408 -- passo «gerar» do BUNDLE de 4 pedras no sandbox C:\\t\\k408c\\final (claude-construtor-v408, 04/11/2026, a serviço da gerência c1).
Molde: preparar_bundle_v407_03nov.py (a v407 era 9 módulos em TGLExt/; a v408 é UMA série de 4 módulos em TGLExt/, na ordem do DESENHO_v408 §1:
TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, Dicionario). As fontes JÁ estão normalizadas pela gerência (insumos\\<Nome>.lean: módulo/namespace = nome final,
cabeçalhos finais, compiladas no sandbox da v407 só no trio; sha256 em insumos\\RECIBO_PEDRAS_v408_NOMES.json): este passo só CONFERE (sha256 da fonte == o recibo; `namespace TGLExt.<Nome>`
e `end TGLExt.<Nome>` uma vez cada; nenhum sorry), REMOVE os `#print axioms` finais (nenhuma prova tocada), grava v408\\pedra\\<Nome>.lean (a cópia durável), pedra\\origem\\<Nome>.lean
(os bytes da fonte) e o sandbox TGLExt\\<Nome>.lean; acrescenta à raiz TGLExt.lean os 4 imports; escreve kernel_modulos_novos_v408.json e BUNDLE_v408.json (sha256 de cada módulo, fonte e
sha256 da fonte) e o construir_kernel_v408.sh + o lançador sem janela. Nada toca o Nós (só leitura). Não sobrescreve nada sem backup de bytes; se o sandbox já tem o módulo e difere, ABORTA.
Uso: C:\\Python314\\python.exe -I -B -X utf8 preparar_bundle_v408_04nov.py [--seco]"""
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
PK8 = Path(os.path.dirname(os.path.abspath(__file__)))
WK = PK8.parent.parent
K8 = Path("C:/t/k408c/final")
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel")
CUN = WK / "cunhagens_13out"
INS = PK8 / "insumos"
sha = lambda b: hashlib.sha256(b).hexdigest()

# as falas dos nomes (04/11/2026): lidas do arquivo; o sha16 e' MEDIDO aqui e gravado no BUNDLE (nunca digitado)
V_NOMES = CUN / "OPERADOR_04nov_nomes_das_pedras_ponto_de_contradicao_p_igual_np_tempo_igual_moeda_tetelestai_terminal_e_inclinacao_modular_verbatim.txt"
V_ORDEM = CUN / "OPERADOR_04nov_ordem_v408_liste_as_pedras_produza_rode_handoff_custodia_completa_verbatim.txt"
t_nomes = V_NOMES.read_text(encoding="utf-8")
for frase in ("1) Ponto de contradição", "2) P=nP", "3) Tempo=moeda", "4) TetelestaiTerminal", "inclinação modular (cociclo)"):
    assert frase in t_nomes, ("a fala dos nomes nao traz o trecho esperado", frase)
assert "produza a v408" in V_ORDEM.read_text(encoding="utf-8")
h_nomes, h_ordem = sha(V_NOMES.read_bytes())[:16], sha(V_ORDEM.read_bytes())[:16]

RECIBO = json.loads((INS / "RECIBO_PEDRAS_v408_NOMES.json").read_text(encoding="utf-8"))
REC_POR_NOME = {Path(p["destino"]).stem: p for p in RECIBO["pedras"]}
# [04/11, tarde: MUDANCA DE INSUMO da gerencia] o 4o modulo e' PIgualNP (o operador deu o sentido de «P=nP», sha16 971d5654e2173771; o Dicionario fica SUPERADO e nao entra); a ordem do bundle vem do proprio recibo
assert {"TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP"} <= set(REC_POR_NOME), sorted(REC_POR_NOME)
assert RECIBO.get("ordem_do_bundle") == ["TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP"], RECIBO.get("ordem_do_bundle")
assert REC_POR_NOME["PIgualNP"].get("estado") == "VIGENTE" and str(REC_POR_NOME.get("Dicionario", {}).get("estado", "")).startswith("SUPERADO"), "o recibo dos nomes nao diz PIgualNP VIGENTE e Dicionario SUPERADO"
V_SENTIDO = CUN / "OPERADOR_04nov_p_igual_np_porque_p_sozinho_e_impossivel_de_ser_lido_sem_o_modulo_de_leitura_n_acoplado_verbatim.txt"
assert "P sozinho é impossível de ser lido, se não houver o módulo de leitura n não minimamente acoplado" in V_SENTIDO.read_text(encoding="utf-8")
h_sentido = sha(V_SENTIDO.read_bytes())[:16]
assert h_sentido == "971d5654e2173771", ("o arquivo do sentido de «P=nP» NAO tem o prefixo que a gerencia deu", h_sentido)   # (o prefixo da ordem da gerencia; o arquivo manda)

# (nome definitivo, fonte normalizada, tipo do nome) -- a ORDEM e' a do DESENHO_v408 §1 + AO LADO (a ordem dos imports na raiz e do ledger)
PEDRAS = [
    {"name": "TetelestaiTerminal", "src": INS / "TetelestaiTerminal.lean", "old": "TetelestaiTerminal", "tipo": "04nov_nome_do_operador", "frase_do_nome": "4) TetelestaiTerminal"},
    {"name": "TempoIgualMoeda", "src": INS / "TempoIgualMoeda.lean", "old": "TempoIgualMoeda", "tipo": "04nov_nome_do_operador", "frase_do_nome": "3) Tempo=moeda"},
    {"name": "PontoDeContradicao", "src": INS / "PontoDeContradicao.lean", "old": "PontoDeContradicao", "tipo": "04nov_nome_do_operador", "frase_do_nome": "1) Ponto de contradição"},
    {"name": "PIgualNP", "src": INS / "PIgualNP.lean", "old": "PIgualNP", "tipo": "04nov_nome_do_operador", "frase_do_nome": "2) P=nP"},
]
RX_PRINT = re.compile(r"^#print axioms .*\r?\n?", re.M)


def normalizar(p):
    b = p["src"].read_bytes()
    t = b.decode("utf-8")
    assert "\r\n" not in t, p["name"]                      # as fontes da gerência são LF
    assert sha(b) == REC_POR_NOME[p["name"]]["sha256"], ("a fonte em insumos\\ NAO e' a que o recibo dos nomes pinou", p["name"], sha(b)[:16])
    n, old = p["name"], p["old"]
    assert old == n, "v408: as fontes ja' estao normalizadas; nada se renomeia"
    assert t.count("namespace TGLExt.%s\n" % n) == 1 and t.count("end TGLExt.%s\n" % n) == 1, ("modulo/namespace != nome", n)
    assert ("nome do operador (04/11): «" in t) or ("NOME dado pelo operador em 04/11/2026: «P=nP»" in t and n == "PIgualNP"), ("cabecalho do nome nao casou", n)
    assert "PROVISÓRIO" not in t, ("nenhum nome provisorio resta no bundle (D48 resolvida)", n)
    # (r2, 05/11: a revisao de terceiro R1 pediu, BAIXO, o cabecalho sem «CANDIDATA»; a gerencia o trocou nas quatro fontes por «entra na v408»: o assert segue o cabecalho NOVO e recusa o velho)
    assert "entra na v408" in t and "candidata à v408" not in t and "CANDIDATA" not in t, ("o cabecalho nao diz «entra na v408» (ou ainda diz candidata)", n)
    n_print = len(RX_PRINT.findall(t))
    assert n_print > 0, ("a fonte nao traz #print axioms (as ancoras sao lidas deles)", n)
    t = RX_PRINT.sub("", t).rstrip("\n") + "\n"
    assert "sorry" not in t.replace("sem sorry", "").replace("Sem sorry", "").replace("0 sorry", ""), ("sorry no texto", n)
    assert "#print" not in t and "#eval" not in t, n
    return b, t, n_print


saida = []
bundle = []
for p in PEDRAS:
    assert p["src"].exists(), p["src"]
    b, t, n_print = normalizar(p)
    out = t.encode("utf-8")
    rel = "TGLExt/%s.lean" % p["name"]
    dur = PK8 / "pedra" / ("%s.lean" % p["name"])
    sb = K8 / "TGLExt" / ("%s.lean" % p["name"])
    saida.append((p, out, rel, dur, sb, sha(b), n_print, len(b)))

# raiz: a do Nós v407 + ROOT_SUFFIX (4 imports)
raiz_nos = (NOS / "TGLExt.lean").read_text(encoding="utf-8", newline="")
raiz_k8 = (K8 / "TGLExt.lean").read_text(encoding="utf-8", newline="")
nl = "\r\n" if "\r\n" in raiz_nos else "\n"
ROOT_SUFFIX = nl.join("import TGLExt.%s" % p["name"] for p in PEDRAS) + nl
if raiz_k8 == raiz_nos + ROOT_SUFFIX:
    raiz_ja = True
else:
    raiz_ja = False
    assert raiz_k8 == raiz_nos, "a raiz do k408c nao e a do Nos nem a do Nos + os 4 imports"
for p in PEDRAS:
    assert ("TGLExt." + p["name"]) not in raiz_nos, p["name"]
    assert not (NOS / "TGLExt" / ("%s.lean" % p["name"])).exists(), ("a pedra ja existe no Nos", p["name"])
    assert (NOS / "TGLExt" / "PsionCanto.lean").exists() and (NOS / "TGLExt" / "Par.lean").exists(), "o Nos nao e' a v407 selada (PsionCanto/Par ausentes)"

if SECO:
    print("SECO: nada gravado;", [(s[0]["name"], len(s[1]), s[6]) for s in saida], "| nomes sha16", h_nomes, "| ordem sha16", h_ordem)
    sys.exit(0)

(PK8 / "pedra").mkdir(exist_ok=True)
(PK8 / "pedra" / "origem").mkdir(exist_ok=True)
for p, out, rel, dur, sb, h_src, n_print, nb in saida:
    og = PK8 / "pedra" / "origem" / p["src"].name
    if og.exists():
        assert og.read_bytes() == p["src"].read_bytes(), ("a copia da origem difere", og.name)
    else:
        og.write_bytes(p["src"].read_bytes())
    if dur.exists():
        assert dur.read_bytes() == out, ("a pedra normalizada em pedra\\ difere do que a normalizacao gera: apague-a pela gerencia se for refazer", dur.name)
    else:
        dur.write_bytes(out)
    if sb.exists():
        assert sb.read_bytes() == out, ("o sandbox ja tem o modulo e DIFERE", sb.name)
    else:
        sb.write_bytes(out)
    assert sb.read_bytes() == dur.read_bytes() == out
    bundle.append({"rel": rel, "sha256": sha(out), "fonte_bancada": None, "origem": str(p["src"]), "sha256_origem": h_src, "sha16_origem": h_src[:16], "tipo_do_nome": p["tipo"], "nome_antigo": p["old"],
                   "frase_do_nome": p["frase_do_nome"], "origem_candidata": REC_POR_NOME[p["name"]]["origem"], "sha256_candidata": REC_POR_NOME[p["name"]]["origem_sha256"],
                   "n_print_axioms_removidos": n_print, "bytes": len(out), "status_integracao": "pedra_da_gerencia_04nov"})

if not raiz_ja:
    bak = K8 / ("TGLExt.lean.bak_" + TS)
    bak.write_bytes((K8 / "TGLExt.lean").read_bytes())
    (K8 / "TGLExt.lean").write_text(raiz_nos + ROOT_SUFFIX, encoding="utf-8", newline="")
assert (K8 / "TGLExt.lean").read_text(encoding="utf-8", newline="") == raiz_nos + ROOT_SUFFIX
rels = [b["rel"] for b in bundle]
(PK8 / "kernel_modulos_novos_v408.json").write_text(json.dumps({"novos": rels, "n": len(rels), "root_suffix": ROOT_SUFFIX, "gerado": TS}, ensure_ascii=False, indent=1), encoding="utf-8")
(PK8 / "BUNDLE_v408.json").write_text(json.dumps({"contrato": "BUNDLE_v408", "gerado": TS, "n": len(bundle), "verbatim_nomes": {"nomes_sha16": h_nomes, "ordem_sha16": h_ordem, "nomes_arquivo": V_NOMES.name, "ordem_arquivo": V_ORDEM.name, "sentido_p_igual_np_sha16": h_sentido, "sentido_p_igual_np_arquivo": V_SENTIDO.name},
                                                  "recibo_dos_nomes": str(INS / "RECIBO_PEDRAS_v408_NOMES.json"), "recibo_dos_nomes_sha256": sha((INS / "RECIBO_PEDRAS_v408_NOMES.json").read_bytes()),
                                                  "root_suffix": ROOT_SUFFIX, "modulos": bundle}, ensure_ascii=False, indent=1), encoding="utf-8")
(PK8 / "kernel").mkdir(exist_ok=True)
sh = """#!/bin/sh
# Constroi o kernel do SANDBOX da v408 (C:\\t\\k408c\\final; nunca o do Nos): `lake build` INCREMENTAL (a v407 selada ja' esta compilada em .lake/build, copiada do Nos; os 4 modulos novos sao os unicos a compilar) e depois o Audit.
# Molde: construir_kernel_v407.sh. Marcas de tempo em kernel/construir_marcas.txt.
K="/c/t/k408c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v408/kernel"
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
(PK8 / "construir_kernel_v408.sh").write_text(sh, encoding="utf-8", newline="\n")
Path("C:/t/k408c/run_build.py").write_text(
    "import subprocess, sys\n"
    "sh = r'C:\\Program Files\\Git\\bin\\sh.exe'\n"
    "scr = r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v408\\construir_kernel_v408.sh'\n"
    "out = open(r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v408\\kernel\\construir_stdout.log', 'ab')\n"
    "r = subprocess.run([sh, scr], stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=r'C:\\t\\k408c\\final', creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)\n"
    "open(r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v408\\kernel\\construir_rc.txt', 'w').write(str(r.returncode))\n", encoding="utf-8")
print("bundle", len(bundle), "modulos; raiz +%d imports; sh e lancador gravados | nomes sha16 %s | ordem sha16 %s" % (len(PEDRAS), h_nomes, h_ordem))
for b in bundle:
    print(" ", b["rel"], b["sha256"][:16], "fonte", b["sha16_origem"], "print_axioms_removidos", b["n_print_axioms_removidos"], b["tipo_do_nome"])
