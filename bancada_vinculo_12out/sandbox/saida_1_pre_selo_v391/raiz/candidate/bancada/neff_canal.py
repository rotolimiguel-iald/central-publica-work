"""Pinned documentary N_eff channel: both Yp hypotheses, no nature verdict.

Reuses F5.2 R3 Table-5 extraction with a stdlib parser. The radiation-background
identity is conditional on rho+p closure; it is not a perturbed CMB likelihood.
No historical calendar or misattributed CMB-SPA row is served. beta_0 is computed
from canonical alpha(0), never inferred from an unspecified high-energy scale.
"""
from __future__ import annotations
import ast
import hashlib
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
from .canonical import read_alpha, require_current

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).with_name("neff_fontes_f52.json")
MANIFEST_SHA256 = "92cb676c4c5e661228577223c7430652e5d3842ee279f55f6b9f0d849da1f277"
F_NU = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)
HEADERS = ("", "SPT-3G D1", "SPT+ACT", "CMB-SPA", "SPT-3G D1 + DESI")
TABLE_ID = "S7.T5.2"

class FonteRecusada(ValueError):
    """Source identity, structure or numeric input was refused."""

def _number(value, name, *, zero=False):
    if type(value) not in (int, float):
        raise FonteRecusada(f"{name}: numeric type required; bool/text refused")
    result = float(value)
    if not math.isfinite(result) or (result < 0 if zero else result <= 0):
        raise FonteRecusada(f"{name}: finite {'nonnegative' if zero else 'positive'} value required")
    return result

def _read_entry(entry):
    if not isinstance(entry, dict):
        raise FonteRecusada("invalid source entry")
    relative, pin, count = (entry.get(k) for k in ("relative_path", "sha256", "bytes"))
    if (not isinstance(relative, str) or not isinstance(pin, str) or not re.fullmatch(r"[0-9a-f]{64}", pin, re.ASCII)
            or type(count) is not int or count <= 0):
        raise FonteRecusada("invalid source path/pin/length")
    path = (ROOT / relative).resolve()
    if not path.is_relative_to((ROOT / "fontes_externas/F5.2").resolve()):
        raise FonteRecusada("source escapes F5.2 custody directory")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise FonteRecusada(f"source unavailable: {path}") from exc
    if hashlib.sha256(raw).hexdigest() != pin or len(raw) != count:
        raise FonteRecusada(f"source hash/size differs: {path.name}")
    return raw, {"path": str(path), "sha256": pin, "bytes": count,
                 "origin": entry.get("origin"), "source_admission": "D8_PENDING"}

def _sources():
    try:
        raw = MANIFEST.read_bytes()
        if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA256:
            raise FonteRecusada("N_eff manifest hash differs")
        manifest = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FonteRecusada("N_eff manifest unreadable") from exc
    if (manifest.get("schema") != "iald.f5_2.channel_sources.v1"
            or set(manifest.get("sources", {})) != {"frozen", "table5_v1", "table5_v2"}):
        raise FonteRecusada("N_eff manifest schema/source set differs")
    contents, provenance = {}, {}
    for key, entry in manifest["sources"].items():
        contents[key], provenance[key] = _read_entry(entry)
    return contents, provenance, manifest

def _frozen(raw):
    """Extract once from checked bytes; reject duplicate assignments."""
    try:
        values = {}
        for node in ast.parse(raw.decode("utf-8-sig")).body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                key = node.targets[0].id
                if key in {"NEFF_SM", "MEDIDAS", "PROJECOES"}:
                    if key in values:
                        raise FonteRecusada(f"duplicate frozen assignment: {key}")
                    values[key] = ast.literal_eval(node.value)
        if set(values) != {"NEFF_SM", "MEDIDAS", "PROJECOES"}:
            raise FonteRecusada("frozen fields missing")
        return values
    except (ValueError, SyntaxError, UnicodeError) as exc:
        raise FonteRecusada("frozen AST cannot be read") from exc

class _Node:
    def __init__(self, tag, attrs=(), parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []
    def nodes(self, tag=None):
        for child in self.children:
            if isinstance(child, _Node):
                if tag is None or child.tag == tag:
                    yield child
                yield from child.nodes(tag)
    def text(self, separator=" "):
        parts = [c.text(separator) if isinstance(c, _Node) else c.strip() for c in self.children]
        return separator.join(p for p in parts if p).strip()

class _TableParser(HTMLParser):
    VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = _Node("root")
        self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        child = _Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(child)
        if tag not in self.VOID:
            self.stack.append(child)
    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(_Node(tag, attrs, self.stack[-1]))
    def handle_endtag(self, tag):
        for index in range(len(self.stack)-1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break
    def handle_data(self, data):
        self.stack[-1].children.append(data)

def _table5(raw, version, source):
    parser = _TableParser()
    parser.feed(raw.decode("utf-8"))
    found = [n for n in parser.root.nodes("table") if n.attrs.get("id") == TABLE_ID]
    if len(found) != 1:
        raise FonteRecusada("Table 5 anchor must be unique")
    table = found[0]
    captions = [n for n in table.parent.nodes() if "ltx_caption" in n.attrs.get("class", "").split()]
    if not any(n.text().startswith("Table 5:") for n in captions):
        raise FonteRecusada("Table 5 caption missing")
    rows = [n for n in table.children if isinstance(n, _Node) and n.tag == "tr"]
    cells = [[n for n in row.children if isinstance(n, _Node) and n.tag in {"th","td"}] for row in rows]
    if len(cells) != 5 or any(len(row) != 5 for row in cells) or tuple(n.text() for n in cells[0]) != HEADERS:
        raise FonteRecusada("Table 5 row/column/reader order differs")
    if any("N eff" not in cells[i][0].text() for i in (1,3)) or any("Y P" not in cells[i][0].text() for i in (2,4)):
        raise FonteRecusada("Table 5 row labels differ")
    result = []
    for index, yp in ((1,"BBN_CONSISTENCY"),(3,"FREE")):
        cell = cells[index][3]
        math_nodes = list(cell.nodes("math"))
        if len(math_nodes) != 1:
            raise FonteRecusada("cell MathML absent/ambiguous")
        values = tuple(_number(float(n.text("")), "MathML value") for n in math_nodes[0].nodes("mn"))
        if len(values) != (2 if yp == "BBN_CONSISTENCY" else 3):
            raise FonteRecusada("symmetric/asymmetric cell form differs")
        result.append({"conjunto":"CMB-SPA (SPT-3G D1 + Planck + ACT)", "version":version, "yp":yp,
                       "N_eff_obs":values[0], "sigma":values[1] if yp == "BBN_CONSISTENCY" else None,
                       "sigma_plus":values[1] if yp == "BBN_CONSISTENCY" else values[2], "sigma_minus":values[1],
                       "source_basis":source, "fonte":f"arXiv:2506.20707{version}; Table 5, CMB-SPA",
                       "table_id":TABLE_ID, "cell_id":cell.attrs.get("id"), "selected_for_verdict":False,
                       "estatuto":"[REAL documental — extraído dos bytes pinados; admissão D8 e escolha X16 OPEN]"})
    return result

def beta_runtime():
    alpha, provenance = read_alpha(root=ROOT)
    alpha = _number(alpha, "canonical alpha")
    return alpha * math.sqrt(math.e), alpha, provenance["um_py_sha256"]

def dN_dbeta(N):
    return (4.0/3.0) * (1.0 + F_NU * _number(N, "N_base", zero=True)) / F_NU

def canal(N_base=None, sigmas_extra=()):
    """Yp stays unselected; this documentary comparison emits no nature verdict."""
    if not isinstance(sigmas_extra, (tuple,list)) or len(sigmas_extra) > 1000:
        raise FonteRecusada("sigmas_extra must be a bounded list/tuple")
    extra = [_number(s, "sigma_extra") for s in sigmas_extra]
    if N_base is not None:
        N_base = _number(N_base, "N_base", zero=True)
    current = require_current("neff_canal", root=ROOT)
    alpha, canonical = read_alpha(root=ROOT)
    alpha = _number(alpha, "canonical alpha")
    beta = alpha * math.sqrt(math.e)
    contents, sources, _ = _sources()
    frozen = _frozen(contents["frozen"])
    base = _number(frozen["NEFF_SM"], "NEFF_SM", zero=True) if N_base is None else N_base
    delta = dN_dbeta(base) * beta
    values, excluded = [], 0
    for center, sigma, label, reference, independent in frozen["MEDIDAS"]:
        if "CMB-SPA" in label:
            excluded += 1
            continue
        center, sigma = _number(center,"published N_eff",zero=True), _number(sigma,"published sigma")
        values.append({"rotulo":label,"fonte":reference,"independente":independent,"N_eff_obs":center,"sigma":sigma,
                       "separacao_TGL_SM_sigma":delta/sigma,"tensao_TGL_contra_centro_sigma":abs(base+delta-center)/sigma,
                       "tensao_SM_contra_centro_sigma":abs(base-center)/sigma,"estatuto":"[DECLARADO — transcrição histórica; D8 pendente]"})
    if excluded != 1:
        raise FonteRecusada("expected one historical CMB-SPA row to suppress")
    options = _table5(contents["table5_v1"],"v1",sources["table5_v1"]) + _table5(contents["table5_v2"],"v2",sources["table5_v2"])
    result = {"ok":True,"mode":"PINNED_DOCUMENTARY_BACKGROUND_EQUIVALENCE","canonical_provenance":canonical,
              "current_contract":current,"source_manifest_sha256":MANIFEST_SHA256,"sources":sources,
              "beta_runtime":beta,"alpha_lido_do_um_py":alpha,"um_py_sha256":canonical["um_py_sha256"],
              "mu_do_rito":"q→0 (Thomson; Teorema da Escala)","beta_scope":"BETA_0_THOMSON",
              "N_base":base,"dN_eff_dbeta":dN_dbeta(base),"delta_N_eff":delta,"N_eff_TGL":base+delta,
              "sigma_para_5sigma_de_separacao":delta/5.0,"medidas":values,
              "projecoes":[{"rotulo":"sigma informada","sigma_N_eff":s,"separacao_TGL_SM_sigma":delta/s,
                            "estatuto":"[DERIVED — cenário fornecido; sem calendário]"} for s in extra],
              "opcoes_CMB_SPA_Yp":[r for r in options if r["version"]=="v2"],"opcoes_CMB_SPA_Yp_v1_v2":options,
              "escolha_Yp":"OPEN_X16_NO_SELECTION","primary_observation":None,"source_admission":"D8_PENDING",
              "obsolete_frozen_row_suppressed":True,"historical_projection_calendars_suppressed":True,"calendar":None,
              "background_only":True,"perturbed_cmb_likelihood":False,"veredito":"NENHUM","gate_effect":"NONE"}
    json.dumps(result, allow_nan=False)
    return result

def controle_anti_dupla_contagem(z=(1.0e6,1.0e7), H0=67.36, ombh2=0.02237, omch2=0.1200,
                               dispositivo="cpu", n_grade=20001, tol=1.0e-4):
    """Synthetic background identity check; no observed likelihood."""
    require_current("neff_controle_anti_dupla_contagem", root=ROOT)
    if not isinstance(z,(tuple,list)) or not z:
        raise FonteRecusada("z must be a nonempty list/tuple")
    redshifts = [_number(x,"z") for x in z]
    H0,ombh2,omch2,tol = (_number(v,k) for v,k in ((H0,"H0"),(ombh2,"ombh2"),(omch2,"omch2"),(tol,"tol")))
    if type(n_grade) is not int or n_grade < 100:
        raise FonteRecusada("invalid integration grid")
    import torch
    from .fundo_gpu import FundoV3Lote
    beta,_,_ = beta_runtime()
    base = FundoV3Lote(dispositivo=dispositivo,n_grade=n_grade)
    shifted = base.Neff + dN_dbeta(base.Neff)*beta
    control = FundoV3Lote(dispositivo=dispositivo,n_grade=n_grade,Neff=shifted)
    t = lambda x: torch.tensor([x],dtype=torch.float64,device=base.dev)
    first = base.fundo(t(H0),t(ombh2),t(omch2),t(beta),t(0.0))
    second = control.fundo(t(H0),t(ombh2),t(omch2),t(0.0),t(0.0))
    zz = torch.tensor([redshifts],dtype=torch.float64,device=base.dev)
    differences = [x-1.0 for x in (base.Ez(first,zz)/control.Ez(second,zz))[0].tolist()]
    if not all(math.isfinite(x) for x in differences):
        raise FonteRecusada("nonfinite background residual")
    return {"z":redshifts,"N_eff_bancada":base.Neff,"N_eff_deslocado":shifted,"razao_E_menos_1":differences,
            "tolerancia":tol,"passou":all(abs(x)<tol for x in differences),"mode":"SYNTHETIC_BACKGROUND_IDENTITY_ONLY",
            "observed_data_used":False,"gate_effect":"NONE"}
