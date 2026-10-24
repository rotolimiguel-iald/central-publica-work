# -*- coding: utf-8 -*-
"""montar_prototipo.py -- gera selo_acom_prototipo.py a partir de selo_acom_prototipo.py.tmpl, COPIANDO o codigo do operador (skygrid acom_mirror.py e
acom_crypto.py) e LENDO dos arquivos todos os hashes (nada de hash de memoria).

O codigo embutido e' o do operador, linha a linha, com SUBSTITUICOES minimas e declaradas (SUBST abaixo; cada uma tem de ocorrer EXATAMENTE uma vez):
a retirada dos imports relativos do pacote skygrid_sim e a troca de tgl_core.beta()/tgl_core.theta_m() por _beta_runtime()/_theta_m_runtime()
(beta = ALPHA_FINE_CODATA_2018 * sqrt(e) em runtime, nunca literal). Escreve so em C:\\IALD\\Central de Patentes\\work\\v399_selo_e_testemunho:
selo_acom_prototipo.py (com backup de BYTES do anterior) e EMBUTIDO_MANIFESTO.json.
Uso: python -I -B -X utf8 montar_prototipo.py
"""
import hashlib
import json
import os
import re
import time

W = r"C:\IALD\Central de Patentes\work\v399_selo_e_testemunho"
SKY = r"C:\IALD\Central de Patentes\Patentes\Skygrid\SkyGrid_Piloto"
FONTES = {
    "mirror": os.path.join(SKY, "skygrid_sim", "acom_mirror.py"),
    "crypto": os.path.join(SKY, "skygrid_sim", "acom_crypto.py"),
    "tgl_core": os.path.join(SKY, "skygrid_sim", "tgl_core.py"),
    "run_tests": os.path.join(SKY, "tests", "run_tests.py"),
    "v17_torch": r"C:\IALD\projetos_pyhton\acom\Acom_v17_mirror_crypto.py",
    "patente_tex": r"C:\IALD\Central de Patentes\Patentes\ACOM_Mirror_Crypto_PI_INPI.tex",
}
TMPL = os.path.join(W, "selo_acom_prototipo.py.tmpl")
OUT = os.path.join(W, "selo_acom_prototipo.py")

# primeira linha (1-based) do corpo copiado: depois do docstring do modulo e antes dos imports
PRIMEIRA = {"mirror": 22, "crypto": 22}
SUBST = {
    "mirror": [
        ("from . import tgl_core\n",
         "# (removido no embutido) from . import tgl_core  -- beta e theta_M vem de _beta_runtime() e _theta_m_runtime() (ALPHA_FINE_CODATA_2018 * sqrt(e))\n"),
        ("self.beta = tgl_core.beta()            # runtime, never literal",
         "self.beta = _beta_runtime()            # runtime, never literal"),
        ("self.theta_miguel = tgl_core.theta_m()",
         "self.theta_miguel = _theta_m_runtime()"),
    ],
    "crypto": [
        ("from . import tgl_core\nfrom .acom_mirror import DimensionalMirror, MirrorReflection, _unpack2bits, PARITY\n",
         "# (removidos no embutido) from . import tgl_core ; from .acom_mirror import ... -- os nomes ja estao neste modulo (bloco acom_mirror acima)\n"),
        ("self.beta = tgl_core.beta()   # runtime",
         "self.beta = _beta_runtime()   # runtime"),
    ],
}
PATENTE = {"mirror": "BR 10 2026 003428-2", "crypto": "BR 10 2026 003431-2"}


def ler(p):
    return open(p, "rb").read()


def sha(b):
    return hashlib.sha256(b).hexdigest()


info = {}
for k, p in FONTES.items():
    b = ler(p)
    info[k] = {"caminho": p, "sha256": sha(b), "bytes": len(b)}

blocos = {}
manifesto_blocos = {}
for k in ("mirror", "crypto"):
    txt = ler(FONTES[k]).decode("utf-8").replace("\r\n", "\n")
    linhas = txt.split("\n")
    corpo = "\n".join(linhas[PRIMEIRA[k] - 1:]).rstrip("\n") + "\n"
    subs = []
    for velho, novo in SUBST[k]:
        assert corpo.count(velho) == 1, (k, velho[:60], corpo.count(velho))
        corpo = corpo.replace(velho, novo)
        subs.append({"velho": velho.strip("\n"), "novo": novo.strip("\n"), "ocorrencias": 1})
    # nenhum uso de tgl_core fora de comentario
    sem_coment = "\n".join(l.split("#")[0] for l in corpo.split("\n"))
    assert "tgl_core." not in sem_coment, "sobrou uso de tgl_core no embutido " + k
    assert not re.search(r"0[.,]012", corpo), "literal 0,012 no embutido " + k
    ini = (f"# >>> ACOM_EMBUTIDO_INICIO: skygrid_sim/{os.path.basename(FONTES[k])} (sha256 {info[k]['sha256']}) -- patente {PATENTE[k]} -- "
           f"linhas {PRIMEIRA[k]}-{len(linhas) - (1 if linhas[-1] == '' else 0)} do fonte, com {len(subs)} substituicao(oes) declarada(s) no EMBUTIDO_MANIFESTO.json >>>\n")
    fim = f"# <<< ACOM_EMBUTIDO_FIM: skygrid_sim/{os.path.basename(FONTES[k])} <<<\n"
    blocos[k] = ini + corpo + fim
    manifesto_blocos[k] = {"fonte": FONTES[k], "fonte_sha256": info[k]["sha256"], "primeira_linha_copiada": PRIMEIRA[k],
                           "ultima_linha_do_fonte": len(linhas) - (1 if linhas[-1] == "" else 0), "substituicoes": subs,
                           "texto_embutido_sha256": sha((corpo).encode("utf-8")), "linhas_embutidas": corpo.count("\n")}

embutido = blocos["mirror"] + "\n" + blocos["crypto"]
# o hash do bloco inteiro (do primeiro marcador de inicio ao ultimo marcador de fim, inclusive) e' o que o prototipo confere sobre si mesmo
embutido_sha = sha(embutido.encode("utf-8"))

t = open(TMPL, "rb").read().decode("utf-8")
SUBS_TMPL = {
    "EMBUTIDO": embutido,
    "EMBUTIDO_SHA256": embutido_sha,
    "SHA_MIRROR": info["mirror"]["sha256"], "SHA_CRYPTO": info["crypto"]["sha256"], "SHA_TGL_CORE": info["tgl_core"]["sha256"],
    "SHA_RUN_TESTS": info["run_tests"]["sha256"], "SHA_V17": info["v17_torch"]["sha256"], "SHA_TEX": info["patente_tex"]["sha256"],
    "BYTES_V17": str(info["v17_torch"]["bytes"]), "BYTES_TEX": str(info["patente_tex"]["bytes"]),
}
for k, v in SUBS_TMPL.items():
    assert ("@@" + k + "@@") in t, "placeholder ausente no template: " + k
    t = t.replace("@@" + k + "@@", v)
restos = re.findall(r"@@[A-Z0-9_]+@@", t)
assert not restos, f"placeholders sem valor: {restos}"

if os.path.exists(OUT):
    ts = time.strftime("%Y%m%d_%H%M%S")
    b = ler(OUT)
    bak = f"{OUT}.bak_{ts}"
    with open(bak, "xb") as f:
        f.write(b)
    assert ler(bak) == b
    print("BACKUP", bak, sha(b)[:16])
tmp = OUT + ".tmp"
with open(tmp, "w", encoding="utf-8", newline="\n") as f:
    f.write(t)
assert os.path.getsize(tmp) > 8000
os.replace(tmp, OUT)
b = ler(OUT)
man = {"prototipo": {"caminho": OUT, "sha256": sha(b), "sha16": sha(b)[:16], "bytes": len(b), "linhas": b.decode("utf-8").count("\n")},
       "fontes": info, "blocos": manifesto_blocos, "bloco_embutido_completo_sha256": embutido_sha,
       "regra_do_hash_do_bloco": "sha256 do texto UTF-8 do primeiro marcador ACOM_EMBUTIDO_INICIO ate o ultimo marcador ACOM_EMBUTIDO_FIM, inclusive (LF)"}
json.dump(man, open(os.path.join(W, "EMBUTIDO_MANIFESTO.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("selo_acom_prototipo.py", man["prototipo"]["sha16"], man["prototipo"]["bytes"], "bytes", man["prototipo"]["linhas"], "linhas | bloco embutido", embutido_sha[:16])
