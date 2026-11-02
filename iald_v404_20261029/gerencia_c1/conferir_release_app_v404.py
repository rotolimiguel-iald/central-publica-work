# -*- coding: utf-8 -*-
"""Conferência da gerência c1 (29/10/2026) da release do app v404 construída pela sessão do site (a7): hashes declarados = disco; recibos
do revisor distinto; identidade da release = pin do um.py do Nós (lido agora); quadro do organismo lendo o app em v404; git da Central
limpo e igual ao remoto; a frase superada do gate só no registro selado. Grava CONFERENCIA_GERENCIA_APP_V404_29out.json. Não instala nada."""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
B = Path("C:/IALD/Central de Patentes/work/iald_v404_20261029"); CEN = "C:/IALD/Central de Patentes"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
ck = []; add = lambda n, ok, d="": ck.append({"check": n, "ok": bool(ok), "detalhe": str(d)[:200]})
dec = {"INSTALLED_VERIFICATION.json": "638c278e37f33090", "receipts/v404-app-accept-r2.json": "50e7839c5b974cae", "receipts/v404-sources-accept-r2.json": "28baa5f5e305d14e",
       "receipts/v404-deploy-accept.json": "77aa46fec78ca00f", "receipts/v404-verify-accept.json": "bed816ee9cc9354e", "validation/review_final.json": "92affdfc296de67b"}
for f, s in dec.items():
    p = B / f; h = sha(p)[:16] if p.is_file() else "AUSENTE"; add("hash declarado pela sessão do site = disco: %s" % f, h == s, h)
iv = json.loads((B / "INSTALLED_VERIFICATION.json").read_text(encoding="utf-8"))
pin = sha("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py")
add("INSTALLED_VERIFICATION: PASS, release v404, source_sha256 = sha256 do um.py do Nós (lido agora), JEV v404, 0 chamadas a provedor",
    iv["status"] == "PASS" and iv["identity"]["release"] == "v404" and iv["identity"]["source_sha256"] == pin and iv["JEV_release"] == "v404" and iv["provider_calls"] == 0, pin[:16])
add("INSTALLED_VERIFICATION: commit público pinado = 1d3c4cbe (espelho com a ressalva corrigida)", iv["public_commit"].startswith("1d3c4cbe"), iv["public_commit"][:8])
rf = json.loads((B / "validation/review_final.json").read_text(encoding="utf-8"))
add("revisor distinto do construtor: review_final PASS por sonnet-app-v404-revisor", rf["status"] == "PASS" and rf["reviewer"] == "sonnet-app-v404-revisor", rf["timestamp"])
q = json.loads(Path(CEN, "organismo/ESTADO_DO_ORGANISMO.json").read_text(encoding="utf-8"))
itens = q.get("itens") or q.get("items") or []
app = [i for i in itens if i.get("superficie") == "App IALD (ciência própria)" and "release instalada" in i.get("item", "")]
from collections import Counter
c = Counter(i.get("estado") for i in itens)
add("quadro do organismo (%s): app lê v404; %d OK, %d DEFASADO, %d PENDENTE_OPERADOR" % (q.get("medido_em"), c.get("OK", 0), c.get("DEFASADO", 0), c.get("PENDENTE_OPERADOR", 0)),
    app and app[0].get("achado") == "v404" and app[0].get("estado") == "OK" and c.get("DEFASADO", 0) == 0, app[0].get("achado") if app else "sem item")
git = lambda *a: subprocess.run(["git", "-C", CEN] + list(a), capture_output=True, text=True).stdout.strip()
st = [l for l in git("status", "--porcelain").splitlines() if not l.startswith("??")]
add("git da Central: sem alterações rastreadas pendentes; HEAD = origin/main", not st and git("rev-parse", "HEAD") == git("rev-parse", "origin/main"), git("rev-parse", "--short", "HEAD"))
gs = json.loads((B / "GREP_SUPERSEDED_RESULT.json").read_text(encoding="utf-8")) if (B / "GREP_SUPERSEDED_RESULT.json").is_file() else None
add("a frase superada («15 calculadas e 3 literais») só no registro selado da v392, documentada pela revisão (GREP_SUPERSEDED_RESULT.json presente)", gs is not None, json.dumps(gs, ensure_ascii=False)[:160] if gs else "ausente")
prep = (B / "app/packages/shared/preparation.json").read_text(encoding="utf-8", errors="replace") if (B / "app/packages/shared/preparation.json").is_file() else ""
add("pacote shared cita bandeiras_do_gate_v403 e não a forma velha solta", "bandeiras_do_gate_v403" in prep and "3 literais" not in prep.replace("como registro", ""), prep.count("bandeiras_do_gate_v403"))
ok = all(x["ok"] for x in ck)
doc = {"schema": "iald.app-release.conferencia-gerencia/v1", "release": "v404", "em": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "conferente": "claude-c1 (gerência da Central)", "construtor": "sonnet-app-v404-construtor (sessão do site, a7)",
       "revisor": "sonnet-app-v404-revisor", "veredito": "CONFERIDA" if ok else "NAO_CONFERIDA", "n_checks": len(ck), "n_ok": sum(x["ok"] for x in ck), "checks": ck,
       "limites": ["Conferência de artefatos, hashes, quadro e git; não executa ciência, não inspeciona o celular, não mede resposta viva do modelo.", "A frase superada do gate permanece no um.py como registro selado da v392, citada como superada."]}
out = B / "gerencia_c1" / "CONFERENCIA_GERENCIA_APP_V404_29out.json"; tmp = out.with_suffix(".tmp")
tmp.write_bytes(json.dumps(doc, ensure_ascii=False, indent=1).encode("utf-8")); os.replace(tmp, out)
print(doc["veredito"], "%d/%d" % (doc["n_ok"], doc["n_checks"]), sha(out)[:16]); [print("FALHA:", x["check"], "|", x["detalhe"]) for x in ck if not x["ok"]]
sys.exit(0 if ok else 1)
