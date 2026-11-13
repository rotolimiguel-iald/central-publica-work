# -*- coding: utf-8 -*-
"""_fork_b_guardas_v411.py -- (claude-construtor-v411, retomada, fork B, 12/11/2026) adapta guardas_estaticas_bancada_v411.py e varredura_fock_omega_v411.py a v411: os caminhos do artefato, do manifesto e da saida
vem do delta (DL.CANDIDATO_ARQ, DL.MANIFESTO_ARQ, DL.saida; no ensaio do topo proposto, a pasta de ensaio fora de work); o pino do esboco R3.5 e' LIDO do mesmo lugar que o gerador da v411 le (v403\\gerar_candidato_v403.py)
e, se o manifesto o trouxer, conferido contra ele. Nada roda. uso: python -B -X utf8 _fork_b_guardas_v411.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _fork_b_lib_v411 as L  # noqa: E402

G = "guardas_estaticas_bancada_v411.py"
_nh = L.linha(G, "# (nota herdada da v408")
L.aplicar(G, [
    (_nh, "# (nota herdada da v408 [claude-construtor-v408-r2, 04/11/2026], reconferida de versao a versao) o corpo serve SEM mudanca de logica: so' a linha unica de ALPHA_FINE_CODATA_2018 e a de UM_VERSION sao lidas do um.py; "
          "nada depende de bundle (a v411 nao tem modulo novo); rotulos v411, contra-alvo v410."),
    ("LICAO da v410, MANTIDA na v411 (so' o rotulo muda: a v411 e' um BUNDLE de 1 modulo de kernel em TGLExt/ e os UNICOS pontos que estas guardas leem no um.py sao a linha unica de ALPHA_FINE_CODATA_2018 e a de UM_VERSION)",
     "LICAO da v400, MANTIDA na v411 (so' o rotulo muda: a v411 NAO tem modulo novo de kernel e os UNICOS pontos que estas guardas leem no um.py sao a linha unica de ALPHA_FINE_CODATA_2018 e a de UM_VERSION)"),
    ('ESBOCO_SHA256 = json.load(open(os.path.join(HERE, "CANDIDATO_v411.json"), encoding="utf-8"))["guardas_estaticas_da_bancada"]["esboco_sha256"]   # (v411) o pino lido do arquivo, nao digitado; o AC.esboco_da_bancada recusa se o esboco em disco nao tiver este sha256',
     '# (v411) o pino do esboco e\' LIDO do mesmo lugar que o gerar_candidato_v411.py le (o ESBOCO_SHA256 pinado em v403\\gerar_candidato_v403.py), nunca digitado; se o manifesto do artefato o trouxer, tem de ser o mesmo;\n'
     '# o AC.esboco_da_bancada recusa se o esboco em disco nao tiver este sha256\n'
     'ESBOCO_SHA256 = re.search(r\'ESBOCO_SHA256 = "([0-9a-f]{64})"\', open(os.path.join(os.path.dirname(HERE), "v403", "gerar_candidato_v403.py"), encoding="utf-8").read()).group(1)\n'
     '_ge_man = (json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8")).get("guardas_estaticas_da_bancada") or {}) if os.path.exists(DL.MANIFESTO_ARQ) else {}\n'
     'assert _ge_man.get("esboco_sha256", ESBOCO_SHA256) == ESBOCO_SHA256, ("o manifesto do artefato pina outro esboco", _ge_man.get("esboco_sha256"))'),
    ('cand_p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, DL.CANDIDATO)\nsaida_p = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "GUARDAS_ESTATICAS_BANCADA_v411.json")',
     'cand_p = sys.argv[1] if len(sys.argv) > 1 else DL.CANDIDATO_ARQ                       # (v411) o candidato, ou, no ensaio do topo proposto, o artefato de ensaio (fora de work)\nsaida_p = sys.argv[2] if len(sys.argv) > 2 else DL.saida("GUARDAS_ESTATICAS_BANCADA_v411.json")'),
    ('"candidato": {"path": cand_p, "sha16": sha(cand)[:16], "bytes": len(cand)}}', '"candidato": {"path": cand_p, "sha16": sha(cand)[:16], "bytes": len(cand), "rotulo": DL.ROTULO_DO_ARTEFATO}, **DL.MARCA_ENSAIO}'),
    ('json.dump(res, open(saida_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)',
     'open(saida_p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1)); os.replace(saida_p + ".tmp", saida_p)'),
], "o corpo serve (so' as linhas unicas de ALPHA_FINE_CODATA_2018 e UM_VERSION sao lidas); o artefato, o manifesto e a saida vem do delta (no ensaio do topo proposto, a pasta de ensaio); o pino do esboco lido de v403\\gerar_candidato_v403.py, como o gerador o le, e conferido contra o manifesto se ele o trouxer; a saida por .tmp")
