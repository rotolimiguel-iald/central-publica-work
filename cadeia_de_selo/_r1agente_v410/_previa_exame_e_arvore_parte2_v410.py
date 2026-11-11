# -*- coding: utf-8 -*-
"""_previa_exame_e_arvore_parte2_v410.py -- PREVIA, antes da cadeia: roda exame_pontos_v410.py e simular_arvore_do_nos_v410.py sobre o candidato corrente com os MESMOS argumentos que o ensaio a seco usa (caminhos absolutos), em processo isolado,
e imprime o que o ensaio leria deles (o ensaio antigo caiu no exame com rc != 0 sem JSON; a causa nao foi esclarecida). Nao e' o ensaio nem o rito.   uso: python -B -X utf8 _previa_exame_e_arvore_parte2_v410.py [exame|arvore|ambos]"""
import hashlib, json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
qual = sys.argv[1] if len(sys.argv) > 1 else "ambos"
cand = os.path.join(HERE, DL.CANDIDATO); KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX; sha = hashlib.sha256(open(cand, "rb").read()).hexdigest()
run = lambda args_: subprocess.run([sys.executable, "-B", "-X", "utf8"] + args_, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600, cwd=HERE)
ok = True
if qual in ("exame", "ambos"):
    t0 = time.time(); r = run([os.path.join(HERE, "exame_pontos_v410.py"), "--candidato", cand, "--logs", KD, "--flags", os.path.join(KD, "FLAGS_v410.json"), "--sandbox", KB, "--sha256", sha])
    p = os.path.join(HERE, "EXAME_PONTOS_%s.json" % sha[:16]); j = json.load(open(p, encoding="utf-8")) if os.path.exists(p) and os.path.getmtime(p) >= t0 else {}
    e_ok = bool(r.returncode == 0 and j.get("algum_falso") == [] and (j.get("ponto_iald2") or {}).get("all_verified") is True and (j.get("ponto_h0dn") or {}).get("all_verified") is True and (j.get("ponto_aescala") or {}).get("all_verified") is True and (j.get("ponto_hms13") or {}).get("all_verified") is True)
    ok = ok and e_ok
    print("exame_pontos: rc", r.returncode, "| json desta rodada:", bool(j), "| algum_falso:", j.get("algum_falso"), "| pontos novos:", {k: (j.get(k) or {}).get("all_verified") for k in ("ponto_iald2", "ponto_aescala", "ponto_h0dn", "ponto_hms13")}, "| ok:", e_ok, "| %.0f s" % (time.time() - t0))
    if not e_ok:
        print("--- stdout (fim):\n" + r.stdout[-2500:]); print("--- stderr (fim):\n" + r.stderr[-2500:])
if qual in ("arvore", "ambos"):
    t0 = time.time(); r = run([os.path.join(HERE, "simular_arvore_do_nos_v410.py"), "--candidato", cand, "--logs", KD])
    p = os.path.join(HERE, "SIMULACAO_ARVORE_NOS_%s.json" % sha[:16]); j = json.load(open(p, encoding="utf-8")) if os.path.exists(p) and os.path.getmtime(p) >= t0 else {}
    regs = list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]
    a_ok = bool(r.returncode == 0 and j.get("kf_all_verified") is True and (j.get("indice") or {}).get("all_verified") is True and (j.get("formal_map_v410") or {}).get("ok") is True and (j.get("chave_do_lema") or {}).get("ok") is True and all((j.get(k) or {}).get("all_verified") is True for k in regs))
    ok = ok and a_ok
    print("simular_arvore: rc", r.returncode, "| json desta rodada:", bool(j), "| kf:", j.get("kf_all_verified"), "| indice:", (j.get("indice") or {}).get("all_verified"), "| formal_map:", (j.get("formal_map_v410") or {}).get("ok"), "| registros v410:", {k: (j.get(k) or {}).get("all_verified") for k in regs}, "| entradas:", j.get("formal_files_n_no_rito_real"), "| ok:", a_ok, "| %.0f s" % (time.time() - t0))
    if not a_ok:
        print("--- stdout (fim):\n" + r.stdout[-2500:]); print("--- stderr (fim):\n" + r.stderr[-2500:]); print("falhas:", {k: (j.get(k) or {}).get("falhas") for k in regs})
print("PREVIA:", "TUDO PASSOU" if ok else "FALHOU"); sys.exit(0 if ok else 1)
