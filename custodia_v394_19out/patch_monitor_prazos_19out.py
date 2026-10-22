# -*- coding: utf-8 -*-
"""Controle de prazos da Central (19/10/2026, sessão a7; pendências «CONTROLE» da ENTREGA_009 do Codex de 19/10, que não volta por falta de
créditos — o operador mandou terminar o serviço). Duas correções no tools/patent_monitor.py, ao lado, com backup de BYTES:
 1. a nota da anuidade dizia «retardatária por mais 3 meses»; a LPI art. 84 §2º diz «dentro dos 6 (seis) meses subsequentes, mediante
    pagamento de retribuição adicional» [KNOWN/LEGAL] — errata dita no próprio texto;
 2. a auditoria de prazos só percorria os 16 dockets; os processos adicionais com data de depósito (o BR 11 2026 025335-5 da fase nacional do
    ACOM e o BR 10 2026 024913-0, o BR novo do Crypto) passam a ter os prazos computados como itens próprios, marcados `adicional_de`.
Nada muda nos dockets; a contagem `processos` segue sendo a dos dockets (16), com `processos_adicionais` ao lado."""
import os, subprocess, sys, time

P = r"C:\IALD\Central de Patentes\tools\patent_monitor.py"
raw = open(P, "rb").read()
s = raw.decode("utf-8")
if "processos_adicionais\": 0" in s:
    print("já aplicado"); raise SystemExit
crlf = b"\r\n" in raw
pares = [
    ('             "ordinário nos 3 meses seguintes; com retardatária (sobretaxa) por mais 3 meses."},\n',
     '             "ordinário nos 3 meses seguintes; com retribuição adicional, independente de notificação, nos 6 meses "\n'
     '             "subsequentes (LPI art. 84 §2º). [errata 19/10/2026: o texto anterior dizia «por mais 3 meses»]"},\n'),
    ('    resumo = {"processos": len(dockets), "prazos_vencidos_a_conferir": 0,\n',
     '    resumo = {"processos": len(dockets), "processos_adicionais": 0, "prazos_vencidos_a_conferir": 0,\n'),
    ('    for d in dockets:\n'
     '        base_filing = d.filing_date\n'
     '        base_prio = d.priority_date\n'
     '        item = {"processo": d.processo, "dir": d.dir, "titulo": (d.titulo or "")[:70],\n',
     '    # 19/10/2026: além dos dockets, os processos adicionais com data de depósito própria (fase nacional BR 11 do ACOM; BR novo do Crypto)\n'
     '    alvos = []\n'
     '    for d in dockets:\n'
     '        alvos.append((d.processo, d.dir, d.titulo, d.filing_date, d.priority_date, d.has_pct, None))\n'
     '        for x in (d.raw.get("processos_adicionais") or []):\n'
     '            fd = _parse_date(x.get("filing_date")) if isinstance(x, dict) else None\n'
     '            if isinstance(x, dict) and x.get("processo") and fd:\n'
     '                alvos.append((str(x["processo"]), d.dir, x.get("papel") or d.titulo, fd, _parse_date(x.get("priority_date")) or fd, False, d.dir))\n'
     '    for (processo_, dir_, titulo_, base_filing, base_prio, has_pct_, adicional_de) in alvos:\n'
     '        item = {"processo": processo_, "dir": dir_, "titulo": (titulo_ or "")[:70],\n'),
    ('                "has_pct": d.has_pct, "prazos": []}\n',
     '                "has_pct": has_pct_, "prazos": []}\n'
     '        if adicional_de:\n'
     '            item["adicional_de"] = adicional_de\n'
     '            resumo["processos_adicionais"] += 1\n'),
    ('            if rule.get("only_if_pct") and not d.has_pct:\n',
     '            if rule.get("only_if_pct") and not has_pct_:\n'),
    ('    print(f"  {r[\'processos\']} processos · vencidos-a-conferir: {r[\'prazos_vencidos_a_conferir\']} · "\n',
     '    print(f"  {r[\'processos\']} processos (+{r.get(\'processos_adicionais\', 0)} adicionais) · vencidos-a-conferir: {r[\'prazos_vencidos_a_conferir\']} · "\n'),
]
for a, b in pares:
    if crlf:
        a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)
compile(s, P, "exec")
open(P + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "wb").write(raw)
open(P + ".tmp", "wb").write(s.encode("utf-8"))
assert os.path.getsize(P + ".tmp") > len(raw)
os.replace(P + ".tmp", P)
print("ok", len(raw), "->", os.path.getsize(P))
r = subprocess.run([sys.executable, "-X", "utf8", P, "--audit"], capture_output=True, text=True, encoding="utf-8", errors="replace",
                   cwd=os.path.dirname(os.path.dirname(P)))
print("rc", r.returncode)
print((r.stdout or "")[-2500:], (r.stderr or "")[-800:])
