# -*- coding: utf-8 -*-
"""v407 -- passo «gerar» do BUNDLE de 9 pedras no sandbox C:\\t\\k407c\\final (claude-prep-v407, 03/11/2026, a serviço da gerência c1).
Molde: preparar_bundle_v406_02nov.py (a v406 era 301 módulos em TGLExt/F1Fecho394; a v407 é UMA série de 9 módulos em TGLExt/).
Lê as 9 fontes (candidatas compiladas pela gerência no sandbox da v406 / v407), NORMALIZA cada uma (módulo sem o sufixo `Candidata`/`R1`; namespace idem; cabeçalho que diz o nome ratificado/dado pelo operador em 03/11/2026;
`#print axioms` finais removidos; nenhuma prova tocada), grava o resultado em v407\\pedra\\<Nome>.lean (a cópia durável) e no sandbox TGLExt\\<Nome>.lean; acrescenta à raiz TGLExt.lean os 9 imports;
escreve kernel_modulos_novos_v407.json e BUNDLE_v407.json (sha256 de cada módulo, fonte e sha256 da fonte) e o construir_kernel_v407.sh + o lançador sem janela.
Nada toca o Nós (só leitura). Não sobrescreve nada sem backup de bytes; se o sandbox já tem o módulo e difere, ABORTA.
Uso: C:\\Python314\\python.exe -I -B -X utf8 preparar_bundle_v407_03nov.py [--seco]"""
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
PK7 = Path(os.path.dirname(os.path.abspath(__file__)))
WK = PK7.parent.parent
K7 = Path("C:/t/k407c/final")
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel")
CUN = WK / "cunhagens_13out"
sha = lambda b: hashlib.sha256(b).hexdigest()

V_RATIF = CUN / "OPERADOR_03nov_decisoes_psion_graviton_estado_ligado_projetor_4x4_nomes_ratificados_teste_d_opcao_c_motor_banho_holografico_verbatim.txt"
V_PAR = CUN / "OPERADOR_03nov_nome_Par_e_vai_para_a_torre_verbatim.txt"
h_ratif, h_par = sha(V_RATIF.read_bytes())[:16], sha(V_PAR.read_bytes())[:16]
assert h_ratif == "73466598d3419fb0", h_ratif          # o prefixo que a ordem da gerência deu (o arquivo manda; divergência aborta)
assert "concordo com todos os nomes e os ratifico" in V_RATIF.read_text(encoding="utf-8") and "Concordo com o nome" in V_RATIF.read_text(encoding="utf-8")
assert "“Par”" in V_PAR.read_text(encoding="utf-8")

# (nome definitivo, fonte, namespace antigo, sufixo/nome antigo a tirar, ordem de import)
P3 = WK / "pedras_candidatas_03nov"
PEDRAS = [
    {"name": "PsionCanto", "src": P3 / "PsionCantoR1.lean", "old": "PsionCantoR1", "tipo": "03nov_nome_aceito", "sha16_da_ordem": "3794f8ccbc6be70b"},   # R2 da gerencia (03/11, 15h): fonte corrigida (BAIXOS 3, 6, 8)
    {"name": "Par", "src": P3 / "OParDePsionsR1.lean", "old": "OParDePsionsR1", "tipo": "03nov_nome_Par", "sha16_da_ordem": None},
    {"name": "APonteDoAtrito", "src": WK / "beta_calor_02nov" / "APonteDoAtritoCandidata.lean", "old": "APonteDoAtritoCandidata", "tipo": "02nov_ratificada", "sha16_da_ordem": None},
    {"name": "OUmInscrito", "src": WK / "fechamento_02nov" / "OUmInscritoCandidata.lean", "old": "OUmInscritoCandidata", "tipo": "02nov_ratificada", "sha16_da_ordem": None},
    {"name": "KEhATangente", "src": WK / "k_guarda_travessia_02nov" / "KEhATangenteCandidata.lean", "old": "KEhATangenteCandidata", "tipo": "02nov_ratificada", "sha16_da_ordem": None},
    {"name": "AChaveDaGuarda", "src": WK / "k_guarda_travessia_02nov" / "AChaveDaGuardaCandidata.lean", "old": "AChaveDaGuardaCandidata", "tipo": "02nov_ratificada", "sha16_da_ordem": None},
    {"name": "OGuarda", "src": WK / "k_guarda_travessia_02nov" / "OGuardaCandidata.lean", "old": "OGuardaCandidata", "tipo": "02nov_ratificada", "sha16_da_ordem": None},
    {"name": "LeituraPreservada", "src": WK / "rota_RE_dualidade_02nov" / "LeituraPreservadaCandidata.lean", "old": "LeituraPreservadaCandidata", "tipo": "02nov_ratificada", "sha16_da_ordem": None},
    {"name": "OIgual", "src": WK / "rota_RE_dualidade_02nov" / "OIgualCandidata.lean", "old": "OIgualCandidata", "tipo": "02nov_ratificada", "sha16_da_ordem": None},
]
NOMES_NOVOS = {p["old"]: p["name"] for p in PEDRAS}
CANDIDATAS_02 = [p["old"] for p in PEDRAS if p["tipo"] == "02nov_ratificada"]

HDR_02_A = "Candidata da gerencia c1 (02/11/2026). Nome provisorio: o nome e do operador. Fora do kernel selado."
HDR_02_B = "# Candidata da gerência c1 (02/11/2026), sobre a fala do operador. O nome é provisório: nomear é do operador."
NOVO_02_A = ("Pedra da gerencia c1 (02/11/2026); NOME RATIFICADO pelo operador em 03/11/2026 (verbatim sha16 `%s`: «concordo com todos os nomes e os ratifico»); entra no kernel na v407; "
             "compilada no sandbox da v407 (k407c/final), so no trio." % h_ratif)
NOVO_02_B = ("# Pedra da gerência c1 (02/11/2026), sobre a fala do operador; NOME RATIFICADO pelo operador em 03/11/2026 (verbatim sha16 `%s`: «concordo com todos os nomes e os ratifico»); entra no kernel na v407; "
             "compilada no sandbox da v407 (k407c/final), só no trio." % h_ratif)
HDR_PSION = ("  [TGLExt — pedra CANDIDATA da gerência c1, 03/11/2026; NOME PROVISÓRIO `PsionCantoR1`: os nomes das pedras são do operador;\n"
             "   compilada no sandbox da v406 (k406c/final), só no trio; instalar e nomear é decisão do operador; para a v407]")
NOVO_PSION = ("  [TGLExt — pedra da gerência c1, 03/11/2026; NOME ACEITO pelo operador em 03/11/2026 (verbatim sha16 `%s`: «Concordo com o nome»; o `R1` do arquivo da candidata era marca de revisão);\n"
              "   compilada no sandbox da v407 (k407c/final), só no trio; entra na v407]" % h_ratif)
HDR_PAR = ("  [TGLExt — pedra CANDIDATA da gerência c1, 03/11/2026; NOME PROVISÓRIO `OParDePsionsR1` (o nome é do operador); compilada no sandbox da v406 (k406c/final),\n"
           "   só no trio; para a v407]")
NOVO_PAR = ("  [TGLExt — pedra da gerência c1, 03/11/2026; NOME dado pelo operador em 03/11/2026: `Par` (verbatim sha16 `%s`, resposta «“Par”»); compilada no sandbox da v407 (k407c/final),\n"
            "   só no trio; entra na v407]" % h_par)

RX_PRINT = re.compile(r"^#print axioms .*\r?\n?", re.M)


def normalizar(p):
    b = p["src"].read_bytes()
    t = b.decode("utf-8")
    assert "\r\n" not in t, p["name"]                      # as fontes da gerência são LF
    old, new = p["old"], p["name"]
    if p["tipo"] == "03nov_nome_aceito":
        assert t.count(HDR_PSION) == 1, "cabecalho do PsionCanto nao casou"
        t = t.replace(HDR_PSION, NOVO_PSION)
    elif p["tipo"] == "03nov_nome_Par":
        assert t.count(HDR_PAR) == 1, "cabecalho do Par nao casou"
        t = t.replace(HDR_PAR, NOVO_PAR)
    else:
        n_a, n_b = t.count(HDR_02_A), t.count(HDR_02_B)
        assert n_a + n_b == 1, (p["name"], n_a, n_b)
        t = t.replace(HDR_02_A, NOVO_02_A).replace(HDR_02_B, NOVO_02_B)
    # nomes: o módulo/namespace e as menções a outras pedras do dia (a OIgualRestauradoCandidata, superada, NAO sobe: nao existe no kernel)
    for o, n in NOMES_NOVOS.items():
        t = re.sub(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(o), n, t)
    n_print = len(RX_PRINT.findall(t))
    t = RX_PRINT.sub("", t).rstrip("\n") + "\n"
    assert "sorry" not in t.replace("sem sorry", "").replace("Sem sorry", "").replace("0 sorry", ""), ("sorry no texto", p["name"])
    return b, t, n_print


saida = []
bundle = []
for p in PEDRAS:
    assert p["src"].exists(), p["src"]
    b, t, n_print = normalizar(p)
    h_src = sha(b)
    if p["sha16_da_ordem"]:
        assert h_src[:16] == p["sha16_da_ordem"], ("a fonte NAO e' a que a ordem pinou", p["name"], h_src[:16])
    out = t.encode("utf-8")
    rel = "TGLExt/%s.lean" % p["name"]
    dur = PK7 / "pedra" / ("%s.lean" % p["name"])
    sb = K7 / "TGLExt" / ("%s.lean" % p["name"])
    saida.append((p, out, rel, dur, sb, h_src, n_print, len(b)))

# raiz: a do Nós v406 + ROOT_SUFFIX
raiz_nos = (NOS / "TGLExt.lean").read_text(encoding="utf-8", newline="")
raiz_k7 = (K7 / "TGLExt.lean").read_text(encoding="utf-8", newline="")
nl = "\r\n" if "\r\n" in raiz_nos else "\n"
ROOT_SUFFIX = nl.join("import TGLExt.%s" % p["name"] for p in PEDRAS) + nl
if raiz_k7 == raiz_nos + ROOT_SUFFIX:
    raiz_ja = True
else:
    raiz_ja = False
    assert raiz_k7 == raiz_nos, "a raiz do k407c nao e a do Nos nem a do Nos + os 9 imports"
for p in PEDRAS:
    assert ("TGLExt." + p["name"]) not in raiz_nos, p["name"]
    assert not (NOS / "TGLExt" / ("%s.lean" % p["name"])).exists(), ("a pedra ja existe no Nos", p["name"])

if SECO:
    print("SECO: nada gravado;", [(s[0]["name"], len(s[1]), s[6]) for s in saida])
    sys.exit(0)

(PK7 / "pedra").mkdir(exist_ok=True)
(PK7 / "pedra" / "origem").mkdir(exist_ok=True)
for p, out, rel, dur, sb, h_src, n_print, nb in saida:
    # a cópia dos BYTES da fonte (origem) e a pedra normalizada (durável) -- sem sobrescrever o que difere
    og = PK7 / "pedra" / "origem" / p["src"].name
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
                   "n_print_axioms_removidos": n_print, "bytes": len(out), "status_integracao": "pedra_da_gerencia_03nov"})

if not raiz_ja:
    bak = K7 / ("TGLExt.lean.bak_" + TS)
    bak.write_bytes((K7 / "TGLExt.lean").read_bytes())
    (K7 / "TGLExt.lean").write_text(raiz_nos + ROOT_SUFFIX, encoding="utf-8", newline="")
assert (K7 / "TGLExt.lean").read_text(encoding="utf-8", newline="") == raiz_nos + ROOT_SUFFIX
rels = [b["rel"] for b in bundle]
(PK7 / "kernel_modulos_novos_v407.json").write_text(json.dumps({"novos": rels, "n": len(rels), "root_suffix": ROOT_SUFFIX, "gerado": TS}, ensure_ascii=False, indent=1), encoding="utf-8")
(PK7 / "BUNDLE_v407.json").write_text(json.dumps({"contrato": "BUNDLE_v407", "gerado": TS, "n": len(bundle), "verbatim_nomes": {"ratificacao_sha16": h_ratif, "par_sha16": h_par}, "root_suffix": ROOT_SUFFIX, "modulos": bundle},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
(PK7 / "kernel").mkdir(exist_ok=True)
sh = """#!/bin/sh
# Constroi o kernel do SANDBOX da v407 (C:\\t\\k407c\\final; nunca o do Nos): `lake build` INCREMENTAL (a v406 selada ja' esta compilada em .lake/build, copiada do Nos; os 9 modulos novos sao os unicos a compilar) e depois o Audit.
# Molde: construir_kernel_v406.sh. Marcas de tempo em kernel/construir_marcas.txt.
K="/c/t/k407c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v407/kernel"
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
(PK7 / "construir_kernel_v407.sh").write_text(sh, encoding="utf-8", newline="\n")
Path("C:/t/k407c/run_build.py").write_text(
    "import subprocess, sys\n"
    "sh = r'C:\\Program Files\\Git\\bin\\sh.exe'\n"
    "scr = r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v407\\construir_kernel_v407.sh'\n"
    "out = open(r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v407\\kernel\\construir_stdout.log', 'ab')\n"
    "r = subprocess.run([sh, scr], stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=r'C:\\t\\k407c\\final', creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)\n"
    "open(r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v407\\kernel\\construir_rc.txt', 'w').write(str(r.returncode))\n", encoding="utf-8")
print("bundle", len(bundle), "modulos; raiz +%d imports; sh e lancador gravados" % len(PEDRAS))
for b in bundle:
    print(" ", b["rel"], b["sha256"][:16], "fonte", b["sha16_origem"], "print_axioms_removidos", b["n_print_axioms_removidos"])
