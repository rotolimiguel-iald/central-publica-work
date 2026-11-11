# -*- coding: utf-8 -*-
"""preparar_bundle_v410_aescala_09nov.py -- v410, parte 2 (D86/D87): instala a SEGUNDA pedra do bundle, TGLExt.AEscala, no sandbox C:\\t\\k410c\\final, como preparar_bundle_v410_06nov.py instalou a IALD2:
CONFERE (a fonte em insumos\\AEscala.lean == o recibo dos nomes, modulo 2; cabecalho com a ratificacao D87; `namespace`/`end` uma vez; 38 `#print axioms` == o recibo; ancora principal e as de secao entre eles; imports do recibo, existentes no Nos v409 ou no bundle;
nenhum sorry/axiom), NORMALIZA (CRLF -> LF; REMOVE o bloco Auditoria -- o comentario, `section Auditoria`, os `#print axioms`, `end Auditoria` --; nenhuma prova tocada), grava v410\\pedra\\AEscala.lean, pedra\\origem\\AEscala.lean e o sandbox TGLExt\\AEscala.lean;
a raiz TGLExt.lean = a do Nos v409 + os DOIS imports; kernel_modulos_novos_v410.json e BUNDLE_v410.json passam a 2 modulos (o da IALD2 inalterado); os artefatos de build da IALD2 vao para a quarentena (o lake build recompila os DOIS modulos novos a frio, como o pos_build exige: linha Built);
o construir_kernel_v410.sh ganha o comentario dos dois modulos. Backups de bytes; escrita por temporario. Nada toca o Nos.  uso: python -B -X utf8 preparar_bundle_v410_aescala_09nov.py [--seco]"""
import datetime, hashlib, json, os, re, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PK = Path(os.path.dirname(os.path.abspath(__file__))); WK = PK.parent.parent
K10 = Path("C:/t/k410c/final"); QUAR = Path("C:/t/k410c") / ("quarentena_" + TS + "_aescala")
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel"); INS = PK / "insumos"
sha = lambda b: hashlib.sha256(b).hexdigest()
RECIBO_P = INS / "RECIBO_PEDRAS_v410_NOMES.json"; RECIBO = json.loads(RECIBO_P.read_text(encoding="utf-8"))
assert [m["modulo"] for m in RECIBO["modulos"]] == ["TGLExt.IALD2", "TGLExt.AEscala"], "o recibo dos nomes tem de trazer os DOIS modulos (rode _d87_ratificar_aescala_v410.py antes)"
REC = RECIBO["modulos"][1]; assert REC["print_axioms"] == REC["no_trio"] == 38 and REC["avisos"] == 0 and REC["ratificados"] is True
RAT = RECIBO["ratificacao_aescala_D87"]; assert RAT["pedra_sha256_depois"] == REC["sha256"]
BL_P = PK / "kernel_modulos_novos_v410.json"; BD_P = PK / "BUNDLE_v410.json"
BL = json.loads(BL_P.read_text(encoding="utf-8")); BD = json.loads(BD_P.read_text(encoding="utf-8"))
assert BL["novos"] == ["TGLExt/IALD2.lean"] and BD["n"] == 1 and BD["modulos"][0]["rel"] == "TGLExt/IALD2.lean", "o bundle ainda nao e' o de UM modulo (IALD2): nada a fazer ou ja' feito"
RX_PRINT = re.compile(r"^#print axioms (\S+)[ \t]*\r?\n?", re.M); RX_IMPORT = re.compile(r"^import (\S+)[ \t]*$", re.M)
src = INS / "AEscala.lean"; b = src.read_bytes(); assert sha(b) == REC["sha256"], ("a fonte em insumos\\ NAO e' a do recibo dos nomes", sha(b)[:16], REC["sha256"][:16])
t = b.decode("utf-8"); n_crlf = t.count("\r\n"); assert t.count("\r") == n_crlf; t = t.replace("\r\n", "\n")
assert t.count("namespace TGLExt.AEscala\n") == 1 and t.count("end TGLExt.AEscala\n") == 1
_tn = re.sub(r"\s+", " ", t)
for f_ in ("RATIFICADOS pelo operador em 09/11/2026", "«ratifico tudo», sha256 " + RAT["sha256"], "agora eu te dei a escala"):
    assert f_ in _tn, ("o cabecalho da pedra nao traz a ratificacao D87 como esperado", f_)
assert "CANDIDATA" not in t and "PROVISÓRIO" not in t
prints = RX_PRINT.findall(t); assert len(prints) == len(set(prints)) == REC["print_axioms"] and prints == list(REC["ancoras"]) and all(p.startswith("TGLExt.AEscala.") for p in prints)
assert REC["ancora_principal"] in prints and all("TGLExt.AEscala." + s in prints for s in REC["ancoras_de_secao"])
imps = RX_IMPORT.findall(t); assert sorted(imps) == sorted(REC["imports"]), imps
for imp in imps:
    rel_ = imp.replace(".", "/") + ".lean"
    assert (NOS / rel_).exists() or rel_ in BL["novos"], ("import ausente do kernel do Nos v409 e do bundle", imp)
# o bloco Auditoria: so' o comentario, a secao, os #print axioms e o end
i_aud = t.index("/-! ## Auditoria"); bloco = t[i_aud:]
resto = [l_ for l_ in bloco.splitlines() if l_.strip() and not l_.startswith("#print axioms") and l_.strip() not in ("section Auditoria", "end Auditoria") and not l_.startswith("/-! ## Auditoria")]
assert not resto, ("o bloco Auditoria traz mais que os #print axioms", resto[:3])
assert len(RX_PRINT.findall(bloco)) == len(prints), "ha' #print axioms fora do bloco Auditoria"
t_out = t[:i_aud].rstrip("\n") + "\n"
assert t_out.endswith("end TGLExt.AEscala\n")
_code = re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", t_out, flags=re.S))   # (o cabecalho da pedra MENCIONA «0 sorry» e «#print axioms»: a guarda e' sobre o CODIGO, sem comentarios e docstrings, como no gerador)
assert "sorry" not in _code and "#print" not in _code and "#eval" not in _code and "\r" not in t_out and not re.search(r"^\s*axiom\s", _code, re.M), "sorry/#print/#eval/axiom no codigo da pedra"
out = t_out.encode("utf-8")
raiz_nos = (NOS / "TGLExt.lean").read_text(encoding="utf-8", newline=""); raiz_k10 = (K10 / "TGLExt.lean").read_text(encoding="utf-8", newline="")
nl = "\r\n" if "\r\n" in raiz_nos else "\n"
assert BL["root_suffix"] == "import TGLExt.IALD2" + nl and raiz_k10 == raiz_nos + BL["root_suffix"], "a raiz do k410c nao e' a do Nos + o import da IALD2"
ROOT_SUFFIX = BL["root_suffix"] + "import TGLExt.AEscala" + nl
assert not (NOS / "TGLExt" / "AEscala.lean").exists(), "a pedra ja' existe no Nos"
if SECO:
    print("SECO: nada gravado;", len(out), "B normalizados;", len(prints), "#print axioms removidos; crlf->lf", n_crlf, "| root_suffix", repr(ROOT_SUFFIX)); sys.exit(0)
retirados = []


def _troca_com_backup(path, novo, no_lugar=True):
    path = Path(path)
    if path.exists():
        velho = path.read_bytes()
        if velho == novo:
            return None
        bk = path.parent / (path.name + ".bak_" + TS) if no_lugar else QUAR / path.relative_to(K10)
        bk.parent.mkdir(parents=True, exist_ok=True); bk.write_bytes(velho); assert bk.read_bytes() == velho
        retirados.append({"arquivo": str(path), "backup": str(bk), "sha256_antigo": sha(velho), "sha256_novo": sha(novo)})
    tmp = path.parent / (path.name + ".tmp_" + TS); tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo); os.replace(tmp, path); assert path.read_bytes() == novo
    return True


(PK / "pedra" / "origem").mkdir(parents=True, exist_ok=True)
_troca_com_backup(PK / "pedra" / "origem" / "AEscala.lean", b)
_troca_com_backup(PK / "pedra" / "AEscala.lean", out)
_troca_com_backup(K10 / "TGLExt" / "AEscala.lean", out, no_lugar=False)
_troca_com_backup(K10 / "TGLExt.lean", (raiz_nos + ROOT_SUFFIX).encode("utf-8"), no_lugar=False)
assert (K10 / "TGLExt.lean").read_text(encoding="utf-8", newline="") == raiz_nos + ROOT_SUFFIX
# os artefatos de build da IALD2 vao a' quarentena: o lake build recompila os DOIS modulos novos (linha Built), como o pos_build exige
movidos = []
for sub, pats in (("lib/lean/TGLExt", ("IALD2.olean", "IALD2.ilean", "IALD2.olean.hash", "IALD2.ilean.hash", "IALD2.trace")), ("ir/TGLExt", ("IALD2.c", "IALD2.c.hash", "IALD2.setup.json"))):
    for n_ in pats:
        p_ = K10 / ".lake" / "build" / sub / n_
        if p_.exists():
            d_ = QUAR / "build_IALD2" / sub; d_.mkdir(parents=True, exist_ok=True); shutil.move(str(p_), str(d_ / n_)); movidos.append(str(p_))
entry = {"rel": "TGLExt/AEscala.lean", "sha256": sha(out), "fonte_bancada": None, "origem": str(src), "sha256_origem": sha(b), "sha16_origem": sha(b)[:16], "tipo_do_nome": "09nov_nome_do_modulo_e_44_declaracoes_RATIFICADOS_pelo_operador_D87", "nome_antigo": "AEscala",
         "frase_do_nome": "agora eu te dei a escala", "origem_candidata": REC["origem"]["candidata"], "sha256_candidata": sha(Path(REC["origem"]["candidata"]).read_bytes()), "sha256_candidata_pre_d87": REC["origem"]["candidata_pre_d87_sha256"], "saida_lean": REC["saida"],
         "registro_anterior": None, "registro_anterior_sha16": None, "n_print_axioms_removidos": len(prints), "n_crlf_normalizados": n_crlf, "bytes": len(out), "status_integracao": "pedra_do_autor_aescala_09nov_ratificada_D87",
         "ancoras": list(prints), "ancora_principal": REC["ancora_principal"], "ancoras_de_secao": ["TGLExt.AEscala." + s for s in REC["ancoras_de_secao"]], "imports": list(REC["imports"]), "recibo_do_autor": REC["origem"]["recibo"], "recibo_do_autor_sha16": REC["origem"]["recibo_sha16"],
         "ratificacao_D87": {"fala": RAT["fala"], "sha256": RAT["sha256"]}}


def grava_txt(path, txt):
    path = Path(path); b_ = txt.encode("utf-8")
    if path.exists():
        if path.read_bytes() == b_:
            return
        (path.parent / (path.name + ".bak_" + TS)).write_bytes(path.read_bytes())
    tmp = path.parent / (path.name + ".tmp"); tmp.write_bytes(b_); assert tmp.stat().st_size == len(b_); os.replace(tmp, path)


rels = BL["novos"] + ["TGLExt/AEscala.lean"]
grava_txt(BL_P, json.dumps({"novos": rels, "n": 2, "root_suffix": ROOT_SUFFIX, "gerado": TS, "nota": "parte 2 (D86/D87): + TGLExt.AEscala; o da IALD2 (06/11) inalterado"}, ensure_ascii=False, indent=1))
BD["n"] = 2; BD["gerado_aescala"] = TS; BD["root_suffix"] = ROOT_SUFFIX; BD["modulos"] = BD["modulos"] + [entry]; BD["retirados_do_sandbox_e_da_pedra"] = BD.get("retirados_do_sandbox_e_da_pedra", []) + retirados
BD["recibo_dos_nomes_sha256"] = sha(RECIBO_P.read_bytes()); BD["quarentena_aescala"] = str(QUAR) if QUAR.exists() else None; BD["build_iald2_movido_para_quarentena"] = movidos
BD["aescala"] = {"ratificacao_D87": {"fala": RAT["fala"], "sha256": RAT["sha256"]}, "nota": "a segunda pedra do bundle, instalada na parte 2 (D86); nome e 44 nomes RATIFICADOS (D87); os #print axioms (bloco Auditoria) removidos da copia instalada, como na IALD2"}
grava_txt(BD_P, json.dumps(BD, ensure_ascii=False, indent=1))
sh_p = PK / "construir_kernel_v410.sh"; sh_t = sh_p.read_text(encoding="utf-8")
sh_t = sh_t.replace("o modulo novo,\n# IALD2, e' o unico a compilar)", "os modulos novos,\n# IALD2 (artefatos de build na quarentena) e AEscala (parte 2, D86/D87), sao os unicos a compilar)")
grava_txt(sh_p, sh_t)
print("bundle 2 modulos; raiz +2 imports; sandbox TGLExt/AEscala.lean gravado | AEscala embutida", sha(out)[:16], "fonte", sha(b)[:16], "| #print removidos", len(prints), "| crlf->lf", n_crlf, "| IALD2 build movido:", len(movidos))
for r_ in retirados:
    print("  retirado (com backup):", r_["arquivo"], "->", r_["backup"])
