# -*- coding: utf-8 -*-
"""registrar_v7_v404_acom.py -- gerencia c1, 29/10/2026: transition ACOM da sessao com a V7 da v404 NO AR, a ressalva do estatuto corrigida
ao lado no espelho, a vitrine do X (adendo C) escrita e despachada. Tudo lido do disco/git; exige a marca no DIARIO_DO_SITE.md."""
import hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def git(cwd, *a): return subprocess.run(["git", "-C", cwd] + list(a), capture_output=True, text=True).stdout.strip()
CEN = r"C:\IALD\Central de Patentes"; TB = r"C:\IALD\Artigo\the_boundary"; BANC = r"C:\IALD\Site\tgl\v3.0_bancada"
tb = git(TB, "rev-parse", "--short=8", "HEAD"); assert tb == git(TB, "rev-parse", "--short=8", "origin/main")
ce = git(CEN, "rev-parse", "--short=8", "HEAD"); assert ce == git(CEN, "rev-parse", "--short=8", "origin/main")
D = os.path.join(BANC, "DIARIO_DO_SITE.md"); dtxt = open(D, encoding="utf-8", errors="replace").read(); assert "<!-- filmes_v7:v404:no_ar -->" in dtxt
C = os.path.join(CEN, r"Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_026_ADENDO_C_fase2_v404.md"); assert os.path.isfile(C)
subs = sorted(d for d in os.listdir(os.path.join(BANC, "subidas")) if re.fullmatch(r"\d{8}_\d{6}", d)); ult = os.path.join(BANC, "subidas", subs[-1], "RELATORIO.md")   # só subidas reais
assert "SUBIDA VERIFICADA" in open(ult, encoding="utf-8", errors="replace").read()
desp = sorted(p for p in os.listdir(r"C:\IALD\PROGRAMA_IALD\despachos") if p.startswith("msg_ordem026_adendo_c")); assert desp
mp = os.path.join(r"C:\IALD\PROGRAMA_IALD\despachos", desp[-1])
evento = os.environ.get("EVENTO_ADENDO_C", "").strip()   # o seq do evento do quadro, se o despacho ja' ocorreu
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
def sm(p):
    r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip().startswith("{") else {"raw": (r.stdout + r.stderr)[:400]})
rc, g = sm({"operation": "get", "reference": REF}); rev = (g.get("result") or {}).get("revision"); print("acom get rc", rc, "revision", rev); assert rev is not None, g
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
agora = time.strftime("%d/%m/%Y %H:%M")
texto = ("%s: a V7 da v404 esta' NO AR (integracao por hash, headless e replay passam, subida verificada %s; o index diz «renderizados do um.py v404»). Correcao ao lado achada no caminho: "
         "o modulo do estatuto do espelho compunha a ressalva da v392 («15 calculadas e 3 literais»), falsa desde a v403 (core: bandeiras_do_gate_v403 = 18 calculadas, 0 literais, 15 no veredito, "
         "3 informativas, 4 experimentais de um so' booleano DECLARADO); a frase ia ao llms-full, ao README/ESTADO_ATUAL/read-brief do espelho e ao artigo da vitrine do X; modulo com ramo v403+ (a v392 como registro), "
         "superficies regeneradas na ordem do G1, guardas do espelho ok, espelho %s = origin/main; Central %s (remendos de ferramenta + leitor da vitrine). Vitrine do X: MANIFEST v404 gerado e "
         "ORDEM 026 ADENDO C (Fase 2 da v404; a da v403 nao existiu) escrito%s. NOT_FALSIFIED nunca e' CONFIRMED; PROVADA = validade; o gate nao se moveu."
         % (agora, subs[-1], tb, ce, (" e despachado (evento %s)" % evento) if evento else " (despacho a seguir)"))
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-v404-v7-no-ar-ressalva-corrigida-29out",
            "changes": {"records": [{"id": "c1-v404-v7-no-ar-ressalva-corrigida", "kind": "fact", "statute": "REAL", "sources": [S(D), S(ult), S(C), S(mp)], "text": texto}],
                        "flow": {"phase": "v404_custodia_PUBLICADA__V7_v404_NO_AR__vitrine_X_fase2_v404_despachada__aguarda_Codex",
                                 "next_action": "conferir a devolucao do Codex (DO_CHATGPT\\ORDEM_026\\VITRINE\\RESULTADO_FASE2_v404.json) por script e dar o aceite; ler a cada etapa o status das ordens despachadas. Ao operador: C21 (release do app), E0, D2, iald.ia.br, Zenodo, nome definitivo da pedra ProjecaoTransversalDaMeiaNat. Candidato ao molde da v405: guarda de «como literais» nas superficies; E09 do G1 com git add -A; recibo_parada le o PID da porta; C20 le o status das ordens."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
