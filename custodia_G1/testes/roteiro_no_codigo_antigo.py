# -*- coding: utf-8 -*-
"""Prova de que os testes de regressão dos céticos PEGAM o defeito: reconstrói num diretório temporário o pacote G1 de ANTES das correções
(os módulos `*.antes` guardados em work\\custodia_G1\\originais_antes_dos_ceticos\\ por cima da cópia atual, sem recibos.py) e roda três dos roteiros
dos céticos contra ele. Só lê o mundo real; escreve em diretório temporário (apagado). A saída vai para o TESTES.md.

  python roteiro_no_codigo_antigo.py            (orquestra: monta o pacote antigo e chama a si mesmo com --dentro)
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
ANTES = CEN / "work" / "custodia_G1" / "originais_antes_dos_ceticos"
MODULOS = ("motor", "util", "site", "quadro", "publica", "espelho", "espelho_pares", "central", "memorias", "conferencia")


def montar_pacote_antigo(destino):
    pk = Path(destino) / "custodia_g1"
    shutil.copytree(CEN / "tools" / "custodia_g1", pk, ignore=shutil.ignore_patterns("__pycache__"))
    (pk / "recibos.py").unlink()
    for m in MODULOS:
        shutil.copyfile(ANTES / ("%s.py.antes" % m), pk / ("%s.py" % m))
    return pk


def dentro(old):
    sys.path.insert(0, old)
    from custodia_g1 import motor, central, espelho, site as old_site
    from custodia_g1.caminhos import Caminhos
    assert "custodia_g1" in sys.modules and str(Path(old)) in sys.modules["custodia_g1"].__file__, sys.modules["custodia_g1"].__file__
    sys.path.insert(0, str(CEN / "work" / "custodia_G1" / "testes"))
    import testes_g1 as T
    # 1) ALTA — E16..E18 por NOME do manifesto: regerar o manifesto (mesmo nome) com relatórios antigos deixa tudo «ok»
    raiz = T.TMP / "antigo"
    site_d, banc = T._site_sandbox(raiz)
    c = Caminhos({"SITE": str(site_d), "BANC": str(banc)})
    man = T._gerar_manifesto(site_d, banc, "manifesto_v398.json")
    T._ensaio(banc, T._agora_mais(1), man)
    T._subida(banc, T._agora_mais(2), man)
    (site_d / "llms.txt").write_text("llms v2 com conteudo novo", encoding="utf-8")
    T._gerar_manifesto(site_d, banc, "manifesto_v398.json")
    ctx = motor.Ctx(c=c, versao="v398", trabalho=raiz / "w")
    print("1) site, conteúdo novo + manifesto regerado + relatórios antigos: E16=%s E17=%s E18=%s  (o certo: aplicado, FALTA, FALTA)" % (
        old_site._ja_e16(ctx).estado, old_site._ja_e17(ctx).estado, old_site._ja_e18(ctx).estado))
    # 2) MEDIA — C11: o recibo dos 16 FINAL vivia no run_dir da execução
    cen = T.TMP / "cen_antigo"
    for nome, slug in (("BR000_A", "a"), ("BR111_MQC", "mqc")):
        d = cen / "patents" / nome
        d.mkdir(parents=True)
        (d / ("%s_FINAL.py" % slug)).write_text("print('ok')\n", encoding="utf-8")
    ctx = motor.Ctx(c=Caminhos({"CEN": str(cen)}), versao="v398", trabalho=T.TMP / "w_antigo", run_dir=T.TMP / "run_antigo")
    central._ap_c11(ctx)
    ctx2 = motor.Ctx(c=Caminhos({"CEN": str(cen)}), versao="v398", trabalho=T.TMP / "w_antigo")
    m = central._ja_c11(ctx2)
    print("2) C11 num PROCESSO SEGUINTE, depois de rodar os 16 FINAL: %s  (o certo: APLICADO)" % m.estado)
    # 3) MEDIA — git fora do PATH: «sem commit»
    path0 = os.environ["PATH"]
    os.environ["PATH"] = r"C:\Python314;C:\Windows\System32;C:\Windows"
    try:
        ctx3 = T.ctx_de("v397")
        p = espelho.passos_fase_b(ctx3)[0]
        m = p.ja(ctx3)
        print("3) E10 de uma tarefa agendada (PATH sem git): %s — %s  (o certo: achar o git; sem git, falha de leitura visível)" % (m.estado, m.detalhe[:60]))
    finally:
        os.environ["PATH"] = path0
    T._rm(T.TMP)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--dentro":
        dentro(sys.argv[2])
        return 0
    tmp = tempfile.mkdtemp(prefix="g1_antigo_")
    try:
        montar_pacote_antigo(tmp)
        r = subprocess.run([sys.executable, "-X", "utf8", str(Path(__file__).resolve()), "--dentro", tmp], capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(r.stdout.strip())
        if r.returncode != 0:
            print("(falhou: %s)" % r.stderr.strip()[-400:])
        return r.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
