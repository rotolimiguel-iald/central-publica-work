# Parecer independente final — aplicação de Araki

09/09/2026. **PASS_INDEPENDENT_SEMANTIC_AND_RECEIPT_SCOPE**. Revisão adversarial da dedução escrita e das fontes efetivas, seguida de conferência dos recibos e dos pins atuais. Nenhuma correção material é necessária.

**Documento revisado:** ESTADO_ARAKI_20260909/DEDUCAO_ESTADO_PERTURBADO_ARAKI.md, integralmente lido. O hash do estado revisado está na evidência JSON; este parecer não aprova silenciosamente versões posteriores.

**Conclusão principal:** é correta a aplicação matemática da perturbação limitada de Araki ao mesmo par (M,Ω), para P arbitrário e a classe local somável construída. A existência do estado fiel normal e a identificação modular/KMS são DERIVED + KNOWN com suas hipóteses concretas pagas. Não devem permanecer listadas como falta de existência matemática dessa classe. O construtor analítico completo de Araki não está sendo promovido a novo teorema Lean do lote.

**Unicidade formal:** UnitaryCocycleUniqueness prova o cancelamento (uv*)'=0 em norma; local_cocycle_unique aplica-o ao cociclo local real. O resultado não assume a conclusão como campo. same_potential_same_cocycle e same_cocycle_same_potential são inversas sustentadas, respectivamente, pela unicidade e pela derivada na origem. same_potential_same_dynamics segue da igualdade de cociclos. O texto corretamente não inverte a última implicação: uma fase central pode deixar a dinâmica inalterada.

**Regularidade:** o uso de HasDerivAt é em norma, explicitado. A continuidade em norma da órbita α_t(V), já provada para a classe local, e a estimativa dos termos do expansional fornecem w'(0)=iV em norma; a lei torcida propaga a derivada. O resto exponencial é O(t²), e a estimativa utiliza |t| também para tempos negativos. Não há promoção silenciosa da regularidade forte geral de Araki à norma em todo elemento do fator.

**Preparação e sinal:** ΦV=exp((logΔ+V)/2)Ω usa a exponencial espectral possivelmente não limitada. Prop4.12 fornece seu domínio; Cor4.4 fornece ciclicidade e separação, de onde Z=‖ΦV‖²>0. O Hamiltoniano relativo físico do artigo é −V, passando a −V+logZ·1 após normalização. O operador modular completo tem logaritmo logΔ+V−JVJ, conforme Prop4.8; não é confundido com o preparador relativo logΔ+V. A igualdade de operadores não limitados é entendida no domínio da igualdade fornecida pelo teorema importado.

**Fase central:** CentralScalarPhase foi lido integralmente e seu recibo conferido. A identidade com Z^(−it) exige Z>0 e essa condição está demonstrada na aplicação escrita. A fase conserva a conjugação e desloca d0 para i(V−logZ·1). Os teoremas do módulo de fase não pressupõem nem provam isoladamente a identidade com a derivada de Connes; o documento a classifica corretamente como aplicação da teoria importada.

**KMS:** vem da demonstração analítica de Araki e da identificação de seu expansional com o cociclo da bancada. Não é inferido de uma definição, nem apenas de estacionariedade. A convenção de tempo modular está mantida; o documento não equipara automaticamente tempo modular e tempo físico.

**Evidência de compilação:** as fontes atuais de UnitaryCocycleUniqueness e LocalInteractionUniqueness coincidem com seus recibos PASS170053 e PASS170237. Também foi conferido CentralScalarPhase/PASS165920. Soma medida: 29 teoremas + 3 outras declarações; 32 linhas de axiomas no trio; seis processos exit 0. A revisão não recompilou fontes ou dependências. Escopo dos recibos preservado: não afirmam recompilação nem hash integral de toda dependência transitiva externa.

O parecer semântico anterior à compilação continua preservado como registro histórico; esta nova nota acrescenta a confirmação dos recibos e a revisão da dedução consolidada, sem apagar o histórico FAIL das tentativas anteriores.

**Limites preservados:** a classe tem soma global de normas finita. A conclusão não fecha automaticamente interações extensivas/não limitadas, UV, anomalias relativísticas ou correspondências físicas entre seleção, geometria e matéria. Os critérios de falsificação existentes não foram reabertos. Nenhum teste empírico ou gate foi alterado.

[Evidência medida](C:/IALD/Central de Patentes/Chatgpt/REVISAO_FINAL_ARAKI_20260909_170730_304080/EVIDENCIA_REVISAO_FINAL.json).

Contagens de verificação: {"checks": 13, "passed_checks": 13, "theorems": 29, "other_declarations": 3, "axiom_rows": 32, "processes": 6}.

Foram escritos somente arquivos novos da bancada. Nenhum original foi alterado; nenhum um.py foi executado/importado.
