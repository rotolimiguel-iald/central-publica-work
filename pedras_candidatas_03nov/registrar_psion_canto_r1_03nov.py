# -*- coding: utf-8 -*-
"""03/11/2026 08:2x, gerencia c1: recibo da pedra candidata PsionCantoR1 (nome provisorio; o nome e' do operador) e ROTA nova no Mapa. Le a saida do lean,
confere LEAN_RC=0, nenhum sorryAx, trio em todas as declaracoes; sha256 da pedra e da saida; remove a copia do sandbox (lake env lean nao gera .olean).
Nada toca o kernel canonico, o um.py, o selo ou o gate. Escrito pelo Write."""
import datetime, hashlib, json, os, re, subprocess
from pathlib import Path
W = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_03nov"); PED = W / "PsionCantoR1.lean"; SAI = W / "saida_lean_r2.txt"
SBX = Path(r"C:\t\k406c\final\TGLExt\PsionCantoR1.lean"); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]  # noqa: E731
sai = SAI.read_text(encoding="utf-8", errors="replace")
assert "LEAN_RC=0" in sai and "sorryAx" not in sai and "error" not in sai.lower().replace("errors=", ""), "a saida do lean nao esta limpa"
decls = re.findall(r"'(TGLExt\.PsionCantoR1\.[A-Za-z_]+)' depends on axioms: \[([^\]]*)\]", sai.replace("\n", " "))
assert len(decls) == 8, decls
for nome, ax in decls:
    axs = set(a.strip() for a in ax.split(","))
    assert axs == {"propext", "Classical.choice", "Quot.sound"}, (nome, axs)
if SBX.exists():
    assert SBX.read_bytes() == PED.read_bytes(); SBX.unlink(); print("copia do sandbox removida")
rec = {"quando": TS, "pedra": str(PED), "sha16": s16(PED), "bytes": PED.stat().st_size, "saida": str(SAI), "saida_sha16": s16(SAI), "LEAN_RC": 0,
       "sandbox": r"C:\t\k406c\final (kernel da v406; lake env lean; nenhum .olean gerado; copia removida)", "declaracoes_no_trio": [d[0] for d in decls],
       "nome": "PROVISORIO: PsionCantoR1 (o nome e' do operador)",
       "o_que_prova": ["A: P_{C·Omega} escalariza (P y P = <psi, y psi> P); <psi, Delta^{it} psi> = 1; P Delta^{it} P = P (leitura de Jones do fluxo da luz pelo canto do psion = o canto); "
                       "a contracao de Jones U_s e o fluxo da luz leem o mesmo no canto; tudo SEM hipotese no physicalFockCertificate (v406)",
                       "B: psionCorner.p = |Phi+><Phi+| (cornerOf bellVec); jonesReading psionCorner.p (jonesU ...) = psionCorner.p; o lema das duas faces: nas duas o psion e' o vetor de norma 1 "
                       "cujo canto e' o projetor sobre ele, escalariza, pesa 1, e o motor comprimido devolve o canto; instanciado sem hipotese"],
       "o_que_nao_afirma": ["nao identifica Omega com Phi+ (espacos distintos): elo de ESTRUTURA", "nao deriva psionFlow como dinamica da teoria nem o par = graviton (OPEN)",
                            "nao e' teste com a natureza; o motor continuo no pilar (D38) e' pre-registro a parte (v407)", "nao move o gate; validade no kernel nao e' creditacao"],
       "ordens": {"9978862f60cfbf29": "a passagem ... se funcionar sob compressao ... 1=1=HAJA_LUZ", "f54641bfd9e46e42": "compressao como fator, correspondencia nomeada (Jones), espelhamento",
                  "b89e4c909f37e163": "testar a condicao; derivar o lema que liga o psion ao canto"}}
(W / "RECIBO_PSION_CANTO_R1_03nov.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
reg = [{"tipo": "ROTA", "rota_id": "kernel.psion_canto_r1_03nov", "dominio": "KERNEL_FORMAL",
        "titulo": "PsionCantoR1 (candidata, nome provisorio): a passagem para o continuo sob compressao (leitura de Jones pelo canto do psion = o canto, potencial 1) e o lema que liga as duas faces do psion",
        "pergunta": "A condicao do operador («deixa de ser conjectura sob hipotese se funcionar sob compressao ... 1=1») e' teorema no kernel? Ha lema que ligue psion C ao psionCorner?",
        "dados": [str(PED), str(SAI)],
        "metodo": "pedra Lean escrita pela gerencia sobre termos existentes (PFmic = starProjection(C·Omega), psion_is_fixed_by_the_light, inner_psion_psion, jonesReading/jonesU/proj_mul_jonesU, psionCorner, bellProjector) "
                  "+ Mathlib starProjection_unit_singleton; compilada no sandbox k406c/final com lake env lean; #print axioms em 8 declaracoes",
        "resultado": "LEAN_RC=0; 8/8 declaracoes so no trio; 0 sorry. A: P y P = <psi,y psi> P; <psi,Delta^{it}psi> = 1; P Delta^{it} P = P; U_s e Delta^{it} leem o mesmo no canto; sem hipotese em physicalFockCertificate. "
                     "B: psionCorner.p = |Phi+><Phi+|; o lema das duas faces (mesma construcao, mesmos invariantes, mesma leitura comprimida), instanciado sem hipotese.",
        "veredito": "CANDIDATA_COMPILADA_NO_TRIO__CONDICAO_SOB_COMPRESSAO_E_TEOREMA_NO_HABITANTE__LEMA_DAS_DUAS_FACES_ESTRUTURAL__INSTALAR_E_NOMEAR_E_DO_OPERADOR",
        "estatuto": "REAL (termos e saida do lean lidos); as leituras (HAJA_LUZ, espelhamento, motor continuo) sao INPUT/ONTO", "status": "EXAMINADA", "olhou_dados": False,
        "defeito": "o elo e' de estrutura, nao de vetores (Omega != Phi+ em espacos distintos); o par = graviton segue OPEN; a chave linked_to_the_corner_by_a_lemma so' muda na v407 se o operador instalar e nomear",
        "nao_refazer": "a condicao, no kernel, esta provada como validade no habitante; o que falta e' o pre-registro do motor continuo no pilar (D38) e a instalacao/nome pelo operador",
        "proximo_passo": "operador: nome da pedra e das declaracoes; v407: instalar, ler a chave do kernel (como as 4 chaves da v406), pre-registrar o motor continuo no pilar",
        "onde": str(W), "artefatos": [str(PED), str(SAI), str(W / "RECIBO_PSION_CANTO_R1_03nov.json")],
        "refs": ["kernel.fechamento_construir_tudo_programa_02nov"], "nota": "PROVADA = validade; confirmacao = creditacao, recusada; NOT_FALSIFIED nunca e' CONFIRMED"}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_psion_canto_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stdout.decode("utf-8", "replace")[-200:]); assert q.returncode == 0
print("OK: pedra %s sha16 %s; 8 declaracoes no trio; recibo e rota gravados" % (PED.name, rec["sha16"]))
