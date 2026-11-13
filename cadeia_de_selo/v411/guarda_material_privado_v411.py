# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] a licao D133 da v410: a MESMA guarda de material privado que a E03 da G1 usa, sobre TODOS os insumos pinados, ANTES do candidato
"""guarda_material_privado_v411.py -- varre os arquivos dados (ou, sem argumento, TODOS os insumos pinados da v411: os 18 embutidos, os 7 citados, os 5 textos da gerencia citados, as 9 falas e as copias duraveis em
v411\\insumos) com a guarda da E03 da custodia G1 (tools\\custodia_g1\\espelho_pares.py: os 7 termos da casa MAIS o conjunto privado de marcadores, carregado pela funcao da propria G1; os padroes NUNCA sao impressos
nem gravados). Grava GUARDA_MATERIAL_PRIVADO_v411.json (por arquivo: caminho, sha256 e a CONTAGEM de ocorrencias; nenhum trecho). rc 0 = nenhum insumo traz material privado; rc 1 = algum traz (o insumo so' pode entrar
por COPIA LIMPA, licao D133); rc 2 = a guarda nao carregou (PARAR: a guarda de 7 termos sozinha e' fraca). Nada e' escrito alem do JSON.
uso: python -B -X utf8 guarda_material_privado_v411.py [arquivo ...]"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "tools"))


def carregar_guarda():
    from custodia_g1 import espelho_pares as E   # noqa: E402   (a guarda da E03 da G1, a mesma funcao)
    return E, E.carregar_marcadores_privados()


def insumos_pinados():
    import delta_v411 as DL
    ps = [i_["arquivo"] for i_ in DL.INSUMOS_V411] + [c_["arquivo"] for c_ in DL.CITADOS_V411] + [g_["arquivo"] for g_ in DL.TEXTOS_DA_GERENCIA_CITADOS] + [f_["arquivo"] for f_ in DL.FALAS_V411]
    ins_ = os.path.join(HERE, "insumos")
    if os.path.isdir(ins_):
        for dp_, dn_, fn_ in os.walk(ins_):
            ps += [os.path.join(dp_, f_) for f_ in fn_ if ".bak_" not in f_ and not f_.endswith(".tmp")]
    return sorted(set(ps))


def varrer(paths):
    E, priv = carregar_guarda()
    out = []
    for p in paths:
        n = E.guarda_conta(p, priv)
        out.append({"arquivo": p, "sha256": hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None, "ocorrencias": n})
    return {"contrato": "GUARDA_MATERIAL_PRIVADO_v411", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "guarda": "tools\\custodia_g1\\espelho_pares.py (GUARDA + carregar_marcadores_privados + guarda_conta: a da E03)",
            "n_marcadores_privados": len(priv), "n_termos_da_casa": len(E.GUARDA), "n_arquivos": len(out), "arquivos": out,
            "com_material_privado": [x_["arquivo"] for x_ in out if x_["ocorrencias"]], "ilegiveis": [x_["arquivo"] for x_ in out if x_["ocorrencias"] is None],
            "limpo": all(x_["ocorrencias"] == 0 for x_ in out), "nota": "so' contagens; os padroes e os trechos nunca sao impressos nem gravados"}


if __name__ == "__main__":
    try:
        paths = sys.argv[1:] or insumos_pinados()
        rep = varrer(paths)
    except Exception as e:   # noqa: BLE001
        print("A GUARDA DE MATERIAL PRIVADO NAO CARREGOU: %s -- PARAR" % type(e).__name__)
        sys.exit(2)
    if not sys.argv[1:]:
        p = os.path.join(HERE, "GUARDA_MATERIAL_PRIVADO_v411.json")
        open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
    print("arquivos varridos: %d | com material privado: %d | ilegiveis: %d | marcadores privados carregados: %d" % (rep["n_arquivos"], len(rep["com_material_privado"]), len(rep["ilegiveis"]), rep["n_marcadores_privados"]))
    for a in rep["com_material_privado"]:
        print("  COM MATERIAL PRIVADO (entra so' por copia limpa):", a)
    sys.exit(0 if rep["limpo"] else 1)
