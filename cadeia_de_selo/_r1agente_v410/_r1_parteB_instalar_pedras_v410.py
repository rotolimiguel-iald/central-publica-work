# -*- coding: utf-8 -*-
"""_r1_parteB_instalar_pedras_v410.py -- R1 (D92), PARTE B, passo 1: instala as pedras R3 (work\\pedras_candidatas_09nov\\R3_escala_no_tipo): AEscala (a ESCALA NO TIPO do LeitorDoFundo e as aspas) e IALD2 (so' docstrings).
Confere os sha256 dos arquivos contra os da ORDEM da gerencia (10/11 00:20) e contra o recibo do autor (divergencia = PARA); copia as fontes para insumos\\ (as anteriores ficam ao lado, com nome proprio); gera as formas instaladas (a fonte sem o bloco Auditoria, LF),
conferindo a da IALD2 contra a forma instalada esperada pela gerencia; grava pedra\\, pedra\\origem\\ e o sandbox k410c (backup em quarentena); atualiza o recibo dos nomes (insumos\\RECIBO_PEDRAS_v410_NOMES.json: as ancoras LIDAS dos #print axioms; os 44 ratificados conferidos; os nomes novos, a ratificar)
e o BUNDLE_v410.json. NAO compila (construir_kernel_v410.sh vem depois) e nao toca o Nos. Backup de BYTES; temporario -> conferir -> substituir.   uso: python -I -B -X utf8 _r1_parteB_instalar_pedras_v410.py [--seco]"""
import datetime, hashlib, json, os, re, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv; TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PK = Path(os.path.dirname(os.path.abspath(__file__))); INS = PK / "insumos"; K10 = Path("C:/t/k410c/final"); QUAR = Path("C:/t/k410c") / ("quarentena_" + TS + "_r3")
R3 = PK.parent.parent / "pedras_candidatas_09nov" / "R3_escala_no_tipo"
sha = lambda b: hashlib.sha256(b).hexdigest()
# [DECLARADO pela gerencia na ORDEM de 10/11 00:20] os sha256 esperados; o que vale e' o LIDO do arquivo, que tem de ser igual
ORDEM = {"AEscala.lean": "ee0bdb45853db4f791295be637a5897beea38807a159965f72bbcaebec6fea91", "IALD2_com_auditoria.lean": "dc152339e6b58e89c6a62881ac1e074f00dcee9ec494c40c392f8ef1b38d276c",
         "IALD2.lean": "4a7b01f5be46c25c1c0f556909e7c7bbc2a620b772392d635ff0872dff656f9e", "RECIBO_AESCALA_R3_09nov.json": "bf6c61d6442a742b70b0c461c3dae9b0d9cdfba135dba55beaf92aac08624e50"}
B = {n: (R3 / n).read_bytes() for n in ORDEM}
for n, h in ORDEM.items():
    assert sha(B[n]) == h, ("PARE: o sha256 lido nao e' o da ordem da gerencia", n, sha(B[n]))
RA = json.loads(B["RECIBO_AESCALA_R3_09nov.json"].decode("utf-8"))
assert RA["aescala_r3"]["sha256"] == ORDEM["AEscala.lean"] and RA["trio"]["todas_no_trio"] is True and RA["trio"]["fora_do_trio"] == {} and RA["compilacao"]["n_erros"] == 0 and RA["compilacao"]["n_avisos"] == 0 and RA["compilacao"]["sorry_no_log"] is False
assert RA["nomes_dos_44_ratificados"]["n_mantidos"] == 44 and RA["nomes_dos_44_ratificados"]["sumidos"] == [] and RA["o_que_nao_fechou"] == [] and RA["frases_vedadas_presentes"] == []
NOVOS = list(RA["nomes_novos"]["lista"]); CAMPOS = list(RA["nomes_novos"]["campos_novos_da_estrutura"])
NOVOS_DA_ORDEM = ["LeitorDoFundo.leitura", "LeitorDoFundo.limite", "LeitorDoFundo.o_brilho_e_a_dissipacao", "LeitorDoFundo.a_leitura_e_a_do_psion", "LeitorDoFundo.sem_escala_a_leitura_e_um", "LeitorDoFundo.a_leitura_tende_ao_que_sou", "LeitorDoFundo.o_limite_e_o_que_sou",
                  "LeitorDoFundo.le_como_dissipacao", "LeitorDoFundo.diz_a_face_sem_leitura", "o_leitor_do_fundo_e_a_iald", "o_decisor_sem_escala_nao_e_leitor_do_fundo", "a_escala_e_meio_por_oitava", "em_n_oitavas_o_fundo_pesa_um_pixel"]
assert sorted(NOVOS) == sorted(NOVOS_DA_ORDEM) and len(NOVOS) == 13 and sorted(CAMPOS) == sorted(["brilho", "sem_escala_nao_ha_medida", "a_lei_da_dissipacao"]), ("os nomes novos do recibo do autor != os da ordem da gerencia", sorted(set(NOVOS) ^ set(NOVOS_DA_ORDEM)), CAMPOS)
RX_PRINT = re.compile(r"^#print axioms (\S+)\s*$", re.M); RX_IMPORT = re.compile(r"^import (\S+)\s*$", re.M)
REC_P = INS / "RECIBO_PEDRAS_v410_NOMES.json"; REC = json.loads(REC_P.read_text(encoding="utf-8")); MI, MA = REC["modulos"]
assert MI["modulo"] == "TGLExt.IALD2" and MA["modulo"] == "TGLExt.AEscala" and len(MA["nomes"]) == 44
BD_P = PK / "BUNDLE_v410.json"; BD = json.loads(BD_P.read_text(encoding="utf-8")); assert BD["n"] == 2 and [m["rel"] for m in BD["modulos"]] == ["TGLExt/IALD2.lean", "TGLExt/AEscala.lean"]


def instalada(nome_mod, fonte_b):
    t = fonte_b.decode("utf-8"); n_crlf = t.count("\r\n"); assert t.count("\r") == n_crlf; t = t.replace("\r\n", "\n")
    assert t.count("namespace TGLExt.%s\n" % nome_mod) == 1 and t.count("end TGLExt.%s\n" % nome_mod) == 1
    prints = RX_PRINT.findall(t); assert prints and len(prints) == len(set(prints)) and all(p.startswith("TGLExt.%s." % nome_mod) for p in prints)
    if "/-! ## Auditoria" in t:   # (a AEscala traz o bloco Auditoria no fim: sai inteiro)
        i_aud = t.index("/-! ## Auditoria"); bloco = t[i_aud:]
        resto = [l_ for l_ in bloco.splitlines() if l_.strip() and not l_.startswith("#print axioms") and l_.strip() not in ("section Auditoria", "end Auditoria") and not l_.startswith("/-! ## Auditoria")]
        fecha = [l_ for l_ in resto if not (l_.strip().startswith("--") or l_.strip() in ("-/",) or "#print axioms" in l_)]   # (so' comentario pode sobrar no bloco)
        assert len(RX_PRINT.findall(bloco)) == len(prints), "ha' #print axioms fora do bloco Auditoria"
        out = t[:i_aud].rstrip("\n") + "\n"
    else:   # (a IALD2 traz so' os #print axioms no fim, sem bloco: saem as linhas)
        i_p = t.index("#print axioms"); assert len(RX_PRINT.findall(t[i_p:])) == len(prints) and not [l_ for l_ in t[i_p:].splitlines() if l_.strip() and not l_.startswith("#print axioms")], "ha' texto entre os #print axioms finais"
        fecha = []; out = t[:i_p].rstrip("\n") + "\n"
    assert out.endswith("end TGLExt.%s\n" % nome_mod), (nome_mod, out[-80:])
    code = re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", out, flags=re.S))
    assert "sorry" not in code and "#print" not in code and "#eval" not in code and "\r" not in out and not re.search(r"^\s*axiom\s", code, re.M), "sorry/#print/#eval/axiom no codigo da pedra"
    return out.encode("utf-8"), prints, RX_IMPORT.findall(t), n_crlf, fecha


outA, printsA, impsA, crlfA, restoA = instalada("AEscala", B["AEscala.lean"])
outI, printsI, impsI, crlfI, restoI = instalada("IALD2", B["IALD2_com_auditoria.lean"])
assert sha(outI) == ORDEM["IALD2.lean"] == sha(B["IALD2.lean"]), ("a forma instalada da IALD2 (a fonte sem a Auditoria) nao e' a esperada pela gerencia", sha(outI)[:16])
assert len(printsA) == RA["trio"]["n_auditadas"] == 51 and printsI == list(BD["modulos"][0]["ancoras"]) and len(printsI) == MI["print_axioms"] == 22, (len(printsA), len(printsI))
tA = outA.decode("utf-8"); tA_ws = re.sub(r"\s+", " ", tA)
for nm in MA["nomes"]:   # os 44 ratificados seguem declarados na R3, com o mesmo nome
    assert re.search(r"(?m)^(?:noncomputable\s+|private\s+|protected\s+)*(?:theorem|lemma|def|structure|abbrev|instance)\s+" + re.escape(nm.split(".")[-1]) + r"\b", tA), ("um dos 44 ratificados nao esta' declarado na R3", nm)
assert MA["ancora_principal"] in printsA and all(("TGLExt.AEscala." + s) in printsA for s in MA["ancoras_de_secao"]) and all(("TGLExt.AEscala." + n) in printsA or n.split(".")[-1] in ("leitura", "limite") for n in NOVOS), "ancora principal, de secao ou nome novo fora dos #print axioms da R3"
RAT = REC["ratificacao_aescala_D87"]
assert "RATIFICADOS pelo operador em 09/11/2026" in tA_ws and RAT["sha256"] in tA_ws and "namespace TGLExt.AEscala" in tA, "o cabecalho da R3 nao traz a ratificacao D87 (a c3 do registro a exige)"
print("AEscala R3: fonte", sha(B["AEscala.lean"])[:16], len(B["AEscala.lean"]), "B -> instalada", sha(outA)[:16], len(outA), "B | #print", len(printsA), "| imports", impsA, "| crlf", crlfA, "| resto do bloco:", restoA[:2])
print("IALD2   R3: fonte", sha(B["IALD2_com_auditoria.lean"])[:16], "-> instalada", sha(outI)[:16], "(= a esperada pela gerencia) | #print", len(printsI), "| imports", len(impsI))
print("nomes novos (a ratificar):", len(NOVOS), "| campos novos:", CAMPOS, "| ancoras novas da AEscala:", len(set(printsA) - set(MA["ancoras"])), "| ancoras que sairam:", sorted(set(MA["ancoras"]) - set(printsA)))
if SECO:
    print("--seco: nada gravado"); sys.exit(0)


def troca(path, novo, guarda_como=None):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        velho = path.read_bytes()
        if velho == novo:
            return
        bk = Path(guarda_como) if guarda_como else path.parent / (path.name + ".bak_" + TS + "_pre_r3")
        bk.parent.mkdir(parents=True, exist_ok=True); bk.write_bytes(velho); assert bk.read_bytes() == velho
    tmp = path.parent / (path.name + ".tmp_" + TS); tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo); os.replace(tmp, path); assert path.read_bytes() == novo


antes = {"AEscala_fonte": sha((INS / "AEscala.lean").read_bytes()), "IALD2_fonte": sha((INS / "IALD2.lean").read_bytes()), "AEscala_instalada": sha((PK / "pedra" / "AEscala.lean").read_bytes()), "IALD2_instalada": sha((PK / "pedra" / "IALD2.lean").read_bytes())}
troca(INS / "AEscala.lean", B["AEscala.lean"], INS / "AEscala_ratificada_D87_pre_r3.lean"); troca(INS / "IALD2.lean", B["IALD2_com_auditoria.lean"], INS / "IALD2_pre_r3.lean")
troca(INS / "RECIBO_AESCALA_R3_09nov.json", B["RECIBO_AESCALA_R3_09nov.json"]); troca(INS / "compile_log_AEscala_R3.txt", (R3 / "compile_log.txt").read_bytes())
troca(PK / "pedra" / "origem" / "AEscala.lean", B["AEscala.lean"]); troca(PK / "pedra" / "origem" / "IALD2.lean", B["IALD2_com_auditoria.lean"])
troca(PK / "pedra" / "AEscala.lean", outA); troca(PK / "pedra" / "IALD2.lean", outI)
troca(K10 / "TGLExt" / "AEscala.lean", outA, QUAR / "TGLExt" / "AEscala.lean"); troca(K10 / "TGLExt" / "IALD2.lean", outI, QUAR / "TGLExt" / "IALD2.lean")
r3 = {"decisao": "D92", "quando": TS, "pasta": str(R3), "recibo_do_autor": str(INS / "RECIBO_AESCALA_R3_09nov.json"), "recibo_do_autor_sha256": ORDEM["RECIBO_AESCALA_R3_09nov.json"], "compile_log_sha256": sha((R3 / "compile_log.txt").read_bytes()), "sha256_antes": antes}
MA.update({"sha256_ratificada_D87": RAT["pedra_sha256_depois"], "sha256": sha(B["AEscala.lean"]), "sha16": sha(B["AEscala.lean"])[:16], "bytes": len(B["AEscala.lean"]), "print_axioms": len(printsA), "no_trio": len(printsA), "avisos": 0, "ancoras": list(printsA), "imports": list(impsA),
           "declaracoes_n": 44, "declaracoes_n_r3": RA["declaracoes"]["n_R3"], "nomes_novos_a_ratificar": list(NOVOS), "campos_novos_da_estrutura": list(CAMPOS), "estatuto_dos_nomes_novos": RA["nomes_novos"]["estatuto"], "r3": r3})
MA["origem"] = dict(MA["origem"], candidata_r3=str(R3 / "AEscala.lean"), candidata_r3_sha256=sha(B["AEscala.lean"]))
MI.update({"sha256_pre_r3": MI["sha256"], "sha256": sha(B["IALD2_com_auditoria.lean"]), "sha16": sha(B["IALD2_com_auditoria.lean"])[:16], "imports": list(impsI) if sorted(impsI) != sorted(MI["imports"]) else MI["imports"], "r3": dict(r3, o_que_mudou="so' docstrings (duas aspas, o cabecalho dos nomes ratificados, o item 5 do atrator)")})
REC["r3_d92"] = {"quando": TS, "nota": "pedras R3 instaladas pelo construtor por ordem da gerencia (D92): AEscala com a escala no TIPO do LeitorDoFundo e as aspas; IALD2 so' docstrings; os 44 ratificados ficam; os nomes novos ficam a ratificar", "nomes_novos_a_ratificar": list(NOVOS), "campos_novos_da_estrutura": list(CAMPOS)}
troca(REC_P, json.dumps(REC, ensure_ascii=False, indent=1).encode("utf-8"))
eI, eA = BD["modulos"]
eI.update({"sha256_pre_r3": eI["sha256"], "sha256": sha(outI), "origem": str(INS / "IALD2.lean"), "sha256_origem": sha(B["IALD2_com_auditoria.lean"]), "sha16_origem": sha(B["IALD2_com_auditoria.lean"])[:16], "bytes": len(outI), "n_crlf_normalizados": crlfI, "r3": "D92: so' docstrings"})
eA.update({"sha256_pre_r3": eA["sha256"], "sha256": sha(outA), "origem": str(INS / "AEscala.lean"), "sha256_origem": sha(B["AEscala.lean"]), "sha16_origem": sha(B["AEscala.lean"])[:16], "bytes": len(outA), "n_crlf_normalizados": crlfA, "n_print_axioms_removidos": len(printsA),
           "ancoras": list(printsA), "imports": list(impsA), "status_integracao": "pedra_R3_a_escala_no_tipo_D92__44_nomes_ratificados_D87__nomes_novos_a_ratificar", "nomes_novos_a_ratificar": list(NOVOS), "campos_novos_da_estrutura": list(CAMPOS),
           "recibo_do_autor_r3": str(INS / "RECIBO_AESCALA_R3_09nov.json"), "recibo_do_autor_r3_sha16": ORDEM["RECIBO_AESCALA_R3_09nov.json"][:16]})
BD["recibo_dos_nomes_sha256"] = sha(REC_P.read_bytes()); BD["r3_d92"] = {"quando": TS, "quarentena": str(QUAR) if QUAR.exists() else None}
troca(BD_P, json.dumps(BD, ensure_ascii=False, indent=1).encode("utf-8"))
print("INSTALADO: insumos, pedra, pedra/origem e sandbox k410c | recibo dos nomes", sha(REC_P.read_bytes())[:16], "| BUNDLE", sha(BD_P.read_bytes())[:16], "| quarentena:", QUAR if QUAR.exists() else "nenhuma")
