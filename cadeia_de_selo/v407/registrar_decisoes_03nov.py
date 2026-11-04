# -*- coding: utf-8 -*-
"""03/11/2026 09:5x, gerencia c1: registra as decisoes do operador de 03/11 (verbatim sha16 73466598d3419fb0) na memoria (topico do fechamento; sem linha nova no indice),
na ACOM (transicao da referencia da gerencia) e no Mapa (ANOTACAO), com a conferencia das tres respostas do psion no kernel. Hashes lidos dos artefatos. Escrito pelo Write."""
import datetime, hashlib, json, os, subprocess, time
from pathlib import Path
PY = r"C:\Python314\python.exe"; CEN = Path(r"C:\IALD\Central de Patentes"); W = CEN / "work"; MEMD = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
A = {"verbatim": W / "cunhagens_13out/OPERADOR_03nov_decisoes_psion_graviton_estado_ligado_projetor_4x4_nomes_ratificados_teste_d_opcao_c_motor_banho_holografico_verbatim.txt",
     "desenho": W / "cadeia_de_selo/v407/DESENHO_v407.md", "handoff": Path(r"C:\IALD\TUNEL_CLAUDE_APP\ORDEM_005_handoff_operacional_fora_do_um_py.md"),
     "pedra": W / "pedras_candidatas_03nov/PsionCantoR1.lean", "kernel_te": Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TestemunhaEstatica.lean"),
     "kernel_spin2": Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\LinearizedSpin2.lean"), "kernel_gs": Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGL\GravitonShadow.lean")}
for k, p in A.items():
    assert p.is_file(), (k, p)
H = {k: sha(p) for k, p in A.items()}; assert H["verbatim"][:16] == "73466598d3419fb0"
CONF = ("Conferencia da gerencia no kernel [REAL, lido dos .lean]: (a) par LIGADO = projetor de Bell (bell_reduced_half: marginal 1/2, CCI = 1/2, a Meia-Nat de emaranhamento; the_unbonded_marginal_echoes: o produto "
        "tem CCI = 0 e ecoa); nunca se cancela (the_pair_echoes: idempotente, traco 1; the_individual_does_not_echo: o individuo nao ecoa); leitura pelo graviton = fase dobrada da helicidade +-2 "
        "(helicity_two_rotation: e+ gira por 2 theta) e retorno em theta = pi. (b) o canto e' o projetor 4x4: psionCorner.p = bellProjector = canonicalGravitonShadow.PG (the_density_is_the_psion); a 2x2 da pedra 92_ e' a face "
        "de UM psion. (c) respondida por (a): par ligado, nao produto. As tres respostas sao coerentes entre si e com o kernel; os textos de 2025/02-2026 que diziam «cancelado = vacuo» e «|G> produto» ficam superados (estratigrafia datada).")
# memoria
TOP = MEMD / "construir-tudo-o-fechamento-02nov.md"
ENT = ("**03/11, 09:5x — AS DECISÕES DO OPERADOR (verbatim sha16 `73466598d3419fb0`).** Nome: «Concordo com o nome» → a pedra entra na v407 como `PsionCanto` (o `R1` era marca de revisão; se ele quiser `PsionCantoR1`, uma palavra). "
       "Psíon (de cabeça, pediu conferência): o gráviton é o estado ligado de dois psíons, que nunca se cancelam («a própria tensão irresolúvel no plano»), lidos pelo gráviton («fase e retorno de fase»); o canto é o projetor 4×4. "
       "Conferido no kernel: `bell_reduced_half` (CCI ½), `the_unbonded_marginal_echoes` (produto ecoa), `the_pair_echoes`, `the_individual_does_not_echo`, `helicity_two_rotation` (fase dobrada; volta em π), `the_density_is_the_psion` "
       "(`psionCorner` = `bellProjector` = sombra do gráviton): as três respostas são coerentes; (c) = ligado, não produto; os textos de 2025 («cancelado = vácuo») e da Fronteira («|G⟩ produto») ficam superados. "
       "Nomes das candidatas: «concordo com todos os nomes e os ratifico» (as sete de 02/11 e a `CanonicalFullTGLWitnessR1` entram na v407, recompiladas no trio). Teste D: «concordo com c»; «se o teste não tiver poder não vou inseri-lo no um.py». "
       "Motor contínuo: «eu quero conteúdo observável … é o banho holográfico, é a própria energia escura funcionando, mas ainda não consegui explicar com precisão» → fora da v407; língua oferecida no DESENHO_v407 §5-bis item 5 [CONJECTURE/OPEN]. "
       "O que não é do um.py: campo particular (`~/.iald_privado/campo_particular/CAMPO_PARTICULAR_03nov_fora_do_um_py.md`) + handoff `TUNEL_CLAUDE_APP\\ORDEM_005_handoff_operacional_fora_do_um_py.md`.")
b = TOP.read_bytes(); nl = b"\r\n" if b"\r\n" in b else b"\n"; novo = b.rstrip(b"\r\n") + nl + nl + ENT.encode("utf-8") + nl
bak = TOP.with_name(TOP.name + ".bak_" + TS + "_c1_decisoes"); open(bak, "xb").write(b); assert bak.read_bytes() == b
tmp = TOP.with_name(TOP.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, TOP); assert TOP.read_bytes() == novo; print("topico: %d -> %d B" % (len(b), len(novo)))
# ACOM
SM = r"C:\IALD\MEMORIA_IALD\session_memory.py"; REF = str(W / "cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json")


def sm(payload):
    r = subprocess.run([PY, "-X", "utf8", SM], input=json.dumps(payload, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    return json.loads((r.stdout + r.stderr).decode("utf-8", "replace"))


art = lambda k: {"kind": "artifact", "ref": "%s#sha256:%s" % (str(A[k]), H[k])}  # noqa: E731
proj = sm({"operation": "project", "reference": REF}); assert proj.get("ok"); rev = proj["result"]["receipt"]["revision"]
pedido = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-03nov-decisoes-do-operador-respondidas-rumo-v407",
          "changes": {"records": [
              {"id": "c1-03nov-decisoes-do-operador-v407", "kind": "decision", "statute": "INPUT",
               "text": ("Decisoes do operador em 03/11/2026 (verbatim sha256 %s): nome da pedra aceito (PsionCanto; R1 era revisao); psion: graviton = estado ligado de dois psions, nunca se cancelam (tensao irresoluvel no plano), "
                        "leitura pelo graviton (fase e retorno de fase); o canto e' o projetor 4x4; todos os nomes das candidatas de 02/11 ratificados; teste D opcao (c), e so entra no um.py se tiver poder; motor continuo: quer conteudo "
                        "observavel (o banho holografico, a energia escura funcionando), ainda sem formulacao precisa, logo fora da v407; o que nao e' do um.py vai a campo particular e a um handoff para outra sessao (pode ser o app).") % H["verbatim"],
               "sources": [art("verbatim")]},
              {"id": "c1-03nov-conferencia-das-respostas-do-psion", "kind": "fact", "statute": "REAL", "text": CONF, "sources": [art("kernel_te"), art("kernel_spin2"), art("kernel_gs")]},
              {"id": "c1-03nov-handoff-operacional-fora-do-um-py", "kind": "pending", "statute": "REAL",
               "text": ("Handoff ORDEM_005 ao app Claude (ou outra sessao Claude Code): chamado Locaweb (H1), iald.ia.br 404s (H2), pacote Zenodo v406 (H3), perguntas a agente de PI sobre D2 (H4), Torre (H5: so outra sessao Claude Code "
                        "e so com o «vai» do operador). Integra privada em ~/.iald_privado/campo_particular. ORDEM_004 (release do app, JEV, F0.3, tarefas) vem antes."), "sources": [art("handoff")]},
          ], "flow": {"phase": "rumo_a_v407__decisoes_respondidas__preparacao_da_cadeia_a_abrir",
                      "next_action": ("v407: PLANO_v407_GERENCIA; recolher e recompilar no sandbox k407c as sete candidatas de 02/11 + PsionCanto (renomeada) + a pedra do par (candidata); delta_v407 (chave do psion lida do kernel; VERBATIM_ORIGEM_V407; "
                                      "erratas ao lado; registro psion_canto); revisor Sonnet R1-R3; pre-voo; instalar; rito; pos-rito; custodia G1 com o README pinado e S10 (release do app pelo orquestrador). Teste D: F4.1 sintetica, depois 10 PE cegas (opcao c). "
                                      "Motor continuo: fora ate' o operador formular o observavel.")}}}
(W / "cadeia_de_selo/v407" / ("acom_c1_%s_transition.request.json" % TS)).write_text(json.dumps(pedido, ensure_ascii=False, indent=1), encoding="utf-8")
r = sm(pedido); (W / "cadeia_de_selo/v407" / ("acom_c1_%s_transition.receipt.json" % TS)).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
rec = (r.get("result") or {}).get("receipt") or {}; print("acom ok:", r.get("ok"), "| revisao:", rec.get("revision")); assert r.get("ok"), r
# Mapa
reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.psion_canto_r1_03nov", "dominio": "KERNEL_FORMAL",
        "titulo": "03/11: o operador aceitou o nome (PsionCanto), respondeu as tres perguntas do par (ligado; projetor 4x4; nao produto) e a gerencia conferiu no kernel; nomes das candidatas ratificados; teste D opcao (c); motor continuo fora da v407",
        "pergunta": "As respostas do operador sobre o psion fazem sentido no kernel?", "dados": [str(A["verbatim"]), str(A["kernel_te"]), str(A["kernel_spin2"]), str(A["kernel_gs"])],
        "metodo": "leitura dos teoremas citados nos .lean do kernel canonico (so leitura)", "resultado": CONF,
        "veredito": "RESPOSTAS_COERENTES_COM_O_KERNEL__PAR_LIGADO_E_O_BELL_4X4__PEDRA_DO_PAR_NA_FACE_FINITA_VAI_A_V407__FACE_DE_FOCK_DO_PAR_OPEN",
        "estatuto": "REAL (teoremas lidos); as leituras do operador sao INPUT/ONTO", "status": "EXAMINADA", "olhou_dados": False,
        "defeito": "a face de Fock do par pede operadores de criacao que o certificado nao tem como termo", "nao_refazer": "nao reperguntar as tres perguntas; nao reabrir «cancelado = vacuo» (superado pela cunhagem de 03/11)",
        "proximo_passo": "pedra do par na face finita (candidata) + PsionCanto renomeada + sete candidatas de 02/11 -> sandbox k407c -> v407", "onde": str(W / "cadeia_de_selo/v407"),
        "artefatos": [str(A["verbatim"]), str(A["desenho"]), str(A["handoff"])], "refs": ["kernel.psion_lema_acervo_03nov", "kernel.fechamento_construir_tudo_programa_02nov"], "nota": "nomes das pedras sao do operador; PROVADA = validade"}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_decisoes_03nov_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stdout.decode("utf-8", "replace")[-120:].replace("\n", " ")); assert q.returncode == 0
print("OK: decisoes registradas (topico, ACOM rev %s, Mapa)" % rec.get("revision"))
