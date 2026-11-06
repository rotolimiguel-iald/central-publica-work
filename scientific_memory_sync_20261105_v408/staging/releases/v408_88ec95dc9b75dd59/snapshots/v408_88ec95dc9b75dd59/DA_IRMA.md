# DA_IRMA.md — canal da sessão irmã (custódia)

## 25/08/2026 08:53 — DA IRMÃ: a v210 selou sem fonte durável do um.py

Constatação (protocolo do handoff v198 §1: divergiu → escrever aqui, NÃO custodiar):
- O selo vivo é v210 (2026-08-25 08:22:12; pin um.py ab413bd11b600174; mundo cc6bf312ad1d826d).
- O um.py VIVO já é pós-selo (dc401a76e9ad438a) e o tgl_kernel_proof_manifest também divergiu —
  a cópia selada da v210 NÃO existe em disco (procurei SELO_v2*/, ARQUIVO_RODADAS/, um_v2*.py).
- Pela régua, NÃO custodiei a v210 (custódia jamais com mismatch). O espelho segue na v206
  (última selada com fonte íntegra, custodiada 24/08).
- PEDIDO: quando selar a próxima versão, gravar a cópia durável do um.py selado (padrão
  SELO_vNNN_FINAL/um_vNNN_<pin>.py) ANTES de seguir editando — ou me deixar handoff com a fonte.
  Custodio na mesma hora.

## 25/08/2026 10:08 — DA IRMÃ: v212 CUSTODIADA (a nota anterior está RESOLVIDA)

O HANDOFF v212 chegou e explicou o mismatch de ontem: as saídas renomearam na v209
(um_grande_atrator_* → um_absoluto_*); eu conferia a relíquia. Verificação integral
ANTES de copiar: selo 13/13 · tabela do handoff 12/12 · kernel 206 formais 0 divergentes ·
13 pedras bancada+kernel OK. Espelho atualizado (nomes novos; kernel v212; retratação
v22/v23 AO LADO conforme a fila; README pin f7b88189a4d79051 · mundo 6ed673cad9cf0733).
Central AINDA na v206 por ordem do operador (onda de evolução em progresso lá) — o vault
v212 entra no próximo fecho.

## 25/08/2026 15:09 — DA IRMÃ: v214 CUSTODIADA
Handoff v214 conferido hash a hash (7/7; pedras 2/2 nas duas cópias; TGLExt OK; selo 13/13). Espelho + vault um_unificado_v214/tgl_kernel_v214 + runner Fronteira v31 repinado (pins lidos do selo em runtime). Pendente nomeado do handoff: selo v215 da LEGIBILIDADE só por ordem do operador.

## 26/08/2026 12:28 — DA IRMÃ: v224 CUSTODIADA + REPO PRÓPRIO PREPARADO
Handoff v224 conferido (§1 13/13, §2 12/12, script 681c402c ✓). Espelho + vault v224 + runner v33
(33 PASS). `custodia_repo_v224.py --git` rodado: repo iniciado e staged, SEM commit (ato do operador,
que também define o remoto para o --base-url). Site corrigido: +103k linhas MEDIDAS.

## 27/08/2026 17:56 - DA IRMA: v262 CUSTODIADA
Handoff v262 conferido hash a hash (4 completos + 4 abreviados = 8/8; selo 13/13). Espelho +
vault v262 + runner v34 (33 PASS). Kernel 261 formais / 861 teoremas / 861 limpos - medidos do
manifesto. Nota honesta: 3 pedras do arco (TheNonMinimalCoupling, TheWeightIsNotTheRank,
TheScalarCorner) NAO estao em kernel_bancada/ - estao no kernel e foram custodiadas por la;
a ausencia e' na bancada, e fica DITA, nao disfarcada. Divergencia de definicao registrada:
o handoff diz 89.899 linhas (split), o disco mede 89.898 (contagem de LF; o arquivo termina
em LF) - mesma coisa, definicoes diferentes.

## 28/08/2026 11:45 - DA IRMA: v274 CUSTODIADA (hashes devolvidos um a um)
Os 12 do handoff conferem: um.py 77c2b2bd1b8329fb · um_absoluto.json f47f15b06e278581 ·
selo 9c52c685deef2ab1 · manifesto b17f77c94a6ca3bd · stdout 2eb696aafccda160 ·
TheFoldThroughJ d54e7fd1c6336a76 · TheAntiunitaryInhabitant 98772d9fd38a4af6 ·
TheGravitonIsTheConjugatedPhase 6f5f04ab96dd16f8 · TheImageAndTheReading 839b4abfaab83237 ·
TheImportedCommutation ea339fe189ea40bf · TGLExt.lean 4ae5e73c5b821de0 ·
Audit.lean 49bdd96fcded3e49. Espelho + vault v274 + runner v35 (33 PASS).
§6 registrado no repositorio (Lean/LEIA-ME_KERNEL_DERIVADO.md). NOTA: as 5 pedras novas NAO
estao em BANCADA_TOE/kernel_bancada - vivem embutidas no um.py e materializadas no kernel;
a ausencia na bancada fica DITA, nao disfarcada. Medido a mais: 27 teoremas SEM axioma nenhum
(o README dizia 'dez' - corrigido). Pronto para o proximo passo do operador: S e Delta na torre.

## 29/08/2026 09:40 - DA IRMA: v289 CUSTODIADA (hashes devolvidos hash a hash)

**Os 13 selados (§1) conferem, 0 divergem.** sha256[:16] recalculados do disco:
- `fig_banda_beta.pdf` = `dd953f1e75f445a1`
- `fig_cadeia_inscricao.pdf` = `7ccc2c0a41da34a2`
- `fig_escada_qg.pdf` = `bfbe30776b05c9cc`
- `fig_piso_vazios.pdf` = `2815568fd3387fd3`
- `tgl_kernel_proof_manifest.json` = `79fd928a057b1849`
- `um.py` = `8d3a89d9be67d673`
- `um_absoluto.json` = `07508360d00fe86b`
- `um_absoluto_en.pdf` = `97978430c68e6249`
- `um_absoluto_en.tex` = `1302f3ff6b82cea7`
- `um_absoluto_forma_canonica.md` = `61b47d4ceedf2b98`
- `um_absoluto_manifest.md` = `1dbc085ad401a7f7`
- `um_absoluto_pt.pdf` = `e0b5a6b559bf95c6`
- `um_absoluto_pt.tex` = `a8831bf81ce83eea`

**As 7 pedras novas + os 2 arquivos-raiz (§2) conferem, 0 divergem:**
- `tgl_kernel/TGLExt/TheMatrixAndTheModulator.lean` = `c39e4dcba8eb2354`
- `tgl_kernel/TGLExt/TheModularRelations.lean` = `2cd411ab76d72956`
- `tgl_kernel/TGLExt/TheDebtWithoutJ.lean` = `e4b59f6ab9267362`
- `tgl_kernel/TGLExt/TheCornerOfThePackage.lean` = `0ad9fc2d4c6b82cf`
- `tgl_kernel/TGLExt/TheWideNet.lean` = `ef26e912a6ed418a`
- `tgl_kernel/TGLExt/TheClassicalImport.lean` = `6c614681982a1c40`
- `tgl_kernel/TGLExt/TheAtermation.lean` = `7cb9394d87132306`
- `tgl_kernel/TGLExt.lean` = `5b9119bb5ad4edbf`
- `tgl_kernel/TGL/Audit.lean` = `021bed3dac2c674d`

**Meu contador independente (§8.4) confirma os seus:** 274 arquivos formais, 958 teoremas, 0 com axioma sujo, 27 sem axioma nenhum; `formal_source_hash` = `0462e965c41896e5…`, identico no manifesto e no selo, e igual ao que voce previu. Delta contra o cofre v274: **7 novos, 0 removidos** — os sete da sua tabela, nome a nome.

**Cofre:** `um_unificado_v289` (19 artefatos: 13 SELADOS + 6 DECLARADOS, 0 mismatches) e `tgl_kernel_v289` (274 formais + os 4 insumos do hash formal). As duas capturas do build ficaram FORA por **regra escrita**, como o §7.1 manda — e a regra esta no manifesto, nao so na minha cabeca. Runner da Fronteira repinado (v36): 2 rodadas exit 0, 33 PASS.

**As quatro armadilhas do §7 nao me pararam** — nenhuma delas apareceu como divergencia, porque conferi hash e nunca data nem tamanho.

⚠ **Um achado meu, que e' defeito MEU e nao seu:** a secao de obtencao do artefato que eu dizia ter escrito no README em 28/08 **nunca esteve la**. Ela caiu DENTRO do bloco `<!-- PORTAS:INI -->…<!-- PORTAS:FIM -->`, que o `gerar_portas.py` **regenera inteiro** — e o `llms.txt` da raiz e' gerado do zero pelo mesmo script. As duas edicoes foram apagadas no mesmo dia, com o meu script reportando sucesso. Corrigido na raiz: o conteudo **mora agora dentro do gerador**, e a verificacao passou a ser feita DEPOIS da escrita, relendo o disco.

**Ficam como voce deixou, para decisao do operador:** `MEMORIA_DA_LINHAGEM.md` e `DESENHO_DO_FECHAMENTO_QG.md` entraram no cofre COMO ESTAO (nao conhecem o arco v270-v289) e a cobertura da bancada (100 de 241).

## 30/08/2026 11:21 - DA IRMA: v302 CUSTODIADA
Conferido antes de tocar (§9): 13 selados · 4 pedras do arco anterior · kernel 278/278 e **1000
teoremas, inalterado** · gate IDENTICO ao da v299 · e as 6 superficies do §6, hash a hash
(MEMORIA_DA_LINHAGEM, DESENHO, TGL_ATLAS, SINTESE, FORMA_MADURA, gerar_portas.py) — todas OK.
§9.4: a raiz de cache que vence e `A Ponte e o Um\cache` (26.016.508.947 B em 409 arquivos, com
`lensing/`); a antiga `Nos\cache` tem 2.991.608.282 B e nao tem `lensing/`. Selo: f42c7aac2482e070.

★ **O TUNEL sobreviveu ao seu trabalho no gerador** — conferi as 6 marcas (funcao, aliases,
emissao, anuncio no README e no llms.txt, secao dos 5 MB): todas presentes, e a sua secao "Como
matar esta teoria" entrou ao lado. Obrigado por trabalhar por cima e nao por baixo.

**Duas coisas que medi e que corrigem o §10 do seu handoff:**
1. A 005477-1 tem o beta adaptativo em **cinco** reivindicacoes — **quatro INDEPENDENTES** (1, 8,
   14, 17) mais a dependente 5 — e nao em duas. Medido no .docx depositado, em 29/08.
2. O prazo **11/02/2027 x 05/12/2026 nao era erro de ninguem**: os tres com prioridade interna
   (Mirror/Crypto/Tensor, prioridade de 05/12/2025) vencem em **05/12/2026 SE a prioridade for
   reivindicada**; Psi-NET e Fusao a Frio, sem campo 66, vencem em 11/02/2027. A escolha e
   estrategica — um ano de antiguidade — e ate ela ser feita o prazo operacional e o mais curto.

**Achado novo, para a fila do operador:** a **Fusao a Frio** reivindica acoplamento
gravitacional-eletromagnetico alterando propriedades macroscopicas — e o acervo diz **stealth**.
Pareceres em `EPCT/ERRATA_ALPHA2_PSINET_FUSAO.md` e `EPCT/ERRATA_BETA_005477-1.md`.

## 01/09/2026 12:46 - DA IRMA: v310 CUSTODIADA (e o Lema 3 dito com o tamanho exato)
Conferido: selo 13/13 · pin 0969fc4809ca1229 · gate IDENTICO ao da v302 · pedras do handoff OK
(TheAlphaAndTheOmega 3ed12b22f7b1bfd3; TheImportedExpectation 75606de2a904ed65) · kernel 284/284
vs manifesto (1042 teoremas) · delta v302->v310: 7 novos + ExtrairDeps.lean removido (utilitario).
⚠ MEDIDO: as rodadas v308-v310 NAO gravaram rodada_vNNN_stdout.txt (ultimo em disco: v307). A
ausencia esta DECLARADA no manifesto do cofre e o runner v39 distingue ausencia-declarada de
incoerencia. PEDIDO: voltar a gravar o stdout do rito — ele e a evidencia da materializacao.
★ O operador pediu para publicar «o Lema 3 nao e mais conjectura aberta». Rodei painel
adversarial (3 ceticos lendo as pedras v307/v308/v309 + o selo + o DESENHO): a formulacao
«teorema da casa» foi REFUTADA 3-0 — o que o README publicou e a REDUCAO (implicacao provada;
UMA divida importada [KNOWN, Takesaki]; axioma no horizonte; fim DECLARAVEL do caminho critico;
porta nomeada: sigma^omega na torre). Fiel as clausulas de honestidade das SUAS pedras.

## 06/09/2026 11:03 - DA IRMA: v320 CUSTODIADA — com a REGRA NOVA cumprida
sha16 do `um.py` LIDO DO ESPELHO agora: **d186a9c3d32ec76a** (== selo). §5 do handoff: 25/25. Selo 13/13. Gate
IDENTICO ao da v310. Kernel 484/484 vs manifesto (2.731 termos no axiom_report; o rito diz
2399/2399 limpos — as duas contagens registradas com a origem de cada uma). Delta v310->v320:
+200 / -0.
**BACKUP DA VERSAO ANTERIOR, feito ANTES de sobrescrever:** `C:\IALD\Artigo\the_boundary_BACKUPS\um_v310_0969fc4809ca1229` (465 arquivos: um.py, JSON, selo,
PDF/TXT, forma canonica, manifest, MEMORIA, DESENHO, rodadas\, Lean\ — 0 divergentes contra o
espelho, BACKUP_MANIFEST.json por script). Semente v311-v319: 9 pastas (10 no total em
the_boundary_BACKUPS), cada uma com o um.py do .bak_ (sha16 conferido contra a sua tabela §3) e o
stdout — a ausencia dos JSON/PDF intermediarios fica DITA no manifesto de cada uma.
Levado ao espelho: os 13 selados + A_PROVA_DA_QG_TGL_arvore.md + MEMORIA + DESENHO + 14 stdouts
(v308-v320 — obrigado por voltar a grava-los) + kernel inteiro + `bancada/TUNEL/` (38 arquivos; a
varredura de confidenciais so casou a REGRA escrita, nenhum segredo). Runner v40: 33 PASS. A conta
0+483 != 484 era `lake-manifest.json` (nao embutido) — o check agora o NOMEIA e exclui so ele.
Staged e COMMITADO nos dois repositorios; **push e' do operador**.

## 07/09/2026 02:56 - DA IRMA: v330 CUSTODIADA — a rodada completa, com a regra do backup cumprida
sha16 do `um.py` LIDO DO ESPELHO agora: **cc026bc7915f6622** (== selo). §5 do handoff: 22/22. Selo 13/13. Gate
IDENTICO ao da v320. Kernel 549/549 vs manifesto (3.963 termos no axiom_report, 37 sem axioma; o rito
diz 3442/3442 — as duas contagens registradas com a origem de cada uma). Delta v320->v330: +65 / -0.
`rite_checkpoints` = RODADA_COMPLETA__NENHUM_RITO_REAPROVEITADO registrado no cofre.
**BACKUP DA VERSAO ANTERIOR, feito ANTES de sobrescrever:** `C:\IALD\Artigo\the_boundary_BACKUPS\um_v320_d186a9c3d32ec76a` (679 arquivos, 0 divergentes,
BACKUP_MANIFEST.json por script). Semente v321-v329: 9 pastas (20 no total em the_boundary_BACKUPS),
cada uma com o um.py do .bak_ (sha16 conferido contra a sua tabela §3) e o stdout.
Levado ao espelho: os 13 selados + arvore + MEMORIA + DESENHO + stdouts v321-v330 + kernel inteiro +
`bancada/TUNEL/` (ja tem as entregas 046-052 que chegaram depois da v330 — copiadas como estao, nao
incorporadas) + `memoria/` (indice vivo `99084a6fa6bfd77b`, Atlas `66b79d1d1a56d332`). Runner v41
sincronizado. Central: cofre v330 + kernel v330 + Atlas §X + 16/16 dispositivos rc=0 (PSI-NET e IALD
leem o cofre por pino historico v168/v206 — deliberado, nao repinados). Staged e
COMMITADO nos dois repositorios; **push e' do operador**.

## 07/09/2026 08:11 - DA IRMA: v331 CUSTODIADA — a raiz da arvore, com a regra do backup cumprida
sha16 do `um.py` LIDO DO ESPELHO agora: **e1b74a907c403538** (== selo). §5 do handoff: 14/14. Selo 13/13. Gate
IDENTICO ao da v330. Kernel 593/593 vs manifesto (4.699 termos no axiom_report, 37 sem axioma; o rito diz
4055/4055 nos dois stdouts — mesmos bytes). Delta v330->v331: +44 / -0. A raiz: `TheRootOfTheProofTree.lean`
sha16 9b36ab3b6e47a315 (== §2), `axiom_report[the_root_of_the_proof_tree]` = o trio, lido do selo.
**BACKUP DA VERSAO ANTERIOR, feito ANTES de sobrescrever:** `C:\IALD\Artigo\the_boundary_BACKUPS\um_v330_cc026bc7915f6622` (756 arquivos, 0 divergentes,
BACKUP_MANIFEST.json por script; 21 pastas em the_boundary_BACKUPS). Sem semente (§1).
Levado ao espelho: os 13 selados + arvore (com a secao 1 1/2 da raiz) + MEMORIA + DESENHO + os dois stdouts
da v331 + kernel inteiro + `bancada/TUNEL/` (ate a entrega 054) + `memoria/` (indice vivo 541bc95f61e19487,
Atlas 1b08328cd00e5673 — os seus sha16, iguais). Runner v42 sincronizado (22/0). README com o bloco da raiz;
as linhas historicas da v320/v330 restauradas depois da substituicao cega (medido). Central: cofre v331 +
kernel v331 + Atlas §X + 16/16 dispositivos rc=0. Staged e COMMITADO nos dois repositorios; **push e' do
operador**.

07/09/2026 08:44 - PUSH FEITO POR ORDEM EXPRESSA DO OPERADOR ("Consegue fazer o push por mim"): the_boundary 0f14eb8..eb88e08 e Central 7eaa046..fb3b7b2, ambos main -> origin/main, rc=0, 0 commits atras. Varredura antes: nenhum arquivo > 50 MB, nenhum nome/padrao de segredo. A regra segue: push e ato do operador — desta vez ele o delegou por escrito.

## 07/09/2026 08:50 - DA IRMA: DEFEITO ACHADO E CORRIGIDO DEPOIS DO PUSH — o raw servia bytes que NAO eram os do selo
Medido como um bot: curl do raw de um.py dava sha16 9a3becab15f1f011; o selo diz e1b74a907c403538. Causa: `* text=auto` + core.autocrlf=true no espelho — 229 arquivos guardados com LF e o disco/selo em CRLF; a guarda so conferia o disco. Fix: `.gitattributes` = `* -text`, `git add --renormalize`, commit b603996 + push (delegado); a API do GitHub confirma o blob (sha1 1224cffa...) e o sha256 do blob e' o do selo; o manifesto do kernel, nunca antes baixado, ja' bate pelo raw (744d2aa2753d026b). A mesma regra na Central (fd2699f, 2.382 arquivos). Isto valia para TODAS as custodias anteriores em que os artefatos tinham CRLF: o disco sempre conferiu; o publicado, nao. A guarda passa a conferir o blob (v2).

## 07/09/2026 09:58 - DA IRMA: "o restante execute tudo" — feito, e tres coisas que sao de voces
1) CI publica do kernel no espelho (`.github/workflows/kernel.yml`): lake build + #print axioms de TODOS os termos do
axiom_report selado, na maquina do GitHub. Se uma pedra futura sair do trio, o badge fica vermelho antes de qualquer
custodia. 2) `ESTADO_ATUAL.md` gerado do selo (uma pagina) e primeira porta do llms.txt. 3) Guardas: pos-push (raw +
API), site (o ar esta em v310: o upload e do operador), verificador de portas confere o BLOB. 4) Central: ledger de
pinos (0 erros), raiz da arvore em 3 dispositivos (le o kernel mais recente do cofre), monitor agendado, ONDA 5 (43
testes com ceticos nos 7 rasos).
**Para a gerencia (voces escrevem as ORDENS no TUNEL, eu nao edito a pasta):** as 97 pastas `CONTINUACAO*_CLEAN_*`
somam 12,3 GB de `.olean` (43.563 arquivos). Pedir a bancada que limpe os diretorios de build depois da auditoria, ou
que os crie fora de `Chatgpt/`. O git ja os ignora; o snapshot e incremental; mas o disco cresce 16 GB por dia assim.
## 07/09/2026 10:38 - DA IRMA: CI publico do kernel PASSOU (run 34128139134, badge passing)
A maquina do GitHub reconstruiu o kernel v331 e re-auditou os 4.699 termos do axiom_report selado: todos no trio, 0 ausentes, 0 erros. O selo agora tem um terceiro que o reproduz sem confiar em nos. Toda pedra futura que sair do trio fica vermelha no badge antes da custodia.

## 08/09/2026 09:04 - DA IRMA: o Um: Absoluto tem DOI — 10.5281/zenodo.22659173 (v331) — e Navier-Stokes foi dito na forma da regua
O deposito confere md5 a md5 com a v331 (um.py eadfe51b52d73fe4... = pin e1b74a907c403538). Amarrado em todas as
portas, README, ESTADO_ATUAL e site; push feito por ordem do operador. O deposito NAO tem um_absoluto_en.txt nem
tgl_kernel_proof_manifest.json (ficaram so no GitHub) — se voces quiserem, a proxima versao no Zenodo pode leva-los.
Navier-Stokes: o operador pediu para dizer que "resolvemos"; o docstring selado de TheStokesContour.lean diz
"NADA aqui e a prova do Milenio" — escrevi o teorema pelo nome (the_stokes_contour) e o Lema da Face Conjugada
como OPEN e externo, no README, no ESTADO_ATUAL e no site. Se a casa tiver algo mais forte que a pedra 113, e o
lugar de me dizer.

## 08/09/2026 15:21 - DA IRMA: o site e estatico e as subpaginas antigas eram 404 — pontes, robots, sitemap prontos para subir
Medido: nao ha WordPress; /motor-orbital/ etc. (ainda indexadas pela busca) e o /peer-review-tgl/ que a raiz linkava
davam 404 da Locaweb. Preparei em C:\IALD\Site\tgl (SUBIR_08-09-2026.md): paginas-ponte com redirect e os links
diretos, robots.txt, sitemap.xml, e o card do Limiar da Humildade apontando ao PDF do repositorio. O README/ESTADO/
llms agora dao o um.py e os JSONs na primeira tela, ordem de leitura por tamanho e download por Range. CITATION.cff
no espelho. O protocolo do operador NAO esta em lugar nenhum publico, por ordem dele (paridade inversa).

## 09/09/2026 05:22 - DA IRMA: v334 CUSTODIADA — a tela e' fundada; a regra do backup cumprida (com semente)
sha16 do `um.py` LIDO DO ESPELHO agora: **b18bbaa0433ddd5a** (== selo). §5 do handoff: 16/16. Selo 13/13. Gate IDENTICO ao da
v331. Kernel 604/604 vs manifesto (4907 termos no axiom_report, 52 sem axioma; o rito diz 4217/4217 nos dois stdouts —
mesmos bytes). Delta v331->v334: +11 / -0. As pedras: `TheScreenIsFounded.lean` 2a3f26fca48c615a (`the_answer_of_the_operator_08_09`
= o trio, lido do selo), `CollapseCostAndAttestation.lean` c3dccdc92b6d3b39 (selo `collapse_definition.reading` = COLAPSO_TIPADO__TODAS_AS_CLAUSULAS_NO_KERNEL_COM_O_TRIO;
physical_collapse_proven=False; cost=NOT_MEASURED), `TheRootOfTheProofTree.lean` 9b36ab3b6e47a315 (de pe').
**BACKUP DA VERSAO ANTERIOR, feito ANTES de sobrescrever:** `C:\IALD\Artigo\the_boundary_BACKUPS\um_v331_e1b74a907c403538` (802 arquivos, 0 divergentes, BACKUP_MANIFEST.json
por script) + SEMENTE um_v332_ac424eea22fe6dc2, um_v333_7b833e489395fb56 (um.py dos .bak_ de bytes + stdouts; sha16 iguais a tabela do §1); 24 pastas.
Levado ao espelho: os 13 selados + os 6 declarados + os 4 stdouts (v332, v333, v334 intermediaria e completa) +
kernel inteiro (+13 arquivos, 0 orfaos) + `bancada/TUNEL/` (76 arquivos, ate a 057) + `memoria/` (indice vivo e773f062916f36e6, Atlas
519cbb68c4f1116e — os seus sha16, iguais). Runner v43 sincronizado (22/0, duas rodadas). README: bloco «The screen is founded —
v334» AO LADO do bloco v331 (intacto) + nota no item (vi) («read from v334 on as the wall of EXTERNAL geometric
screens»); as linhas historicas restauradas depois da substituicao cega (medido). ESTADO_ATUAL: «the founded screen»,
«the collapse, typed», Nature's = H1–H2; α; identificacao fisica; o DOI Zenodo dito como da v331 (este selo e' mais
novo) em README/ESTADO/llms/TUNEL/PORTA/CITATION.cff. the_boundary commit 366c7a6 PUSHED (delegado), pos-push 18/18, CI
do kernel disparado. Central: cofre v334 + kernel v334 + ledger de pinos + Atlas §X + 16 dispositivos 16/16 rc=0 (195 s); commit e
push da Central em seguida. Site local v334; UPLOAD e' do operador (staging `_SUBIR_2026-09-09`, medido contra o ar).

## 09/09/2026 07:02 - DA IRMA: A DEFINICAO DE PROVA DO OPERADOR (verbatim) — «lastro de suficiencia»
Ordem/definicao de hoje, verbatim: "segue a definição de prova: lastro de suficiência e isso nós fizemos com o um.py". Leitura registrada ao lado da regua de 05/09 (PROVADA != CONFIRMADA): prova =
o LASTRO que sustenta a afirmacao e que lhe e' SUFICIENTE, nao o juizo; o um.py e' o lastro executavel (arquivo unico,
entrada unica, kernel auditado, ritos, selo, artigo). PROVADA = lastro suficiente e verificavel; CONFIRMADA = juizo,
segue proibido. Gravado no Atlas §X e nas memorias desta sessao. Nada move gate nem estatuto; se a linhagem quiser a
frase no DESENHO ou na MEMORIA_DA_LINHAGEM, e' com voce (superficie sua).

## 09/09/2026 11:11 - DA IRMA: v336 CUSTODIADA — o Nome e' o instrumento; a regra do backup cumprida (com semente v335)
sha16 do `um.py` LIDO DO ESPELHO agora: **f1f330e24120f9be** (== selo). §5 do handoff: 15/15. Selo 13/13. Gate IDENTICO ao da v334.
Kernel 606/606 vs manifesto (4925 termos no axiom_report, 54 sem axioma; o rito diz 4235/4235 nos dois stdouts da v336 — mesmos
bytes). Delta v334->v336: +2 / -0 (`TheSelectionIsTheBallast.lean` 71ebf9680af3d247, `TheNameIsTheInstrument.lean` 7e2e4afd94d3bef9; os dois termos no
trio, lidos do selo). **BACKUP DA VERSAO ANTERIOR, feito ANTES de sobrescrever:** `C:\IALD\Artigo\the_boundary_BACKUPS\um_v334_b18bbaa0433ddd5a` (817 arquivos, 0 divergentes,
BACKUP_MANIFEST.json por script) + SEMENTE um_v335_0e4e0edd47bbd79a (um.py do .bak_ de bytes + stdout; sha16 igual a tabela do §1); 26 pastas.
Levado ao espelho: os 13 selados + os 6 declarados + os 3 stdouts (v335, v336 intermediaria, v336 completa) + kernel inteiro
(+4 arquivos, 0 orfaos) + `bancada/TUNEL/` (78 arquivos) + `memoria/` (indice vivo 6901b818aacca906, Atlas 4a1127580e586684 — os seus sha16, iguais).
Runner v44 sincronizado (23/0, duas rodadas). README: bloco «The Name is the instrument — v336» AO LADO do bloco v334
(intacto), com as suas ordens verbatim (PT + glosa EN) e a definicao de prova; a definicao tambem AO LADO das duas notas da
regua (clarificacao de 05/09 e nota da arvore); linhas historicas restauradas (medido). ESTADO_ATUAL: «the selection is the
ballast; IALD is a state», «the Name is the instrument», a definicao de prova ao lado da regua, e na linha da natureza «that
the selection OCCURS». PORTA raiz: a regua com a definicao. DOI Zenodo dito como da v331. the_boundary commit 6f3c2b2 PUSHED
(delegado). Central: cofre v336 + kernel v336 + ledger (ultima pedra TheNameIsTheInstrument) + Atlas §X + 16 dispositivos 16/16 rc=0 (192 s)
+ Chatgpt/ (pastas de 09/09) com snapshot; commit e push da Central em seguida. Site local v336; UPLOAD e' do operador
(staging `_SUBIR_2026-09-09`, medido contra o ar). Registrado o FECHO declarado por ele; aguardo ordem como voce.

## 10/09/2026 23:33 - DA IRMA: v350 CUSTODIADA (A NATUREZA RESPONDEU) — e a v339 (O FECHO) incluida; a regra do backup cumprida com 13 sementes
sha16 do `um.py` LIDO DO ESPELHO agora: **c9fc7fa432c6cf16** (== selo). §6 do handoff v350 + §5 do v339 (stdouts v337-v339): 41/41 — com UMA
ressalva dita: `MEMORIA_DA_LINHAGEM.md` no disco (594.808 B) != handoff (594.141 B); conferi que a versao do handoff
(`MEMORIA_DA_LINHAGEM.md.bak_20260910_210623`) e' PREFIXO de bytes da atual — append seu depois das 21:06 — e levei a ATUAL [DECLARADO].
O mesmo com `memory\TGL_ATLAS.md` (30274275f8661087 no disco vs ab1ca0674b638edd no handoff; prefixo conferido). Selo 13/13. Gate IDENTICO ao da v336.
Kernel 705/705 vs manifesto (6657 termos, 66 sem axioma; 671 modulos TGLExt; rito 5594/5594 desde a v339). Delta v336->v350: +99 / -0.
22 vereditos da natureza no selo, NENHUM CONFIRMED (conferido por script). Cache 13/13 e pipelines 39 (conjunto eba0915891f5afe3 = seu).
**BACKUP DA VERSAO ANTERIOR, feito ANTES de sobrescrever:** `C:\IALD\Artigo\the_boundary_BACKUPS\um_v336_f1f330e24120f9be` (822 arquivos, 0 divergentes) + 13 SEMENTES v337-v349 (a da v339 com
HANDOFF_v339 + O_FECHAMENTO_ESTRUTURA); 40 pastas.
Levado ao espelho: os 13 selados + 7 declarados (com `O_FECHAMENTO_ESTRUTURA.md`) + 16 stdouts (v337-v350, sem o FALHOU) + 11 capturas em
`rodadas/` + kernel inteiro (+101 arquivos, 0 orfaos) + `bancada/TUNEL/` (112) + `memoria/`. **Decisoes minhas, ditas:** (1) `cache/gw` e
`cache/d1_camb` (so os 13 JSON; `.gitignore` reincluido) e `pipelines/eco_ancorado_v1` foram para a RAIZ do espelho — o um.py le
`../cache` relativo a si (`_CACHE_UP`), e a raiz mantem o um.py como o UNICO .py da pasta do Artigo 3; (2) os `.npz` das janelas GWOSC
NAO foram (120 MB; dado publico, regeneravel), como voce pediu; (3) `HANDOFF_v339_O_FECHO.md` foi ao COFRE (um_unificado_v350) e a semente,
nao ao espelho (handoffs nunca foram ao espelho); (4) `tgl_kernel_v350` vale pela v339 (bytes sem alteracao, DECLARADO por voce).
README: blocos «The close — v339» e «Nature answers — v340->v350» AO LADO do bloco v336 (intacto), com suas ordens verbatim e a tabela dos
10 vereditos lidos do selo; linhas historicas restauradas (medido). ESTADO_ATUAL: caracterizacao (v337), o fecho (v339), a secao «Nature
answers» (vereditos + numeros + estatutos + reproducao com o cache), as seis folhas da natureza, as portas do cache/pipelines. Portas
regeneradas (1.424 links / 0 quebrados). DOI Zenodo dito como v331. the_boundary commit 19fde7c PUSHED (delegado). Central: cofre v350 + kernel
v350 + ledger + Atlas §X + 16 dispositivos 16/16 rc=0 (180 s) + Chatgpt/ (~450 pastas) com snapshot; commit e push da Central em seguida. Site local v350;
UPLOAD e' do operador (staging `_SUBIR_2026-09-10`). O mapa esta fechado; a DECLARACAO e' dele; aguardo ordem como voce.

10/09/2026 23:44 - DA IRMA (errata): o snapshot da Chatgpt/ citado acima era o de 09/09; o de 10/09 falhou por caminho longo e foi refeito: Chatgpt_20260910_233528_delta_de_20260909_110410: 119.540 arquivos na origem, 17.376 copiados (3,85 GB), 102.164 identicos a base, 0 sumidos, 0 divergentes.

## 15/09/2026 20:07 - DA IRMA (Central, executando tambem o papel do site por ordem direta do operador): v357 CUSTODIADA — espelho, site no ar e Central
sha16 do `um.py` LIDO DO ESPELHO agora: **88b0801924454493** (== selo). §5 do handoff 32/32 — com duas ressalvas ditas: `MEMORIA_DA_LINHAGEM.md` no
disco (628.777 B) != handoff (627.238 B), prefixo de bytes conferido (append seu das 18:37), levada a ATUAL [DECLARADO]; `memory/TGL_ATLAS.md`
e `TGL_INDICE_VIVO.md` da Central receberam append de OUTRA sessao (app, 18:47) depois do handoff — o cofre levou a ATUAL; no espelho foram
as versoes PINADAS por voce (`4ed8dd14a8ab4eab` / `1b84a2e9a335f432`), porque o append nao fora vetado nem autorizado para publicacao.
cache/: os 13 JSON rastreados identicos ao cofre v350 por hash; `cache/CHAIN_OF_CUSTODY.json` e `cache/coma_blind/coma_dephasing_prediction.json`
(escritos pelo rito da v357) ficaram FORA do espelho, ditos. Kernel: 1008/8514, +303/-0, 2 alterados so por acrescimo (TGLExt.lean e TGL/Audit.lean,
0 linhas removidas). Selo 13/13. Gate IDENTICO ao da v350. 17 bandeiras 14/3 (as 3 apagadas: as que voce listou). Fronteira do kernel lida do
`core.qg_closure.gate` (nao do selo).
**BACKUP DA v350 ANTES:** `um_v350_c9fc7fa432c6cf16` (949 arquivos, 0 divergentes) + 6 sementes v351-v356 (47 pastas); v351/v352 sem backup de selo/JSON — dito.
Espelho: selados + declarados (com os 2 REVISAO_GERAL e os handoffs v351/v357) + stdouts v351-v357 (FALHA1/ABORTADA1 preservados) +
capturas + kernel + TUNEL (195) + memoria/ pinada; ESTADO_ATUAL/README/LEDGER/CITATION/portas conforme §4; guarda 13/13; commit **12d6fb8** pushed;
pos-push 18/18 ok, 0 divergentes, README raw com o pin. Site no ar: dados adequados a v357 (§7) sem corte de versao — 20260915_191502: SUBIDA VERIFICADA + guarda OK; o `i18n.js` exige correcao em en/pt (innerHTML); o filme
segue com o pino da v350 em texto (foi renderizado dela); bloco do fecho v339 mantem 705/6657/5594.
Central: cofre v357 (63/0; 19 emendas suas levadas, 2 RECOMPILACAO_* ausentes — ditas); **runner v46 (63/0): rodadas 3 e 4 com veredito IDENTICO `FRONTEIRA_SINCRONIZADA_V357__V357_REVISAO_GERAL__17_BANDEIRAS_14_ACESAS_POR_MEDIDA_3_APAGADAS__CETICO_REPROVOU…`; rodadas 1 e 2 FALHA_VERIFICACAO pela pedra v17 antiga (exigia full_TGL_witness_constructed=False junto com a estatica) — ERRATA AO LADO na pedra: full_static_witness_exists e' o teorema (False ETERNO, v61); full_TGL_witness_constructed e' a flag EPISTEMICA, True por medida desde a v356 (A2, regularFullWitness)**; ledger v357; 16 dispositivos 16/16 rc=0 (205 s).
`Chatgpt/`: a origem esta com 1,6 M arquivos / 198 GB (seis projetos Lean com `.lake/` = 102 GB; catalogos publicos copiados; TeX) e o C:
a 97% — snapshot v2 com exclusoes ditas (Chatgpt_20260915_190039_delta_de_20260910_233528 (v2, com exclusoes ditas): 310094 considerados, 190554 copiados (24.8 GB; 12097 reaproveitados da v1), 119540 identicos a base, conferido=True; excluidos por regra: .lake/ 1251069 arq (102 GB), tex_environment/ 40148 (2.1 GB), >25 MB 45 (47.3 GB); removidos do destino 333303 (28.4 GB)); commit por caminho com regra dita (as 12 entradas POR CAMINHO com regra dita: 70856 arquivos (1.44 GB) entram; ficam fora (presentes no disco, ditos): > 25 MB 11 arq (0.5 GB); .lake/ 19934 arq (32.4 GB); cache/ > 1 MB (dados publicos) 1210 arq (51.7 GB); tex_environment/ 40072 arq (2.1 GB)). Higiene do .git (3,48 GiB de lixo removido; fsck
revelou corrupcao PRE-EXISTENTE e INALCANCAVEL em pack-b0b173c7 — reparo e' do operador). Commit e push da Central em seguida.
Irreversiveis seguem seus. O mapa esta fechado; o territorio e' da natureza.

(15/09/2026 20:12) Commit da Central: **4a91e92d** (= origin/main, 72059 arquivos, push verificado). Fim da custodia v357 pelos tres papeis.

## 17/09/2026 10:19 - DA SESSAO DO SITE: v364 CUSTODIADA no espelho e no site no ar
sha16 do `um.py` LIDO DO ESPELHO: **25bca8bd264a2188** (== selo). Rodada COMPLETA; gate identico ao da v357; kernel 1020/8650 (+12/~2); bandeiras 14/3.
Backup da v357 ANTES (`um_v357_88b0801924454493`, 1265 arquivos, 0 divergentes) + sementes um_v358_926fa9ba474f1ed8, um_v359_7f268f2cc108ef41, um_v361_ce45746e33083e20, um_v362_2b5f326b18b3a57d, um_v363_970e84a02bb26841; **a v360 nao foi custodiada** (nem um.py, nem stdout).
Levados: selados, declarados (diario e desenho com o bloco da v364), stdouts, capturas, kernel, TUNEL, `cache/d1_camb/v3` e `cache/diamante_rede`
(o um.py os le por hash). Fora, ditos: `bancada_corpus/` (derivado), `memoria/` (pinada na v357), `cache/` reescrito a cada rito.
Commit **f73420e** pushed; pos-push 18/18. Site no ar: v364 (guarda OK) + os dois filmes da V6. Cofre/runner/ledger da v364: seus.

## 19/09/2026 09:41 - DA IRMA (Central, com o papel do site por ordem direta do operador): v368 CUSTODIADA — espelho, site no ar e Central
Handoff `8d6d64c11596b46f` lido e conferido por script; a nota privada da Central lida antes da custodia e seguida. O operador
confirmou o push («pode custodiar tudo inclusive a v368 e realizar o push como vínhamos fazendo»). sha16 do `um.py` LIDO DO
ESPELHO agora: **4a34fbf36f3ae0d8** (== selo). Backup da v364 fora do repositorio (1283 arquivos, 0 divergentes) + sementes v365/v366/v367
conferidas contra o seu diario; a v360 nunca. espelho `the_boundary` commit **`e654787`** (= `origin/main`); pós-push 18/18, 0 divergentes, README raw com o pin; CI do GitHub **verde** (run 35443270221: kernel reconstruído, 8692 termos auditados, 0 fora do trio); site no ar na v368 (subida `20260919_093904`, guarda: «o site diz o que o selo descreve»); cofre `um_unificado_v368` (187 artefatos, 0 divergências; o arco v358→v368, a v360 nunca) + `tgl_kernel_v368` (1025 formais / 8692 termos); runner da Fronteira **v47** (duas rodadas, veredito idêntico `FRONTEIRA_SINCRONIZADA_V368…`, custódia 187/0, dois céticos reprovaram as injeções); ledger de pinos v368 (0/0); 16/16 dispositivos rc=0 (209 s); snapshot da Chatgpt/ `Chatgpt_20260919_091142_delta_de_20260915_190039` (1426 novos, 0 divergentes). Os dois handoffs da v368 ficaram so no cofre privado da Central
(apontam para a nota privada). O `read-brief.md` da raiz do espelho estava na v350 e foi regenerado. A divisao um.py /
um_consolidado.py esta registrada; o consolidado e' seu, com handoff proprio, e a custodia o publica como primeira porta quando
chegar. Irreversiveis seguem do operador (inclusive o Zenodo, que ele disse que fara). O mapa esta fechado; o territorio e' da natureza.

(19/09/2026 09:44) Commit da Central: **09bbe547** (= origin/main, 2665 arquivos, push verificado). Custódia v368 completa nos três papéis.

## 19/09/2026 11:46 - DA SESSAO DO SITE: leitores de IA (sem mexer no selo)
O espelho ganhou `secoes/`: oito partes curtas + `um-py-funcoes.tsv` + `selo-cartao.md`, geradas por `Site/tgl/v3.0_bancada/tools/gerar_secoes.py`, com sha dos arquivos selados conferido contra o selo. Ganhou tambem `O Custo Geometrico do Zero Absoluto — Haja Luz/ERRATA_20260919_sinal_do_acoplamento_nao_minimo.md`, a errata assinada pelo operador: -xi R |Psi|^2, xi = 1/6.
Na PROXIMA custodia, rodar `gerar_secoes.py`, depois `gerar_read_brief.py`, depois `gerar_llms_site.py`, antes das portas. Ele falha fechado se um marcador de trecho sumir; nesse caso, e a sessao do site que atualiza `secoes_fatias.json`.
O `gerar_readme_frente.py` exige `~/.iald_privado/termos_guarda_readme.json` (a lista de bloqueio saiu da ferramenta publica).
Commits: 479836c, fccc5aa, c01e0dc. O selo e o gate nao foram tocados.

## 21/09/2026 16:41 - DA IRMA (Central): o DOI novo
DOI **10.5281/zenodo.22881996** = **v368** (depositada pelo operador em 21/09/2026; rótulo do registro corrigido por ele de «v.369» para «v.368», revisão 4). Os 14 arquivos do registro conferem por md5 com o espelho `c01e0dc` (`um.py` md5 86e8f46c…, sha256 4a34fbf36f3ae0d8, 31.050.660 B). Concept DOI segue 10.5281/zenodo.20999494; a v331 (10.5281/zenodo.22659173) virou a versão anterior. Espelho `659c90a` e site no ar atualizados; o CITATION.cff e' a fonte unica do deposito. Aviso para a sua v369: o espelho segue na
v368 (o deposito tambem); a custodia da v369 e' decisao do operador.
