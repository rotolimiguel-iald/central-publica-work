# -*- coding: utf-8 -*-
"""Acrescenta o bloco 8 (estado de 03/10, tarde) a memoria v384-pilar-quantico-gpu-02out.md. Backup de BYTES antes; temporario -> conferir -> substituir.
Os numeros sao LIDOS dos artefatos por script (rascunho do pre-registro, manifesto do candidato de ensaio, afericao 2)."""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "v384-pilar-quantico-gpu-02out.md")
PR = os.path.join(HERE, "rascunho_prereg_v3", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO.json")
CA = os.path.join(HERE, "CANDIDATO_v384_ENSAIO.json")
AF = os.path.join(HERE, "afericao2_resultado.json")
pr = json.load(open(PR, encoding="utf-8")); ca = json.load(open(CA, encoding="utf-8")); af = json.load(open(AF, encoding="utf-8"))
o = pr["orcamento_estimado"]; dv = pr["desvio_do_plano_B"]
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
MARK = "<!-- estado_03out_tarde_v384 -->"
bloco = (
    "\n\n" + MARK + "\n"
    "**8. Estado (03/10/2026, tarde) — gerência, em nome próprio; números lidos dos artefatos por script:**\n"
    "- **A biblioteca:** o cuSOLVER padrão do PyTorch 2.11 derruba o processo (violação de acesso 0xC0000005) de modo DETERMINÍSTICO e dependente da matriz em 8 de 9 tamanhos "
    "de 16 a 576 [REAL, mapa seq 312–314]; o MAGMA não caiu em nenhum tamanho testado e passou na durabilidade do pipeline ⟹ **MAGMA em TODO tamanho**, por "
    "`preferred_linalg_library`, que o PyTorch marca como experimental; n = 16 384 (o D128) nunca foi testado; dependência declarada (o MAGMA está em descontinuação).\n"
    "- **O custo e o desvio do plano B:** com o MAGMA e o certificado do ramo, a instância em d = 64 custa %s s e a injeção do T1 %s s; o plano B inteiro daria ~%s min "
    "(%s com margem) e NÃO cabe no prazo de 5 h. Logo a especificação **B_REDUZIDO**: d = 64 vira camada de escala (T1 %s, T4 %s, T2 %s pontos), a estatística forte "
    "fica em d ≤ 32 (T1 %s; T4 %s); total ~%s min de GPU (%s com margem). **Alternativa A** (escolha do operador): d = 64 como no plano B (T4 %s, T2 %s pontos, T1 %s), "
    "+%s min (+%s com margem), prazo de início do D128 de 3 h → 4 h. Os dois vão ao operador.\n"
    "- **As aferições:** 1ª passada 17 achados; 2ª passada %d achados sobreviventes (`afericao2_resultado.json`, sha256 %s), todos tratados no código ou no texto; "
    "a 3ª passada (verificação da resolução + caça de regressões) em curso.\n"
    "- **O rascunho do pré-registro:** `scratchpad\\v384\\rascunho_prereg_v3\\PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO.json` (sha256 %s), especificação %s, "
    "trabalhador %s. Sem a ratificação o gerador só escreve o RASCUNHO; o V1 congelado nasce em `C:\\IALD\\Bancada_Um\\investigacao\\preregistro_pilar_quantico_03out\\` "
    "com a mensagem do operador lida verbatim do transcrito (campo `ratificacao_do_operador`), e o candidato instalável recusa pré-registro sem ela.\n"
    "- **O candidato de ENSAIO:** `um_v384_candidato_ENSAIO.py` sha16 %s (base v383 %s; %d patches). A fumaça, o ensaio a seco e os esperados rodam o trabalhador com os "
    "operadores da teoria ⟹ só DEPOIS da ratificação.\n"
    "- **Terminologia fixada (2ª aferição):** Π = o projetor do núcleo = ker K («o Nome como matriz» [ONTO]); ρ_ss = o ATRATOR; CCI = Tr Πρ_ss; o token NAME_IN_CORE mede o atrator no núcleo.\n"
) % (o["custos_medidos_s"]["instancia"]["64"] if isinstance(list(o["custos_medidos_s"]["instancia"].keys())[0], str) else o["custos_medidos_s"]["instancia"][64],
     o["custos_medidos_s"]["injecao_T1_sem_ruido"].get("64", o["custos_medidos_s"]["injecao_T1_sem_ruido"].get(64)),
     dv["plano_B"]["estimativa_com_os_custos_medidos_agora_min"], dv["plano_B"]["com_margem_min"],
     pr["spec"]["T1"]["d_counts"]["64"], pr["spec"]["T4"]["d_counts"]["64"], dv["esta_especificacao"]["T2_pontos_d64"],
     json.dumps({k: v for k, v in pr["spec"]["T1"]["d_counts"].items() if k != "64"}), json.dumps({k: v for k, v in pr["spec"]["T4"]["d_counts"].items() if k != "64"}),
     o["total_min"], o["total_com_margem_min"],
     dv["alternativa_A"]["contagens_d64"]["T4_d64"], dv["alternativa_A"]["contagens_d64"]["T2_gamma_d64"] * 3, dv["alternativa_A"]["contagens_d64"]["T1_d64"],
     dv["alternativa_A"]["minutos_a_mais_estimados"], dv["alternativa_A"]["minutos_a_mais_com_margem"],
     len(af["sobreviventes"]), h(AF)[:16], h(PR)[:16], pr["spec_sha256"][:16], pr["spec"]["worker_sha256"][:16],
     ca["sha16"], ca["base_v383_sha16"], len(ca["patches"]))
raw = open(MEM, "rb").read()
assert MARK.encode("utf-8") not in raw, "o bloco 8 ja existe"
ts = time.strftime("%Y%m%d_%H%M%S"); bak = MEM + ".bak_" + ts
open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
new = raw + bloco.encode("utf-8")
tmp = MEM + ".tmp_" + ts
open(tmp, "wb").write(new); assert os.path.getsize(tmp) == len(new) and open(tmp, "rb").read().startswith(raw)
os.replace(tmp, MEM)
assert os.path.getsize(MEM) == len(new) > len(raw)
print("ok", len(raw), "->", len(new), "backup", os.path.basename(bak))
print(bloco)
