# -*- coding: utf-8 -*-
"""As correcoes da 3a afericao no GERADOR DO CANDIDATO: o pre-registro do candidato instalavel so do lugar permanente (nunca RASCUNHO, TEMP ou scratchpad);
a ratificacao tem de ser da especificacao apresentada ao operador; a leitura do selo do ENSAIO diz DRAFT, nao FROZEN; o terceiro balde nomeado no stdout
(W08c, regra v303); as citacoes dos achados da 2a passada corrigidas (32 e 36). Backup de bytes; ast."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "gerar_candidato_v384.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
bak = P + ".bak_antes_afer3"
if not os.path.exists(bak):
    open(bak, "wb").write(raw)
assert open(bak, "rb").read() == raw
PAIRS = [
    ('''if not ENSAIO:
    assert RAT.get("verbatim") and RAT.get("quando"), "o pre-registro NAO tem a ratificacao do operador gravada: so candidato de ensaio (TGL_CANDIDATO_ENSAIO=1)"''',
     '''PERM = "C:/IALD/Bancada_Um/investigacao/preregistro_pilar_quantico_03out/"
if not ENSAIO:
    assert RAT.get("verbatim") and RAT.get("quando"), "o pre-registro NAO tem a ratificacao do operador gravada: so candidato de ensaio (TGL_CANDIDATO_ENSAIO=1)"
    _pp = PRJ.replace(BS, "/")
    assert _pp.startswith(PERM) and "RASCUNHO" not in _pp.upper() and "/TEMP/" not in _pp.upper() and "SCRATCHPAD" not in _pp.upper(), \\
        "o pre-registro do candidato instalavel tem de morar no lugar permanente (%s), nunca rascunho/TEMP: %s" % (PERM, _pp)   # 3a afericao'''),
    ('''assert SPEC_SHA == PJ["spec_sha256"], "o hash da especificacao nao bate com o gravado no pre-registro"''',
     '''assert SPEC_SHA == PJ["spec_sha256"], "o hash da especificacao nao bate com o gravado no pre-registro"
if not ENSAIO:
    assert RAT.get("spec_sha256_ratificada") == SPEC_SHA == RAT.get("spec_sha256_do_rascunho_apresentado") and RAT.get("a_especificacao_ratificada_e_a_do_rascunho") is True, \\
        "a ratificacao nao e' da especificacao apresentada ao operador"   # 3a afericao'''),
    ('''+ 'L_ANTI_IS_SQRT_BETA_SQRT_K_THE_ROOT_LAW__GAMMA_DISS_FREE_NEVER_CALIBRATED__PREREGISTRATION_V1_FROZEN_BY_HASH_' + SPEC_SHA[:16].upper() + ('_RATIFIED_BY_THE_OPERATOR' if RAT else '_DRY_RUN_CANDIDATE_NOT_RATIFIED') + '__FOLD_HIERARCHY_IS_MATHEMATICS_NOT_A_TEST__\'''',
     '''+ 'L_ANTI_IS_SQRT_BETA_SQRT_K_THE_ROOT_LAW__GAMMA_DISS_FREE_NEVER_CALIBRATED__' + (('PREREGISTRATION_V1_FROZEN_BY_HASH_' + SPEC_SHA[:16].upper() + '_RATIFIED_BY_THE_OPERATOR') if (RAT and not ENSAIO) else ('PREREGISTRATION_V1_DRAFT_SPEC_HASH_' + SPEC_SHA[:16].upper() + '_DRY_RUN_CANDIDATE_NOT_RATIFIED')) + '__FOLD_HIERARCHY_IS_MATHEMATICS_NOT_A_TEST__\''''),
    ('''    + "    # v384 AO LADO (afericao 2, achado 36): o pilar quantico nao concluido''', '''    + "    # v384 AO LADO (afericao 2, achado 32): o pilar quantico nao concluido'''),
    ('''"um_absoluto_pilar_quantico.json"]:   # v384: o resultado do pilar no hash do selo (afericao 2, achado 40)\'''', '''"um_absoluto_pilar_quantico.json"]:   # v384: o resultado do pilar no hash do selo (afericao 2, achado 36)\''''),
    ('''A09 = '                  "tgl_kernel_proof_manifest.json"]:' + CRLF''',
     '''A08c = ('    print("[selo] custodia de sentido: %d modulo(s) all_verified=False -- formais (divida): %s | recusas de dado (ativos): %s"' + CRLF
        + '          % (len(_not_sealed), ", ".join(_formais) or "nenhum", ", ".join(_recusas) or "nenhuma"))' + CRLF)
add("W08c_terceiro_balde_stdout", "G_SELO", A08c,
    '    print("[selo] custodia de sentido: %d modulo(s) all_verified=False -- formais (divida): %s | recusas de dado (ativos): %s | computacao nao concluida: %s"   # v384: o terceiro balde nomeado (regra v303)' + CRLF
    + '          % (len(_not_sealed), ", ".join(_formais) or "nenhum", ", ".join(_recusas) or "nenhuma", ", ".join(_computacao) or "nenhuma"))' + CRLF,
    "stdout: o terceiro balde nomeado na linha da custodia de sentido (regra v303).")
A09 = '                  "tgl_kernel_proof_manifest.json"]:' + CRLF'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8")
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS))
