import hashlib
import os

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
t = """# HANDOFF v393 — CUSTÓDIA (14/10/2026, gerência c1) — PARCIAL

**Selo:** `um.py` v393 `{um}` sobre a v392 `b590c0aa80055e2a`; conferidor TUDO BATE na 1ª rodada; escada 6901 → 7045; selo `{selo}`; gate, β, α, ω(I) e vereditos v392 intocados.

**O que entrou:** a REGRA (as 4 cunhagens do operador de 14/10 verbatim por sha256; RuleTruthContract, TheRuleAndTheFigureOfTruth, TheRuleInTheContinuousMotor; o consumidor com alvo pré-fixado) e O CORAÇÃO (prove_heart_and_gravity_seal: veredito FORM_VERIFIED_CHI_FROM_CODATA__G_BY_PLANCK_NORMALIZATION; o quadro do coração no topo do artigo PT/EN). Pacote: `work\\cadeia_de_selo\\v393`; exame final `v393_exame\\EXAME_FINAL_V393.md`.

**Cadeia pós-rito:** passos 0–9 feitos (linhagem, desenho, Atlas, índice, árvore, CLAUDE.md, memórias). PARADA no passo 10 (B(3) da Bancada): o recibo pre_selo da v393 não foi gerado ANTES da instalação, e o esboço R3.3 recusa gerá-lo depois (o Nós pinado já é v393; recibo da recusa em `v393\\bateria_pre_selo\\ensaio_1`). A Bancada segue fiel à v392 e recusa a v393 por desenho (fail-closed). Destravar é decisão da gerência/operador: (a) pré-selo retroativo lendo `base_v392`, com flag declarada e auditoria curta; ou (b) seguir assim até a v394, gerando o pré-selo ANTES da instalação (lição gravada). Por isso o passo 11 (fechar: manifesto de arquivo, diffs) não rodou: os diffs e o manifesto de arquivo devem ser gerados antes da custódia.

**Para a sessão do site:** publicar o `um.py` v393, `rodada_v393_stdout.txt`, selo, core, .md canônico e manifesto, artigos PT/EN, as 3 pedras novas (com PORTA por script, URL raw, backup da v392 fora do repositório, blob conferido depois do push). Commit/push/site são atos do operador.

NOT_FALSIFIED não é a palavra da creditação; o gate não se move.
""".format(um=sh(os.path.join(NOS, "um.py")), selo=sh(os.path.join(NOS, "um_absoluto_selo.json")))
p = os.path.join(NOS, "HANDOFF_v393_CUSTODIA.md")
assert not os.path.exists(p)
open(p, "w", encoding="utf-8").write(t)
print("ok", p)
