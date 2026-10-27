# -*- coding: utf-8 -*-
"""sonda_p1b_restauracao.py -- P1 limpo: em _escrever_atomico, se OUTRO escritor grava no arquivo entre o os.replace e a conferência final de
_substitui, o ramo «restaura do backup imediato» devolve o ANTIGO e apaga a escrita alheia (que não tem backup em lugar nenhum).
O gancho simula o outro escritor UMA só vez (no primeiro replace); o replace da restauração roda puro. Cópia C:\\t\\mem_rev\\sonda (nunca o real)."""
import importlib.util, json, os, shutil
S = r"C:\t\mem_rev\sonda"; RC = r"C:\t\mem_rev\real_copia"
H = os.path.dirname(os.path.abspath(__file__))
if os.path.isdir(S):
    shutil.rmtree(S)
os.makedirs(os.path.join(S, "fila"))
shutil.copy2(os.path.join(RC, "fila", "memoria.py"), os.path.join(S, "fila", "memoria.py"))
os.environ["MEMORIA_DIR"] = S
spec = importlib.util.spec_from_file_location("memoria_sonda_p1b", os.path.join(S, "fila", "memoria.py")); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
alvo = os.path.join(S, "alvo.txt"); open(alvo, "wb").write(b"ANTIGO\n")
replace0 = m.os.replace; vez = {"n": 0}
def hook(src, dst):
    replace0(src, dst); vez["n"] += 1
    if vez["n"] == 1:                     # o OUTRO escritor (ex.: o pos-rito) grava logo depois do NOSSO replace, uma vez so'
        with open(dst, "ab") as f:
            f.write(b"LINHA DE OUTRO ESCRITOR (sem backup em lugar nenhum)\n")
m.os.replace = hook
try:
    m._escrever_atomico(alvo, b"NOVO\n"); erro = None
except Exception as e:
    erro = "%s: %s" % (type(e).__name__, getattr(e, "mensagem", e))
m.os.replace = replace0
fim = open(alvo, "rb").read()
R = {"erro": erro, "replaces": vez["n"], "conteudo_final": fim.decode(), "voltou_ao_ANTIGO": fim == b"ANTIGO\n", "linha_alheia_sobreviveu": b"OUTRO ESCRITOR" in fim,
     "NOVO_sobreviveu": b"NOVO" in fim, "backups": sorted(f for f in os.listdir(S) if f.startswith("alvo.txt.bak_")),
     "conteudo_dos_backups": [open(os.path.join(S, f), "rb").read().decode() for f in sorted(os.listdir(S)) if f.startswith("alvo.txt.bak_")],
     "leitura": "o 2o replace e' a restauracao (linhas 247-250 de memoria.py): o arquivo volta a ANTIGO; a linha do outro escritor e o NOVO nao estao em backup algum"}
json.dump(R, open(os.path.join(H, "SONDA_P1B.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
