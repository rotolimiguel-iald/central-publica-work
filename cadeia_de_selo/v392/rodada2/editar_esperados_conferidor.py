# -*- coding: utf-8 -*-
"""editar_esperados_conferidor.py -- (gerencia c1, rodada 2) adapta gerar_esperados_v392.py e conferir_rito_v392.py: 14 pedras, escada [N,N] (achado do agente CHAIN: o conferidor lia
[antes, depois] como [clean, expected]), os registros por spec, a cobertura KH-N1 (a). Backup de bytes antes."""
import os, shutil, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def abrir(nome):
    p = os.path.join(HERE, nome); shutil.copyfile(p, p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_integracao")
    return p, open(p, encoding="utf-8", newline="").read()


def mk(s):
    def rep(old, new, n=1):
        nonlocal s
        assert s.count(old) == n, (old[:80], s.count(old)); s = s.replace(old, new)
    return rep, (lambda: s)


# ---------------- esperados
p, s = abrir("gerar_esperados_v392.py")
rep, get = mk(s)
rep('assert esp["veredito_pedras_do_ensaio"].startswith("TGL_PEDRAS_V392__13_NEW_KERNEL_MODULES__")', 'assert esp["veredito_pedras_do_ensaio"].startswith("TGL_PEDRAS_V392__%d_NEW_KERNEL_MODULES__" % len(CM["pedras"]))')
rep('"veredito_varredura_do_ensaio": ens["mainflow"]["varredura"]["verdict"],', '"veredito_varredura_do_ensaio": ens["mainflow"]["varredura"]["verdict"],\n       "registros_v392": {k: v["verdict"] for k, v in ens["registros_v392"].items()}, "cobertura_kh_n1": ens["cobertura_kh_n1"], "axiom_report_esperado_min": ens["cobertura_kh_n1"]["lidas_pelo_regex"],')
rep('"artigo_marcas": {"pt": [', '"artigo_marcas": {"pt": ["Os registros ao lado do gate (v392).", "PostoAdendo", ')
rep('"en": ["The v392 stones: fourteen new kernel modules and two', '"en": ["The records beside the gate (v392).", "PostoAdendo", "The v392 stones: fourteen new kernel modules and two')
rep('"escada": CM["escada"],', '"escada": [CM["escada"][1], CM["escada"][1]], "escada_v391_e_v392": CM["escada"],')
open(p, "w", encoding="utf-8", newline="").write(get())

# ---------------- conferidor
p, s = abrir("conferir_rito_v392.py")
rep, get = mk(s)
rep('"as 13 pedras no kernel do Nos com os sha do candidato"', '"as %d pedras no kernel do Nos com os sha do candidato" % len(ESP["pedras_sha256"])')
rep('"selo um_version v392; os 2 registros v392 do selo iguais aos do core"', '"selo um_version v392; os 2 registros v392 do selo e o resumo registros_v392 iguais aos do core"')
rep('''and (selo.get("varredura_e_sorry_v392") or {}).get("verdict") == V("varredura_e_sorry_v392") and bool(V("varredura_e_sorry_v392")),''', '''and (selo.get("varredura_e_sorry_v392") or {}).get("verdict") == V("varredura_e_sorry_v392") and bool(V("varredura_e_sorry_v392"))
        and all(((selo.get("registros_v392") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in ESP["registros_v392"]),
    "os %d registros por spec v392 SELARAM e cada veredito == o do ensaio" % len(ESP["registros_v392"]): all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v392"].items()),
    "KH-N1 (a): a cobertura do axiom_report no fecho inteiro passou (decl=%s) e o axiom_report cresceu a >= %s" % (ESP["cobertura_kh_n1"]["decl"], ESP["axiom_report_esperado_min"]): (kf.get("axiom_coverage_v392") or {}).get("ok") is True
        and (kf.get("axiom_coverage_v392") or {}).get("decl") == ESP["cobertura_kh_n1"]["decl"] and len(axr) >= ESP["axiom_report_esperado_min"],''')
rep('E = ESP["escada"]\n', 'E = ESP["escada"]   # [N, N]: depois do rito o core le [clean, expected] = [N, N] (a rodada 2 corrigiu: antes era [antes, depois])\n')
rep('"o axiom_report da v391 segue no trio e so\' cresceu": len(axr) >= ESP["axiom_report_v391_n"] and all(set(v or []) <= TRIO for v in axr.values()),', '"o axiom_report da v391 segue no trio e so\' cresceu": len(axr) >= ESP["axiom_report_v391_n"] and all(set(v or []) <= TRIO for v in axr.values()),\n    "os registros por spec nao deixaram chave nova fora da lista (nada alem de pedras, varredura e registros)": sorted(k for k in core if k not in ESP["vereditos_v391"] and isinstance(core[k], dict) and str(k).endswith("_v392")) == sorted(["pedras_v392", "varredura_e_sorry_v392"] + list(ESP["registros_v392"])),')
open(p, "w", encoding="utf-8", newline="").write(get())
print("ok")
