# -*- coding: utf-8 -*-
"""guard_D.py -- GUARDA NOVO do conjunto D (ramo B do ringdown), pinado ao PRE-REGISTRO V1 (sha16 86f98fcc124dd9ca).
Substitui a cadeia vencida 013-bis/015 (registration_guard: hard_deadline 2026-10-03, recibo de auditoria ausente, pasta Chatgpt so leitura,
caminhos de strain fora da raiz permitida). A API reproduz os nomes que pe_runner.py/run_controlled.py (v1_1_2) importam de registration_guard:
  checked_registration, authorize_event, time_guard, contained, sha, load_jobs, validate_launch, positive, integer, publish_new, utc, output_path
de modo que as copias deles podem trocar o import por `import guard_D as registration_guard` sem mexer em mais nada.

O que confere, FAIL-CLOSED (qualquer divergencia = excecao, nunca "ok" falso):
  (1) V1 (JSON+MD) por sha256 contra V1_RAMO_B_HASHES.json e contra o sha16 da ordem do operador;
  (2) PINOS_D_V1.json: os 10 eventos SEM HOLD do V1 (os 4 holds e os 8 pendentes ficam FORA), GPS do catalogo, strain (caminho+bytes+sha256 do
      MANIFESTO O4), constantes da Fase 6, beta = alpha*sqrt(e) em runtime, arvore de codigo (cada .py de codigo_D) e copias somente-leitura;
  (3) modo por evento: blind_test (PE cega) e calibration (SO injecao C2 em off-source REAL do proprio evento, longe do intervalo protegido);
  (4) relogio NOVO (RELOGIO_D.json), com prazo dito, ligado ao hash dos pinos; sem relogio aberto, nada lanca;
  (5) anti-CLI direto (validate_launch): contexto de lancamento, lider de sessao, PRIVATE.log como stdout/stderr.
Nada aqui abre posterior de evento real. Estatuto: codigo [REAL]; hipotese do V1 [ONTO/CONJECTURE].
"""
import hashlib
import json
import math
import os
import re
import stat
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

CODE = Path(__file__).resolve().parent
BASE = CODE.parent
sys.path.insert(0, str(CODE))
import v1_ramo_b as V  # noqa: E402

PRIV = Path(V.native("C:/Users/rotol/.iald_privado/conjunto_D_20261029"))
PINOS = BASE / "PINOS_D_V1.json"
RELOGIO = BASE / "RELOGIO_D.json"
JOBS = BASE / "JOBS_D_V1.json"
CONGELAMENTO = BASE / "CONGELAMENTO_D.json"
SAIDAS = PRIV / "pe"
PRAZO_DIAS_PROPOSTO = 21          # prazo dito (proposta); o ato de abrir o relogio o grava e o liga ao hash dos pinos
JANELA_C2_DISTANCIA_MIN_S = 64    # a janela de ruido da injecao termina >= 64 s antes do GPS do evento real
DESLOC_JANELA_REAL_S = 12         # segment_start real = floor(GPS) - 12 (inteiro: o leitor recusa inicio fracionario fora da grade)
DURACAO_S = 16
PRIOR_TEMPO_S = 0.1               # geocent_time in [GPS - 0,1; GPS + 0,1]

MODOS = ("blind_test", "calibration")


class GuardError(RuntimeError):
    pass


# --------------------------------------------------------------------------------------------------- utilidades
def strict_json(payload):
    return V.strict_json(payload)


def sha(path):
    return V.sha256_file(str(path))


def utc(value):
    v = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if v.tzinfo is None:
        raise GuardError("fuso horario exigido")
    return v.astimezone(timezone.utc)


def positive(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError("valor positivo e finito exigido: " + name)
    return value


def integer(value, name, minimum=1):
    if type(value) is not int or value < minimum:
        raise ValueError("inteiro invalido: " + name)
    return value


def publish_new(path, value):
    raw = (json.dumps(value, indent=2, allow_nan=False, ensure_ascii=False) + "\n").encode()
    path = Path(path)
    temp = path.with_name(path.name + ".pending")
    with open(temp, "xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    if temp.stat().st_size != len(raw):
        raise OSError("temporario incompleto retido")
    os.link(temp, path)
    temp.unlink()


def _raizes_permitidas():
    return [Path(V.native(V.STRAIN_RAIZ)).resolve(), PRIV.resolve(), BASE.resolve()]


def contained(name, root=None):
    p = Path(V.native(str(name))).resolve()
    raizes = [Path(root).resolve()] if root is not None else _raizes_permitidas()
    if not any(p == r or r in p.parents for r in raizes):
        raise GuardError("caminho fora das raizes registradas: " + str(name))
    return p


def output_path(name):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,150}", name):
        raise ValueError("nome de saida inseguro")
    return SAIDAS / name


# --------------------------------------------------------------------------------------------------- pinos
def arvore_de_codigo():
    """sha256 de cada .py de codigo_D (a propria arvore e pinada; mudou um byte, o guarda recusa)."""
    return {p.name: sha(p) for p in sorted(CODE.glob("*.py"))}


def copias_ro():
    d = BASE / "copias_somente_leitura"
    return {p.name: sha(p) for p in sorted(d.glob("*.py"))}


def carregar_pinos():
    if not PINOS.exists():
        raise GuardError("PINOS_D_V1.json ausente: o guarda e fail-closed")
    raw = PINOS.read_bytes()
    return strict_json(raw), hashlib.sha256(raw).hexdigest()


def verificar_strain_bytes(eventos=None, pinos=None):
    """sha256 completo dos HDF5 contra o MANIFESTO (so bytes; NENHUMA amostra e aberta). Custa leitura de ~2 GB."""
    pinos = pinos or carregar_pinos()[0]
    out = {}
    for ev, e in pinos["eventos"].items():
        if eventos and ev not in eventos:
            continue
        for det, s in e["strain"].items():
            real = sha(contained(s["hdf5"]))
            if real != s["hdf5_sha256"]:
                raise GuardError("strain difere do manifesto: %s %s" % (ev, det))
            out[ev + "_" + det] = real[:16]
    return out


def _checar_pinos(pinos, v1, v1info, cr, k):
    if pinos["v1"]["json_sha256"] != v1info["PREREGISTRO_RAMO_B_RINGDOWN_V1.json"] or pinos["v1"]["md_sha256"] != v1info["PREREGISTRO_RAMO_B_RINGDOWN_V1.md"]:
        raise GuardError("V1 difere dos pinos")
    d10 = V.eventos_d10(v1)
    if sorted(pinos["eventos_d10"]) != sorted(d10) or sorted(pinos["eventos"]) != sorted(d10):
        raise GuardError("os 10 eventos dos pinos diferem dos 10 sem hold do V1")
    d = v1["spec"]["conjuntos"]["D"]
    if set(d10) & (set(d["com_data_quality_hold"]) | set(d["pendentes_AWAITING_GR_METADATA"])):
        raise GuardError("evento com hold/pendente dentro de D10")
    if V.sha256_file(V.MANIFESTO_STRAIN) != pinos["manifesto_strain_sha256"] or V.sha256_file(V.CATALOGO) != pinos["catalogo_sha256"]:
        raise GuardError("manifesto de strain ou catalogo difere dos pinos")
    cat = V.catalogo_d(d10)
    sp = V.strain_pins(d10)
    for ev in d10:
        e = pinos["eventos"][ev]
        if e["GPS"] != cat[ev]["GPS"]:
            raise GuardError("GPS difere do catalogo: " + ev)
        if e["segment_start_real"] != math.floor(e["GPS"]) - DESLOC_JANELA_REAL_S:
            raise GuardError("segment_start_real fora da regra floor(GPS)-12: " + ev)
        for det in ("H1", "L1"):
            m, p = sp[(ev, det)], e["strain"][det]
            if (m["hdf5_sha256"], m["hdf5_bytes"], m["hdf5"]) != (p["hdf5_sha256"], p["hdf5_bytes"], p["hdf5"]):
                raise GuardError("pino de strain difere do manifesto: %s %s" % (ev, det))
            f = contained(p["hdf5"])
            if not f.exists() or f.stat().st_size != p["hdf5_bytes"]:
                raise GuardError("arquivo de strain ausente ou com tamanho diferente: %s %s" % (ev, det))
    if pinos["fase6_criterios"] != {x: cr[x] for x in ("min_eventos", "z_excl", "poder_min", "sistematica_max_relativa")}:
        raise GuardError("criterios da Fase 6 diferem dos pinos")
    if abs(pinos["beta_runtime"] - k["beta"]) > 1e-15 or abs(k["beta"] - v1["spec"]["beta"]["valor_runtime"]) > 1e-15:
        raise GuardError("beta (alpha*sqrt(e)) difere do V1")
    for ev, e in pinos.get("sinteticos", {}).items():
        if ev in pinos["eventos"] or ev in d10:
            raise GuardError("evento sintetico com nome de evento real: " + ev)
        for det in ("H1", "L1"):
            p = e["strain"][det]
            f = contained(p["hdf5"])
            if not f.exists() or f.stat().st_size != p["hdf5_bytes"] or sha(f) != p["hdf5_sha256"]:
                raise GuardError("arquivo sintetico ausente ou difere do pino: %s %s" % (ev, det))
    if pinos["codigo"] != arvore_de_codigo():
        raise GuardError("arvore de codigo difere dos pinos (mudou byte depois do congelamento)")
    if pinos["copias_somente_leitura"] != copias_ro():
        raise GuardError("copias somente-leitura diferem dos pinos")


def checked_registration(verificar_relogio=True):
    """Devolve (reg, digest). digest = sha256 de PINOS_D_V1.json."""
    v1, v1info = V.carregar_v1()
    pinos, digest = carregar_pinos()
    cr = V.criterios_fase6()
    k = V.constantes_um_py()
    _checar_pinos(pinos, v1, v1info, cr, k)
    reg = dict(pinos)
    reg["calibration_event_ids"] = list(pinos["eventos_d10"])    # semantica: eventos cujo off-source pode receber injecao C2
    reg["event_reference_GPS"] = {ev: e["GPS"] for ev, e in pinos["eventos"].items()}
    reg["blinding"] = {"seed_path": pinos["semente"]["caminho"], "seed_commitment_sha256": pinos["semente"]["compromisso_sha256"],
                       "offset_half_range": pinos["semente"]["offset_half_range"]}
    reg["criterios"] = cr
    # F4.1 (qualificacao do instrumento): eventos SINTETICOS (ruido gaussiano de PSD de projeto, arquivos em formato GWOSC no diretorio privado), so em mode=calibration
    reg["sinteticos"] = pinos.get("sinteticos", {})
    for ev, e in reg["sinteticos"].items():
        reg["calibration_event_ids"].append(ev)
        reg["event_reference_GPS"][ev] = e["GPS"]
    reg["limites"] = {}
    if CONGELAMENTO.exists():
        cong = strict_json(CONGELAMENTO.read_bytes())
        if cong["pinos_sha256"] != digest:
            raise GuardError("congelamento ligado a outros pinos")
        reg["limites"] = cong.get("limites", {})
    if verificar_relogio:
        time_guard(reg)
    return reg, digest


# --------------------------------------------------------------------------------------------------- relogio
def abrir_relogio(prazo_dias, ordem_de_lancamento, pinos_digest=None, agora=None):
    """ATO DE LANCAMENTO (nao roda sozinho): grava RELOGIO_D.json em modo exclusivo. A ordem e um arquivo JSON do operador/gerencia
    com {opcao, ordem_operador_sha256, decidido_utc}. O prazo fica DITO e ligado ao hash dos pinos."""
    ordem_path = Path(ordem_de_lancamento)
    ordem = strict_json(ordem_path.read_bytes())
    for campo in ("opcao", "ordem_operador_sha256", "decidido_utc"):
        if campo not in ordem:
            raise GuardError("ordem de lancamento sem o campo " + campo)
    if ordem["opcao"] not in ("a", "c"):
        raise GuardError("opcao de lancamento deve ser 'a' (cadeia completa) ou 'c' (PE cega ate o estagio cego)")
    pinos_digest = pinos_digest or carregar_pinos()[1]
    now = agora or datetime.now(timezone.utc)
    prazo = integer(prazo_dias, "prazo_dias")
    dado = {"start_utc": now.isoformat(), "hard_deadline_utc": (now + timedelta(days=prazo)).isoformat(), "prazo_dias": prazo,
            "opcao": ordem["opcao"], "ordem_de_lancamento_sha256": sha(ordem_path), "ordem_operador_sha256": ordem["ordem_operador_sha256"],
            "pinos_sha256": pinos_digest}
    publish_new(RELOGIO, dado)
    return dado


def time_guard(reg=None):
    """Relogio NOVO. Fail-closed: ausente, adulterado, ligado a outros pinos, no futuro ou vencido => excecao."""
    if not RELOGIO.exists():
        raise GuardError("relogio novo nao aberto (RELOGIO_D.json ausente): nada lanca")
    r = strict_json(RELOGIO.read_bytes())
    if set(r) != {"start_utc", "hard_deadline_utc", "prazo_dias", "opcao", "ordem_de_lancamento_sha256", "ordem_operador_sha256", "pinos_sha256"}:
        raise GuardError("esquema do relogio difere")
    if r["pinos_sha256"] != carregar_pinos()[1]:
        raise GuardError("relogio ligado a outros pinos")
    start, dead, now = utc(r["start_utc"]), utc(r["hard_deadline_utc"]), datetime.now(timezone.utc)
    if dead != start + timedelta(days=r["prazo_dias"]):
        raise GuardError("aritmetica do prazo difere")
    if start > now + timedelta(seconds=2):
        raise GuardError("relogio comeca no futuro")
    if now >= dead:
        raise TimeoutError("prazo do relogio novo do conjunto D vencido")
    return dead


# --------------------------------------------------------------------------------------------------- semente / runtime
def check_seed(reg):
    b = reg["blinding"]
    p = contained(b["seed_path"])
    if not p.exists() or sha(p) != b["seed_commitment_sha256"] or p.stat().st_size != 32:
        raise GuardError("semente de cegueira ausente ou difere do compromisso")
    return True


def check_runtime(reg):
    """Compara as versoes do runtime WSL com as pinadas (so quando os modulos existem; no PE eles existem)."""
    esp = reg.get("runtime_esperado") or {}
    if not esp:
        raise GuardError("runtime nao pinado")
    from importlib import metadata
    atual = {}
    for mod in esp.get("pacotes", {}):
        try:
            atual[mod] = metadata.version(mod)
        except metadata.PackageNotFoundError:
            raise GuardError("pacote do runtime ausente: " + mod)
    if atual != esp["pacotes"] or ".".join(map(str, sys.version_info[:3])) != esp["python"]:
        raise GuardError("runtime difere do pinado")
    return True


# --------------------------------------------------------------------------------------------------- autorizacao de evento e jobs
def authorize_event(reg, event, mode):
    if mode not in MODOS:
        raise GuardError("modo desconhecido")
    if event in set(reg.get("sinteticos", {})):
        if mode != "calibration":
            raise GuardError("evento sintetico so em mode=calibration")
        return True
    d10 = set(reg["eventos_d10"])
    if event not in d10:
        raise GuardError("evento fora dos 10 sem hold do V1 (holds e pendentes ficam FORA): " + str(event))
    if mode == "blind_test":
        check_seed(reg)
    # calibration so existe para injecao C2 em off-source REAL do proprio evento; o gate de verdade e validate_job_D (load_jobs)
    return True


def _entrada(reg, ev):
    e = reg["eventos"].get(ev)
    return e if e is not None else reg["sinteticos"][ev]


def priors_do_evento(reg, event, tempo_central=None):
    """D1 (escrito ANTES): d_L ate 10 000 Mpc (5 de 10 eventos > 2 000 Mpc); so dtau220 livre; tempo +-0,1 s em torno do GPS do catalogo."""
    gps = _entrada(reg, event)["GPS"] if tempo_central is None else tempo_central
    return {
        "mass_1": {"kind": "Uniform", "minimum": 15.0, "maximum": 100.0},
        "mass_2": {"kind": "Uniform", "minimum": 10.0, "maximum": 100.0},
        "mass_ratio": {"kind": "Constraint", "minimum": 0.125, "maximum": 1.0},
        "chi_1": {"kind": "Uniform", "minimum": -0.99, "maximum": 0.99},
        "chi_2": {"kind": "Uniform", "minimum": -0.99, "maximum": 0.99},
        "luminosity_distance": {"kind": "Uniform", "minimum": 100.0, "maximum": 10000.0},
        "theta_jn": {"kind": "Sine", "minimum": 0.0, "maximum": math.pi},
        "phase": {"kind": "Uniform", "minimum": 0.0, "maximum": 2 * math.pi, "boundary": "periodic"},
        "ra": {"kind": "Uniform", "minimum": 0.0, "maximum": 2 * math.pi, "boundary": "periodic"},
        "dec": {"kind": "Cosine", "minimum": -math.pi / 2, "maximum": math.pi / 2},
        "psi": {"kind": "Uniform", "minimum": 0.0, "maximum": math.pi, "boundary": "periodic"},
        "geocent_time": {"kind": "Uniform", "minimum": gps - PRIOR_TEMPO_S, "maximum": gps + PRIOR_TEMPO_S},
        "dtau220": {"kind": "Uniform", "minimum": -0.8, "maximum": 2.0},
        "dtau440": 0.0, "domega220": 0.0, "domega440": 0.0,
    }


def validate_job_D(reg, nome, cfg):
    """O gate de verdade de cada job (a cadeia antiga fazia isso com revisoes; aqui: pinos + regras fixas do V1/D1)."""
    ev, mode = cfg["event"], cfg["mode"]
    authorize_event(reg, ev, mode)
    e = _entrada(reg, ev)
    sintetico = ev in reg.get("sinteticos", {})
    if float(cfg["event_GPS"]) != e["GPS"]:
        raise GuardError("event_GPS do job difere do pino")
    centro = None
    if mode == "calibration" and cfg.get("injection") is not None:
        centro = cfg["injection"]["parameters"]["geocent_time"]     # C2: o prior de tempo e centrado no instante INJETADO (off-source), nao no evento real
    if cfg["priors"] != priors_do_evento(reg, ev, centro):
        raise GuardError("priors do job diferem do contrato D1: " + nome)
    if cfg.get("fixed_deformation_parameters") != {"dtau440": 0.0, "domega220": 0.0, "domega440": 0.0} or cfg.get("variant") != "registered_fixed_deformation_variant":
        raise GuardError("so dtau220 e livre no V1")
    if cfg["duration_s"] != DURACAO_S or cfg["privacy_mode"] != "procedural_same_host":
        raise GuardError("duracao/privacidade fora do contrato")
    positive(cfg["wall_budget_seconds"], "wall_budget_seconds")
    if cfg["sampler"]["workers"] > 28:
        raise GuardError("teto de workers")
    teto = reg.get("limites", {}).get("wall_max_por_job_s")
    if teto is not None and cfg["wall_budget_seconds"] > teto:
        raise GuardError("parede por job acima do teto dos pinos")
    for det in cfg["detectors"]:
        d = cfg["data"][det]
        pin = e["strain"][det]
        for chave in ("onsource", "offsource"):
            if contained(d[chave + "_path"]) != contained(pin["hdf5"]) or d[chave + "_sha256"] != pin["hdf5_sha256"]:
                raise GuardError("job aponta strain fora dos pinos: %s %s" % (nome, det))
    gps, start = e["GPS"], float(cfg["segment_start_GPS"])
    if mode == "blind_test":
        if cfg.get("injection") is not None:
            raise GuardError("injecao proibida em job cego")
        if start != e["segment_start_real"]:
            raise GuardError("janela do job cego difere da regra floor(GPS)-12")
        if cfg["offsource_exclusion_s"] < 16:
            raise GuardError("exclusao do PSD menor que 16 s")
    else:
        inj = cfg.get("injection")
        if inj is None or inj.get("family") != "pSEOBNRv4HM_PA" or inj.get("noise_kind") != "REAL_OFFSOURCE":
            raise GuardError("calibration so com injecao pSEOB em off-source (real, em D; sintetico, em F4.1)")
        if start + cfg["duration_s"] > gps - JANELA_C2_DISTANCIA_MIN_S:
            raise GuardError("janela de ruido da injecao encosta no evento real")
        if float(inj["target_network_optimal_SNR"]) != e["snr_rede"]:
            raise GuardError("SNR-alvo da injecao difere do SNR de rede do catalogo")
        p = inj["parameters"]
        if p["dtau440"] != 0 or p["domega220"] != 0 or p["domega440"] != 0:
            raise GuardError("injecao C2 deforma so o 220")
        if p["dtau220"] not in (0.0, e.get("delta_pred_pinado")):
            raise GuardError("dtau220 injetado deve ser 0 (so-RG) ou o delta_pred do V1 para o evento")
    return True


def load_jobs(reg, digest):
    if not CONGELAMENTO.exists() or not JOBS.exists():
        raise GuardError("congelamento ausente: JOBS_D_V1.json so vale com CONGELAMENTO_D.json")
    cong = strict_json(CONGELAMENTO.read_bytes())
    if cong["pinos_sha256"] != digest or cong["jobs_sha256"] != sha(JOBS):
        raise GuardError("jobs/pinos diferem do congelamento")
    jobs = strict_json(JOBS.read_bytes())
    reg = dict(reg)
    reg["limites"] = cong.get("limites", {})       # D2: o teto de parede por job vem do congelamento (decidido pela medida de F4.1)
    for nome, cfg in jobs.items():
        validate_job_D(reg, nome, cfg)
    return jobs


def validate_launch(context_path, reg, digest, job, cfg):
    """Porta de validate_launch (v1_1_2 l.357-386): so o run_controlled satisfaz; CLI direto e recusado."""
    path = contained(context_path)
    context = strict_json(path.read_bytes())
    out = output_path(cfg["output_directory_name"])
    if path != out / "LAUNCH_CONTEXT.json" or context["registration_sha256"] != digest or context["job"] != job:
        raise GuardError("identidade de lancamento difere")
    if context["config_sha256"] != hashlib.sha256(json.dumps(cfg, sort_keys=True, allow_nan=False).encode()).hexdigest():
        raise GuardError("config difere do contexto do controlador")
    if os.name != "posix" or context["controller_pid"] != os.getppid() or os.getsid(0) != os.getpid() or os.getpgrp() != os.getpid():
        raise GuardError("o runner deve ser lider de novo grupo sob o controlador")
    pid = context["controller_pid"]
    ticks = Path("/proc/%d/stat" % pid).read_text().rsplit(")", 1)[1].split()[19]
    if ticks != context["controller_start_ticks"]:
        raise GuardError("PID do controlador reutilizado")
    if utc(context["stop_utc"]) > time_guard(reg) or datetime.now(timezone.utc) >= utc(context["stop_utc"]):
        raise TimeoutError("prazo de lancamento invalido")
    expected = (out / "PRIVATE.log").stat()
    for fd in (1, 2):
        actual = os.fstat(fd)
        if os.isatty(fd) or not stat.S_ISREG(actual.st_mode) or (actual.st_dev, actual.st_ino) != (expected.st_dev, expected.st_ino):
            raise GuardError("stdout/stderr devem ser o arquivo regular PRIVATE.log")
    if cfg["privacy_mode"] != "procedural_same_host":
        raise GuardError("contrato de privacidade desconhecido")
    check_runtime(reg)
    publish_new(out / "LAUNCH_CLAIM.json", dict(pid=os.getpid(), pgid=os.getpgrp(), registration_sha256=digest, context_sha256=sha(path),
                                                claimed_utc=datetime.now(timezone.utc).isoformat()))
    return context, out
