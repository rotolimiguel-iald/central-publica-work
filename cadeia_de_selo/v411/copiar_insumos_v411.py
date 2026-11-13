# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] as COPIAS DURAVEIS dos insumos da v411 em v411\insumos e a lista CONGELADA das falas (VERBATIM_CONGELADO_v411.json)
"""copiar_insumos_v411.py -- copia de BYTES, para v411\\insumos, tudo o que a v411 pina (DESENHO_v411 secoes 2 e 3, lido pelo delta): os 18 insumos EMBUTIDOS (prefixo h0dn_), os 7 CITADOS por sha256 (prefixo citado_),
os 5 textos da gerencia citados e as 9 falas do operador (em insumos\\cunhagens, com o nome original). Cada copia e' conferida por sha256 contra o arquivo de origem e contra o sha16 do DESENHO; o que ja' existe e e' igual fica;
o que difere ABORTA (nao sobrescreve). Depois grava VERBATIM_CONGELADO_v411.json (a lista congelada das 9 falas: arquivo, sha256, bytes, autor, papel; a mesma estrutura do da v410) e roda a guarda de material privado
(guarda_material_privado_v411.py, a da E03 da G1) sobre as copias: insumo com material privado entra so' por COPIA LIMPA (D133) e este script PARA. Veto: nada da pasta do Kimi e' copiado.
uso: python -B -X utf8 copiar_insumos_v411.py"""
import datetime, hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens")
os.makedirs(CUN, exist_ok=True)
plano = [(i_["arquivo"], os.path.join(INS, "h0dn_" + i_["nome"]), i_["sha256"]) for i_ in DL.INSUMOS_V411]
plano += [(c_["arquivo"], os.path.join(INS, "citado_" + c_["nome"]), c_["sha256"]) for c_ in DL.CITADOS_V411]
plano += [(g_["arquivo"], os.path.join(CUN, g_["nome"]), g_["sha256"]) for g_ in DL.TEXTOS_DA_GERENCIA_CITADOS]
plano += [(f_["arquivo"], os.path.join(CUN, f_["nome"]), f_["sha256"]) for f_ in DL.FALAS_V411]
assert len({d_ for _, d_, _ in plano}) == len(plano) == len(DL.INSUMOS_V411) + len(DL.CITADOS_V411) + len(DL.TEXTOS_DA_GERENCIA_CITADOS) + len(DL.FALAS_V411) == 18 + 7 + 6 + 11, "destinos repetidos"   # (12/11, AO LADO: 6 textos da gerencia, 11 falas)
assert not any("kimi" in s_.lower().replace("ordem_ao_kimi", "").split(os.sep) for s_, _, _ in plano), "veto: nada da pasta do Kimi"
rep = []
for src, dst, h in plano:
    b = open(src, "rb").read(); assert sha(b) == h, ("a origem nao tem o sha256 do DESENHO", src)
    if os.path.exists(dst):
        assert open(dst, "rb").read() == b, ("a copia ja existe e DIFERE da origem: nao sobrescrevo", dst)
        estado = "igual"
    else:
        open(dst + ".tmp", "wb").write(b); assert os.path.getsize(dst + ".tmp") == len(b); os.replace(dst + ".tmp", dst); estado = "copiado"
    assert sha(open(dst, "rb").read()) == h
    rep.append({"origem": src, "copia": dst, "sha256": h, "bytes": len(b), "estado": estado})
cong = {"contrato": "VERBATIM_CONGELADO_v411", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "n": len(DL.FALAS_V411), "arquivos": [f_["arquivo"] for f_ in DL.FALAS_V411],
        "registro": [{"arquivo": f_["arquivo"], "sha256": f_["sha256"], "bytes": f_["bytes"], "autor": "operador", "papel": f_["papel"]} for f_ in DL.FALAS_V411],
        "fora_do_desenho": {n_: DL.sha16_arquivo(os.path.join(DL.CUN, n_)) for n_ in DL.VERBATIM_FORA_DO_DESENHO_V411_NOMEADAS if os.path.exists(os.path.join(DL.CUN, n_))},
        "textos_da_gerencia_citados_por_sha256": [{"arquivo": g_["arquivo"], "sha256": g_["sha256"], "bytes": g_["bytes"], "autor": g_["autor"]} for g_ in DL.TEXTOS_DA_GERENCIA_CITADOS],
        "nota": "as %d falas do operador de 11 e 12/11/2026 que a v411 CITA por data e sha256 (D181: o programa e o artigo nao as transcrevem; o texto fica na casa; DESENHO_v411 secao 3, a tabela, lida por script; sha16 do DESENHO conferido contra cada arquivo); as falas de 06 a 10/11 ja estao no um.py v410 e nao entram de novo; ficam FORA as de 11/11 sobre o fecho (H, U), a torcao, a direcao, a carga e a Primeira Lei (esperam nomes), a da Central publica (custodia) e a listada em fora_do_desenho; os textos da gerencia entram so' citados por sha256 (nao sao falas do operador)" % len(DL.FALAS_V411)}
pc = os.path.join(HERE, "VERBATIM_CONGELADO_v411.json")
bc = json.dumps(cong, ensure_ascii=False, indent=1).encode("utf-8")
if os.path.exists(pc) and open(pc, "rb").read() != bc:
    open(pc + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(open(pc, "rb").read())
open(pc + ".tmp", "wb").write(bc); assert os.path.getsize(pc + ".tmp") == len(bc); os.replace(pc + ".tmp", pc)
pm = os.path.join(HERE, "MANIFESTO_INSUMOS_v411.json")
bm = json.dumps({"contrato": "MANIFESTO_INSUMOS_v411", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "n": len(rep), "copias": rep}, ensure_ascii=False, indent=1).encode("utf-8")
open(pm + ".tmp", "wb").write(bm); os.replace(pm + ".tmp", pm)
r = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "guarda_material_privado_v411.py")], capture_output=True, text=True, encoding="utf-8")
print("copias:", sum(1 for x_ in rep if x_["estado"] == "copiado"), "novas,", sum(1 for x_ in rep if x_["estado"] == "igual"), "iguais | congelado:", cong["n"], "falas, sha16", sha(bc)[:16])
print("guarda de material privado:", r.stdout.strip(), "| rc", r.returncode)
sys.exit(0 if r.returncode == 0 else 1)
