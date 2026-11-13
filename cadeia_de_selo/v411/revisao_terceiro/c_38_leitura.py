import sys, os, json, importlib.util, shutil, copy
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
sys.path.insert(0, V); sys.path.insert(0, V + r"\pos_rito")
POS = r"C:\t\k411c\revisao_C\nos_pos"; VAR = r"C:\t\k411c\revisao_C\nos_var2"
spec = importlib.util.spec_from_file_location("leitura_rev", V + r"\pos_rito\leitura_v411.py")
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
E = json.load(open(V + r"\ESPERADOS_v411.json", encoding="utf-8"))
ap = {"um_py_novo": {"sha16": E["candidato_sha16"]}, "backups": {"um.py": {"sha16": E["origem_sha16"], "backup": V + r"\base_um_v410.py"}}, "ts": "20261112_190000"}
L._aplicado = lambda: (ap, "emulado")
def roda(nos):
    L.NOS = nos
    V_, P = L.ler()
    return P
print("== POSITIVO (Nos emulado copiado):")
P = roda(POS)
print("   PROBLEMAS:", len(P), [p[:120] for p in P[:3]])
# variantes no core
def variante(nome, mut):
    if os.path.exists(VAR): shutil.rmtree(VAR)
    os.makedirs(VAR)
    for f in os.listdir(POS):
        if f in ("tgl_kernel",): continue
        shutil.copyfile(POS + "\\" + f, VAR + "\\" + f) if f != "um_absoluto.json" else None
    j = json.load(open(POS + r"\um_absoluto.json", encoding="utf-8"))
    mut(j["core"])
    json.dump(j, open(VAR + r"\um_absoluto.json", "w", encoding="utf-8"), ensure_ascii=False)
    Pn = roda(VAR)
    print("== %s: PROBLEMAS %d | %s" % (nome, len(Pn), [p[:110] for p in Pn[:2]]))
def m_ladder(c): c["external_ladder"]["n_theorems_clean"] -= 1
def m_autores(c): c["cunhagens_v411"]["extras"]["autores"][next(iter(c["cunhagens_v411"]["extras"]["autores"]))] = "gerencia"
def m_kh9(c): c["kh_n1_cobertura_v409"]["erratas"].append(dict(c["kh_n1_cobertura_v409"]["erratas"][-1], agora="adulterada"))
def m_k(c): c["h0dn_bg1_v411"]["values"]["K"] = c["h0dn_bg1_v411"]["values"]["K"] * 1.0000001
def m_p2(c): c["h0dn_bg1_v411"].pop("p2_ao_lado_da_v387", None)
for n, m in (("escada do core -1", m_ladder), ("autoria da fala 1 = gerencia", m_autores), ("errata a mais no kh v409", m_kh9), ("K adulterado em 1e-7 relativo", m_k)):
    variante(n, m)
