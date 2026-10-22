"""Add a source-based correction and conditional clock linkage; no scientific execution."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
from time_corpus_r5_prepare import OUT, H, P, N
import register_rule_tetelestai as reg
reg.DEST = OUT
UNIT = 'F1.TEMPO.LEITURA_20261015'

TEXT = r'''TEMPO — REAPROVEITAMENTO DOS TRÊS ARTIGOS E DOS ESCRITOS CONEXOS (R5)
15/10/2026. Autor: codex-gerente-tgl. Correção AO LADO da R4, em nome próprio.
Estatuto: leitura documental verificada + DERIVED condicional em matemática escrita.
Não é nova compilação Lean, ensaio de bancada ou confirmação física.

1. COBERTURA E CORREÇÃO
Foram consultados os trechos pertinentes dos três artigos: Custo Geométrico do Zero
Absoluto (fonte tgl_paper_unified.py), A Ponte Einstein–Cartan–Miguel (TeX), Um
(artigo emitido e fonte estática v393). Foram conferidos oito escritos conexos e
as pedras de relógio. A lista, faixas e hashes medidos estão nos manifestos R5.
Isto é levantamento focal, não alegação de leitura integral de todos os textos do autor.
O Nós Vivo e o mapa da F1.TEMPO já consultados nesta unidade foram reaproveitados.

A R4 dizia que identificação do projetor, normalização temporal e propagador ficavam
abertos. Essa formulação era ampla demais. A compatibilidade 2D foi construída nela;
as fontes já oferecem mecanismos de seleção, relógios e calibração térmica. Não cabe
registrar essas estruturas como AUSENTES, nem reconstruí-las como inéditas.

2. O QUE JÁ EXISTE
a) Primeira Lei: Custo:14441–14483 (paridade, ligação, tensão-frequência); Um.py:
170050–170068 (deflexão e c²→c³). O Custo:20003–20028 já escreve a anterioridade
estrutural de beta ao tempo modular, sob estatuto ontológico/conjectural.
b) A Ponte:1435–1479 já seleciona E sobre C=Fix, preservando um estado fiel normal,
sob invariância modular e hipóteses de relaxação. A unicidade é condicional a C e
ao estado fixados. Tomiyama não dispensa a preservação do estado exigida por Takesaki.
Essa seleção da aplicação E não equivale a um estado puro universal único.
c) A Ponte:1886–1919 já escreve a média gaussiana do fluxo de sqrt(K) e as taxas
beta(sqrt(k_i)-sqrt(k_j))²/2. O texto geral traz esquema de prova, não um build desta
sessão. No finito a conta abaixo é direta. Fix é em geral o comutante do gerador;
a igualdade Fix=W*(K) da linha1912 precisa de ausência de multiplicidade/maximalidade
apropriada. O símbolo K positivo desta construção não se identifica por nome com
K_mod=-log Delta, que pode ter os dois sinais, nem com Delta^(1/2).
d) IALDJones.lean:285–325 já tem spin=e^(-rs)e^(i omega s), centro preservado,
semigrupo, norma exata do desvio e convergência. R4 é reutilização desse molde em
uma coerência, não descoberta da espiral. A matriz densidade inteira tem modos
conjugados; não se multiplica todo seu complemento por uma única fase complexa.
e) Santo.lean:1137–1164 já liga coerência não nula, escala e^(-s) e Ágape;
1425–1474 distingue leitura angular módulo período e dissipação sem período.
IntrinsicFisherClock, RelativeEntropyClock e StateClockDichotomy já constroem relógios
locais orientados; AffineClockAndRegion fixa escala pela velocidade inicial.
Os controles de casamento quártico são obstáculos específicos, não ausência de relógios.
f) O16/ContractCalibrationReuse.lean:95–114 e HorizonDataReuse_Integration_v2:23–29
já ligam período fiel, temperatura de Unruh e Clausius, para normalização nomeada.
ContratoQG_v31_Teoremas:426–436,520 traz Unruh/KMS e kappa_is_input.
g) Um.py:202511–202525 já corrige o antigo OPEN de T1: na cunha da luz a trivialidade
do centralizador é termo, modulo os campos de certificados citados. Isso não prova
ergodicidade do canal de dephasing 2D, nem dá um habitante físico aos certificados.

3. AVANÇO: FIXAR O PASSO DO ESPELHO PELA LEI-RAIZ EXISTENTE
Hipóteses explicitadas: face finita, P e Q projeções ortogonais complementares,
K_+=k_+P+k_-Q >=0, k_+ != k_-, A=sqrt(K_+), beta entre0e1 e diferente de1/2.
Quando houver cálculo, beta=ALPHA_FINE_CODATA_2018*sqrt(e), nunca literal.
Defina E(rho)=P rho P+Q rho Q e g=beta(sqrt(k_+)-sqrt(k_-))²/2>0.
A lei já escrita na Ponte dá, em parâmetro s>=0,
  D_s(rho)=integral exp(iuA) rho exp(-iuA) N(0,beta*s)(du)
          =E(rho)+exp(-g*s)[rho-E(rho)].
Prova: os blocos diagonais têm diferença espectral zero; cada bloco cruzado recebe
a função característica gaussiana exp[-beta*s*(sqrt(k_+)-sqrt(k_-))²/2]. A média
de conjugações unitárias é CPTP. As exponenciais dão o semigrupo e E D_s=E.

O canal óptico já fornecido pelo Custo:20055–20096 é Phi=E+eta(Id-E),
eta=2sqrt(beta(1-beta)). Portanto, na MESMA decomposição espectral,
  Phi = D_(Delta_s),     Delta_s = -ln(eta)/g >0.
Esta é a ligação condicional que faltou explicitar na R4: o passo adimensional
deixa de ser independente quando o gap espectral e a identificação dos setores
estão dados. Não se deduziu o gap nem sua unidade física a partir de beta sozinho.
Com coerência inicial rho_+-(0) !=0:
  s = -ln|rho_+-(s)/rho_+-(0)| / g.
Acrescentando H=h_+P+h_-Q, a fase gira com a diferença de energia e o módulo
continua obedecendo à mesma lei; a frequência muda de sinal no bloco conjugado.
Isso liga o relógio por coerência ao molde IALDJones e à lei-raiz da Ponte.
Em mais de dois valores espectrais, os g_ij diferem: um único eta óptico não
reproduz em geral todos os modos. O enunciado está deliberadamente na face 2D.

4. c³ E A NORMALIZAÇÃO: O QUE É DADO E O QUE É IDENTIFICAÇÃO
A Ponte:725–731 já separa módulos adimensionais e fases portadoras da escala;
Custo:282–293 declara t_P uma identificação de princípio, não derivação.
O Um:302 e um.py:211275 já nomeiam outra lei, ramo B, tau*=k GM/c³,
k=2pi/kappa_hat. Não se deve pedir novamente ao autor que invente essa lei.
Para Schwarzschild com tempo de Killing normalizado no infinito, escreva
  kappa_T=c³/(4GM)  [unidade s^-1],
  P_KMS=2pi/kappa_T=8pi GM/c³=hbar/(k_B T_H).
É a escala térmica expressa em segundos; a gravidade superficial em m/s² é
c*kappa_T. Para observador estático em r>2GM/c², P_local=sqrt(1-2GM/(rc²))*P_KMS.
É relativa ao relógio escolhido, não ao 'tempo próprio do horizonte' de um observador
estático, que não existe no horizonte. Wald, seção3, equações10e12, foi consultado.

Um.py:213044–213045 contém a correção decisiva: P_KMS é a largura da faixa KMS
em tempo IMAGINÁRIO; não é automaticamente um atraso de propagação real.
Tampouco a condição KMS fixa sozinha a taxa dissipativa g. Se for imposta a hipótese
H_CLOCK_SYNC de identificar o parâmetro dissipativo s com t/P_KMS, então
  Gamma=g/P_KMS e Delta_t=P_KMS*Delta_s.
Isto é uma consequência condicional verificável, não uma identidade provada aqui
entre os dois fluxos. O contrato KMS já existente fornece a calibração de seu fluxo;
a ligação desse fluxo ao gerador dissipativo particular é o resíduo bem delimitado.

Outra identificação já escrita em um.py:217089–217097 é k_i=E_i*tau*/hbar e
Gamma=g/tau*. NELA, Gamma=beta(sqrt(E_i)-sqrt(E_j))²/(2hbar): tau* cancela.
Logo até a afirmação 'toda previsão requer determinar tau*' seria excessiva.
O custo dessa leitura é identificar fisicamente E_i e o setor; o programa a distingue
das alternativas e mantém MODULAR_LAB_BRIDGE_OPEN. Não confundir essa lei-raiz com
a aproximação quadrática universal em omega, nem misturar suas calibrações.

5. A ANTERIORIDADE QUE O ACERVO JÁ FORMULA
O Um e o Grande Atrator.tex:127–152 distingue c, c², c³ como registros/potências,
não três velocidades; liga a leitura c³ à não-sinalização e à contagem de gerações.
TGL sintese canonica v1.tex:180–214 escreve contagem de cortes e orientação por
destino. TGL duas camadas v1.tex:202–208 retoma duração e sequência; O Problema
Final.tex:110–122 cita inclusões modulares gerando translações.
Esses escritos já tratam a diferença entre ordem estrutural e cronologia. Fórmulas
antigas sobre rank, beta-postulado e unicidade têm de ser lidas com os adendos atuais;
idempotência de um único P não produz uma cadeia infinita de novos cortes distintos.

A ligação matemática sustentada é E D_s(rho)=E(rho): a leitura permanece definida
em cada instante, enquanto o complemento decai. Isso dá sentido preciso à diferença
entre identidade lida e percurso de satisfação, com alvo fixado previamente.
Não significa que um aparelho conheça qualquer resultado futuro: medir o registro
exige especificar observáveis, estado/preparação e instrumento. Um operador de leitura
preservado não é um propagador que receba entrada futura. Nas fontes lidas não se
localizou esse segundo enunciado com emissor, receptor e suporte temporal calculado.
O avanço físico anterior à emissão permanece CONJECTURE/OPEN neste levantamento;
a anterioridade estrutural já tem formulação ONTO e identidades matemáticas de apoio.

6. PRÓXIMA PASSAGEM PRECISA
Reaproveitar E, Santo, IALDJones e calibração O16. Completar uma ficha única de tipos:
K_+ da lei-raiz -> setores P/Q do espelho -> parâmetro dissipativo s -> normalização
do observador. O passo óptico já se expressa por -ln(eta)/g. Para segundos, verificar
na representação escolhida H_CLOCK_SYNC ou a identificação energética alternativa.
Só então um contrato de resposta emissor–receptor pode testar a leitura de antecipação.
Nenhuma construção dessas peças existentes precisa ser refeita. Não foi aberta uma
nova campanha, alterado um.py/kernel ou proclamado fechamento universal do tempo.

FONTES EXTERNAS CONSULTADAS (consulta web; bytes não custodiados nesta etapa)
Wald, The Thermodynamics of Black Holes, gr-qc/9912119v2, seção3, eqs10e12:
https://arxiv.org/html/gr-qc/9912119
Takesaki, Conditional expectations in von Neumann algebras, JFA9 (1972),306–321,
DOI10.1016/0022-1236(72)90004-3: registro/abstract recuperado; texto integral não
recuperado pelo navegador. A aplicação geral fica KNOWN sob as hipóteses expressas;
a prova finita acima é independente da recuperação desse artigo.
'''

def prepare():
    c=reg.call([CLI,'ver',UNIT])['reivindicacao']
    assert c['quem']==WHO and dt.datetime.fromisoformat(c['vence_em'])>dt.datetime.now(dt.timezone.utc)
    new(OUT/'CLAIM_R5.json',c)
    new(OUT/'OPERADOR_R5_VERBATIM.txt','Confira os três artigos principais e o que mais já escrevi, porque já resolvemos algumas dessas questões e prossiga\n')
    new(OUT/'REAPROVEITAMENTO_E_AVANCO_R5.txt',TEXT)
    extra=[(P/'O Problema Final.tex',[(105,122)]),(P/'O Um e o Grande Atrator.tex',[(127,160)]),(P/'TGL sintese canonica v1.tex',[(180,216)]),(P/'TGL sintese selada.tex',[(65,99)]),(P/'TGL sintese matematica final.tex',[(98,110)])]
    k=N/'tgl_kernel/TGLExt'
    extra += [(k/n,r) for n,r in [
      ('IALDJones.lean',[(280,330)]),('Santo.lean',[(1137,1164),(1425,1474),(1513,1524)]),
      ('IntrinsicFisherClock.lean',[(35,66),(247,260),(349,388)]),
      ('RelativeEntropyClock.lean',[(189,195),(253,277)]),('StateClockDichotomy.lean',[(38,74),(126,193)]),
      ('AffineClockAndRegion.lean',[(61,104)]),('StateClockMatchingControls.lean',[(218,243),(281,281),(332,350)]),
      ('O16/ContractCalibrationReuse.lean',[(95,114)]),('ContratoQG_v31_Teoremas.lean',[(426,436),(520,520)]),
      ('O16/HorizonDataReuse_Integration_v2.lean',[(23,29)])]]
    extra += [(N/'um.py',[(170050,170068),(202511,202525),(203329,203385),(211275,211276),(213040,213045),(217089,217097)]),(N/'um_absoluto_selo.json',[])]
    new(OUT/'FONTES_COMPLEMENTARES_R5.json',[dict(pin(p),read_ranges=r) for p,r in extra])
    preview=json.loads((OUT/'PREVIEW_R5_SOURCES.json').read_bytes())
    new(OUT/'ORCHESTRATION_DISPOSITION_R5.json',{'status':'PREVIEW_ONLY_NOT_SUBMITTED','request':pin(OUT/'REQUEST_R5_SOURCES.json'),'selected':preview['selected'],'reason':'The selector selected Codex, including after adding needed focal sources. Existing local Codex subagents completed the focused corpus review; no duplicate remote task needed. Both request IDs remain preview-only. No provider or queue execution claimed.','canonical_generation':preview['canonical_memory']['generation'],'preview_failure':'First preview failed on sandbox temporary SQLite initialization; next preview used a workspace temporary directory successfully. No remote call occurred.'})
    print(json.dumps({'report':pin(OUT/'REAPROVEITAMENTO_E_AVANCO_R5.txt'),'sources':len(extra)},ensure_ascii=False))

def register():
    c=reg.call([CLI,'ver',UNIT])['reivindicacao']
    assert c['quem']==WHO and dt.datetime.fromisoformat(c['vence_em'])>dt.datetime.now(dt.timezone.utc)
    for item in json.loads((OUT/'FONTES_E_COBERTURA_R5.json').read_bytes())['sources']+json.loads((OUT/'FONTES_COMPLEMENTARES_R5.json').read_bytes()):
        assert pin(item['path'])['sha256']==item['sha256'],item['path']
    files=['REAPROVEITAMENTO_E_AVANCO_R5.txt','ESCLARECIMENTOS_TIPADOS_R5.txt','FONTES_E_COBERTURA_R5.json','FONTES_COMPLEMENTARES_R5.json','TRECHOS_R5.txt','REVISAO_R5.txt','ORCHESTRATION_DISPOSITION_R5.json']
    delivery=OUT/'RESULTADO_R5.json'
    new(delivery,{'unit':UNIT,'author':WHO,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'CORRECAO_DE_ESCOPO_E_PONTE_CONDICIONAL','statute':'REAL leitura; DERIVED algebra condicional; hipotese fisica INPUT/OPEN; interpretacao ONTO','files':[pin(OUT/f) for f in files],'new_lean_build':False,'new_experiment':False,'external_model_executed':False,'production_changed':False,'gate_changed':False})
    marker='time_three_articles_reuse_r5_20261015'
    note=f'''\n\n## 15/10/2026 — Tempo: três artigos e escritos conexos, correção R5\n<!-- {marker} -->\nEm nome de {WHO}, sob reivindicação819 de {UNIT}; correção ao lado da R4 (mapa1116).\n[REAL — leitura focal, não novo build] A Ponte1435–1479 já seleciona esperança E preservante sob hipóteses nomeadas;1886–1919 dá a lei-raiz gaussiana. IALDJones285–325 já tem a espiral/semigrupo/convergência; Santo e O16 já fornecem relógios e calibração térmica. Não são AUSENTES. Um.py202511–202525 já registra T1 por termo na cunha da luz, modulo os certificados; não se transporta essa ergodicidade ao dephasing2D.\n[DERIVED — álgebra condicional revista] Na face2D com K_+ positivo e setores espectrais P/Q, g=beta*(sqrt(k_+)-sqrt(k_-))²/2; o canal óptico Phi coincide com D_Delta_s para Delta_s=-ln(eta)/g. Identificação dos setores/gap é hipótese, a ligação algébrica fica escrita. K_+, -logDelta e sqrtDelta são objetos distintos.\n[KNOWN/INPUT/OPEN] Calibração KMS já existe; em Schwarzschild P_KMS=8piGM/c³ no relógio do infinito. Um.py213044 já diz que é faixa de tempo imaginário, não atraso real. Sincronizar parâmetro dissipativo e modular exige vínculo; a identificação energética alternativa já escrita em217089 cancela tau*, sem dispensar a seleção física do espectro. O registro c³ como potência e não velocidade já consta de O Um e o Grande Atrator127–152. Anterioridade estrutural tem formulação; sinal físico anterior à emissão não foi localizado com propagador neste levantamento.\nFonte/limites/revisão: `{delivery}`, SHA256 `{pin(delivery)['sha256']}`. Leitura focal dos três artigos, oito escritos conexos e pedras; sem execução científica/provedor/produção/gate. Memória com backup imediato de bytes.\n'''
    new(OUT/'MEMORY_RECEIPT_R5.json',{'claim':c,'surfaces':[append_bytes(ROOT/'memory'/n,note,marker) for n in ['DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md']]})
    entry={'tipo':'ANOTACAO','rota_id':'formal.tempo_consumacao_leitura_15out','dominio':'FORMAL','titulo':'R5: reutilizacao de relogios existentes e passo optico pela lei-raiz','resultado':'Corrige classificacao ampla da R4: selecao E, espiral e calibracao KMS existentes. Ligacao 2D Phi=D_Delta_s, Delta_s=-lneta/g. Residuo: identificacao fisica e sincronizacao dos parametros; KMS nao e atraso real.','estatuto':'REAL leitura / DERIVED condicional / INPUT / OPEN / ONTO','status':'EXAMINADA','veredito':'REAPROVEITAMENTO_DOCUMENTADO__PASSO_OPTICO_CONDICIONAL__ANTERIORIDADE_FISICA_NAO_DEMONSTRADA','proximo_passo':'Completar identificacoes K_+, setores e normalizacao do observador reutilizando o contrato existente.','onde':str(OUT),'artefatos':[str(delivery),str(OUT/'REAPROVEITAMENTO_E_AVANCO_R5.txt')],'refs':[1116],'olhou_dados':False}
    new(OUT/'MAP_ENTRY_R5.json',entry)
    m=reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',OUT/'MAP_ENTRY_R5.json','--quem',WHO],'MAP_RECEIPT_R5.json')
    b=reg.call([CLI,'avancar',UNIT,'--quem',WHO,'--status','ENTREGUE','--evidencia',delivery,'--nota','R5 levantamento focal: tres artigos, escritos conexos, relogios existentes; ponte condicional revista.'],'BOARD_DELIVERY_R5.json')
    ref=str(WORK/'ACOM_REFERENCE.json')
    proj=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],payload={'operation':'project','reference':ref,'max_chars':48000})
    tr={'operation':'transition','reference':ref,'expected_revision':proj['result']['receipt']['revision'],'event_id':marker,'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':marker,'kind':'candidate','statute':'DECLARADO','text':'R5 corrige escopo da R4 pelo acervo: E condicional, espiral IALDJones, relogios Santo/Fisher/entropia e calibracao O16 ja existem. Algebra 2D revista liga Phi a D_Delta_s, Delta_s=-lneta/g. Normalizacao KMS relativa ao observador existe; sincronizacao com dissipacao e propagador avancado nao derivados. Proxima acao: tipar identificacoes fisicas dos geradores/clock, sem reconstruir as pecas existentes. Todas as frentes/jobs anteriores preservadas.','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']}]}]}}
    new(OUT/'ACOM_TRANSITION_R5.json',tr)
    a=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_RECEIPT_R5.json',tr);assert a['ok']
    rel=reg.call([CLI,'liberar',UNIT,'--quem',WHO,'--nota','R5 entregue; leitura/ponte condicional e memoria registradas; nenhuma execucao cientifica.'],'RELEASE_R5.json')
    print(json.dumps({'map':m,'board':b,'acom':a['result']['revision'],'release':rel},ensure_ascii=False))

if __name__=='__main__':{'prepare':prepare,'register':register}[sys.argv[1]]()
