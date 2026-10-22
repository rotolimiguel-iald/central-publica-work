# -*- coding: utf-8 -*-
"""sincronizar_bancada.py -- o elo B(n) da cadeia de selo: vincula a Bancada Um ao um.py selado.

ESBOCO FUNCIONAL (12/10/2026) do desenho da gerencia c1, por ordem do operador de 12/10 (verbatim em
work\\cunhagens_12out\\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt, sha256 lido por script no recibo).
NAO ESTA INSTALADO. Roda em sandbox contra uma COPIA da Bancada. A instalacao na cadeia (passo B(n)) e a primeira
re-pinagem da producao (B3, depois do selo da v392) sao atos que o desenho (VINCULO_BANCADA_UMPY.md) reserva a gerencia
e ao operador.

O que faz, nesta ordem, e tudo fail-closed (qualquer divergencia = recusa visivel, codigo 2; bateria reprovada = codigo 3):
  1. LE O SELO do Nos (um_absoluto_selo.json) e o um.py: a versao (UM_VERSION, coluna 0), o sha256 do um.py que o selo
     pina, a linha UNICA de ALPHA_FINE_CODATA_2018 e beta = alpha*sqrt(e) EM RUNTIME (nunca literal), conferido contra o
     beta do core (um_absoluto.json) com tolerancia NOMEADA.
  2. LE O MANIFESTO VIGENTE da Bancada (canonical_contracts.json) e o estado do contrato instalado: depois de um selo,
     o canonical.py INSTALADO tem de recusar (PIN_CHANGED / CANONICAL_VERSION_CHANGED / SEAL_PROGRAM_MISMATCH); se o
     Nos alvo mora noutro caminho (sandbox), a mesma recusa e provada por sonda em RAM.
  3. REGENERA O MANIFESTO: mesmos pinos de codigo e de fontes (deriva de codigo ou de fonte NAO e sincronizacao: e
     implantacao B, com plano e evento proprios -> recusa), pinos novos do um.py e do selo, geracao B(n), linhagem,
     evento c1 nomeado, e o CONTRATO_CANONICO_B{n}.md gerado.
  4. RE-PINA numa COPIA de ensaio (staging) e confere com o canonical.py instalado: ok, versao, sha e beta bit a bit.
  5. RODA A BATERIA sintetica (BATERIA_VINCULO.json: T01-T17 da frente H_BANCADA, fontes pinadas por sha256, copias
     byte a byte dos testes do tunel) contra a copia; cada teste deixa recibo com comando, inicio, fim, exit e hashes.
  6. GRAVA O RECIBO (RECIBO_SINCRONIZACAO_<versao>_<stamp>.json) com todos os hashes; so em --modo aplicar, e so com
     evento c1 nomeado, grava o manifesto novo na Bancada (backup de bytes, temporario -> conferir -> os.replace,
     reconferencia pelo canonical.py instalado, rollback se falhar) e copia o recibo para estado\\sincronizacao\\.
Nada aqui le dado observado para veredito, nada move o gate, nada e leitura fisica. NOT_FALSIFIED nunca e creditacao.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import math
import os
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import patch

if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (asserts sao guardas)")

AQUI = Path(__file__).resolve().parent
PRODUCAO = Path(r"C:\IALD\Bancada_Um")
NOS_PADRAO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
TUNEL_PADRAO = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019")
EVENTOS_QUADRO = Path(r"C:\IALD\PROGRAMA_IALD\eventos.jsonl")
PORTA_BANCADA = 18777
# a MESMA regex do canonical.py instalado (l.73-74): coluna 0, sem indentacao
RE_VERSAO = re.compile(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', re.M)
RE_ALPHA = re.compile(r'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)', re.M)
# a regra mais forte dos runners do atrator (uma unica linha nao indentada): o esboco a exige; a B3 a leva ao canonical.py
RE_ALPHA_LINHAS = re.compile(r'^ALPHA_FINE_CODATA_2018[ \t]*=', re.M)
RE_GERACAO = re.compile(r'^B(\d+)-')
ESPERADOS_POS_SELO = ("PIN_CHANGED", "CANONICAL_VERSION_CHANGED", "SEAL_PROGRAM_MISMATCH")
# a guarda da regua (a mesma do um.py e do iald.py), montada em pedacos para que o token nunca exista neste arquivo
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
BETA_TOLERANCIA_REL = 1e-11   # medido em 12/10 (H_BANCADA): |beta_core - beta_runtime|/beta = 5.43e-13; a tolerancia e nomeada, nao escondida


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def agora():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def pin(p):
    b = Path(p).read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=sha256(b))


class Recusa(Exception):
    """Recusa fail-closed: o codigo e a primeira palavra; o resto e o motivo."""


def gravar_novo(p, data):
    """Grava arquivo NOVO (nunca sobrescreve): temporario -> conferir tamanho e bytes -> os.replace."""
    p = Path(p)
    if p.exists():
        raise Recusa("ARQUIVO_JA_EXISTE: " + str(p))
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp_sync")
    with tmp.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if tmp.stat().st_size != len(data) or tmp.read_bytes() != data:
        tmp.unlink()
        raise Recusa("ESCRITA_CURTA: " + str(p))
    os.replace(tmp, p)
    if p.read_bytes() != data:
        raise Recusa("ESCRITA_DIVERGE: " + str(p))
    return p


def json_bytes(obj):
    s = json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False, default=str)
    if GUARDA.search(s):
        raise Recusa("PALAVRA_PROIBIDA_NA_SAIDA")
    return (s + "\n").encode("utf-8")


def carregar_canonical(bancada):
    """Importa o canonical.py INSTALADO naquela Bancada (nunca o de outra), com nome de modulo unico."""
    p = Path(bancada) / "bancada" / "canonical.py"
    if not p.is_file():
        raise Recusa("CANONICAL_PY_AUSENTE: " + str(p))
    nome = "canonical_instalado_" + sha256(p.read_bytes())[:12]
    spec = importlib.util.spec_from_file_location(nome, p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome] = mod
    spec.loader.exec_module(mod)
    return mod, pin(p)


# ---------------------------------------------------------------- 1. o selo e o um.py
def ler_nos(nos, versao):
    nos = Path(nos).resolve()   # o manifesto pina caminhos ABSOLUTOS: um caminho relativo seria resolvido contra a raiz da Bancada (PIN_UNREADABLE)
    um_p, selo_p, core_p = nos / "um.py", nos / "um_absoluto_selo.json", nos / "um_absoluto.json"
    for p in (um_p, selo_p):
        if not p.is_file():
            raise Recusa("NOS_INCOMPLETO: " + str(p))
    raw = um_p.read_bytes()
    selo_raw = selo_p.read_bytes()
    try:
        selo = json.loads(selo_raw)
    except ValueError as exc:
        raise Recusa("SELO_ILEGIVEL: " + str(exc))
    if selo.get("um_version") != versao:
        raise Recusa("SELO_VERSAO_DIFERENTE: selo=%r alvo=%r" % (selo.get("um_version"), versao))
    pinado = (selo.get("sha256") or {}).get("um.py")
    if pinado != sha256(raw):
        raise Recusa("SELO_NAO_PINA_O_UM_PY_DO_DISCO: selo=%s disco=%s" % (str(pinado)[:16], sha256(raw)[:16]))
    texto = raw.decode("utf-8-sig")
    v, a = RE_VERSAO.search(texto), RE_ALPHA.search(texto)
    if v is None or a is None:
        raise Recusa("CANONICAL_DECLARATION_MISSING")
    if v.group(1) != versao:
        raise Recusa("UM_VERSION_DIFERENTE_DO_ALVO: %r" % v.group(1))
    n_alpha = len(RE_ALPHA_LINHAS.findall(texto))
    if n_alpha != 1:
        raise Recusa("ALPHA_LINHA_NAO_UNICA: %d linhas nao indentadas" % n_alpha)
    alpha = float(a.group(1))
    if not (math.isfinite(alpha) and 0 < alpha < 1):
        raise Recusa("ALPHA_OUTSIDE_CONTRACT")
    linha_alpha = texto[:a.start()].count("\n") + 1
    beta = alpha * math.sqrt(math.e)          # EM RUNTIME, nunca literal
    core_info = None
    if core_p.is_file():
        core_raw = core_p.read_bytes()
        pin_core = (selo.get("sha256") or {}).get("um_absoluto.json")
        if pin_core is not None and pin_core != sha256(core_raw):
            raise Recusa("SELO_NAO_PINA_O_CORE_DO_DISCO")
        core = json.loads(core_raw).get("core") or {}
        beta_core = core.get("beta")
        if not isinstance(beta_core, (int, float)):
            raise Recusa("CORE_SEM_BETA")
        rel = abs(beta - float(beta_core)) / beta
        if rel > BETA_TOLERANCIA_REL:
            raise Recusa("BETA_CORE_DIVERGE_DO_RUNTIME: rel=%.3e" % rel)
        core_info = dict(path=str(core_p), bytes=len(core_raw), sha256=sha256(core_raw), beta_core=repr(float(beta_core)),
                         beta_rel_diff=rel, tolerancia_rel=BETA_TOLERANCIA_REL, qg_closure_verdict=core.get("qg_closure_verdict"))
    else:
        raise Recusa("CORE_AUSENTE: " + str(core_p))
    return dict(dir=str(nos), um_py=dict(path=str(um_p), bytes=len(raw), sha256=sha256(raw)),
                selo=dict(path=str(selo_p), bytes=len(selo_raw), sha256=sha256(selo_raw), um_version=selo.get("um_version"),
                          qg_closure_verdict=selo.get("qg_closure_verdict")),
                core=core_info, UM_VERSION=v.group(1), alpha=dict(valor=alpha, linha=linha_alpha, n_linhas_nao_indentadas=n_alpha),
                beta_runtime=repr(beta), _beta=beta, _raw=raw, _selo_raw=selo_raw)


# ---------------------------------------------------------------- 2. o manifesto vigente e o estado do contrato
def estado_anterior(bancada, canonical_mod):
    bancada = Path(bancada)
    man_p = bancada / "canonical_contracts.json"
    if not man_p.is_file():
        raise Recusa("MANIFESTO_AUSENTE: " + str(man_p))
    raw = man_p.read_bytes()
    man = json.loads(raw)
    if man.get("schema") != 1:
        raise Recusa("CANONICAL_SCHEMA_UNSUPPORTED")
    estado, recibo = "OK", None
    try:
        reg = canonical_mod.CanonicalRegistry(bancada)
        recibo = reg.check("pre_sincronizacao")
    except canonical_mod.CanonicalError as exc:
        estado = str(exc).split(":")[0]
    return dict(path=str(man_p), bytes=len(raw), sha256=sha256(raw), deployment_id=man.get("deployment_id"),
                version=(man.get("canonical") or {}).get("version"),
                um_py_pinado=((man.get("canonical") or {}).get("script") or {}).get("sha256"),
                script_path_pinado=((man.get("canonical") or {}).get("script") or {}).get("path"),
                seal_path_pinado=((man.get("canonical") or {}).get("seal") or {}).get("path"),
                n_code=len(man.get("code") or []), n_sources=len(man.get("sources") or []),
                estado_do_contrato_instalado=estado,
                recibo=({k: recibo[k] for k in ("ok", "canonical_version", "um_py_sha256", "beta_tgl", "deployment_id")} if recibo else None),
                _man=man, _raw=raw)


def sonda_pos_selo_em_ram(bancada, canonical_mod, anterior, nos_info):
    """Quando o Nos alvo NAO mora no caminho pinado (sandbox): prova em RAM que, se os bytes do caminho pinado fossem os do
    Nos alvo (o que o selo faz em producao), o canonical.py INSTALADO recusaria. Nada e escrito."""
    script_p = Path(anterior["script_path_pinado"]).resolve()
    seal_p = Path(anterior["seal_path_pinado"]).resolve()
    orig = Path.read_bytes

    def leitor(path):
        p = Path(path).resolve()
        if p == script_p:
            return nos_info["_raw"]
        if p == seal_p:
            return nos_info["_selo_raw"]
        return orig(path)
    with patch.object(Path, "read_bytes", leitor):
        try:
            canonical_mod.CanonicalRegistry(Path(bancada))
            return dict(recusou=False, codigo="ACEITO (inesperado)")
        except canonical_mod.CanonicalError as exc:
            return dict(recusou=True, codigo=str(exc).split(":")[0])


# ---------------------------------------------------------------- 3. o manifesto regenerado
def contrato_md(n, versao, nos_info, anterior, evento, stamp):
    return ("# Contrato de fidelidade da Bancada Um -- B%d / %s (sincronizacao)\n\n"
            "[REAL] Gerado por sincronizar_bancada.py em %s UTC, no passo B(%d) da cadeia de selo da %s, sob o evento c1 %s.\n\n"
            "## Identidade pinada\n\n"
            "- um.py %s: sha256 %s (%d B), linha de alpha %d (unica, coluna 0); beta = alpha*sqrt(e) em runtime = %s.\n"
            "- selo: sha256 %s.\n"
            "- manifesto anterior: %s (sha256 %s).\n\n"
            "## A regra\n\n"
            "Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que\n"
            "o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa\n"
            "sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash. Nada se grava\n"
            "na Bancada sem evento c1 nomeado. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao; nenhum rito move o gate.\n"
            % (n, versao, stamp, n, versao, evento, versao, nos_info["um_py"]["sha256"], nos_info["um_py"]["bytes"], nos_info["alpha"]["linha"],
               nos_info["beta_runtime"], nos_info["selo"]["sha256"], anterior["deployment_id"], anterior["sha256"])).encode("utf-8")


def regenerar(bancada, anterior, nos_info, versao, evento, script_sha, bateria_sha, modo, forcar, stamp):
    bancada = Path(bancada)
    man = anterior["_man"]
    m = RE_GERACAO.match(str(man.get("deployment_id") or ""))
    if not m:
        raise Recusa("DEPLOYMENT_ID_SEM_GERACAO: %r" % man.get("deployment_id"))
    n = int(m.group(1)) + 1
    code, sources = [], []
    for e in man["code"]:
        p = bancada / e["path"]
        if not p.is_file():
            raise Recusa("PIN_UNREADABLE: " + str(p))
        b = p.read_bytes()
        if len(b) != e["bytes"] or sha256(b) != e["sha256"]:
            raise Recusa("CODE_DRIFT_NAO_E_SINCRONIZACAO: " + e["path"])
        code.append(dict(path=e["path"], bytes=len(b), sha256=sha256(b)))
    for e in man["sources"]:
        p = Path(e["path"])
        p = p if p.is_absolute() else bancada / p
        if not p.is_file():
            raise Recusa("PIN_UNREADABLE: " + str(p))
        b = p.read_bytes()
        if len(b) != e["bytes"] or sha256(b) != e["sha256"]:
            raise Recusa("SOURCE_DRIFT_NAO_E_SINCRONIZACAO: " + e["path"])
        sources.append(dict(e, bytes=len(b), sha256=sha256(b)))
    rotulo = "CONTRATO_CANONICO_B%d.md" % n
    if any(c["path"] == rotulo for c in code):
        raise Recusa("CONTRATO_B%d_JA_PINADO" % n)
    md = contrato_md(n, versao, nos_info, anterior, evento, stamp)
    code.append(dict(path=rotulo, bytes=len(md), sha256=sha256(md)))
    code.sort(key=lambda c: c["path"])
    novo = dict(schema=1,
                deployment_id="B%d-%s-%s-R1" % (n, versao, stamp[:8]),
                created_utc=agora(),
                canonical=dict(version=versao,
                               script=dict(path=nos_info["um_py"]["path"], bytes=nos_info["um_py"]["bytes"], sha256=nos_info["um_py"]["sha256"]),
                               seal=dict(path=nos_info["selo"]["path"], bytes=nos_info["selo"]["bytes"], sha256=nos_info["selo"]["sha256"])),
                code=code, sources=sources,
                contracts=dict(man.get("contracts") or {},
                               sync_policy="B(n) a cada versao selada por sincronizar_bancada.py: pino velho recusa (PIN_CHANGED); evento c1 nomeado; "
                                           "bateria sintetica antes de gravar; codigo e fontes so mudam por implantacao B com plano proprio"),
                sincronizacao=dict(passo="B%d" % n, versao=versao, modo=modo, forcada=bool(forcar),
                                   anterior=dict(deployment_id=anterior["deployment_id"], manifest_sha256=anterior["sha256"],
                                                 version=anterior["version"], um_py_pinado=anterior["um_py_pinado"],
                                                 estado_do_contrato_instalado=anterior["estado_do_contrato_instalado"]),
                                   evento_c1=evento, selo_sha256=nos_info["selo"]["sha256"], um_py_sha256=nos_info["um_py"]["sha256"],
                                   core_sha256=nos_info["core"]["sha256"], alpha_linha=nos_info["alpha"]["linha"],
                                   beta_runtime=nos_info["beta_runtime"], beta_core=nos_info["core"]["beta_core"],
                                   gerado_por=dict(script_sha256=script_sha, bateria_sha256=bateria_sha), quando_utc=agora(),
                                   scope="IDENTITY_RE_PIN_ONLY; NOT_A_PHYSICAL_READING", gate_effect="NONE"))
    return novo, md, rotulo, n


# ---------------------------------------------------------------- 4. a copia de ensaio (staging) e a re-pinagem
def montar_staging(bancada, man, raiz, novo_manifesto_bytes=None, contrato=None):
    """Copia byte a byte (conferindo os pinos do manifesto dado) o codigo e as fontes RELATIVAS da Bancada para raiz/candidate."""
    bancada, cand = Path(bancada), Path(raiz) / "candidate"
    if cand.exists():
        raise Recusa("STAGING_JA_EXISTE: " + str(cand))
    copias = []
    for e in man["code"] + [s for s in man["sources"] if not Path(s["path"]).is_absolute()]:
        src = bancada / e["path"]
        if contrato is not None and e["path"] == contrato[0]:
            b = contrato[1]
        else:
            b = src.read_bytes()
        if len(b) != e["bytes"] or sha256(b) != e["sha256"]:
            raise Recusa("PIN_CHANGED_AO_COPIAR: " + e["path"])
        dst = cand / e["path"]
        if dst.exists():
            # o mesmo arquivo pode estar pinado em code E em sources (B2: fontes_externas/F5.2/10_frozen_neff_v1.py): duplicata so com bytes iguais
            if dst.read_bytes() != b:
                raise Recusa("DUPLICATA_COM_BYTES_DIFERENTES: " + e["path"])
            copias.append(dict(path=e["path"], bytes=len(b), sha256=sha256(b), duplicata_de_pino=True))
            continue
        gravar_novo(dst, b)
        copias.append(dict(path=e["path"], bytes=len(b), sha256=sha256(b)))
    (cand / "estado").mkdir(exist_ok=True)
    man_bytes = novo_manifesto_bytes if novo_manifesto_bytes is not None else (bancada / "canonical_contracts.json").read_bytes()
    gravar_novo(cand / "canonical_contracts.json", man_bytes)
    return cand, copias


def conferir_repinagem(canonical_mod, raiz_bancada, nos_info, versao, operacao):
    reg = canonical_mod.CanonicalRegistry(Path(raiz_bancada))
    rc = reg.check(operacao)
    falhas = []
    if not rc.get("ok"):
        falhas.append("ok=false")
    if rc.get("canonical_version") != versao:
        falhas.append("versao %r" % rc.get("canonical_version"))
    if rc.get("um_py_sha256") != nos_info["um_py"]["sha256"]:
        falhas.append("um.py sha")
    if rc.get("seal_sha256") != nos_info["selo"]["sha256"]:
        falhas.append("selo sha")
    if rc.get("beta_tgl") != nos_info["_beta"]:
        falhas.append("beta nao e bit a bit igual: %r vs %r" % (rc.get("beta_tgl"), nos_info["_beta"]))
    if falhas:
        raise Recusa("REPINAGEM_DIVERGE: " + "; ".join(falhas))
    return {k: rc[k] for k in ("ok", "canonical_version", "um_py_sha256", "seal_sha256", "canonical_manifest_sha256", "alpha", "beta_tgl",
                               "deployment_id", "mu_do_rito", "scope", "gate_effect")}


# ---------------------------------------------------------------- 5. a bateria
def copiar_testes(bateria, raiz):
    raiz = Path(raiz)
    feitas = []
    for c in bateria.get("copias", []):
        b = Path(c["de"]).read_bytes()
        if len(b) != c["bytes"] or sha256(b) != c["sha256"]:
            raise Recusa("FONTE_DA_BATERIA_ALTERADA: " + c["de"])
        gravar_novo(raiz / c["para"], b)
        feitas.append(dict(de=c["de"], para=str(raiz / c["para"]), sha256=c["sha256"], bytes=c["bytes"]))
    return feitas


def _subst(x, ctx):
    if isinstance(x, str):
        for k, v in ctx.items():
            x = x.replace("{" + k + "}", str(v))
        return x
    if isinstance(x, list):
        return [_subst(i, ctx) for i in x]
    if isinstance(x, dict):
        return {k: _subst(v, ctx) for k, v in x.items()}
    return x


VOLATEIS_PADRAO = {"started_utc", "finished_utc", "elapsed_seconds", "environment", "began_utc", "ended_utc", "seconds", "created_utc",
                   "python", "platform", "numpy", "path", "source_snapshot_before", "source_snapshot_after"}


def _strip(o, vol):
    if isinstance(o, dict):
        return {k: _strip(v, vol) for k, v in o.items() if k not in vol}
    if isinstance(o, list):
        return [_strip(x, vol) for x in o]
    return o


def _diff(a, b, path="", acc=None):
    acc = acc if acc is not None else {"max_abs": 0.0, "mismatch": []}
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b:
                acc["mismatch"].append(path + "." + k + " (missing)")
                continue
            _diff(a[k], b[k], path + "." + k, acc)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            acc["mismatch"].append(path + " (len)")
            return acc
        for i, (x, y) in enumerate(zip(a, b)):
            _diff(x, y, path + "[%d]" % i, acc)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        d = abs(float(a) - float(b))
        acc["max_abs"] = max(acc["max_abs"], d)
        if d != 0.0:
            acc["mismatch"].append(path + " (num %.3e)" % d)
    elif a != b:
        acc["mismatch"].append(path + " (value)")
    return acc


def verificar(ver, saida_texto, exit_code, ctx):
    """Devolve (passa, detalhe)."""
    t = ver.get("tipo", "exit0")
    if exit_code != 0 and t != "kernel_recibo":
        return False, "exit=%d" % exit_code
    if t == "exit0":
        return True, "exit 0"
    if t == "stdout_regex":
        ok = re.search(ver["regex"], saida_texto) is not None
        return ok, ("regex %r %s" % (ver["regex"], "casou" if ok else "NAO casou"))
    if t == "json_igual":
        p = Path(_subst(ver["arquivo"], ctx))
        if not p.is_file():
            return False, "arquivo ausente: " + str(p)
        d = json.loads(p.read_bytes())
        for campo, valor in ver["campos"].items():
            v = d
            for parte in campo.split("."):
                v = v.get(parte) if isinstance(v, dict) else None
            if v != valor:
                return False, "%s=%r esperado %r" % (campo, v, valor)
        return True, "campos conferem: " + ", ".join("%s=%r" % kv for kv in ver["campos"].items())
    if t == "comparar_json":
        novo, arq = Path(_subst(ver["novo"], ctx)), Path(_subst(ver["arquivado"], ctx))
        if not novo.is_file() or not arq.is_file():
            return False, "arquivo ausente para comparar"
        vol = set(ver.get("volateis") or VOLATEIS_PADRAO)
        d = _diff(_strip(json.loads(novo.read_bytes()), vol), _strip(json.loads(arq.read_bytes()), vol))
        ok = len(d["mismatch"]) == 0
        return ok, "max_abs=%.3e mismatch=%d %s" % (d["max_abs"], len(d["mismatch"]), d["mismatch"][:5])
    if t == "kernel_recibo":
        kp = ctx.get("kernel_recibo")
        if not kp:
            return None, "sem --kernel-recibo"
        kp = Path(kp)
        if not kp.is_file():
            return False, "recibo do kernel ausente: " + str(kp)
        k = json.loads(kp.read_bytes())
        ok = k.get("rc") == 0 and k.get("sorry") == 0 and bool(k.get("build_full_log_sha256"))
        return ok, "recibo do kernel: rc=%r sorry=%r" % (k.get("rc"), k.get("sorry"))
    return False, "tipo de verificacao desconhecido: " + t


def rodar_bateria(bateria, ctx, recibos_dir, modo, fase="pos_selo", sandbox=False, recibo_pre_selo=None):
    recibos_dir = Path(recibos_dir)
    recibos_dir.mkdir(parents=True, exist_ok=True)
    resultados = []
    for t in bateria["testes"]:
        tid = t["id"]
        rec = dict(id=tid, teste=t.get("teste"), fases=t.get("fases", ["pre_selo", "pos_selo"]), obrigatorio_em=t.get("obrigatorio_em", ["ensaio", "aplicar"]),
                   fontes=[], inicio=agora())
        if fase not in rec["fases"]:
            # o teste pertence a outra fase (ex.: os runners do atrator pinam o um.py ANTERIOR e so rodam antes do selo):
            # na fase pos_selo ele e lido do recibo da fase pre_selo, por hash, nunca refeito
            if fase == "pos_selo" and "pre_selo" in rec["fases"]:
                det = "nao pertence a fase pos_selo; o resultado vale pelo recibo pre-selo %s" % ((recibo_pre_selo or {}).get("sha256") or "(ausente)")
            else:
                det = "nao pertence a fase %s (fases: %s)" % (fase, rec["fases"])
            rec.update(resultado="NAO_EXECUTADO", detalhe=det, fim=agora())
            resultados.append(rec)
            continue
        fontes_ok = True
        for f in t.get("fontes", []):
            p = Path(f["path"])
            if not p.is_file():
                rec["fontes"].append(dict(f, estado="AUSENTE"))
                fontes_ok = False
                continue
            b = p.read_bytes()
            est = "OK" if (len(b) == f["bytes"] and sha256(b) == f["sha256"]) else "ALTERADA"
            fontes_ok = fontes_ok and est == "OK"
            rec["fontes"].append(dict(f, estado=est))
        if not fontes_ok:
            rec.update(resultado="FALHA", detalhe="fonte pinada ausente ou alterada", fim=agora())
            resultados.append(rec)
            continue
        ver = t.get("verificacao", {"tipo": "exit0"})
        if ver.get("tipo") == "kernel_recibo" and not ctx.get("kernel_recibo"):
            exig = (modo in rec["obrigatorio_em"]) and not sandbox
            rec.update(resultado=("FALHA" if exig else "NAO_EXECUTADO"), detalhe="sem --kernel-recibo (T17 e lido do recibo do build do kernel da etapa 2 da cadeia)" + ("; tolerado so em --sandbox" if sandbox else ""), fim=agora())
            resultados.append(rec)
            continue
        cmd = _subst(t["comando"], ctx)
        cwd = _subst(t.get("cwd", "{raiz}"), ctx)
        rec["comando"], rec["cwd"] = cmd, cwd
        t0 = time.perf_counter()
        try:
            r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=float(t.get("timeout_s", 900)), env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8"))
            exit_code, out = r.returncode, (r.stdout or "") + "\n--- STDERR ---\n" + (r.stderr or "")
        except subprocess.TimeoutExpired as exc:
            exit_code, out = -1, "TIMEOUT apos %.0f s\n%s\n%s" % (float(t.get("timeout_s", 900)), exc.stdout or "", exc.stderr or "")
        rec["segundos"] = round(time.perf_counter() - t0, 3)
        log = recibos_dir / (tid + ".log")
        gravar_novo(log, ("COMMAND: %r\nCWD: %s\nEXIT: %d\n%s" % (cmd, cwd, exit_code, out)).encode("utf-8"))
        rec["log"] = dict(path=str(log), sha256=sha256(log.read_bytes()), bytes=log.stat().st_size)
        rec["exit"] = exit_code
        passa, detalhe = verificar(ver, out, exit_code, ctx)
        rec["detalhe"] = detalhe
        if passa is None:
            rec["resultado"] = "FALHA" if (modo in rec["obrigatorio_em"] and not sandbox) else "NAO_EXECUTADO"
        else:
            rec["resultado"] = "PASSA" if passa else "FALHA"
        if GUARDA.search(out.replace("NOT_CONF" + "IRMED", "").replace("UNCONF" + "IRMED", "")):
            rec["resultado"], rec["detalhe"] = "FALHA", "palavra proibida na saida do teste; " + detalhe
        rec["fim"] = agora()
        resultados.append(rec)
    n_passa = sum(1 for r in resultados if r["resultado"] == "PASSA")
    n_falha = sum(1 for r in resultados if r["resultado"] == "FALHA")
    n_nexec = sum(1 for r in resultados if r["resultado"] == "NAO_EXECUTADO")
    return dict(n=len(resultados), passa=n_passa, falha=n_falha, nao_executado=n_nexec, testes=resultados,
                veredito=("BATERIA_PASSA" if n_falha == 0 else "BATERIA_FALHOU"))


# ---------------------------------------------------------------- 6. evento c1, servico, aplicacao
def verificar_evento(evento, versao, bancada, sandbox):
    if evento is None or not str(evento).strip():
        raise Recusa("EVENTO_C1_AUSENTE: nenhuma gravacao na Bancada sem evento c1 nomeado")
    ev = str(evento).strip()
    if ev.startswith("SANDBOX:"):
        if not sandbox:
            raise Recusa("EVENTO_SANDBOX_FORA_DO_SANDBOX")
        return dict(evento=ev, verificado=False, nota="sandbox: evento literal, nao conferido no quadro")
    if not ev.isdigit():
        raise Recusa("EVENTO_C1_INVALIDO: %r (seq numerico de eventos.jsonl ou SANDBOX:<texto>)" % ev)
    if not EVENTOS_QUADRO.is_file():
        raise Recusa("EVENTOS_JSONL_AUSENTE")
    seq = int(ev)
    for linha in EVENTOS_QUADRO.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        e = json.loads(linha)
        if e.get("seq") == seq:
            texto = json.dumps(e.get("dados"), ensure_ascii=False)
            if e.get("quem") != "claude-c1":
                raise Recusa("EVENTO_NAO_E_DA_C1: seq %d por %r" % (seq, e.get("quem")))
            if versao not in texto or str(Path(bancada).name) not in texto or "sincroniz" not in texto.lower():
                raise Recusa("EVENTO_NAO_NOMEIA_A_GRAVACAO: seq %d tem de citar %s, %s e a sincronizacao" % (seq, versao, Path(bancada).name))
            return dict(evento=seq, verificado=True, quando=e.get("quando"), tipo=e.get("tipo"), hash=e.get("hash"))
    raise Recusa("EVENTO_NAO_ENCONTRADO: seq %d" % seq)


def servico_responde(porta=PORTA_BANCADA):
    s = socket.socket()
    s.settimeout(1.5)
    try:
        s.connect(("127.0.0.1", porta))
        return True
    except OSError:
        return False
    finally:
        s.close()


def aplicar_na_bancada(bancada, canonical_mod, novo_bytes, contrato, nos_info, versao, n, stamp):
    bancada = Path(bancada)
    man_p = bancada / "canonical_contracts.json"
    antes = man_p.read_bytes()
    bak = man_p.with_name(man_p.name + ".bak_B%d_%s" % (n, stamp))
    if bak.exists():
        raise Recusa("BACKUP_JA_EXISTE: " + str(bak))
    with bak.open("xb") as f:
        f.write(antes)
    if bak.read_bytes() != antes:
        raise Recusa("BACKUP_DIVERGE")
    contrato_p = bancada / contrato[0]
    gravar_novo(contrato_p, contrato[1])
    tmp = man_p.with_name(man_p.name + ".tmp_B%d" % n)
    with tmp.open("xb") as f:
        f.write(novo_bytes)
        f.flush()
        os.fsync(f.fileno())
    if tmp.read_bytes() != novo_bytes:
        tmp.unlink()
        raise Recusa("ESCRITA_CURTA_DO_MANIFESTO")
    if man_p.read_bytes() != antes:
        tmp.unlink()
        raise Recusa("MANIFESTO_MUDOU_ENTRE_LEITURA_E_TROCA")
    os.replace(tmp, man_p)
    try:
        if man_p.read_bytes() != novo_bytes:
            raise Recusa("MANIFESTO_DIVERGE_APOS_TROCA")
        pos = conferir_repinagem(canonical_mod, bancada, nos_info, versao, "pos_sincronizacao")
    except Exception as exc:
        # rollback: o manifesto anterior volta byte a byte; o contrato novo sai
        tmp2 = man_p.with_name(man_p.name + ".tmp_rollback_B%d" % n)
        with tmp2.open("xb") as f:
            f.write(antes)
        os.replace(tmp2, man_p)
        if contrato_p.exists():
            contrato_p.unlink()
        raise Recusa("APLICACAO_REVERTIDA: " + str(exc))
    return dict(manifesto=str(man_p), backup=str(bak), backup_sha256=sha256(antes), contrato=str(contrato_p), pos_conferencia=pos)


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="o elo B(n): sincroniza a Bancada Um com o um.py selado (esboco funcional, 12/10/2026)")
    ap.add_argument("--nos", default=str(NOS_PADRAO))
    ap.add_argument("--bancada", required=True)
    ap.add_argument("--versao", required=True)
    ap.add_argument("--saida", required=True, help="pasta nova desta sincronizacao (recibos, staging)")
    ap.add_argument("--bateria", required=True, help="BATERIA_VINCULO.json")
    ap.add_argument("--tunel", default=str(TUNEL_PADRAO))
    ap.add_argument("--modo", choices=("ensaio", "aplicar"), default="ensaio")
    ap.add_argument("--evento", default=None, help="seq do evento c1 que nomeia a gravacao; em sandbox, SANDBOX:<texto>")
    ap.add_argument("--producao", action="store_true", help="obrigatorio quando --bancada e a Bancada de producao")
    ap.add_argument("--sandbox", action="store_true", help="permite Nos fora do caminho pinado e evento SANDBOX:*")
    ap.add_argument("--kernel-recibo", default=None, help="recibo do build do kernel da etapa 2 (T17)")
    ap.add_argument("--fase", choices=("pre_selo", "pos_selo"), default="pos_selo",
                    help="pre_selo = os testes finais contra a versao ainda canonica (etapa 1 da cadeia); pos_selo = o elo B(n) depois do selo")
    ap.add_argument("--recibo-pre-selo", default=None, help="na fase pos_selo: o RECIBO_SINCRONIZACAO da fase pre_selo (lido por hash; obrigatorio fora do sandbox)")
    ap.add_argument("--forcar-regeracao", action="store_true", help="regenera mesmo se a Bancada ja pina a versao alvo")
    ap.add_argument("--sem-bateria", action="store_true", help="SO para controles negativos: pula a bateria (nunca em aplicar)")
    a = ap.parse_args(argv)

    stamp = time.strftime("%Y%m%d_%H%M%S")
    saida = Path(a.saida).resolve()
    saida.mkdir(parents=True, exist_ok=True)
    bancada = Path(a.bancada).resolve()
    script_sha = sha256(Path(__file__).read_bytes())
    bateria_p = Path(a.bateria).resolve()
    bateria_raw = bateria_p.read_bytes()
    bateria = json.loads(bateria_raw)
    recibo = dict(esboco="sincronizar_bancada.py (12/10/2026) -- NAO INSTALADO; desenho da gerencia c1; roda em sandbox contra uma copia",
                  script_sha256=script_sha, bateria=dict(path=str(bateria_p), sha256=sha256(bateria_raw), versao=bateria.get("versao_bateria")),
                  inicio_utc=agora(), stamp=stamp, modo=a.modo, sandbox=bool(a.sandbox), producao=(bancada == PRODUCAO.resolve()),
                  fase=a.fase, recibo_pre_selo=None,
                  versao_alvo=a.versao, bancada=dict(dir=str(bancada)), nos=None, manifesto_anterior=None, manifesto_novo=None, bateria_resultado=None,
                  aplicacao=None, veredito=None, escopo="IDENTIDADE_E_TESTES_SINTETICOS; NENHUMA_LEITURA_FISICA; NOT_FALSIFIED nao e creditacao",
                  gate_effect="NONE")

    def fechar(veredito, codigo=0, recusa=None):
        recibo["veredito"] = veredito
        recibo["recusa"] = recusa
        recibo["fim_utc"] = agora()
        nome = ("RECIBO_SINCRONIZACAO_%s_%s.json" if recusa is None else "RECUSA_SINCRONIZACAO_%s_%s.json") % (a.versao, stamp)
        p = gravar_novo(saida / nome, json_bytes(recibo))
        print(json.dumps(dict(veredito=veredito, recusa=recusa, recibo=str(p), recibo_sha256=sha256(p.read_bytes())), ensure_ascii=False))
        return codigo

    try:
        # guardas de producao e de sandbox
        if recibo["producao"]:
            if not a.producao:
                raise Recusa("PRODUCAO_SEM_FLAG: --bancada e a Bancada de producao; exige --producao")
            if a.sandbox:
                raise Recusa("SANDBOX_NA_PRODUCAO")
            if a.modo == "aplicar" and servico_responde():
                raise Recusa("SERVICO_NO_AR: quiesce e pare o um_bancada.py (ato com recibo) antes de aplicar; o manifesto em RAM nao recarrega")
        if a.modo == "aplicar" and a.sem_bateria:
            raise Recusa("APLICAR_SEM_BATERIA_PROIBIDO")
        if a.fase == "pos_selo":
            if a.recibo_pre_selo:
                rp = Path(a.recibo_pre_selo)
                if not rp.is_file():
                    raise Recusa("RECIBO_PRE_SELO_AUSENTE: " + str(rp))
                rj = json.loads(rp.read_bytes())
                if rj.get("fase") != "pre_selo" or (rj.get("bateria_resultado") or {}).get("veredito") != "BATERIA_PASSA":
                    raise Recusa("RECIBO_PRE_SELO_INVALIDO: fase=%r bateria=%r" % (rj.get("fase"), (rj.get("bateria_resultado") or {}).get("veredito")))
                recibo["recibo_pre_selo"] = dict(path=str(rp), sha256=sha256(rp.read_bytes()), versao=rj.get("versao_alvo"), veredito=rj.get("veredito"))
            elif a.modo == "aplicar" and not a.sandbox:
                raise Recusa("RECIBO_PRE_SELO_AUSENTE: o elo B(n) exige o recibo dos testes finais da fase pre_selo")
        evento = verificar_evento(a.evento, a.versao, bancada, a.sandbox) if a.modo == "aplicar" else (dict(evento=a.evento, verificado=False, nota="ensaio: nenhuma gravacao na Bancada") if a.evento else None)
        recibo["evento_c1"] = evento
        # 1. o selo e o um.py
        nos_info = ler_nos(a.nos, a.versao)
        recibo["nos"] = {k: v for k, v in nos_info.items() if not k.startswith("_")}
        # 2. o manifesto vigente
        canonical_mod, canonical_pin = carregar_canonical(bancada)
        recibo["bancada"]["canonical_py_instalado"] = canonical_pin
        anterior = estado_anterior(bancada, canonical_mod)
        recibo["manifesto_anterior"] = {k: v for k, v in anterior.items() if not k.startswith("_")}
        nos_pinado = Path(anterior["script_path_pinado"]).resolve() == Path(nos_info["um_py"]["path"]).resolve()
        if not nos_pinado and not a.sandbox:
            raise Recusa("NOS_DIFERENTE_DO_PINADO: o manifesto pina %s; o alvo e %s (so em --sandbox)" % (anterior["script_path_pinado"], nos_info["um_py"]["path"]))
        ja_sincronizada = (anterior["estado_do_contrato_instalado"] == "OK" and anterior["version"] == a.versao
                           and anterior["um_py_pinado"] == nos_info["um_py"]["sha256"] and nos_pinado)
        if anterior["estado_do_contrato_instalado"] not in ("OK",) + ESPERADOS_POS_SELO:
            raise Recusa("BANCADA_EM_ESTADO_DESCONHECIDO: " + anterior["estado_do_contrato_instalado"])
        if not nos_pinado:
            recibo["sonda_pos_selo_em_ram"] = sonda_pos_selo_em_ram(bancada, canonical_mod, anterior, nos_info)
            if not recibo["sonda_pos_selo_em_ram"]["recusou"] or recibo["sonda_pos_selo_em_ram"]["codigo"] not in ESPERADOS_POS_SELO:
                raise Recusa("CANONICAL_INSTALADO_NAO_RECUSOU_PINO_VELHO: " + str(recibo["sonda_pos_selo_em_ram"]))
        elif anterior["estado_do_contrato_instalado"] in ESPERADOS_POS_SELO:
            recibo["pino_velho_recusado_pelo_instalado"] = anterior["estado_do_contrato_instalado"]
        # 3. regenerar (ou nao)
        raiz = saida / "raiz"
        if ja_sincronizada and not a.forcar_regeracao:
            recibo["manifesto_novo"] = None
            cand, copias = montar_staging(bancada, anterior["_man"], raiz)
            recibo["staging"] = dict(candidate=str(cand), n_copias=len(copias), manifesto="o vigente (ja sincronizada)")
            recibo["repinagem"] = conferir_repinagem(canonical_mod, cand, nos_info, a.versao, "ensaio_ja_sincronizada")
            veredito_base = "JA_SINCRONIZADA"
            novo_bytes = contrato = n = None
        else:
            novo, md, rotulo, n = regenerar(bancada, anterior, nos_info, a.versao, (evento or {}).get("evento"), script_sha, sha256(bateria_raw), a.modo, a.forcar_regeracao, stamp)
            novo_bytes = json_bytes(novo)
            contrato = (rotulo, md)
            gravar_novo(saida / ("MANIFESTO_CANDIDATO_B%d.json" % n), novo_bytes)
            gravar_novo(saida / rotulo, md)
            recibo["manifesto_novo"] = dict(deployment_id=novo["deployment_id"], sha256=sha256(novo_bytes), bytes=len(novo_bytes), n_code=len(novo["code"]),
                                            n_sources=len(novo["sources"]), contrato=rotulo, contrato_sha256=sha256(md), candidato=str(saida / ("MANIFESTO_CANDIDATO_B%d.json" % n)))
            cand, copias = montar_staging(bancada, novo, raiz, novo_bytes, contrato)
            recibo["staging"] = dict(candidate=str(cand), n_copias=len(copias), manifesto="o regenerado B%d" % n)
            recibo["repinagem"] = conferir_repinagem(canonical_mod, cand, nos_info, a.versao, "ensaio_repinagem_B%d" % n)
            veredito_base = "REPINADA_B%d" % n
        # 5. a bateria (contra a copia)
        if a.sem_bateria:
            recibo["bateria_resultado"] = dict(veredito="BATERIA_PULADA_SO_CONTROLE_NEGATIVO")
        else:
            recibo["copias_de_testes"] = copiar_testes(bateria, raiz)
            ctx = dict(py=sys.executable, vinculo=str(AQUI), raiz=str(raiz), candidate=str(cand), nos=str(Path(a.nos).resolve()), versao=a.versao,
                       recibos=str(saida / "recibos"), tunel=str(Path(a.tunel).resolve()), saida=str(saida), rotulo="V" + stamp, kernel_recibo=a.kernel_recibo or "")
            recibo["bateria_resultado"] = rodar_bateria(bateria, ctx, saida / "recibos", a.modo, a.fase, a.sandbox, recibo.get("recibo_pre_selo"))
            if recibo["bateria_resultado"]["veredito"] != "BATERIA_PASSA":
                return fechar(veredito_base + "__BATERIA_FALHOU__NADA_GRAVADO_NA_BANCADA", 3)
        # 6. aplicar (so com evento verificado e bateria passada)
        if a.modo == "aplicar":
            if novo_bytes is None:
                recibo["aplicacao"] = dict(nota="ja sincronizada: nada a gravar")
                return fechar(veredito_base + "__NADA_A_GRAVAR", 0)
            recibo["aplicacao"] = aplicar_na_bancada(bancada, canonical_mod, novo_bytes, contrato, nos_info, a.versao, n, stamp)
            est = bancada / "estado" / "sincronizacao"
            est.mkdir(parents=True, exist_ok=True)
            recibo["aplicacao"]["copia_do_recibo"] = str(est / ("RECIBO_SINCRONIZACAO_%s_%s.json" % (a.versao, stamp)))
            recibo["veredito"] = veredito_base + "__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO"
            recibo["fim_utc"] = agora()
            gravar_novo(est / ("RECIBO_SINCRONIZACAO_%s_%s.json" % (a.versao, stamp)), json_bytes(recibo))
            return fechar(recibo["veredito"], 0)
        return fechar(veredito_base + "__ENSAIO__NADA_GRAVADO_NA_BANCADA", 0)
    except Recusa as exc:
        return fechar("RECUSADA", 2, str(exc))
    except Exception as exc:   # qualquer erro nao previsto tambem e recusa visivel, com recibo -- nunca traceback mudo nem "ok" falso
        return fechar("RECUSADA", 2, "ERRO_NAO_PREVISTO: %s: %s" % (type(exc).__name__, exc))


if __name__ == "__main__":
    sys.exit(main())
