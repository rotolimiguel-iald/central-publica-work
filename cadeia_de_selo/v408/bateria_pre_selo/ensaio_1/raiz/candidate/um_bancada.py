# -*- coding: utf-8 -*-
"""um_bancada.py -- a BANCADA UM da TGL: o motor residente (CPU + GPU) com dados reais carregados, a régua dentro da máquina, uma API
para o operador e para as IAs, e a interface visual.

Uso:   C:\\Python314\\python.exe C:\\IALD\\Bancada_Um\\um_bancada.py          (abre em http://127.0.0.1:18777)
       ... --check    (só confere se está no ar)
Rede:  só 127.0.0.1; Host conferido; corpo POST ≤ 64 KB; nenhuma rota escreve fora de C:\\IALD\\Bancada_Um\\estado.
"""
import json
import os
import sys
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from bancada.canonical import CanonicalError, canonical_state, require_current

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
PORTA = 18777
HOSTS = {"127.0.0.1:%d" % PORTA, "localhost:%d" % PORTA}
UI = os.path.join(RAIZ, "ui")
ESTADO = os.path.join(RAIZ, "estado")
LAGO = [r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache", r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\cache",
        r"C:\IALD\observaveis_tgl\tgl_data_cache", r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\cache\gwosc"]
GW_OFICIAL = "http://127.0.0.1:18765"


class Bancada:
    def __init__(self):
        os.makedirs(ESTADO, exist_ok=True)
        self.activity_lock = threading.RLock()
        self.active_requests = 0
        self.quiescing = False
        self.inicio = time.time()
        self.pronta = False
        self.erro = None
        self.lago = None
        self.canonical_receipt = None
        try:
            self.canonical_receipt = require_current("server_startup", root=RAIZ)
        except Exception as exc:
            self.erro = str(exc)
            return
        from bancada.lago import Lago
        self.lago_res = Lago(LAGO)
        from bancada.gw import GWResidente
        self.gw = GWResidente(RAIZ)                      # o banco residente de ondas gravitacionais (Fase 6, 01/10)
        threading.Thread(target=self.gw.carregar, daemon=True).start()
        threading.Thread(target=self._carrega, daemon=True).start()
        threading.Thread(target=self._cataloga_lago, daemon=True).start()

    def _carrega(self):
        try:
            from bancada.motor import Motor
            from bancada.regua import Livro
            from bancada.evidencia import Evidencia
            self.motor = Motor(RAIZ)
            self.livro = Livro(os.path.join(ESTADO, "livro.sqlite3"))
            self.ev = Evidencia(self.motor, self.livro)
            require_current("resident_engine_loaded", root=RAIZ)  # no observed-data evaluation at startup
            self.pronta = True
            threading.Thread(target=self.lago_res.carregar_tudo, daemon=True).start()   # o lago inteiro na RAM, e fica
        except Exception as e:
            self.erro = repr(e)

    def _cataloga_lago(self):
        t0 = time.time()
        raizes = []
        for r in LAGO:
            tot, n, ext = 0, 0, {}
            maiores = []
            if os.path.isdir(r):
                for dp, dn, fn in os.walk(r):
                    for f in fn:
                        try:
                            s = os.path.getsize(os.path.join(dp, f))
                        except OSError:
                            continue
                        tot += s; n += 1
                        e = os.path.splitext(f)[1].lower() or "(sem)"
                        ext[e] = ext.get(e, 0) + s
                        maiores.append((s, os.path.relpath(os.path.join(dp, f), r)))
            maiores.sort(reverse=True)
            raizes.append(dict(raiz=r, existe=os.path.isdir(r), arquivos=n, bytes=tot,
                               por_extensao=dict(sorted(ext.items(), key=lambda kv: -kv[1])[:10]), maiores=[dict(bytes=s, arquivo=a) for s, a in maiores[:12]]))
        self.lago = dict(raizes=raizes, bytes_total=sum(x["bytes"] for x in raizes), segundos=round(time.time() - t0, 1),
                         nota="catálogo de tamanhos (só leitura); a carga RESIDENTE, com sha256 e tabelas, está em «residente»")

    def estado(self):
        import torch
        canon = canonical_state(root=RAIZ)
        out = dict(bancada="Bancada Um da TGL", versao="0.2-canonical", no_ar_desde=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.inicio)),
                   pronta=self.pronta and canon["ok"], motor_carregado=self.pronta, erro=self.erro,
                   canone=canon, atividades=self.atividades())
        try:
            import ctypes
            class M(ctypes.Structure):
                _fields_ = [("l", ctypes.c_ulong), ("c", ctypes.c_ulong), ("t", ctypes.c_ulonglong), ("a", ctypes.c_ulonglong),
                            ("tp", ctypes.c_ulonglong), ("ap", ctypes.c_ulonglong), ("tv", ctypes.c_ulonglong), ("av", ctypes.c_ulonglong), ("e", ctypes.c_ulonglong)]
            m = M(); m.l = ctypes.sizeof(M); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            out["ram"] = dict(total_gib=round(m.t / 2 ** 30, 1), livre_gib=round(m.a / 2 ** 30, 1))
        except Exception:
            out["ram"] = None
        if torch.cuda.is_available():
            livre, total = torch.cuda.mem_get_info()
            out["gpu"] = dict(nome=torch.cuda.get_device_name(0), vram_total_gib=round(total / 2 ** 30, 1), vram_livre_gib=round(livre / 2 ** 30, 1),
                              usada_pela_bancada_gib=round(torch.cuda.memory_allocated() / 2 ** 30, 3))
        if self.pronta:
            m = self.motor
            out["motor"] = dict(dispositivo=str(m.dev), n_grade=m.fundo.n, beta_tgl=m.beta_tgl, alpha=m.alpha,
                                tabela_camb=dict(sha256=m.tab.manifesto["sha256"], grade=m.tab.manifesto["grade"], erro_no_teste=m.erro_tabela),
                                fontes=dict(d1_v3=m.prov_d1, desi_dr2=m.prov_dr2, pantheon=m.prov_pan, alpha=m.prov_alpha))
            out["livro"] = dict(total=self.livro.resumo(0)["total"], familias_de_teste=self.livro.n_familias_de_teste())
        vals = {}
        for f in sorted(os.listdir(ESTADO)):
            if f.startswith("validacao") and f.endswith(".json"):
                try:
                    v = json.load(open(os.path.join(ESTADO, f), encoding="utf-8"))
                    vals[f] = dict(historico=True, resumo=v.get("resumo_curto"), veredito=v.get("veredito"),
                                   campos_disponiveis=list(v), alcance="VALIDACAO_HISTORICA_DELIMITADA")
                except Exception:
                    vals[f] = None
        out["validacoes"] = vals
        return out

    def atividades(self):
        active = []
        if not self.pronta and not self.erro:
            active.append(dict(kind="engine", estado="carregando"))
        for name in ("gw", "lago_res"):
            state = getattr(getattr(self, name, None), "estado", {})
            if state.get("estado") == "carregando":
                active.append(dict(kind=name, estado="carregando"))
        if self.active_requests:
            active.append(dict(kind="http", requests=self.active_requests))
        for kind, obj in (("cosmology", getattr(self, "ev", None)), ("gw", getattr(self, "gw", None))):
            for ident, task in list(getattr(obj, "tarefas", {}).items()):
                if task.get("estado") not in ("pronta", "falhou", "concluida", "cancelada"):
                    active.append(dict(kind=kind, id=ident, estado=task.get("estado")))
        return dict(idle=not active, active=active, quiescing=self.quiescing)

    def dados(self):
        m = self.motor
        d1 = m.d1
        from bancada.motor import OPCOES_ARTIGO, OPCOES_CORRIGIDO, OPCOES_SELADO, OPCOES_TGL
        return dict(
            planck_comp=dict(nome="Planck 2018 comprimido (R, ℓ_A, ω_b): média e diagonal do pipeline selado; fonte Chen, Huang & Wang 2019",
                             valores=d1["planck_mean"].tolist(), cov=d1["planck_cov"].tolist(), proveniencia=m.prov_d1,
                             errata_28set=("a citação «Zhai+ 2019» estava errada; as correlações fora da diagonal do pipeline estão mal transcritas "
                                           "(auditoria 28/09, D1F-03) — o modo «corrigido» usa a Tabela I de Chen+2019"),
                             cov_chen2019=m.planck_cov_chen.tolist(), proveniencia_chen2019=m.prov_planck_chen),
            opcoes=dict(padrao=OPCOES_TGL, selado_historico=OPCOES_SELADO, corrigido=OPCOES_CORRIGIDO, artigo=OPCOES_ARTIGO,
                        explicacao=dict(planck_cov="pipeline (o selado) | chen2019 (Tabela I de Chen, Huang & Wang 2019)",
                                        dr1_cov="diagonal (o selado) | correlacionada (DM–DH do mesmo z, DESI 2024 VI Tab. 1)",
                                        dm_star="direto (o selado; neutrino massivo contado duas vezes) | razao_camb (D_M(z*) por razão TGL/ΛCDM sobre o CAMB)",
                                        mapa_R="nu (Ω_m nu em R, o selado) | eff ((1+β)Ω_m: a escolha do Nível 2 S) — ESCOLHA [INPUT] não derivada; decide a sensibilidade a β",
                                        lei="d1a ((1+z*)^β, 𝒲 = 1) | d1b (E_ΛCDM(z*)^{2β/3}, 𝒲 = |1+w_eff|: o núcleo DERIVADO do artigo 1; Fase 4, 30/09)",
                                        beta_no_fundo="sim (β no fundo: mapa/E1) | nao (fundo ΛCDM, β só na lei: a convenção do artigo 1; empilhar os dois conta β duas vezes)",
                                        lei_sn="nenhuma (distâncias com o H0 de fundo) | sombra (D_M/K em todo z: o fator constante) | acumulada (K(z) na integral de D_M: o fluxo acumulado); SH0ES, 01/10",
                                        lei_cc="acumulada (a Fase 4) | nenhuma (os relógios leem a face)",
                                        cc_cov="diagonal (o que havia) | moresco2020 (Moresco+2020: 15 pontos com (z, H) da fonte + IMF/SPS correlacionados; 17 outros diagonais) | moresco2020_todos (faixa conservadora); Fase 7, 01/10"),
                        dr1_correlacoes=m.prov_dr1_corr),
            desi_dr1=dict(nome="DESI DR1 BAO (12 medidas, erro diagonal)", linhas=[dict(z=r[0], tipo=["DM/rd", "DH/rd", "DV/rd"][r[1]], sigma=r[2], valor=v)
                                                                             for r, v in zip(d1["desi_rows"], d1["desi_vals"].tolist())], proveniencia=m.prov_d1),
            desi_dr2=dict(nome="DESI DR2 BAO (13 medidas + covariância)", linhas=[dict(z=float(z), tipo={"DM_over_rs": "DM/rd", "DH_over_rs": "DH/rd", "DV_over_rs": "DV/rd"}[q],
                                                                                   valor=float(v), sigma=float(s ** 0.5))
                                                                              for z, v, q, s in zip(m.dr2["z"], m.dr2["valor"], m.dr2["grandeza"], m.dr2["cov"].diagonal())],
                          proveniencia=m.prov_dr2),
            sh0es=dict(nome="SH0ES H0", valor=d1["sh0es_mean"], sigma=d1["sh0es_sigma"], proveniencia=m.prov_d1),
            sh0es_local=dict(nome="SH0ES H0 lido como H0_local = H0·(1+z*)^β (lei D1a [CONJECTURE]; z* = 1089,95 [INPUT]; Fase 2, 30/09)",
                             valor=d1["sh0es_mean"], sigma=d1["sh0es_sigma"], proveniencia=m.prov_d1),
            cc_moresco=dict(nome="Cronômetros cósmicos H(z), Moresco+ 2022 (32 pontos; importados do artigo 1; Fase 4, 30/09: lidos com a lei acumulada de z* até z)",
                            n=int(m.cc["n"]), linhas=[dict(z=float(z), H=float(h), sigma=float(s)) for z, h, s in zip(m.cc["z"], m.cc["H"], m.cc["sigma"])], proveniencia=m.prov_cc),
            pantheon=dict(nome="Pantheon+ (cov STAT+SYS 1701×1701 LIGADA em 30/09; amostra só-cosmologia zHD > 0,01 sem calibradores; M profilado)",
                          n=int(len(m.pan["zHD"])), n_usadas=m.pantheon.n, proveniencia=m.prov_pan, ligacao=m.pantheon.proveniencia, diag=m.pantheon.diag_ratio),
            pantheon_sh0es=dict(nome="Pantheon+SH0ES (01/10): a amostra de H0 -- 1580 de cosmologia + 77 calibradores Cefeida (μ = CEPH_DIST, 37 hospedeiras); cov completa; M profilado",
                                n_usadas=m.pantheon_sh0es.n, n_calibradores=m.pantheon_sh0es.n_cal_usados, n_hospedeiras=m.pantheon_sh0es.n_hosts, proveniencia=m.prov_pan, ligacao=m.pantheon_sh0es.proveniencia),
            limites=m.limites)


B = None  # --check and imports must not start a second engine


class H(BaseHTTPRequestHandler):
    server_version = "BancadaUm/0.2-canonical"

    def log_message(self, fmt, *a):
        pass

    def _host_ok(self):
        return self.headers.get("Host", "") in HOSTS

    def _json(self, obj, code=200):
        if getattr(self, "_request_receipt", None) is not None:
            try:
                after = require_current("http_response", root=RAIZ)
                if after["canonical_manifest_sha256"] != self._request_receipt["canonical_manifest_sha256"]:
                    raise CanonicalError("CONTRACT_CHANGED_DURING_OPERATION")
                if isinstance(obj, dict):
                    obj = dict(obj, canonical_at_delivery=after)
            except CanonicalError as exc:
                obj, code = dict(ok=False, erro=str(exc), code="CANONICAL_REVALIDATION_REQUIRED"), 409
            self._request_receipt = None
        try:
            b = json.dumps(obj, ensure_ascii=False, default=str, allow_nan=False).encode("utf-8")
        except (ValueError, TypeError):
            b = b'{"ok":false,"erro":"NONFINITE_OR_INVALID_OUTPUT"}'; code = 422
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def _arquivo(self, rel):
        p = os.path.normpath(os.path.join(UI, rel))
        if os.path.commonpath([os.path.abspath(p), os.path.abspath(UI)]) != os.path.abspath(UI) or not os.path.isfile(p):
            return self._json(dict(erro="não encontrado"), 404)
        tipo = {".html": "text/html", ".js": "application/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".md": "text/markdown",
                ".json": "application/json"}.get(os.path.splitext(p)[1], "application/octet-stream")
        b = open(p, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", tipo + "; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _dispatch(self, method):
        path = self.path.split('?')[0]
        exempt = path in ('/api/estado', '/api/atividades', '/api/contratos', '/api/maintenance/quiesce') or not path.startswith('/api/')
        with B.activity_lock:
            if B.quiescing and not exempt:
                return self._json(dict(ok=False, erro='BENCH_MAINTENANCE'), 503)
            if not exempt:
                B.active_requests += 1
        try:
            return method()
        finally:
            if not exempt:
                with B.activity_lock:
                    B.active_requests -= 1

    def do_GET(self):
        return self._dispatch(self._get)

    def do_POST(self):
        return self._dispatch(self._post)

    def _get(self):
        self._request_receipt = None
        if not self._host_ok():
            return self._json(dict(erro="Host recusado"), 403)
        caminho = self.path.split("?")[0]
        try:
            if caminho in ("/", "/index.html"):
                return self._arquivo("index.html")
            if caminho.startswith("/ui/"):
                return self._arquivo(caminho[4:])
            if caminho == "/api/estado":
                return self._json(B.estado())
            if caminho == "/api/atividades":
                return self._json(B.atividades())
            if caminho == "/api/contratos":
                return self._json(canonical_state(root=RAIZ))
            if caminho.startswith("/api/"):
                self._request_receipt = require_current(caminho, root=RAIZ)
            if caminho == "/api/neff":
                from bancada.neff_canal import canal
                return self._json(canal())
            if caminho == "/api/neutrino/contrato":
                from bancada.neutrino_contract import contract
                return self._json(contract())
            if caminho == "/api/neutrino/fontes":
                from bancada.neutrino_canal_v2 import canal
                return self._json(canal())
            if caminho == "/api/lago":
                from bancada.lago import cache_gpu_resumo
                return self._json(dict(catalogo=B.lago or dict(estado="catalogando"), residente=B.lago_res.resumo(), cache_gpu=cache_gpu_resumo()))
            if caminho == "/api/lago/colunas":
                q = dict(kv.split("=", 1) for kv in self.path.split("?", 1)[1].split("&")) if "?" in self.path else {}
                from urllib.parse import unquote
                t = B.lago_res.tabela(unquote(q.get("caminho", "")), int(q.get("hdu", "0")))
                return self._json(dict(caminho=t.arquivo, hdu=t.hdu, tipo=t.tipo, linhas=t.n_linhas, colunas=t.colunas()[:400],
                                       cabecalho={k: str(v) for k, v in list(t.cab.items())[:40]}))
            if caminho == "/api/gw":
                try:
                    with urllib.request.urlopen(GW_OFICIAL + "/api/universe/status", timeout=3) as r:
                        oficial = dict(fonte=GW_OFICIAL, estado=json.loads(r.read().decode("utf-8")))
                except Exception as e:
                    oficial = dict(fonte=GW_OFICIAL, fora_do_ar=True, erro=repr(e))
                return self._json(dict(oficial=oficial, residente=B.gw.resumo()))
            if caminho.startswith("/api/gw/"):
                from urllib.parse import unquote
                q = {k: unquote(v) for k, v in (kv.split("=", 1) for kv in self.path.split("?", 1)[1].split("&") if "=" in kv)} if "?" in self.path else {}
                if caminho == "/api/gw/eventos":
                    return self._json(B.gw.lista_eventos({k: v for k, v in q.items() if v != ""}))
                if caminho == "/api/gw/serie":
                    return self._json(B.gw.serie(q["key"], q.get("branqueada", "1") != "0", float(q.get("t0", "-0.5")), float(q.get("dur", "1.0")), int(q.get("n_max", "4000"))))
                if caminho == "/api/gw/espectro":
                    return self._json(B.gw.espectro(q["key"], float(q.get("f_max", "1024"))))
                if caminho == "/api/gw/resultados":
                    return self._json(B.gw.resultados())
                if caminho.startswith("/api/gw/tarefa/"):
                    t = B.gw.tarefas.get(caminho.rsplit("/", 1)[1])
                    return self._json(t if t else dict(erro="tarefa inexistente"), 200 if t else 404)
                return self._json(dict(erro="rota gw desconhecida"), 404)
            if not B.pronta:
                return self._json(dict(erro="motor carregando", detalhe=B.erro), 503)
            if caminho == "/api/dados":
                return self._json(B.dados())
            if caminho == "/api/livro":
                return self._json(B.livro.resumo(40))
            if caminho.startswith("/api/tarefas/"):
                t = B.ev.tarefas.get(caminho.rsplit("/", 1)[1])
                return self._json(t if t else dict(erro="tarefa inexistente"), 200 if t else 404)
            if caminho == "/api/validacao":
                return self._json({f: json.load(open(os.path.join(ESTADO, f), encoding="utf-8")) for f in os.listdir(ESTADO)
                                   if f.startswith("validacao") and f.endswith(".json")})
            return self._json(dict(erro="rota desconhecida"), 404)
        except CanonicalError as e:
            return self._json(dict(ok=False, erro=str(e), code="CANONICAL_REVALIDATION_REQUIRED"), 409)
        except Exception as e:
            return self._json(dict(erro=repr(e)), 500)

    def _post(self):
        self._request_receipt = None
        if not self._host_ok():
            return self._json(dict(erro="Host recusado"), 403)
        try:
            n = int(self.headers.get("Content-Length", "0") or 0)
        except ValueError:
            return self._json(dict(erro="Content-Length inválido"), 400)
        if n < 0 or n > 65536:
            return self._json(dict(erro="corpo grande demais"), 413)
        try:
            self.connection.settimeout(10)
            raw = self.rfile.read(n)
            if len(raw) != n:
                raise ValueError("truncated request")
            corpo = json.loads(raw.decode("utf-8") or "{}", parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
            if not isinstance(corpo, dict):
                raise ValueError("object required")
        except Exception:
            return self._json(dict(erro="JSON inválido"), 400)
        cliente = str(self.headers.get("X-Cliente", "interface"))[:60]
        caminho = self.path.split("?")[0]
        for key in ('curvas', 'c_livre', 'controle', 'series', 'log'):
            if key in corpo and type(corpo[key]) is not bool:
                return self._json(dict(erro=key + ': boolean required'), 422)
        if 'opcoes' in corpo and not isinstance(corpo['opcoes'], dict):
            return self._json(dict(erro='opcoes: object required'), 422)
        if caminho == '/api/maintenance/quiesce':
            with B.activity_lock:
                B.quiescing = True
            return self._json(B.atividades())
        try:
            self._request_receipt = require_current(caminho, root=RAIZ)
        except CanonicalError as exc:
            return self._json(dict(ok=False, erro=str(exc), code="CANONICAL_REVALIDATION_REQUIRED"), 409)
        if caminho == "/api/neutrino/sintetico":
            try:
                from bancada.neutrino_contract import simulate
                return self._json(simulate(corpo))
            except (ValueError, TypeError, KeyError, OverflowError) as exc:
                return self._json(dict(ok=False, erro=str(exc)), 422)
        if caminho == "/api/neff":
            try:
                from bancada.neff_canal import canal, controle_anti_dupla_contagem
                out = canal(sigmas_extra=corpo.get("sigmas_extra", []))
                if corpo.get("controle", False):
                    out["controle_anti_dupla_contagem"] = controle_anti_dupla_contagem()
                return self._json(out)
            except (ValueError, TypeError) as exc:
                return self._json(dict(ok=False, erro=str(exc)), 422)
        if caminho.startswith("/api/gw/"):                       # o banco residente de ondas gravitacionais não depende do motor cosmológico
            try:
                if caminho == "/api/gw/empilhar":
                    return self._json(B.gw.empilhar(corpo.get("sub", "todos"), corpo.get("filtros") or {}, corpo.get("sigma_regra", "max"), corpo.get("versao", "v3")))
                if caminho == "/api/gw/rodar":
                    return self._json(dict(ok=False, code="EXPLICIT_RITE_DISPATCH_REQUIRED", erro="Rodadas historicas exigem despacho pelo executor pinado; esta API nao abre dados."), 409)
                if caminho == "/api/gw/recarregar":
                    B.gw._arq.clear(); B.gw._ler_remanescentes()
                    if corpo.get("series", True): threading.Thread(target=B.gw.carregar, daemon=True).start()   # as séries novas do disco entram sem reiniciar
                    return self._json(dict(ok=True, recarregando_series=bool(corpo.get("series", True)), resumo=B.gw.resumo()))
                return self._json(dict(erro="rota gw desconhecida"), 404)
            except ValueError as e:
                return self._json(dict(erro=str(e)), 400)
            except Exception as e:
                return self._json(dict(erro=repr(e)), 500)
        if not B.pronta:
            return self._json(dict(erro="motor carregando", detalhe=B.erro), 503)
        try:
            if caminho == "/api/lago/carregar":
                threading.Thread(target=B.lago_res.carregar_tudo, daemon=True).start()
                return self._json(dict(ok=True, estado=B.lago_res.estado))
            if caminho in ("/api/lago/histograma", "/api/lago/mapa"):
                from bancada import lago as L
                t = B.lago_res.tabela(corpo["caminho"], int(corpo.get("hdu", 0)))
                dev = str(B.motor.dev)
                with B.motor.lock:
                    if caminho.endswith("histograma"):
                        return self._json(L.histograma(t, corpo["coluna"], int(corpo.get("bins", 120)), corpo.get("faixa"), bool(corpo.get("log", False)), dev))
                    return self._json(L.mapa2d(t, corpo["x"], corpo["y"], tuple(corpo.get("bins", (360, 180))), corpo.get("faixa"), dev))
            op = corpo.get("opcoes", {})
            if caminho == "/api/avaliar":
                return self._json(B.ev.avaliar(corpo.get("theta", {}), corpo.get("conjuntos"), corpo.get("curvas", True), op))
            if caminho == "/api/ajustar":
                return self._json(B.ev.ajustar(corpo.get("conjuntos"), corpo.get("beta", "livre"), corpo.get("c_livre", False), cliente, op))
            if caminho == "/api/comparar":
                return self._json(B.ev.comparar(corpo.get("conjuntos"), corpo.get("c_livre", False), cliente, op))
            if caminho == "/api/amostrar":
                return self._json(B.ev.amostrar(corpo.get("conjuntos"), corpo.get("c_livre", False), corpo.get("walkers", 256), corpo.get("passos", 2000),
                                                corpo.get("queima", 500), corpo.get("semente", 42), cliente, op))
            return self._json(dict(erro="rota desconhecida"), 404)
        except ValueError as e:
            return self._json(dict(erro=str(e)), 400)
        except Exception as e:
            return self._json(dict(erro=repr(e)), 500)


def main():
    global B
    if "--check" in sys.argv:
        try:
            with urllib.request.urlopen("http://127.0.0.1:%d/api/estado" % PORTA, timeout=5) as r:
                e = json.loads(r.read().decode("utf-8"))
            print(json.dumps(dict(no_ar=True, pronta=e.get("pronta"), erro=e.get("erro"), gpu=e.get("gpu"), ram=e.get("ram"), livro=e.get("livro"),
                                  validacoes=e.get("validacoes")), ensure_ascii=False, indent=1))
        except Exception as e:
            print(json.dumps(dict(no_ar=False, erro=repr(e))))
        return
    B = Bancada()
    srv = ThreadingHTTPServer(("127.0.0.1", PORTA), H)
    print("Bancada Um no ar: http://127.0.0.1:%d" % PORTA, flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
