# -*- coding: utf-8 -*-
"""Prova de que os testes t38..t45 PEGAM os defeitos do cético final: reconstrói num diretório temporário o pacote G1 de ANTES das correções
(os módulos `*.antes` guardados em work\\custodia_G1\\originais_antes_do_cetico_final\\ por cima da cópia atual) e roda os roteiros dos achados contra ele.
Só lê o mundo real; escreve em diretório temporário (apagado). A saída vai para o TESTES.md.

  python roteiro_no_codigo_antes_do_cetico_final.py     (orquestra: monta o pacote antigo e chama a si mesmo com --dentro)
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
ANTES = CEN / "work" / "custodia_G1" / "originais_antes_do_cetico_final"
MODULOS = ("site", "central", "espelho", "quadro", "publica", "caminhos", "motor", "util")


def montar_pacote_antigo(destino):
    pk = Path(destino) / "custodia_g1"
    shutil.copytree(CEN / "tools" / "custodia_g1", pk, ignore=shutil.ignore_patterns("__pycache__"))
    for m in MODULOS:
        shutil.copyfile(ANTES / ("%s.py.antes" % m), pk / ("%s.py" % m))
    return pk


def dentro(old):
    sys.path.insert(0, old)
    from custodia_g1 import motor, central, espelho, site as old_site, textos, util
    from custodia_g1.caminhos import Caminhos
    assert "custodia_g1" in sys.modules and str(Path(old)) in sys.modules["custodia_g1"].__file__, sys.modules["custodia_g1"].__file__
    assert not hasattr(old_site, "_natureza") and not hasattr(central, "commitar_so_a_lista"), "este não é o pacote de ANTES"
    sys.path.insert(0, str(CEN / "work" / "custodia_G1" / "testes"))
    import testes_g1 as T
    from custodia_g1.util import Divergencia
    # 1) MEDIA — «nada a subir» depois de uma subida verificada
    raiz, site_d, banc, c, man = T._cenario_site("antigo1")
    mk = lambda: motor.Ctx(c=c, versao="v398", trabalho=raiz / "w")
    T._ensaio(banc, T._agora_mais(1), man)
    T._subida(banc, T._agora_mais(2), man)
    antes_nada = old_site._ja_e18(mk()).estado
    T._nada(banc, T._agora_mais(30), man)
    m = old_site._ja_e18(mk())
    orig = util.rodar
    try:
        util.rodar = lambda cmd, **kw: {"rc": 0, "saida": "a subir: 0 de 5\n# SUBIDA 20261024_140000 \u2014 nada a subir: o ar j\u00e1 \u00e9 igual ao manifesto\n"}
        try:
            old_site._ap_e18(mk())
            ap = "aceitou"
        except Divergencia as e:
            ap = "Divergencia (%s)" % e.motivo[:48]
    finally:
        util.rodar = orig
    print("1) subida verificada (E18=%s) e depois uma repetição «nada a subir»: E18=%s (%s); _ap_e18 com o banner «nada a subir»: %s  (o certo: APLICADO; aceita)" % (antes_nada, m.estado, m.detalhe[:70], ap))
    # 2) MEDIA — C14: o arquivo alheio já staged entra no commit custodia(vN) e é empurrado
    raiz = T.TMP / "antigo2"
    base = {"memory/TGL_ATLAS.md": b"atlas\n", "alheio/a.txt": b"a\n"}
    repo = T._git_toy(raiz, "cen", [("init", base)])
    bare = raiz / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", str(bare)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "push", "-q", "-u", "origin", "main"], check=True, capture_output=True)
    (repo / "vault" / "originals_copy" / "um_unificado_v998").mkdir(parents=True)
    (repo / "vault" / "originals_copy" / "um_unificado_v998" / "x.json").write_bytes(b"{}\n")
    (repo / "alheio" / "a.txt").write_bytes(b"alheio staged por outra sessao\n")
    subprocess.run(["git", "-C", str(repo), "add", "--", "alheio/a.txt"], check=True, capture_output=True)
    salvos = (central.caminhos_a_commitar, central.commit_central, textos.portao, textos.conhecidos_da_rodada)
    try:
        central.caminhos_a_commitar = lambda ctx: (["vault/originals_copy/um_unificado_v998"], [])
        central.commit_central = lambda ctx, Fa: "custodia(v998): teste\n"
        textos.portao = lambda *a, **k: []
        textos.conhecidos_da_rodada = lambda ctx: set()
        ctx = motor.Ctx(c=Caminhos({"CEN": str(repo)}), versao="v998", data="24/10/2026", trabalho=raiz / "w")
        ctx._memo["fatos"] = {"anterior": "v997"}
        central._ap_c14(ctx)
    finally:
        central.caminhos_a_commitar, central.commit_central, textos.portao, textos.conhecidos_da_rodada = salvos
    no_origin = set(util.git(bare, "diff-tree", "--no-commit-id", "--name-only", "-r", "main").splitlines())
    print("2) C14 com um arquivo alheio já staged: o origin recebeu %s  (o certo: só vault/originals_copy/um_unificado_v998/x.json; o alheio fica staged, fora do commit)" % sorted(no_origin))
    # 3) BAIXA — E19: o relatório MAIS NOVO reprova e um mais antigo passou
    from datetime import datetime
    raiz, site_d, banc, c, man = T._cenario_site("antigo3")
    mk = lambda: motor.Ctx(c=c, versao="v398", trabalho=raiz / "w", data="24/10/2026")
    T._ensaio(banc, T._agora_mais(1), man)
    sub = T._subida(banc, T._agora_mais(2), man)
    t_sub = datetime(2026, 10, 24, 11, 26, 33)
    os.utime(sub / "RELATORIO.md", (t_sub.timestamp(), t_sub.timestamp()))
    (banc / "revisoes" / "leitor_ia_20261024_v398.md").write_text("# LEITOR-IA (R1) \u2014 24/10/2026 09:32:05\n\n**R1: PASSA \u2014 os quatro alvos**\n", encoding="utf-8")
    m_velho = old_site._ja_e19(mk())
    (banc / "revisoes" / "leitor_ia_20261025_v398.md").write_text("# LEITOR-IA (R1) \u2014 25/10/2026 09:00:00\n\n**R1: FALHA \u2014 read-brief n\u00e3o achado(s)**\n", encoding="utf-8")
    m_falha = old_site._ja_e19(mk())
    print("3) E19: R1 PASSA de 09:32 e a subida verificada de 11:26 → %s; depois um R1 mais novo que FALHA → %s  (o certo: FALTA nos dois casos)" % (m_velho.estado, m_falha.estado))
    # 4) BAIXA — E01: o BACKUP_MANIFEST autodeclarado (um byte trocado num arquivo crítico)
    import hashlib
    raiz = T.TMP / "antigo4"
    um = b"# um.py de brinquedo v900\n" * 40
    pin = hashlib.sha256(um).hexdigest()
    b = raiz / "bk" / ("um_v900_%s" % pin[:16])
    arqs = {"um.py": um, "um_absoluto.json": b'{"core": 1}\n', "um_absoluto_selo.json": ('{"um_version": "v900", "sha256": {"um.py": "%s"}}' % pin).encode()}
    for rel, d in arqs.items():
        (b / rel).parent.mkdir(parents=True, exist_ok=True)
        (b / rel).write_bytes(d)
    import json
    (b / "BACKUP_MANIFEST.json").write_text(json.dumps({"versao": "v900", "conferido_contra_origem": True, "n_arquivos": 3,
                                                        "arquivos": {r: {"bytes": len(d), "sha256": hashlib.sha256(d).hexdigest()} for r, d in arqs.items()}}), encoding="utf-8")
    raw = bytearray(arqs["um_absoluto.json"])
    raw[2] ^= 1
    (b / "um_absoluto.json").write_bytes(bytes(raw))
    import types
    salvo = espelho._diario
    espelho._diario = lambda ctx: {"v900": types.SimpleNamespace(pin16=pin[:16])}
    try:
        r, det = espelho.backup_valido(motor.Ctx(c=Caminhos({"BK": str(raiz / "bk")}), versao="v901"), "v900")
    finally:
        espelho._diario = salvo
    print("4) E01 com um byte trocado em um_absoluto.json do backup e o manifesto dizendo «conferido_contra_origem: true»: %s  (o certo: recusado — sha256 da amostra difere)" % ("ACEITO" if r else "recusado"))
    # 5) BAIXA — o auditor L04 não via o formato do llms.txt e do index.md
    raiz = T.TMP / "antigo5"
    (raiz / "site" / "secoes").mkdir(parents=True)
    (raiz / "tb").mkdir()
    (raiz / "site" / "secoes" / "07-o-programa-um-py.md").write_bytes(b"x" * 11731)
    url = "https://teoriadagravitacaoluminodinamica.com/secoes/07-o-programa-um-py.md"
    (raiz / "site" / "llms.txt").write_text("- [The program](%s) (11762 bytes; espelho: https://raw/x.md)\n" % url, encoding="utf-8")
    (raiz / "site" / "index.md").write_text("[07](%s) (11.762 bytes) \u00b7 espelho: [raw](https://raw/x.md)\n" % url, encoding="utf-8")
    d = espelho.auditar_numeros_citados(motor.Ctx(c=Caminhos({"TB": str(raiz / "tb"), "SITE": str(raiz / "site")}), versao="v398"))
    print("5) auditor L04 com secoes/07 citada 11762 (real 11731) no llms.txt e no index.md: %d defasado(s) achado(s)  (o certo: 2)" % len(d))
    # 6) BAIXA — a mensagem do commit da Central afirma a rota antes de C16
    ctx = T.ctx_de("v398")
    texto = central.commit_central(ctx, ctx.fatos)
    print("6) mensagem do commit da Central: %s  (o certo: não cita a rota no mapa — ela só entra em C16)" % ("diz «rota custodia.v398 no mapa de rotas»" if "rota custodia.v398 no mapa de rotas" in texto else "não cita a rota"))
    T._rm(T.TMP)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--dentro":
        dentro(sys.argv[2])
        return 0
    tmp = tempfile.mkdtemp(prefix="g1_antigo_final_")
    try:
        montar_pacote_antigo(tmp)
        r = subprocess.run([sys.executable, "-X", "utf8", str(Path(__file__).resolve()), "--dentro", tmp], capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(r.stdout.strip())
        if r.returncode != 0:
            print("(falhou: %s)" % r.stderr.strip()[-600:])
        return r.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
