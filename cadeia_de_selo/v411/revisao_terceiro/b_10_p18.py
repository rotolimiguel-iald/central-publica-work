from b_lib import *
import re, sys
cand = open(V + r"\um_v411_candidato.py", "rb").read().decode("utf-8")
def get_def(name):
    i = cand.index("def %s(" % name)
    m = re.search(r"\r?\n(?=\S)", cand[i + 5:])
    # end at next top-level statement after the def's body
    j = i + 5
    while True:
        m = re.search(r"\r?\n(?=[^\s#])", cand[j:])
        if not m: return cand[i:]
        k = j + m.start()
        nxt = cand[k + 1 + (1 if cand[k] == "\r" else 0):][:12]
        # the def body continues while next line is indented; here (?=\S) means a top-level line
        return cand[i:k]
n_occ = len(re.findall(r"def _v411_p18_sem_cabeca\(", cand)); print("def _v411_p18_sem_cabeca no candidato:", n_occ)
src_p18 = get_def("_v411_p18_sem_cabeca")
print(src_p18[:1200])
# guarda v392 src
n_occ2 = len(re.findall(r"def _v392_guarda_texto\(", cand)); print("def _v392_guarda_texto no candidato:", n_occ2)
src_g = get_def("_v392_guarda_texto")
ns = {}
exec(compile(src_g.replace("\r\n", "\n"), "g392", "exec"), ns)
exec(compile(src_p18.replace("\r\n", "\n"), "p18", "exec"), ns)
f = ns["_v411_p18_sem_cabeca"]; g = ns["_v392_guarda_texto"]
RAMOS = json.loads(open(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v411_emenda_11nov\producao\RAMOS_V411.json", "rb").read().decode("utf-8"))
n = int(__import__("math").floor(core()["core"]["h0dn_bg1_v411"]["values"]["primario"]["z_null"]))
cab = "".join(RAMOS["vereditos"]["leitura_partes"]) % n
print("cabeca montada:", cab[:80], "...", n)
print("cabeca real do core == montada:", cab == core()["core"]["h0dn_bg1_v411"]["values"]["primario"]["cabeca_do_teste"])
tex = cab.replace("\\", "").replace("_", r"\_\allowbreak{}")
res = {}
res["exata_retirada"] = f("a cabeca: " + cab, RAMOS, n) == []
res["exata_tex_retirada"] = f(r"\texttt{" + tex + "}", RAMOS, n) == []
troc = cab[:-1] + ("X" if cab[-1] != "X" else "Y")
res["um_caractere_trocado_recusado"] = bool(f("a cabeca: " + troc, RAMOS, n))
res["crua_recusada"] = bool(g("a cabeca: " + cab))
res["outro_n_recusado"] = bool(f("a cabeca: " + "".join(RAMOS["vereditos"]["leitura_partes"]) % (n + 1), RAMOS, n))
# my extra controls
meio = cab.replace("PROVED_IN_NATURE", "PROVED_IN_NATUR")
res["cabeca_truncada_recusada"] = bool(f("a cabeca: " + cab[:-5], RAMOS, n))
res["cabeca_mais_palavra_proibida_recusada"] = bool(f("a cabeca: " + cab + " CONF" + "IRMED", RAMOS, n))
res["texto_comum_com_palavra_proibida_recusado"] = bool(f("TGL CONF" + "IRMED pela natureza", RAMOS, n))
res["texto_limpo_passa"] = f("o teste nao e cego; validade, nao creditacao", RAMOS, n) == []
print(json.dumps(res, indent=1))
print("o que a P18 acha na cabeca crua:", [x[0] for x in g("a cabeca: " + cab)])
