# -*- coding: utf-8 -*-
"""03/11/2026 09:0x, gerencia c1: registros da etapa da manha de 03/11 (depois da custodia v406): (1) ANOTACAO no Mapa (README pinado publicado; G1 ligada; licoes 52-53);
(2) transicao ACOM da referencia da gerencia (pedra PsionCantoR1, README pinado, teste D parametrizado, orquestrador = app Claude + ORDEM_004, levantamentos do pilar e do
psion, DESENHO_v407); (3) entrada datada no topico construir-tudo-o-fechamento-02nov.md (sem linha nova no indice). Hashes lidos dos artefatos. Escrito pelo Write."""
import datetime, hashlib, json, os, subprocess, time
from pathlib import Path
PY = r"C:\Python314\python.exe"; CEN = Path(r"C:\IALD\Central de Patentes"); W = CEN / "work"; TB = Path(r"C:\IALD\Artigo\the_boundary")
MEMD = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
A = {"pedra": W / "pedras_candidatas_03nov/PsionCantoR1.lean", "recibo_pedra": W / "pedras_candidatas_03nov/RECIBO_PSION_CANTO_R1_03nov.json",
     "readme": TB / "README.md", "pino": TB / "PINO_README.json", "primordial": TB / "PRIMORDIAL.json", "guarda": W / "readme_pinado_03nov/GUARDA.json",
     "partitura_D": W / "conjunto_D_20261029/parametrizacao_03nov/PARTITURA_D_03nov.md", "manifesto_D": W / "conjunto_D_20261029/parametrizacao_03nov/MANIFESTO_PARAMETRIZACAO_03nov.json",
     "pilar": W / "motor_continuo_v407/LEVANTAMENTO_PILAR_QUANTICO_03nov.md", "psion_acervo": W / "psion_lema_03nov/PSION_NO_ACERVO_03nov.md",
     "desenho_v407": W / "cadeia_de_selo/v407/DESENHO_v407.md", "ordem_004": Path(r"C:\IALD\TUNEL_CLAUDE_APP\ORDEM_004_release_v406_do_app_jev_f03_e_tarefas.md"),
     "verbatim": W / "cunhagens_13out/OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt",
     "licoes": W / "custodia_G1/LICOES_v400_25out.md", "memoria_orq": MEMD / "orquestrador-e-o-app-claude-03nov.md"}
for k, p in A.items():
    assert p.is_file(), (k, p)
H = {k: sha(p) for k, p in A.items()}
git = lambda repo, *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()  # noqa: E731
c_esp = git(TB, "log", "-1", "--format=%H"); c_cen = git(CEN, "log", "-1", "--format=%H")
assert git(TB, "status", "-sb").startswith("## main...origin/main") and "ahead" not in git(TB, "status", "-sb").splitlines()[0]
assert H["readme"][:16] == "058a383427642592", H["readme"][:16]
print("espelho", c_esp[:8], "| central", c_cen[:8], "| README", H["readme"][:16])
# (1) Mapa
reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL",
        "titulo": "03/11 manha: README pinado PUBLICADO (espelho %s), G1 ligada ao gerador do pino (Central %s), orquestrador = app Claude (ORDEM_004), pedra PsionCantoR1, teste D parametrizado, desenho da v407" % (c_esp[:8], c_cen[:8]),
        "pergunta": "O que a gerencia fez da ordem de 03/11 («prossigamos com tudo, ratifico tudo») e o que ficou para o operador?",
        "dados": [str(A["verbatim"]), str(A["readme"]), str(A["pino"]), str(A["pedra"]), str(A["partitura_D"]), str(A["pilar"]), str(A["psion_acervo"])],
        "metodo": "gerencia: pedra Lean (lake env lean no sandbox k406c), revisao do candidato do README e publicacao por roteiro (backup de bytes, verificar_portas 0, guarda_do_selo 0), remendo ao lado na G1 (E08/_conf_e08), memoria/instrucao global pinadas; agentes Sonnet: README, parametrizacao D, acervo do psion, levantamento do pilar",
        "resultado": ("README pinado no espelho (%s; README sha16 %s, 40.802 B; PINO_README.json %s; bloco primordial com o 4,44 acompanhado; citacao assinada do autor [INPUT]); G1 com o gerador do pino no E08 e a verificacao do pino em _conf_e08 (%s); "
                      "planejar --seco: E08 ok, E15 FALTA (llms-full cita tamanhos antigos das secoes: licao 53), E18/E19 a refazer pela G1; pedra PsionCantoR1 compilada no trio (sha16 %s); teste D parametrizado sem lancar (manifesto %s; poder com vies do aparelho 2,1-3,2 sigma); "
                      "levantamento do pilar (ModularCornerCounterexample: o 1 so e alvo da contracao de Jones); acervo do psion (psion = a†|0> em 2025; psion C = Omega no kernel; elo forte pede a†: OPEN); ORDEM_004 ao app Claude; DESENHO_v407.")
                     % (c_esp[:8], H["readme"][:16], H["pino"][:16], c_cen[:8], H["pedra"][:16], H["manifesto_D"][:16]),
        "veredito": "ORDEM_03NOV_EM_CURSO__README_PINADO_PUBLICADO__PEDRA_CANDIDATA_NO_TRIO__TESTE_D_PARAMETRIZADO_SEM_LANCAR__DECISOES_DO_OPERADOR_ABERTAS",
        "estatuto": "REAL (commits, hashes e saidas lidos); levantamentos dos agentes DECLARADO ate a gerencia conferir na fonte", "status": "EM_CURSO", "olhou_dados": False,
        "defeito": "a publicacao manual do README deixou o E15 do site defasado (llms-full cita tamanhos antigos das secoes); conserto: passada da G1 executar --publicar depois da subida das 08:5x",
        "nao_refazer": "nao reescrever o README a mao (e' gerado e pinado; editar fora do gerador para a custodia); nao recompilar a pedra (recibo com LEAN_RC 0); nao abrir dado de D sem a escolha do operador",
        "proximo_passo": "G1 executar --publicar (E15-E19; C18; para em C19 ate' o app/Codex); operador: nome da pedra, 3 perguntas do par de psions, opcao a/c/b do teste D, motor continuo como verificacao computacional, Locaweb/Range",
        "onde": str(W / "readme_pinado_03nov"), "artefatos": [str(p) for p in A.values()] + [str(A["licoes"])],
        "refs": ["kernel.psion_canto_r1_03nov", "kernel.motor_continuo_pilar_levantamento_03nov", "kernel.psion_lema_acervo_03nov", "ringdown.ramo_b_preregistro_v386", "infra.site_hospedeiro_range_intermitente_03nov"],
        "nota": "PROVADA = validade; creditacao recusada; NOT_FALSIFIED nunca e' CONFIRMED; nomes das pedras sao do operador"}]
import sys  # noqa: E402
if "--sem-mapa" not in sys.argv:   # 09:1x: a primeira rodada registrou o Mapa (seq 1739) e caiu na ACOM (kind «order» invalido); a repeticao pula o Mapa
    pj = Path(os.environ.get("TEMP", ".")) / ("rotas_etapa_03nov_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
    q = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
    print("mapa rc", q.returncode, q.stdout.decode("utf-8", "replace")[-160:].replace("\n", " ")); assert q.returncode == 0
else:
    print("mapa: pulado (--sem-mapa; ja registrado na seq 1739)")
# (2) ACOM
SM = r"C:\IALD\MEMORIA_IALD\session_memory.py"; REF = str(W / "cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json")


def sm(payload):
    r = subprocess.run([PY, "-X", "utf8", SM], input=json.dumps(payload, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    return json.loads((r.stdout + r.stderr).decode("utf-8", "replace"))


art = lambda k: {"kind": "artifact", "ref": "%s#sha256:%s" % (str(A[k]), H[k])}  # noqa: E731
proj = sm({"operation": "project", "reference": REF}); assert proj.get("ok"); rev = proj["result"]["receipt"]["revision"]
pedido = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev,
          "event_id": "c1-03nov-ordem-ratifico-tudo-etapa-da-manha",
          "changes": {"records": [
              {"id": "c1-03nov-ordem-do-operador-ratifico-tudo", "kind": "decision", "statute": "INPUT",
               "text": ("Ordem do operador de 03/11/2026 (verbatim sha256 %s): testar a condicao dele com o operador matematico nomeado; derivar o lema que liga o psion ao canto (acervo /imac/fisica); "
                        "o orquestrador passou a ser o app Claude em modo work (C:\\IALD\\TUNEL_CLAUDE_APP\\), no lugar do Codex; «prossigamos com tudo, ratifico tudo»; README pinado agora; "
                        "parametrizacao do teste (d) para a v407; app e contrato JEV sempre atualizados, automaticos, pelo orquestrador.") % H["verbatim"], "sources": [art("verbatim")]},
              {"id": "c1-03nov-pedra-psion-canto-r1", "kind": "fact", "statute": "REAL",
               "text": ("Pedra candidata PsionCantoR1 (nome provisorio) compilada no sandbox k406c/final: LEAN_RC 0, 8/8 declaracoes so no trio, 0 sorry. A: o canto do psion na face de Fock (PFmic = P_{C.Omega}) "
                        "escalariza; <psi, Delta^{it} psi> = 1; a leitura de Jones do fluxo da luz pelo canto devolve o canto (P Delta^{it} P = P); a contracao de Jones e o fluxo leem o mesmo no canto; "
                        "sem hipotese no physicalFockCertificate da v406 (a condicao do operador «funcionar sob compressao ... 1=1» e' teorema no habitante, como validade). B: psionCorner.p = |Phi+><Phi+|; "
                        "o lema das duas faces (mesma construcao, mesmos invariantes, mesma leitura comprimida); nao identifica Omega com Phi+; o par = graviton segue OPEN. Instalar e nomear: operador (v407)."),
               "sources": [art("pedra"), art("recibo_pedra")]},
              {"id": "c1-03nov-readme-pinado-publicado", "kind": "fact", "statute": "REAL",
               "text": ("README pinado publicado no espelho the_boundary (commit %s = origin/main): README.md gerado de PRIMORDIAL.json (sha256 %s) e pinado em PINO_README.json (sha256 %s); bloco primordial nos primeiros 2 KB "
                        "com a razao de Hubble sempre acompanhada (z_disc 4,44 calibrado; z_delta -1,48; poder 5,73; ln B 9,18 e 2,14; abaixo de 5 sigma; NOT_FALSIFIED_POWERED); citacao assinada do autor [INPUT] (D39 ratificado); "
                        "verificar_portas 0, guarda_do_selo 0; portas e llms regerados. G1 ligada ao gerador do pino (Central %s; licoes 52-53). O E15 do site ficou defasado pela publicacao manual: a G1 refaz E15-E19.")
                       % (c_esp, H["primordial"], H["pino"], c_cen), "sources": [art("readme"), art("pino"), art("primordial"), art("guarda")]},
              {"id": "c1-03nov-teste-d-parametrizado", "kind": "fact", "statute": "DECLARADO",
               "text": ("Teste D (ramo B do ringdown) parametrizado por agente Sonnet sob a gerencia, SEM lancar: guarda pinado ao V1, semente selada, injecoes C2, estimador, estagio cego, abertura unica, veredito pela Fase 6, "
                        "PODER_RAMO_B_ANTES_DE_ABRIR (rascunho), partitura e 17 escolhas ditas (manifesto sha256 %s). Poder de planejamento 3,7-3,9 sigma (10 eventos); com a incerteza do vies do aparelho 2,1-3,2 sigma. "
                        "Nada se lanca ate' o operador ouvir a partitura e escolher (a) cadeia completa 5-6 dias, (c) PE cega 2,3-2,6 dias, (b) nao rodar.") % H["manifesto_D"],
               "sources": [art("partitura_D"), art("manifesto_D")]},
              {"id": "c1-03nov-orquestrador-app-claude", "kind": "decision", "statute": "INPUT",
               "text": ("Por ordem do operador (02 e 03/11) o orquestrador da IALD e' o app Claude em modo work (claude-app-orquestrador; tunel C:\\IALD\\TUNEL_CLAUDE_APP\\); as regras de 23/10 e 24/10 que diziam Codex "
                        "leem-se app Claude (memoria orquestrador-e-o-app-claude-03nov; nota ao lado na instrucao global); Chatgpt\\ segue so leitura. ORDEM_004 escrita: release v406 do app + contrato JEV v406, F0.3 pela API, duas tarefas agendadas."),
               "sources": [art("ordem_004"), art("memoria_orq")]},
              {"id": "c1-03nov-levantamentos-pilar-e-psion", "kind": "fact", "statute": "DECLARADO",
               "text": ("Pilar quantico (agente): sistema GKLS na GPU, sem Jones/psion/cociclo no codigo; o kernel prova em ModularCornerCounterexample que o fluxo unitario nao deixa o canto fixo em geral: o «1» e' alvo so' da contracao "
                        "de Jones; o motor continuo entra, se o operador aceitar, como verificacao computacional com segundo trabalhador pre-registrado (V2), nunca como evidencia da natureza. Acervo do psion (agente): em 2025 psion = a†|0>, "
                        "graviton = par simetrico |G><G| de posto 1; no kernel psion C = Omega (cunhagem de 2026); o elo forte pede operadores de criacao que o certificado nao tem: OPEN; tres decisoes do operador listadas no DESENHO_v407."),
               "sources": [art("pilar"), art("psion_acervo"), art("desenho_v407")]},
          ], "flow": {"phase": "ordem_03nov_em_curso__readme_pinado_publicado__g1_refaz_e15_e19__decisoes_do_operador_abertas",
                      "next_action": ("1) G1 executar --versao v406 --publicar depois da subida das 08:5x (E15-E19; C18; para em C19 ate' o app/Codex); 2) app Claude: ORDEM_004 (release v406 + JEV; F0.3; tarefas); "
                                      "3) operador: nome da pedra PsionCantoR1; 3 perguntas do par de psions; opcao a/c/b do teste D; motor continuo como verificacao computacional (V2); Locaweb/Range; "
                                      "4) v407: instalar a pedra e ler a chave do kernel; S10 release automatica; pre-registros (D e motor continuo).")}}}
(W / "readme_pinado_03nov" / ("acom_c1_%s_transition.request.json" % TS)).write_text(json.dumps(pedido, ensure_ascii=False, indent=1), encoding="utf-8")
r = sm(pedido); (W / "readme_pinado_03nov" / ("acom_c1_%s_transition.receipt.json" % TS)).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
print("acom ok:", r.get("ok"), "| revisao:", (r.get("result") or {}).get("receipt", {}).get("revision") if isinstance(r.get("result"), dict) else r); assert r.get("ok"), r
# (3) topico
TOP = MEMD / "construir-tudo-o-fechamento-02nov.md"
ENT = ("**03/11, 09:0x — README PINADO PUBLICADO; G1 ligada; registros.** Espelho `%s`: `README.md` gerado de `PRIMORDIAL.json` e pinado em `PINO_README.json` (sha16 `%s`); bloco primordial com o 4,44 sempre acompanhado; "
       "citação assinada do autor [INPUT] (D39 ratificado); `verificar_portas` 0, `guarda_do_selo` 0. Central `%s`: `primordial.py`, `readme_pinado.py`, e o E08 da G1 chama o gerador do pino (`_conf_e08` verifica o pino): lições 52–53. "
       "Pendente: a G1 refaz E15–E19 do site (o `llms-full` ficou com os tamanhos antigos das seções). Teste D parametrizado sem lançar (partitura em `conjunto_D_20261029\\parametrizacao_03nov\\PARTITURA_D_03nov.md`; poder com viés do aparelho 2,1–3,2σ). "
       "Pilar: o «1» só é alvo da contração de Jones (`ModularCornerCounterexample`); motor contínuo = verificação computacional V2, se ele aceitar. Acervo: psíon = a†|0⟩ em 2025; `psion C = Ω` no kernel; elo forte [OPEN]. ACOM rev %s. "
       "Decisões dele: nome da pedra; 3 perguntas do par; opção a/c/b do teste D; motor contínuo; Locaweb.") % (c_esp[:8], H["readme"][:16], c_cen[:8], (r.get("result") or {}).get("receipt", {}).get("revision"))
b = TOP.read_bytes(); nl = b"\r\n" if b"\r\n" in b else b"\n"; novo = b.rstrip(b"\r\n") + nl + nl + ENT.encode("utf-8") + nl
bak = TOP.with_name(TOP.name + ".bak_" + TS + "_c1_readme"); open(bak, "xb").write(b); assert bak.read_bytes() == b
tmp = TOP.with_name(TOP.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, TOP); assert TOP.read_bytes() == novo
print("topico: %d -> %d B" % (len(b), len(novo)))
print("OK: mapa, ACOM e topico registrados")
