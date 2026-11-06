# -*- coding: utf-8 -*-
"""Revisor terceiro v409 (R1): importa o orquestrador (NAO executa main) e roda _plano() (so' leitura) com ORQ REDIRECIONADO para a minha pasta, para nada ser escrito fora de revisao_terceiro/.
Confere: a ordem dos passos no main (SEM S7 e SEM S10, D57a), a AUT contra o verbatim, o S6d (glob do script dos textos da custodia; portao do G1 sobre o HANDOFF INTEIRO), o S1b (le arquivos_revisados), padroes proibidos
(kill por nome, restauracao, publicacao fora da G1, commit/push), e que s7_g1 / s10_app NAO sao chamadas em nenhum lugar alcancavel do main/_plano."""
import ast, importlib.util, io, json, os, re, sys, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
spec = importlib.util.spec_from_file_location("pos_treino_rev", R + "orquestrador/pos_treino_v409.py"); O = importlib.util.module_from_spec(spec); sys.modules["pos_treino_rev"] = O; spec.loader.exec_module(O)
meu = Path(R + "revisao_terceiro/_orq_sandbox"); meu.mkdir(exist_ok=True)
O.ORQ = meu; O.ESTADO = meu / "ESTADO_l.json"; O.LOG = meu / "orq_l.log"
print("== _plano() ==")
ok_plano = O._plano()
print("plano rc:", ok_plano)
src = open(R + "orquestrador/pos_treino_v409.py", encoding="utf-8").read()
tr = ast.parse(src)
m = re.search(r"for passo in \(([^)]*)\)", src); print("ordem no main:", m.group(1))
ordem_main = [x.strip() for x in m.group(1).split(",")]
print("main SEM s7_g1 e SEM s10_app:", "s7_g1" not in ordem_main and "s10_app" not in ordem_main)
# chamadas a s7_g1 / s10_app / _ensaio_s10 em qualquer lugar do arquivo (alem da definicao)
for nome in ("s7_g1", "s10_app", "_ensaio_s10", "renderizar_ordem", "recibo_do_app"):
    chamadas = []
    for n in ast.walk(tr):
        if isinstance(n, ast.Call):
            f = n.func
            nm = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
            if nm == nome: chamadas.append(n.lineno)
    print("chamadas a %-18s linhas: %s" % (nome, chamadas))
# _plano: lista de passos
mp = re.search(r"passos = \[([^\]]*)\]", src); print("passos do _plano:", mp.group(1)[:400])
# a ORDEM e a AUT
corp = {}
for p in list(Path("C:/IALD/Central de Patentes/work/cunhagens_13out").glob("*verbatim.txt")):
    b = p.read_bytes(); corp[hashlib.sha256(b).hexdigest()[:16]] = (p.name, re.sub(r"\s+", " ", b.decode("utf-8", "replace")))
sh = "8b9b77e992902ff4"; nome, t = corp.get(sh, (None, ""))
print("fala da ordem", sh, nome, "| existe:", bool(nome))
frase = "Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados"
print("   frase na fala:", frase in t, "| frase no AUT:", frase in O.AUT, "| sha16 da ordem no AUT:", sh in O.AUT)
print("AUT (inicio):", O.AUT[:420])
print("sha16 ORDEM arquivo:", O.sha16(O.ORDEM), "| _conferir_ordem():", O._conferir_ordem())
# padroes proibidos
for pad in (r"taskkill", r"Stop-Process\s+-Name", r"Get-Process[^\n]*\|\s*Stop", r"/IM\b", r"pkill", r"killall", r"Stop-Process -Id", r"Remove-Item", r"rmtree", r"shutil\.move", r"os\.remove", r"unlink"):
    n = [(src.count("\n", 0, mm.start()) + 1) for mm in re.finditer(pad, src)]; print("padrao %-30s linhas: %s" % (pad, n[:12]))
for pad in (r"git\s+push", r"git\s+commit", r"--publicar", r"restaur", r"reverter_v409", r"instalar_v409", r"rito_v409\.sh", r"\bgate\b", r"COAUTOR", r"Fable"):
    n = [(src.count("\n", 0, mm.start()) + 1) for mm in re.finditer(pad, src)]; print("padrao %-20s linhas: %s" % (pad, n[:14]))
# S6d
print("S6d glob 'textos_custodia_handoff_v409*.py' (suffix .py):", [p.name for p in (O.PK / "pos_rito").glob("textos_custodia_handoff_v409*.py") if p.suffix == ".py"], "| todos:", [p.name for p in (O.PK / "pos_rito").glob("textos_custodia_handoff_v409*")])
# S1b: le arquivos_revisados
i = src.index("def s1b_revisao"); print(src[i:i + 1800].count("arquivos_revisados"), "usos de arquivos_revisados no S1b")
print("RESUMO: plano_rc=%s" % ok_plano)
