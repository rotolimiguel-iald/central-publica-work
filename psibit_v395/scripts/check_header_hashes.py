"""Confere que todo sha16 citado no cabeçalho de Psibit.lean bate com o sha256 calculado AGORA do arquivo citado.

Casos tratados:
  * arquivos-fonte estáveis (patentes, códigos, verbatins): sha256 recomputado tem de bater;
  * o Atlas é arquivo VIVO (outras sessões acrescentam texto): o sha16 do cabeçalho é «do arquivo na data»; se o hash mudou, confere-se que as
    linhas citadas (2137–2141) seguem IGUAIS ao que foi lido (fontes_trechos.txt) e registra-se a mudança;
  * sha16 de VERSÃO do próprio Psibit.lean (a 1ª, examinada): tem de bater com o backup `Psibit.lean.bak_20261021_130122`;
  * os 5 verbatins do operador aparecem INTEIROS no cabeçalho (espaços normalizados).
"""
import hashlib
import json
import re

W = r"C:\IALD\Central de Patentes\work\psibit_v395"
lean = open(W + r"\Psibit.lean", encoding="utf-8").read()
header = lean.split("-/", 1)[0]
citados = sorted(set(re.findall(r"`([0-9a-f]{16})`", header)))

fontes = json.load(open(W + r"\fontes_sha.json", encoding="utf-8"))
atual = {}
for grupo in ("fontes", "verbatins"):
    for k, v in fontes[grupo].items():
        h = hashlib.sha256(open(v["caminho"], "rb").read()).hexdigest()
        atual[v["sha256"][:16]] = (grupo, k, v["caminho"], h == v["sha256"], h[:16])

# versões do próprio Psibit.lean
versoes = {}
bak = W + r"\Psibit.lean.bak_20261021_130122"
hb = hashlib.sha256(open(bak, "rb").read()).hexdigest()
versoes[hb[:16]] = {"arquivo": bak, "papel": "1ª versão (examinada)"}

# trechos do Atlas lidos na 1ª passada
def trechos_atlas():
    out, dentro = {}, False
    for ln in open(W + r"\fontes_trechos.txt", encoding="utf-8"):
        if ln.startswith("==="):
            dentro = ln.startswith("=== atlas")
            continue
        if dentro:
            m = re.match(r"\s*(\d+)\| ?(.*)$", ln.rstrip("\n"))
            if m:
                out[int(m.group(1))] = m.group(2)
    return out

resultado = {"citados": citados, "conferidos": {}, "versoes_do_proprio_arquivo": {}, "arquivo_vivo": {}, "nao_encontrados": []}
for c in citados:
    g = atual.get(c)
    if g is None:
        if c in versoes:
            resultado["versoes_do_proprio_arquivo"][c] = {**versoes[c], "recomputado_igual": True}
            continue
        resultado["nao_encontrados"].append(c)
        continue
    grupo, chave, caminho, igual_ao_json, h_agora = g
    if chave == "atlas":
        # arquivo vivo: hash «na data»; confere o trecho citado
        antigo = trechos_atlas()
        linhas = open(caminho, encoding="utf-8", newline="").read().split("\n")
        iguais = all(linhas[n - 1].rstrip("\r") == t for n, t in antigo.items())
        resultado["arquivo_vivo"][c] = {
            "chave": chave, "sha16_na_data": c, "sha16_agora": h_agora, "hash_mudou": h_agora != c,
            "linhas_citadas": [min(antigo), max(antigo)] if antigo else None, "trecho_citado_segue_igual": iguais,
        }
        continue
    resultado["conferidos"][c] = {"grupo": grupo, "chave": chave, "recomputado_igual_ao_json": igual_ao_json}

verb = {}
corpo = re.sub(r"\s+", " ", re.sub(r"\n>\s?", " ", header))
for k, v in fontes["verbatins"].items():
    txt = open(v["caminho"], encoding="utf-8").read().strip()
    alvo = re.sub(r"\s+", " ", txt)
    verb[k] = {"texto_inteiro_presente": alvo in corpo, "caracteres": len(alvo)}
resultado["verbatins_embutidos"] = verb

ok = (not resultado["nao_encontrados"]) \
    and all(x["recomputado_igual_ao_json"] for x in resultado["conferidos"].values()) \
    and all(x["trecho_citado_segue_igual"] for x in resultado["arquivo_vivo"].values()) \
    and all(x["texto_inteiro_presente"] for x in verb.values())
resultado["tudo_confere"] = ok
print(json.dumps(resultado, ensure_ascii=False, indent=1))
