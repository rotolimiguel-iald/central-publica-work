# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R4), item C: (1) _ensaio_s10() da cadeia (ORQ redirecionado para _orq_sandbox; 10 de 10?); (2) recibo_do_app() com casos MEUS em dirs sinteticos
dentro de _orq_sandbox/r4_s10 (nunca o TUNEL_CLAUDE_APP real): RESULTADOS/NNN_RESULTADO.json cumprida abre, parcial/recusada/incerta/cumprida_parcial fecham, ordem de outro numero fecha,
resultado anterior a ordem fecha, JSON invalido/lista nao derruba, e os outros 3 elos (a release errada, pino errado...) seguem exigidos mesmo com o JSON cumprida."""
import hashlib, importlib.util, json, os, shutil, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
spec = importlib.util.spec_from_file_location("pos_treino_rev5", R + "orquestrador/pos_treino_v407.py"); O = importlib.util.module_from_spec(spec); sys.modules["pos_treino_rev5"] = O; spec.loader.exec_module(O)
meu = Path(R + "revisao_terceiro/_orq_sandbox"); O.ORQ = meu; O.LOG = meu / "orq_r4.log"; O.ESTADO = meu / "ESTADO_r4.json"
print("== _ensaio_s10() =="); ok = O._ensaio_s10(); print("ensaio ok:", ok)
out = meu / "r4_s10"
if out.exists(): shutil.rmtree(out)
(out / "tunel").mkdir(parents=True); (out / "app").mkdir(); (out / "work" / "iald_v407_ens").mkdir(parents=True)
pin = O.jload(O.PK / "CANDIDATO_v407.json")["sha256"]
ordem = out / "tunel" / "ORDEM_002_x.md"; ordem.write_text("ordem", encoding="utf-8"); num = 2
time.sleep(1.1)
jv = out / "app" / "jev_control_v407.json"; jv.write_text("{}", encoding="utf-8")
def base(release="v407", srcsha=pin):
    (out / "work" / "iald_v407_ens" / "INSTALLED_VERIFICATION.json").write_text(json.dumps({"status": "PASS", "identity": {"release": release, "source_sha256": srcsha}}), encoding="utf-8")
    (out / "app" / "iald_nucleo_fixo.json").write_text(json.dumps({"operational_core": {"current_release": release, "release_source_sha256": srcsha}, "jev_control": {"release": release, "source_sha256": srcsha, "path": str(jv), "sha256": hashlib.sha256(jv.read_bytes()).hexdigest()}}), encoding="utf-8")
rd = out / "tunel" / "RESULTADOS"
def limpa():
    if rd.exists(): shutil.rmtree(rd)
    for p in (out / "tunel").glob("RELATORIO_*.md"): p.unlink()
def caso(rotulo, esperado, nome="002_RESULTADO.json", conteudo=None, release="v407", srcsha=pin, antes_da_ordem=False, bruto=None):
    limpa(); base(release, srcsha); rd.mkdir()
    p = rd / nome
    if bruto is not None: p.write_text(bruto, encoding="utf-8")
    else: p.write_text(json.dumps(conteudo), encoding="utf-8")
    if antes_da_ordem: os.utime(p, (ordem.stat().st_mtime - 100, ordem.stat().st_mtime - 100))
    try:
        okx, d = O.recibo_do_app(ordem, num, "v407", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); r = okx
    except Exception as e:  # noqa: BLE001
        r = "EXCECAO " + repr(e)[:90]
    print("%-3s %-78s -> %s" % ("OK" if r == esperado else "XX", rotulo, r))
    return r == esperado
n = 0
n += not caso("cumprida, ORDEM_002, 002_RESULTADO.json", True, conteudo={"ordem": "ORDEM_002", "estado": "cumprida"})
n += not caso("cumprida com maiusculas e espaco ('CUMPRIDA ')", True, conteudo={"ordem": "ORDEM_002", "estado": "CUMPRIDA "})
n += not caso("parcial", False, conteudo={"ordem": "ORDEM_002", "estado": "parcial"})
n += not caso("recusada", False, conteudo={"ordem": "ORDEM_002", "estado": "recusada"})
n += not caso("incerta", False, conteudo={"ordem": "ORDEM_002", "estado": "incerta"})
n += not caso("cumprida_parcial (nao e' cumprida)", False, conteudo={"ordem": "ORDEM_002", "estado": "cumprida_parcial"})
n += not caso("sem campo estado", False, conteudo={"ordem": "ORDEM_002"})
n += not caso("outra ordem: ORDEM_999 em 999_RESULTADO.json", False, nome="999_RESULTADO.json", conteudo={"ordem": "ORDEM_999", "estado": "cumprida"})
n += not caso("campo ordem de outro numero, nome 002 (o campo diz ORDEM_020)", True, conteudo={"ordem": "ORDEM_020", "estado": "cumprida"})   # comportamento: o nome do arquivo basta
n += not caso("ORDEM_0020 no campo e nome 020_RESULTADO.json", False, nome="020_RESULTADO.json", conteudo={"ordem": "ORDEM_0020", "estado": "cumprida"})
n += not caso("sem campo ordem, nome 002 (basta o nome)", True, conteudo={"estado": "cumprida"})
n += not caso("anterior a ordem (mtime -100 s)", False, conteudo={"ordem": "ORDEM_002", "estado": "cumprida"}, antes_da_ordem=True)
n += not caso("JSON invalido", False, bruto="{nao e json")
n += not caso("JSON e' uma lista (nao dict)", False, bruto="[1,2]")
n += not caso("JSON e' string", False, bruto="\"cumprida\"")
n += not caso("cumprida mas release errada no app (outros elos seguem exigidos)", False, conteudo={"ordem": "ORDEM_002", "estado": "cumprida"}, release="v405")
n += not caso("cumprida mas pino errado", False, conteudo={"ordem": "ORDEM_002", "estado": "cumprida"}, srcsha="0" * 64)
# sem pasta RESULTADOS nem RELATORIO
limpa(); base(); r, _ = O.recibo_do_app(ordem, num, "v407", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); print("%-3s %-78s -> %s" % ("OK" if r is False else "XX", "sem RELATORIO e sem RESULTADOS", r)); n += not (r is False)
# RELATORIO da forma antiga continua valendo
limpa(); base(); (out / "tunel" / "RELATORIO_20261103.md").write_text("da ORDEM_002", encoding="utf-8"); r, _ = O.recibo_do_app(ordem, num, "v407", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); print("%-3s %-78s -> %s" % ("OK" if r is True else "XX", "RELATORIO antigo (forma da R3) continua valendo", r)); n += not (r is True)
print("RESUMO: casos com resultado inesperado:", n)
