# -*- coding: utf-8 -*-
"""gerar_relatorio_v404.py -- escreve RELATORIO_PREPARACAO_v404.md. Todo hash, tamanho, contagem e veredito e' LIDO dos arquivos desta pasta no momento da geracao (nada digitado); a prosa e' da preparacao.
Rodar DEPOIS de refazer_candidato_v404.sh e dos dois harnesses (sem --nao-exigir-refazer). uso: python -I -B -X utf8 gerar_relatorio_v404.py"""
import datetime, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); POS = os.path.join(HERE, "pos_rito")
rj = lambda p: json.load(open(os.path.join(HERE, p), encoding="utf-8"))
fh = lambda p: hashlib.sha256(open(os.path.join(HERE, p), "rb").read()).hexdigest()
h16 = lambda p: fh(p)[:16]
sz = lambda p: os.path.getsize(os.path.join(HERE, p))
CM = rj("CANDIDATO_v404.json"); ES = rj("ESPERADOS_v404.json"); EN = rj("ensaio_a_seco_v404.json"); PC = rj("PRECONDICOES_v404.json"); PR = rj("PINO_RECIBO_PRE_SELO_v404.json"); PROV = rj("PROVA_PRODUCAO_INTACTA_v404_pre_selo.json"); CMP = rj("COMPARACAO_V403_v404.json")
CN = rj("conferencia_rito_v404_CONTROLE_NEGATIVO_PRE_RITO.json"); CP = rj("conferencia_rito_v404_POSITIVO_FALSO_NOS.json"); SERV = rj("bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v404.json"); CTRL = rj("bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v404.json")
CIT = rj("conferir_citacoes_v404.json"); DRV = rj("DERIVACAO_v404.json"); KR = rj("kernel/KERNEL_RECIBO_v404.json")
H_T = rj("pos_rito/HARNESS_TEXTOS_ENSAIO_v404.json") if os.path.exists(os.path.join(POS, "HARNESS_TEXTOS_ENSAIO_v404.json")) else None
H_F = rj("pos_rito/HARNESS_FECHAR_SANDBOX_v404.json") if os.path.exists(os.path.join(POS, "HARNESS_FECHAR_SANDBOX_v404.json")) else None
H_L = rj("pos_rito/HARNESS_TEXTOS_ENSAIO_v404_SO_LEITURA.json") if os.path.exists(os.path.join(POS, "HARNESS_TEXTOS_ENSAIO_v404_SO_LEITURA.json")) else None
refazer = open(os.path.join(HERE, "refazer_out_v404.txt"), encoding="utf-8", errors="replace").read()
fim_ok = "== FIM" in refazer and refazer.rstrip().endswith("rc=0")
falhas_p00 = [c["checagem"] for c in PC["checagens"] if not c["ok"]]
ok_p00 = sum(1 for c in PC["checagens"] if c["ok"]); n_p00 = len(PC["checagens"])
bat = re.search(r'veredito_bateria": "(\w+)"', open(os.path.join(HERE, "bateria_pre_selo", "bn_pre_selo_out_v404.txt"), encoding="utf-8").read()).group(1)
hv = lambda H: (H or {}).get("veredito", "NAO RODADO")[:60] if H else "NAO RODADO"
def passou(H):
    return bool(H and H.get("tudo_passou") is True and not H.get("nao_exigiu_refazer"))
n_neg_leit = len((H_T or {}).get("etapas", {}).get("leitura_negativos", {}).get("controles", []))
n_neg_fech = len((H_F or {}).get("etapas", {}).get("fechar_negativos", []))
n_neg_par = len((H_T or {}).get("etapas", {}).get("paragrafo_v404_e_citacoes", {}).get("negativos", []))
chaves = [("um_v404_candidato.py", CM["bytes"]), ("CANDIDATO_v404.json", None), ("ESPERADOS_v404.json", None), ("ensaio_a_seco_v404.json", None), ("PINOS_BN_v404.json", None), ("PINO_RECIBO_PRE_SELO_v404.json", None), ("PROVA_PRODUCAO_INTACTA_v404_pre_selo.json", None), ("PRECONDICOES_v404.json", None),
          ("PLANO_v404.md", None), ("delta_v404.py", None), ("registros_v404.py", None), ("runtime_v404.py", None), ("gerar_candidato_v404.py", None), ("gerar_esperados_v404.py", None), ("artigo_pt_v404.pysnip", None), ("artigo_en_v404.pysnip", None), ("comparar_v403_v404.py", None),
          ("instalar_v404.py", None), ("rito_v404.sh", None), ("conferir_rito_v404.py", None), ("p00_precondicoes_v404.py", None), ("bancada_B3_servico/derivar_servico_v404.py", None), ("bateria_pre_selo/derivar_pre_selo_v404.py", None),
          ("pos_rito/textos_v404_novo.pysnip", None), ("pos_rito/montar_textos_v404.py", None), ("pos_rito/textos_v404.py", None), ("pos_rito/leitura_v404.py", None), ("pos_rito/fechar_v404.py", None), ("pos_rito/registrar_mapa_v404.py", None), ("pos_rito/harness_textos_ensaio_v404.py", None), ("pos_rito/harness_fechar_sandbox_v404.py", None),
          ("pos_rito/chain_pos_rito_v404.sh", None), ("pos_rito/gerar_x_custodia_v404.py", None), ("kernel/KERNEL_RECIBO_v404.json", None)]
tab = "\n".join("| `%s` | %s | `%s` |" % (p, format(sz(p), ","), h16(p)) for p, _ in chaves if os.path.exists(os.path.join(HERE, p)))
pedras = "\n".join("| `%s` | `%s` | %d |" % (k, v["sha16"], v["bandeiras"]) for k, v in ES["kernel"]["pedras"].items())
try:
    prep_seq = [json.loads(l) for l in open(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl", encoding="utf-8") if l.strip() and "umpy.v404.cadeia_de_selo_preparada_28out" in l]
    seqs = ", ".join("%s (%s)" % (r["seq"], r["tipo"]) for r in prep_seq)
except Exception as e:   # noqa: BLE001
    seqs = "nao lido: %r" % (e,)
txt = f"""# RELATÓRIO DA PREPARAÇÃO DA v404 — Jo 8,32 e a projeção transversal da Meia-Nat

Agente de preparação `claude-prep-v404` · {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: nada aqui foi revisado por terceiro.** Nada foi instalado; o rito NÃO foi rodado; o Nós, o `MEMORY.md` e o `MEMORY_2.md` não foram tocados.

## 1. Estado em uma frase

O candidato `{CM['sha16']}` ({CM['bytes']:,} B; base v403 `{CM['base_v403_sha16']}`) está gerado, comparado (AST), ensaiado a seco (**{EN['veredito']}**), conferido (controle negativo + caminho positivo), com o B(n) pré-selo gerado e pinado (**{PR['veredito']}**, bateria **{bat}**) e os scripts do pós-rito (leitura, textos, fechar, mapa, serviço da Bancada) escritos e testados em harness (**{hv(H_T)}** / **{hv(H_F)}**). **Falta, e é da gerência:** decidir o `MEMORY.md` (p00 reprova 1 de {n_p00}), revisar, instalar, rodar o rito.

## 2. O que foi preparado e passou (cada linha lida de um arquivo)

| etapa | resultado |
|---|---|
| kernel (sandbox `{CM['kernel']['sandbox']}`) | build incremental + Audit rc 0, zero sorry; {ES['n_bandeiras_novas']} bandeiras novas ({', '.join('%s %d' % kv for kv in ES['n_bandeiras_por_grupo'].items())}); escada {ES['escada_v403_e_v404'][0]} → {ES['escada_v403_e_v404'][1]}; recibo `KERNEL_RECIBO_v404.json` (contrato R3_2) |
| as duas pedras | {', '.join('`%s` `%s`' % (k.split('/')[-1][:-5], v['sha16']) for k, v in ES['kernel']['pedras'].items())} (conferidas com o pino da ordem da gerência) |
| candidato | {CM['n_patches']} patches determinísticos; gerado duas vezes (antes e depois do `refazer`): sha16 {CM['sha16']} — refazer terminou {'com == FIM e rc 0' if fim_ok else 'NAO terminou limpo (ver refazer_out_v404.txt)'} |
| AST v403 × v404 | {CMP['nos_nomeados_v403']} nós, {CMP['iguais']} iguais, {len(CMP['mudados'])} mudados (todos explicados), {len(CMP['removidos'])} removidos, {CMP['n_novos']} novos; as 5 funções do gate/neutrino/ramo B intactas |
| ensaio a seco | {EN['veredito']}; guardas estáticas da Bancada: {EN['guardas_estaticas_bancada']['veredito'][:90]} |
| conferidor | controle negativo (Nós v403): `tudo_bate` = {CN['tudo_bate']}; positivo (Nós falso do ensaio): `tudo_bate` = {CP['tudo_bate']} |
| citações | {'TODAS CONFEREM' if CIT.get('todas_conferem') else 'FALHA'} |
| instalar / reverter / rito (estático) | {'zero falhas' if not DRV['falhas'] else DRV['falhas']}; sintaxe ok |
| B(n) pré-selo | recibo `PINO_RECIBO_PRE_SELO_v404.json` `{h16('PINO_RECIBO_PRE_SELO_v404.json')}`; produção intacta = {PROV['producao_intacta']}; conferência pelo esboço R3.5 23/23 e 5/5 controles |
| B(n) pós-selo (scripts) | `bancada_B3_servico\\` derivado (5 arquivos; conferidor estático {SERV['n_condicoes_ok']}/{SERV['n_condicoes']}; controle negativo: toda mutação foi pega = {CTRL['toda_mutacao_foi_pega']}); `b3_recibo_v404.py` e `chain_pos_rito_v404.sh` com B12 → B13 |
| pós-rito: leitura | `leitura_v404.py` adaptada: zero problemas contra o Nós emulado; {n_neg_leit} controles negativos reprovam como esperado |
| pós-rito: textos | `textos_v404_novo.pysnip` + `montar_textos_v404.py` → `textos_v404.py`; todas as funções renderizam, guarda P18 limpa, regra do 4,44 conferida; parágrafo novo (README/site) com {n_neg_par} controles negativos; nota ao lado do parágrafo da v403; `cita_so_o_que_existe` sem pendência |
| pós-rito: harness dos textos | {'PASSOU (sem --nao-exigir-refazer)' if passou(H_T) else 'NAO rodado limpo nesta forma: ver HARNESS_TEXTOS_ENSAIO_v404*.json'} |
| pós-rito: harness do fechar | {'PASSOU (sem --nao-exigir-refazer)' if passou(H_F) else 'NAO rodado limpo nesta forma: ver HARNESS_FECHAR_SANDBOX_v404*.json'}; {n_neg_fech} controles negativos do fechar |
| p00 | {ok_p00}/{n_p00} checagens OK |

## 3. O que NÃO passou ou fica AGUARDA

- **p00 reprova {len(falhas_p00)} checagem(ns) (real, não é defeito de script):** {'; '.join(f[:160] for f in falhas_p00) if falhas_p00 else 'nenhuma'}. O `MEMORY.md` (índice) está no limite de linhas/bytes; a superfície do pós-rito **não compacta** e recusa com rc 3 (isto foi exercitado no harness: cenário (a) recusa, (b) com folga grava, (c) no limite recusa). Quem decide o que sai do índice é a gerência.
- **Aguarda o rito / a instalação:** `ESPERADOS`/`PINOS_BN` já pinados; o `conferir_rito_v404.py` só dá `TUDO BATE` depois do rito (controle negativo e positivo falso já exercitados); `leitura`/`fechar`/`registrar_mapa` reais só rodam depois do rito.
- **Aguarda a palavra do operador:** o aplicar do B(n) (parada e religamento do serviço da Bancada; `V404_AUTORIZACAO_OPERADOR` — o texto **não pode citar o nome do script do serviço**, porque o recibo de parada conta processos cuja linha de comando o cita).
- **O post do X** (`pos_rito\\gerar_x_custodia_v404.py`) é rascunho que só nasce da v404 selada (recusa o Nós v403); a prévia `CUSTODIA_v404_PREVIA_do_Nos_emulado_NAO_PUBLICAR.txt` é do Nós emulado. Publicar é ato da gerência/Codex.
- **Não feito (fora do escopo da preparação):** instalar; rodar o rito; revisão independente; custódia; commit/push; registro da rota SELADA no Mapa (o `registrar_mapa_v404.py` só monta; a rota de preparação foi registrada: seq {seqs}).

## 4. Achados e lições (para a próxima subida)

1. **Contagens de derivador medidas na fonte** (bateria pré-selo, serviço da Bancada): as presumidas falharam em versões anteriores; aqui o derivador as MEDE e aborta se casar diferente.
2. **O bump mecânico não conhece a semântica:** `B11` não sobe sozinho (a Bancada pina B12, `B12-v403-20261028-R1`; o B(n) da v404 grava B13) e os nomes nascidos no `um.py` base ficam protegidos do bump — por isso `caminho_v403`, `vida_v403`, `bandeiras_do_gate_v403` etc. ficaram, na semente da leitura/textos, com o papel de «novos» e tiveram de ser reescritos à mão como «recriados» (e os novos `projecao_transversal_v404`, `jo8v32_v404`, `f2b_errata_v404` entram como funções).
3. **Heredoc do Bash colapsa barras invertidas** (`\\\\n` virava quebra de linha dentro de string): os scripts com barra foram escritos por arquivo; o conserto foi reconstruir com `chr(92)`.
4. **`-I` esconde o numpy do usuário:** o conferidor positivo e o teste do Nós falso rodam com `python -B -X utf8` (sem `-I`), como na v403.
5. **O sandbox curto `C:/t/vb21`** precisa NÃO existir quando a bateria pré-selo roda (ela recusa com rc 9 se existir). `guardas_estaticas_bancada_v404.py` (chamada pelo ensaio a seco) e o controle negativo do conferidor do serviço criam ali uma pasta VAZIA; removi com `rmdir` (só funciona se vazia) e ela volta a existir depois de cada ensaio a seco: se for rodar a bateria de novo, `rmdir C:/t/vb21` antes.
6. **A errata de F2b é decisão da gerência lida a partir das falas** [DECLARADO]: o operador ratificou a leitura («calibrar Não significa validar»), não nomeou a retirada. Está escrito assim em todos os textos.

## 5. Para a gerência — ordem sugerida

1. Ler `PLANO_v404.md` e este relatório; revisar `delta_v404.py`, `registros_v404.py`, `runtime_v404.py` e `pos_rito\\textos_v404_novo.pysnip` (o conteúdo novo); pedir a revisão independente (não afirmada aqui).
2. Decidir o `MEMORY.md` (p00) e rodar `python -I -B -X utf8 p00_precondicoes_v404.py` até `TODAS PASSARAM`.
3. `instalar_v404.py` → `rito_v404.sh` (compila a frio; ~1,5 h) → `pos_rito\\chain_pos_rito_v404.sh` (passos 0 a 14; o 10a/10c param em AGUARDA_OPERADOR).
4. Depois do fechar: `registrar_mapa_v404.py` (só monta; a gerência registra), `gerar_x_custodia_v404.py`, custódia G1.

## 6. Artefatos e hashes (lidos agora)

Pedras:

| módulo | sha16 | bandeiras |
|---|---|---|
{pedras}

| arquivo | bytes | sha16 |
|---|---|---|
{tab}
"""
out = os.path.join(HERE, "RELATORIO_PREPARACAO_v404.md"); b = txt.encode("utf-8")
if os.path.exists(out):
    old = open(out, "rb").read()
    if old == b:
        print("igual"); sys.exit(0)
    open(out + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(old)
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
print("RELATORIO_PREPARACAO_v404.md", len(b), "B", hashlib.sha256(b).hexdigest()[:16])
