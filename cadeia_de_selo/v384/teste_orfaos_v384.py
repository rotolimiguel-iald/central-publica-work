# -*- coding: utf-8 -*-
"""TESTE da logica dos ORFAOS do congelamento (9a afericao, 9N0/9N13), numa pasta de TESTE com transcrito de TESTE (copia do real + mensagem SINTETICA):
(O1) congelado; depois o JSON do V1 APAGADO (a tentativa interrompida) e uma copia da pasta de evidencias ADULTERADA -> a nova tentativa poe o MD e a pasta
     para o lado (.incompleto_*, com os bytes preservados), copia de novo e grava o V1 (rc 0);
(O2) com o JSON do V1 PRESENTE e a pasta de evidencias adulterada -> RECUSA, e nada se move (nem MD, nem pasta, nem JSON);
(O3) com o JSON do V1 PRESENTE e a pasta de evidencias com um arquivo A MAIS -> RECUSA, nada se move.
Nada toca a pasta permanente."""
import hashlib, json, os, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
TW, TM, TT = os.path.join(HERE, "pilar_quantico_worker.py"), os.path.join(HERE, "teste_motor_v8", "result.json"), os.path.join(HERE, "teste_tempo_v9", "result.json")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
D = os.path.join(HERE, "teste_orfaos")
if os.path.isdir(D):
    shutil.rmtree(D)
os.makedirs(D); G = os.path.join(D, "gerar.py"); shutil.copyfile(GEN, G)


def run(args, trans=None):
    env = dict(os.environ); env["PYTHONIOENCODING"] = "utf-8"
    if trans:
        env["TGL_PREREG_TRANSCRITO_TESTE"] = trans
    r = subprocess.run([sys.executable, G] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    return r.returncode, (r.stdout + r.stderr)


def estado():
    return sorted(os.listdir(D)), {f: h(os.path.join(D, f)) for f in os.listdir(D) if os.path.isfile(os.path.join(D, f))}


RES = {}
rc0, o0 = run([TW, TT, TM, HERE, "--escolha=B_REDUZIDO"]); assert rc0 == 0, o0[-800:]
RASC = os.path.join(D, "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_REDUZIDO.json")
time.sleep(1.2)
TR = os.path.join(D, "transcrito_TESTE.jsonl"); shutil.copyfile(REAL, TR)
with open(TR, "a", encoding="utf-8") as fh:
    fh.write("\n" + json.dumps({"type": "user", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
                                "message": {"role": "user", "content": "TESTE SINTETICO (orfaos): ratifico o b reduzido"}}, ensure_ascii=False) + "\n")
RATARGS = [TW, TT, TM, HERE, "--escolha=B_REDUZIDO", "--ratificacao-prefixo=TESTE SINTETICO (orfaos)", "--rascunho=" + RASC]
V1 = os.path.join(D, "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json"); MD = V1[:-5] + ".md"; EV = os.path.join(D, "evidencias_PREREGISTRO_V1")
rc, o = run(RATARGS, TR); assert rc == 0 and os.path.exists(V1) and os.path.exists(MD) and os.path.isdir(EV), o[-800:]
# (O2) JSON presente + pasta adulterada -> recusa, nada se move
alvo = os.path.join(EV, sorted(os.listdir(EV))[0]); orig = open(alvo, "rb").read()
open(alvo, "ab").write(b"\nADULTERADO PELO TESTE\n")
antes = estado(); ev_antes = sorted(os.listdir(EV))
time.sleep(1.2)
rc, o = run(RATARGS, TR)
RES["O2_json_presente_pasta_adulterada"] = {"rc": rc, "saida": o.strip().splitlines()[-1][:200], "nada_moveu": estado() == antes and sorted(os.listdir(EV)) == ev_antes,
                                           "passou": rc != 0 and estado() == antes and sorted(os.listdir(EV)) == ev_antes}
open(alvo, "wb").write(orig)
# (O3) JSON presente + arquivo a mais -> recusa, nada se move
extra = os.path.join(EV, "A_MAIS.txt"); open(extra, "wb").write(b"a mais")
antes = estado(); ev_antes = sorted(os.listdir(EV))
rc, o = run(RATARGS, TR)
RES["O3_json_presente_arquivo_a_mais"] = {"rc": rc, "saida": o.strip().splitlines()[-1][:200],
                                         "passou": rc != 0 and estado() == antes and sorted(os.listdir(EV)) == ev_antes}
os.remove(extra)
# (O1) a tentativa interrompida: JSON apagado (copia guardada fora), pasta adulterada -> MD e pasta para o lado, nova copia, V1 gravado
md_bytes = open(MD, "rb").read(); open(alvo, "ab").write(b"\nADULTERADO PELO TESTE\n"); adult = open(alvo, "rb").read()
os.replace(V1, os.path.join(D, "_V1_guardado_pelo_teste.json.txt"))
time.sleep(1.2)
rc, o = run(RATARGS, TR)
inc_md = [f for f in os.listdir(D) if f.startswith(os.path.basename(MD) + ".incompleto_")]
inc_ev = [f for f in os.listdir(D) if f.startswith("evidencias_PREREGISTRO_V1.incompleto_")]
ok_md = len(inc_md) == 1 and open(os.path.join(D, inc_md[0]), "rb").read() == md_bytes
ok_ev = len(inc_ev) == 1 and open(os.path.join(D, inc_ev[0], os.path.basename(alvo)), "rb").read() == adult
j = json.load(open(V1, encoding="utf-8")) if os.path.exists(V1) else {}
ok_novo = bool(j) and all(h(e["copia_permanente"]) == e["sha256"] for e in j.get("evidencias", []))
RES["O1_interrompida_md_e_pasta_para_o_lado"] = {"rc": rc, "avisos": [l for l in o.splitlines() if l.startswith("AVISO")], "md_preservado": ok_md, "pasta_preservada": ok_ev,
                                                "v1_novo_com_evidencias_que_conferem": ok_novo, "passou": rc == 0 and ok_md and ok_ev and ok_novo and os.path.exists(MD)}
for k, v in RES.items():
    print(k, "PASSOU" if v["passou"] else "FALHOU", "| rc", v["rc"], "|", v.get("saida") or v.get("avisos"))
out = os.path.join(HERE, "teste_orfaos_v384.json")
json.dump(RES, open(out + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(out + ".tmp", out)
print("TUDO PASSOU" if all(v["passou"] for v in RES.values()) else "HA FALHA", "|", h(out)[:16])
