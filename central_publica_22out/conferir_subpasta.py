# -*- coding: utf-8 -*-
"""A conferência independente (conferir_preparos.py, as mesmas funções, sem importar a guarda) aplicada só a UMA subpasta de um preparo —
para os arquivos que entraram depois da conferência completa (22/10/2026: a pasta da esteira, atualizada antes de publicar o work).
Uso: conferir_subpasta.py <pasta_do_preparo> <subpasta>   (exit 1 se achar algo)"""
import os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D, SUB = Path(sys.argv[1]), sys.argv[2].strip("/\\")
src = Path(__file__).with_name("conferir_preparos.py").read_text(encoding="utf-8")
ns = {"__file__": str(Path(__file__).with_name("conferir_preparos.py"))}
sys.argv = [sys.argv[0], str(D), "regiao"]
exec(src.split("SEM_INDICE = ")[0], ns)
ach = []
raiz = "\\\\?\\" + str((D / SUB).resolve())
for dp, dns, fns in os.walk(raiz):
    for f in fns:
        p = os.path.join(dp, f)
        rel = SUB + "/" + os.path.relpath(p, raiz).replace(os.sep, "/")
        t = open(p, "rb").read().decode("utf-8", "replace")
        esteira = f in ("aplicar_regra_escritorio.py", "conferir_preparos.py", "guarda_publica.py", "testar_regra_escritorio.py")
        motivos = []
        if ns["CPF"].search(t) or ns["RG"].search(t):
            motivos.append("CPF/RG")
        if ns["FONE"].search(t):
            motivos.append("telefone")
        if ns["EMAIL_PESSOAL"].search(t):
            motivos.append("e-mail pessoal")
        if ns["ENDERECO"].search(t):
            motivos.append("endereço/CEP/nascimento")
        if (ns["ESCRIT"].search(t) or ns["ESCRIT"].search(rel)) and not esteira:
            motivos.append("Escritório")
        import re
        fora_b64 = re.sub(r"[A-Za-z0-9+/]{1000,}={0,2}", " ", t) if len(t) >= 1000 else t
        if ns["cred"](fora_b64):
            motivos.append("credencial")
        if motivos:
            ach.append((rel, motivos))
print("%s/%s: %s" % (D.name, SUB, "APROVADO" if not ach else "REPROVADO"), ach[:20])
sys.exit(1 if ach else 0)
