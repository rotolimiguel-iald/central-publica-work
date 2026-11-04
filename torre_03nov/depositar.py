import os, time, json, hashlib
def J(p): return json.load(open(p, encoding="utf-8"))
W = r"C:\IALD\Central de Patentes\work\torre_03nov"
HL = J(W + r"\PROVA_SEM_PERDA_Haja_Luz_CLAUDE.json"); NA = J(W + r"\PROVA_SEM_PERDA_Nativa_CLAUDE.json")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
rel = W + r"\RELATORIO_TORRE_03nov.md"
d = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\claude-torre"
os.makedirs(d, exist_ok=True)
fn = os.path.join(d, time.strftime("%Y%m%d_%H%M%S") + "_torre_claude_md_compactados_e_missao_acom.md")
assert not os.path.exists(fn)
txt = f"""---
quem: claude-torre
casa: Central de Patentes
tipo: project
estatuto: REAL
alvo_sugerido: novo:torre-claude-md-compactados-03nov
fontes:
  - {rel}  sha256:{sha(rel)}
  - {W}\\PROVA_SEM_PERDA_Haja_Luz_CLAUDE.json  sha256:{sha(W + chr(92) + 'PROVA_SEM_PERDA_Haja_Luz_CLAUDE.json')}
  - {W}\\PROVA_SEM_PERDA_Nativa_CLAUDE.json  sha256:{sha(W + chr(92) + 'PROVA_SEM_PERDA_Nativa_CLAUDE.json')}
---
[REAL] 03/11/2026, com o «Vai» do operador (H5 da ORDEM_005): os dois CLAUDE.md acima do teto da Torre foram compactados SEM PERDA. Haja_Luz {HL['original']['bytes']:,} para {HL['substituido']['bytes']:,} B ({HL['secoes_movidas']} seções em {HL['arquivos_de_parte']} partes, `C:\\IALD\\Artigo\\Haja_Luz\\CLAUDE_memoria\\`); Nativa {NA['original']['bytes']:,} para {NA['substituido']['bytes']:,} B ({NA['secoes_movidas']} seções em {NA['arquivos_de_parte']} partes, `C:\\IALD\\projetos_pyhton\\IALD\\CLAUDE_memoria\\`). Backups de bytes `CLAUDE.md.bak_20261103_100238` ao lado de cada um; prova por reconstrução byte a byte (antes de substituir) e por segundo verificador lendo do disco. Ficou no arquivo: cabeçalho, carta da casa, ordens e erratas vigentes, e (Haja_Luz) as entradas `vNNN SELADA` de v386 a v406; o resto virou índice com faixa de linhas originais (erratas que citam «Linha NNNNN» valem para o original). `torre.py gerar`: os dois itens «Instrução» saíram de DEFASADO (ficam em ALERTA 65.536 B).
[REAL] A missão ACOM `claude-central-9c_patentes-atualizacao-12out` segue recusada pelo guarda por UMA fonte (`q.records[2].sources[0].ref`, regra `escritorio_path`: caminho da casa Escritório citado como fonte de um registro `pending`). Encerrar por `transition` não a tira da Torre (a Torre lê só o mtime do diário em 30 dias; a transição o reinicia) e uma errata que a supersede não passa pelo guarda (a projeção traz o original junto com a correção; testado em memória, nada gravado). Parede medida; nada foi escrito no banco, no diário nem no guarda. Proposta: esperar a janela (sai da Torre em 12/11/2026) ou reclassificar o ITEM da Torre (recusa por `escritorio_path` como INFO); mudar o guarda, nunca.
[OPEN] `build_acervo_index.py` (Nativa) indexa o Haja_Luz sem recursão: acrescentar `CLAUDE_memoria` às SOURCES. Lição 54 anexada em `work\\custodia_G1\\LICOES_v400_25out.md`; rota `infra.torre_claude_md_compactacao_03nov` no Mapa.
"""
open(fn, "w", encoding="utf-8", newline="\n").write(txt)
print(fn, os.path.getsize(fn))
