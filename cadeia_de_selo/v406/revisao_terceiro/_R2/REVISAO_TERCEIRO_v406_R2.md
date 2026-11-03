# Revisao de terceiro da v406 (R2)

Revisor independente (agente Claude Sonnet; nao construi a v406). Candidato `9bac0146d95d702f`, lido do arquivo ao fechar, 2026-11-02T22:53:51. **Veredito: AINDA NAO APROVADA: um MEDIO, fora do candidato -- 0 ALTO, 1 MEDIO, 3 BAIXO.** A R1 (1 ALTO, 3 MEDIO, 11 BAIXO) esta em `_R1/`.

## 1. A R1: o que foi corrigido (conferido por script, nao pela fala da coordenacao)

- ALTO 1 (joint_contract_open_v394): FECHADO. psibit_v395 volta a `bool(open_joint_contract)` (True no ensaio) e ganha `joint_contract_items_still_open_v406` (3 itens por conteudo: sem «twenty-one»); rede_fock_v394.joint_contract_v406 escolhe o habitado por conteudo (1 item) e os 3 abertos; conferido no diff e no core do ensaio.
- MEDIO 1 (#eval): FECHADO. RESSALVAS_V406[4] com N_EVAL_BLOCOS = 56 e N_EVAL_MODULOS = 15 lidos do BUNDLE (i_eval_diff.py reproduz: 56 blocos, 15 modulos, 44 IO.println + 12 IO.FS, 92 linhas); no contrato (bundle.eval_removidos), no artigo PT e EN («O que entra»), na linha .md e no fechamento_v406.
- MEDIO 2 (frases no presente): FECHADO no artigo PT/EN («As quatro chaves»), na ERRATA_E14, na RESSALVAS_V406[9] e nos limites de fechamento_v406. NO README: ver o MEDIO acima (a ressalva 10 sai cortada).
- MEDIO 3 (hno): FECHADO. E15, LEITURA_V406["um_inscrito"] e a errata do spec dizem «SOB a hipotese nomeada hno»; gamma_vacuum e exponential_zero sem ela (conferi: gamma_vacuum e exponential_zero nao tem hipotese); 8 ocorrencias de `hno` em cunhagens_v406 + fechamento_v406.
- BAIXOS 1 a 11 da R1: FECHADOS (specs comecam pelo estado vigente; .md «tres literais e uma medida»; RESSALVAS[8] do cabecalho, tambem no artigo; `_v406_certificado_habitado` exige all_verified: 2 casos novos, 56/56 ok; modalidade das falas mantida e `atrito` rotulado; E16 reescrita; «compile ...» inteira; o item do 4,44 carrega regra_do_4_44; diz[1] «quanto ao TERMO» e nao_diz com a condicao; 474 modulos + 475 fontes = 474 oleans + o topo, conferido contra o MANIFEST).

## 2. O que ainda trava

- **MEDIO** [pos_rito/textos_v406.py, _paragrafo_v406_de (linha 792: ress = ... x.split(":")[0] ...) e verificar_paragrafo_v406 (linha 839: r_.split(":")[0] ... not in par); sai no README do espelho e no site] O paragrafo pronto do README/site corta cada ressalva no PRIMEIRO dois-pontos. Renderizado sobre o core do ensaio (10 ressalvas): (6) fica «R4/R5 da missao da bancada (identificacao do dispositivo fisico» (perde «seguem bloqueados ... NAO entram nesta versao»); (9) fica com o rotulo UNCOMPILED CANDIDATE e sem «a compilacao que vale e'...»; (10), a ressalva que corrige as frases «o kernel nao habita o certificado», termina «... dizem no presente que o kernel NAO habita o certificado de Fock, leia-se.» sem o que se le; (1) perde «so' na cunha»; (8) perde «os nomes das pedras sao do operador». O verificador usa o MESMO corte, entao nao pega (verificacao: []). Eu nao renderizei esta funcao na R1 e deixei passar a parte que ja existia (R4/R5).
  - **Evidencia:** import de pos_rito/textos_v406.py + `_paragrafo_v406_de(core_ensaio)`; `verificar_paragrafo_v406(par, core, esp)` devolve []. A funcao `_limites` e `_ressalvas` ja usam o texto inteiro; so' o paragrafo do README ficou.
  - **Corrigir:** Linha 792: "; ".join("(%d) %s" % (i + 1, x) for i, x in enumerate(fe["ressalvas"])); linha 839: c_ = _sem_chaves(r_) (texto inteiro). Nao muda o candidato nem o sha16; so' pos_rito/textos_v406.py. Re-renderizar sobre dry_v406/core_ensaio.json e ver as 10 inteiras.

## 3. BAIXOS novos (nao travam)

1. [fechamento_v406.diz[1] e nao_diz[2] (entram no paragrafo do README/site)] «fica para ele ler (regra do posto)» e «a gerencia le essa condicao a ele ao relatar a v406» sao instrucao interna de trabalho dentro de texto publico. **Corrigir:** Dizer no texto publico so' «a condicao ... NAO e' testada aqui (v407)»; a leitura ao operador e' ato da gerencia, fora do README.
2. [delta_v406.py LEITURA_V406["atrito"]] «a RESPOSTA DA GERENCIA, que ele leu e seguiu»: ratificacao dele nao esta nas 23 falas (a fala e36df7f1 usa «Atrito constante», o que nao e' ratificar a resposta). **Corrigir:** Tirar «que ele leu e seguiu» ou citar a fala que ratifica.
3. [delta_v406.py ERRATA_E14 e RESSALVAS_V406[9]] A lista dos lugares desatualizados diz «(estatuto, limites, diz, extras)» mas nao cita o VEREDITO de psibit_v395, que segue com o token CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE ao lado de status INHABITED_BY_physicalFockCertificate_V406. **Corrigir:** Acrescentar «veredito (o token UNINHABITED e' o nome da data)» a E14 e a ressalva 10.

## 4. Ressalvas

- Revisao R2: reli SO' o que a coordenacao disse que mudou, mais o que o conserto podia tocar. Reexecutei: AST dos intocados (iguais), diff das tres funcoes, fail-closed (56 casos, 0 falha; +7 do c2), kernel (301 == sandbox == BUNDLE, raiz e Audit iguais; o kernel nao mudou, logo a compilacao propria da R1 vale), hashes (so' pendente o B(n) pre-selo), gate (qg_closure igual a base), guardas (0), citacoes (operador: exatas), specs (so' as checagens ditas), e RENDERIZEI o paragrafo do README sobre o core do ensaio.
- Nao examinados (como na R1): B(n) pre-selo; instalar/reverter/rito; duracao do rito; as provas dos 301 modulos; a fisica; fechar_v406.py e leitura_v406.py; os textos de rito (handoff, linhagem) alem das funcoes lidas.
- Se o MEDIO for corrigido so' em pos_rito/textos_v406.py, o sha16 do candidato nao muda. Reler so' as linhas 792 e 839 e o paragrafo renderizado basta para a R3.
- Textos revisados (sha16 lidos ao fechar): pos_rito/textos_v406.py ab6b1348f6d4913b; artigo_pt_v406.pysnip a0d40c709cdaa3bd; artigo_en_v406.pysnip 55a783f12c45f833; runtime_v406.py 34ab0ce24765bc2c; delta_v406.py 995f7e50612a9191; registros_v406.py 09e11d145cd6fbef; ESPERADOS_v406.json f5afff5286124295; PINOS_BN_v406.json fd71c638f9febce0. Se algum mudar, a revisao dele nao vale.

## 5. Fecho

`aprovada: False`. O candidato `9bac0146d95d702f` esta limpo nos itens 1 a 6 do pedido; o unico bloqueio e' o corte das ressalvas no paragrafo do README (pos_rito/textos_v406.py, 2 linhas, sem regerar o candidato). Corrigido isso, a R3 e' so' reler essas duas linhas e o paragrafo renderizado.
