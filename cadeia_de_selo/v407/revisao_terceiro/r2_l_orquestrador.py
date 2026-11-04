# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R1): importa o orquestrador (NAO executa main) e roda _plano() (so' leitura) e _ensaio_s10() (a seco) com ORQ REDIRECIONADO para a minha pasta,
para nada ser escrito fora de revisao_terceiro/. Confere ainda: a ordem dos passos no main, a citacao da AUT contra os verbatims, S1b fail-closed."""
import importlib.util, io, json, os, re, sys, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
spec = importlib.util.spec_from_file_location("pos_treino_rev", R + "orquestrador/pos_treino_v407.py"); O = importlib.util.module_from_spec(spec); sys.modules["pos_treino_rev"] = O; spec.loader.exec_module(O)
meu = Path(R + "revisao_terceiro/_orq_sandbox"); meu.mkdir(exist_ok=True)
O.ORQ = meu
print("== _plano() ==")
ok_plano = O._plano()
print("plano rc:", ok_plano)
print("== _ensaio_s10() (ORQ redirecionado) ==")
ok_ens = O._ensaio_s10()
print("ensaio ok:", ok_ens)
# a ordem dos passos no main (texto)
src = open(R + "orquestrador/pos_treino_v407.py", encoding="utf-8").read()
m = re.search(r"for passo in \(([^)]*)\)", src); print("ordem no main:", m.group(1))
# AUT: as citacoes contra os verbatims
corp = {}
for p in list(Path("C:/IALD/Central de Patentes/work/cunhagens_13out").glob("*verbatim.txt")):
    b = p.read_bytes(); corp[hashlib.sha256(b).hexdigest()[:16]] = (p.name, re.sub(r"\s+", " ", b.decode("utf-8", "replace")))
for sh16, citacoes in (("b89e4c909f37e163", ["prossigamos com tudo, ratifico tudo", "o app e o contrato do JEV precisam ser sempre atualizados para a forma canônica mais madura, podia ser até automático isso, e o orquestrador pode executar o que vc mandar"]),
                       ("b5717ff445a883cd", ["compile a nova versão do um.py, rode, publique e atualize tudo por favor"])):
    nome, t = corp.get(sh16, (None, ""))
    print("fala", sh16, nome, "| existe:", bool(nome))
    for c in citacoes: print("   ", repr(c[:70]), "->", c in t)
print("AUT cita b89e..:", "b89e4c909f37e163" in O.AUT, "| b5717..:", "b5717ff445a883cd" in O.AUT)
print("sha16 ORDEM arquivo:", O.sha16(O.ORDEM), "| esperado b89e4c909f37e163")
# proibicoes: mata por nome? restaura? publica fora da G1?
for pad in (r"taskkill", r"Stop-Process\s+-Name", r"Get-Process[^\n]*\|\s*Stop", r"/IM\b", r"pkill", r"killall", r"Stop-Process -Id"):
    n = len(re.findall(pad, src)); print("padrao %-30s ocorrencias: %d" % (pad, n))
for pad in (r"git\s+push", r"git\s+commit", r"--publicar", r"restaur", r"reverter_v407"):
    n = [(src.count("\n", 0, mm.start()) + 1) for mm in re.finditer(pad, src)]; print("padrao %-20s linhas: %s" % (pad, n[:12]))
# S1b fail-closed: simular com REV de outro candidato
tmp = meu / "REV_FAKE.json"; tmp.write_text(json.dumps({"aprovada": True, "candidato_sha16": "0" * 16}), encoding="utf-8")
O.REV = tmp; O.parar_pedido = lambda: False
import time as _t
chamadas = {"n": 0}
real_sleep = _t.sleep
def _sleep(s): chamadas["n"] += 1; raise SystemExit("sleep chamado: o S1b ficou esperando (nao aprovou), como esperado")
O.time.sleep = _sleep
e = {"passos": {}}
O.gravar = lambda e_: None   # nao escreve o ESTADO
O.LOG = meu / "orq.log"
try:
    O.s1b_revisao(e)
except SystemExit as ex:
    print("S1b com candidato_sha16 de outro candidato:", ex)
tmp.write_text(json.dumps({"aprovada": False, "candidato_sha16": O.sha16(O.PK / "um_v407_candidato.py")}), encoding="utf-8")
try:
    O.s1b_revisao(e)
except SystemExit as ex:
    print("S1b com aprovada False:", ex)
tmp.write_text(json.dumps({"aprovada": "true", "candidato_sha16": O.sha16(O.PK / "um_v407_candidato.py")}), encoding="utf-8")
try:
    O.s1b_revisao(e)
except SystemExit as ex:
    print("S1b com aprovada string 'true':", ex)
print("RESUMO: plano_rc=%s ensaio_ok=%s" % (ok_plano, ok_ens))
