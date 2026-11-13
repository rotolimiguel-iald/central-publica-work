# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411; ajustado na retomada pelo fork B] a marca de copia mecanica e' MONTADA por concatenacao (este arquivo nao a traz literal, e por isso o p00 nao o conta como copia mecanica); a logica nao mudou
"""_marca_adaptado_v411.py -- troca a marca de copia mecanica de rotulo (a linha que comeca com MARCA, abaixo) por `# [ADAPTADO v411, 12/11/2026, claude-construtor-v411] <motivo>` SO' nos arquivos em que o construtor CONFERIU que o
corpo subido por rotulo ja' e' o certo para a v411 (versao sem modulo novo). Backup de BYTES antes; respeita o fim de linha do arquivo; confere que so' a linha da marca mudou. Ja' rodou em 12/11/2026 sobre os dois arquivos de
MOTIVOS (guarda_p18_v411.py e kernel\\refazer_audit_v411.sh): rodar de novo PARA, visivel, porque a marca ja' saiu deles. uso: python -B -X utf8 _marca_adaptado_v411.py"""
import datetime, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
MARCA = "# [A ADAPTAR v" + "411]"
MOTIVOS = {"guarda_p18_v411.py": "conferido: o corpo e' a guarda P18 da v392, igual de versao a versao (o diff do bump e' so' o rotulo)",
           os.path.join("kernel", "refazer_audit_v411.sh"): "conferido: refaz SO' o Audit do sandbox k411c (caminhos C:/t/k411c/final e v411/kernel); nao roda sem queda que corte o Audit"}
for rel, mot in MOTIVOS.items():
    p = os.path.join(HERE, rel); b = open(p, "rb").read(); t = b.decode("utf-8")
    ls = t.split("\n"); idx = [i for i, l in enumerate(ls) if l.startswith(MARCA)]
    assert len(idx) == 1, (rel, len(idx), "a marca ja' saiu deste arquivo (rodado em 12/11/2026)" if not idx else "")
    cr = "\r" if ls[idx[0]].endswith("\r") else ""
    ls[idx[0]] = "# [ADAPTADO v411, 12/11/2026, claude-construtor-v411] " + mot + cr
    novo = "\n".join(ls).encode("utf-8")
    assert len(novo.split(b"\n")) == len(b.split(b"\n"))
    open(p + ".bak_" + TS, "wb").write(b)
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p)
    print("marcado:", rel)
