# -*- coding: utf-8 -*-
"""Revisor terceiro v408 (R1): importa o orquestrador (NAO executa main) e roda _plano() (so' leitura) e _ensaio_s10() (a seco) com ORQ REDIRECIONADO para a minha pasta, para nada ser escrito fora de revisao_terceiro/.
Confere ainda: a ordem dos passos no main, a citacao da AUT contra os verbatims, o S6d (glob do script dos textos da custodia), padroes proibidos (kill por nome, restauracao, publicacao fora da G1)."""
import importlib.util, io, json, os, re, sys, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
spec = importlib.util.spec_from_file_location("pos_treino_rev", R + "orquestrador/pos_treino_v408.py"); O = importlib.util.module_from_spec(spec); sys.modules["pos_treino_rev"] = O; spec.loader.exec_module(O)
meu = Path(R + "revisao_terceiro/_orq_sandbox"); meu.mkdir(exist_ok=True)
O.ORQ = meu; O.ESTADO = meu / "ESTADO_l.json"; O.LOG = meu / "orq_l.log"
print("== _plano() ==")
ok_plano = O._plano()
print("plano rc:", ok_plano)
print("== _ensaio_s10() (ORQ redirecionado) ==")
ok_ens = O._ensaio_s10()
print("ensaio ok:", ok_ens)
src = open(R + "orquestrador/pos_treino_v408.py", encoding="utf-8").read()
m = re.search(r"for passo in \(([^)]*)\)", src); print("ordem no main:", m.group(1))
corp = {}
for p in list(Path("C:/IALD/Central de Patentes/work/cunhagens_13out").glob("*verbatim.txt")):
    b = p.read_bytes(); corp[hashlib.sha256(b).hexdigest()[:16]] = (p.name, re.sub(r"\s+", " ", b.decode("utf-8", "replace")))
for sh16, citacoes in (("685b8d8bcf0ddbbd", ["liste as pedras que eu preciso nominar e em seguida produza a v408, rode e quando estiver completa, dê a ordem de handoff para a sessão irmã realizar a custódia completa e atualizar tudo (site, repositório, e todos os links), todos os dispositovos e a central de patentes e em seguida publicar, push e commit de tudo"]),
                       ("b89e4c909f37e163", ["prossigamos com tudo, ratifico tudo", "o orquestrador pode executar o que vc mandar"]),
                       ("b5717ff445a883cd", ["compile a nova versão do um.py, rode, publique e atualize tudo por favor"])):
    nome, t = corp.get(sh16, (None, ""))
    print("fala", sh16, nome, "| existe:", bool(nome))
    for c in citacoes: print("   ", repr(c[:70]), "->", c in t)
print("AUT cita 685b..:", "685b8d8bcf0ddbbd" in O.AUT, "| b89e..:", "b89e4c909f37e163" in O.AUT, "| b5717..:", "b5717ff445a883cd" in O.AUT)
print("sha16 ORDEM arquivo:", O.sha16(O.ORDEM), "| _conferir_ordem():", O._conferir_ordem())
for pad in (r"taskkill", r"Stop-Process\s+-Name", r"Get-Process[^\n]*\|\s*Stop", r"/IM\b", r"pkill", r"killall", r"Stop-Process -Id", r"Remove-Item", r"rmtree", r"shutil\.move", r"os\.remove", r"unlink"):
    n = [(src.count("\n", 0, mm.start()) + 1) for mm in re.finditer(pad, src)]; print("padrao %-30s linhas: %s" % (pad, n[:12]))
for pad in (r"git\s+push", r"git\s+commit", r"--publicar", r"restaur", r"reverter_v408", r"instalar_v408", r"rito_v408\.sh", r"\bgate\b"):
    n = [(src.count("\n", 0, mm.start()) + 1) for mm in re.finditer(pad, src)]; print("padrao %-20s linhas: %s" % (pad, n[:14]))
# S6d: o glob acha o script?
print("S6d glob 'textos_custodia_handoff_v408_*.py':", [p.name for p in (O.PK / "pos_rito").glob("textos_custodia_handoff_v408_*.py")], "| arquivo real:", [p.name for p in (O.PK / "pos_rito").glob("textos_custodia_handoff_v408*.py")])
print("RESUMO: plano_rc=%s ensaio_ok=%s" % (ok_plano, ok_ens))
