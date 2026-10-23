# -*- coding: utf-8 -*-
"""Conferência de CONTEÚDO dos arquivos da raiz dos três preparos públicos (README, PATENTES, vínculo, llms.txt do Kimi, exclusões,
índice e .gitattributes) com as mesmas funções do conferidor independente (23/10/2026: a raiz passou a ser conferida em conteúdo; antes
era pulada inteira). Só contagens e nomes. Uso: testar_raiz_preparos.py   (exit 1 se achar algo)"""
import re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
src = (W / "conferir_preparos.py").read_text(encoding="utf-8")
ach = []
for prep in ("central-publica", "central-publica-work", "central-publica-bancada"):
    D = Path(r"C:\IALD\Central_publica") / prep
    ns = {"__file__": str(W / "conferir_preparos.py")}
    sys.argv = [sys.argv[0], str(D)] + ([] if prep == "central-publica" else ["regiao"])
    exec(src.split("SEM_INDICE = ")[0], ns)
    for nome in ("README.md", "PATENTES.md", "vinculo_patentario.json", "llms.txt", "EXCLUSOES_PUBLICAS.json", "INDICE_PUBLICO.json", ".gitattributes"):
        p = D / nome
        if not p.is_file():
            continue
        t = p.read_bytes().decode("utf-8", "replace")
        motivos = []
        if ns["CPF"].search(t) or ns["RG"].search(t):
            motivos.append("CPF/RG")
        if ns["FONE"].search(t):
            motivos.append("telefone")
        if ns["EMAIL_PESSOAL"].search(t):
            motivos.append("e-mail pessoal")
        if ns["ENDERECO"].search(t):
            motivos.append("endereço/CEP/nascimento")
        if ns["TERC"] is not None and ns["TERC"].search(t):
            motivos.append("terceiro")
        if ns["ESCRIT"].search(t):
            motivos.append("Escritório")
        fora_b64 = re.sub(r"[A-Za-z0-9+/]{1000,}={0,2}", " ", t) if len(t) >= 1000 else t
        if ns["cred"](fora_b64):
            motivos.append("credencial")
        print("%-26s %-26s %8d B  %s" % (prep, nome, len(t), "OK" if not motivos else "ACHADO: " + ", ".join(motivos)))
        if motivos:
            ach.append((prep, nome, motivos))
print("RAIZ DOS PREPAROS:", "APROVADA" if not ach else "REPROVADA %s" % ach)
sys.exit(1 if ach else 0)
