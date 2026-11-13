# -*- coding: utf-8 -*-
"""_adapt_pequenos_forkA_v411.py -- (claude-construtor-v411, retomada, fork A, 12/11/2026) adapta DE VERDADE os scripts pequenos da frente do fork A que trazem a marca de copia mecanica: troca a linha da marca por
`# [ADAPTADO v411, ...] <o que mudou>` e faz, em cada um, as trocas de TEXTO e de CODIGO que a v411 (sem modulo novo) pede, cada uma com ancora UNICA (senao PARA). Backup de BYTES antes; respeita o fim de linha; ast.parse / sh -n depois.
uso: python -B -X utf8 _adapt_pequenos_forkA_v411.py"""
import ast, datetime, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
MARCA = "# [A ADAPTAR v" + "411]"
CAB = "# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] "

PLANO = {
    "carimbar_stdout_v411.py": ("conferido: o corpo e' o carimbador do stdout (le bytes, grava identico, carimba por linha), independente de versao e de bundle; so' o rotulo v411 e o nome do arquivo canonico (rodada_v411_stdout.txt)",
                                [("[copia na cadeia v411, 06/11/2026, claude-construtor-v411: o corpo e' o do carimbador da v410 (sha16 do arquivo da v410, lido pelo adaptador: b4ddd87343005850)",
                                  "[copia na cadeia v411, 12/11/2026, claude-construtor-v411: o corpo e' o do carimbador da v410 (sha16 do arquivo da v410, lido pelo adaptador de 12/11: %s; a subida de 06/11 dizia o da v409)" % __import__("hashlib").sha256(open(os.path.join(os.path.dirname(HERE), "v410", "carimbar_stdout_v410.py"), "rb").read()).hexdigest()[:16])]),
    "copiar_logs_do_kernel_v411.py": ("o conferidor idempotente dos logs do kernel da v411 (build incremental SEM modulo novo, nada compilado; o Audit): o registro que o pos_build_kernel_v411.py gravou e' o KERNEL_RECIBO_v411.json (build_full_log e audit_log, sha256) e o POS_BUILD_v411.json (marcas); o LOGS_COPIADOS_v411.json NAO e' escrito na v411 e, se existir, tambem e' conferido; nada e' gravado",
                                      [("`lake build` a frio do modulo novo do bundle (IALD2) e `lake env lean TGL/Audit.lean`", "`lake build` incremental -- a v411 NAO tem modulo novo; nada a compilar -- e `lake env lean TGL/Audit.lean`"),
                                       ("(d) o bytes e o sha256 de cada um dos tres arquivos, recalculados agora, == o que kernel\\\\LOGS_COPIADOS_v411.json registrou (o log nao mudou depois do pos_build).",
                                        "(d) o sha256 do lake_build.log e do audit.log, recalculados agora, == o que kernel\\\\KERNEL_RECIBO_v411.json registrou (build_full_log, audit_log) e as marcas == as do kernel\\\\POS_BUILD_v411.json (o log nao mudou depois do pos_build); "
                                        "(v411) o LOGS_COPIADOS_v411.json nao e' escrito pelo pos_build da v411: se existir, o bytes e o sha256 dos tres arquivos tambem sao conferidos contra ele."),
                                       ('jp = os.path.join(KD, "LOGS_COPIADOS_v411.json")\nif not os.path.exists(jp):\n    chk("kernel\\\\LOGS_COPIADOS_v411.json existe (o pos_build_kernel_v411.py o grava; este script NAO grava)", False, jp)\nelse:',
                                        'kr = json.load(open(os.path.join(KD, "KERNEL_RECIBO_v411.json"), encoding="utf-8")); pb = json.load(open(os.path.join(KD, "POS_BUILD_v411.json"), encoding="utf-8"))   # (v411) o registro que o pos_build_kernel_v411.py gravou\n'
                                        'chk("KERNEL_RECIBO_v411.json[build_full_log] e [audit_log]: sha256 == os recalculados agora (lake_build.log e audit.log)", kr["build_full_log"]["sha256"] == atual["lake_build.log"]["sha256"] and kr["audit_log"]["sha256"] == atual["audit.log"]["sha256"], [kr["build_full_log"]["sha256"][:16], kr["audit_log"]["sha256"][:16]])\n'
                                        'chk("POS_BUILD_v411.json[marcas] == as marcas lidas agora de construir_marcas.txt (os epochs e os rc)", {k_: int(v_) for k_, v_ in pb["marcas"].items() if k_.startswith("epoch_")} == mm and all(pb["marcas"].get(k_) == "0" for k_ in ("rc", "rc_build", "rc_audit")), pb.get("marcas"))\n'
                                        'jp = os.path.join(KD, "LOGS_COPIADOS_v411.json")\nif not os.path.exists(jp):\n    print("     (o LOGS_COPIADOS_v411.json nao existe: o pos_build da v411 nao o escreve; o registro conferido acima e\' o KERNEL_RECIBO e o POS_BUILD)")\nelse:')]),
    "purga_v411.py": ("conferido: so' leitura; conta os padroes da fala de 25/10 e da fala da lista de exclusao na pasta v411 e em C:\\t\\k411c (o corpo nao depende de versao nem de bundle; os padroes vem do delta, por concatenacao); corre por fora (~20 min)", []),
    "pino_memoria_py_v411.py": ("conferido: pina, LENDO do arquivo, o memoria.py da fila (o corpo nao depende de versao nem de bundle); o contrato do pino passa a PINO_MEMORIA_PY_v411 (a subida o deixara no nome da v410); ato da gerencia antes do p00; NAO executado pelo construtor",
                                [('out = {"contrato": "PINO_MEMORIA_PY_v410",', 'out = {"contrato": "PINO_MEMORIA_PY_v411",'), ('print("PINO_MEMORIA_PY_v410:",', 'print("PINO_MEMORIA_PY_v411:",')]),
    "regras_v411.py": ("conferido: regras de permissao da cadeia v411 (RECUSA sem V411_REGRAS_AUTORIZADAS=sim; ato da gerencia; NAO executado); o corpo nao depende de bundle", []),
    "refazer_arvore_v411_pos_selo.py": ("pos-selo: refaz C:/t/k411c/arvore a partir do Nos v411 e confere contra KERNEL_RECIBO_v411.json; a v411 NAO tem modulo novo (R['pedras'] e' VAZIA: so' a raiz, o Audit e as contagens sao conferidos); NAO executado na preparacao",
                                        [("o modulo novo em TGLExt/ (R[\"pedras\"]: path e sha256, um por um, na arvore refeita E no Nos)", "os modulos novos em TGLExt/ (R[\"pedras\"]: path e sha256, um por um, na arvore refeita E no Nos; na v411 a lista e' VAZIA: nenhum modulo novo)"),
                                         ('assert os.path.normpath(R["arvore"]) == os.path.normpath(ARV)\n',
                                          'SANDBOX = r"C:\\t\\k411c\\final"   # (v411) o recibo do kernel da v411 aponta a arvore para o SANDBOX (o pos_build_kernel_v411.py nao refaz a copia so-fontes): ela e\' so\' conferida, NUNCA apagada\n'
                                          '_n_ = lambda p_: os.path.normcase(os.path.normpath(p_))\nassert _n_(R["arvore"]) in (_n_(ARV), _n_(SANDBOX)) and _n_(ARV) != _n_(SANDBOX) and R["pedras"] == [], ("o recibo da v411 (nenhum modulo novo) nao aponta a arvore esperada", R["arvore"])\n'),
                                         ('chk("n_lean", n, R["varredura_tokens"]["arquivos_lean"]); chk("n_o16", no, R["varredura_tokens"]["arquivos_lean_em_TGLExt_O16"]); chk("links", links, [])',
                                          '_vt = R.get("varredura_tokens")\nif _vt:\n    chk("n_lean", n, _vt["arquivos_lean"]); chk("n_o16", no, _vt["arquivos_lean_em_TGLExt_O16"])\n'
                                          'else:   # (v411) o recibo da v411 nao traz varredura_tokens: as contagens sao conferidas contra as FONTES do sandbox medido (sem .lake), so\' lidas\n'
                                          '    nsb = nosb = 0\n    for d, ds, fs in os.walk(SANDBOX):\n        ds[:] = [x for x in ds if x != ".lake"]\n        for f in fs:\n            if f.lower().endswith(".lean") and os.path.relpath(os.path.join(d, f), SANDBOX).replace("\\\\", "/").split("/")[0] in ("TGL", "TGLExt", "TGLExt.lean", "TGL.lean"):\n'
                                          '                nsb += 1; nosb += os.path.relpath(os.path.join(d, f), SANDBOX).replace("\\\\", "/").startswith("TGLExt/O16/")\n    chk("n_lean==sandbox", n - sum(1 for f in os.listdir(ARV) if f.lower().endswith(".lean") and f not in ("TGLExt.lean", "TGL.lean")), nsb); chk("n_o16==sandbox", no, nosb)\n'
                                          'chk("links", links, [])')]),
    "refazer_sandbox_v411_pos_selo.sh": ("pos-selo: chama refazer_arvore_v411_pos_selo.py (NAO executado na preparacao); a v411 nao tem modulo novo (o recibo nao lista pedra)",
                                         [("(raiz, Audit, o modulo novo em TGLExt/ e as contagens de .lean)", "(raiz, Audit, os modulos novos em TGLExt/ -- nenhum na v411 -- e as contagens de .lean)")]),
}


def aplica(rel, motivo, trocas):
    p = os.path.join(HERE, rel); b = open(p, "rb").read(); t = b.decode("utf-8"); crlf = "\r\n" in t
    t = t.replace("\r\n", "\n")
    ls = t.split("\n"); im = [i for i, l in enumerate(ls) if l.startswith(MARCA)]
    assert len(im) == 1, (rel, "marca", len(im))
    ls[im[0]] = CAB + motivo; t = "\n".join(ls)
    for a_, n_ in trocas:
        assert t.count(a_) == 1, (rel, a_[:100], t.count(a_))
        t = t.replace(a_, n_)
    assert MARCA not in t
    if rel.endswith(".py"):
        ast.parse(t)
    nt = t.replace("\n", "\r\n") if crlf else t
    nb = nt.encode("utf-8")
    bk = p + ".bak_" + TS + "_marca"; open(bk, "wb").write(b); assert open(bk, "rb").read() == b
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
    if rel.endswith(".sh"):
        r = subprocess.run(["sh", "-n", p], capture_output=True, text=True); assert r.returncode == 0, (rel, r.stderr)
    print("ADAPTADO", rel, len(b), "->", len(nb))


for rel, (motivo, trocas) in PLANO.items():
    aplica(rel, motivo, trocas)
