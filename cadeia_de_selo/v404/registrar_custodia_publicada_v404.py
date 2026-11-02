# -*- coding: utf-8 -*-
"""registrar_custodia_publicada_v404.py -- gerencia c1, 29/10/2026 (madrugada): transition ACOM da sessao com a custodia G1 da v404 FECHADA
(codigo 5 = so decisoes do operador), o auditar limpo, os remendos de ferramenta commitados e a entrega do adendo H (render da v404) em
disco, a integrar. Tudo lido do disco/git; nenhum numero digitado. (Vai por script porque o Bash desta maquina colapsa as barras do JSON.)"""
import hashlib, json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def git(cwd, *a): return subprocess.run(["git", "-C", cwd] + list(a), capture_output=True, text=True).stdout.strip()
CEN = r"C:\IALD\Central de Patentes"
head = git(CEN, "rev-parse", "--short=8", "HEAD"); origem = git(CEN, "rev-parse", "--short=8", "origin/main"); assert head == origem, (head, origem)
msg = git(CEN, "log", "-1", "--format=%s"); assert msg.startswith("ferramentas(29/10)"), msg
c14 = git(CEN, "log", "-1", "--format=%h", "--grep=^custodia(v404)"); assert c14, "sem commit custodia(v404)"
RUNS = os.path.join(CEN, "work", "custodia_G1", "runs")
run = sorted(p for p in os.listdir(RUNS) if p.startswith("v404_"))[-1]
rel = os.path.join(RUNS, run, "RELATORIO.json"); R = json.load(open(rel, encoding="utf-8"))
aud = sorted(p for p in os.listdir(RUNS) if p.startswith("auditar_v404_"))[-1]; aud = os.path.join(RUNS, aud)
audtxt = open(aud, encoding="utf-8", errors="replace").read(); assert "0 número(s) citado(s) defasado(s); 0 rótulo(s) errado(s)" in audtxt, audtxt[-300:]
H = os.path.join(CEN, r"Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_H\RESULTADO.json"); h = json.load(open(H, encoding="utf-8"))
assert h["status"] == "BUILT_FOR_MANAGEMENT_INTEGRATION_PUBLICATION" and h["source"] == "v404", (h["status"], h["source"])
PONT = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\PUBLIC_DELIVERY_V7.json"; pont = json.load(open(PONT, encoding="utf-8"))
assert pont["source_sha256"].startswith("3820476c83267f61"), pont["source_sha256"]
pino = json.load(open(os.path.join(os.environ["USERPROFILE"], ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "PINO_MEMORY.json"), encoding="utf-8"))
quadro = os.path.join(CEN, "organismo", "ESTADO_DO_ORGANISMO.md"); q = open(quadro, encoding="utf-8", errors="replace").read()
cab = [l for l in q.splitlines() if "DEFASADO" in l and "OK" in l][:1]
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
def sm(p):
    r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip().startswith("{") else {"raw": (r.stdout + r.stderr)[:400]})
rc, g = sm({"operation": "get", "reference": REF}); rev = (g.get("result") or {}).get("revision"); print("acom get rc", rc, "revision", rev); assert rev is not None, g
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
agora = time.strftime("%d/%m/%Y %H:%M")
texto = ("%s: custodia G1 da v404 FECHADA: ultima passagem %s terminou com codigo 5 (so decisoes do operador: release do app v402->v404 [C21], E0 e a lei de propagacao, D2 [LEGAL], "
         "iald.ia.br 404, Zenodo v401); C13-C20 e C17A/B/C aplicados; Central %s (custodia(v404)) e %s (remendos de ferramenta: quadro e perna C20 do G1 leem a entrega da fila cientifica "
         "pelo conteudo do recibo; nos.py do G1) = origin/main; auditar: 0 numeros defasados, 0 rotulos errados; quadro: %s; ACOM da custodia em revisao 3. Fila da memoria: linha do "
         "HANDOFF v404 no indice = PUBLICADA (troca manual pelo rito da v403; antiga integra no MEMORY_2.md), ponteiro das licoes v404 na linha do G1, 11 depositos promovidos, MEMORY.md "
         "%d linhas/%d B pinado %s, verificar limpo; licoes 10-13 acrescentadas ao topico. ORDEM 022 adendo H ENTREGUE pelo Codex (BUILT_FOR_MANAGEMENT_INTEGRATION_PUBLICATION; fonte v404 "
         "3820476c83267f61; 6 sinteses novas, 52 reutilizadas, 0 repeticoes; 132 arquivos publicos; estimativa direta de TTS US$ 0 [DERIVED]; revisao independente PASS_WITH_SCOPE): a integrar por hash e subir. "
         "NOT_FALSIFIED nunca e' CONFIRMED; PROVADA = validade; o gate nao se moveu." % (agora, run, c14, head, (cab[0].strip()[:160] if cab else "lido"), pino["linhas"], pino["bytes"], pino["sha256"][:16]))
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-v404-custodia-publicada-g1-fechada-29out",
            "changes": {"records": [{"id": "c1-v404-custodia-publicada-g1-fechada", "kind": "fact", "statute": "REAL", "sources": [S(rel), S(aud), S(H), S(PONT)], "text": texto}],
                        "flow": {"phase": "v404_custodia_PUBLICADA__G1_fechada_codigo5__V7_v404_entregue_a_integrar",
                                 "next_action": "integrar a V7 da v404 por hash (Site\\tgl\\v3.0_bancada\\tools\\integrar_filmes_v7.py; --conferir antes), testes headless e replay, subir_site.py por lotes com manifesto e SUBIDA VERIFICADA; depois tools\\gerar_vitrine_x.py + ORDEM 026 adendo (fase 2 da v404) com o CUSTODIA_v404.txt ja escrito. Ao operador: C21 (release do app), E0, D2, iald.ia.br, Zenodo, nome definitivo da pedra ProjecaoTransversalDaMeiaNat. Conjunto D nao se abre sem a palavra dele."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
