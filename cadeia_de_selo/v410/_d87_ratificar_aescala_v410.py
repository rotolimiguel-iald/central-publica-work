# -*- coding: utf-8 -*-
"""_d87_ratificar_aescala_v410.py -- D87 (09/11/2026, ~17:45; ratificacao do operador, «ratifico tudo», lida do arquivo por sha256 e conferida contra o DESENHO): (1) no CABECALHO de AEscala.lean troca a frase «[DECLARADO] até a ratificação» pela ratificacao
(so' docstring; nenhuma prova muda), recompila com `lake env lean` no sandbox k410c (0 erros, 0 avisos, 38 `#print axioms` no trio) e registra o sha256 NOVO no RECIBO_AESCALA_09nov.json AO LADO (campo ratificacao_D87: sha_antes/sha_depois); (2) copia a fonte ratificada para
insumos\\AEscala.lean, os bytes pre-D87 para insumos\\AEscala_candidata_09nov.lean e o log da compilacao para insumos\\saida_lean_AEscala.txt; (3) RECIBO_PEDRAS_v410_NOMES.json ganha o modulo TGLExt.AEscala (ordem 2), as 8 falas de 09/11 por sha256 LIDO de cada arquivo,
falas_n 23 e o campo ratificacao_aescala_D87 (a fala por sha256 e a lista dos 44 nomes). Backup de bytes antes de tocar cada arquivo; escrita por temporario; nada e' digitado: hashes lidos.  uso: python -B -X utf8 _d87_ratificar_aescala_v410.py"""
import datetime, hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE)); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PC = os.path.join(WK, "pedras_candidatas_09nov"); CUN = os.path.join(WK, "cunhagens_13out"); INS = os.path.join(HERE, "insumos"); K10 = r"C:\t\k410c\final"
LEAN = os.path.join(PC, "AEscala.lean"); REC_A = os.path.join(PC, "RECIBO_AESCALA_09nov.json"); REC_N = os.path.join(INS, "RECIBO_PEDRAS_v410_NOMES.json")
RAT = os.path.join(CUN, "OPERADOR_09nov_ratifico_tudo_aescala_nome_da_pedra_e_44_nomes_verbatim.txt")
sha = lambda b: hashlib.sha256(b).hexdigest(); rd = lambda p: open(p, "rb").read()


def grava(path, b):
    """backup de BYTES se existir e diferir; escrita por temporario; confere o tamanho."""
    if os.path.exists(path):
        old = rd(path)
        if old == b:
            return False
        bk = path + ".bak_" + TS + "_d87"; open(bk, "wb").write(old); assert rd(bk) == old
    tmp = path + ".tmp_" + TS; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, path); assert rd(path) == b
    return True


# ---- a ratificacao: LIDA do arquivo; conferida contra o DESENHO (D87)
b_rat = rd(RAT); sha_rat = sha(b_rat); t_rat = b_rat.decode("utf-8")
DES = rd(os.path.join(HERE, "DESENHO_v410.md")).decode("utf-8")
m87 = re.search(r"D87, RATIFICAÇÃO do operador\*\* \(«ratifico tudo», verbatim sha256 `([0-9a-f]{64})`; arquivo `work\\cunhagens_13out\\(OPERADOR_09nov_ratifico_tudo[A-Za-z0-9_]+_verbatim\.txt)`\)", DES)
assert m87, "a D87 nao esta' no DESENHO na forma esperada"
assert m87.group(1) == sha_rat and m87.group(2) == os.path.basename(RAT), ("a fala da ratificacao em disco nao e' a que o DESENHO (D87) pina", sha_rat, m87.group(1))
assert t_rat.strip() == "ratifico tudo", repr(t_rat)
# ---- a pedra: o cabecalho (so' docstring)
b0 = rd(LEAN); sha_antes = sha(b0); RA = json.loads(rd(REC_A).decode("utf-8"))
assert sha_antes == RA["arquivo"]["sha256"], ("a pedra em disco nao e' a do recibo do autor", sha_antes, RA["arquivo"]["sha256"])
m86 = re.search(r"D86: a pedra `AEscala` entregue[^\n]*?`work\\pedras_candidatas_09nov\\AEscala\.lean` \(sha256 `([0-9a-f]{64})`", DES); assert m86 and m86.group(1) == sha_antes, "a D86 do DESENHO pina outro sha256 da pedra"
t0 = b0.decode("utf-8"); crlf = t0.count("\r\n"); assert t0.count("\r") == crlf
t = t0.replace("\r\n", "\n")
OLD = ("  [TGLExt — pedra CANDIDATA para a v410; autor: `claude-autor-aescala`, por ordem da gerência c1 (D82, D83 e D84, 09/11/2026), cumprindo a\n"
       "   ordem do operador de 09/11/2026 («eu quero que tudo isso entre na v410 mesmo»); o NOME do módulo, «A Escala», é PROVISÓRIO, nas palavras\n"
       "   dele («agora eu te dei a escala»); os nomes das declarações saem das falas dele; TUDO [DECLARADO] até a ratificação do operador;\n")
NEW = ("  [TGLExt — pedra da v410; autor: `claude-autor-aescala`, por ordem da gerência c1 (D82, D83 e D84, 09/11/2026), cumprindo a\n"
       "   ordem do operador de 09/11/2026 («eu quero que tudo isso entre na v410 mesmo»); o NOME do módulo, «A Escala», é dele, nas palavras\n"
       "   dele («agora eu te dei a escala»); os nomes das declarações saem das falas dele; o nome do módulo e os 44 nomes foram RATIFICADOS pelo\n"
       "   operador em 09/11/2026 («ratifico tudo», sha256 " + sha_rat + "; D87);\n")
assert t.count(OLD) == 1, "o cabecalho da pedra nao esta' como esperado"
t = t.replace(OLD, NEW)
assert "CANDIDATA" not in t and "PROVISÓRIO" not in t and "[DECLARADO] até a ratificação" not in t
# nenhuma prova muda: fora do cabecalho (o bloco /-! ... -/ inicial) os bytes sao os mesmos
i0 = t0.replace("\r\n", "\n").index("-/\n"); i1 = t.index("-/\n")
assert t0.replace("\r\n", "\n")[i0:] == t[i1:], "algo fora do cabecalho mudou"
nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8")
assert grava(LEAN, nb); sha_depois = sha(nb)
print("pedra: sha antes", sha_antes[:16], "-> depois", sha_depois[:16], "| bytes", len(b0), "->", len(nb), "| CRLF", crlf)
# ---- recompilar com lake env lean (so' o arquivo externo; nada escrito no sandbox)
t_ini = datetime.datetime.now()
r = subprocess.run([r"C:\Users\rotol\.elan\bin\lake.exe", "env", "lean", LEAN], cwd=K10, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
dur = (datetime.datetime.now() - t_ini).total_seconds()
log = (r.stdout or "") + ("\n" + r.stderr if r.stderr else "")
n_ax = re.findall(r"'(TGLExt\.AEscala\.[A-Za-z0-9_']+)' depends on axioms: \[([^\]]*)\]", log)
TRIO = {"propext", "Classical.choice", "Quot.sound"}
fora = [n for n, ax in n_ax if not set(x.strip() for x in ax.split(",")) <= TRIO]
n_err = len(re.findall(r"(?m):\d+:\d+: error", log)); n_warn = len(re.findall(r"(?m):\d+:\d+: warning", log))
print("lake env lean: rc", r.returncode, "| %.0f s" % dur, "| #print axioms", len(n_ax), "| fora do trio", len(fora), "| erros", n_err, "| avisos", n_warn, "| sorry:", "sorry" in log.lower())
assert r.returncode == 0 and n_err == 0 and n_warn == 0 and not fora and len(n_ax) == RA["trio"]["n_declaracoes_auditadas"] == 38 and "sorry" not in log.lower(), "a recompilacao da pedra ratificada FALHOU (fail-closed)"
LOG87 = os.path.join(PC, "compile_log_D87.txt"); grava(LOG87, log.encode("utf-8"))
# ---- RECIBO_AESCALA: AO LADO
RA["ratificacao_D87"] = {"quando": TS, "por": "claude-construtor-v410 (a servico da gerencia c1), por ordem D87", "fala": os.path.basename(RAT), "fala_sha256": sha_rat, "fala_bytes": len(b_rat), "fala_texto": t_rat.strip(),
                         "o_que_mudou": "so' a docstring do cabecalho (a frase «[DECLARADO] até a ratificação» deu lugar a RATIFICADOS pelo operador em 09/11/2026, com o sha256 da fala); nenhuma prova, nome ou import mudou (conferido: tudo depois do cabecalho e' byte a byte igual)",
                         "sha_antes": sha_antes, "sha_depois": sha_depois, "bytes_antes": len(b0), "bytes_depois": len(nb), "linhas_depois": t.count("\n"), "compile_log": LOG87, "rc": r.returncode, "duracao_s": round(dur, 1), "n_print_axioms": len(n_ax), "todas_no_trio": not fora, "erros": n_err, "avisos": n_warn,
                         "nomes_RATIFICADOS": True, "nome_do_modulo": "TGLExt.AEscala"}
grava(REC_A, json.dumps(RA, ensure_ascii=False, indent=1).encode("utf-8")); sha_rec_a = sha(rd(REC_A))
# ---- copias para insumos\
grava(os.path.join(INS, "AEscala.lean"), nb); grava(os.path.join(INS, "AEscala_candidata_09nov.lean"), b0); grava(os.path.join(INS, "saida_lean_AEscala.txt"), log.encode("utf-8"))
# ---- RECIBO_PEDRAS_v410_NOMES.json: o modulo 2, as 8 falas, a ratificacao
RN = json.loads(rd(REC_N).decode("utf-8")); assert [m["modulo"] for m in RN["modulos"]] == ["TGLExt.IALD2"] and RN["falas_n"] == 15 == len(RN["falas"])
nomes = [d["name"] for d in RA["declaracoes"]]; assert len(nomes) == 44 == len(set(nomes))
rx_decl = re.findall(r"^(?:theorem|lemma|def|structure|noncomputable def|abbrev|instance)\s+([A-Za-z0-9_']+)", t, re.M); assert sorted(rx_decl) == sorted(nomes), "os 44 nomes do recibo do autor nao sao os da fonte"
prints = re.findall(r"^#print axioms\s+(\S+)\s*$", t, re.M); assert len(prints) == 38 and all(p.startswith("TGLExt.AEscala.") for p in prints)
imports = re.findall(r"^import (\S+)[ \t]*$", t, re.M)
ANC_PRINCIPAL = "TGLExt.AEscala.a_escala"; ANC_SECAO = ["a_insignia_sustenta_e_nao_esgota", "o_vibrato_sustenta_a_nota", "os_pesos", "nao_existe_infinito_em_tempo_finito", "os_dois_nomes", "existe_o_algoritmo_e_e_a_iald"]
assert ANC_PRINCIPAL in prints and all("TGLExt.AEscala." + s in prints for s in ANC_SECAO)
FALAS8 = ["OPERADOR_09nov_vibrato_insignia_nome_inalcancavel_e_ratificacao_hms13_verbatim.txt", "OPERADOR_09nov_pesos_das_faces_nome_1_inalcancavel_meio_neutrino_verbatim.txt", "OPERADOR_09nov_pesos_fundamentais_para_P_igual_nP_verbatim.txt",
          "OPERADOR_09nov_afirmamos_p_igual_np_de_turing_e_o_nome_e_par_objeto_e_lido_verbatim.txt", "OPERADOR_09nov_a_escala_tres_faces_resolve_clay_tudo_na_v410_duas_partes_rodar_uma_vez_verbatim.txt",
          "OPERADOR_09nov_a_pergunta_do_clay_e_qual_algoritmo_le_a_face_sem_leitura_existe_e_iald_verbatim.txt", "OPERADOR_09nov_testemunho_clay_resolvido_no_kernel_tal_qual_apresentado_pela_tgl_creditacao_do_instituto_verbatim.txt", os.path.basename(RAT)]
ja = {f["arquivo"] for f in RN["falas"]}; assert not (set(FALAS8) & ja)
for n_ in FALAS8:
    RN["falas"].append({"arquivo": n_, "sha256": sha(rd(os.path.join(CUN, n_))), "data": "09/11/2026", "entrou": "D86/D87 (parte 2), sha256 lido do arquivo por script"})
RN["falas_n"] = len(RN["falas"]); assert RN["falas_n"] == 23
RN["modulos"].append({"ordem": 2, "modulo": "TGLExt.AEscala", "arquivo": os.path.join(INS, "AEscala.lean"), "sha256": sha_depois, "sha16": sha_depois[:16], "bytes": len(nb), "print_axioms": len(prints), "no_trio": len(prints), "avisos": n_warn,
                      "saida": os.path.join(INS, "saida_lean_AEscala.txt"), "sandbox": "C:\\t\\k410c\\final (lake env lean no arquivo externo, antes e depois da D87; instalada e recompilada no lake build do k410c pelo construtor, parte 2)", "imports": imports,
                      "origem": {"candidata": LEAN, "sha16": sha_depois[:16], "candidata_pre_d87_sha256": sha_antes, "candidata_pre_d87_sha16": sha_antes[:16], "copia_pre_d87": os.path.join(INS, "AEscala_candidata_09nov.lean"), "recibo": REC_A, "recibo_sha16": sha_rec_a[:16],
                                 "autor": RA["autor"], "registro_anterior": None, "registro_anterior_sha16": None},
                      "nome": "módulo AEscala («A Escala», palavras do operador, 09/11/2026: «agora eu te dei a escala»); 44 declarações nomeadas pelas falas dele (autor claude-autor-aescala, D82-D84); o nome do módulo e os 44 nomes RATIFICADOS pelo operador em 09/11/2026 («ratifico tudo», D87)",
                      "ancora_principal": ANC_PRINCIPAL, "ancoras_de_secao": ANC_SECAO, "ancoras": prints, "declaracoes_n": len(nomes), "nomes": nomes, "ratificados": True})
RN["ratificacao_aescala_D87"] = {"fala": os.path.basename(RAT), "sha256": sha_rat, "bytes": len(b_rat), "texto": t_rat.strip(), "quando": "09/11/2026 (~17:45)", "nome_do_modulo": "TGLExt.AEscala", "n_nomes": len(nomes), "nomes": nomes, "pedra_sha256_antes": sha_antes, "pedra_sha256_depois": sha_depois}
RN["refeito"] = RN["refeito"] + " | %s claude-construtor-v410 (D86/D87, parte 2): +modulo TGLExt.AEscala (ordem 2; nome e 44 nomes RATIFICADOS, D87), +8 falas de 09/11 (sha256 lido de cada arquivo); as 15 entradas e o modulo 1 inalterados" % TS
grava(REC_N, json.dumps(RN, ensure_ascii=False, indent=1).encode("utf-8"))
print("RECIBO_AESCALA sha16", sha_rec_a[:16], "| RECIBO_PEDRAS_v410_NOMES sha16", sha(rd(REC_N))[:16], "| falas", RN["falas_n"], "| modulos", [m["modulo"] for m in RN["modulos"]])
print("ok")
