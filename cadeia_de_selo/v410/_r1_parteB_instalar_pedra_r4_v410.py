# -*- coding: utf-8 -*-
"""_r1_parteB_instalar_pedra_r4_v410.py -- R1, PARTE B (ordem da gerencia de 10/11 00:40, D93/D94): instala a pedra AEscala R4 (work\\pedras_candidatas_09nov\\R4_o_leitor_e_a_escala), que SUBSTITUI a R3 (instalada como provisoria); a IALD2 e' a da R3, ja' instalada (conferida aqui).
Confere os sha256 contra os da ORDEM e contra o recibo do autor (divergencia = PARA); a fonte vai a insumos\\ (a R3 fica ao lado); a forma instalada (a fonte sem o bloco Auditoria, LF) vai a pedra\\ e ao sandbox k410c (backup em quarentena);
o recibo dos nomes e o BUNDLE sao atualizados: as ancoras LIDAS dos #print axioms; os 44 ratificados e os nomes da R3 conferidos; os nomes novos (os 13 da R3 mais os da R4) e os 3 campos ficam A RATIFICAR. NAO compila e nao toca o Nos.   uso: python -I -B -X utf8 _r1_parteB_instalar_pedra_r4_v410.py [--seco]"""
import datetime, hashlib, json, os, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv; TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PK = Path(os.path.dirname(os.path.abspath(__file__))); INS = PK / "insumos"; K10 = Path("C:/t/k410c/final"); QUAR = Path("C:/t/k410c") / ("quarentena_" + TS + "_r4")
R3 = PK.parent.parent / "pedras_candidatas_09nov" / "R3_escala_no_tipo"; R4 = PK.parent.parent / "pedras_candidatas_09nov" / "R4_o_leitor_e_a_escala"
sha = lambda b: hashlib.sha256(b).hexdigest()
# [DECLARADO pela gerencia na ORDEM de 10/11 00:40] os sha256 esperados; o que vale e' o LIDO do arquivo, que tem de ser igual
ORDEM = {"AEscala.lean": "cd45cf1528269760d9b70d860c11185ef3f825817d1e90d92895955759d3d194", "RECIBO_AESCALA_R4_10nov.json": "e61f4801b0caea60b188ef21013b2d9306ec8945aeb92f4146fd6b90c6b067c5",
         "IALD2_com_auditoria.lean": "dc152339e6b58e89c6a62881ac1e074f00dcee9ec494c40c392f8ef1b38d276c", "IALD2.lean": "4a7b01f5be46c25c1c0f556909e7c7bbc2a620b772392d635ff0872dff656f9e"}
B = {"AEscala.lean": (R4 / "AEscala.lean").read_bytes(), "RECIBO_AESCALA_R4_10nov.json": (R4 / "RECIBO_AESCALA_R4_10nov.json").read_bytes(), "IALD2_com_auditoria.lean": (R3 / "IALD2_com_auditoria.lean").read_bytes(), "IALD2.lean": (R3 / "IALD2.lean").read_bytes()}
for n, h in ORDEM.items():
    assert sha(B[n]) == h, ("PARE: o sha256 lido nao e' o da ordem da gerencia", n, sha(B[n]))
RA = json.loads(B["RECIBO_AESCALA_R4_10nov.json"].decode("utf-8")); LOG = (R4 / "compile_log.txt").read_bytes()
assert RA["aescala_r4"]["sha256"] == ORDEM["AEscala.lean"] and RA["trio"]["todas_no_trio"] is True and RA["trio"]["fora_do_trio"] == {} and RA["compilacao"]["n_erros"] == 0 and RA["compilacao"]["n_avisos"] == 0 and RA["compilacao"]["sorry_no_log"] is False and RA["compilacao"]["log_sha256"] == sha(LOG)
assert RA["nomes_da_R3_incluindo_os_44_ratificados"]["sumidos"] == [] and RA["frases_vedadas_presentes"] == [], (RA["nomes_da_R3_incluindo_os_44_ratificados"]["sumidos"], RA["frases_vedadas_presentes"])
RX_PRINT = re.compile(r"^#print axioms (\S+)\s*$", re.M); RX_IMPORT = re.compile(r"^import (\S+)\s*$", re.M)
REC_P = INS / "RECIBO_PEDRAS_v410_NOMES.json"; REC = json.loads(REC_P.read_text(encoding="utf-8")); MI, MA = REC["modulos"]
assert MI["modulo"] == "TGLExt.IALD2" and MA["modulo"] == "TGLExt.AEscala" and len(MA["nomes"]) == 44 and MI["sha256"] == ORDEM["IALD2_com_auditoria.lean"], "o recibo dos nomes nao esta' no estado da R3 (rode antes _r1_parteB_instalar_pedras_v410.py)"
assert sha((PK / "pedra" / "IALD2.lean").read_bytes()) == ORDEM["IALD2.lean"] == sha((K10 / "TGLExt" / "IALD2.lean").read_bytes()) and sha((INS / "IALD2.lean").read_bytes()) == ORDEM["IALD2_com_auditoria.lean"], "a IALD2 instalada nao e' a da R3"
NOVOS_R3 = list(MA.get("nomes_novos_a_ratificar_r3") or MA["nomes_novos_a_ratificar"]); NOVOS_R4 = list(RA["nomes_novos"]["lista"]); CAMPOS = list(MA["campos_novos_da_estrutura"])
NOVOS_R4_DA_ORDEM = ["o_leitor_e_a_escala", "cada_ciclo_aplica_a_mesma_regra", "os_passos_sao_o_ciclo_ate_o_tetelestai", "a_mentira_lida_como_mentira_e_verdade", "o_pai_da_mentira_so_nao_reconhece"]
assert len(NOVOS_R3) == 13 and sorted(NOVOS_R4) == sorted(NOVOS_R4_DA_ORDEM) and len(CAMPOS) == 3 and not (set(NOVOS_R3) & set(NOVOS_R4)), ("os nomes novos do recibo != os da ordem", NOVOS_R3, NOVOS_R4)
NOVOS = NOVOS_R3 + NOVOS_R4
BD_P = PK / "BUNDLE_v410.json"; BD = json.loads(BD_P.read_text(encoding="utf-8")); assert BD["n"] == 2 and [m["rel"] for m in BD["modulos"]] == ["TGLExt/IALD2.lean", "TGLExt/AEscala.lean"]
t = B["AEscala.lean"].decode("utf-8"); n_crlf = t.count("\r\n"); assert t.count("\r") == n_crlf; t = t.replace("\r\n", "\n")
assert t.count("namespace TGLExt.AEscala\n") == 1 and t.count("end TGLExt.AEscala\n") == 1
prints = RX_PRINT.findall(t); assert len(prints) == len(set(prints)) == RA["trio"]["n_auditadas"] and all(p.startswith("TGLExt.AEscala.") for p in prints)
i_aud = t.index("/-! ## Auditoria"); bloco = t[i_aud:]; assert len(RX_PRINT.findall(bloco)) == len(prints), "ha' #print axioms fora do bloco Auditoria"
out = (t[:i_aud].rstrip("\n") + "\n"); assert out.endswith("end TGLExt.AEscala\n")
code = re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", out, flags=re.S)); assert "sorry" not in code and "#print" not in code and "#eval" not in code and not re.search(r"^\s*axiom\s", code, re.M)
outb = out.encode("utf-8"); imps = RX_IMPORT.findall(t); t_ws = re.sub(r"\s+", " ", out); RAT = REC["ratificacao_aescala_D87"]
for nm in list(MA["nomes"]) + NOVOS:   # os 44 ratificados, os 13 da R3 e os da R4 estao declarados na R4
    assert re.search(r"(?m)^(?:noncomputable\s+|private\s+|protected\s+)*(?:theorem|lemma|def|structure|abbrev|instance)\s+" + re.escape(nm) + r"\b", out), ("nome nao declarado na R4", nm)
assert MA["ancora_principal"] in prints and all(("TGLExt.AEscala." + s) in prints for s in MA["ancoras_de_secao"]) and all(a in prints for a in MA["ancoras"]), "ancora principal, de secao ou ancora da R3 fora dos #print axioms da R4"
assert "RATIFICADOS pelo operador em 09/11/2026" in t_ws and RAT["sha256"] in t_ws, "o cabecalho da R4 nao traz a ratificacao D87 (a c3 do registro a exige)"
import importlib.util as _ilu
sys.path.insert(0, str(PK)); import delta_v410 as DL   # (so' as frases canonicas, para conferir que a pedra as traz intactas)
assert re.sub(r"\s+", " ", DL.FRASE_CLAY_CANONICA_PT) in t_ws and re.sub(r"\s+", " ", DL.FRASE_D83_OBRIGATORIA_PT) in t_ws, "a frase canonica (D84) ou a forma da D83 nao estao intactas na R4"
print("AEscala R4: fonte", sha(B["AEscala.lean"])[:16], len(B["AEscala.lean"]), "B -> instalada", sha(outb)[:16], len(outb), "B | #print", len(prints), "| imports", imps, "| ancoras novas sobre a R3:", sorted(set(prints) - set(MA["ancoras"])))
print("nomes novos a ratificar:", len(NOVOS), "(13 da R3 +", len(NOVOS_R4), "da R4) | campos:", CAMPOS, "| IALD2: a da R3, ja' instalada")
if SECO:
    print("--seco: nada gravado"); sys.exit(0)


def troca(path, novo, guarda_como=None):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        velho = path.read_bytes()
        if velho == novo:
            return
        bk = Path(guarda_como) if guarda_como else path.parent / (path.name + ".bak_" + TS + "_pre_r4")
        bk.parent.mkdir(parents=True, exist_ok=True); bk.write_bytes(velho); assert bk.read_bytes() == velho
    tmp = path.parent / (path.name + ".tmp_" + TS); tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo); os.replace(tmp, path); assert path.read_bytes() == novo


antes = {"AEscala_fonte_R3": sha((INS / "AEscala.lean").read_bytes()), "AEscala_instalada_R3": sha((PK / "pedra" / "AEscala.lean").read_bytes())}
troca(INS / "AEscala.lean", B["AEscala.lean"], INS / "AEscala_R3_pre_r4.lean"); troca(INS / "RECIBO_AESCALA_R4_10nov.json", B["RECIBO_AESCALA_R4_10nov.json"]); troca(INS / "compile_log_AEscala_R4.txt", LOG)
troca(PK / "pedra" / "origem" / "AEscala.lean", B["AEscala.lean"]); troca(PK / "pedra" / "AEscala.lean", outb); troca(K10 / "TGLExt" / "AEscala.lean", outb, QUAR / "TGLExt" / "AEscala.lean")
r4 = {"decisao": "D93/D94", "quando": TS, "pasta": str(R4), "recibo_do_autor": str(INS / "RECIBO_AESCALA_R4_10nov.json"), "recibo_do_autor_sha256": ORDEM["RECIBO_AESCALA_R4_10nov.json"], "compile_log_sha256": sha(LOG), "sha256_antes": antes}
MA.update({"sha256_r3": MA["sha256"], "sha256": sha(B["AEscala.lean"]), "sha16": sha(B["AEscala.lean"])[:16], "bytes": len(B["AEscala.lean"]), "print_axioms": len(prints), "no_trio": len(prints), "avisos": 0, "ancoras": list(prints), "imports": list(imps),
           "nomes_novos_a_ratificar_r3": list(NOVOS_R3), "nomes_novos_a_ratificar_r4": list(NOVOS_R4), "nomes_novos_a_ratificar": list(NOVOS), "campos_novos_da_estrutura": list(CAMPOS), "r4": r4})
MA["origem"] = dict(MA["origem"], candidata_r4=str(R4 / "AEscala.lean"), candidata_r4_sha256=sha(B["AEscala.lean"]))
REC["r4_d94"] = {"quando": TS, "nota": "pedra AEscala R4 instalada pelo construtor por ordem da gerencia (D93/D94: a resposta do operador): o leitor E' a escala; os passos SAO o ciclo ate' o Tetelestai; a IALD2 e' a da R3; os 44 ratificados ficam; os nomes novos (R3 e R4) ficam a ratificar",
                 "nomes_novos_a_ratificar": list(NOVOS), "campos_novos_da_estrutura": list(CAMPOS)}
troca(REC_P, json.dumps(REC, ensure_ascii=False, indent=1).encode("utf-8"))
eA = BD["modulos"][1]
eA.update({"sha256_r3": eA["sha256"], "sha256": sha(outb), "origem": str(INS / "AEscala.lean"), "sha256_origem": sha(B["AEscala.lean"]), "sha16_origem": sha(B["AEscala.lean"])[:16], "bytes": len(outb), "n_crlf_normalizados": n_crlf, "n_print_axioms_removidos": len(prints),
           "ancoras": list(prints), "imports": list(imps), "status_integracao": "pedra_R4_o_leitor_e_a_escala_D94__44_nomes_ratificados_D87__nomes_novos_a_ratificar", "nomes_novos_a_ratificar": list(NOVOS), "campos_novos_da_estrutura": list(CAMPOS),
           "recibo_do_autor_r4": str(INS / "RECIBO_AESCALA_R4_10nov.json"), "recibo_do_autor_r4_sha16": ORDEM["RECIBO_AESCALA_R4_10nov.json"][:16]})
BD["recibo_dos_nomes_sha256"] = sha(REC_P.read_bytes()); BD["r4_d94"] = {"quando": TS, "quarentena": str(QUAR) if QUAR.exists() else None}
troca(BD_P, json.dumps(BD, ensure_ascii=False, indent=1).encode("utf-8"))
print("INSTALADA a R4: insumos, pedra, pedra/origem e sandbox k410c | recibo dos nomes", sha(REC_P.read_bytes())[:16], "| BUNDLE", sha(BD_P.read_bytes())[:16], "| quarentena:", QUAR if QUAR.exists() else "nenhuma")
