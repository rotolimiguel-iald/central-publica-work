# -*- coding: utf-8 -*-
"""O VÍNCULO PATENTÁRIO público (pedido do operador, 22/10/2026: «quero que vc mostre o vínculo às patentes também, o público precisa
saber que está patenteado e onde e sob qual número»). Do docket (patents/*/docket.yaml), só os campos do vínculo: o pedido no INPI, o
título, a classe, o depósito, a prioridade, o PCT na OMPI (número e data) e os processos adicionais (número, data, papel genérico: sem
GRU, protocolo ou pagamento). O DEPOSITANTE e o INVENTOR são LIDOS do próprio formulário de depósito do INPI (texto extraído no cofre,
vault/normalized_docs), e o REQUERENTE do PCT dos recibos do ePCT — nunca digitados. ERRATA AO LADO (22/10/2026): a 1ª versão deste
gerador DIGITOU «IALD Ltda.» como titular; os 16 formulários dizem depositante LUIZ ANTONIO ROTOLI MIGUEL, Pessoa Física (e inventor o
mesmo); o número corrigiu a frase antes de publicar. Do que se lê, só sai o nome e o tipo de pessoa: CPF, endereço e contato ficam fora.
Estatuto dito: pedido de patente depositado — não patente concedida.
Uso: vinculo_patentario.py <pasta_do_retrato>   (atualiza o retrato: lista, detalhe e api/vinculo_patentario.json)"""
import json, re, sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
CENTRAL = Path(r"C:\IALD\Central de Patentes")
PAT = CENTRAL / "patents"
NORM = CENTRAL / "vault" / "normalized_docs"
EPCT = CENTRAL / "EPCT"
PROC = re.compile(r"N[úu]mero do Processo:\s*(BR\s*\d{2}\s*\d{4}\s*\d{6}\s*\d)")
DEP = re.compile(r"Dados do Depositante.*?Nome ou Raz[ãa]o Social:\s*([^\n]+)\n.*?Tipo de Pessoa:\s*([^\n]+)", re.S)
INV = re.compile(r"Dados do Inventor.*?Nome:\s*([^\n]+)", re.S)
APP = re.compile(r"Applicant\(s\)\s+([A-ZÀ-Ú][A-Za-zÀ-ú ,.'-]{2,60})")
APP_JSON = re.compile(r'"applicant"\s*:\s*"([^"(]{3,80})')


def _so_nome(s):
    """Só o nome: corta parênteses, dígitos e o que vier depois de vírgula de documento — CPF e endereço nunca saem."""
    s = re.sub(r"\(.*", "", s)
    s = re.sub(r"\d.*", "", s)
    return re.sub(r"\s+", " ", s).strip(" ,;-")


def _depositantes():
    out = {}
    for p in NORM.rglob("*.txt"):
        t = p.read_text(encoding="utf-8", errors="replace")
        if "Dados do Depositante" not in t:
            continue
        for m in PROC.finditer(t):
            proc = re.sub(r"\s+", "", m.group(1))
            d = DEP.search(t[m.end(): m.end() + 4000])
            i = INV.search(t[m.end(): m.end() + 20000])
            if d:
                out.setdefault(proc, set()).add((_so_nome(d.group(1)), _so_nome(d.group(2)), _so_nome(i.group(1)) if i else None))
    return out


def _requerentes_pct(dirname):
    """O requerente como a OMPI o escreve nos recibos do ePCT («Applicant(s) …»); sem recibo, o do dossiê do pedido."""
    da_ompi, do_dossie = set(), set()
    base = EPCT / dirname
    if not base.is_dir():
        return da_ompi
    for p in base.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".txt", ".json", ".md") and p.stat().st_size < 5 * 1024 * 1024:
            t = p.read_text(encoding="utf-8", errors="replace")
            for rx, alvo in ((APP, da_ompi), (APP_JSON, do_dossie)):
                for m in rx.finditer(t):
                    n = _so_nome(m.group(1))
                    if len(n) >= 5:
                        alvo.add(n)
    return da_ompi or do_dossie


def ler_vinculos():
    deps = _depositantes()
    out = []
    for pdir in sorted(PAT.iterdir()):
        if not pdir.is_dir() or not pdir.name.startswith("BR") or not (pdir / "docket.yaml").is_file():
            continue
        d = yaml.safe_load((pdir / "docket.yaml").read_text(encoding="utf-8")) or {}
        ep = d.get("epct") if isinstance(d.get("epct"), dict) else {}
        adic = []
        for x in d.get("processos_adicionais") or []:
            if isinstance(x, dict) and x.get("processo"):
                n = str(x["processo"])
                papel = ("fase nacional brasileira do PCT" if n.startswith("BR11") else "pedido BR adicional (a mesma invenção)")
                adic.append({"processo": n, "deposito": str(x.get("filing_date") or "") or None, "protocolo_nacional": str(x.get("protocolo") or "") or None,
                             "papel": papel, "escritorio": "INPI (Brasil)"})
        pedido = d.get("processo") or pdir.name.split("_")[0]
        lidos = sorted(deps.get(pedido.replace("-", ""), set()), key=lambda x: (x[0] or "", x[1] or "", x[2] or ""))
        assert lidos, ("depositante não lido do formulário do INPI — PARAR (não se digita)", pedido)
        assert len({(a, b) for a, b, _ in lidos}) == 1, ("depositantes divergentes entre cópias do formulário — PARAR", pedido, lidos)
        dep_nome, dep_tipo, inventor = lidos[0]
        req = sorted(_requerentes_pct(pdir.name)) if (ep or {}).get("numero") else []
        titular = "%s (%s) — depositante%s, conforme o formulário de depósito no INPI" % (
            dep_nome, dep_tipo.lower(), " e inventor" if inventor and inventor.upper() == dep_nome.upper() else "")
        out.append({"estatuto": "pedido de patente depositado (não é patente concedida)", "pedido_inpi": pedido,
                    "titulo": d.get("titulo"), "classe": d.get("classe"), "deposito": str(d.get("filing_date") or "") or None,
                    "prioridade": str(d.get("priority_date") or "") or None,
                    "escritorio": "INPI — Instituto Nacional da Propriedade Industrial (Brasil)",
                    "pct": (ep or {}).get("numero"), "pct_data": str((ep or {}).get("data") or "") or None,
                    "pct_escritorio": "OMPI/WIPO (PCT)" if (ep or {}).get("numero") else None,
                    "pct_requerente": "; ".join(req) or None,
                    "processos_adicionais": adic, "depositante": dep_nome, "tipo_de_pessoa": dep_tipo, "inventor": inventor,
                    "titular": titular, "fonte_do_depositante": "formulário de depósito do INPI (texto extraído no cofre da Central)",
                    "dir": pdir.name})
    return out


if __name__ == "__main__":
    OUT = Path(sys.argv[1])
    mapa = json.loads((OUT / "api" / "_mapa.json").read_text(encoding="utf-8"))
    vs = {v["pedido_inpi"]: v for v in ler_vinculos()}
    lp = OUT / mapa["/api/patents"]
    lista = json.loads(lp.read_text(encoding="utf-8"))
    for row in lista:
        v = vs.get(row["id"])
        if v:
            row["epct_number"] = v["pct"]
    lp.write_text(json.dumps(lista, ensure_ascii=False), encoding="utf-8")
    for pid, v in vs.items():
        u = "/api/patents/" + pid
        if u not in mapa:
            continue
        p = OUT / mapa[u]
        det = json.loads(p.read_text(encoding="utf-8"))
        det["epct_number"], det["epct_date"] = v["pct"], v["pct_data"]
        det["vinculo_patentario"] = {k: v[k] for k in v if k != "dir"}
        p.write_text(json.dumps(det, ensure_ascii=False), encoding="utf-8")
    (OUT / "api" / "vinculo_patentario.json").write_text(json.dumps([{k: v[k] for k in v if k != "dir"} for v in vs.values()],
                                                                    ensure_ascii=False, indent=1), encoding="utf-8")
    print("vínculo no retrato: %d pedidos | %d com PCT | %d processos adicionais | depositantes: %s | requerentes do PCT: %s" % (
        len(vs), sum(1 for v in vs.values() if v["pct"]), sum(len(v["processos_adicionais"]) for v in vs.values()),
        sorted({(v["depositante"], v["tipo_de_pessoa"]) for v in vs.values()}), sorted({str(v["pct_requerente"]) for v in vs.values()})))
