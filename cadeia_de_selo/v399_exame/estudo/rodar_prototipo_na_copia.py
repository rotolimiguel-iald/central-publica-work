# -*- coding: utf-8 -*-
"""rodar_prototipo_na_copia.py -- revisao independente do estudo v399 (c1, 24/10/2026): roda o PROTOTIPO do preparador (importado como modulo, sem a CLI) sobre a MINHA COPIA
dos tres objetos do Nos (copia\\um.py v398, um_absoluto.json, um_absoluto_selo.json), nunca no Nos; e refaz, com codigo MEU, a enumeracao do alfabeto (C96/Q8, C128/Q8, C0/Q8),
a inexatidao da Dobra pura e a auditoria de separacao. Escreve so' nesta pasta. uso: python -B -X utf8 rodar_prototipo_na_copia.py"""
import hashlib, importlib.util, json, math, os, sys, time, zlib
import numpy as np
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); COP = os.path.join(H, "copia")
S = r"C:\IALD\Central de Patentes\work\v399_selo_e_testemunho"
spec = importlib.util.spec_from_file_location("selo_acom_prototipo", os.path.join(S, "selo_acom_prototipo.py")); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
R = {"prototipo_sha16": hashlib.sha256(open(os.path.join(S, "selo_acom_prototipo.py"), "rb").read()).hexdigest()[:16], "python": sys.version.split()[0], "numpy": np.__version__, "zlib": getattr(zlib, "ZLIBNG_VERSION", None) and ("zlib-ng " + zlib.ZLIBNG_VERSION) or zlib.ZLIB_VERSION}
hx = lambda b: hashlib.sha256(b).hexdigest()
# (0) o bloco embutido confere? (a funcao do prototipo e o MEU calculo: do primeiro INICIO ate a PRIMEIRA linha-marcador de FIM do acom_crypto, inclusive)
R["bloco_embutido_funcao"] = P.conferir_bloco_embutido()
t = open(os.path.join(S, "selo_acom_prototipo.py"), "rb").read().decode("utf-8").replace("\r\n", "\n")
ini = t.index("# >>> ACOM_EMBUTIDO_INICIO"); marca = "# <<< ACOM_EMBUTIDO_FIM: skygrid_sim/acom_crypto.py <<<\n"; fim = t.index(marca) + len(marca)
R["bloco_embutido_meu_calculo"] = {"sha256": hx(t[ini:fim].encode("utf-8")), "igual_ao_declarado": hx(t[ini:fim].encode("utf-8")) == P.ACOM_PROVENIENCIA["bloco_embutido_sha256"], "linhas": t[ini:fim].count("\n")}
# as fontes do operador, lidas agora
R["fontes"] = P.estudo_fontes()["_todos_conferem"]
# (1) selar / verificar o um.py v398 (copia)
b = open(os.path.join(COP, "um.py"), "rb").read(); R["um_py"] = {"sha16": hx(b)[:16], "bytes": len(b)}
t0 = time.perf_counter(); selo, p = P.selar(b, "um.py", devolver_partes=True); R["um_py"]["selar_s"] = time.perf_counter() - t0
a = selo["acom"]; R["um_py"].update(psi_sha16=a["psi"]["sha256"][:16], theta_sha16=a["theta"]["sha256"][:16], kappa_sha16=a["kappa"]["sha256"][:16], lut_sha16=a["kappa"]["campos"]["lut_sha256"][:16],
                   psi_bytes=a["psi"]["bytes"], theta_bytes=a["theta"]["bytes"], kappa_bytes=a["kappa"]["bytes"], m=a["kappa"]["campos"]["m_max_abs"], f_exp=a["estrutura"]["f_exp"], entropia=a["estrutura"]["entropia_dos_estados_bits"],
                   round_trip=a["prova_de_reconstrucao"], separacao={k: a["auditoria_de_separacao"][k] for k in ("fracao_de_L_negativo", "theta_mais_kappa_com_sinal_unico", "psi_ou_psi_mais_kappa_sem_magnitudes", "kappa_sozinho_melhor_chute_constante", "psi_redundante")})
t0 = time.perf_counter(); v = P.verificar(b, selo); R["um_py"]["verificar_s"] = time.perf_counter() - t0; R["um_py"]["verificacao"] = v
# MEU round trip independente: reconstruo so' das partes (psi_raw, theta_raw, kappa) com a formula da Dobra + rint, sem a funcao do prototipo
kap = a["kappa"]["campos"]; n = kap["n_elements"]; m = kap["m_max_abs"]; qmax = 255
psi_states = P._unpack2bits(p["psi_raw"], n); theta_q = np.frombuffer(p["theta_raw"], dtype=np.uint8)
real = (math.sqrt(m) * np.sin(theta_q.astype(np.float64) / qmax * (math.pi / 2))) ** 2
sinal = np.where(psi_states >= 2, -1, 1)
rec_meu = (sinal * np.rint(real).astype(np.int64) + 96).astype(np.uint8).tobytes()
R["um_py"]["round_trip_meu_sha16_igual"] = hx(rec_meu) == hx(b)
R["um_py"]["dobra_pura_sem_rint"] = {"bytes_com_erro_gt_1e-6": int((np.abs(real - np.abs(np.frombuffer(b, dtype=np.uint8).astype(np.int64) - 96)) > 1e-6).sum()),
                                     "bytes_com_erro_gt_1e-2": int((np.abs(real - np.abs(np.frombuffer(b, dtype=np.uint8).astype(np.int64) - 96)) > 1e-2).sum()),
                                     "erro_max": float(np.abs(real - np.abs(np.frombuffer(b, dtype=np.uint8).astype(np.int64) - 96)).max())}
del real, rec_meu
# o caminho LITERAL do metodo embutido (reflect/manifest em float64 sobre o objeto inteiro) == o caminho rapido?
t0 = time.perf_counter(); L = (np.frombuffer(b, dtype=np.uint8).astype(np.int16) - 96).astype(np.float64); r = P.DimensionalMirror(angular_bits=8).reflect(L); t_ref = time.perf_counter() - t0
t0 = time.perf_counter(); dec = P.DimensionalMirror(angular_bits=8).manifest(r); t_man = time.perf_counter() - t0
R["um_py"]["literal"] = {"reflect_s": t_ref, "manifest_s": t_man, "psi_igual": zlib.decompress(r.psi_packed) == p["psi_raw"], "theta_igual": zlib.decompress(r.theta_packed) == p["theta_raw"],
                         "erro_max_literal": float(np.abs(dec - L).max()), "gt_1e-6": int((np.abs(dec - L) > 1e-6).sum()), "gt_1e-2": int((np.abs(dec - L) > 1e-2).sum()),
                         "rint_igual_ao_objeto": bool(np.array_equal(np.rint(dec).astype(np.int64) + 96, np.frombuffer(b, dtype=np.uint8).astype(np.int64)))}
del L, dec, r
# (2) controles negativos: objeto inteiro e amostra
t0 = time.perf_counter(); c_full = P.controles_negativos(b); R["controles_um_py_inteiro"] = {"n": c_full["n_controles"], "todos_recusados": c_full["todos_recusados"], "s": time.perf_counter() - t0, "obtidos": {c["id"]: c["obtido"] for c in c_full["controles"]}, "N5_sem_hash_nao_muda": next((c.get("sem_hash_a_reconstrucao_nao_muda") for c in c_full["controles"] if c["id"] == "N5"), None)}
c_1m = P.controles_negativos(b[:1 << 20]); R["controles_1MiB"] = {"n": c_1m["n_controles"], "todos_recusados": c_1m["todos_recusados"]}
# (3) a enumeracao do alfabeto, com codigo MEU (a formula do metodo), para C96/Q8, C128/Q8, C0/Q8
def enum_meu(centro, bits):
    M = max(centro, 255 - centro); qmax = (1 << bits) - 1; casos = falhas = nao_inj = 0; erro_max = 0.0
    for mm in range(1, M + 1):
        v = np.arange(0, mm + 1, dtype=np.float64); g = np.sqrt(v); gmax = math.sqrt(mm)
        q = np.clip(np.round(np.arcsin(np.clip(g / (gmax + 1e-10), 0.0, 1.0)) / (math.pi / 2) * qmax), 0, qmax).astype(np.int64)
        realv = (gmax * np.sin(q / qmax * (math.pi / 2))) ** 2
        casos += mm + 1; falhas += int((np.rint(realv) != v).sum()); erro_max = max(erro_max, float(np.abs(realv - v).max())); nao_inj += int(len(set(q.tolist())) != len(q))
    return {"centro": centro, "bits": bits, "m_max": M, "casos": casos, "falhas_apos_rint": falhas, "m_nao_injetivos": nao_inj, "erro_real_max": erro_max, "exato": falhas == 0 and nao_inj == 0, "limite_teorico": M * math.pi / (4 * qmax)}
R["alfabeto_meu"] = [enum_meu(96, 8), enum_meu(128, 8), enum_meu(0, 8), enum_meu(0, 12)]
# a LUT do prototipo para m = 144 (o m do um.py) == a minha?
v = np.arange(0, 145, dtype=np.float64); q_meu = np.clip(np.round(np.arcsin(np.clip(np.sqrt(v) / (math.sqrt(144) + 1e-10), 0, 1)) / (math.pi / 2) * 255), 0, 255).astype(np.uint8).tobytes()
R["lut_m144_igual_ao_prototipo"] = hx(q_meu) == a["kappa"]["campos"]["lut_sha256"]
# (3b) o perfil C0 esvazia a separacao? (4 MB): Theta+kappa com sinal unico (+) reconstroi? em Q=8 e Q=12; e a funcao selar com CENTRO 0 e 128
x = b[:4_000_000]; Lx = np.frombuffer(x, dtype=np.uint8).astype(np.float64); out0 = {}
for bits in (8, 12):
    rr = P.DimensionalMirror(angular_bits=bits).reflect(Lx); th = np.frombuffer(zlib.decompress(rr.theta_packed), dtype=np.uint8 if bits <= 8 else np.uint16); qm = (1 << bits) - 1
    recx = np.rint((rr.metadata["g_max"] * np.sin(th.astype(np.float64) / qm * (math.pi / 2))) ** 2).astype(np.int64)
    est = np.bincount(P._unpack2bits(zlib.decompress(rr.psi_packed), len(x)), minlength=4)
    out0["Q%d" % bits] = {"bytes_errados_so_theta_kappa": int((recx != np.frombuffer(x, dtype=np.uint8)).sum()), "estados_psi": [int(c) for c in est], "estados_negativos": int(est[2] + est[3])}
def tenta(centro, obj):
    ant = P.CENTRO; P.CENTRO = centro
    try:
        P.selar(obj, "ingenuo"); return "ACEITOU"
    except P.SeloRecusado as e:
        return "RECUSOU:" + str(e)[:120]
    finally:
        P.CENTRO = ant
ascii_puro = bytes(c for c in b[:400000] if c < 128)
out0["selar"] = {"centro_0_um_py_4MB": tenta(0, x), "centro_0_ASCII": tenta(0, ascii_puro), "centro_128_ASCII": tenta(128, ascii_puro), "centro_128_um_py_4MB": tenta(128, x), "centro_96_ASCII": tenta(96, ascii_puro), "centro_96_um_py_4MB": tenta(96, x)}
R["perfil_sem_sinal"] = out0
# (4) separacao: Theta+kappa com sinal unico acerta quantos bytes do um.py? (meu calculo: a melhor escolha de sinal)
hist = np.bincount(np.frombuffer(b, dtype=np.uint8), minlength=256); neg = int(hist[:96].sum()); pos = int(hist[97:].sum()); zero = int(hist[96])
R["separacao_meu"] = {"frac_neg": neg / len(b), "frac_pos_ou_zero": (pos + zero) / len(b), "theta_kappa_sinal_unico_acerta_frac": max(neg, pos + zero) / len(b), "erra_frac": min(neg, pos + zero) / len(b)}
# (5) sidecar dos tres objetos (copias) e comparacao com o do preparador
objs = [(nm, open(os.path.join(COP, nm), "rb").read()) for nm in ("um.py", "um_absoluto.json", "um_absoluto_selo.json")]
t0 = time.perf_counter(); sc = P.sidecar(objs, quem="exame independente (copia)"); R["sidecar_s"] = time.perf_counter() - t0
prep = json.load(open(os.path.join(S, "recibos", "um_absoluto_selo_acom.json"), encoding="utf-8"))
pp = {it["nome"]: it for it in prep["objetos"]}
R["sidecar"] = {"veredito": sc["veredito"], "recusas": sc["recusas"], "objetos": {it["nome"]: {"sha16": it["sha256"][:16], "psi": it["acom"]["psi"]["sha256"][:16], "theta": it["acom"]["theta"]["sha256"][:16], "kappa": it["acom"]["kappa"]["sha256"][:16],
                                                                                            "igual_ao_do_preparador": all(it["acom"][k]["sha256"] == pp[it["nome"]]["acom"][k]["sha256"] for k in ("psi", "theta", "kappa")) and it["sha256"] == pp[it["nome"]]["sha256"]} for it in sc["objetos"]},
               "honestidade_presente": "honestidade" in sc, "confidencialidade_texto": sc.get("honestidade", {}).get("confidencialidade", "")[:80]}
R["verificar_core_e_selo"] = {it["nome"]: P.verificar(dict(objs)[it["nome"]], it)["ok"] for it in sc["objetos"]}
# (6) o registro no formato do core (sobre a copia) e a camada de transporte (amostras)
t0 = time.perf_counter(); reg = P.registro_core_v399(b, sha256_do_codigo=hx(b)); R["registro_core"] = {"all_verified": reg["all_verified"], "verdict": reg["verdict"], "checks": reg["checks"], "s": time.perf_counter() - t0, "statuses": reg["statuses"]}
R["transporte"] = {k: v for k, v in P.estudo_transporte(b).items() if k in ("razao_de_tempo_encrypt_1024KiB_sobre_512KiB", "extrapolacao_para_o_um_py_inteiro_se_quadratico", "controles_na_camada_do_operador")}
R["transporte"]["ultima_amostra"] = P.estudo_transporte(b[:256 * 1024])["amostras"][-1]
json.dump(R, open(os.path.join(H, "PROTOTIPO_NA_COPIA.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str)[:14000])
