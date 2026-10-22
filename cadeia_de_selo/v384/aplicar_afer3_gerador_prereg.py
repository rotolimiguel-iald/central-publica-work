# -*- coding: utf-8 -*-
"""3a afericao no GERADOR DO PRE-REGISTRO: n(c2) sai da comparacao da CPU (so informacao); o volume do MAGMA em n = 4096 conta as sondas de tempo; a
ratificacao exige o rascunho APRESENTADO (--rascunho=<json>: a mesma especificacao e uma mensagem do operador POSTERIOR a ele); o instante com fuso;
os rascunhos por escolha (B_REDUZIDO e A) com nomes proprios; a afericao lida do arquivo de disposicoes; os textos: o plano B sem margem, as janelas como
«ao menos um ponto», a CPU independente so na algebra linear, NOT_COMPARABLE, o modo zero no D128, ParentGone, o lancador, o E8, o D128 sem cache.
Backup de bytes; ast."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
bak = P + ".bak_antes_afer3_" + time.strftime("%Y%m%d_%H%M%S")
open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
PAIRS = []
A = lambda o, n: PAIRS.append((o, n))

# --- uso e argumentos
A('''       [--escolha=B_REDUZIDO|A] [--ratificacao-prefixo=<inicio da mensagem do operador>] [--rascunho-spec=<spec_sha256 do rascunho apresentado>]"""''',
  '''       [--escolha=B_REDUZIDO|A] [--ratificacao-prefixo=<inicio da mensagem do operador> --rascunho=<o JSON do rascunho APRESENTADO ao operador>]"""''')
A('''RASCUNHO_SPEC = OPT.get("rascunho-spec")''', '''RASCUNHO_P = OPT.get("rascunho")
assert not RAT_PREFIXO or RASCUNHO_P, "a ratificacao exige o rascunho APRESENTADO ao operador (--rascunho=<json>)"
RASC = json.load(open(RASCUNHO_P, encoding="utf-8")) if RASCUNHO_P else None
RASCUNHO_SPEC = RASC["spec_sha256"] if RASC else None
DISP = os.path.join(ESTD, "disposicoes_afericoes_v384.json")''')
# --- a spec: n(c2) fora da comparacao; a nota do MAGMA com as sondas de tempo
A('''               "tol": {"cci": 1e-9, "purity": 1e-9, "folds_n_c1": 1e-9, "folds_n_c2": 1e-6, "gap_rel_rel": 1e-6, "choi_min": 1e-9, "min_gap_rel_for_compare": 1e-6},''',
  '''               "tol": {"cci": 1e-9, "purity": 1e-9, "folds_n_c1": 1e-9, "gap_rel_rel": 1e-6, "choi_min": 1e-9, "min_gap_rel_for_compare": 1e-6},''')
A('''                        "matriz (8 de 9 tamanhos de 16 a 576); o MAGMA nao caiu em nenhum tamanho TESTADO (n <= 1024 em volume; n = 4096 com 5 chamadas; n = 16384 nunca); "''',
  '''                        "matriz (8 de 9 tamanhos de 16 a 576); o MAGMA nao caiu em nenhum tamanho TESTADO (n <= 1024 em volume; n = 4096 com %d chamadas: %d no estresse e %d nas "
                        "sondas de tempo deste trabalhador; n = 16384 nunca); "''')
A('''                        "a troca de backend (torch.backends.cuda.preferred_linalg_library) e' marcada pelo PyTorch como experimental; o backend MAGMA esta em descontinuacao")},''',
  '''                        "a troca de backend (torch.backends.cuda.preferred_linalg_library) e' marcada pelo PyTorch como experimental; o backend MAGMA esta em descontinuacao") % (
                            N4096_EST + N4096_TIM, N4096_EST, N4096_TIM)},''')
A('''assert "branch_margin" not in wsrc, "o trabalhador ainda le branch_margin"''',
  '''assert "branch_margin" not in wsrc, "o trabalhador ainda le branch_margin"
assert "E8_cpu_reference_comparator_selftest" in wsrc and "CPU_REFERENCE_NOT_COMPARABLE" in wsrc and "class ParentGone(BaseException)" in wsrc, "o trabalhador nao e' o da 3a afericao"
# o MAGMA em n = 4096 (d = 64), LIDO: as chamadas do estresse e as das sondas de tempo deste trabalhador (3 por repeticao: o espectro e dois geradores)
N4096_EST = sum(int(v["reps"]) for k, v in list(ESTJ["pequeno"].items()) + list(ESTJ["grande"].items()) if "_magma_" in k and k.endswith("_4096") and v.get("rc") == 0)
N4096_TIM = 3 * int(tim["64"]["reps"])''')
# --- a ratificacao ligada ao rascunho apresentado e ao tempo
A('''RAT = None
if RAT_PREFIXO:
    r_ = _last(RAT_PREFIXO)
    assert r_, "a mensagem de ratificacao nao foi achada no transcrito: %r" % RAT_PREFIXO
    RAT = {"quando": r_[0], "verbatim": r_[1], "escolha": ESCOLHA, "spec_sha256_ratificada": SPEC_SHA, "spec_sha256_do_rascunho_apresentado": RASCUNHO_SPEC,
           "a_especificacao_ratificada_e_a_do_rascunho": (RASCUNHO_SPEC == SPEC_SHA) if RASCUNHO_SPEC else None}
VER = "V1" if RAT else "V1_RASCUNHO"''',
  '''RAT = None
if RAT_PREFIXO:
    r_ = _last(RAT_PREFIXO)
    assert r_, "a mensagem de ratificacao nao foi achada no transcrito: %r" % RAT_PREFIXO
    assert RASC.get("gerado_utc") and r_[0] > RASC["gerado_utc"], "a mensagem do operador (%s) nao e' POSTERIOR ao rascunho apresentado (%s)" % (r_[0], RASC.get("gerado_utc"))
    assert RASC["spec_sha256"] == SPEC_SHA and (RASC.get("desvio_do_plano_B") or {}).get("esta_especificacao", {}).get("escolha") == ESCOLHA, \\
        "a especificacao ratificada nao e' a do rascunho apresentado (escolha %s)" % ESCOLHA
    RAT = {"quando": r_[0], "verbatim": r_[1], "escolha": ESCOLHA, "spec_sha256_ratificada": SPEC_SHA, "spec_sha256_do_rascunho_apresentado": RASCUNHO_SPEC,
           "rascunho_apresentado": {"arquivo": os.path.basename(RASCUNHO_P), "sha256": fsha(RASCUNHO_P), "gerado_utc": RASC["gerado_utc"]},
           "a_especificacao_ratificada_e_a_do_rascunho": RASCUNHO_SPEC == SPEC_SHA}
VER = "V1" if RAT else ("V1_RASCUNHO_" + ESCOLHA)''')
# --- o plano B: tambem sem margem
A('''              "instância (o plano B contava %.1f s); (3) por isso o plano B inteiro, com os custos medidos agora, dá cerca de %.0f min (%.0f com a margem) e %s no prazo "
              "congelado de 5 h. Logo d = 64 vira camada de ESCALA''',
  '''              "instância (o plano B contava %.1f s); (3) por isso o plano B inteiro, com os custos medidos agora, dá cerca de %.0f min (%.0f com a margem) e, com a margem, %s no prazo "
              "congelado de 5 h; e, mesmo SEM margem, as fases do plano B antes do D128 levam cerca de %.0f min, acima do prazo de início de %.0f min: o D128 não rodaria. Logo d = 64 vira camada de ESCALA''')
A('''        "NÃO cabe" if totB * MARGEM >= SPEC["execution"]["um_py_timeout_s"] else "cabe", PLANO_B["T1"]["16"],''',
  '''        "NÃO cabe" if totB * MARGEM >= SPEC["execution"]["um_py_timeout_s"] else "cabe", (totB - estB["D128"]) / 60, 10800 / 60, PLANO_B["T1"]["16"],''')
# --- terminologia e textos dos testes
A('''        "CCI": "CCI = Tr Π ρ_ss: o peso do atrator no núcleo. O token NAME_IN_CORE_k_OF_c do veredito conta as configurações (d, n_c) em que existe, na grade, uma janela de γ_diss com atrator ÚNICO e CCI ≥ 1/2 — mede o ATRATOR no núcleo, não Π (Tr ΠΠ / Tr Π = 1 seria trivial).",''',
  '''        "CCI": "CCI = Tr Π ρ_ss: o peso do atrator no núcleo. O token NAME_IN_CORE_k_OF_c do veredito conta as configurações (d, n_c) com AO MENOS UM ponto da grade de atrator ÚNICO e CCI ≥ 1/2 (a «janela» relatada é o intervalo [menor γ, maior γ] desses pontos, com a contagem; os pontos não precisam ser contíguos) — mede o ATRATOR no núcleo, não Π (Tr ΠΠ / Tr Π = 1 seria trivial).",''')
A('''                    "o_que": "E1 amortecimento de amplitude (espectro e estado fundamental exatos); E2 dephasing puro detectado como DEGENERADO; E3 lei-raiz exata; E4 o estimador cego recupera b e p = 1/2 de gerador conhecido, com o certificado do ramo; E5 qubit térmico (Gibbs) e Spohn monótono; E6 a inversão do tempo não é CP; E7 o PISO do estimador: 6 000 matrizes exatas de posto um (d de 8 a 64; p = 1/2 e 1; inclusive k quase iguais), máximo ≤ critério/10. Se um falhar, NADA se calcula."},''',
  '''                    "o_que": "E1 amortecimento de amplitude (espectro e estado fundamental exatos); E2 dephasing puro detectado como DEGENERADO; E3 lei-raiz exata; E4 o estimador cego recupera b e p = 1/2 de gerador conhecido, com o certificado do ramo; E5 qubit térmico (Gibbs) e Spohn monótono; E6 a inversão do tempo não é CP; E7 o PISO do estimador: 6 000 matrizes exatas de posto um (d de 8 a 64; p = 1/2 e 1; inclusive k quase iguais), máximo ≤ critério/10; E8 o COMPARADOR da referência na CPU com linhas sintéticas (igual concorda; CCI fora da tolerância discorda; só n(c²) diferente concorda; tudo perto do limiar é não comparável; marca da rodada errada recusa). Se um falhar, NADA se calcula."},''')
A('''               "estrutural": "a unicidade do atrator em todos os pontos DA GRADE; a janela de γ_diss, entre pontos de atrator ÚNICO, em que o atrator guarda ao menos metade do peso no núcleo (CCI ≥ 1/2; o token NAME_IN_CORE); a janela das dobras n(c¹) ∈ [2,5; 3,5] e n(c²) ∈ [1,5; 2,5] entre pontos de atrator ÚNICO — como''',
  '''               "estrutural": "a unicidade do atrator em todos os pontos DA GRADE; se há AO MENOS UM ponto de atrator ÚNICO em que o atrator guarda ao menos metade do peso no núcleo (CCI ≥ 1/2; o token NAME_IN_CORE; relatados o menor e o maior γ desses pontos e a contagem, que não precisam ser contíguos); idem para as dobras n(c¹) ∈ [2,5; 3,5] e n(c²) ∈ [1,5; 2,5] (o token FOLDS_WINDOW) — como''')
A('''                 "o_que": "uma instância canônica em d = 128 (superoperador 16 384 × 16 384; n_c = 3; γ_diss = 1): espectro inteiro, estado estacionário, CCI e dobras; Spohn''',
  '''                 "o_que": "uma instância canônica em d = 128 (superoperador 16 384 × 16 384; n_c = 3; γ_diss = 1): espectro inteiro (com a identidade do modo zero: um espectro sem 0 é violação de identidade, IDENTITY_VIOLATED), estado estacionário, CCI e dobras (sem CCI se o atrator for DEGENERADO); Spohn''')
A('''                "o_que": "um subprocesso independente (numpy/scipy, 4 fios, prioridade baixa), lançado no começo e corrido em paralelo, recalcula todos os pontos do T2 em d = 8 e 16, sete em d = 32 e um em d = 64; compara status, CCI (1e−9), pureza (1e−9), dobras n(c¹) (1e−9) e n(c²) (1e−6; n(c³) não, porque λ^{1/4} amplia o arredondamento de autovalores ínfimos), gap (1e−6 relativo) e o menor autovalor de Choi (1e−9). As linhas com gap relativo < 1e−6 (em qualquer das duas bibliotecas) são CONTADAS e NÃO comparadas: perto do limiar de unicidade, duas bibliotecas corretas podem discordar no status e no gap (medido pela 2ª aferição); a referência só vale se ao menos uma linha for comparada. Vale só se a marca da rodada, o hash da especificação, β e o hash do trabalhador baterem e o filho sair com código 0. A espera pela CPU é de até 1 h DEPOIS das fases da GPU. Discordância ou ausência anula o resultado."}},''',
  '''                "o_que": "um subprocesso INDEPENDENTE NA ÁLGEBRA LINEAR (numpy/LAPACK contra torch/MAGMA, processo à parte, 4 fios, prioridade baixa), com a MESMA construção dos operadores e o mesmo classificador do trabalhador — a construção é conferida pelas fontes por sha256 e pelo E1..E8, não pela CPU —, lançado no começo e corrido em paralelo, recalcula todos os pontos do T2 em d = 8 e 16, sete em d = 32 e um em d = 64; compara status, CCI (1e−9), pureza (1e−9), dobras n(c¹) (1e−9), gap (1e−6 relativo) e o menor autovalor de Choi (1e−9); n(c²) e n(c³) só como INFORMAÇÃO (as potências λ^{1/2} e λ^{1/4} ampliam o arredondamento de autovalores ínfimos: a 2ª e a 3ª aferições mediram, com operadores aleatórios, |Δn(c²)| até cerca de 9e−6 com gap relativo perto de 1e−6, entre MAGMA e LAPACK [DECLARADO pela aferição]). As linhas com gap relativo < 1e−6 (em qualquer das duas bibliotecas) são CONTADAS e NÃO comparadas: perto do limiar de unicidade, duas bibliotecas corretas podem discordar no status e no gap; se NENHUMA linha puder ser comparada, o veredito é CPU_REFERENCE_NOT_COMPARABLE (não houve discordância nem conferência). Vale só se a marca da rodada, o hash da especificação, β e o hash do trabalhador baterem e o filho sair com código 0; o filho confere que o trabalhador vive e sai se ele morrer. A espera pela CPU é de até 1 h DEPOIS das fases da GPU. Discordância, ausência ou nenhum ponto comparável anulam o resultado."}},''')
# --- a arvore
A('''        "0. recusas e falhas antes do cálculo, todas TGL_QUANTUM_PILLAR_V1__NOT_RUN__<motivo>__GATE_UNTOUCHED: no trabalhador MISSING_ARGUMENTS, SPEC_HASH_MISMATCH, WORKER_HASH_MISMATCH, GPU_UNAVAILABLE, WORKER_FATAL (exceção fora das fases) e PARENT_GONE (o um.py morreu: o trabalhador se encerra sozinho);''',
  '''        "0. recusas e falhas fora das fases (antes, entre ou DEPOIS delas), todas TGL_QUANTUM_PILLAR_V1__NOT_RUN__<motivo>__GATE_UNTOUCHED: no trabalhador MISSING_ARGUMENTS, SPEC_HASH_MISMATCH, WORKER_HASH_MISMATCH, GPU_UNAVAILABLE, WORKER_FATAL (exceção fora das fases; se vier depois delas, os dados de T1–T4 continuam no result.json, mas o veredito é NOT_RUN) e PARENT_GONE (o um.py morreu: o trabalhador o vê nas fases, na espera da CPU e no RK4 do D128 e se encerra; a exceção não é engolida pelos tratadores das fases);''')
A('''        "8. a referência na CPU discorda, falta ou não é desta rodada -> ..._CPU_REFERENCE_DISAGREES_OR_ABSENT__RESULTS_VOID__GATE_UNTOUCHED",''',
  '''        "8. a referência na CPU discorda, falta ou não é desta rodada -> ..._CPU_REFERENCE_DISAGREES_OR_ABSENT__RESULTS_VOID__GATE_UNTOUCHED; nenhum ponto comparável (todos perto do limiar) -> ..._CPU_REFERENCE_NOT_COMPARABLE__RESULTS_VOID__GATE_UNTOUCHED",''')
A('''        "7. uma identidade foi violada -> ..._IDENTITY_VIOLATED_<n>__ENGINE_SUSPECT__RESULTS_VOID__GATE_UNTOUCHED",''',
  '''        "7. uma identidade foi violada (inclusive o modo zero no D128) -> ..._IDENTITY_VIOLATED_<n>__ENGINE_SUSPECT__RESULTS_VOID__GATE_UNTOUCHED",''')
# --- negativos
A('''        "NAME_IN_CORE k < 12: em alguma configuração, na grade, o atrator nunca guarda metade do peso no núcleo",''',
  '''        "NAME_IN_CORE k < 12: em alguma configuração, entre os pontos de atrator ÚNICO da grade, nenhum guarda metade do peso no núcleo",''')
A('''        "D128 NOT_RUN_* ou INTERRUPTED: a escala não foi alcançada nesta rodada — dito"],''',
  '''        "D128 NOT_RUN_* ou INTERRUPTED: a escala não foi alcançada nesta rodada — dito; um resultado completo sem o D128 rodado é negativo honesto: vale para a custódia, não vai ao cache, e a razão fica gravada (not_cached_code) e dita no artigo"],''')
# --- execucao
A('''        "se o um.py sair por qualquer caminho, um gancho de saída encerra a ÁRVORE do trabalhador (taskkill /T /F; a referência na CPU junto); se o um.py morrer à força, o trabalhador vê o pai morto e se encerra (PARENT_GONE)",''',
  '''        "se o um.py sair por qualquer caminho, um gancho de saída encerra a ÁRVORE do trabalhador (taskkill /T /F; a referência na CPU junto); se o um.py morrer à força, o trabalhador vê o pai morto — nas fases, na espera da CPU e no RK4 do D128 (não durante uma única chamada longa de espectro ou estacionário, que termina primeiro) — e se encerra (PARENT_GONE); se o trabalhador morrer (por exemplo, queda nativa), a referência na CPU o vê e sai; o arquivo do pilar de uma rodada anterior no Nós nunca sobrevive (um marcador desta rodada o substitui)",''')
A('''        "o lançador do rito (ato da gerência) registra o estado de antes (a tarefa «IALD Llama Server» existe? o servidor estava ligado?), encerra trabalhadores órfãos de rodadas mortas, para a tarefa agendada e o supervisor, exige nenhum llama-server vivo e VRAM usada ≤ 6 000 MiB (senão não roda), vigia contra o religamento durante o rito (o vigia sai se o lançador morrer, e em 8 h no máximo) e, no fim, mesmo se o rito falhar, encerra órfãos e religa a tarefa SÓ se ela existia e o servidor estava ligado antes",''',
  '''        "o lançador do rito (ato da gerência) lê o estado de antes pela TAREFA «IALD Llama Server» e pelo processo (sonda vazia conta como «ligado»), RECUSA se o servidor estiver ligado sem a tarefa (não saberia religá-lo), encerra trabalhadores de rodadas mortas, arma a restauração ANTES de parar, para a tarefa e o supervisor, exige nenhum llama-server vivo e VRAM usada LEGÍVEL e ≤ 6 000 MiB (senão não roda), vigia contra o religamento durante o rito (o vigia sai se o lançador morrer, e em 8 h no máximo), e no fim — mesmo se o rito falhar ou o lançador receber TERM/HUP/INT, caso em que encerra primeiro a árvore do um.py — encerra o vigia e os trabalhadores restantes e religa a tarefa se o servidor estava ligado; enquanto o servidor estiver parado pelo rito, um marcador fica no pacote, e a rodada seguinte o lê e religa",''')
# --- reaproveitamento
A('''        "rodada completa (sem TGL_RITE_CHECKPOINT): calcula sempre e, só se o resultado for COMPLETO (o ramo 9 da árvore, sem parcial, com a cadeia conferida E com o D128 RODADO), GRAVA em cache/checkpoints/quantum_pillar/<chave>/ — prazo, memória, recusa, fase falhada ou D128 não rodado nunca vão ao cache; uma falha ao gravar o cache fica registrada sem tocar o veredito",''',
  '''        "rodada completa (sem TGL_RITE_CHECKPOINT): calcula sempre e, só se o resultado for COMPLETO (o ramo 9 da árvore, sem parcial, com a cadeia conferida E com o D128 RODADO), GRAVA em cache/checkpoints/quantum_pillar/<chave>/ — prazo, memória, recusa, fase falhada ou D128 não rodado nunca vão ao cache (a razão fica em not_cached_code e no artigo); uma falha ao gravar o cache fica registrada sem tocar o veredito, e o cache antigo volta ao lugar",''')
# --- a afericao, lida do arquivo de disposicoes
A('''    "afericao": ("1ª passada do aferidor (03/10): 17 achados, corrigidos no trabalhador ou no texto; 2ª passada (03/10): %d achados sobreviventes à verificação adversarial, "
                 "todos corrigidos no código ou no texto antes deste documento; o registro verbatim e as disposições ficam em AFERIDOR_v384.txt no pacote da "
                 "v384 (afericao2_resultado.json, sha256 %s)") % (len(AF2["sobreviventes"]), fsha(AFER2)[:16]),''',
  '''    "afericao": DISP_J["texto_para_o_pre_registro"] + " (disposições achado a achado em %s, sha256 %s; registro verbatim em AFERIDOR_v384.txt)" % (os.path.basename(DISP), fsha(DISP)[:16]),''')
A('''AF2 = json.load(open(AFER2, encoding="utf-8"))''', '''AF2 = json.load(open(AFER2, encoding="utf-8"))
DISP_J = json.load(open(DISP, encoding="utf-8"))''')
# --- o instante com fuso
A('''    "gerado": time.strftime("%Y-%m-%d %H:%M:%S"),''', '''    "gerado": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "gerado_utc": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),''')
# --- o MD da ratificacao
A('''    if RASCUNHO_SPEC:
        A("- especificação do rascunho apresentado: `%s` (%s)" % (RASCUNHO_SPEC, "a mesma" if RAT["a_especificacao_ratificada_e_a_do_rascunho"] else "OUTRA: a escolha mudou as contagens"))''',
  '''    A("- rascunho apresentado: `%s` (sha256 `%s`, gerado %s); especificação `%s` (%s)" % (RAT["rascunho_apresentado"]["arquivo"], RAT["rascunho_apresentado"]["sha256"],
      RAT["rascunho_apresentado"]["gerado_utc"], RASCUNHO_SPEC, "a mesma" if RAT["a_especificacao_ratificada_e_a_do_rascunho"] else "OUTRA"))''')
A('''    A("**PENDENTE.** Este é o RASCUNHO levado ao operador; nada se calcula com os operadores da teoria antes da ratificação, e o candidato instalável recusa um pré-registro sem ela.")''',
  '''    A("**PENDENTE.** Este é o RASCUNHO (escolha %s) levado ao operador; nada se calcula com os operadores da teoria antes da ratificação, e o candidato instalável recusa um pré-registro sem ela." % ESCOLHA)''')

for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:130])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8")
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS), "trocas; backup", os.path.basename(bak))
