# -*- coding: utf-8 -*-
"""gerar_registro_r3_5.py (R3.5, 19/10/2026) -- escreve R3_5/registro_mapa_F0.6_R3_5.json (RESULTADO, rota infra.bancada_um.sincronizacao_vnnn; so os campos de `rotas.py modelo`) com os NUMEROS lidos dos artefatos.
Registro PREPARADO e NAO registrado (ato da gerencia). So le; escreve UM arquivo NOVO. uso: python -I -B -X utf8 gerar_registro_r3_5.py"""
import sys
sys.dont_write_bytecode = True
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
V394 = AQUI.parent.parent / "cadeia_de_selo" / "v394"
C = json.loads((AQUI / "CONTROLES_NEGATIVOS_R3_5.json").read_bytes())
V = json.loads((AQUI / "VERIFICACAO_DIFF_R3_5.json").read_bytes())
F = json.loads((AQUI / "evidencias" / "fusao_pinos_bn_r35.json").read_bytes())
D = json.loads((AQUI / "evidencias" / "derivacao_passo10_r35.json").read_bytes())
E1 = json.loads((AQUI / "evidencias" / "ensaio_passo10_standin.json").read_bytes())
E2 = json.loads((AQUI / "evidencias" / "ensaio_passo10_real.json").read_bytes())
assert C["veredito"] == "TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO" and V["reproduz_bit_a_bit"] is True and V["passo10"]["reproduz_bit_a_bit"] is True
nomes = [c["controle"] for c in C["controles"]]
n_m, n_v, n_p = (sum(1 for n in C["novos_R3_5"] if n.startswith(p)) for p in ("R35_M_", "R35_V_", "R35_P_"))
n_ev = sum(1 for n in C["novos_R3_5"] if n.startswith("R35_M_evasao_"))
base = str(AQUI)
arts = ["sincronizar_bancada.py", "controles_negativos_r3_5.py", "montar_sandbox.py", "CONTROLES_NEGATIVOS_R3_5.json", "DIFF_R3_4_R3_5.patch", "DIFF_PASSO10_R3_5.patch", "VERIFICACAO_DIFF_R3_5.json", "PINOS_R3_5.json",
        "RESULTADO_R3_5.md", "evidencias/fusao_pinos_bn_r35.json", "evidencias/derivacao_passo10_r35.json", "evidencias/ensaio_passo10_standin.json", "evidencias/ensaio_passo10_real.json",
        "_construcao/fundir_pinos_bn_r35.py", "_construcao/derivar_passo10_r35.py", "_construcao/ensaio_passo10_r35.py"]
reg = dict(
    tipo="RESULTADO", rota_id="infra.bancada_um.sincronizacao_vnnn", dominio="INFRA",
    titulo="R3.5 do esboco sincronizar_bancada.py: lista de PERMISSAO estrita dos modulos de auditoria (as evasoes da revisao independente fechadas), PINOS_BN da v394 fundido e passo 10 do pos-rito re-derivado; %d/%d controles com python -I -B -X utf8" % (C["passam"], C["n"]),
    pergunta="A R3.5 fecha o desvio B-M da revisao independente (Lean.addDecl/Lean.modifyEnv qualificados; open IO.FS in + writeFile) sem regredir os 547 controles da R3.4, mantem valido o recibo pre_selo 0d82d598 da R3.4 gerado antes da instalacao da v394, "
             "e deixa o PINOS_BN e o passo 10 do pos-rito prontos para o B(n) em salto v392 a v394?",
    dados=["Bancada de producao (so lida): manifesto B3 %s" % C["producao_intocada"]["manifesto_sha256"][:16],
           "revisao independente work/cadeia_de_selo/v394_exame/delta/EXAME_DELTA_E_R3_4.md (parte B)",
           "recibo pre_selo real da R3.4 (gerado antes da instalacao da v394): REPINADA_B4__SALTO_v392_v393__ENSAIO, bateria PASSA",
           "candidato real d19 (o instalado) como stand-in do Nos v394 com selo sintetico; copia de bytes da custodia v393 como stand-in do Nos v393 (o Nos real esta no meio do rito)",
           "PINOS_BN_v394.json vivo %s fundido em %s (backup de bytes %s)" % (F["sha256_do_vivo_antes"][:16], F["sha256"][:16], Path(F["backup"]).name),
           "chain_pos_rito_v394.sh %s -> %s e b3_recibo_v394.py %s -> %s (backups de bytes)" % (D["chain_sha256_antes"][:16], D["chain_sha256"][:16], D["helper_sha256_antes"][:16], D["helper_sha256"][:16]),
           "sandbox C:/t/vb11 (raiz curta; %d juncoes desfeitas com os.rmdir no link; apagado)" % len(C["juncoes_criadas"])],
    metodo="copia da R3.4 (12d504a1114f9f9c) com patch unico no esboco: auditar_fonte_de_auditoria por LISTA DE PERMISSAO (import so de Lean/TGLExt/TGL, open so de Lean, #print axioms, run_cmd; no corpo do run_cmd, vocabulario fechado de palavras, locais, "
           "funcoes, metodos, nomes, numeros, textos e sinais); controles herdados com os runs refeitos (a familia b1 e os que liam o Nos real migrados para o stand-in da custodia v393), %d novos (R35_M evasoes, R35_V recibo real, R35_P bateria da v394 contra o "
           "candidato real); fundir_pinos_bn_r35.py (backup de bytes, so o que e da R3.4/R3.5); derivar_passo10_r35.py (pela secao 7 do RESULTADO_R3_4.md; bateria da v394 gerada por script depois do selo); ensaio a seco do passo 10 em stand-in e contra o Nos real" % len(C["novos_R3_5"]),
    resultado="%s %d/%d em %s s (R3.4 %d/%d presentes; %d novos: %d M, %d V, %d P; %d herdados mudaram de formato); o recibo pre_selo real e aceito pela conferencia da R3.5; DIFF R3.4->R3.5 e DIFF do passo 10 reproduzem bit a bit; "
              "ensaio a seco do passo 10: stand-in para em NOS_DIFERENTE_DO_PINADO depois de gerar a bateria, Nos real (no meio do rito) para no gerador (selo v393)" % (
                  C["veredito"], C["passam"], C["n"], C["segundos"], C["da_R3_4_presentes"], C["n_da_R3_4"], len(C["novos_R3_5"]), n_m, n_v, n_p, C["n_controles_da_R3_4_que_mudaram_de_formato"]),
    veredito="R3_5_ENTREGUE__AGUARDA_REAUDITORIA_CURTA", estatuto="REAL", status="EM_CURSO", olhou_dados=False,
    defeito="a lista de permissao confere a FORMA, nao a inocuidade semantica do corpo do run_cmd (liftCoreM getEnv, collectAxioms e IO.println executam na compilacao); o T17 e o nos_pinado do pos_selo so se decidem com o selo e o manifesto reais da v394 "
            "(o ensaio a seco para antes); a cadeia prova consistencia de copias, nao autenticidade; o adendo de pino do T12 espera o Codex; residuos da R3.4 e R3.3 seguem",
    nao_refazer="nao refazer a lista de permissao, a fusao do PINOS_BN nem a re-derivacao do passo 10; nao rodar o passo 10 antes do fim do rito; nao copiar PINOS_BN_v394.R3_4.json (candidato e esperados vencidos)",
    proximo_passo="gerencia: reauditar so R35_M/V/P e o diff do passo 10; depois do rito, CHAIN_DE=10 CHAIN_ATE=10 (ensaio do salto v392 a v394, gera e pina a bateria da v394), operador: parada do servico, evento c1 que nomeia a v394, 10b, religamento",
    onde=base, artefatos=[str(AQUI / a) for a in arts], refs=[],
    nota="F0.6 R3.5, construtor Sonnet da gerencia c1, a pedido da gerencia (revisao independente de 19/10). Registro preparado e NAO registrado (ato da gerencia). NOT_FALSIFIED nunca e creditacao; gate NONE.")
p = AQUI / "registro_mapa_F0.6_R3_5.json"
with open(p, "xb") as f:
    f.write(json.dumps(reg, ensure_ascii=False, indent=1).encode("utf-8"))
print(p, len(reg["artefatos"]), len(nomes))
