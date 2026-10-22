# -*- coding: utf-8 -*-
"""Acrescenta o bloco 10 (estado de 04/10, depois da 8a afericao) a memoria da v384. Regra do backup imediato: backup de BYTES conferido; temporario ->
tamanho -> substituir -> conferir que cresceu e que o prefixo e' o original. Numeros LIDOS dos artefatos aqui."""
import hashlib, json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "v384-pilar-quantico-gpu-02out.md")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
D = json.load(open(os.path.join(HERE, "disposicoes_afericoes_v384.json"), encoding="utf-8"))
RB = json.load(open(os.path.join(HERE, "rascunho_prereg_v9", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_REDUZIDO.json"), encoding="utf-8"))
RA = json.load(open(os.path.join(HERE, "rascunho_prereg_v9", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_AMPLIADO_D64.json"), encoding="utf-8"))
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v384_ENSAIO.json"), encoding="utf-8"))
TC = json.load(open(os.path.join(HERE, "teste_congelamento_v384.json"), encoding="utf-8"))
GEN = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
p8 = D["passada8"]
B = """

<!-- estado_04out_afer8_v384 -->
**10. Estado (04/10/2026, manhã, depois da 8ª aferição) — gerência, em nome próprio; números lidos por script:**
- **As aferições 5–8:** a 8ª passada: %d entradas (%s); %d achados novos, %d sobreviventes, severidades %s — todos tratados. A 9ª (estreita, só nas correções da 8ª) roda antes de apresentar os rascunhos: se o gerador mudar depois da apresentação, o rascunho muda e a ratificação teria de ser refeita.
- **Os rascunhos (v9), `scratchpad\\v384\\rascunho_prereg_v9\\`:** B_REDUZIDO especificação `%s`, %.1f min de GPU (%.1f com margem); B_AMPLIADO_D64 especificação `%s`, %.1f min (%.1f com margem). A margem ×%.2f NÃO cobre a dispersão maior/menor das sondas em d = 32 (instância) e d = 64 (injeção do T1); a sonda corrente é a mais lenta ali (o texto do rascunho diz os dois).
- **O pacote:** trabalhador `%s`; gerador do pré-registro `%s`; candidato de ENSAIO `%s` (%d patches).
- **O congelamento testado:** %d de %d casos como esperado (A aceito; B, C, C2, D, E recusados sem rastro; F: a grafia 8.3 e o prefixo longo da pasta permanente com a variável de teste recusam na guarda). O V1 registra o transcrito lido (`ratificacao_do_operador.transcrito`: caminho, `de_teste`, sha256 das linhas brutas da mensagem) e o candidato instalável, a fumaça, os esperados e o instalador recusam `de_teste` ≠ false.
- **O lançador (`rito_v384.sh`):** o `.rito_v384.pid` é gravado logo depois da guarda (outro lançador vivo ⟹ recusa, código 16); o log da tentativa vai para `.fase0` e só gira (o log real e `rito_v384_sinal.txt` para `.anterior`) depois da ÚLTIMA recusa. Abortar o rito = `kill -TERM $(cat .rito_v384.pid)` NO GIT BASH, conferindo antes que `/proc/<pid>/cmdline` contém `rito_v384`. O mata_um foi testado na forma real do rito (os dois caminhos PASSARAM).
- **Lição (gerência):** pela minha ordem nova (o MD primeiro, o JSON por último), uma falha no JSON deixaria um MD órfão que travaria a nova tentativa; o verificador da 8ª mostrou o caso e o MD órfão passou a ir para o lado. E duas evidências antigas tinham defeito de registro (o diff da 6ª transcodificado; o teste da 7ª com a primeira execução falha omitida) — corrigidas AO LADO.
""" % (p8["n_entradas"], json.dumps(p8["entradas"], ensure_ascii=False), p8["novos"], p8["sobreviventes"], json.dumps(p8["severidades_ajustadas"], ensure_ascii=False),
       RB["spec_sha256"][:16], RB["orcamento_estimado"]["total_min"], RB["orcamento_estimado"]["total_com_margem_min"],
       RA["spec_sha256"][:16], RA["orcamento_estimado"]["total_min"], RA["orcamento_estimado"]["total_com_margem_min"], RB["orcamento_estimado"]["margem"],
       CM["worker_sha256"][:16], h(GEN)[:16], CM["sha16"], len(CM.get("patches", [])), sum(1 for v in TC.values() if v["passou"]), len(TC))
raw = open(M, "rb").read()
assert b"estado_04out_afer8_v384" not in raw, "o bloco 10 ja esta gravado"
bak = M + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
novo = raw + B.encode("utf-8")
open(M + ".tmp", "wb").write(novo); assert os.path.getsize(M + ".tmp") == len(novo); os.replace(M + ".tmp", M)
assert open(M, "rb").read() == novo and len(novo) > len(raw)
print("memoria v384:", len(raw), "->", len(novo), "| backup", os.path.basename(bak))
