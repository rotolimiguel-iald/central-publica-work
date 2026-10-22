# -*- coding: utf-8 -*-
"""SÓ LEITURA, saída local sem valores: no preparo de uma região, o que é DADO DE USUÁRIO do app (achado de 22/10/2026: a pasta
«iald_<conta>_invite_<data>» com o provisionamento da conta de um terceiro). Procura (1) pastas cujo nome traga convite, provisionamento,
testador, conta ou usuário; (2) arquivos com atribuição de conta/usuário/destinatário a um valor que não seja de teste. Grava a lista
(varredura_usuarios_<preparo>.txt) e imprime contagens e exemplos de CAMINHO."""
import json, os, re, sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = Path(sys.argv[1])
PASTA = re.compile(r"(?i)(invite|convite|provision|tester|testers|account|accounts|conta_|_conta|usuario|usuarios|\buser\b|users|cadastro|onboard)")
ATR = re.compile(r"(?i)(?:\"(?:account|username|user_name|login|recipient|destinat[aá]rio|invitee|tester|email_to|to_email)\"\s*:\s*\"([^\"]{3,80})\"|"
                 r"\b(?:USER|USERNAME|ACCOUNT|INVITEE)\s*=\s*['\"]([^'\"]{3,80})['\"])")
FALSO = re.compile(r"(?i)(dado pessoal removido|teste|test|fake|synthetic|exemplo|example|fulano|dummy|operador|operator|admin|owner|<|\{|^demo|^x+$)")
TXT = {".py", ".md", ".json", ".jsonl", ".txt", ".yaml", ".yml", ".html", ".js", ".ts", ".tsx", ".log", ".csv"}
raiz = "\\\\?\\" + str(D.resolve())
pastas, arqs, exemplos = Counter(), [], []
for dp, dns, fns in os.walk(raiz):
    dns[:] = [x for x in dns if x != ".git"]
    reld = os.path.relpath(dp, raiz).replace(os.sep, "/")
    comp = [c for c in reld.split("/") if c and c != "."]
    hit_pasta = next((c for c in comp if PASTA.search(c)), None)
    for f in fns:
        rel = (reld + "/" + f) if reld != "." else f
        motivo = None
        if hit_pasta:
            motivo = "pasta:" + hit_pasta
        elif Path(f).suffix.lower() in TXT:
            try:
                t = open(os.path.join(dp, f), "rb").read().decode("utf-8", "replace")
            except OSError:
                continue
            for m in ATR.finditer(t):
                v = m.group(1) or m.group(2) or ""
                if not FALSO.search(v):
                    motivo = "atribuição de conta/usuário"
                    break
        if motivo:
            arqs.append(rel)
            pastas[motivo if motivo.startswith("atrib") else "pasta:" + (comp[0] if comp else "")] += 1
print("%s: %d arquivos" % (D.name, len(arqs)))
for k, n in pastas.most_common(40):
    print("   %5d  %s" % (n, k[:120]))
Path(__file__).with_name("varredura_usuarios_%s.txt" % D.name).write_text("\n".join(arqs) + ("\n" if arqs else ""), encoding="utf-8")
