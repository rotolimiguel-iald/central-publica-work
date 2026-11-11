# -*- coding: utf-8 -*-
"""_r5c_05_resumo_v410.py -- o RESUMO da revisao do construtor sobre a adaptacao da R5 (10/11/2026): para cada arquivo tocado pelos scripts _r5c_01 a _r5c_04, o sha16 de ANTES (o backup .bak_*_r5c* MAIS ANTIGO, bytes) e o de DEPOIS (o arquivo em disco).
So' leitura dos arquivos; grava _r5c_RESULTADO_v410.json por temporario + os.replace."""
import glob, hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
baks = sorted(glob.glob(os.path.join(HERE, "*.bak_*_r5c*")) + glob.glob(os.path.join(HERE, "pos_rito", "*.bak_*_r5c*")))
por_arquivo = {}
for b in baks:
    orig = b[:b.index(".bak_")]; por_arquivo.setdefault(orig, []).append(b)
linhas = []
for orig in sorted(por_arquivo):
    mais_antigo = sorted(por_arquivo[orig], key=lambda x: x[x.index(".bak_") + 5:])[0]
    a = h16(mais_antigo); d = h16(orig)
    linhas.append({"arquivo": os.path.relpath(orig, HERE).replace(os.sep, "/"), "sha16_antes": a, "sha16_depois": d, "mudou": a != d, "backup_mais_antigo": os.path.basename(mais_antigo), "n_backups": len(por_arquivo[orig])})
out = {"contrato": "R5c_RESULTADO_v410", "quando": time.strftime("%d/%m/%Y %H:%M:%S"), "quem": "claude-construtor-v410 (a revisao do construtor sobre a adaptacao da R5 feita pelo agente; scripts _r5c_01 a _r5c_04)",
       "nota_dos_antes": "o sha16 'antes' e' o do backup _r5c MAIS ANTIGO do arquivo, isto e', o estado que o agente da R5 deixou (o 'depois' dele em _r5ag_RESULTADO_v410.json)",
       "arquivos": linhas, "n_arquivos": len(linhas), "n_mudados": sum(1 for x in linhas if x["mudou"]),
       "scripts": ["_r5c_01_revisao_do_construtor_v410.py", "_r5c_02_controles_da_juncao_v410.py", "_r5c_03_relatorio_v410.py", "_r5c_04_teste_offline_v410.py", "_r5c_05_resumo_v410.py", "_r2_copiar_insumos_guardando_v410.py", "_r2_gerar_instalador_r5_v410.py", "_r2_instalar_pedra_r5_v410.py"]}
p = os.path.join(HERE, "_r5c_RESULTADO_v410.json"); tmp = p + ".tmp"
open(tmp, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, indent=1)); assert os.path.getsize(tmp) > 0; os.replace(tmp, p)
print("arquivos com backup _r5c:", len(linhas), "| mudados:", out["n_mudados"])
for x in linhas:
    print(" ", x["arquivo"], x["sha16_antes"], "->", x["sha16_depois"])
