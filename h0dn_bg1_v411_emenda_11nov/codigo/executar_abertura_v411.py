# -*- coding: utf-8 -*-
"""v411 -- executor da ABERTURA (roda UMA vez por arquivo de pinos; aqui so' testado com vetores sinteticos).

  python executar_abertura_v411.py --pinos <json> [--ensaio]

JSON de pinos, campos OBRIGATORIOS:
  rede, congelado, s0, bg, readme, ramos, pre_registro, vetor : {path, sha256}   (vetor tem tambem `chave` e `convencao`)
  vetor.convencao : exatamente "raw_MAS"
  saida           : {path}   (o caminho da saida vem dos pinos; nao ha --saida)
  emenda          : {rotulo, regra_antiga, data, motivo}   (quatro strings nao vazias)
  alvo_fp         : string decimal
  codigo          : {nome: sha256} para abertura_v411.py, estimator_v411.py, veredito_v411.py, executar_abertura_v411.py

Todos os sha256 (insumos, pre_registro e codigo do pacote) sao conferidos ANTES de carregar qualquer coisa. O pre_registro e' so'
conferido por sha (nao e' carregado como codigo). Os TRES modulos (estimator_v411, veredito_v411, abertura_v411) sao executados a
partir dos MESMOS bytes que foram conferidos (compile+exec; nao se le o arquivo duas vezes), e os insumos numericos tambem sao
carregados desses bytes. O executor confere o sha256 do proprio arquivo, mas JA ESTA EM EXECUCAO quando o faz: essa conferencia
detecta o arquivo trocado depois, nao o trocado antes de rodar.
--ensaio: confere pinos + integridade de desenho (conferir_integridade) e sai SEM np.load do vetor (os bytes do vetor so' sao somados
para o sha256) e sem gravar saida. Saida OU <saida>.sha256 ja existente = recusa (codigo 4), tambem no ensaio (a execucao real
seria recusada). Depois de gravar a saida (atomica: temporario -> conferir tamanho -> substituir) grava ao lado <saida>.sha256
(uma linha: "<sha256>  <nome do arquivo>"). ValueError de integridade/vetor = codigo 3, nada gravado.
Codigos: 0 ok, 2 pino/insumo/campo, 3 integridade/vetor, 4 saida existente, 5 leitura do vetor/gravacao.
"""
import argparse
import hashlib
import io
import json
import os
import re
import sys
import types
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ARQ_CODIGO = ("abertura_v411.py", "estimator_v411.py", "veredito_v411.py", "executar_abertura_v411.py")
CAMPOS_ARQ = ("rede", "congelado", "s0", "bg", "readme", "ramos", "pre_registro", "vetor")
CAMPOS_EMENDA = ("rotulo", "regra_antiga", "data", "motivo")
CONVENCAO = "raw_MAS"
HEX64 = re.compile(r"[0-9a-f]{64}")


class Recusa(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def validar_campos(pinos):
    """Estrutura do JSON de pinos (sem tocar arquivo nenhum)."""
    if not isinstance(pinos, dict):
        raise Recusa("o JSON de pinos nao e' um objeto")
    for k in CAMPOS_ARQ:
        e = pinos.get(k)
        if not isinstance(e, dict) or not isinstance(e.get("path"), str) or not isinstance(e.get("sha256"), str) or not HEX64.fullmatch(e["sha256"]):
            raise Recusa("campo de pino ausente ou mal formado: " + k)
    if not isinstance(pinos["vetor"].get("chave"), str) or not pinos["vetor"]["chave"]:
        raise Recusa("campo ausente: vetor.chave")
    if pinos["vetor"].get("convencao") != CONVENCAO:
        raise Recusa("vetor.convencao deve ser exatamente %r (veio %r)" % (CONVENCAO, pinos["vetor"].get("convencao")))
    s = pinos.get("saida")
    if not isinstance(s, dict) or not isinstance(s.get("path"), str) or not s["path"]:
        raise Recusa("campo ausente: saida.path")
    em = pinos.get("emenda")
    if not isinstance(em, dict) or any(not isinstance(em.get(k), str) or not em[k].strip() for k in CAMPOS_EMENDA):
        raise Recusa("campo emenda ausente ou com campo vazio (exigidos: %s)" % ", ".join(CAMPOS_EMENDA))
    if not isinstance(pinos.get("alvo_fp"), str):
        raise Recusa("campo ausente: alvo_fp (string decimal)")
    try:
        fp = float(pinos["alvo_fp"])
    except ValueError:
        raise Recusa("alvo_fp nao e' decimal")
    if fp != fp or fp in (float("inf"), float("-inf")):
        raise Recusa("alvo_fp nao e' finito")
    cod = pinos.get("codigo")
    if not isinstance(cod, dict) or any(not isinstance(cod.get(n), str) or not HEX64.fullmatch(cod[n]) for n in ARQ_CODIGO):
        raise Recusa("campo ausente ou mal formado: codigo[%s]" % ", ".join(ARQ_CODIGO))


def conferir_pinos(pinos):
    """Confere TODOS os sha256 antes de carregar qualquer coisa. Devolve ({campo: bytes}, {arquivo_de_codigo: bytes})."""
    validar_campos(pinos)
    cod = pinos["codigo"]
    brutos, codigo_raw = {}, {}
    for k in CAMPOS_ARQ:
        p = Path(pinos[k]["path"])
        if not p.is_file():
            raise Recusa("arquivo ausente: %s (%s)" % (k, p))
        raw = p.read_bytes()
        if sha(raw) != pinos[k]["sha256"]:
            raise Recusa("sha256 diferente do pino em %s (%s): %s" % (k, p, sha(raw)))
        brutos[k] = raw
    for nome in ARQ_CODIGO:
        raw = (HERE / nome).read_bytes()
        if sha(raw) != cod[nome]:
            raise Recusa("sha256 diferente do pino no codigo %s: %s" % (nome, sha(raw)))
        codigo_raw[nome] = raw
    return brutos, codigo_raw


def carregar_codigo(codigo_raw):
    """Executa os tres modulos a partir dos bytes JA conferidos (ordem: estimador, veredito, abertura)."""
    mods = {}
    for nome in ("estimator_v411.py", "veredito_v411.py", "abertura_v411.py"):
        modnome = nome[:-3]
        m = types.ModuleType(modnome)
        m.__file__ = str(HERE / nome)
        sys.modules[modnome] = m
        exec(compile(codigo_raw[nome], str(HERE / nome), "exec"), m.__dict__)
        mods[modnome] = m
    return mods


def _fl(x):
    if hasattr(x, "item") and getattr(x, "ndim", 1) == 0:
        return x.item()
    if hasattr(x, "tolist"):
        return x.tolist()
    raise TypeError("nao serializavel: %r" % type(x))


def _gravar_atomico(destino, raw):
    tmp = Path(str(destino) + ".tmp")
    with tmp.open("xb") as f:
        f.write(raw)
    if tmp.stat().st_size != len(raw):
        tmp.unlink()
        raise OSError("tamanho do temporario nao confere")
    if destino.exists():
        tmp.unlink()
        raise FileExistsError(str(destino))
    os.replace(tmp, destino)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pinos", required=True)
    ap.add_argument("--ensaio", action="store_true")
    a = ap.parse_args(argv)
    try:
        pinos = json.loads(Path(a.pinos).read_text(encoding="utf-8"))
        validar_campos(pinos)
    except (Recusa, OSError, ValueError) as e:
        print("RECUSA: %s" % e, file=sys.stderr)
        return 2
    saida = Path(pinos["saida"]["path"])
    sha_arq = Path(str(saida) + ".sha256")
    if saida.exists() or sha_arq.exists():
        print("RECUSA: a saida ou o .sha256 ja existe (a abertura e' uma vez so' por arquivo de pinos): %s" % (saida if saida.exists() else sha_arq),
              file=sys.stderr)
        return 4
    try:
        brutos, codigo_raw = conferir_pinos(pinos)
    except (Recusa, OSError, ValueError) as e:
        print("RECUSA: %s" % e, file=sys.stderr)
        return 2
    # a partir daqui tudo foi conferido por sha256
    mods = carregar_codigo(codigo_raw)
    ab = mods["abertura_v411"]
    np = ab.np
    try:
        rede = ab.carregar_rede(brutos["rede"])
        congelado = ab.carregar_congelado(brutos["congelado"])
        s0 = ab.carregar_s0(brutos["s0"])
        bg = ab.carregar_bg(brutos["bg"])
        ramos = json.loads(brutos["ramos"].decode("utf-8"))
        alvos = ab.ler_alvos_readme(brutos["readme"], pinos["readme"]["sha256"])
        alvos["fp"] = float(pinos["alvo_fp"])
        ab.conferir_integridade(rede, congelado, s0, bg, ramos)
    except ValueError as e:
        print("RECUSA (%s)" % e, file=sys.stderr)
        return 3 if str(e).startswith("integridade") else 2
    if a.ensaio:
        print("ENSAIO OK: pinos conferidos (insumos, pre_registro e codigo) e integridade de desenho aprovada; "
              "vetor NAO aberto (np.load nao executado; so' os bytes foram somados para o sha256); nenhuma saida gravada.")
        return 0
    try:
        y = np.load(io.BytesIO(brutos["vetor"]), allow_pickle=False)[pinos["vetor"]["chave"]]
    except Exception as e:  # chave ausente, formato errado
        print("RECUSA: nao consegui ler o vetor (%s: %s)" % (type(e).__name__, e), file=sys.stderr)
        return 5
    try:
        res = ab.abrir(y, rede, congelado, s0, bg, alvos, ramos, emenda=pinos["emenda"])
    except ValueError as e:
        print("RECUSA (%s); nada gravado" % e, file=sys.stderr)
        return 3
    out = {"versao": "v411", "pinos_de_entrada": {k: pinos[k] for k in CAMPOS_ARQ}, "pre_registro": pinos["pre_registro"],
           "vetor_convencao": pinos["vetor"]["convencao"], "emenda": pinos["emenda"], "alvo_fp": pinos["alvo_fp"],
           "pinos_do_codigo": pinos["codigo"],
           "alvos": {k: alvos[k] for k in ("H0", "sig", "chi2", "ndof", "fp", "sha256")}, "resultado": res}
    raw = (json.dumps(out, ensure_ascii=False, indent=1, default=_fl) + "\n").encode("utf-8")
    try:
        _gravar_atomico(saida, raw)
        _gravar_atomico(sha_arq, ("%s  %s\n" % (sha(raw), saida.name)).encode("utf-8"))
    except FileExistsError as e:
        print("RECUSA: apareceu durante a execucao: %s" % e, file=sys.stderr)
        return 4
    except OSError as e:
        print("RECUSA: gravacao falhou (%s); confira %s" % (e, saida), file=sys.stderr)
        return 5
    print("SAIDA GRAVADA: %s | sha256 %s | %d bytes | %s" % (saida, sha(raw), len(raw), sha_arq.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
