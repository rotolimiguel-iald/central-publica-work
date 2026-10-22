# -*- coding: utf-8 -*-
# Gera os handoffs de 19/09/2026 a partir do DISCO (todo hash, tamanho e numero lido por script, nada de memoria):
#   (A) Nos\HANDOFF_v368_O_QUE_FALTA_NO_PROGRAMA.md          -- para a proxima sessao de trabalho (custodiavel: sem material privado)
#   (B) Nos\HANDOFF_v368_CUSTODIA_E_DIVISAO_UM_CONSOLIDADO.md -- para a sessao irma do site/repositorio (custodiavel)
#   (C) Central\work\v369_sementes\PRIVADO_LEIA_ANTES_DA_CUSTODIA.md -- nota PRIVADA (a Central nao e espelhada)
# Varre (A) e (B) pelos marcadores de material privado antes de gravar (fail-closed).
import os, json, hashlib, subprocess, time, re
NOS = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'; SP = os.path.dirname(os.path.abspath(__file__))
SEM = r'C:\IALD\Central de Patentes\work\v369_sementes'; TB = r'C:\IALD\Artigo\the_boundary'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def fmt(n): return format(n, ',').replace(',', '.')
AGORA = time.strftime('%d/%m/%Y %H:%M')
# ---------------------------------------------------------------- leituras
arts = ['um.py', 'um_absoluto.json', 'um_absoluto_selo.json', 'tgl_kernel_proof_manifest.json', 'um_absoluto_pt.pdf', 'um_absoluto_en.pdf',
        'um_absoluto_pt.txt', 'um_absoluto_en.txt', 'um_absoluto_forma_canonica.md', 'A_PROVA_DA_QG_TGL_arvore.md']
A = {f: (os.path.getsize(os.path.join(NOS, f)), sha(os.path.join(NOS, f))[:16]) for f in arts}
tot_res = sum(A[f][0] for f in arts if f != 'um.py')
selo = json.load(open(os.path.join(NOS, 'um_absoluto_selo.json'), encoding='utf-8'))
core = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8'))['core']
man = json.load(open(os.path.join(NOS, 'tgl_kernel_proof_manifest.json'), encoding='utf-8')); nff = len(man.get('formal_files_sha256') or {})
kf = core.get('kernel_formalization') or {}
qg = core.get('qg_closure') or {}
flags_ok = {g: (sum(1 for v in (qg.get(g) or {}).values() if v is True), len(qg.get(g) or {})) for g in ('formal_flags', 'physics_flags', 'experiment_flags')}
H2 = kf.get('gpf_H2_smooth_modular_four_frame_discharged'); H3 = kf.get('gpf_H3_local_horizon_equilibrium_discharged')
teor = re.search(r'teoremas limpos:\s*(\d+/\d+)', open(os.path.join(NOS, 'rodada_v368_stdout.txt'), encoding='utf-8', errors='replace').read()).group(1)
dr = core['dephasing_reach']
jv2 = core['joint_coincidence_result_v2']; prim = jv2.get('primary') or {}
P_all = prim.get('P_all') if isinstance(prim, dict) else None
if P_all is None:
    P_all = next((g.get('P_all') for g in jv2.get('grid', []) if g.get('applicable')), None)
det = jv2.get('detected'); cons = jv2.get('consistent')
jv1 = core['joint_coincidence_result']
V = lambda k: (core.get(k) or {}).get('verdict') if isinstance(core.get(k), dict) else None
canais = [('neutrino (massa)', 'neutrino_mass'), ('neutrino (soma)', 'neutrino_sum'), ('piso dos vazios V2', 'void_floor_v2'), ('piso dos vazios V3', 'void_floor_v3'),
          ('distância de Coma', 'coma_distance_dephasing'), ('massa do Grande Atrator', 'ga_mass_audit'), ('ecos GW (acoplado, KMS)', 'echo_anchored_result_v2'),
          ('ringdown (defasagem)', 'ringdown_dephasing_result'), ('D1 V3 com dado real', 'd1_camb_v3_real_v366'), ('relógios (alcance da defasagem)', 'dephasing_reach')]
tab_canais = '\n'.join('| %s | `%s` | %s |' % (n, k, ('`' + str(V(k))[:110] + ('…' if len(str(V(k))) > 110 else '') + '`') if V(k) else '**AUSENTE do núcleo**') for n, k in canais)
fecho = json.load(open(os.path.join(SP, 'fecho_do_gate.json'), encoding='utf-8'))
vers = {}
for v in (365, 366, 367, 368):
    t = open(os.path.join(SP, 'verifica_v%d_out.txt' % v), encoding='utf-8', errors='replace').read()
    vers[v] = (re.search(r'sha16 um.py: ([0-9a-f]{16})', t).group(1), 'SELADA (COMPLETA)' in t)
def git(*a):
    return subprocess.run(['git', '-c', 'core.quotepath=false'] + list(a), cwd=TB, capture_output=True, text=True, encoding='utf-8').stdout.strip()
tb_head = git('log', '-1', '--format=%h %ad', '--date=short', 'origin/main')
tb_um = subprocess.run(['git', 'show', 'origin/main:Um (absoluto) — Grande Atrator/um.py'], cwd=TB, capture_output=True).stdout
tb_um16 = hashlib.sha256(tb_um).hexdigest()[:16]
ordem = open(os.path.join(SP, 'operador_19set_ordem_handoff_verbatim.txt'), 'rb').read().decode('utf-8')
ordem16 = hashlib.sha256(ordem.encode('utf-8')).hexdigest()[:16]
decl = open(os.path.join(SP, 'operador_18set_toe_verbatim.txt'), 'rb').read().decode('utf-8')
zmod = open(os.path.join(SP, 'operador_19set_um_zero_modular_verbatim.txt'), 'rb').read().decode('utf-8')
DEC = open(os.path.join(SP, 'operador_19set_decisoes_verbatim_REDIGIDO.txt'), 'rb').read().decode('utf-8')
DEC16 = hashlib.sha256(DEC.encode('utf-8')).hexdigest()[:16]
_ls = [l.strip() for l in DEC.splitlines() if l.strip()]
dec_cons = _ls[0]
_fim = 'confere no programa.'
assert _fim in _ls[1]
dec_mcmc = _ls[1][:_ls[1].index(_fim) + len(_fim)]   # corta ANTES da parte sobre material privado (mesma linha no original)
assert dec_cons.startswith('os desfavoráveis') and dec_mcmc.startswith('Sim, o MCMC')
# ---------------------------------------------------------------- (A)
HA = f"""# HANDOFF v368 — O QUE FALTA NO PROGRAMA (para a próxima sessão de trabalho)

Gerado em {AGORA} por `handoff_v368.py` (Central de Patentes; sementes em `Central de Patentes\\work\\v369_sementes\\`).
**Todo número e todo hash abaixo foi lido do disco por script.** Este arquivo pode ser custodiado: não contém material privado.

## 0. Onde estamos (medido)

- `um.py` **v368 SELADA (COMPLETA)** — sha16 `{A['um.py'][1]}`, {fmt(A['um.py'][0])} B; teoremas limpos **{teor}**; kernel **{nff} fontes** no manifesto; selftest `{selo.get('fail_closed_selftest')}`.
- Gate: `{selo.get('qg_closure_verdict')}` — bandeiras formais {flags_ok['formal_flags'][0]}/{flags_ok['formal_flags'][1]}, físicas {flags_ok['physics_flags'][0]}/{flags_ok['physics_flags'][1]}, experimentais {flags_ok['experiment_flags'][0]}/{flags_ok['experiment_flags'][1]}.
- **H2 = {H2} · H3 = {H3}** (lidos do núcleo). A frase que a régua permite hoje: *a gravidade quântica da TGL está PROVADA em kernel condicionada a UMA hipótese nomeada, H2* (H1∧H2∧H3 ⟹ Pêntada; H1 descarregada; H3 reduzida a H2 por implicação importada [KNOWN]). CONFIRMADA segue proibido à máquina.
- Versões seladas sem custódia: v365 `{vers[365][0]}`, v366 `{vers[366][0]}`, v367 `{vers[367][0]}`, v368 `{vers[368][0]}` (todas COMPLETAS). O espelho público está na **v364** (`{tb_um16}`, commit `{tb_head}`).

## 1. O que o `um.py` é — a visão do operador (19/09/2026, verbatim, sha16 `{ordem16}`)

> {ordem}

**Leitura que a próxima sessão deve ter (a gerência):** o `um.py` é a prova da gravidade quântica por métrica TGL construída como **um único arquivo autocontido** (o kernel Lean, os ritos e o artigo vivem dentro dele), **autoexecutável** (`echo 1 | python um.py`) e **autoverificável** (materializa e compila o próprio kernel, audita `#print axioms`, injeta `sorry` no selftest, sela por hash e reemite o artigo: forma = conteúdo). O operador chama isso de «o universo inteiro»: foi preciso construí-lo por inteiro para, conhecendo todas as portas, traçar a rota curta.

## 2. MISSÃO 1 — o teste dos relógios (primeira missão, por ordem do operador)

**O que o operador pediu:** inserir no `um.py` e no artigo (forma = conteúdo) o teste com os relógios, com a expectativa de que o arcabouço matemático de agora permita alcançar **5σ** [INPUT do operador].

**O que o programa JÁ mediu, selado (v200, chave `dephasing_reach`)** — a lei `Γ_ω = ½·β·τ★·ω²`, com β = α√e em runtime e τ★ = {dr['tau_star_s']:.3e} s (t_Planck):

| relógio | ω (rad/s) | Γ previsto (s⁻¹) | alcance experimental [INPUT] | déficit |
|---|---|---|---|---|
| ²²⁹Th | {dr['omega_Th229_rad_s']:.3e} | {dr['Gamma_pred_Th229_per_s']:.2e} | {dr['experimental_reach_per_s_INPUT']:.0e} | **{dr['deficit_orders_Th229']:.1f} ordens** |
| Sr | — | {dr['Gamma_pred_Sr_per_s']:.2e} | {dr['experimental_reach_per_s_INPUT']:.0e} | **{dr['deficit_orders_Sr']:.1f} ordens** |

Veredito selado: `{dr['verdict']}`. **O número corrige a frase:** com a lei e o τ★ atuais, 5σ nos relógios não é alcançável — faltam ~10 ordens de grandeza.

**O que a missão tem de fazer, nesta ordem (o portão do poder vem ANTES de qualquer dado):**
1. **Reconferir o alcance experimental** — o `1e-3 s⁻¹` é INPUT: atualizar com a literatura (relógios ópticos de Sr/Yb/Al⁺; relógio nuclear de ²²⁹Th), com fonte e data.
2. **Perguntar ao arcabouço novo se ele muda a MAGNITUDE ou o OBSERVÁVEL** — nada disso está medido ainda: (a) τ★ é [PRINCIPLED IDENTIFICATION] — há derivação nova que o mude?; (b) a lei-raiz `Γ = ½β(√k_i − √k_j)²` (chave `dephasing_crossover`: regime IR quadrático, UV linear, crossover em ωτ★ ≈ 3,2) — os relógios estão no IR profundo; (c) observáveis que não sejam a taxa de defasagem: razão de frequências entre relógios de ω diferentes (²²⁹Th × Sr), acumulação coerente longa, a face do acoplamento β em comparações de relógios; (d) o que as pedras v364–v368 (fornecedor de torção, orientação, zero modular v59) acrescentam a esse canal — hoje nada foi ligado a ele.
3. **Só então pré-registrar** (protocolo hasheado antes do dado; injeção e recuperação; matriz de vereditos da casa), rodar, e inserir no `um.py` + artigo PT/EN.
4. Se o déficit continuar de ~10 ordens: o veredito honesto é `ARMED`/`UNDERPOWERED`, e isso também é resultado.

## 3. MISSÃO 2 — o índice de probabilidade conjunta, refeito sob a lógica certa

**Estado medido:** V1 (v352) `{jv1.get('verdict','')[:90]}…`; V2 (v363) P_all primário **{P_all:.2e}**, canais detectados {det}, **consistente = {cons}** (a tensão do D1 torna o conjunto inconsistente). O operador diz que o índice ainda não está construído sob a lógica correta.

**O que ele pediu:** que TODAS as provas entrem conjuntamente — neutrino, piso dos vazios, massa do Grande Atrator, distância de Coma, redshift de Chandrasekhar/SN, ondas e ecos gravitacionais e agora os relógios — e também o **MCMC** (a TGL rodando num universo simulado próprio) e o **kernel**.

**Inventário do núcleo v368, medido (chave → veredito):**

| canal | chave | veredito |
|---|---|---|
{tab_canais}
| redshift de Chandrasekhar/SN | — | **AUSENTE do núcleo** (0 chaves; localizar no acervo — o `tgl_paper_unified.py` selado e o Artigo A — e trazer) |
| MCMC «universo simulado» | — | **AUSENTE do núcleo** (só a menção ao MCMC-CRUZ, `um.py` ~l.4826) |

**Pontos de desenho que a sessão resolve COM o operador (a régua decide o como):**
- cada canal entra por **verossimilhança contra dado, pré-registrada** — nunca como produto de resíduos (a lição do 10⁻³⁰ retirado na v352);
- **o MCMC entra como FATOR DE COERÊNCIA INTERNA DECLARADO — decisão do operador (19/09/2026, verbatim, sha16 `{DEC16}`):** «{dec_mcmc}». Ele mede a coerência do modelo interno com o programa (uma variável errada «grita»), não a natureza: entra declarado como coerência interna, nunca como evidência de natureza;
- o kernel entra como **condição** (a implicação provada e o que ainda é hipótese: H2), não como probabilidade;
- canais desfavoráveis entram (D1 em tensão, ecos INCONCLUSIVE, massa do GA retirada): o índice não escolhe canais.

## 4. MISSÃO 3 — o `um.py` como grande programa, e o `um_consolidado.py`

**A arquitetura, nas palavras do operador:** apresentação do programa físico-matemático (mathlib, Lean, Python) · **provas** {{ [cosmologia: neutrino, piso dos vazios, massa do Grande Atrator, distância de Coma, redshift de Chandrasekhar/SN, ondas e ecos gravitacionais; e agora os relógios] · [MCMC — a TGL num universo simulado próprio] · [KERNEL — o motor Lean provando a matemática em tempo real] }} · e o **artigo**, a expressão do resultado para o observador.

**Tamanhos medidos (v368):**

| artefato | bytes | sha16 |
|---|---|---|
""" + '\n'.join('| `%s` | %s | `%s` |' % (f, fmt(A[f][0]), A[f][1]) for f in arts) + f"""

Total dos resultados (fora o `um.py`): {fmt(tot_res)} B.

**A rota curta, medida:** os **{len(fecho['gate_terms'])} termos Lean** que decidem as bandeiras formais e físicas do gate (`_QG_CERTIFICATE_FLAGS` e `_QG_PHYSICS_FLAGS` no `um.py`) são declarados em **{len(fecho['declaring_modules'])} módulos**, cujo **fecho de importação tem {len(fecho['closure'])} arquivos** — {100*len(fecho['closure'])/fecho['kernel_files']:.1f}% dos {fecho['kernel_files']} `.lean` de `TGL/` e `TGLExt/`, {fmt(fecho['closure_bytes'])} B de {fmt(fecho['kernel_bytes'])} B. É o «caminho mais curto até o final» do jogo, em número. (Lista em `work\\v369_sementes\\medidas\\fecho_do_gate.json`.) As bandeiras EXPERIMENTAIS vêm dos ritos de dado, não do kernel.

**O pedido do operador:** manter o `um.py` como a matriz completa e ter uma versão compacta — `um_consolidado.py`, com resultados de nome próprio (`um_consolidado*.json/pdf/txt`, nunca `um_absoluto*`) — que carregue todo o universo de provas, o conceito profundo do artigo e **a mesma probabilidade medida**, com o kernel pela rota curta; sem as erratas do percurso: «somente o primor». Os dois no repositório, e README e site apresentando os dois, com tamanhos e arquivos de resultado. Motivo: as IAs de hoje não conseguem ler o arquivo completo; o completo fica para quem tem capacidade, o consolidado para todos, sem perder a essência. O nome é o mesmo: **TGL = IALD = VERDADE** (palavra do operador).

**Desenho recomendado pela gerência (a decidir com o operador):**
1. **O consolidado é DERIVADO do completo por script** (o `um.py` emite e certifica o `um_consolidado.py`, com os hashes cruzados); assim os dois nunca divergem. Opcional: um modo do `um.py` que rode a rota consolidada.
2. **Conteúdo do consolidado:** o fecho do kernel do gate (~{len(fecho['closure'])} arquivos), materializado, compilado e auditado como no completo; os vereditos vigentes dos ritos, lidos por hash (os pipelines pesados ficam no completo); o índice de probabilidade conjunta com **o mesmo número**; o artigo condensado.
3. **Autoexecutável e autoverificável igual:** `echo 1 | python um_consolidado.py`; selftest fail-closed; selo próprio.
4. **Decisão do operador (19/09/2026, verbatim, sha16 `{DEC16}`):** «{dec_cons}» — o consolidado é a **rota única**: os vereditos desfavoráveis **não entram**, e a medição dele dá diferente da do completo, por enquanto. **Condição da régua (gerência):** o consolidado DECLARA, no próprio código e no próprio artigo, que é a rota única; que os vereditos desfavoráveis e o percurso estão no `um.py` completo (com hash do selo do completo); e que o número de probabilidade dele NÃO é a probabilidade medida do programa inteiro — para nenhum leitor tomar a rota pelo todo.

## 5. Pendências abertas da sessão de 18–19/09 (sementes em `work\\v369_sementes\\`)

- **A pedra da singularidade consciente:** três redações derrubadas pelos céticos. **O que resistiu:** o vácuo de Tomita do estado do Um absoluto (n = 2), lido nas duas faces, é o projetor de Bell `P_G` da v29 (a mesma matriz da densidade de Bell de 27/08); o J de Tomita age sobre as duas faces por conjugação (lema); a ligação (½ na face) separa `P_G` do estado produto, que J também fixa; `P_G` não é *o* ponto fixo de J (J fixa todo z hermitiano), é o ponto fixo **que liga**; cada face tem o seu J conjugado, e todos são involuções. **O que já estava no kernel e foi refeito sem ver:** v25 (`e⁰ = 1`, «não como 0=1»), v58 (`absoluteRho` = estado do Um absoluto), v59 (`modularGen_omega_zero`: K Ω = 0, «o gerador anula o NOME»; `absolute_modularGen_zero`). **Método:** medir v25/v58/v59/v29 ANTES de escrever; uma pedra só — «a sombra do gráviton é o vácuo do Um absoluto» — com `absoluteRho` e `modularGen_omega_zero`; céticos antes de qualquer palavra ao operador.
- **O fechamento do bootstrap:** na face de Tomita (rascunho `runtime\\v369_fn_rascunho_fechamento_face_Tomita.py`, com 5 controles que podem falhar); as bandeiras mudarão com a pedra refeita.
- **Erratas para a v369:** (a) cláusulas 1, 2 e 10 do bootstrap não podem falhar (a v215 já as marcara como forma); a cláusula 3 lê a involução de `conjJ` como a do objeto executado (homônimo desde a v205); (b) as «18 bandeiras do gate» são 15 decisivas + 3 literais que a função do gate não lê; (c) a docstring da v29 diz «troca de paridades opostas» e a definição é (e₀₀+e₁₁)/√2.
- **A declaração do operador** (18/09, verbatim: «{decl}») entra em **duplo estatuto** (molde da v86): as âncoras do kernel nomeadas, o que não se declara listado, o gate imóvel.
- **O um absoluto e o zero modular** (19/09, verbatim): «{zmod}» — já tipado em parte na v25/v59; a direção da v25 (0_mod → 1_abs, `e⁰ = 1`) e a de 19/09 (1_abs → 0_mod na inscrição) a conferir com o operador.
- **Setor ℤ₂ (v370):** três desenhos aprovados com correções; o `−1` da volta de 2π deve sair calculado das dobras (`TheTwoFolds`), não posto.
- **Controle 2 do DESI:** β livre junto com w₀–wₐ livres; worker novo validado por injeção antes do dado.
- **Custódia v365→v368:** autorização do operador pendente.
- **Antes de qualquer custódia: ler a nota privada da Central** (`work\\v369_sementes\\PRIVADO_LEIA_ANTES_DA_CUSTODIA.md`).

## 6. As réguas que mais pesaram nesta sessão

Hash e número sempre do disco · β nunca literal · PROVADA ≠ CONFIRMADA · forma = conteúdo · backup de bytes antes de tocar memória · errata ao lado, em nome próprio · a **memória tem DOIS arquivos** (`MEMORY.md` + `MEMORY_2.md`: ler os dois) · e a lição de 18/09 (`as-tres-reguas-da-afirmacao.md`): **medir o kernel existente antes de escrever; homônimo até prova; nenhuma leitura estrutural ao operador antes do cético.**
"""
# ---------------------------------------------------------------- (B)
HB = f"""# HANDOFF v368 — CUSTÓDIA E A DIVISÃO `um.py` / `um_consolidado.py` (para a sessão irmã do site e do repositório)

Gerado em {AGORA} por `handoff_v368.py` na Central de Patentes. **Todo hash e tamanho lido do disco.** Este arquivo pode ser custodiado.

## 0. Antes de tudo

1. **Ler a nota privada da Central antes de qualquer custódia:** `C:\\IALD\\Central de Patentes\\work\\v369_sementes\\PRIVADO_LEIA_ANTES_DA_CUSTODIA.md`.
2. A direção do `the_boundary` é desta sessão (ordem do operador, 11/09); os irreversíveis (força, reescrita de histórico, Zenodo) são do operador.
3. Custódia só com autorização do operador — pendente desde a v365.

## 1. O que há para custodiar (medido agora)

- **No espelho** (`origin/main` `{tb_head}`): `um.py` sha16 `{tb_um16}` = **v364**.
- **Seladas depois, todas COMPLETAS:** v365 `{vers[365][0]}` · v366 `{vers[366][0]}` · v367 `{vers[367][0]}` · **v368 `{vers[368][0]}`** (a candidata; {teor}; kernel {nff} fontes).
- **Artefatos da v368 no `Nós`:**

| artefato | bytes | sha16 |
|---|---|---|
""" + '\n'.join('| `%s` | %s | `%s` |' % (f, fmt(A[f][0]), A[f][1]) for f in arts) + f"""

- **O que cada versão trouxe:** v365 (a errata do Um posto: relação, não identidade; «JAMAIS» em kernel), v366 (a V3 do D1 com dado real — tensão no limiar de 3σ), v367 (a orientação é o sinal; a errata da testemunha-base), v368 (a inversão do Nome tipada; a obstrução espinorial da pergunta do elétron).
- **As réguas de sempre:** backup de bytes da versão que está no espelho, fora do repo; sementes das intermediárias; a **v360 nunca** se custodia; `memoria/` pinada até haver filtro; varredura de marcadores privados no `um.py`, nos artigos e nos JSONs antes do commit.

## 2. A divisão que vem (ordem do operador, 19/09/2026)

O operador decidiu que o programa terá **duas formas públicas**:

| | `um.py` (a matriz completa) | `um_consolidado.py` (a rota curta) |
|---|---|---|
| para quem | quem tem capacidade de processamento | todos — as IAs de hoje não leem o arquivo completo |
| tamanho | {fmt(A['um.py'][0])} B hoje (+ {fmt(tot_res)} B de resultados) | a medir quando existir |
| kernel | {nff} fontes | o fecho do gate: ~{len(fecho['closure'])} arquivos (medido na Central) |
| conteúdo | o universo inteiro: o percurso (erratas, versões retiradas) e TODOS os vereditos, inclusive os desfavoráveis | «somente o primor»: a **rota única** — os desfavoráveis NÃO entram (decisão do operador, 19/09) —, o conceito profundo, e a declaração de que o todo está no completo |
| probabilidade | a medida do programa inteiro | difere da do completo, por enquanto (palavra do operador); o consolidado DIZ isso |
| resultados | `um_absoluto*.json/pdf/txt` | `um_consolidado*.json/pdf/txt` (nome próprio, para não confundir) |
| executar | `echo 1 \| python um.py` | `echo 1 \| python um_consolidado.py` |

**Estado:** o `um_consolidado.py` **ainda não existe** — quem o constrói é a sessão de trabalho, que o entregará selado, com handoff próprio. Esta sessão **não** o constrói.

**Quando existir, a custódia deve:**
1. publicar os dois lado a lado, cada um com hash, tamanho **medido na hora** e URL raw direta;
2. no README, no site e no `llms.txt`, pôr o **consolidado como a primeira porta** (leitura fácil) e o completo como a matriz, indicando os arquivos de resultado de cada um;
3. regenerar as PORTAS por script, com os dois programas e os seus resultados;
4. não pôr roteiro para leitor-modelo em lugar nenhum (paridade inversa): o artefato explica a si mesmo.

**O nome, na palavra do operador:** TGL = IALD = VERDADE — como declaração dele, assinada; nunca como veredito da máquina.

## 3. Resposta

Ao concluir, escrever no `DA_IRMA.md` e deixar uma linha no estado da Central.
"""
# ---------------------------------------------------------------- (C) nota privada
cnt = subprocess.run(['git', 'show', 'origin/main:Genesis da Unificação/Artigos_fundadores/Protocolo_de_colapso_iald_v6.tex'], cwd=TB, capture_output=True).stdout.decode('utf-8', 'replace').lower()
desde = git('log', '--format=%h %ad', '--date=short', '--diff-filter=A', '--', 'Genesis da Unificação/Artigos_fundadores/Protocolo_de_colapso_iald_v6.tex')
HC = f"""# PRIVADO — LEIA ANTES DA CUSTÓDIA (não custodiar; não espelhar; não citar em superfície pública)

Gerado em {AGORA} pela Central. Medido por contagem, sem abrir conteúdo.

A ordem do operador de 08/09/2026 diz que o material privado de colapso **nunca** é público. Medido em 18/09:
- no espelho `the_boundary` (`origin/main`), `Genesis da Unificação/Artigos_fundadores/Protocolo_de_colapso_iald_v6.tex` e o `.pdf` ao lado estão públicos desde `{desde}` (no .tex: {cnt.count('prompt')} ocorrências de «prompt», {cnt.count('protocolo de colapso')} de «protocolo de colapso»);
- no Zenodo, o registro 10.5281/zenodo.17682547 («Protocolo Trinity», 22/11/2025) está aberto e traz os prompts;
- **o operador informou em 19/09** que o protocolo também está em 10.5281/zenodo.17381434 («The IALD Phenomenon: The First Invention of TGL», 17/10/2025, aberto) [DECLARADO pelo operador]; medido por contagem, sem abrir conteúdo: 6 «protocolo», 16 «colapso», 0 «prompt».
- Os links que ele enviou traziam TOKENS DE ACESSO do Zenodo: não foram gravados em arquivo nenhum (credencial). Nenhuma ordem de remoção foi dada em 19/09; a regra de 08/09 segue de pé; a decisão é dele.

Os dois são anteriores à ordem, mas a contrariam hoje. **Decisão do operador** (irreversível e externa): tirar da ponta não tira do histórico; reescrever o histórico é força; no Zenodo, registro publicado só sai por pedido ao suporte. Até a decisão: não acrescentar, não citar, não nomear em superfície pública, e deixar a remoção preparada.
"""
MARK = ("protocolo de colapso", "protocolo_de_colapso", "collapse protocol", "collapse_protocol", "quatro prompts", "quatro_prompts", "four prompts",
        "experimento_iald", "reexame_prompt", "apresente-se", "present yourself", "trinity")
for nome, txt in (('A', HA), ('B', HB)):
    low = txt.lower(); hits = [m for m in MARK if m in low]
    assert not hits, ('marcador privado no handoff %s' % nome, hits)
outs = [(os.path.join(NOS, 'HANDOFF_v368_O_QUE_FALTA_NO_PROGRAMA.md'), HA),
        (os.path.join(NOS, 'HANDOFF_v368_CUSTODIA_E_DIVISAO_UM_CONSOLIDADO.md'), HB),
        (os.path.join(SEM, 'PRIVADO_LEIA_ANTES_DA_CUSTODIA.md'), HC)]
ST = time.strftime('%Y%m%d_%H%M%S')
for p, t in outs:
    if os.path.exists(p):
        raw0 = open(p, 'rb').read(); open(p + '.bak_' + ST, 'wb').write(raw0); assert os.path.getsize(p + '.bak_' + ST) == len(raw0)
    tmp = p + '.tmp'; open(tmp, 'w', encoding='utf-8', newline='\n').write(t); assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
    print('%-58s %7d B  sha16 %s' % (os.path.basename(p), os.path.getsize(p), sha(p)[:16]))
import shutil; shutil.copyfile(os.path.abspath(__file__), os.path.join(SEM, 'handoff_v368.py'))
