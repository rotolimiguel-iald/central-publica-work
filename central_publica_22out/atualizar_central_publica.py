# -*- coding: utf-8 -*-
"""A CADEIA DA CENTRAL PÚBLICA NUM SÓ COMANDO (23/10/2026, sessão a7; ordem do operador: «atualizei o um.py ... já atualiza tudo
automaticamente»). Encadeia, na ordem em que foram rodados à mão em 22/10, os scripts que levam o estado corrente da Central aos três
repositórios públicos, ao /central/ do site e ao um.acom — e termina medindo o organismo. Cada passo é um script que já existe e já
foi medido; este arquivo só os chama, para e registra. Nada de novo entra no público sem a conferência independente (conferir_delta,
conferir_preparos, conferir_um_acom) e nenhum push ou subida acontece sem --publicar.

Grupos: repos (incrementais -> esteira -> README -> índice -> conferência do delta -> publicação) · site (retrato -> um.acom -> conferência
-> vínculo -> central_extra -> montagem -> conferência -> llms (Kimi, 23/10) -> sitemap -> manifesto -> subida em ensaio -> subida) · fim (estado do organismo).
Uso: atualizar_central_publica.py [--grupo repos|site|tudo] [--desde "AAAA-MM-DD HH:MM:SS"] [--so passo,passo] [--ate passo]
                                   [--publicar] [--titulo "título do commit"] [--listar]
Registro de cada rodada em rodadas/<data>.json (rc, segundos e a última linha de cada passo)."""
import argparse, json, shutil, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
PY, PYB = r"C:\Python314\python.exe", r"C:\IALD\Central de Patentes\backend\.venv\Scripts\python.exe"
CEN, PUB = Path(r"C:\IALD\Central de Patentes"), Path(r"C:\IALD\Central_publica")
BANC, SITE = Path(r"C:\IALD\Site\tgl\v3.0_bancada"), Path(r"C:\IALD\Site\tgl\v3.0")
REPOS = ("central-publica", "central-publica-work", "central-publica-bancada")
STAMP = time.strftime("%Y%m%d_%H%M%S")
MAN = BANC / "revisoes" / ("manifesto_central_publica_%s.json" % STAMP)
ap = argparse.ArgumentParser()
ap.add_argument("--grupo", default="tudo", choices=("repos", "site", "tudo"))
ap.add_argument("--desde", default=None)
ap.add_argument("--so", default=None)
ap.add_argument("--ate", default=None)
ap.add_argument("--publicar", action="store_true")
ap.add_argument("--titulo", default="Central aberta — atualização pela cadeia (%s)" % time.strftime("%d/%m/%Y"))
ap.add_argument("--listar", action="store_true")
a = ap.parse_args()


def copiar_acom_anterior():
    src = BANC / "central_publica" / "acom"
    dst = BANC / "central_publica" / ("acom_anterior_" + STAMP)
    shutil.copytree(src, dst)
    return "cópia do um.acom anterior em %s" % dst.name


P = []


def add(nome, grupo, argv=None, cwd=None, py=PY, publica=False, func=None):
    P.append({"nome": nome, "grupo": grupo, "argv": ([py, "-X", "utf8"] + argv) if argv else None, "cwd": str(cwd or W), "publica": publica, "func": func})


desde = ["--desde", a.desde] if a.desde else []
for tipo in ("nucleo", "work", "Chatgpt"):
    add("incremental_" + tipo, "repos", [str(W / "rodar_incremental.py"), tipo] + desde)
add("esteira_no_work", "repos", [str(W / "atualizar_pasta_no_preparo.py"), str(PUB / "central-publica-work"), "central_publica_22out"])
add("readmes", "repos", [str(W / "gerar_readmes_publicos.py"), str(PUB)], py=PYB)
for r in REPOS:
    add("indexar_raiz_" + r, "repos", [str(W / "indexar_raiz.py"), str(PUB / r)])
for r in REPOS:
    add("conferir_delta_" + r, "repos", [str(W / "conferir_delta.py"), str(PUB / r)] + ([] if r == "central-publica" else ["regiao"]))
for r in REPOS:
    add("publicar_" + r, "repos", [str(W / "atualizar_repo_publico.py"), r, str(PUB / r), a.titulo], publica=True)
add("retrato", "site", [str(W / "refazer_retrato.py")])
add("conferir_retrato", "site", [str(W / "conferir_retrato.py")])   # (24/10/2026) PORTAO: exportacao inteira (0 falhas; /api/classes e /api/patents no mapa) ou a rodada para
add("acom_anterior", "site", func=copiar_acom_anterior)
add("acom", "site", [str(W / "gerar_um_acom_publico.py"), str(BANC / "central_publica" / "acom")], cwd=CEN / "backend", py=PYB)
add("conferir_acom", "site", [str(W / "conferir_um_acom_publico.py"), str(BANC / "central_publica" / "acom" / "um.acom")], cwd=CEN / "backend", py=PYB)
add("vincular", "site", [str(W / "vincular_central_no_site.py")], py=PYB)
add("central_extra", "site", [str(W / "gerar_central_extra.py")])   # (24/10/2026) os contratos do organismo, pensamentos e custódias, ANTES do montar que os copia
add("montar", "site", [str(W / "montar_central_no_site.py")])
add("conferir_central", "site", [str(W / "conferir_preparos.py"), str(SITE / "central")])
add("llms_site", "site", [str(BANC / "tools" / "gerar_llms_site.py")], cwd=BANC)
add("sitemap", "site", [str(BANC / "tools" / "gerar_sitemap.py"), "--saida", str(SITE / "sitemap.xml"), "--base", str(SITE)], cwd=BANC)
add("manifesto", "site", [str(BANC / "tools" / "gerar_manifesto.py"), "--base", str(SITE), "--saida", str(MAN), "--url-base", "https://teoriadagravitacaoluminodinamica.com/"], cwd=BANC)
add("subir_ensaio", "site", [str(BANC / "tools" / "subir_site.py"), "--manifesto", str(MAN), "--dry-run"], cwd=BANC)
add("subir", "site", [str(BANC / "tools" / "subir_site.py"), "--manifesto", str(MAN)], cwd=BANC, publica=True)
add("estado_do_organismo", "fim", [str(CEN / "tools" / "estado_do_organismo.py")], cwd=CEN)

if a.listar:
    for p in P:
        print("%-36s %-6s %s" % (p["nome"], p["grupo"], "(só com --publicar)" if p["publica"] else ""))
    sys.exit(0)
so = set(a.so.split(",")) if a.so else None
sel = [p for p in P if (a.grupo == "tudo" or p["grupo"] in (a.grupo, "fim")) and (so is None or p["nome"] in so)]
if a.ate:
    sel = sel[: [p["nome"] for p in sel].index(a.ate) + 1]
log = {"rodada": STAMP, "args": vars(a), "passos": []}
(W / "rodadas").mkdir(exist_ok=True)
ok_geral = True
for p in sel:
    t0 = time.time()
    if p["publica"] and not a.publicar:
        print("  [%s] pulado (sem --publicar)" % p["nome"]); log["passos"].append({"nome": p["nome"], "estado": "pulado_sem_publicar"}); continue
    if p["func"]:
        try:
            msg = p["func"](); rc = 0
        except Exception as e:  # noqa: BLE001
            msg, rc = repr(e), 1
        ult, err = msg, ""
    else:
        r = subprocess.run(p["argv"], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=p["cwd"])
        rc = r.returncode
        linhas = [l for l in (r.stdout or "").splitlines() if l.strip() and not l.startswith(("Multiple definitions", "EOF marker"))]
        ult, err = (linhas[-1] if linhas else ""), (r.stderr or "")[-1200:]
    dt = time.time() - t0
    informativo = p["nome"] == "estado_do_organismo"   # rc 1/2 ali é medida, não falha da cadeia
    print("  [%s] rc=%d %.0f s | %s" % (p["nome"], rc, dt, ult[:300]), flush=True)
    log["passos"].append({"nome": p["nome"], "rc": rc, "segundos": round(dt), "ultima_linha": ult[:400], "stderr": err if rc else ""})
    if rc != 0 and not informativo:
        print(err); ok_geral = False
        print("PARADO em %s — os passos seguintes não rodaram" % p["nome"]); break
log["ok"] = ok_geral
(W / "rodadas" / (STAMP + ".json")).write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
print("rodada %s: %s | %d passo(s) | registro em rodadas/%s.json" % (STAMP, "COMPLETA" if ok_geral else "PARADA", len(log["passos"]), STAMP))
sys.exit(0 if ok_geral else 1)
