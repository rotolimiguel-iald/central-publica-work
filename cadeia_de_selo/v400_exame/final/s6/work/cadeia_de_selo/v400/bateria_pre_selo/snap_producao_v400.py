# -*- coding: utf-8 -*-
"""snap_producao_v400.py -- SO LEITURA. Fotografa a Bancada de producao e o Nos para provar, antes e depois do ensaio pre_selo da v400, que nada foi gravado.
uso: python -I -B -X utf8 snap_producao_v400.py <rotulo: antes|depois|final> <pasta de destino (sandbox curto)>
(antes = antes do ensaio; depois = logo depois do ensaio; final = depois de TUDO que esta tarefa leu da producao, inclusive a conferencia do recibo pelo esboco)
Grava na pasta de destino:
  fp_bancada_<rotulo>.json : a lista COMPLETA de C:\\IALD\\Bancada_Um, uma linha [caminho relativo, tipo, tamanho, mtime_ns] por entrada (arquivos e pastas; link simbolico entra como folha; juncao e' seguida uma vez);
  fp_nos_<rotulo>.json.gz  : o mesmo para a pasta do Nos (so' o resumo vai ao recibo: contagem e sha256 da lista);
  chaves_<rotulo>.json     : sha256 e tamanho dos arquivos-chave (manifesto canonico da Bancada; um.py, selo, core e manifesto do kernel do Nos), lidos por script.
Nao escreve na Bancada nem no Nos (so' os abre para leitura). Nada e' digitado de memoria."""
import gzip
import hashlib
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
BAN = os.path.join("C:" + os.sep, "IALD", "Bancada_Um")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
CHAVES = (("bancada", BAN, "canonical_contracts.json"), ("nos", NOS, "um.py"), ("nos", NOS, "um_absoluto_selo.json"),
          ("nos", NOS, "tgl_kernel_proof_manifest.json"), ("nos", NOS, "um_absoluto.json"))


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 22), b""):
            h.update(bloco)
    return h.hexdigest()


def varrer(raiz):
    """lista ordenada de [rel, tipo, tamanho, mtime_ns]; o prefixo \\\\?\\ evita o limite de 260 caracteres; link simbolico nao e' seguido; juncao SIM (uma vez por destino real,
    sem ciclo): o Nos tem uma so', tgl_kernel/.lake/packages, e a lista tem de cobrir o que ela alcanca."""
    saida, erros = [], []
    visitados = {os.path.realpath(raiz)}
    pilha = [("", "\\\\?\\" + raiz)]
    while pilha:
        rel, p = pilha.pop()
        try:
            with os.scandir(p) as it:
                for e in it:
                    r = (rel + "/" + e.name) if rel else e.name
                    try:
                        st = e.stat(follow_symlinks=False)
                        junc = e.is_junction()
                        link = e.is_symlink()
                        pasta = e.is_dir(follow_symlinks=False)
                    except OSError as exc:
                        erros.append([r, repr(exc)])
                        continue
                    tipo = "J" if junc else ("L" if link else ("D" if pasta else "F"))
                    saida.append([r, tipo, 0 if pasta else st.st_size, st.st_mtime_ns])
                    if tipo in ("D", "J"):
                        alvo_p = os.path.join(p, e.name)
                        if tipo == "J":
                            real = os.path.realpath(alvo_p)
                            if real in visitados:
                                continue
                            visitados.add(real)
                        pilha.append((r, alvo_p))
        except OSError as exc:
            erros.append([rel, repr(exc)])
    saida.sort(key=lambda x: x[0])
    return saida, erros


def sha_lista(lista):
    h = hashlib.sha256()
    for r, t, s, m in lista:
        h.update(("%s\t%s\t%d\t%d\n" % (r, t, s, m)).encode("utf-8"))
    return h.hexdigest()


def main(argv):
    if len(argv) != 3 or argv[1] not in ("antes", "depois", "final"):
        print("uso: snap_producao_v400.py antes|depois|final <pasta de destino>")
        return 2
    rot, dest = argv[1], os.path.abspath(argv[2])
    if not os.path.isdir(dest):
        print("a pasta de destino nao existe:", dest)
        return 2
    quando = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    resumo = {"rotulo": rot, "quando": quando}
    for nome, raiz in (("bancada", BAN), ("nos", NOS)):
        t0 = time.time()
        lista, erros = varrer(raiz)
        resumo[nome] = {"raiz": raiz, "n_entradas": len(lista), "n_arquivos": sum(1 for x in lista if x[1] == "F"), "n_pastas": sum(1 for x in lista if x[1] == "D"),
                        "n_juncoes_ou_links": sum(1 for x in lista if x[1] in ("J", "L")), "bytes_arquivos": sum(x[2] for x in lista if x[1] == "F"),
                        "sha256_da_lista": sha_lista(lista), "erros_de_leitura": erros, "segundos": round(time.time() - t0, 1)}
        alvo = os.path.join(dest, "fp_%s_%s.json" % (nome, rot))
        dados = json.dumps(lista, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        if nome == "nos":
            alvo += ".gz"
            dados = gzip.compress(dados, 6)
        if os.path.exists(alvo):
            print("ja existe, nao sobrescrevo:", alvo)
            return 2
        with open(alvo + ".tmp", "wb") as fh:
            fh.write(dados)
        assert os.path.getsize(alvo + ".tmp") == len(dados)
        os.replace(alvo + ".tmp", alvo)
        resumo[nome]["arquivo_da_lista"] = alvo
    chaves = []
    for dono, base, rel in CHAVES:
        p = os.path.join(base, rel)
        chaves.append({"dono": dono, "arquivo": rel, "path": p, "bytes": os.path.getsize(p), "sha256": sha(p)})
    resumo["chaves"] = chaves
    alvo = os.path.join(dest, "chaves_%s.json" % rot)
    if os.path.exists(alvo):
        print("ja existe, nao sobrescrevo:", alvo)
        return 2
    with open(alvo + ".tmp", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(resumo, ensure_ascii=False, indent=1) + "\n")
    os.replace(alvo + ".tmp", alvo)
    print(json.dumps({"rotulo": rot, "bancada": {k: resumo["bancada"][k] for k in ("n_entradas", "n_arquivos", "sha256_da_lista", "segundos")},
                      "nos": {k: resumo["nos"][k] for k in ("n_entradas", "n_arquivos", "sha256_da_lista", "segundos")},
                      "erros": len(resumo["bancada"]["erros_de_leitura"]) + len(resumo["nos"]["erros_de_leitura"]),
                      "chaves": {"%s/%s" % (c["dono"], c["arquivo"]): c["sha256"][:16] for c in chaves}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
