# -*- coding: utf-8 -*-
"""ensaio_passo10_r35.py (R3.5, 19/10/2026) -- ENSAIO A SECO do passo 10 re-derivado do pos_rito/chain_pos_rito_v394.sh: extrai do chain o cabecalho (funcoes) e o bloco do passo 10, aponta PK e NOS para pastas do
sandbox e roda com `sh` (CHAIN_DE=10 CHAIN_ATE=10). NADA e gravado na Bancada (o passo 10 e --modo ensaio), nada na pasta v394 real (PK e o do sandbox; os pinos apontam arquivos reais SO LIDOS), o Nos real so e lido.
  modo standin: NOS = <raiz>/nos_v394s (o um.py CANDIDATO real d19 + selo sintetico): o chain gera a bateria da v394, passa todos os pinos ao esboco R3.5 e o esboco, contra a producao real (so lida), le o Nos, confere os
                pinos da bateria e PARA em NOS_DIFERENTE_DO_PINADO (a producao pina o caminho real do Nos, que ainda e a v393 por dentro) -- o ponto em que o rito terminado muda o resultado.
  modo real:    NOS = o Nos real (hoje no meio do rito: um.py v394, selo v393): o chain PARA ao gerar a bateria (o selo nao pina o um.py) -- depois do rito, passa.
uso: python -I -B -X utf8 ensaio_passo10_r35.py <chain_pos_rito_v394.sh> <raiz C:/t/vb*> standin|real"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
from pathlib import Path

CHAIN, RAIZ, MODO = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
assert RAIZ.parent == Path("C:/t") and re.match(r"^vb[0-9A-Za-z_-]*$", RAIZ.name) and MODO in ("standin", "real")
AQUI = Path(__file__).resolve().parent.parent
PK_REAL = AQUI.parent.parent / "cadeia_de_selo" / "v394"
PROD = Path("C:/IALD/Bancada_Um")
NOS_REAL = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


raiz_e = RAIZ / ("passo10_" + MODO)
if raiz_e.exists():
    shutil.rmtree(raiz_e)
pk, sel = raiz_e / "pk", raiz_e / "pk" / "pos_rito"
sel.mkdir(parents=True)
nos = (RAIZ / "nos_v394s") if MODO == "standin" else NOS_REAL
# o PINOS_BN: o vivo, se ja fundido; senao a fusao em ensaio (so imprime)
vivo = json.loads((PK_REAL / "PINOS_BN_v394.json").read_bytes())
if "esboco_R3_5" in vivo:
    shutil.copyfile(PK_REAL / "PINOS_BN_v394.json", pk / "PINOS_BN_v394.json")
    fonte_pinos = "o PINOS_BN vivo (ja fundido)"
else:
    r = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", str(AQUI / "_construcao" / "fundir_pinos_bn_r35.py"), "--ensaio"], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    (pk / "PINOS_BN_v394.json").write_bytes(r.stdout.encode("utf-8"))
    fonte_pinos = "a fusao em --ensaio (o vivo ainda nao foi fundido)"
shutil.copyfile(PK_REAL / "pos_rito" / "b3_recibo_v394.py", sel / "b3_recibo_v394.py")
t = CHAIN.read_text(encoding="utf-8")
cab = t[:t.index('echo "== 0. guardas')]
b10 = t[t.index("if quer 10; then\n"):t.index("if quer 10a; then\n")]
posix = lambda p: str(p).replace(chr(92), "/")
cab, n1 = re.subn(r'(?m)^PK="[^"]*"; SEL="\$PK/pos_rito"$', lambda m: 'PK="%s"; SEL="$PK/pos_rito"' % posix(pk), cab)
cab, n2 = re.subn(r'(?m)^NOS="[^"]*"$', lambda m: 'NOS="%s"' % posix(nos), cab)
assert n1 == 1 and n2 == 1, (n1, n2)
script = raiz_e / "ensaio_passo10.sh"
script.write_bytes((cab + b10 + 'echo "== FIM do ensaio a seco do passo 10 $(date +%T)"\n').encode("utf-8"))
man_antes = sha(PROD / "canonical_contracts.json")
lista_prod = sorted(os.listdir(PROD))
n_v394_antes = sum(1 for _ in os.scandir(PK_REAL))
env = dict(os.environ, CHAIN_DE="10", CHAIN_ATE="10")
r = subprocess.run(["sh", "-n", str(script)], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("sh -n do script do ensaio: rc=%d %s" % (r.returncode, r.stderr[:200]))
r = subprocess.run(["sh", str(script)], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=1800, stdin=subprocess.DEVNULL)
saida = r.stdout + r.stderr
(raiz_e / "ensaio_passo10_saida.txt").write_bytes(saida.encode("utf-8"))
print("modo=%s nos=%s pinos=%s rc=%d" % (MODO, posix(nos), fonte_pinos, r.returncode))
for linha in saida.splitlines():
    print("  | " + linha[:300])
res = dict(modo=MODO, nos=str(nos), fonte_dos_pinos=fonte_pinos, rc=r.returncode, producao_manifesto_igual=sha(PROD / "canonical_contracts.json") == man_antes, producao_lista_igual=sorted(os.listdir(PROD)) == lista_prod,
           itens_no_topo_do_v394_real_antes=n_v394_antes, itens_no_topo_do_v394_real_depois=sum(1 for _ in os.scandir(PK_REAL)),
           bateria_gerada=(pk / "bateria_pos_selo" / "BATERIA_VINCULO_v394.json").is_file(), saida_sha256=hashlib.sha256(saida.encode("utf-8")).hexdigest())
print(json.dumps(res, ensure_ascii=False))
(raiz_e / "RESULTADO_ENSAIO.json").write_bytes(json.dumps(dict(res, saida=saida), ensure_ascii=False, indent=1).encode("utf-8"))
