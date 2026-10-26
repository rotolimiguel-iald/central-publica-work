# -*- coding: utf-8 -*-
"""patch_p00_v401.py -- aplica, por substituicoes de contagem EXATA, a logica da v401 sobre p00_precondicoes_v401.py (origem v399, a cadeia de CONTEUDO, com a licao da v400: as guardas estaticas da Bancada). Recusa rodar duas vezes."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = sys.argv[1] if len(sys.argv) > 1 else "p00_precondicoes_v401.py"
t = open(P, encoding="utf-8").read()
assert "# [v401-patch]" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:110], t.count(old), n)
    t = t.replace(old, new)


sub('Molde: p00_precondicoes_v400.py. uso:', 'Molde: p00_precondicoes_v399.py (a cadeia de CONTEUDO) com a licao da v400. uso:')
sub('import ast, glob, hashlib, json, os, re, shutil, subprocess, sys\n', 'import ast, glob, hashlib, json, os, re, shutil, subprocess, sys\n# [v401-patch]\n')
sub('chk("nenhum registro v401 no core ainda", not any(k.endswith("_v399") for k in core), [k for k in core if k.endswith("_v399")])', 'chk("nenhum registro v401 no core ainda (os da v399 ja estao: a v400 os selou)", not any(k.endswith("_v401") for k in core) and all(k in core for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")), [k for k in core if k.endswith("_v401")])')
# o runtime: o bloco novo da v401 (a funcao do registro da falsidade), nao um runtime MONTADO dos insumos do estudo
i = t.index('RM = json.load(open(os.path.join(HERE, "RUNTIME_MONTAGEM_v401.json"), encoding="utf-8"))\n'); j = t.index('cand = os.path.join(HERE, DL.CANDIDATO); cb = rd(cand)')
t = t[:i] + '''_rt = rd(os.path.join(HERE, "runtime_v401.py")).decode("utf-8")
chk("o runtime novo (runtime_v401.py: o registro falsidade_da_inercia_v401, escrito a mao) e' o que o candidato embute: o sha256 do CANDIDATO_v401.json == o do arquivo; o bloco extraido do candidato (v401_pins.py) o contem; nenhum literal de beta no codigo (C9); a secao do selo ACOM (a da v400) NAO mudou: o hash do bloco embutido e' o que a v400 pinou",
    CM["runtime"]["sha256"] == sha(rd(os.path.join(HERE, "runtime_v401.py"))) and _rt.rstrip("\\n") in rd(os.path.join(HERE, "v401_pins.py")).decode("utf-8") and not AC.literais_de_beta(_rt) and CM["acom"].get("nota") and AC.bloco_das_fontes()[1] == esp4["acom_estudo"]["bloco_embutido_sha256"], [CM["runtime"]["sha256"][:16], CM["runtime"]["bytes"]])
chk("as 6 fontes do operador do ACOM (a origem so' leitura == a copia duravel da cadeia v400 == os pinos do ESPERADOS_v400)", all(sha(rd(o_)) == sha(rd(os.path.join(DL.V400, "insumos", "acom", "fontes_operador", n_))) == esp4["acom_estudo"]["fontes_do_operador"][n_] for n_, o_ in DL.ACOM_FONTES_OPERADOR.items()), len(DL.ACOM_FONTES_OPERADOR))
chk("a pedra FalsidadeDaInercia e' UMA (a lista dos modulos novos tem um elemento); as CINCO inscricoes de 25/10 tem os prefixos de sha256 da ordem (4cf668f8, 344a8ae9, 0516c064, 0b244a5f, 901dd8fc); o adendo de 03-04/09 (erratado ao lado) e' o que a ordem pinou",
    len(json.load(open(os.path.join(HERE, "kernel_modulos_novos_v401.json"), encoding="utf-8"))["novos"]) == 1 and [v_["sha16"][:8] for v_ in DL.verbatins401(os.path.join(HERE, "insumos", "cunhagens"))] == DL.VERBATIM_PREFIXOS_DA_ORDEM_V401
    and sha(rd(DL.ADENDO_ARQ))[:16] == DL.ADENDO_SHA16_DA_ORDEM, DL.VERBATIM_PREFIXOS_DA_ORDEM_V401)
''' + t[j:]
# as guardas estaticas da Bancada (licao da v400), logo depois do ensaio
sub('ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v401.json"), encoding="utf-8"))\n', '''ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v401.json"), encoding="utf-8"))
ESBOCO = os.path.join(WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"); ESBOCO_SHA256 = "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"
gb = lj(os.path.join(HERE, "GUARDAS_ESTATICAS_BANCADA_v401.json"))
chk("[LICAO DA v400] as guardas ESTATICAS do esboco R3.5 da Bancada (a funcao ler_nos do esboco pinado) sobre o CANDIDATO: passa (uma so' linha de alfa e de UM_VERSION); a v399 selada e' recusada com a mensagem EXATA do recibo da Bancada; os 9 controles negativos recusam; o ensaio as rodou",
    gb["veredito"].startswith("GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA") and gb["candidato"]["sha16"] == CM["sha16"] and gb["esboco"]["sha256"] == ESBOCO_SHA256 == sha(rd(ESBOCO)) and gb["v399_selada_o_defeito_real"]["mensagem_identica_a_do_recibo"] is True
    and len(gb["controles_negativos"]) == 9 and all(v["ok"] for v in gb["controles_negativos"].values()) and gb["contagem_direta"] == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0} and ens["guardas_estaticas_bancada"]["veredito"] == gb["veredito"], [gb["candidato_v401"]["alpha"]["n_linhas_nao_indentadas"], gb["contagem_direta"]])
''')
sub('"Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas")))', '"Psibit", "TestemunhaEstatica", "Token", "Sonico", "AfinacaoDasCordas", "Testemunho")))')
sub('chk("as quatro cunhagens de 24/10 (todas falas do operador): arquivo duravel == sha256 == fonte original", len([k for k in MI if k.startswith("cunhagens/")]) == 4', 'chk("as cinco cunhagens de 25/10 (todas falas do operador): arquivo duravel == sha256 == fonte original", len([k for k in MI if k.startswith("cunhagens/")]) == 5')
sub('o resultado == o sha256 da ordem da v397; as QUATRO inscricoes de 24/10 desta versao tem os prefixos de sha256 que a ordem da gerencia deu (todas falas do operador)",', 'o resultado == o sha256 da ordem da v397; as CINCO inscricoes de 25/10 desta versao tem os prefixos de sha256 que a ordem da gerencia deu (todas falas do operador)",')
sub('len(DL.verbatins(os.path.join(HERE, "insumos", "cunhagens"))) == 4, [sha(rd(p_))[:16] for _, p_ in F9])', 'len(DL.verbatins401(os.path.join(HERE, "insumos", "cunhagens"))) == 5, [sha(rd(p_))[:16] for _, p_ in F9])')
sub('for k_ in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399",', 'for k_ in ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399",')
sub('and exm["ponto_veracidade"]["all_verified"] is True and exm["ponto_veracidade"]["depois_do_psibit_e_da_testemunha"] is True', 'and exm["ponto_falsidade"]["all_verified"] is True and exm["ponto_falsidade"]["logo_depois_da_declaracao_v399"] is True and exm["ponto_falsidade"]["costless_ok"] is True and exm["ponto_veracidade"]["all_verified"] is True and exm["ponto_veracidade"]["depois_do_psibit_e_da_testemunha"] is True')
sub('o da declaracao_do_operador_v399 logo depois do selo e o do teste_de_veracidade_fase9_v397', 'o da declaracao_do_operador_v399 logo depois do selo, o da falsidade_da_inercia_v401 logo depois da declaracao e o do teste_de_veracidade_fase9_v397')
# scripts: a lista vem da pasta (todos os .py da cadeia), nao de uma lista digitada
i = t.index('for f in ("delta_v401.py", "preparar_kernel_v401.py"'); j = t.index('    try:\n        ast.parse(open(os.path.join(HERE, f), encoding="utf-8").read()); s_ = True')
t = t[:i] + '''_pys = sorted(f for f in os.listdir(HERE) if f.endswith(".py") and ".bak" not in f)
for f in _pys:
''' + t[j:]
sub('for f in ("rito_v401.sh", "refazer_sandbox_v401.sh", "refazer_sandbox_v401_pos_selo.sh", "construir_kernel_v401.sh", "refazer_candidato_v401.sh", os.path.join("pos_rito", "chain_pos_rito_v401.sh")):', 'for f in ("rito_v401.sh", "construir_kernel_v401.sh", "copiar_k401c.sh", "refazer_candidato_v401.sh", "refazer_sandbox_v401_pos_selo.sh", os.path.join("pos_rito", "chain_pos_rito_v401.sh")):')
sub('chk("a derivacao do rito/instalar/reverter: zero falha nos invariantes e a sintaxe de todos"', 'chk("a conferencia do instalar/reverter/rito: zero falha nos invariantes (a lista de modulos novos LIDA tem UM elemento e e a dos ESPERADOS; o sidecar entra nos backups; o recibo pre_selo e\' o da v401; a Bancada que JA pina a v400) e a sintaxe de todos"')
ast.parse(t)
open(P + ".tmp", "w", encoding="utf-8", newline="").write(t); os.replace(P + ".tmp", P)
print("patch aplicado:", P)
