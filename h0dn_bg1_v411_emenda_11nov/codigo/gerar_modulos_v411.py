# -*- coding: utf-8 -*-
"""Gera, por script, os dois modulos da emenda v411 e os diffs (nenhum dado observado e' lido).

1. estimator_v411.py = estimator.py congelado (pasta B) com UMA mudanca em `evaluate`:
   a guarda 'data_outside_support' sai; a projecao no nulo vira so' diagnostico (+ chave support_l2).
2. veredito_v411.py = texto-fonte de `veredito_h0dn` do um.py (v410), extraido por script, com UMA mudanca de logica:
   o ramo (1) passa a depender so' de `portao_1_ok`.
Grava artefatos/DIFF_estimator_v410_para_v411.txt, artefatos/DIFF_veredito_v410_para_v411.txt e
artefatos/ORIGENS_MODULOS.json (sha256 e bytes das entradas e saidas; sha256 do texto-fonte v410).
"""
import difflib
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "artefatos"
B = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
UM = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
EST_FROZEN = B / "estimator.py"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin(p):
    b = Path(p).read_bytes()
    return {"path": str(Path(p).resolve()), "bytes": len(b), "sha256": sha(b)}


def replace_once(text, old, new, what):
    n = text.count(old)
    if n != 1:
        raise ValueError("%s: esperado 1 ocorrencia, achei %d" % (what, n))
    return text.replace(old, new)


def write_text(path, text):
    raw = text.encode("utf-8")
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(raw)
    assert tmp.stat().st_size == len(raw)
    tmp.replace(path)


def unified(a_text, b_text, a_name, b_name):
    return "".join(difflib.unified_diff(a_text.splitlines(True), b_text.splitlines(True), a_name, b_name, n=2))


def changed_original_lines(a_text, b_text):
    """Indices (0-based) das linhas do original removidas/alteradas."""
    a, b = a_text.splitlines(), b_text.splitlines()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ch = set()
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            ch.update(range(i1, i2))
    return sorted(ch)


# ---------------------------------------------------------------- 1. estimator
def gerar_estimator():
    # newline='' preserva os bytes do original (CRLF/LF) na comparacao
    raw = EST_FROZEN.read_bytes()
    orig = raw.decode("utf-8")
    crlf = "\r\n" in orig
    t = orig.replace("\r\n", "\n")
    # docstring do modulo (acrescenta a nota da emenda)
    t = replace_once(
        t,
        '"""Frozen linear estimator of centered synthetic H0DN and BG1 vectors.\n',
        '"""Frozen linear estimator of centered synthetic H0DN and BG1 vectors.\n'
        "v411 amendment: evaluate() no longer raises data_outside_support; the projection on the\n"
        "covariance null space is only reported (support_max_abs, support_l2). geometry() is unchanged.\n",
        "docstring do modulo")
    # docstring de evaluate
    t = replace_once(
        t,
        '    """No access to labels. data: local centered rows, BG centered parameters."""\n',
        '    """No access to labels. data: local centered rows, BG centered parameters.\n'
        "    v411: the null-space projection is a diagnostic only (no guard).\"\"\"\n",
        "docstring de evaluate")
    # a guarda sai; a norma l2 por linha entra
    old_guard = (
        "    if support_error > 1e-8*max(1.,np.max(np.abs(local))): raise ValueError('data_outside_support')\n")
    new_guard = (
        "    support_l2=np.linalg.norm(local@null,axis=1) if null.shape[1] else np.zeros(local.shape[0])  # v411: diagnostic, no guard\n")
    t = replace_once(t, old_guard, new_guard, "guarda data_outside_support")
    t = replace_once(
        t,
        "            'support_max_abs':np.array(support_error)}\n",
        "            'support_max_abs':np.array(support_error),'support_l2':support_l2}\n",
        "dicionario de retorno")
    if "data_outside_support" in t.replace("v411 amendment: evaluate() no longer raises data_outside_support", ""):
        raise ValueError("a string da guarda ainda aparece no codigo")
    out_text = t.replace("\n", "\r\n") if crlf else t
    dest = HERE / "estimator_v411.py"
    # grava BYTES (preserva o fim de linha do original)
    raw_out = out_text.encode("utf-8")
    tmp = dest.with_suffix(".py.tmp")
    tmp.write_bytes(raw_out)
    assert tmp.stat().st_size == len(raw_out)
    tmp.replace(dest)
    d = unified(orig.replace("\r\n", "\n"), t, "estimator.py (congelado, v410)", "estimator_v411.py")
    write_text(OUT / "DIFF_estimator_v410_para_v411.txt", d)
    # o diff so' pode tocar: docstring do modulo, docstring de evaluate, a linha da guarda, o return
    a_lines = orig.replace("\r\n", "\n").splitlines()
    tocadas = changed_original_lines(orig.replace("\r\n", "\n"), t)
    permitido = {i for i, ln in enumerate(a_lines)
                 if ln.startswith('"""Frozen linear estimator') or ln.startswith('    """No access to labels')
                 or ln.startswith("    if support_error > 1e-8") or ln.startswith("            'support_max_abs'")}
    assert set(tocadas) <= permitido, (tocadas, permitido)
    # geometry identica (texto-fonte)
    def func_src(text, name):
        lines = text.splitlines()
        i0 = next(i for i, ln in enumerate(lines) if ln.startswith("def %s(" % name))
        i1 = next(i for i in range(i0 + 1, len(lines)) if lines[i].startswith("def "))
        return "\n".join(lines[i0:i1]).rstrip() + "\n"
    g_a, g_b = func_src(orig.replace("\r\n", "\n"), "geometry"), func_src(t, "geometry")
    assert g_a == g_b
    return {"crlf": crlf, "linhas_originais_tocadas": [a_lines[i] for i in tocadas],
            "geometry_sha256_texto": sha(g_a.encode("utf-8")), "geometry_identica": True,
            "frozen": pin(EST_FROZEN), "v411": pin(dest)}


# ---------------------------------------------------------------- 2. veredito
def gerar_veredito():
    um_bytes = UM.read_bytes()
    um_text = um_bytes.decode("utf-8").replace("\r\n", "\n")
    lines = um_text.split("\n")
    idx = {}
    for i, ln in enumerate(lines):
        for nome in ("def _v410_h0dn_cabeca(", "def veredito_h0dn(", "def _v410_h0dn_vigia_arquivos("):
            if ln.startswith(nome):
                if nome in idx:
                    raise ValueError("definicao duplicada: " + nome)
                idx[nome] = i
    i_cab, i_ver, i_vig = idx["def _v410_h0dn_cabeca("], idx["def veredito_h0dn("], idx["def _v410_h0dn_vigia_arquivos("]
    assert i_cab < i_ver < i_vig

    def bloco(a, b):
        seg = lines[a:b]
        while seg and seg[-1].strip() == "":
            seg.pop()
        return "\n".join(seg) + "\n"          # como inspect.getsource: sem linhas em branco finais, com \n
    cab_v410 = bloco(i_cab, i_ver)
    ver_v410 = bloco(i_ver, i_vig)
    sha_ver_v410 = sha(ver_v410.encode("utf-8"))
    sha_cab_v410 = sha(cab_v410.encode("utf-8"))

    v = ver_v410
    v = replace_once(
        v, "def veredito_h0dn(z_null, z_tgl, D_esperado, covariancia_fisica_fechada, no_suporte, ramos):",
        "def veredito_h0dn_v411(z_null, z_tgl, D_esperado, portao_1_ok, ramos):", "assinatura")
    v = replace_once(
        v, '    """v410 -- A FUNCAO DE VEREDITO CONGELADA do teste H0DN x BG1 (D72 + E30 + D76): a PRIMEIRA que casa decide. Devolve (cabeca, outcome, ramo).\n',
        '    """v411 (EMENDA de 11/11, derivada textualmente de veredito_h0dn da v410) -- a funcao de veredito do teste H0DN x BG1 (D72 + E30 + D76): a PRIMEIRA que casa decide. Devolve (cabeca, outcome, ramo).\n'
        "    EMENDA: a assinatura troca (covariancia_fisica_fechada, no_suporte) por portao_1_ok; so' o ramo (1) muda; (2) a (6) ficam textualmente iguais.\n",
        "docstring linha 1")
    v = replace_once(
        v, "(1) INCONCLUSIVE_SYSTEMATICS se a covariancia fisica nao estiver fechada (G3/G4) ou o vetor estiver fora do suporte;",
        "(1) INCONCLUSIVE_SYSTEMATICS se o primeiro portao do rito (reproducao do numero local publicado, centragem na referencia do fundo, impressao digital) falhar (portao_1_ok falso);",
        "docstring ramo 1")
    v = replace_once(
        v, "    if not covariancia_fisica_fechada or not no_suporte:\n",
        "    if not portao_1_ok:\n", "ramo 1")
    ver_v411 = v

    corpo = (
        '# -*- coding: utf-8 -*-\n'
        '"""v411 -- funcao de veredito emendada do teste H0DN x BG1 (nenhum dado observado e\' lido).\n'
        'GERADO por gerar_modulos_v411.py a partir do texto-fonte de veredito_h0dn do um.py (v410); nao editar a mao.\n'
        'sha256 do texto-fonte v410 (estilo inspect.getsource): ' + sha_ver_v410 + '\n'
        '"""\n\n\n' + cab_v410 + "\n\n" + ver_v411)
    dest = HERE / "veredito_v411.py"
    write_text(dest, corpo)
    d = unified(ver_v410, ver_v411, "veredito_h0dn (um.py v410)", "veredito_h0dn_v411")
    write_text(OUT / "DIFF_veredito_v410_para_v411.txt", d)
    # so' podem mudar: a linha 'def', a docstring (linhas que comecam por aspas triplas ou pelo texto de ramos) e o ramo (1)
    a_lines = ver_v410.splitlines()
    tocadas = changed_original_lines(ver_v410, ver_v411)
    for i in tocadas:
        ln = a_lines[i]
        assert (ln.startswith("def veredito_h0dn(") or ln.lstrip().startswith('"""v410 --')
                or ln.lstrip().startswith("(1) INCONCLUSIVE_SYSTEMATICS")
                or "(1) INCONCLUSIVE_SYSTEMATICS" in ln
                or ln.startswith("    if not covariancia_fisica_fechada")), ln
    # corpo dos ramos (2) a (6): as linhas apos o ramo (1) sao iguais
    def depois_ramo1(text):
        ls = text.splitlines()
        k = next(i for i, ln in enumerate(ls) if ln.startswith('        return V_["inconclusivo"]'))
        return ls[k:]
    assert depois_ramo1(ver_v410) == depois_ramo1(ver_v411)
    return {"um_py": {"path": str(UM), "bytes": len(um_bytes), "sha256": sha(um_bytes)},
            "fonte_v410_veredito_h0dn_sha256": sha_ver_v410, "fonte_v410_veredito_h0dn_bytes": len(ver_v410.encode("utf-8")),
            "fonte_v410_cabeca_sha256": sha_cab_v410,
            "linhas_do_original_tocadas": [a_lines[i] for i in tocadas],
            "ramos_2_a_6_textualmente_iguais": True, "v411": pin(dest)}


def main():
    OUT.mkdir(exist_ok=True)
    r_est = gerar_estimator()
    r_ver = gerar_veredito()
    rec = {"estimator": r_est, "veredito": r_ver,
           "diffs": {"estimator": pin(OUT / "DIFF_estimator_v410_para_v411.txt"),
                     "veredito": pin(OUT / "DIFF_veredito_v410_para_v411.txt")}}
    write_text(OUT / "ORIGENS_MODULOS.json", json.dumps(rec, ensure_ascii=False, indent=1))
    print(json.dumps({"estimator_tocadas": r_est["linhas_originais_tocadas"],
                      "veredito_tocadas": r_ver["linhas_do_original_tocadas"],
                      "sha_fonte_v410": r_ver["fonte_v410_veredito_h0dn_sha256"],
                      "geometry_identica": r_est["geometry_identica"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
