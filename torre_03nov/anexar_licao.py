import time, shutil, hashlib, os, json
P = r"C:\IALD\Central de Patentes\work\custodia_G1\LICOES_v400_25out.md"
b = open(P, "rb").read()
crlf = b.count(b"\r\n"); lf = b.count(b"\n") - crlf
ts = time.strftime("%Y%m%d_%H%M%S")
bak = P + ".bak_" + ts + "_torre"
open(bak, "wb").write(b)
assert open(bak, "rb").read() == b
eol = b"\r\n" if crlf > lf else b"\n"
termina = b.endswith(b"\n")
prova = json.load(open(r"C:\IALD\Central de Patentes\work\torre_03nov\PROVA_SEM_PERDA_Haja_Luz_CLAUDE.json", encoding="utf-8"))
pn = json.load(open(r"C:\IALD\Central de Patentes\work\torre_03nov\PROVA_SEM_PERDA_Nativa_CLAUDE.json", encoding="utf-8"))
txt = (
"54. **Instrução de casa acima do teto da Torre: mover por bytes com prova, e o guarda da memória não se contorna por errata.** Em 03/11/2026 (operador: «Vai»; handoff H5) o `CLAUDE.md` do Haja_Luz tinha "
f"{prova['original']['bytes']:,} B e o da Nativa {pn['original']['bytes']:,} B, acima do teto de 262.144 B (item «Torre IALD › Instrução»). Conserto sem perda: `work\\torre_03nov\\compactar.py` segmenta em bytes (seções `## ` fora de cercas; títulos partidos em duas linhas `## ` fundem), "
f"grava cada seção movida em `CLAUDE_memoria\\NNN_slug.md` (as seções acima de 90 KB dividem-se nos `###`), deixa um índice no lugar de cada uma (título, faixa de linhas originais, bytes, gancho, caminho) e SÓ substitui o arquivo depois de reconstruir o original byte a byte (nota e blocos de índice retirados, cada bloco trocado pelas partes na ordem) e de um segundo verificador, por outro caminho, lendo backup, compactado e partes do disco (`PROVA_SEM_PERDA_*.json`, `VERIFICACAO_INDEPENDENTE.json`); CAS pelo sha256 do backup antes do `os.replace`. Resultado: Haja_Luz {prova['original']['bytes']:,} para {prova['substituido']['bytes']:,} B ({prova['secoes_movidas']} seções movidas em {prova['arquivos_de_parte']} partes) e Nativa {pn['original']['bytes']:,} para {pn['substituido']['bytes']:,} B ({pn['secoes_movidas']} em {pn['arquivos_de_parte']}); a Torre tirou os dois itens de DEFASADO (ficam em ALERTA de 65.536 B). "
"Cuidados que valem para a v407: (a) erratas que citam NÚMERO DE LINHA (a de 01/10 cita «Linha 15242») passam a valer para o original: o índice guarda a faixa `Lx–y` e a nota do topo diz isso; (b) a custódia que mede `grep -c vNNN` nas superfícies continua achando as entradas `vNNN SELADA` porque a linhagem viva (v386 em diante) ficou no arquivo; (c) `build_acervo_index.py` indexa `Haja_Luz` sem recursão: o conteúdo movido sai do `acervo_index.json` na próxima reconstrução até `CLAUDE_memoria` entrar nas `SOURCES`. "
"A missão ACOM `claude-central-9c_patentes-atualizacao-12out` é recusada pelo guarda por UMA fonte (`q.records[2].sources[0].ref`, regra `escritorio_path`: caminho da casa Escritório citado como fonte); errata que a supersede NÃO resolve, porque a projeção traz o registro substituído junto com a correção (`project_snapshot`, linhagem inseparável; testado em memória, nada gravado), e `transition` de encerramento NÃO tira a missão da Torre (a Torre só lê o mtime do diário em 30 dias; a transição o reinicia). É parede medida do desenho, não defeito do guarda: o que se muda é o ITEM da Torre (classificar a recusa por `escritorio_path` como INFO) ou se espera a janela (12/11/2026). "
"Lição de ferramenta: `python -` com heredoc vazio no shell bash do harness pendura esperando stdin; script por arquivo.")
add = txt.encode("utf-8")
nov = (b"" if termina else eol) + add + eol
open(P + ".tmp_torre", "wb").write(b + nov)
t2 = open(P + ".tmp_torre", "rb").read()
assert t2.startswith(b) and len(t2) > len(b)
assert open(P, "rb").read() == b, "arquivo mudou durante a anexacao"
os.replace(P + ".tmp_torre", P)
fin = open(P, "rb").read()
print(json.dumps({"backup": bak, "bytes_antes": len(b), "bytes_depois": len(fin), "eol": "CRLF" if eol == b"\r\n" else "LF", "sha256_depois": hashlib.sha256(fin).hexdigest()}, indent=1))
