# -*- coding: utf-8 -*-
"""G1.0 — a instalação ÚNICA do gancho da custódia parametrizada (NÃO APLICADO; escrito em 24/10/2026 por G1, sem tocar nada existente).

O que faz (só com --aplicar; sem a flag apenas CONFERE as âncoras e mostra o que faria):
  1. copia os dois módulos genéricos (já escritos e testados em tools\\custodia_g1\\generico\\) para os lugares onde são carregados POR CAMINHO:
        fronteira_tgl\\runner\\custodia_generica.py          (a pedra do runner)
        patents\\_formula_completa\\camada_generica.py        (o item do módulo dos 16 dispositivos; build_final_code.py o empacota em todo *_FINAL.py)
     — arquivos NOVOS; se já existir um igual, não faz nada; se existir um DIFERENTE, recusa (backup de bytes e errata, decisão da gerência);
  2. fronteira_tgl\\runner\\one_fronteira.py: o carregador `_custodia_generica(versao, anterior)` antes de `def shadow_the_station` (1 troca contada);
  3. patents\\_formula_completa\\tgl_formula_completa.py: `CAMADAS_GENERICAS = ()`, o carregador, a chamada e o `**_genericas` no retorno (3 trocas contadas).
Cada troca exige `count == 1`, respeita o fim de linha (os dois arquivos são CRLF), faz backup de BYTES `<arquivo>.bak_G1_0_<TS>` e `py_compile` no
temporário antes do `os.replace`. As pedras e camadas artesanais anteriores FICAM como estão (exatas para sempre).

QUANDO RODAR: só depois que NENHUMA outra custódia esteja remendando esses arquivos (a v398 os remendou à mão hoje) — o script recusa se a árvore
tem mudança pendente nos três caminhos ou se há trava de custódia viva em work\\custodia_G1\\runs\\. DEPOIS: rebuild dos 16 FINAL (C10), porque o módulo
dos dispositivos muda (o `modulo_sha256` que cada results.json grava muda) — o quadro confere isso por mtime.
Uso:  python instalar_g1_0.py            (confere)
      python instalar_g1_0.py --aplicar  (instala)"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import patches, util   # noqa: E402

PARES = (("tools/custodia_g1/generico/custodia_generica.py", "fronteira_tgl/runner/custodia_generica.py"),
         ("tools/custodia_g1/generico/camada_generica.py", "patents/_formula_completa/camada_generica.py"))


def git(*a):
    return subprocess.run(["git", "-C", str(CEN)] + list(a), capture_output=True, text=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    problemas = []
    pend = git("status", "--porcelain", "--", "fronteira_tgl/runner/one_fronteira.py", "patents/_formula_completa")
    if pend:
        problemas.append("há mudança pendente nos arquivos a remendar (outra custódia em curso?):\n" + pend)
    runs = CEN / "work" / "custodia_G1" / "runs"
    for lk in runs.glob("*.lock") if runs.is_dir() else []:
        problemas.append("trava de custódia: %s" % lk)
    for src, dst in PARES:
        s, d = CEN / src, CEN / dst
        if not s.is_file():
            problemas.append("fonte ausente: %s" % src)
        elif d.is_file() and util.sha256_arquivo(s) != util.sha256_arquivo(d):
            problemas.append("destino existe e DIFERE da fonte (errata ao lado): %s" % dst)
    runner, formula = CEN / patches.ARQ_RUNNER, CEN / patches.ARQ_FORMULA
    r_txt, _, _ = util.ler_eol(runner)
    f_txt, _, _ = util.ler_eol(formula)
    try:
        _, t_r = patches.runner_g1_0(r_txt)
        _, t_f = patches.formula_g1_0(f_txt)
    except util.Parar as e:
        problemas.append("âncora: %s %s" % (e.motivo, e.faltam))
        t_r = t_f = []
    print("G1.0 — conferência das âncoras:\n  runner :", t_r, "\n  módulo :", t_f)
    if problemas:
        print("RECUSADO:")
        for p in problemas:
            print("  -", p)
        return 20
    if not a.aplicar:
        print("(conferência apenas: nada foi gravado; passe --aplicar para instalar)")
        return 0
    ts = util.carimbo()
    for src, dst in PARES:
        d = CEN / dst
        if not d.is_file():
            d.write_bytes((CEN / src).read_bytes())
            print("  copiado:", dst)
    rr = patches.aplicar_em_arquivo(runner, patches.runner_g1_0, "G1_0", ts)
    rf = patches.aplicar_em_arquivo(formula, patches.formula_g1_0, "G1_0", ts)
    # o módulo comum tem de rodar (um elo quebrado levanta RuntimeError)
    run = subprocess.run([sys.executable, "-X", "utf8", str(formula)], cwd=str(formula.parent), capture_output=True, text=True)
    print("  runner:", rr["estado"], "| módulo:", rf["estado"], "| módulo roda: rc", run.returncode)
    (CEN / "work" / "custodia_G1" / ("INSTALACAO_G1_0_%s.json" % ts)).write_text(json.dumps({"runner": rr, "modulo": rf, "modulo_rc": run.returncode}, ensure_ascii=False, indent=1), encoding="utf-8")
    if run.returncode != 0:
        print("O MÓDULO NÃO RODA depois do patch: restaure o backup .bak_G1_0_%s" % ts)
        return 20
    print("FEITO. Próximo: rebuild dos 16 FINAL (custodiar.py executar --so C10) — o módulo comum mudou.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
