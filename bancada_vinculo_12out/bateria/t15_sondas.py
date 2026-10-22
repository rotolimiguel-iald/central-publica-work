# -*- coding: utf-8 -*-
# T15_SONDAS -- sondas SO EM RAM sobre a COPIA: (P1) um um.py da versao seguinte sob o manifesto vigente e RECUSADO (PIN_CHANGED);
# (P2) uma segunda linha nao indentada de alpha: o canonical.py aceita a primeira (documentado), os runners do atrator recusam;
# (P3) um manifesto tipo B(n+1) pinando a versao seguinte e aceito com o MESMO beta. Nenhum byte de um.py/selo/manifesto e escrito.
# Porte parametrizado de H_BANCADA\scripts\sonda_v392.py.
# uso: t15_sondas.py <candidate> <versao> <saida.json>
import datetime, hashlib, json, math, re, sys
from pathlib import Path
from unittest.mock import patch
cand, versao, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3])
sys.dont_write_bytecode = True
sys.path.insert(0, str(cand))
from bancada import canonical
assert Path(canonical.__file__).resolve().is_relative_to(cand)


def sha(b):
    return hashlib.sha256(b).hexdigest()


orig_read = Path.read_bytes
man = json.loads(orig_read(cand / "canonical_contracts.json"))
UMPY = Path(man["canonical"]["script"]["path"]).resolve()
SEAL = Path(man["canonical"]["seal"]["path"]).resolve()
MANP = (cand / "canonical_contracts.json").resolve()
um = orig_read(UMPY)
txt = um.decode("utf-8-sig")
mv = re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', txt, re.M)
assert mv and mv.group(1) == versao, (mv.group(1) if mv else None, versao)
num = re.match(r"v(\d+)$", versao)
seguinte = "v%d" % (int(num.group(1)) + 1) if num else versao + "-seguinte"
# a troca EXATA da linha de coluna 0 (mesmo comprimento quando possivel)
velha = mv.group(0).encode("utf-8")
nova = velha.replace(versao.encode("utf-8"), seguinte.encode("utf-8"), 1)
um_seg = um.replace(velha, nova, 1)
assert um_seg != um
res = dict(teste="T15_SONDAS", quando=datetime.datetime.now().isoformat(timespec="seconds"), versao=versao, versao_seguinte=seguinte)
# P1
canonical._registries.clear()
with patch.object(Path, "read_bytes", lambda p: um_seg if Path(p).resolve() == UMPY else orig_read(p)):
    try:
        canonical.get_registry(cand).check("P1")
        res["P1_seguinte_sob_manifesto_vigente"] = "ACEITO (inesperado)"
        p1 = False
    except canonical.CanonicalError as e:
        res["P1_seguinte_sob_manifesto_vigente"] = "RECUSADO: " + str(e).split(":")[0]
        p1 = str(e).split(":")[0] in ("PIN_CHANGED", "CANONICAL_VERSION_CHANGED", "SEAL_PROGRAM_MISMATCH")
# P2
txt2 = txt + "\nALPHA_FINE_CODATA_2018 = 7.2973525693e-3\n"
m_canon = re.search(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", txt2, re.M)
m_runner = list(re.finditer(r"^ALPHA_FINE_CODATA_2018[ \t]*=[ \t]*([^\r\n]+)\r?$", txt2, re.MULTILINE))
res["P2_alpha_linhas_hoje"] = len(list(re.finditer(r"^ALPHA_FINE_CODATA_2018[ \t]*=", txt, re.M)))
res["P2_canonical_py_com_segunda_linha"] = "ACEITA a primeira ocorrencia (linha %d), sem recusa -- a B3 leva a unicidade ao canonical.py" % (txt2[:m_canon.start()].count("\n") + 1)
res["P2_runner_do_atrator_com_segunda_linha"] = "RECUSA (Alpha assignment not unique)" if len(m_runner) != 1 else "aceita"
p2 = res["P2_alpha_linhas_hoje"] == 1 and len(m_runner) != 1
# P3
seal = json.loads(orig_read(SEAL))
seal_seg = dict(seal)
seal_seg["um_version"] = seguinte
seal_seg["sha256"] = dict(seal.get("sha256", {}))
seal_seg["sha256"]["um.py"] = sha(um_seg)
seal_seg_b = json.dumps(seal_seg, ensure_ascii=False).encode("utf-8")
man_seg = json.loads(orig_read(MANP))
man_seg["canonical"]["version"] = seguinte
man_seg["canonical"]["script"]["sha256"] = sha(um_seg)
man_seg["canonical"]["script"]["bytes"] = len(um_seg)
man_seg["canonical"]["seal"]["sha256"] = sha(seal_seg_b)
man_seg["canonical"]["seal"]["bytes"] = len(seal_seg_b)
man_seg["deployment_id"] = "B-SIMULADO-EM-RAM"
man_b = json.dumps(man_seg, ensure_ascii=False).encode("utf-8")


def leitor3(path):
    p = Path(path).resolve()
    if p == UMPY:
        return um_seg
    if p == SEAL:
        return seal_seg_b
    if p == MANP:
        return man_b
    return orig_read(path)


canonical._registries.clear()
with patch.object(Path, "read_bytes", leitor3):
    try:
        r3 = canonical.get_registry(cand).check("P3")
        beta0 = float(re.search(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", txt, re.M).group(1)) * math.sqrt(math.e)
        res["P3_manifesto_tipo_B_seguinte"] = dict(ok=r3["ok"], version=r3["canonical_version"], beta_tgl=repr(r3["beta_tgl"]), beta_inalterado=(r3["beta_tgl"] == beta0))
        p3 = r3["ok"] and r3["canonical_version"] == seguinte and r3["beta_tgl"] == beta0
    except canonical.CanonicalError as e:
        res["P3_manifesto_tipo_B_seguinte"] = "RECUSADO: " + str(e)
        p3 = False
canonical._registries.clear()
res["P0_estado_real_apos_sondas"] = canonical.get_registry(cand).check("P0")["canonical_version"]
p0 = res["P0_estado_real_apos_sondas"] == versao
res["veredito"] = "PASSA" if (p1 and p2 and p3 and p0) else "FALHA"
res["scope"] = "RAM-only probes; no um.py/seal/manifest bytes written anywhere"
with out.open("x", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False))
sys.exit(0 if res["veredito"] == "PASSA" else 1)
