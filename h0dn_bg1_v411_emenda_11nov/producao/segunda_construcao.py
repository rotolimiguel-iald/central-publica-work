"""Segunda construcao independente do vetor observado local do teste H0DN x BG1.

Regras (ordem do operador, 11/11/2026): comparar SO HASHES; nenhum valor do
vetor e' impresso, registrado, plotado ou resumido. Sobre o vetor so saem:
dtype, forma, sha256 dos bytes e booleanos de igualdade (e, se os hashes das
duas construcoes diferirem, a contagem de entradas que diferem e dois
booleanos allclose).

Metodo: importa o pacote PUBLICO h0_constrainer da colaboracao, troca
h0_constrainer.solver.solve_system por uma funcao que levanta uma excecao
propria carregando o equation_data (o solver NUNCA roda), roda main() da
colaboracao com a configuracao de BASE (base_variants_config.ini, que e' a V00
de variants.ini) com stdout/stderr em os.devnull, e le yval do equation_data.

Uso:  C:\\Python314\\python.exe -X utf8 segunda_construcao.py
(o orquestrador lanca dois processos-trabalhador; o segundo nao grava o npz).
"""

import contextlib
import configparser
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

WORK = Path(r"C:\IALD\Central de Patentes\work")
UPSTREAM = WORK / "astra_bell_fock_tt_05nov" / "h0dn_bg1_06nov" / "network" / "upstream"
PKG_ROOT = UPSTREAM / "h0_constrainer"               # contem a pasta do pacote h0_constrainer
PKG_DIR = PKG_ROOT / "h0_constrainer"
CFG_DIR = PKG_ROOT / "configs"
CFG_BASE = CFG_DIR / "base_variants_config.ini"
CFG_VARIANTS = CFG_DIR / "variants.ini"
CFG_PLAIN = CFG_DIR / "config.ini"
DATA_DIR = UPSTREAM / "data"
NETWORK_NPZ = UPSTREAM.parent / "network.npz"
KIMI_NPZ = WORK / "h0dn_bg1_v410_09nov" / "kimi" / "y_obs.npz"
OUT_DIR = WORK / "h0dn_bg1_v411_emenda_11nov" / "producao"
OUT_NPZ = OUT_DIR / "vetor_y255.npz"
OUT_RECIBO = OUT_DIR / "RECIBO_SEGUNDA_CONSTRUCAO.json"


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class _SolverBlocked(Exception):
    """Levantada no lugar de solve_system; carrega o equation_data."""

    def __init__(self, equation_data):
        super().__init__("solve_system bloqueado")
        self.equation_data = equation_data


def _blocked_solve_system(equation_data):
    raise _SolverBlocked(equation_data)


# ---------------------------------------------------------------------------
# TRABALHADOR (um processo por construcao)
# ---------------------------------------------------------------------------
def worker(run_id, out_json, write_npz, compare_npz):
    import numpy as np

    sys.dont_write_bytecode = True           # nao escrever __pycache__ na pasta da colaboracao
    sys.path.insert(0, str(PKG_ROOT))
    result = {"run": run_id}

    tmpdir = Path(tempfile.mkdtemp(prefix="h0dn_seg_"))
    try:
        # configuracao de BASE, com datadir absoluto e sem log/arquivo de saida
        cp = configparser.ConfigParser()
        cp.read(CFG_BASE)
        cp["DEFAULT"]["datadir"] = str(DATA_DIR) + os.sep
        cp["DEFAULT"]["verbose"] = "False"
        cp["DEFAULT"]["warn"] = "False"
        cp["DEFAULT"]["logfile"] = "none"
        cp["DEFAULT"]["savefile"] = "none"
        cfg_tmp = tmpdir / "base_v00_producao.ini"
        with open(cfg_tmp, "w", encoding="utf-8") as f:
            cp.write(f)
        result["config_chaves_usadas"] = {k: v for k, v in cp["DEFAULT"].items()}

        devnull = open(os.devnull, "w")
        eq = None
        err = None
        with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
            import warnings
            warnings.simplefilter("ignore")
            try:
                import h0_constrainer.solver as solver_mod
                solver_mod.solve_system = _blocked_solve_system
                from h0_constrainer import main as main_mod
                from h0_constrainer import config_reader as cr
                main_mod.main(str(cfg_tmp))
                err = "main terminou sem passar pelo solver (inesperado)"
            except _SolverBlocked as e:
                eq = e.equation_data
            except BaseException as e:          # noqa: BLE001  (so classe e localizacao)
                tb = traceback.extract_tb(e.__traceback__)
                err = {"classe": type(e).__name__,
                       "locais": [f"{Path(t.filename).name}:{t.lineno}" for t in tb[-4:]]}
            read_keys = [[k, str(v)] for k, v in cr.give_keys()[0]] if "cr" in dir() else None
        devnull.close()
        result["config_chaves_lidas"] = read_keys

        if eq is None:
            result["erro"] = err
            Path(out_json).write_text(json.dumps(result), encoding="utf-8")
            return 2

        net = np.load(NETWORK_NPZ, allow_pickle=False)
        A, C = net["A"], net["C"]
        row_names = [str(x) for x in net["row_names"]]
        param_names = [str(x) for x in net["param_names"]]
        h_index = int(net["h_index"])

        y = eq["yval"]
        coeffs, covar = eq["coeffs"], eq["covar"]
        ihub = int(eq["ihub"])
        eq_param_names = [str(p["objname"]) for p in eq["parinfo"]]

        result["conferencias"] = {
            "yval_dtype": str(y.dtype),
            "yval_forma": list(y.shape),
            "yval_dtype_float64": bool(y.dtype == np.float64),
            "yval_forma_255": bool(y.shape == (255,)),
            "yval_todo_finito": bool(np.isfinite(y).all()),
            "coeffs_forma_igual_A": bool(coeffs.shape == A.shape),
            "covar_forma_igual_C": bool(covar.shape == C.shape),
            "coeffs_array_equal_A": bool(np.array_equal(coeffs, A)),
            "covar_array_equal_C": bool(np.array_equal(covar, C)),
            "eq_descr_igual_row_names": bool(list(eq["eq_descr"]) == row_names),
            "nomes_param_iguais_param_names": bool(eq_param_names == param_names),
            "ihub": ihub,
            "h_index": h_index,
            "ihub_igual_h_index_igual_63": bool(ihub == h_index == 63),
            "neq": int(eq["neq"]),
            "npars": int(eq["npars"]),
        }

        yc = np.ascontiguousarray(y, dtype=np.float64)
        y_sha = sha256_bytes(yc.tobytes())
        result["y_sha256"] = y_sha
        result["y_dtype"] = str(y.dtype)
        result["y_forma"] = list(y.shape)

        # grava o npz (so a rodada 1), escrita atomica: temporario -> tamanho -> renomear
        if write_npz:
            if OUT_NPZ.exists():
                result["erro"] = "vetor_y255.npz ja existia; nao sobrescrito"
                Path(out_json).write_text(json.dumps(result), encoding="utf-8")
                return 3
            tmp_npz = OUT_DIR / "vetor_y255.npz.tmp"
            if tmp_npz.exists():
                tmp_npz.unlink()
            with open(tmp_npz, "xb") as f:
                np.savez(f, y_uncentered=yc)
            size = tmp_npz.stat().st_size
            if size < yc.nbytes:
                tmp_npz.unlink()
                result["erro"] = "npz temporario menor que o vetor"
                Path(out_json).write_text(json.dumps(result), encoding="utf-8")
                return 3
            os.rename(tmp_npz, OUT_NPZ)           # falha se o destino existir
            back = np.load(OUT_NPZ, allow_pickle=False)
            back_y = back["y_uncentered"]
            result["npz"] = {
                "arquivo": str(OUT_NPZ),
                "bytes": OUT_NPZ.stat().st_size,
                "sha256_arquivo": sha256_file(OUT_NPZ),
                "chaves": list(back.files),
                "so_a_chave_y_uncentered": bool(list(back.files) == ["y_uncentered"]),
                "dtype": str(back_y.dtype),
                "forma": list(back_y.shape),
                "sha256_y_relido": sha256_bytes(np.ascontiguousarray(back_y).tobytes()),
                "relido_igual_ao_construido": bool(np.array_equal(back_y, yc)),
            }

        # comparacao com a primeira construcao (so na rodada 1)
        if write_npz:
            kimi_file_sha = sha256_file(KIMI_NPZ)
            kd = np.load(KIMI_NPZ, allow_pickle=False)
            ky = kd["y_uncentered"]
            ky_sha = sha256_bytes(ky.tobytes())
            comp = {
                "sha256_arquivo_y_obs_npz": kimi_file_sha,
                "bytes_arquivo_y_obs_npz": KIMI_NPZ.stat().st_size,
                "chave_y_uncentered": {
                    "dtype": str(ky.dtype),
                    "forma": list(ky.shape),
                    "sha256_tobytes": ky_sha,
                },
                "hash_igual": bool(ky_sha == y_sha),
            }
            if ky_sha != y_sha:
                # unico detalhe permitido: contagem e allclose
                if ky.shape == yc.shape and np.issubdtype(ky.dtype, np.floating):
                    comp["n_entradas_diferentes"] = int((yc != ky).sum())
                    comp["allclose_atol_1e-12"] = bool(np.allclose(yc, ky, rtol=0, atol=1e-12))
                    comp["allclose_atol_1e-9"] = bool(np.allclose(yc, ky, rtol=0, atol=1e-9))
                else:
                    comp["comparacao_entrada_a_entrada"] = "impossivel: dtype/forma diferentes"
            result["primeira_construcao"] = comp

        # comparacao com a rodada 1 (so na rodada 2): relê o npz gravado pela rodada 1
        if compare_npz:
            pd_ = np.load(compare_npz, allow_pickle=False)["y_uncentered"]
            prev_sha = sha256_bytes(np.ascontiguousarray(pd_).tobytes())
            comp2 = {"sha256_rodada1_relido": prev_sha, "hash_igual_rodada1": bool(prev_sha == y_sha)}
            if prev_sha != y_sha:
                comp2["n_entradas_diferentes"] = int((yc != pd_).sum())
                comp2["allclose_atol_1e-12"] = bool(np.allclose(yc, pd_, rtol=0, atol=1e-12))
                comp2["allclose_atol_1e-9"] = bool(np.allclose(yc, pd_, rtol=0, atol=1e-9))
            result["comparacao_com_rodada1"] = comp2

        Path(out_json).write_text(json.dumps(result), encoding="utf-8")
        return 0
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# ORQUESTRADOR
# ---------------------------------------------------------------------------
def collab_hashes():
    out = {"pacote_py": {}, "configs": {}, "dados": {}}
    for p in sorted(PKG_DIR.glob("*.py")):
        out["pacote_py"][p.name] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    for p in (CFG_BASE, CFG_PLAIN, CFG_VARIANTS):
        out["configs"][p.name] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    for p in sorted(DATA_DIR.iterdir()):
        if p.is_file():
            out["dados"][p.name] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    return out


def run_worker(run_id, write_npz, compare_npz=None):
    out_json = Path(tempfile.gettempdir()) / f"h0dn_seg_rodada{run_id}_{os.getpid()}.json"
    cmd = [sys.executable, "-X", "utf8", str(Path(__file__).resolve()),
           "--worker", str(run_id), str(out_json)]
    if write_npz:
        cmd.append("--write-npz")
    if compare_npz:
        cmd += ["--compare-npz", str(compare_npz)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    res = None
    if out_json.exists():
        res = json.loads(out_json.read_text(encoding="utf-8"))
        out_json.unlink()
    # stdout/stderr do trabalhador: so o tamanho (ele nao imprime nada de proposito)
    return proc.returncode, res, len(proc.stdout), len(proc.stderr)


def main_orch():
    import numpy as np
    import scipy
    import pandas

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if OUT_NPZ.exists():
        print("ERRO: vetor_y255.npz ja existe; nada feito.")
        return 1

    # conferencias de configuracao (sem dado)
    base = configparser.ConfigParser()
    base.read(CFG_BASE)
    plain = configparser.ConfigParser()
    plain.read(CFG_PLAIN)
    dbase = {k: v.strip() for k, v in base["DEFAULT"].items() if k != "warn"}
    dplain = {k: v.strip() for k, v in plain["DEFAULT"].items() if k != "warn"}
    vpar = configparser.ConfigParser()
    vpar.read(CFG_VARIANTS)
    v00 = [s for s in vpar.sections() if s.startswith("V00")]
    cfg_checks = {
        "config_ini_equivale_base_variants_config_exceto_warn": bool(dbase == dplain),
        "variants_meta_base_e_base_variants_config_ini": bool(vpar["meta"]["base"] == "base_variants_config.ini"),
        "variants_V00_Baseline_existe_sem_overrides": bool(len(v00) == 1 and len(dict(vpar[v00[0]])) == 0),
    }

    before = collab_hashes()

    rc1, r1, so1, se1 = run_worker(1, write_npz=True)
    rc2, r2, so2, se2 = run_worker(2, write_npz=False, compare_npz=OUT_NPZ if OUT_NPZ.exists() else None)

    after = collab_hashes()
    colab_inalterada = bool(before == after)

    recibo = {
        "titulo": "Segunda construcao independente do vetor observado local H0DN x BG1",
        "gerado_em": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "declaracao": "nenhum valor do vetor foi impresso, registrado ou resumido",
        "metodo": {
            "descricao": ("pacote publico h0_constrainer importado de upstream\\h0_constrainer; "
                          "h0_constrainer.solver.solve_system substituido por funcao que levanta "
                          "excecao propria carregando equation_data (o solver nunca rodou); "
                          "main() da colaboracao rodado com stdout/stderr em os.devnull e warnings "
                          "ignorados; yval lido do equation_data capturado. A GLS interna do "
                          "intercept.py (alfa de fluxo de Hubble, que entra em yval) e' parte da "
                          "montagem publica do vetor e rodou normalmente; solve_system, "
                          "numeros_colaboracao, abrir e evaluate nao foram chamados."),
            "configuracao": "configs\\base_variants_config.ini (= secao [V00 - Baseline] de variants.ini, sem overrides)",
            "chaves_de_configuracao_usadas": (r1 or {}).get("config_chaves_usadas"),
            "chaves_de_configuracao_lidas_pelo_codigo": (r1 or {}).get("config_chaves_lidas"),
            "override_nossos": {"datadir": "caminho absoluto de upstream\\data\\",
                                "verbose": "False", "warn": "False", "logfile": "none", "savefile": "none"},
            "selecao_da_analise_de_base": ("main(cf_file) le o INI; sem laco de variantes no caminho de "
                                           "arquivo unico (cli.py so itera secoes com -v); a base e' o INI "
                                           "base_variants_config.ini / config.ini, equivalentes."),
            "conferencias_de_configuracao": cfg_checks,
        },
        "conferencias_rodada1": (r1 or {}).get("conferencias"),
        "conferencias_rodada2": (r2 or {}).get("conferencias"),
        "y": {
            "dtype": (r1 or {}).get("y_dtype"),
            "forma": (r1 or {}).get("y_forma"),
            "sha256_tobytes_rodada1": (r1 or {}).get("y_sha256"),
            "sha256_tobytes_rodada2": (r2 or {}).get("y_sha256"),
            "determinismo_hash_igual_entre_rodadas": bool(r1 and r2 and r1.get("y_sha256") == r2.get("y_sha256")),
            "comparacao_rodada2_com_npz_da_rodada1": (r2 or {}).get("comparacao_com_rodada1"),
        },
        "vetor_y255_npz": (r1 or {}).get("npz"),
        "primeira_construcao": (r1 or {}).get("primeira_construcao"),
        "erros": {"rodada1": (r1 or {}).get("erro"), "rodada2": (r2 or {}).get("erro"),
                  "returncodes": [rc1, rc2],
                  "bytes_stdout_stderr_trabalhadores": [so1, se1, so2, se2]},
        "colaboracao_inalterada_durante_a_execucao": colab_inalterada,
        "arquivos_da_colaboracao": before,
        "versoes": {"python": sys.version, "plataforma": platform.platform(),
                    "numpy": np.__version__, "scipy": scipy.__version__, "pandas": pandas.__version__},
        "nenhum_valor_do_vetor_foi_impresso_registrado_ou_resumido": True,
    }
    tmp = OUT_RECIBO.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(recibo, indent=1, ensure_ascii=False), encoding="utf-8")
    if tmp.stat().st_size < 500:
        print("ERRO: recibo temporario pequeno demais")
        return 1
    os.replace(tmp, OUT_RECIBO)

    # resumo (so booleanos e hashes)
    c1 = (r1 or {}).get("conferencias") or {}
    print("returncodes:", rc1, rc2, "| bytes stdout/stderr dos trabalhadores:", so1, se1, so2, se2)
    print("erros:", (r1 or {}).get("erro"), (r2 or {}).get("erro"))
    for k, v in c1.items():
        print(f"  {k}: {v}")
    print("config:", cfg_checks)
    print("y sha256 r1:", (r1 or {}).get("y_sha256"))
    print("y sha256 r2:", (r2 or {}).get("y_sha256"))
    print("determinismo:", recibo["y"]["determinismo_hash_igual_entre_rodadas"])
    print("npz:", (r1 or {}).get("npz"))
    print("primeira construcao:", (r1 or {}).get("primeira_construcao"))
    print("colaboracao inalterada:", colab_inalterada)
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--worker":
        run_id = int(sys.argv[2])
        out_json = sys.argv[3]
        write_npz = "--write-npz" in sys.argv
        compare = None
        if "--compare-npz" in sys.argv:
            compare = sys.argv[sys.argv.index("--compare-npz") + 1]
        sys.exit(worker(run_id, out_json, write_npz, compare))
    sys.exit(main_orch())
