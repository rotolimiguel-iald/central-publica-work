# -*- coding: utf-8 -*-
"""gerar_resultado_r3_5.py (R3.5, 19/10/2026) -- escreve R3_5/RESULTADO_R3_5.md (arquivo NOVO) com todo numero e todo hash LIDOS dos artefatos (nenhum digitado): CONTROLES_NEGATIVOS_R3_5.json, VERIFICACAO_DIFF_R3_5.json,
evidencias/*.json (a fusao do PINOS_BN, a derivacao do passo 10, os dois ensaios a seco), o PINOS_BN fundido (vivo) e o chain re-derivado. SO LE; escreve um arquivo. Recusa (assert) se um numero nao bate.
uso: python -I -B -X utf8 gerar_resultado_r3_5.py"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import re
from pathlib import Path
from string import Template

AQUI = Path(__file__).resolve().parent.parent
R34 = AQUI.parent / "R3_4"
V394 = AQUI.parent.parent / "cadeia_de_selo" / "v394"
POS = V394 / "pos_rito"
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def J(p):
    return json.loads(Path(p).read_bytes())


C = J(AQUI / "CONTROLES_NEGATIVOS_R3_5.json")
V = J(AQUI / "VERIFICACAO_DIFF_R3_5.json")
F = J(AQUI / "evidencias" / "fusao_pinos_bn_r35.json")
D = J(AQUI / "evidencias" / "derivacao_passo10_r35.json")
E1, E2 = J(AQUI / "evidencias" / "ensaio_passo10_standin.json"), J(AQUI / "evidencias" / "ensaio_passo10_real.json")
PB = J(V394 / "PINOS_BN_v394.json")
BA, BF = J(AQUI / "_construcao" / "baseline_antes.json"), J(AQUI / "_construcao" / "baseline_final.json")
R1 = J(AQUI / "_construcao" / "rodada1_CONTROLES_NEGATIVOS_R3_5.json")
esb = AQUI / "sincronizar_bancada.py"
# ---- conferencias
assert C["veredito"] == "TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO" and C["passam"] == C["n"] == len(C["controles"]) and all(x["passa"] is True for x in C["controles"])
assert C["da_R3_4_presentes"] == C["n_da_R3_4"] and not C["da_R3_4_ausentes"] and C["juncoes_restantes"] == [] and C["script_sha256"] == sha(esb)
assert V["reproduz_bit_a_bit"] is True and V["passo10"]["reproduz_bit_a_bit"] is True
assert F["sha256"] == sha(V394 / "PINOS_BN_v394.json") and PB["esboco_R3_5"]["sha256"] == sha(esb) and PB["fusao_r35"]["sha256_do_vivo_antes"] == F["sha256_do_vivo_antes"]
assert D["chain_sha256"] == sha(POS / "chain_pos_rito_v394.sh") and D["helper_sha256"] == sha(POS / "b3_recibo_v394.py")
assert E1["producao_manifesto_igual"] and E1["producao_lista_igual"] and E2["producao_manifesto_igual"] and E2["producao_lista_igual"]
import importlib.util
_spec = importlib.util.spec_from_file_location("esb_r35_ger", esb)
M = importlib.util.module_from_spec(_spec)
sys.modules["esb_r35_ger"] = M
_spec.loader.exec_module(M)
novos = C["novos_R3_5"]
n_m, n_v, n_p = (sum(1 for n in novos if n.startswith(p)) for p in ("R35_M_", "R35_V_", "R35_P_"))
n_ev = sum(1 for n in novos if n.startswith("R35_M_evasao_"))
assert n_m + n_v + n_p == len(novos) == C["n_novos_R3_5"]
mud = C["controles_da_R3_4_que_mudaram_de_formato"]
n_mud_nos = sum(1 for x in mud if any("--nos <stand-in" in m for m in x["motivos"]))
nr = C["nos_real_so_lido"]
nv = {x["controle"]: x for x in C["controles"]}
pin = lambda k: PB[k]
prod_ok = BA["producao"]["lista_sha256"] == BF["producao"]["lista_sha256"] and BA["producao"]["manifesto_sha256"] == BF["producao"]["manifesto_sha256"]
assert prod_ok
ult_json = lambda saida: json.loads([l for l in saida.splitlines() if l.strip().startswith("{")][-1])


def recusa_do(e):
    for l in reversed([l for l in e["saida"].splitlines() if l.strip().startswith("{")]):
        try:
            j = json.loads(l)
        except ValueError:
            continue
        if "recusa" in j or "veredito" in j:
            return j
    return {}


j1, j2 = recusa_do(E1), recusa_do(E2)
parada1 = next((l for l in E1["saida"].splitlines() if l.startswith("PARADA")), "(sem PARADA)")
parada2 = next((l for l in E2["saida"].splitlines() if l.startswith("PARADA")), "(sem PARADA)")
d = dict(
    esb16=sha(esb)[:16], esb_antes16=sha(R34 / "sincronizar_bancada.py")[:16], veredito=C["veredito"], passam=C["passam"], n=C["n"], segundos=int(round(C["segundos"])), ctrl16=sha(AQUI / "CONTROLES_NEGATIVOS_R3_5.json")[:16],
    n_r34=C["n_da_R3_4"], r34_pres=C["da_R3_4_presentes"], n_r33=C["n_da_R3_3"], r33_pres=C["da_R3_3_presentes"], n_novos=len(novos), n_m=n_m, n_ev=n_ev, n_v=n_v, n_p=n_p, n_mud=len(mud), n_mud_nos=n_mud_nos,
    patch16=V["patch"]["sha256"][:16], patch_n=V["patch"]["bytes"], patch10_16=V["passo10"]["patch"]["sha256"][:16], arq_diff=len(V["por_arquivo"]),
    fus16=F["sha256"][:16], fus_full=F["sha256"], fus_antes16=F["sha256_do_vivo_antes"][:16], fus_antes_full=F["sha256_do_vivo_antes"], fus_bytes=F["bytes"], fus_bak=Path(F["backup"]).name, fus_chaves=F["chaves"],
    ch_antes16=D["chain_sha256_antes"][:16], ch_16=D["chain_sha256"][:16], hp_antes16=D["helper_sha256_antes"][:16], hp_16=D["helper_sha256"][:16], ch_bak=Path(D["chain_backup"]).name, hp_bak=Path(D["helper_backup"]).name,
    e1_rc=E1["rc"], e2_rc=E2["rc"], e1_bat=("sim" if E1["bateria_gerada"] else "nao"), e2_bat=("sim" if E2["bateria_gerada"] else "nao"), e1_recusa=(re.search(r'"recusa": "([A-Z_]+)', E1["saida"]) or re.search(r"(PARADA.*)", E1["saida"])).group(1), e2_parada=parada2[:220], e2_causa=(re.search(r"(SELO_DE_OUTRA_VERSAO[^\n]*)", E2["saida"]) or re.search(r"(PARADA.*)", E2["saida"])).group(1)[:160], e1_parada=parada1[:200],
    r1_passam=R1["passam"], r1_n=R1["n"], nos_itens=nr["itens_depois"], nos_um16=sha(NOS / "um.py")[:16], nos_selo16=sha(NOS / "um_absoluto_selo.json")[:16], nos_lista_acr=", ".join(nr["acrescentados"][:6]) or "(nenhum)", nos_n_acr=len(nr["acrescentados"]), nos_rem=len(nr["removidos"]),
    ev_ini=BA["eventos"]["linhas"], ev_fim=BF["eventos"]["linhas"], prod_n=BA["producao"]["n_arquivos"], man16=BA["producao"]["manifesto_sha256"][:16],
    k_esb=pin("esboco_R3_5")["path"], k_esb_sha=pin("esboco_R3_5")["sha256"], k_cad=pin("cadeia_de_selos")["path"], k_cad_sha=pin("cadeia_de_selos")["sha256"], k_rps=pin("recibo_pre_selo")["path"], k_rps_sha=pin("recibo_pre_selo")["sha256"],
    k_selo=pin("selo_anterior_v393")["path"], k_kman=pin("kernel_manifesto_anterior_v393")["path"], k_kr=pin("kernel_recibo")["path"], k_kr_sha=pin("kernel_recibo")["sha256"], k_cri=pin("criterios")["path"], k_cri_sha=pin("criterios")["sha256"],
    k_rps16=pin("recibo_pre_selo")["sha256"][:16], k_kr16=pin("kernel_recibo")["sha256"][:16], k_cad16=pin("cadeia_de_selos")["sha256"][:16], k_cand16=pin("candidato")["sha256"][:16], k_esp16=pin("esperados")["sha256"][:16],
    bat_base_sha=pin("bateria_base_R2")["sha256"][:16], vivo_antes_k=", ".join(F["chaves_do_vivo_mantidas"]),
    r35v_aceito=nv["R35_V_recibo_pre_selo_real_da_R3_4_e_aceito_pela_R3_5"]["script_do_recibo"], r35v_r35=nv["R35_V_recibo_pre_selo_real_da_R3_4_e_aceito_pela_R3_5"]["script_da_r35"],
    n_chaves_b3=len(re.search(r"b3_prepara\(\) \{.*?for k in ([^;]*); do", (POS / "chain_pos_rito_v394.sh").read_text(encoding="utf-8"), re.S).group(1).split()),
    n_pal=len(M.AUD_CORPO_PALAVRAS), n_loc=len(M.AUD_CORPO_LOCAIS), n_glob=len(M.AUD_CORPO_GLOBAIS), n_met=len(M.AUD_CORPO_METODOS), n_nom=len(M.AUD_CORPO_NOMES), n_sin=len(M.AUD_CORPO_PONTUACAO),
    v394s_pass=nv["R35_P_run_bateria_inteira_contra_o_um_py_v394_candidato"]["passa"],
)
TEXTO = Template(r"""VINCULO R3.5 — 19/10

# Resultado da R3.5 do esboço `sincronizar_bancada.py` (F0.6, gerência c1)

Construtor: subagente da gerência c1 (Sonnet). Base: a R3.4 em `../R3_4/` (esboço `$esb_antes16`). Todo hash e todo número abaixo foi lido dos arquivos por `_construcao/gerar_resultado_r3_5.py`; os hashes dos entregáveis estão em `PINOS_R3_5.json`. Esboço R3.5: sha16 `$esb16`.

Pedido (revisão independente `work/cadeia_de_selo/v394_exame/delta/EXAME_DELTA_E_R3_4.md`, parte B; a v394 já está instalada e o rito corre): (1) fechar o filtro dos módulos de auditoria com lista de PERMISSÃO estrita, com controle negativo para cada evasão, re-rodar todos os controles em `C:/t/vb11` e provar que o recibo pre_selo `0d82d598` da R3.4 segue valendo; (2) fundir o `PINOS_BN` vivo com o que é da R3.4/R3.5; (3) re-derivar o passo 10 do pós-rito.

## 1. Veredito

**`$veredito`: $passam/$n em $segundos s**, com `python -I -B -X utf8` no sandbox curto `C:/t/vb11` [REAL, `CONTROLES_NEGATIVOS_R3_5.json`, sha16 `$ctrl16`]:
- os $n_r34 controles da R3.4 presentes $r34_pres/$n_r34 (e, dentro deles, os $n_r33 da R3.3: $r33_pres/$n_r33), com os mesmos nomes; $n_mud mudaram de formato, cada um com o motivo em `controles_da_R3_4_que_mudaram_de_formato` ($n_mud_nos porque ganharam `--nos` do stand-in v393, §3);
- $n_novos controles novos: $n_m `R35_M_` (a lista de permissão; $n_ev evasões), $n_v `R35_V_` (o recibo pre_selo real) e $n_p `R35_P_` (a bateria da v394 contra o candidato real);
- a 1ª rodada deu $r1_passam/$r1_n (JSON em `_construcao/rodada1_CONTROLES_NEGATIVOS_R3_5.json`): um controle herdado (`R32_R31_1_guarda_antes_de_qualquer_import`) pegou uma linha do MEU parágrafo de docstring que começava por `import` (o parágrafo foi reescrito) e um `R35_V_` meu esperava um prefixo só de recusa (a recusa real, `CADEIA_DE_SELOS_NAO_PARTE_DA_BANCADA`, é igualmente legítima: expectativa corrigida). A rodada que vale é a 2ª, com o esboço e os controles finais.

## 2. (1) A lista de permissão estrita [REAL, `DIFF_R3_4_R3_5.patch` sha16 `$patch16`, $arq_diff arquivos, reproduz bit a bit com `core.autocrlf=false`]

- **Defeito (B-M da revisão):** a R3.4 recusava por lista de PROIBIÇÃO, com um lookbehind que excluía o ponto; passavam `Lean.addDecl`, `Lean.modifyEnv` e `Lean.Meta.evalExpr` qualificados, `open IO.FS in` + `writeFile` e `open IO in` + `Process.output`. Reproduzidos, eram aceitos; agora são recusados.
- **Conserto:** `auditar_fonte_de_auditoria` passa a lista de PERMISSÃO. Comandos de topo: `import` só de `Lean`, `TGLExt.*` ou `TGL.*`; `open` só de `Lean`; `#print axioms`; `run_cmd`. No corpo do `run_cmd` (código executado na compilação), cada token tem de estar num vocabulário FECHADO: $n_pal palavras (`let`, `mut`, `for`, `in`, `do`, `if`, `then`, `else`, `unless`, `match`, `with`, `fun`, `some`, `pure`, `_`), $n_loc locais, $n_glob funções globais (`Elab.Command.liftCoreM`, `getEnv`, `collectAxioms`, `throwError`, `IO.println`, `toString`, `String.intercalate`, `Name.toString`), $n_met métodos, $n_nom nomes com crase mais os de `TGLExt`/`TGL`, números, literais de texto (interpolação só de local) e $n_sin sinais. Qualquer outro token é recusado, qualificado ou não, aberto por `open` ou não; `;`, `$$`, comentário na linha, caractere não ASCII fora de texto, local novo e método fora da lista também.
- **Controles novos (`R35_M_`):** as cinco evasões exatas da revisão e as mesmas com o `open` permitido; variantes de qualificação (`_root_`, `IO.FS.writeFile` completo, `IO.Process.spawn`, `System.FilePath`), método do local (`env.addDecl`), campo depois de parênteses, tab, interpolação de termo, `;`, `$$`, comentário na linha, `include_str`, `unsafe`, nome com crase fora da lista, homóglifo cirílico, local novo, número colado, escape e texto sem fechamento; `open` de `Lean.Meta`, de `Lean IO`, de `IO` sem `in`; `import` de `Mathlib` e de `Lean.Elab.Command`; `run_cmd` com comando na mesma linha. Cada um passa por `variante_auditoria` + `verificar_kernel_recibo` (o caminho real do B(n)) e o detalhe nomeia o token. Contraprova: a fixture inalterada passa. O derivador também recusa as evasões. As 3 fontes REAIS (`NetworkProofAuditR3/R7/R8`) passam (R3: 936 `#print axioms`; R7 e R8: um `run_cmd` de 121 tokens cada), inclusive na árvore real do kernel (`C:/t/k394d/arvore`, sha igual ao do recibo).
- **O recibo pre_selo real `$k_rps16` continua valendo (`R35_V_`):** o recibo gerado pela R3.4 antes da instalação (`script_sha256` `$r35v_aceito`, diferente do da R3.5 `$r35v_r35`) é aceito, sem mudar um byte, por `conferir_recibo_pre_selo` da R3.5 contra a Bancada de PRODUÇÃO real (só lida), o selo e o manifesto do kernel da v393 (custódia) e a cadeia: veredito `REPINADA_B4__SALTO_v392_v393__ENSAIO__NADA_GRAVADO_NA_BANCADA`, próxima a selar v394. A conferência não abre arquivo do Nós vivo. Recusas: sem a cadeia, com um byte mudado, contra outra Bancada, com o selo anterior errado.
- **Bateria da v394 contra o candidato real (`R35_P_`):** o `gerar_bateria_r3_4.py --versao v394` sobre um stand-in do Nós v394 (o um.py CANDIDATO d19, `$nos_um16`, o instalado; selo sintético) e a bateria INTEIRA rodada contra uma Bancada pinada nele: 13 PASSA, 0 FALHA, T12/T13/T14 repinados para o v394 (linha de alpha 5584 medida); o T17 só roda no pós-selo.
- **Limite [DECLARADO]:** a lista confere a FORMA; não prova a inocuidade semântica do corpo (`liftCoreM getEnv`, `collectAxioms` e `IO.println` executam na compilação do Lean). Uma forma legítima nova numa versão futura (outro local, outra função) é recusada de forma visível até a lista ser estendida por ato consciente.

## 3. O Nós real no meio do rito: os controles migraram para o stand-in da custódia v393

O Nós real está em obra (um.py `$nos_um16`, o v394, com o selo `$nos_selo16` ainda o da v393; a pasta do Nós teve $nos_itens itens no topo no início e no fim da corrida, com $nos_n_acr acrescentados e $nos_rem removidos). A R3.4 lia o Nós real em ~20 controles (a família b1) e no `montar_sandbox`, o que falharia. Na R3.5 o "Nós real v393" é `nos_real/`, cópia de bytes de `cadeia_de_selo/v394/base_v393` conferida pelos sha256 que o recibo pre_selo real registra; `b1` pina o stand-in; `b1real` pina o caminho REAL (só para a guarda A2, que recusa antes de qualquer conteúdo do Nós importar); `nos_v394s`/`b1v394s` trazem o candidato real. Os $n_mud controles herdados que mudaram de formato (lista e motivos no JSON) mantêm a recusa ou o veredito esperado; mudam só uma asserção lateral em `RUN_1a` (`pina_o_nos_real` agora é falso: o stand-in não está no caminho real) e em dois controles do pino do T12 (o `.path` do pino do um.py também difere), três guardas A2 passam a `b1real`, e três da varredura de auditoria mudam de forma por causa da lista de permissão: o import da amostra, o CRLF/tab e a inversão de `palavras_dentro_de_nome` (um local fora da lista agora é recusado). O Nós real foi SÓ lido (lista e sha do um.py antes e depois); este script nunca grava nele.

## 4. (2) A fusão do `PINOS_BN_v394.json` [REAL, `evidencias/fusao_pinos_bn_r35.json`]

- Parti do arquivo VIVO: sha256 `$fus_antes_full` (a revisão leu `d50e8fd0`), conferido por script antes de escrever. **Fundido: sha256 `$fus_full`** ($fus_bytes B, $fus_chaves chaves). Backup de bytes ao lado: `$fus_bak`. Escrita por temporário + `os.replace`, formato do vivo preservado (CRLF, indent 1).
- Ficam como estavam: $vivo_antes_k (candidato `$k_cand16`, esperados `$k_esp16`). Entram: `esboco_R3_5`, `esboco_R3_4_do_recibo_pre_selo`, `gerador_bateria`, `driver_t12_t14`, `bateria` (a do pre_selo, v393), `bateria_base_R2`, `pino_um_py_da_bateria`, `cadeia_de_selos` (`$k_cad16`), `recibo_pre_selo` (`$k_rps16`, com o pino do pino), `selo_anterior_v393`, `kernel_manifesto_anterior_v393` e `kernel_recibo` = o R3_4 (`$k_kr16`, com `modulos_de_auditoria`). O que saiu de uso fica ao lado em `*_substituido` / `*_original` / `nota_anterior` (esboço R3.3, bateria R2, ensaio da R3.3, recibo do kernel R3_2). NÃO copiei `PINOS_BN_v394.R3_4.json` (candidato `7abb7ba9` e esperados vencidos).

## 5. (3) O passo 10 re-derivado [REAL, `DIFF_PASSO10_R3_5.patch` sha16 `$patch10_16`, reproduz bit a bit]

- Re-derivei, pela §7 do `RESULTADO_R3_4.md` com a R3.5, o `b3_prepara`, o passo 10 e o passo 10b do `v394/pos_rito/chain_pos_rito_v394.sh` e o helper `b3_recibo_v394.py`. Backups de bytes: `$ch_bak` e `$hp_bak`. Chain: `$ch_antes16` -> `$ch_16`; helper: `$hp_antes16` -> `$hp_16`. Passos 0-9, 10a, 10c e 11-14 byte a byte como estavam. NÃO rodei `derivar_cadeia_v394.py`; NÃO toquei `textos_v394.py`, `registrar_mapa_v394.py`, `fechar_v394.py`. `sh -n` OK.
- O que o passo 10 faz agora: lê os pinos fundidos ($n_chaves_b3 chaves conferidas por sha); exige que o um.py do Nós seja o `candidato` pinado; usa o recibo do kernel R3_4 (não mais o R3_2); **gera a bateria da v394 por script** (`gerar_bateria_r3_4.py --versao v394`, depois do selo) e a pina ao lado (`bateria_pos_selo/PINOS_BATERIA_v394.json`; o 10 e o 10b usam a mesma); passa `--cadeia-de-selos` e o recibo pre_selo `$k_rps16`; o helper exige que o recibo DECLARE o salto, com a cadeia pinada, `proxima_a_selar` v394, veredito `__SALTO_` e os pinos da bateria da v394 conferidos.
- **Ensaio a seco (nada gravado na Bancada nem na pasta v394 real; só `--modo ensaio`):** (a) stand-in do Nós v394: o chain gerou a bateria ($e1_bat), passou os pinos e o esboço, contra a produção real, parou como previsto em: `$e1_recusa` (`$e1_parada`); (b) Nós real (no meio do rito): causa `$e2_causa`; `$e2_parada` (bateria gerada: $e2_bat). Manifesto e lista da produção iguais antes e depois nos dois. O que só o rito terminado decide: o selo e o manifesto do kernel reais da v394 (T17) e o `nos_pinado`.

## 6. Comandos exatos do passo 10 (a rodar DEPOIS do rito; `cd "C:/IALD/Central de Patentes/work/cadeia_de_selo/v394/pos_rito"`)

O passo 0 (guardas) roda sempre, qualquer que seja o `CHAIN_DE`: exige `RITO_RC=` no stdout do rito e que o um.py do disco seja o instalado e o candidato. Os passos abaixo são só do B(n); os demais (1 a 9, 11 a 14) seguem a ordem de sempre.

```
# 10 — ensaio pós-selo, SALTO v392 -> v394 (nada gravado na Bancada); gera e pina a bateria da v394 na primeira vez
CHAIN_DE=10 CHAIN_ATE=10 sh chain_pos_rito_v394.sh
# 10-bis-a — a parada do serviço da Bancada (porta 18777) é ATO DO OPERADOR com recibo (bancada_B3_servico/RECIBO_PARADA_v394.json); o chain só confere o recibo
CHAIN_DE=10a CHAIN_ATE=10a sh chain_pos_rito_v394.sh
# 10-bis — APLICAR (grava o manifesto B4 na Bancada de produção; backup de bytes e rollback no esboço); exige o evento c1 que nomeia a v394
B3_AUTORIZADO=sim EVENTO=<seq> EVENTO_HASH=<hash16 do retorno de iald.py anotar> CHAIN_DE=10b CHAIN_ATE=10b sh chain_pos_rito_v394.sh
# 10-ter — o religamento do serviço com recibo é ATO DO OPERADOR (bancada_B3_servico/RECIBO_RELIGAMENTO_v394.json); o chain só confere o recibo
CHAIN_DE=10c CHAIN_ATE=10c sh chain_pos_rito_v394.sh
```
O esboço que o passo 10 chama (valores lidos do `PINOS_BN` fundido; `<bateria...>` é a gerada no 10):
```
python -I -B -X utf8 "$k_esb" --bancada "C:\IALD\Bancada_Um" --producao --nos "$nos_dir" --versao v394 --fase pos_selo --modo ensaio \
  --bateria "<v394/bateria_pos_selo/BATERIA_VINCULO_v394.json>" --bateria-sha256 <sha lido de bateria_pos_selo/PINOS_BATERIA_v394.json> \
  --cadeia-de-selos "$k_cad" --cadeia-de-selos-sha256 $k_cad_sha \
  --recibo-pre-selo "$k_rps" --recibo-pre-selo-sha256 $k_rps_sha --selo-anterior "$k_selo" --kernel-manifesto-anterior "$k_kman" \
  --kernel-recibo "$k_kr" --kernel-recibo-sha256 $k_kr_sha --criterios "$k_cri" --criterios-sha256 $k_cri_sha --saida "<v394/bancada_B3_ensaio_AAAAMMDD_HHMMSS>"
```
O 10b é o mesmo com `--modo aplicar --evento "$$EVENTO" --evento-hash "$$EVENTO_HASH"` e `--saida` numa pasta nova (`bancada_B3`, `bancada_B3_2`...). Resultado esperado do 10: `REPINADA_B4__SALTO_v392_v394__ENSAIO__NADA_GRAVADO_NA_BANCADA`; do 10b: `REPINADA_B4__SALTO_v392_v394__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO`.

## 7. Garantias [REAL]

- Produção ($prod_n arquivos, manifesto `$man16`) e Nós: só lidos; a lista da produção e o manifesto iguais no início e no fim. O livro de eventos só foi lido ($ev_ini linhas no início, $ev_fim no fim; só cresce por outras frentes). Nenhum rito, instalação, conferidor, reversão, `ESPERADOS`, candidato, kernel ou Nós tocado; o serviço da Bancada não foi parado nem religado; o B(n) NÃO foi aplicado; nenhum `.bak_` apagado; processos só os meus.
- Escrevi só em `R3_5`, `C:/t/vb11` (apagado no fim) e, com backup de bytes, em `PINOS_BN_v394.json`, `chain_pos_rito_v394.sh` e `b3_recibo_v394.py` (v394).
- A palavra proibida da régua não aparece como palavra inteira em nenhum arquivo da R3_5 (`grep -r -i -w`, rc 1).

## 8. Resíduos

- Os da R3.4 e R3.3 seguem (a cadeia mostra consistência, não autenticidade; o adendo de pino do T12 espera a ratificação do Codex; o corpo do `run_cmd` não tem inocuidade semântica provada).
- O T17 e o `nos_pinado` do pós-selo só se decidem com o selo e o manifesto reais da v394; o ensaio a seco para antes (§5). Se o rito reconstruir o kernel, derivar de novo o recibo R3_4 (`derivar_recibo_kernel_r3_4.py`) e refazer o pino.
- O `PINOS_BN_v394.json` é vivo (outras sessões o editam): a fusão conferiu o sha antes de escrever e antes do `os.replace`; uma corrida mais curta que isso é residual.

## 9. Atos

**Gerência c1:** reauditar só a lista de permissão (`R35_M_`), os `R35_V_` e os `R35_P_`; conferir o `PINOS_BN` fundido (sha acima) e o chain (diff); depois do rito, rodar o passo 10 (comandos acima); registrar no mapa (`registro_mapa_F0.6_R3_5.json`, pronto e NÃO registrado) e no ACOM.
**Operador:** a parada do serviço (10-bis-a), o evento c1 que nomeia a v394 e a aplicação (10-bis), o religamento (10-ter), X19 e o aceite, como antes.
""")
texto = TEXTO.substitute(d, nos_dir=str(NOS).replace("/", chr(92)))
assert texto.split("\n")[0] == "VINCULO R3.5 — 19/10"
PROIBIDAS = re.compile(r"(?i)\b(" + "|".join(a + b for a, b in (("conf", "irmed"), ("pro", "ved"))) + r")\b")
assert not PROIBIDAS.search(texto)
out = AQUI / "RESULTADO_R3_5.md"
with open(out, "xb") as f:
    f.write(texto.encode("utf-8"))
print(out, len(texto.encode("utf-8")), "bytes")
