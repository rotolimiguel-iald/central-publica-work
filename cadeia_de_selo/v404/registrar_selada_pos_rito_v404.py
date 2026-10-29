# -*- coding: utf-8 -*-
"""registrar_selada_pos_rito_v404.py -- gerencia c1, 28/10/2026: registra no quadro (iald.py anotar) e na memoria ACOM da sessao (transition) a etapa material
«v404 SELADA (rito 2, RITO_RC=0), conferidor TUDO BATE, pos-rito 0-14 fechado, B13 aplicado na Bancada com os tres recibos, Mapa registrado». Numeros e hashes LIDOS dos arquivos."""
import glob, hashlib, io, json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"; H = os.path.dirname(os.path.abspath(__file__)); NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest(); rj = lambda p: json.load(open(p, encoding="utf-8"))
um16 = sha(os.path.join(NOS, "um.py"))[:16]; conf = rj(os.path.join(H, "conferencia_rito_v404.json")); assert conf["tudo_bate"] and conf["um_py_sha16"] == um16 == "3820476c83267f61"
stdout = io.open(os.path.join(NOS, "rodada_v404_stdout.txt"), encoding="utf-8", errors="replace").read(); assert stdout.rstrip().endswith("RITO_RC=0")
log = io.open(os.path.join(H, "rito_servidor_v404.log"), encoding="utf-8", errors="replace").read(); assert "21:56:54 fim do rito" in log and "porta 8081 escuta" in log
rp = rj(os.path.join(H, "bancada_B3_servico", "RECIBO_PARADA_v404.json")); rr = rj(os.path.join(H, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v404.json"))
rb = sorted(glob.glob(os.path.join(H, "bancada_B3", "RECIBO_SINCRONIZACAO_v404_*.json"))); assert len(rb) == 1; b = rj(rb[0])
assert b["veredito"].startswith("REPINADA_B13__APLICADA") and rr["versao_servida"] == "v404" and rr["identidade"]["um_py_sha256"][:16] == um16
hand = os.path.join(os.environ["USERPROFILE"], ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "handoff-v404-custodia.md"); hand_nos = os.path.join(NOS, "HANDOFF_v404_CUSTODIA.md")
run4 = io.open(os.path.join(H, "pos_rito", "chain_pos_rito_v404_run4_10c_14.out"), encoding="utf-8", errors="replace").read(); assert "CHAIN_RC=0" in run4 and "FECHADO v404" in run4
mapa = rj(os.path.join(H, "pos_rito", "registro_mapa_v404.json")); rota = [r for r in mapa if r["tipo"] == "ROTA"][0]["rota_id"]
selo16 = sha(os.path.join(NOS, "um_absoluto_selo.json"))[:16]
hoje = time.strftime("%d/%m/%Y"); agora = time.strftime("%H:%M")
dados = {"quando": hoje + " " + agora, "etapa": "v404 SELADA e pos-rito FECHADO", "um_py_sha16": um16, "selo_sha16": selo16, "rito": "RITO_RC=0 (20:33:59-21:56:54; tentativa 1 revertida antes)",
         "conferidor": "TUDO BATE (67 OK, 0 NAO; gate identico ao da v403; escada 9698)", "pos_rito": "0-14 FIM (CHAIN_RC=0); superficies 11 alvos; MEMORY.md 187 linhas/23132 B pinado",
         "bancada": "B12 -> B13 (%s); parada PID %s; religada PID %s servindo v404" % (b["veredito"], rp["pid"], rr["pid"]), "mapa": "rota %s + 9 anotacoes + 1 errata registradas" % rota,
         "handoff": {"memoria": sha(hand)[:16], "nos": sha(hand_nos)[:16]}, "proximo": "custodia G1 (executar sem --publicar, depois --publicar), vitrine X, Atlas/topicos; E0 e conjunto D seguem do operador"}
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "etapa", "--unidade", "F4.1", "--dados", json.dumps(dados, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", errors="replace"); print("quadro rc", r.returncode, (r.stdout or r.stderr).strip()[:200])
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
def sm(p):
    rr_ = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return rr_.returncode, (json.loads(rr_.stdout) if rr_.stdout.strip().startswith("{") else {"raw": (rr_.stdout + rr_.stderr)[:400]})
rc, g = sm({"operation": "get", "reference": REF}); rev = (g.get("result") or {}).get("revision"); print("acom get rc", rc, "revision", rev, g.get("message", "") or g.get("raw", ""))
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-v404-selada-pos-rito-fechado-28out",
            "changes": {"records": [{"id": "c1-v404-selada-pos-rito-fechado", "kind": "fact", "statute": "REAL",
                                     "sources": [S(os.path.join(H, "conferencia_rito_v404.json")), S(rb[0]), S(os.path.join(H, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v404.json")), S(hand)],
                                     "text": "28/10/2026 %s: v404 SELADA (um.py %s; selo %s; rito 2 RITO_RC=0 20:33:59-21:56:54), conferidor TUDO BATE (gate identico ao da v403; escada 9698), pos-rito 0-14 fechado (handoff %s), B13 aplicado na Bancada (parada PID %s, religada PID %s servindo v404), Mapa registrado (rota %s). NOT_FALSIFIED nunca e' CONFIRMED; o gate nao se moveu." % (agora, um16, selo16, sha(hand)[:16], rp["pid"], rr["pid"], rota)}],
                        "flow": {"phase": "v404_selada__custodia_G1_a_seguir", "next_action": "G1: custodiar.py executar --versao v404 --aceitar-molde (sem --publicar), conferir, depois --publicar e auditar; depois vitrine do X (adendo do render -> V7 -> ORDEM 026), Atlas e topicos de memoria; triar o deposito claude-prep-v404 na fila. E0 segue pergunta ao operador; conjunto D nao se abre sem a palavra dele."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
