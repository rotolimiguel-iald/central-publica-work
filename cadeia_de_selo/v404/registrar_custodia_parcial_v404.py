# -*- coding: utf-8 -*-
"""registrar_custodia_parcial_v404.py -- gerencia c1, 28/10/2026 (noite): transition ACOM da sessao com o que JA e' material e para fora na custodia G1 da v404:
espelho commitado e empurrado, site no ar com o pino, adendos G e H da ORDEM 022 despachados, dez depositos da fila triados e indice re-pinado. Tudo lido do disco/git."""
import hashlib, json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def git(cwd, *a): return subprocess.run(["git", "-C", cwd] + list(a), capture_output=True, text=True).stdout.strip()
TB = r"C:\IALD\Artigo\the_boundary"; head = git(TB, "rev-parse", "--short=8", "HEAD"); origem = git(TB, "rev-parse", "--short=8", "origin/main"); assert head == origem, (head, origem)
msg = git(TB, "log", "-1", "--format=%s"); assert msg.startswith("custodia(v404)"), msg
PC = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT"
G = os.path.join(PC, "ORDEM_022_ADENDO_G_render_v404_e_frases_do_gate.md"); H = os.path.join(PC, "ORDEM_022_ADENDO_H_duas_sinteses_adicionais_autorizadas.md")
X = os.path.join(PC, "X_VITRINE", "CUSTODIA_v404.txt")
pino = json.load(open(os.path.join(os.environ["USERPROFILE"], ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "PINO_MEMORY.json"), encoding="utf-8"))
run = sorted(p for p in os.listdir(r"C:\IALD\Central de Patentes\work\custodia_G1\runs") if p.startswith("v404_"))[-1]
rel = os.path.join(r"C:\IALD\Central de Patentes\work\custodia_G1\runs", run, "RELATORIO.json")
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
def sm(p):
    r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip().startswith("{") else {"raw": (r.stdout + r.stderr)[:400]})
rc, g = sm({"operation": "get", "reference": REF}); rev = (g.get("result") or {}).get("revision"); print("acom get rc", rc, "revision", rev)
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
agora = time.strftime("%H:%M")
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-v404-custodia-parcial-publicada-28out",
            "changes": {"records": [{"id": "c1-v404-custodia-parcial-publicada", "kind": "fact", "statute": "REAL", "sources": [S(rel), S(G), S(H), S(X)],
                                     "text": "28/10/2026 %s: custodia G1 da v404 em curso: espelho the_boundary %s = origin/main (custodia(v404)), site no ar com v404 3820476c83267f61, E10-E19 e C2 ok; parou em C13 a espera do snapshot C5 (pid 26348, em curso desde 22:24:45). ORDEM 022: adendo G (frases do gate lidas do core: 18 calculadas, 0 literais; render da v404; evento 1335) e adendo H (duas sinteses adicionais autorizadas; seis unidades; evento 1341) despachados; a parada do adendo F de 13:10 estava sem resposta. Fila da memoria: 10 depositos triados; linha da fila v392-v404 + marcador V404; MEMORY.md %d linhas/%d B pinado %s. CUSTODIA_v404.txt da vitrine escrito. NOT_FALSIFIED nunca e' CONFIRMED; o gate nao se moveu." % (agora, head, pino["linhas"], pino["bytes"], pino["sha256"][:16])}],
                        "flow": {"phase": "v404_custodia_G1_em_curso__C13_a_C17C_pendentes", "next_action": "ao fim do snapshot C5: custodiar.py executar --versao v404 --aceitar-molde --publicar (C13..C17C), auditar; promover os depositos de claude-site (handoff PUBLICADA no indice) e a linha do topico licoes-cadeia-v404-28out; esperar o render do adendo H (integracao por hash pela sessao do site; depois ORDEM 026 fase 2 v404). E0 segue pergunta ao operador; conjunto D nao se abre sem a palavra dele."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
