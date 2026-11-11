# -*- coding: utf-8 -*-
r"""Errata AO LADO no G1 (central.py, C3), 11/11/2026, claude-site-custodia: a guarda de +-50% da cadeia de selo nao afrouxa; fora da faixa,
so segue com a declaracao que confira a contagem e o sha256 da lista exata de hoje. Edita em bytes, preserva CRLF; o backup ja foi feito."""
import os
import sys

P = r"C:\IALD\Central de Patentes\tools\custodia_g1\central.py"
b = open(P, "rb").read()
assert b.count(b"\r\n") == b.count(b"\n"), "central.py nao e CRLF puro"
t = b.decode("utf-8").replace("\r\n", "\n")

S1_A = r'''    for d in (v, v + "_selo"):
        src = c.CS / d
'''
S1_N = r'''    listas_cad = {}   # AO LADO (11/11/2026, v410): a lista exata do que entra, para a guarda de +-50% (abaixo)
    for d in (v, v + "_selo"):
        src = c.CS / d
'''
S2_A = r'''        ent, fora_sub, grandes = 0, {}, []
        for p in src.rglob("*"):'''
S2_N = r'''        ent, fora_sub, grandes = 0, {}, []
        listas_cad[d] = []
        for p in src.rglob("*"):'''
S3_A = r'''            shutil.copyfile(p, dst)
            ent += 1
        cad["pastas"][d] = {"arquivos_no_cofre": ent,'''
S3_N = r'''            shutil.copyfile(p, dst)
            ent += 1
            listas_cad[d].append(rel.as_posix())
        cad["pastas"][d] = {"arquivos_no_cofre": ent,'''
S4_A = r'''            if not 0.5 <= r <= 1.5:
                raise Parar("a cadeia de selo copiada (%d arquivos) está fora de ±50%% da anterior (%d): diretório de ensaio novo entrando em silêncio?"
                            % (cad["pastas"][v]["arquivos_no_cofre"], a_["arquivos_no_cofre"]))'''
S4_N = r'''            if not 0.5 <= r <= 1.5:
                # AO LADO (11/11/2026, claude-site-custodia; a C3 da v410 parou aqui com 1174 contra 697): a guarda NÃO afrouxa. Fora da faixa,
                # só segue com a DECLARAÇÃO work\custodia_G1\decisoes\CADEIA_DE_SELO_FORA_DA_FAIXA_vNNN.json que confira a contagem e o sha256
                # da lista exata de hoje (um arquivo a mais ou a menos = PARAR de novo). Sem ela, grava o candidato na pasta de trabalho e PARA.
                lst = sorted(listas_cad.get(v, []))
                h = hashlib.sha256("\n".join(lst).encode("utf-8")).hexdigest()
                dec = _cadeia_fora_da_faixa_declarada(ctx, len(lst), h)
                if dec is None:
                    por_pasta = {}
                    for x in lst:
                        k = x.split("/")[0] if "/" in x else "(primeiro nivel)"
                        por_pasta[k] = por_pasta.get(k, 0) + 1
                    cand = {"versao": v, "arquivos_no_cofre": len(lst), "lista_sha256": h, "anterior": ant,
                            "arquivos_no_cofre_anterior": a_["arquivos_no_cofre"], "razao": round(r, 3),
                            "por_pasta": dict(sorted(por_pasta.items())), "lista": lst}
                    util.mkdir(ctx.W)
                    pc = ctx.W / ("C3_CADEIA_FORA_DA_FAIXA_%s_candidato.json" % v)
                    util.escrever_json(pc, cand, backup=False)
                    raise Parar("a cadeia de selo copiada (%d arquivos) está fora de ±50%% da anterior (%d): diretório de ensaio novo entrando em silêncio?"
                                % (cad["pastas"][v]["arquivos_no_cofre"], a_["arquivos_no_cofre"]), ["candidato com a lista exata: %s" % pc])
                cad["fora_da_faixa_declarado"] = dec'''
S5_A = r'''def _ap_c3(ctx):'''
S5_N = r'''def _cadeia_fora_da_faixa_declarada(ctx, n, h):
    r"""[AO LADO, 11/11/2026, claude-site-custodia] A declaração de que a cadeia de selo fora de ±50% da anterior foi EXAMINADA (nenhum
    diretório de ensaio novo entrando calado): work\custodia_G1\decisoes\CADEIA_DE_SELO_FORA_DA_FAIXA_vNNN.json = {"versao",
    "arquivos_no_cofre", "lista_sha256", "por", "exame"}. Vale só para a versão corrente e só se a contagem e o sha256 da lista de hoje
    forem idênticos aos declarados. Sem o arquivo: None (a guarda para, como era). Arquivo que não confere: PARAR."""
    p = ctx.c.G1 / "decisoes" / ("CADEIA_DE_SELO_FORA_DA_FAIXA_%s.json" % ctx.versao)
    if not p.is_file():
        return None
    d = util.ler_json(p)
    if d.get("versao") != ctx.versao or d.get("arquivos_no_cofre") != n or d.get("lista_sha256") != h:
        raise Parar("a declaração da cadeia de selo fora da faixa não confere com a cópia de hoje (versão, contagem ou sha256 da lista)", [str(p)])
    return {"declaracao": str(p), "sha16": util.sha16(p), "por": d.get("por"), "exame": d.get("exame")}


def _ap_c3(ctx):'''

for a, n in ((S1_A, S1_N), (S2_A, S2_N), (S3_A, S3_N), (S4_A, S4_N), (S5_A, S5_N)):
    k = t.count(a)
    if k != 1:
        sys.exit("trecho encontrado %d vezes: %r" % (k, a[:80]))
    t = t.replace(a, n, 1)
nb = t.replace("\n", "\r\n").encode("utf-8")
tmp = P + ".tmp"
open(tmp, "wb").write(nb)
assert os.path.getsize(tmp) == len(nb)
os.replace(tmp, P)
print(len(b), "->", len(nb), "B | CRLF", nb.count(b"\r\n"), "| LF solto", nb.count(b"\n") - nb.count(b"\r\n"))
