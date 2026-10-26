# -*- coding: utf-8 -*-
"""25/10/2026 (gerência a7, custódia v400): a Central pública parou no C18 porque um ambiente conda/mamba inteiro (o teste de voz dos
filmes V7, work/filmes_v7_20261024/voice_test/mamba_root: 21.927 arquivos de pacotes de terceiros) entrou no delta do work; a conferência
independente achou três «credenciais em texto» que eram da biblioteca padrão do Python (falsos positivos), e REPROVOU — certo.
A esteira já excluía .venv, venv, node_modules e site-packages, mas não um ambiente conda. Acrescenta os marcadores de ambiente conda
ao EXCL_DIR dos dois construtores de região (o completo e o incremental). Trocas contadas; backup de bytes; py_compile."""
import os, py_compile, time
from pathlib import Path

W = Path(__file__).resolve().parent
TS = time.strftime("%Y%m%d_%H%M%S")
A = '"site-packages", "dist-packages", ".mypy_cache", ".pytest_cache", "build", ".cache"}'
B = ('"site-packages", "dist-packages", ".mypy_cache", ".pytest_cache", "build", ".cache",\n'
     '            # 25/10/2026: ambientes conda/mamba (pacotes de terceiros; o C18 da v400 parou num deles)\n'
     '            "mamba_root", "micromamba", "conda-meta", ".conda", "conda_pkgs", "miniconda3", "miniforge3", "anaconda3"}')
for nome in ("construir_regiao_publica.py", "construir_regiao_incremental.py"):
    p = W / nome
    raw = p.read_bytes(); s = raw.decode("utf-8")
    if '"mamba_root"' in s:
        print(nome, "já aplicado"); continue
    nl = "\r\n" if "\r\n" in s else "\n"
    a, b = A, B.replace("\n", nl)
    assert s.count(a) == 1, (nome, s.count(a))
    s = s.replace(a, b)
    p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    t = p.with_name(p.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, p)
    print(nome, len(raw), "->", p.stat().st_size)
