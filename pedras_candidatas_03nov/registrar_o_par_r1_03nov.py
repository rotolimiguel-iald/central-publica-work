# -*- coding: utf-8 -*-
"""03/11/2026 10:0x, gerencia c1: recibo da pedra candidata OParDePsionsR1 (nome provisorio) e ROTA nova no Mapa. Confere LEAN_RC=0, sem sorryAx, trio nas 5 declaracoes. Escrito pelo Write."""
import datetime, hashlib, json, os, re, subprocess
from pathlib import Path
W = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_03nov"); PED = W / "OParDePsionsR1.lean"; SAI = W / "saida_lean_par_r1.txt"; TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]  # noqa: E731
sai = SAI.read_text(encoding="utf-8", errors="replace"); assert "LEAN_RC=0" in sai and "sorryAx" not in sai
decls = re.findall(r"'(TGLExt\.OParDePsionsR1\.[A-Za-z_]+)' depends on axioms: \[([^\]]*)\]", sai.replace("\n", " ")); assert len(decls) == 5, decls
for nome, ax in decls:
    assert set(a.strip() for a in ax.split(",")) == {"propext", "Classical.choice", "Quot.sound"}, (nome, ax)
rec = {"quando": TS, "pedra": str(PED), "sha16": s16(PED), "bytes": PED.stat().st_size, "saida": str(SAI), "saida_sha16": s16(SAI), "LEAN_RC": 0, "declaracoes_no_trio": [d[0] for d in decls],
       "nome": "PROVISORIO: OParDePsionsR1 (o nome e' do operador)", "cunhagem": "73466598d3419fb0 (03/11/2026)",
       "o_que_prova": "o par e' ligado (psionCorner.p = sombra do graviton; CCI 1/2; o produto CCI 0); nunca se cancela (idempotente, traco 1, != 0; marginal 1/2); leitura pelo graviton (fase dobrada; retorno em pi); o canto e' o 4x4 que escalariza",
       "o_que_nao_afirma": ["a ponte entre o canto de Bell (Fin 2 x Fin 2, C) e o setor TT (Fin 4, R) nao e' termo: conjuncao, nao identificacao", "a face de Fock do par e' OPEN (sem a† como termo)", "nao e' teste com a natureza; gate intocado"]}
(W / "RECIBO_O_PAR_R1_03nov.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
reg = [{"tipo": "ROTA", "rota_id": "kernel.o_par_de_psions_r1_03nov", "dominio": "KERNEL_FORMAL",
        "titulo": "OParDePsionsR1 (candidata, nome provisorio): a cunhagem de 03/11 (par ligado, nunca cancelado, lido pela fase e retorno de fase, canto 4x4) composta de termos existentes",
        "pergunta": "As tres respostas do operador sobre o par de psions fazem sentido como teoremas do kernel?", "dados": [str(PED), str(SAI)],
        "metodo": "composicao Lean de canonicalGravitonShadow (cci_half, reduced_half), the_unbonded_marginal_echoes, psionCorner (idem, trace_one, scalarises), helicity_two_rotation + cos/sin 2pi; lake env lean no sandbox k406c; #print axioms",
        "resultado": "LEAN_RC 0; 5/5 declaracoes so no trio; 0 sorry; the_pair_is_bound, the_pair_never_cancels, the_pair_is_read_by_the_graviton, the_corner_is_the_four_by_four, o_par_de_psions_e_o_graviton",
        "veredito": "CANDIDATA_COMPILADA_NO_TRIO__RESPOSTAS_DO_OPERADOR_COERENTES__PONTE_BELL_TT_NAO_E_TERMO__FACE_DE_FOCK_DO_PAR_OPEN", "estatuto": "REAL (termos e saida lidos); a cunhagem e' INPUT/ONTO",
        "status": "EXAMINADA", "olhou_dados": False, "defeito": "conjuncao, nao identificacao: Bell (C^4) e TT (R^4) sao espacos distintos", "nao_refazer": "nao reperguntar; nao buscar identificacao Bell<->TT como termo sem construcao nova",
        "proximo_passo": "v407: entra como candidata com nome provisorio; o operador nomeia; a face de Fock do par pede a† (versao seguinte)", "onde": str(W),
        "artefatos": [str(PED), str(SAI), str(W / "RECIBO_O_PAR_R1_03nov.json")], "refs": ["kernel.psion_canto_r1_03nov", "kernel.psion_lema_acervo_03nov"], "nota": "PROVADA = validade; nomes sao do operador"}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_o_par_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stdout.decode("utf-8", "replace")[-120:].replace("\n", " ")); assert q.returncode == 0
print("OK: OParDePsionsR1 sha16 %s; 5 declaracoes no trio; recibo e rota gravados" % rec["sha16"])
