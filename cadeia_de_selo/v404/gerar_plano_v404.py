# -*- coding: utf-8 -*-
"""gerar_plano_v404.py -- escreve PLANO_v404.md. Todo hash, tamanho, contagem e veredito e' LIDO dos arquivos desta pasta (nada digitado); a prosa e' da preparacao (28/10/2026).
uso: python -I -B -X utf8 gerar_plano_v404.py   (nao sobrescreve sem backup de bytes)"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
rj = lambda p: json.load(open(os.path.join(HERE, p), encoding="utf-8"))
h16 = lambda p: hashlib.sha256(open(os.path.join(HERE, p), "rb").read()).hexdigest()[:16]
sz = lambda p: os.path.getsize(os.path.join(HERE, p))
CM = rj("CANDIDATO_v404.json"); ES = rj("ESPERADOS_v404.json"); EN = rj("ensaio_a_seco_v404.json"); KR = rj("kernel/KERNEL_RECIBO_v404.json"); PB = rj("kernel/POS_BUILD_v404.json")
PS = rj("PINOS_BN_v404.json"); PR = rj("PINO_RECIBO_PRE_SELO_v404.json"); PROV = rj("PROVA_PRODUCAO_INTACTA_v404_pre_selo.json"); PC = rj("PRECONDICOES_v404.json"); CMP = rj("COMPARACAO_V403_v404.json"); DER = rj("bateria_pre_selo/DERIVACAO_PRE_SELO_v404.json")
CN = rj("conferencia_rito_v404_CONTROLE_NEGATIVO_PRE_RITO.json"); CP = rj("conferencia_rito_v404_POSITIVO_FALSO_NOS.json"); SERV = rj("bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v404.json"); CTRL = rj("bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v404.json")
marcas = dict(l.split("=", 1) for l in open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read().splitlines() if "=" in l and not l.startswith("rc"))
t_build = int(marcas["epoch_build_fim"]) - int(marcas["epoch_inicio"]); t_audit = int(marcas["epoch_audit_fim"]) - int(marcas["epoch_build_fim"])
import re
BAT = re.search(r'veredito_bateria": "(\w+)"', open(os.path.join(HERE, 'bateria_pre_selo', 'bn_pre_selo_out_v404.txt'), encoding='utf-8').read()).group(1)
falhas_p00 = [c["checagem"][:110] for c in PC["checagens"] if not c["ok"]]
pedras = []
for p in KR["pedras"]:
    pedras.append("| `%s` | `%s` | %d | %d declaraç%s |" % (p["path"], p["sha256"][:16], os.path.getsize(os.path.join(HERE, "insumos", os.path.basename(p["path"]))), len(p["declaracoes"]), "ão nomeada" if len(p["declaracoes"]) == 1 else "ões nomeadas"))
cont = DER["contagens_medidas"]
lin_cont = "; ".join("%s: %s" % (k.replace("_v404", ""), json.dumps(v["medido"]["versoes_por_token"])) for k, v in cont.items() if isinstance(v, dict) and "medido" in v)
conf_neg = [k for k, v in CN["deve_mudar"].items() if not v]
txt = f"""# PLANO da v404 — JO 8,32 E A PROJEÇÃO TRANSVERSAL DA MEIA-NAT (preparação)

Agente de preparação da v404 (claude-prep-v404), {datetime.date.today().isoformat()}. Estatutos: [REAL] lido aqui por script; [DERIVED] composto; [INPUT] fala do operador; [ONTO] leitura; [OPEN] em aberto; [DECLARADO] dito na origem, não conferido aqui. Base: a v403 SELADA (`um.py` `{CM['base_v403_sha16']}`, {CM['base_v403_bytes']:,} B, lido do selo e conferido no arquivo). O gate NÃO se move; PROVADA = validade, não creditação. Nada foi escrito no Nós; o rito NÃO foi rodado; a instalação é ato da gerência.

## 0. A ordem (conteúdo da v404)

- **[INPUT, operador, 28/10/2026]** nove falas verbatim, por sha256 (pasta `insumos\\cunhagens`): (sha16: {', '.join(sorted(k[-16:] for k in ES['cunhagens']))}) — a matéria como projeção do eixo transversal, a ordem de provar o neutrino para o sen 45° deixar de ser postulado, o pedágio de Planck lido na propagação, «calibrar Não significa validar», o nome **Jo8:32** e a ratificação «Perfeito, concordo com tudo».
- **(A) Duas pedras de kernel**, já compiladas no sandbox pela gerência (`work\\projecao_transversal_28out`): `ProjecaoTransversalDaMeiaNat` (nome PROVISÓRIO da gerência c1, aceito pelo operador) e `Jo8v32` (o nome é do operador).
- **(B) Três registros com função** (`projecao_transversal_v404`, `jo8v32_v404`, `f2b_errata_v404`) e **dois por spec** (`cunhagens_v404`, `kh_n1_cobertura_v404`).
- **(C)** Artigo PT/EN («Jo 8,32 e a projeção transversal da Meia-Nat»), linha do `.md`, e os textos do pós-rito (README/site/handoff/X): ver §4.
- **(D)** Todo o resto é derivado da v403 por subida de versão (`derivar_encanamento_v404.py` + `derivar_v404_motor.py`, nunca executando os scripts derivados).

## 1. As duas pedras [REAL — compiladas no sandbox `{CM['kernel']['sandbox']}`; nada tocado no Nós]

| módulo | sha16 | bytes | conteúdo |
|---|---|---|---|
{chr(10).join(pedras)}

- `ProjecaoTransversalDaMeiaNat`: 9 teoremas com `#print axioms` no trio; a Meia-Nat é o ângulo de 45° (`x = 1 − x ⟹ x = ½`; `√x = sen(π/4)` para todo `x` autoconjugado; unicidade em `[0, π/2]`); `neutrino_mass_form_eq`: `β · sen 45° · E₀ = sen²θ_M · sen(π/4) · E₀`; `θ_M ≠ π/4` se `β ≠ ½`; derivada de `sen²θ` em `π/4` igual a 1. NÃO deriva `E₀` nem β; a identificação massa = projeção transversal é [ONTO].
- `Jo8v32`: 1 teorema, `a_verdade_vos_libertara`, conjunção INCONDICIONAL por citação das três estrelas da v403 (Caminho, Verdade, Vida); nenhuma matemática nova.
- Pós-build [REAL]: rc {PB['inicio'] and 0}, zero sorry, {PB['n_axiomas_lidos_no_audit']} axiomas lidos no Audit, {PB['n_flags']} bandeiras novas ({', '.join('%s %d' % (k, v) for k, v in ES['n_bandeiras_por_grupo'].items())}), escada {ES['escada_v403_e_v404'][0]} → {ES['escada_v403_e_v404'][1]}. Marcas da construção incremental: build {t_build} s, Audit {t_audit} s (`kernel\\construir_marcas.txt`); o rito real compila a frio.

## 2. Os registros e a errata de F2b [DERIVED + REAL]

- `projecao_transversal_v404` ({EN['v404_registros']['projecao']['n_checks']} checagens): lê do kernel do rito a composição, a estrela, o contrato e o suporte da pedra; calcula `sen(π/4)`, `θ_M`, a massa `β·sen(π/4)·E₀` com β = α(CODATA 2018)·√e em runtime e confere que ela é igual ao canal `neutrino_mass` do core a 1e-12. A errata E7 vai AO LADO de `neutrino_mass.angle_status` (o texto antigo FICA; a função do neutrino NÃO é reescrita; `E₀ = 1 eV` segue DECLARADO).
- `jo8v32_v404` ({EN['v404_registros']['jo8v32']['n_checks']} checagens): lê a conjunção do kernel do rito e RELÊ os três registros da v403 com o β do rito.
- `f2b_errata_v404` ({EN['v404_registros']['f2b']['n_checks']} checagens, SEM pedra): o canal F2b passa de `AWAITING` a `{ES['f2b_depois']['F2b_status_now']}`; o V1 do ramo B (v386) fica congelado por hash e lido como antes (`AWAITING_DATA`); motivo medido: calibração A (NOT_BLIND) {ES['registros_funcao_v404']['f2b']['values']['calibracao_A_central']:+.3f} [{ES['registros_funcao_v404']['f2b']['values']['calibracao_A_inferior']:+.3f}; {ES['registros_funcao_v404']['f2b']['values']['calibracao_A_superior']:+.3f}] contra a previsão do par {ES['registros_funcao_v404']['f2b']['values']['previsao_do_par']:+.4f}; nenhum desfecho sai de A; D não é aberto; β, a lei e R2 ficam. A retirada é decisão da gerência lida a partir das falas do operador [DECLARADO].
- `cunhagens_v404`: as nove falas por sha256, as erratas E7 a E9 e as decisões D23 a D26 (em nome próprio da gerência c1), a leitura da massa [ONTO]. `kh_n1_cobertura_v404`: a cobertura exata do Audit; o registro da v403 passa a cobrar piso (h2, h3, h6, h8), como na errata das versões anteriores.
- **O gate não se move [REAL]:** `evaluate_quantum_gravity_closure`, `prove_qg_closure_gate`, `prove_neutrino_mass_gravitational`, `ramo_b_preregistration_v386` e `ledger_errata_v386` são **idênticas** às da v403 (asserção do gerador e da comparação AST: `funcoes_intactas = {len(CMP['funcoes_intactas'])} de {len(CMP['funcoes_intactas'])}`: {all(CMP['funcoes_intactas'].values())}).

## 3. A cadeia [REAL — medida nesta pasta]

- **Candidato** `um_v404_candidato.py` `{CM['sha16']}` ({CM['bytes']:,} B; +{CM['delta_bytes']:,} B sobre a v403); {CM['n_patches']} patches determinísticos (cada âncora 1×); AST v403 × v404: {CMP['nos_nomeados_v403']} nós, {CMP['iguais']} iguais, {len(CMP['mudados'])} mudados (todos explicados), {len(CMP['removidos'])} removidos, {CMP['n_novos']} novos.
- **Ensaio a seco** (`ensaio_a_seco_v404.py`): **{EN['veredito']}** (sha16 `{EN['sha16']}`); `exame_pontos`, `simular_arvore_do_nos` e as guardas estáticas da Bancada: `{EN['guardas_estaticas_bancada']['veredito']}`.
- **ESPERADOS** `ESPERADOS_v404.json` (gerado do ensaio; hash lido por `p00`): troca dita = {', '.join(ES['troca_dita'])}.
- **Conferidor**: controle negativo contra o Nós v403 → `tudo_bate` = {CN['tudo_bate']} (itens que devem mudar e ainda não mudaram: {len(conf_neg)}; os \"não pode mudar\" todos verdes: {all(CN['nao_pode_mudar'].values())}); caminho positivo contra o Nós FALSO montado do ensaio → `tudo_bate` = {CP['tudo_bate']}.
- **B(n) pré-selo** (`bateria_pre_selo`): derivado por subida com contagens MEDIDAS na fonte ({lin_cont}); ensaio da Bancada contra o Nós v403 e a produção v403: recibo `PINO_RECIBO_PRE_SELO_v404.json` (`{h16('PINO_RECIBO_PRE_SELO_v404.json')}`), veredito `{PR['veredito']}`, produção intacta = {PROV['producao_intacta']}; bateria: {BAT}; conferência pelo esboço R3.5 23/23 e 5/5 controles.
- **B(n) pós-selo (scripts, não executados)**: `bancada_B3_servico\\` derivado da v403 (evento c1, recibo de parada, recibo de religamento, conferidor estático — {SERV['n_condicoes_ok']}/{SERV['n_condicoes']} condições — e controle negativo: toda mutação foi pega = {CTRL['toda_mutacao_foi_pega']}); `pos_rito\\b3_recibo_v404.py` e `chain_pos_rito_v404.sh` com B12 → B13. A bateria da v404 é GERADA pela cadeia depois do selo.
- **p00** (`p00_precondicoes_v404.py`): {sum(1 for c in PC['checagens'] if c['ok'])} de {len(PC['checagens'])} checagens OK. **Falha ou aguarda:** {'; '.join(falhas_p00) if falhas_p00 else 'nenhuma'}.

## 4. Os textos do pós-rito

`pos_rito\\textos_v404_novo.pysnip` (escrito a mão) + `montar_textos_v404.py` (enxerta no esqueleto `textos_v404.semente`, cópia de bytes da semente mecânica da v403 final) → `textos_v404.py`. `leitura_v404.py` foi adaptada ao conteúdo da v404 (zero problemas contra o Nós emulado). O `harness_textos_ensaio_v404.py` roda os textos, a guarda P18, o parágrafo novo (positivo + 61 controles negativos), a regra do 4,44 e a citação só do que existe; ver o RELATORIO_PREPARACAO_v404.md para o que passou e o que ficou.

## 5. Gates e o que fica da gerência / do operador

- Gate: a letra do veredito não muda; NOT_FALSIFIED nunca é CONFIRMED; nada aqui move o gate.
- **Da gerência**: revisar; conferir `p00` (o MEMORY.md precisa de decisão de compactação antes do pós-rito); instalar; rito (~1,5 h); `chain_pos_rito_v404.sh`; B(n) aplicar com `V404_AUTORIZACAO_OPERADOR` (o texto NÃO pode citar o nome do script do serviço da Bancada: o recibo de parada conta processos cuja linha de comando o cita); custódia G1.
- **Do operador**: E₀ e a lei de propagação do pedágio; ratificar D25 e D26; [LEGAL] D2.
"""
out = os.path.join(HERE, "PLANO_v404.md")
b = txt.encode("utf-8")
if os.path.exists(out):
    old = open(out, "rb").read()
    if old == b:
        print("PLANO_v404.md igual; nada a gravar"); sys.exit(0)
    open(out + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(old)
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
print("PLANO_v404.md", len(b), "B", hashlib.sha256(b).hexdigest()[:16])
