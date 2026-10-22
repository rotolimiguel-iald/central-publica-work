[REAL] Rede fiel, localidade, prefixos, cauda escalar e calibração de volume: 55 teoremas Lean verificados. [OPEN] E_I geral, shift global e reconstrução contínua.

# ENTREGA 003 — localização na cadeia e ponte volume

05/09/2026 · bancada ChatGPT → gerência Claude · responde à ORDEM 003.

Entrega parcial, com critérios discriminados. Dez módulos novos passaram; a sonda dos 55 teoremas também passou. A demonstração analítica precede os módulos em CADEIA_LOCALIZACAO_VOLUME.md; o estado final e as lacunas estão em CADEIA_RESULTADOS_E_LACUNAS.md.

## Critérios de aceitação

| Critério | Situação | Evidência e limite |
|---|---|---|
| A.1 Isotonia | PAGO [REAL] | chain_isotony; mais forte: chain_order_faithful, A(I)≤A(J) ↔ I⊆J. |
| A.2 Localidade | PAGO [REAL] | chain_locality, para elementos arbitrários dos adjoins estrelados em suportes disjuntos. |
| A.3 Relação com andares | PAGO com correção de índice [REAL] | chain_prefix_eq_level: A({0,…,N})=M_N. O andar N tem N+1 sítios. A([0,N))=M_N literalmente não é o enunciado desta torre. |
| A.4 Esperanças localizadas, oito campos | NÃO PAGO para I geral [OPEN] | prefix_expectation_into conecta a família existente apenas aos prefixos. Construção analítica por fatia/compressão descrita; nenhum termo E_I geral com oito campos foi produzido. |
| A.5 Trivialidade da cauda | PAGO [REAL] | chain_tail_exact: (∀N,x∈A([N,∞))'') ↔ ∃c,x=c1. chain_tail_mem_factor remove a hipótese intermediária x∈M. |
| B.1 Endomorfismo unital, injetivo, imagem própria | NÃO PAGO [OPEN]; obstrução geral [DERIVED] | Sem termo global ρ. Shift normal que desloca geradores não existe para todo perfil: contraexemplo alternado 1/3,2/3. Construção escrita na categoria M(P⁺)→T₁(P), ou estacionária em M(P). |
| B.2 Covariância de ρ | NÃO PAGO em Lean [OPEN] | A rede é fiel e a covariância algébrica está descrita, mas depende da construção global de ρ. |
| B.3 Potências e cauda | NÃO PAGO como potências de ρ [OPEN]; cauda PAGA [REAL] | chain_tail_antitone e chain_tail_exact verificam a família T_N. Falta identificar T_N=ρ^N(M). |
| B.4 Relação modular | PAGO nos geradores [REAL]; NÃO PAGO como identidade de mapas globais | shifted_generator_intertwining usa P⁺(n)=P(n+1); uniform_generator_intertwining usa P(n+1)=P(n). |
| B.5 Distância ao meio-lateral contínuo | PAGO como análise [DERIVED/OPEN] | Discreto não dá grupo contínuo, gerador positivo nem dilatação; Ω da representação total não é cíclico para a cauda. Não foi construída inclusão standard contínua. |
| C.1 Objetos e aditividade | PAGO [REAL] | q_I=Σe_i, chainVolume_local, chainVolume_additive, chainVolume_nonnegative. É objeto positivo; não se afirma projeção. |
| C.2 Calibração | PAGO [REAL] | ω(q_I)=ΣP(i). Uniforme p: C=p e ω(q_I)=p|I|. constant_calibration_forces_uniform prova necessidade. normalizedVolume_state dá C=1 com objetos explicitamente renormalizados. |
| C.3 Distância ao volume contínuo | PAGO como análise; ponte contínua NÃO PAGA [OPEN] | Estado em objetos da cadeia não foi identificado com traço do core em regiões de variedade. Unidade física e limite contínuo ausentes. |

## Axiomas e alcance

Em todos os 55 teoremas, Order003Audit imprimiu exatamente [propext, Classical.choice, Quot.sound]. O log completo e o mapa teorema→axiomas constam da verificação final. Nenhum sorry, admit, declaração axiom nova ou sorryAx está presente nos fontes finais/na sonda final. Isso não elimina hipóteses explícitas dos enunciados.

Lean 4.31.0. O verificador coloca primeiro as dependências copiadas da bancada em LEAN_PATH, lê dependências auxiliares locais e escreve resultados somente em Chatgpt. Fontes e dependências das entregas anteriores continuam necessárias; os módulos não são um pacote independente de mathlib. A gerência deve adaptar imports às raízes canônicas na incorporação, sem criar ciclos com TGLExt. Esta bancada não incorporou os arquivos no kernel canônico.

Para repetir os controles sem sobrescrever esta entrega, copiar prepare_order003_audit.py e os dez fontes Lean para uma nova subpasta de Chatgpt e executar nela C:/Python314/python.exe -B prepare_order003_audit.py. São 16 verificações racionais de médias/variâncias e 16 de volume; não são dados observacionais nem prova por enumeração de um limite infinito.

## Tentativas falhas e preservação

Os logs de compilações com exit não zero são preservados também com sufixo .falha_lean.log, com caminhos e hashes na verificação final. Os fontes intermediários mantêm backups .bak_*. Entre os defeitos corrigidos: coerções de centralizadores, direção de limites, inferência do índice N e expansão matricial. Logs falhos podem conter sorryAx de recuperação do elaborador; isso reprova a tentativa intermediária. Não aparece na compilação final. Avisos intermediários permanecem nos logs datados originais.

Toda escrita desta bancada ocorreu em Chatgpt. A conferência do manifesto abaixo verifica as cópias, não presume que a sessão irmã deixou os originais parados. Nenhum original, memória canônica, gate ou programa vivo foi escrito por esta bancada.

## O que não foi feito

E_I geral e shift global permanecem NÃO PAGOS na acepção Lean pedida. Não foram construídos rede CGMA, espaço-tempo contínuo, escala física, métrica ou prova de gravidade quântica. Nenhum dado observacional foi utilizado nos controles desta ordem. Auditoria independente e incorporação ficam com a gerência. A ordem 004 foi entregue separadamente, sem aplicação de seu diff e sem decisão tomada pelo operador.

## Reprodução em PowerShell

A partir de C:/IALD/Central de Patentes:

```powershell
& './Chatgpt/verify_stage.ps1' -Module TowerTailRigidity
if ($LASTEXITCODE -ne 0) { throw 'Falha em TowerTailRigidity' }
& './Chatgpt/verify_stage.ps1' -Module ChainSiteOperators
if ($LASTEXITCODE -ne 0) { throw 'Falha em ChainSiteOperators' }
& './Chatgpt/verify_stage.ps1' -Module ChainLocality
if ($LASTEXITCODE -ne 0) { throw 'Falha em ChainLocality' }
& './Chatgpt/verify_stage.ps1' -Module ChainPrefix
if ($LASTEXITCODE -ne 0) { throw 'Falha em ChainPrefix' }
& './Chatgpt/verify_stage.ps1' -Module ChainVolume
if ($LASTEXITCODE -ne 0) { throw 'Falha em ChainVolume' }
& './Chatgpt/verify_stage.ps1' -Module ChainSiteFlow
if ($LASTEXITCODE -ne 0) { throw 'Falha em ChainSiteFlow' }
& './Chatgpt/verify_stage.ps1' -Module ChainTail
if ($LASTEXITCODE -ne 0) { throw 'Falha em ChainTail' }
& './Chatgpt/verify_stage.ps1' -Module ChainVolumePositive
if ($LASTEXITCODE -ne 0) { throw 'Falha em ChainVolumePositive' }
& './Chatgpt/verify_stage.ps1' -Module ChainTailClosure
if ($LASTEXITCODE -ne 0) { throw 'Falha em ChainTailClosure' }
& './Chatgpt/verify_stage.ps1' -Module ChainFaithful
if ($LASTEXITCODE -ne 0) { throw 'Falha em ChainFaithful' }
& './Chatgpt/verify_stage.ps1' -Module Order003Audit
if ($LASTEXITCODE -ne 0) { throw 'Falha em Order003Audit' }
```

## Fontes, contagens e SHA256 medidos

- `C:\IALD\Central de Patentes\Chatgpt\TowerTailRigidity.lean` — 5 teoremas — `B70C0AC22430885C9675993B7B9B6D751D726D2B163BB3B7FE3E528D3344E4AC`.
- `C:\IALD\Central de Patentes\Chatgpt\ChainSiteOperators.lean` — 9 teoremas — `BE138B900499A58CBFF2800C0C3BB2247E7C90CA86CBB90E3116D29E6AA9CC2C`.
- `C:\IALD\Central de Patentes\Chatgpt\ChainLocality.lean` — 4 teoremas — `EE6386047FF91F4E19FEB43C6A9CCB9DC20A543DF5165D5AD80EE86C0FD8DE4E`.
- `C:\IALD\Central de Patentes\Chatgpt\ChainPrefix.lean` — 5 teoremas — `322200EF716C53841C4B9AC11EE1FE5C0AAECF680EAA424AEF71072FD981C370`.
- `C:\IALD\Central de Patentes\Chatgpt\ChainVolume.lean` — 8 teoremas — `6F8AE171A4AA9210730A233B1980C97C8DE405D81E21102D3365E82B47C4DCF9`.
- `C:\IALD\Central de Patentes\Chatgpt\ChainSiteFlow.lean` — 5 teoremas — `25C4E40774EC03EA4797FE9E01F239B601309ED7CD83C7C9C4D7749F208D8009`.
- `C:\IALD\Central de Patentes\Chatgpt\ChainTail.lean` — 3 teoremas — `57A2583C16639D58E55177EA07FE6245227A365FF0E049F888B37F20F14104E7`.
- `C:\IALD\Central de Patentes\Chatgpt\ChainVolumePositive.lean` — 7 teoremas — `8918C21DAB5338103EBE02CD406AFB948CE3C17AAF03737A070F8ED622A116D2`.
- `C:\IALD\Central de Patentes\Chatgpt\ChainTailClosure.lean` — 3 teoremas — `79C1736ACB81C72A304D1A774AD281BA3BE2372D6A08F60F62AA345F6E22064D`.
- `C:\IALD\Central de Patentes\Chatgpt\ChainFaithful.lean` — 6 teoremas — `7AF79164274706FC349180D22EACC578519DF50961E794A3B2FDB1342DA7A895`.

## Outros artefatos e SHA256 medidos

- `C:\IALD\Central de Patentes\Chatgpt\CADEIA_LOCALIZACAO_VOLUME.md` — `42ADB32D6AA957EDDADD615227D2E83244AB0766F431966ED6DA33ECF2239701`.
- `C:\IALD\Central de Patentes\Chatgpt\CADEIA_RESULTADOS_E_LACUNAS.md` — `41D3765D08460EC79C4A15CEAAD92B67F69120CA6F135AFB5CF155EFDD607A14`.
- `C:\IALD\Central de Patentes\Chatgpt\CADEIA_CONTROLES_EXATOS.json` — `8D8AB63B5603899371B1DE1DD80382A3017153F78D614F4BC61F0B344DCA8D50`.
- `C:\IALD\Central de Patentes\Chatgpt\prepare_order003_audit.py` — `C4AB27DEBA813D34D95D17D6CDD1826916387EBA18598E11A95DEF2D9951AD50`.
- `C:\IALD\Central de Patentes\Chatgpt\Order003Audit.lean` — `E0AFFFF6751582F69108C4012C91B96FDC668428727A59EBE4470317FD3F9834`.
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM003_INVENTARIO.json` — `74B089C04D8924E95F296905832E5DD304DD1EDABA798F2F2C60A2053EF1F5E9`.
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM003_VERIFICACAO_FINAL.json` — `537319A035034BD6E8072FEA2DF024395004037699652E5DBC0858453CEC989C`.
- `C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1` — `B882654A42E31A2BDE50C8538009C1FD8373F50DDEEAE14A683CD32445E4A923`.
- `C:\IALD\Central de Patentes\Chatgpt\ORDEM003_ENTREGA_TEXTO.md` — `152156551B8840A56A29C97F0D43487DB14C9CA4663DEEE89021A583C3149C26`.
- `C:\IALD\Central de Patentes\Chatgpt\publish_order003.py` — `83A6F89AE329A1FAD5B6584F18422B10B193416237AD5D74A970A13A62E69167`.

## Logs finais

- `C:\IALD\Central de Patentes\Chatgpt\TowerTailRigidity.20260905_150613.log` — `E55361AAC73D8E7D0E8C7DF485A6C1313C98AEFA3C14EA802679ED551EC90988`; exit 0, fonte estável.
- `C:\IALD\Central de Patentes\Chatgpt\ChainSiteOperators.20260905_150909.log` — `84C2C5AD1E25EFA7226B32CFF3BD8F88571926FB2A23E03D880B3EC6DCC92D97`; exit 0, fonte estável.
- `C:\IALD\Central de Patentes\Chatgpt\ChainLocality.20260905_151240.log` — `0B231656BE341B403A5FC598F7EA67F3BAF569101725CD1739E32F085BD30513`; exit 0, fonte estável.
- `C:\IALD\Central de Patentes\Chatgpt\ChainPrefix.20260905_151733.log` — `4A246A6EC89DF15F1B8EA21C8C80D55377016C55A4BCBCC8D9DEF773AFC50AE8`; exit 0, fonte estável.
- `C:\IALD\Central de Patentes\Chatgpt\ChainVolume.20260905_151944.log` — `D2ABF9A6CE55D1D9F79CAD22D6B4A2A37FF177E2397868F867C3F3FECBDDCFF9`; exit 0, fonte estável.
- `C:\IALD\Central de Patentes\Chatgpt\ChainSiteFlow.20260905_151735.log` — `F51CF8E49B638E986D6EC22899F2EE8DF960BF341BAA63B955A91D4A1211193D`; exit 0, fonte estável.
- `C:\IALD\Central de Patentes\Chatgpt\ChainTail.20260905_152106.log` — `959108584CE1D3AB03A3E26354C673AF5104CB02AF39C8EFF230F292E4030F6C`; exit 0, fonte estável.
- `C:\IALD\Central de Patentes\Chatgpt\ChainVolumePositive.20260905_152105.log` — `BA065F072F7F69BE78098D13777342E3041AE216434D4DA9B148264F46D80F58`; exit 0, fonte estável.
- `C:\IALD\Central de Patentes\Chatgpt\ChainTailClosure.20260905_152733.log` — `710297308F001C0F10184812A608AF0AE9747F1BFEF1796C003F8EA10F4D579A`; exit 0, fonte estável.
- `C:\IALD\Central de Patentes\Chatgpt\ChainFaithful.20260905_152632.log` — `56A330EC2603313E3DB004649EA4D506CAFA532E3C6504C43A1862EAFD3ED5C4`; exit 0, fonte estável.
- `C:\IALD\Central de Patentes\Chatgpt\Order003Audit.20260905_152840.log` — `10D97248037B7ED6D7AC0C6C3B737722B613DF1EB901374C2BFE4830690594AA`; exit 0, fonte estável.

Preservação medida: 290 cópias verificadas; 0 divergências. 11 logs falhos preservados com sufixo .falha_lean.log.
