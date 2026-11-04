# -*- coding: utf-8 -*-
"""03/11/2026 15:2x, gerencia c1 (R2): (1) recibos R2 da PsionCanto e do Par (fontes corrigidas, recompiladas no sandbox da v406: saida_lean_r3.txt e saida_lean_par_r2.txt; LEAN_RC 0, trio);
(2) delta_v407.py ganha os caminhos dos recibos/saidas R2; registros_v407.py ganha as chaves, as ORIGENS e as FONTES R2, e os papeis das fontes R1 passam a dizer a verdade (a fonte atual e' a R2;
a R1 esta' em pedra/antes_de_*_r2/origem e nos .bak); (3) as copias antigas em insumos/ das 5 pedras corrigidas e das 2 origens saem para insumos/antes_de_<ts>_r2/ (copiar_insumos aborta em divergencia);
(4) ANOTACAO no Mapa nas rotas das duas pedras. Backups de bytes; py_compile. Escrito pelo Write."""
import datetime, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes"); W = CEN / "work"; V7 = W / "cadeia_de_selo" / "v407"; P3 = W / "pedras_candidatas_03nov"; TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sys.path.insert(0, str(CEN / "tools")); from custodia_g1 import patches  # noqa: E402,E401
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]  # noqa: E731


def recibo(nome_ped, fonte, saida, ns, n_esp, saida_r1, recibo_r1, nota):
    sai = Path(saida).read_text(encoding="utf-8", errors="replace"); assert "LEAN_RC=0" in sai and "sorryAx" not in sai and " error" not in sai.lower()
    decls = re.findall(r"'(%s\.[A-Za-z_]+)' depends on axioms: \[([^\]]*)\]" % re.escape(ns), sai.replace("\n", " ")); assert len(decls) == n_esp, (len(decls), n_esp)
    for n_, ax in decls:
        assert set(a.strip() for a in ax.split(",")) == {"propext", "Classical.choice", "Quot.sound"}, (n_, ax)
    rec = {"quando": TS, "rodada": "R2 (correcoes de docstring da gerencia c1 sobre os BAIXOS da revisao de terceiro R1 da v407; nenhuma prova tocada)", "pedra": str(fonte), "sha16": s16(fonte), "bytes": Path(fonte).stat().st_size,
           "saida": str(saida), "saida_sha16": s16(saida), "LEAN_RC": 0, "sandbox": r"C:\t\k406c\final (kernel da v406; lake env lean; copia removida)", "declaracoes_no_trio": [d[0] for d in decls],
           "r1": {"recibo": str(recibo_r1), "recibo_sha16": s16(recibo_r1), "saida": str(saida_r1), "saida_sha16": s16(saida_r1), "sha16_da_fonte_r1": json.loads(Path(recibo_r1).read_text(encoding="utf-8"))["sha16"]},
           "nome_no_kernel_v407": nome_ped, "nota": nota}
    return rec


r_psi = recibo("TGLExt.PsionCanto", P3 / "PsionCantoR1.lean", P3 / "saida_lean_r3.txt", "TGLExt.PsionCantoR1", 8, P3 / "saida_lean_r2.txt", P3 / "RECIBO_PSION_CANTO_R1_03nov.json",
               "R2: citacao exata «virar essa chave de conjectura para provado»; escopo do lema dito (vale para qualquer vetor unitario fixo; nao relaciona as faces por aplicacao); «nome provisorio» fora do docstring do teorema")
r_par = recibo("TGLExt.Par", P3 / "OParDePsionsR1.lean", P3 / "saida_lean_par_r2.txt", "TGLExt.OParDePsionsR1", 5, P3 / "saida_lean_par_r1.txt", P3 / "RECIBO_O_PAR_R1_03nov.json",
               "R2: «em theta = pi a polarizacao e+ do setor TT volta a si» (nao «o par»); [KNOWN/ONTO] -> [ONTO]; «nome provisorio» -> «conjuncao, nao identificacao»; o nome Par e' do operador (57250bbbaca9fd39)")
(P3 / "RECIBO_PSION_CANTO_R2_03nov.json").write_text(json.dumps(r_psi, ensure_ascii=False, indent=1), encoding="utf-8")
(P3 / "RECIBO_O_PAR_R2_03nov.json").write_text(json.dumps(r_par, ensure_ascii=False, indent=1), encoding="utf-8")
print("recibos R2:", r_psi["sha16"], r_par["sha16"])
# ---------------------------------------------------------------- delta: caminhos R2
O_D = 'SAIDA_PAR_ARQ = os.path.join(P3, "saida_lean_par_r1.txt")\n'
N_D = (O_D + 'RECIBO_PSION_R2_ARQ = os.path.join(P3, "RECIBO_PSION_CANTO_R2_03nov.json")   # R2 da gerencia (03/11, 15h): a fonte corrigida, recompilada no sandbox da v406\n'
       'RECIBO_PAR_R2_ARQ = os.path.join(P3, "RECIBO_O_PAR_R2_03nov.json")\n'
       'SAIDA_PSION_R2_ARQ = os.path.join(P3, "saida_lean_r3.txt")\n'
       'SAIDA_PAR_R2_ARQ = os.path.join(P3, "saida_lean_par_r2.txt")\n')


def f_delta(s):
    assert s.count(O_D) == 1 and "RECIBO_PSION_R2_ARQ" not in s
    return s.replace(O_D, N_D), ["1 caminhos dos recibos/saidas R2"]


print(json.dumps(patches.aplicar_em_arquivo(V7 / "delta_v407.py", f_delta, "r2_recibos"), ensure_ascii=False)[:160])
# ---------------------------------------------------------------- registros: chaves, ORIGENS, FONTES, lista de fontes do registro
O_K = 'CHAVE_SAIDA_PAR = "saida_lean_par_r1_03nov"\n'
N_K = (O_K + 'CHAVE_RECIBO_PSION_R2 = "recibo_psion_canto_r2_03nov"      # R2 da gerencia (03/11): a fonte corrigida recompilada no sandbox da v406\n'
       'CHAVE_RECIBO_PAR_R2 = "recibo_o_par_r2_03nov"\nCHAVE_SAIDA_PSION_R2 = "saida_lean_psion_canto_r2_03nov"\nCHAVE_SAIDA_PAR_R2 = "saida_lean_par_r2_03nov"\n')
O_O = '("saida_lean_r2.txt", DL.SAIDA_PSION_ARQ), ("saida_lean_par_r1.txt", DL.SAIDA_PAR_ARQ),'
N_O = (O_O + '\n              ("RECIBO_PSION_CANTO_R2_03nov.json", DL.RECIBO_PSION_R2_ARQ), ("RECIBO_O_PAR_R2_03nov.json", DL.RECIBO_PAR_R2_ARQ), ("saida_lean_r3.txt", DL.SAIDA_PSION_R2_ARQ), ("saida_lean_par_r2.txt", DL.SAIDA_PAR_R2_ARQ),')
O_P1 = '"papel": "a fonte de origem da PsionCanto, como foi compilada em 03/11/2026 no sandbox da v406 (PsionCantoR1.lean, sha16 ae74b8334c3c0c8e; o R1 era marca de revisao)'
N_P1 = '"papel": "a fonte de origem da PsionCanto (PsionCantoR1.lean; o R1 do nome do arquivo e\' marca de revisao da candidata): a versao R2, com as correcoes de docstring da gerencia c1 de 03/11/2026 sobre a revisao de terceiro (nenhuma prova tocada; sha16 %s), recompilada no sandbox da v406 (saida_lean_r3.txt) e embutida no kernel da v407 como TGLExt.PsionCanto; a R1 (sha16 ae74b8334c3c0c8e) fica como registro em pedra\\\\antes_de_*_r2\\\\origem' % r_psi["sha16"]
O_P2 = '"papel": "a fonte de origem da pedra Par, como foi compilada em 03/11/2026 no sandbox da v406 (OParDePsionsR1.lean, nome provisorio que o operador substituiu por «Par»'
N_P2 = '"papel": "a fonte de origem da pedra Par (OParDePsionsR1.lean, o nome provisorio que o operador substituiu por «Par»): a versao R2, com as correcoes de docstring da gerencia c1 de 03/11/2026 (nenhuma prova tocada; sha16 %s), recompilada no sandbox da v406 (saida_lean_par_r2.txt) e embutida no kernel da v407 como TGLExt.Par; a R1 (sha16 444763c0dc8c4bbc) fica como registro' % r_par["sha16"]
O_F = '    {"chave": CHAVE_SAIDA_PAR, "arquivo": os.path.join(INS, "saida_lean_par_r1.txt"), "papel": "a saida do lean ao compilar a pedra do par (03/11/2026) [REAL: saida do lean]"},\n'
N_F = (O_F +
       '    {"chave": CHAVE_RECIBO_PSION_R2, "arquivo": os.path.join(INS, "RECIBO_PSION_CANTO_R2_03nov.json"), "papel": "o recibo R2 da PsionCanto: a fonte corrigida pela gerencia (03/11/2026, docstring; nenhuma prova tocada) recompilada no sandbox da v406 (LEAN_RC 0; 8 declaracoes no trio); e\' a fonte que entra no kernel da v407 [REAL: saida do lean lida]"},\n'
       '    {"chave": CHAVE_RECIBO_PAR_R2, "arquivo": os.path.join(INS, "RECIBO_O_PAR_R2_03nov.json"), "papel": "o recibo R2 da pedra Par: a fonte corrigida pela gerencia (03/11/2026) recompilada no sandbox da v406 (LEAN_RC 0; 5 declaracoes no trio); e\' a fonte que entra no kernel da v407 [REAL: saida do lean lida]"},\n'
       '    {"chave": CHAVE_SAIDA_PSION_R2, "arquivo": os.path.join(INS, "saida_lean_r3.txt"), "papel": "a saida do lean ao recompilar a PsionCanto corrigida (R2, 03/11/2026) [REAL: saida do lean]"},\n'
       '    {"chave": CHAVE_SAIDA_PAR_R2, "arquivo": os.path.join(INS, "saida_lean_par_r2.txt"), "papel": "a saida do lean ao recompilar a pedra Par corrigida (R2, 03/11/2026) [REAL: saida do lean]"},\n')
O_L = '[CHAVE_CANDIDATA_PSION_R1, CHAVE_CANDIDATA_PAR_R1, CHAVE_RECIBO_PSION, CHAVE_RECIBO_PAR, CHAVE_SAIDA_PSION, CHAVE_SAIDA_PAR'
N_L = O_L + ', CHAVE_RECIBO_PSION_R2, CHAVE_RECIBO_PAR_R2, CHAVE_SAIDA_PSION_R2, CHAVE_SAIDA_PAR_R2'


def f_reg(s):
    for o in (O_K, O_O, O_P1, O_P2, O_F, O_L):
        assert s.count(o) == 1, ("registros: trecho nao esta' UMA vez (%d): %s" % (s.count(o), o[:80]))
    assert "CHAVE_RECIBO_PSION_R2" not in s
    for o, n in ((O_K, N_K), (O_O, N_O), (O_P1, N_P1), (O_P2, N_P2), (O_F, N_F), (O_L, N_L)):
        s = s.replace(o, n)
    return s, ["chaves R2", "ORIGENS R2", "papel PsionCantoR1 (R2)", "papel OParDePsionsR1 (R2)", "FONTES R2", "lista de fontes do registro"]


print(json.dumps(patches.aplicar_em_arquivo(V7 / "registros_v407.py", f_reg, "r2_fontes"), ensure_ascii=False)[:200])
# ---------------------------------------------------------------- insumos antigos saem do caminho
ANT = V7 / "insumos" / ("antes_de_%s_r2" % TS); ANT.mkdir(parents=True, exist_ok=True)
for n in ("PsionCanto.lean", "Par.lean", "OUmInscrito.lean", "OIgual.lean", "APonteDoAtrito.lean", "PsionCantoR1.lean", "OParDePsionsR1.lean", "MANIFESTO_INSUMOS_v407.json"):
    p = V7 / "insumos" / n
    if p.exists():
        shutil.move(str(p), str(ANT / n)); print("insumo antigo movido:", n)
if (V7 / "MANIFESTO_INSUMOS_v407.json").exists():
    shutil.copy2(V7 / "MANIFESTO_INSUMOS_v407.json", ANT / "MANIFESTO_INSUMOS_v407.json.raiz"); print("MANIFESTO_INSUMOS (raiz) copiado para antes_de (o copiar_insumos regrava)")
# ---------------------------------------------------------------- Mapa
reg = [{"tipo": "ANOTACAO", "rota_id": rid, "dominio": "KERNEL_FORMAL", "titulo": "R2 da gerencia (03/11, 15h): docstring corrigida sobre a revisao de terceiro R1 da v407; recompilada no sandbox da v406; nenhuma prova tocada; e' a fonte que entra na v407",
        "pergunta": "A fonte corrigida compila igual?", "dados": [str(sai)], "metodo": "lake env lean no k406c/final", "resultado": "LEAN_RC 0; %d declaracoes no trio; sha16 da fonte %s (R1: %s)" % (n_, rr["sha16"], rr["r1"]["sha16_da_fonte_r1"]),
        "veredito": "R2_COMPILADA_NO_TRIO__SO_DOCSTRING_MUDOU", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False, "defeito": "", "nao_refazer": "a R1 fica como registro; a R2 e' a vigente",
        "proximo_passo": "kernel k407c (build incremental) -> candidato -> R2 do revisor", "onde": str(P3), "artefatos": [str(sai), str(rec_p)], "refs": [], "nota": "nomes do operador: PsionCanto, Par"}
       for rid, sai, n_, rr, rec_p in (("kernel.psion_canto_r1_03nov", P3 / "saida_lean_r3.txt", 8, r_psi, P3 / "RECIBO_PSION_CANTO_R2_03nov.json"), ("kernel.o_par_de_psions_r1_03nov", P3 / "saida_lean_par_r2.txt", 5, r_par, P3 / "RECIBO_O_PAR_R2_03nov.json"))]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_r2_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300); assert q.returncode == 0
print("OK: recibos R2, delta e registros atualizados, insumos antigos movidos, Mapa anotado")
