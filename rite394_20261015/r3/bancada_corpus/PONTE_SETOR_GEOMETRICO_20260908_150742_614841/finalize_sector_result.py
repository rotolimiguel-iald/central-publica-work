"""Finalize only a successfully compiled local result; no canonical writes."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
folder=Path(__file__).resolve().parent
assert folder.parent==Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
source=folder/"GeometricSectorObstruction.lean"
raw=source.read_bytes()
digest=hashlib.sha256(raw).hexdigest()
history=[]
passed=[]
for directory in sorted(folder.glob("BUILD_*")):
    marker=directory/"BUILD_RESULT.json"
    if marker.is_file():
        r=json.loads(marker.read_text(encoding="utf-8"))
        history.append({"build":directory.as_posix(),"status":r["status"],"source_sha256":r["source"]["sha256"]})
        if r["status"]=="PASS_COMPILED_SCOPE" and r["source"]["sha256"]==digest:passed.append(r)
    else:
        history.append({"build":directory.as_posix(),"status":"NO_COMPLETED_BUILD_MARKER","note":"The initial attempt was reported by the runner as a 240-second timeout; no completed result is claimed."})
assert passed,"No completed build matches the current source"
result=passed[-1]
build=Path(result["build"])
assert (build/source.name).read_bytes()==raw
assert len(result["runs"])==2 and all(r["exit_code"]==0 for r in result["runs"])
log=(build/"GeometricSectorObstruction.log").read_text(encoding="utf-8")
pat=re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
matches=list(pat.finditer(log))
assert not pat.sub("",log).strip()
assert "sorryAx" not in log
assert len(matches)==29
assert all(set(v.strip() for v in (m.group(2) or "").split(",") if v.strip())<={"propext","Classical.choice","Quot.sound"} for m in matches)
assert (build/"ImportsGeometricSector.log").read_bytes()==b""
assert not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom|trace_state)\b",raw.decode("utf-8"))
exact=json.loads((folder/"TESTEMUNHA_EXATA.json").read_text(encoding="utf-8"))
assert exact["status"]=="PASS_EXACT_WITNESS" and all(exact["checks"].values())
assert len(exact["checks"])==exact["check_count"]==63
assert hashlib.sha256((folder/"exact_relative_selector.py").read_bytes()).hexdigest()==exact["script_sha256"]

def record(path):
    data=path.read_bytes()
    return {"path":path.as_posix(),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
boundary_after=[record(Path(item["path"])) for item in result["external_boundary"]]
assert boundary_after==result["external_boundary"]
consulted=[
folder.parent/"DensityStateUniqueness.lean",
folder.parent/"CentralizerPhaseOrbit.lean",
folder.parent/"AUDITORIA_PONTE_20260908_145123_320885"/"AUDITORIA_PONTE.md",
folder.parent/"TUNEL/PARA_CHATGPT/ORDEM_010_horizontes_concretos_aperiodico_e_o_relogio_apos_a_obstrucao.md",
]
consulted_records=[record(path) for path in consulted]
template="# Setor geométrico: construção finita, obstrução e cociclo relativo\n\n**Ainda não foi obtida uma prova de gravidade quântica.** Este trabalho resolve uma questão matemática delimitada que surgiu na auditoria: como obter uma saída comutativa do colapso sem confundir a álgebra de blocos com a álgebra gerada pelo estado.\n\n[REAL — escopo compilado] {{THEOREMS}} teoremas e {{DEFINITIONS}} definições/abreviações no módulo novo, {{PRINTS}} declarações conferidas por impressão de axiomas. Compilação do módulo e de um importador: {{BUILD_STATUS}}. [REAL — cálculo racional] {{CHECKS}} verificações exatas adicionais passaram.\n\nA conclusão útil tem duas partes. Existe uma esperança comutativa canônica em cada corte finito. Porém, para a passagem usual de um sítio a dois, ela não retém todo observável do sítio anterior. Um segundo estado, e portanto um cociclo relativo com informação adicional, permite uma construção diferente que distingue os elementos do bloco. Isso é uma possibilidade matemática verificada neste caso; a escolha física do segundo estado permanece aberta.\n\n## 1. A construção positiva no corte finito\n\n[DERIVED — demonstração matemática escrita; a generalidade desta seção não foi compilada em Lean]\n\nSeja ρ uma matriz densidade fiel em dimensão finita, com decomposição espectral\n\n\\[\n\\rho=\\sum_{\\lambda}\\lambda P_\\lambda,\\qquad\nm_\\lambda=\\operatorname{rank}P_\\lambda,\\qquad \\lambda>0.\n\\]\n\nA álgebra Aρ=W*(ρ) consiste nas matrizes escalares em cada bloco espectral. Defina\n\n\\[\nF_\\rho(X)=\\sum_\\lambda\n \\frac{\\operatorname{Tr}(P_\\lambda X P_\\lambda)}{m_\\lambda}\\,P_\\lambda.\n\\]\n\nEsta aplicação tem imagem Aρ e as propriedades necessárias de uma esperança condicional:\n\n1. **Unidade e idempotência.** Fρ(I)=I. Em cada bloco, a média de cλPλ é cλ; portanto Fρ fixa Aρ e Fρ²=Fρ.\n2. **Bimodularidade.** Para B,C em Aρ, seus valores em cada bloco são escalares. A fórmula dá Fρ(BXC)=B Fρ(X) C.\n3. **Preservação do estado.** Tr(ρFρ(X))=Σλ λ Tr(PλXPλ)=Tr(ρX).\n4. **Completa positividade.** Escolha uma base ortonormal apenas para escrever a prova em cada bloco, e ponha Vλ,ij=mλ⁻¹ᐟ²|λ,i⟩⟨λ,j|. Então Fρ(X)=Σλ,i,j Vλ,ij X Vλ,ij*. Essa soma preserva positividade em todas as amplificações, pois cada termo é uma congruência por I⊗Vλ,ij.\n5. **Covariância.** Para ρ′=UρU*, as projeções espectrais são P′λ=UPλU* e os postos não mudam. A invariância do traço implica Fρ′(UXU*)=UFρ(X)U*. Não foi escolhida uma base para definir Fρ.\n6. **Unicidade no contrato.** Se G é outra esperança condicional ρ-preservante sobre Aρ, escreva G(PλXPλ)=cλPλ usando a bimodularidade. Preservar o estado dá λmλcλ=λTr(PλXPλ). Como λ>0, cλ é o coeficiente da fórmula acima. A bimodularidade anula os blocos cruzados, completando G=Fρ.\n\nA normalidade aqui é automática pela dimensão finita. A caracterização de completa positividade por representações de Kraus e por matriz de Choi é exposta no [teorema2.22 de Watrous](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.2.pdf), pp.82–84. A aplicação específica e as igualdades acima estão demonstradas nesta nota.\n\n**Distinção essencial:** a esperança por blocos Eρ(X)=ΣλPλXPλ fixa a álgebra {ρ}′. Já Fρ faz também a média interna de cada bloco. Em geral Fρ≠Eρ; de fato Fρ∘Eρ=Fρ. A segunda operação é um passo matemático adicional ao colapso gaussiano que apenas elimina frequências diferentes.\n\n## 2. O que acontece ao acrescentar um sítio\n\n[REAL — cálculo e caso compilado]\n\nUse ρ₀=diag(1/3,2/3) no primeiro sítio e ρ₁=ρ₀⊗ρ₀ nos dois sítios:\n\n\\[\n\\rho_1=\\operatorname{diag}(1/9,2/9,2/9,4/9).\n\\]\n\nA inclusão usual leva P₀=diag(1,0) ao observável\n\n\\[\nP=P_0\\otimes I=\\operatorname{diag}(1,1,0,0).\n\\]\n\nNo primeiro sítio, Fρ₀(P₀)=P₀. Nos dois sítios,\n\n\\[\nF_{\\rho_1}(P)=\\operatorname{diag}(1,1/2,1/2,0)\\ne P.\n\\]\n\nLogo Fρ₁∘ι ≠ ι∘Fρ₀. Além disso, W*(ρ₀) incluída dessa maneira não está contida em W*(ρ₁): P não é escalar no bloco degenerado 01/10.\n\nO módulo prova que, entre os observáveis locais diag(a,a,b,b), a aplicação retém exatamente aqueles com a=b. As informações locais não constantes são perdidas por essa média.\n\nA aplicação compilada spectralCenterAverage é a fórmula da partição 1+2+1 desse exemplo. Ela não é apresentada como a projeção sobre W*(ρ) em todos os perfis: por exemplo, em p=1/2 há uma degenerescência maior e a verdadeira média espectral seria diferente.\n\n## 3. Teorema de incompatibilidade com hipóteses explícitas\n\n[REAL — compilado; não é uma impossibilidade de toda reconstrução geométrica]\n\nConsidere qualquer conjunto S de matrizes 4×4 que satisfaça:\n\n- P=diag(1,1,0,0) pertence a S;\n- quaisquer dois elementos de S comutam;\n- S é preservado por conjugação por todo unitário que preserva ρ₁.\n\nEssas três condições são incompatíveis. Basta o unitário V que atua como identidade fora do bloco 01/10 e nesse bloco vale\n\n\\[\nV_{\\rm bloco}=\\begin{pmatrix}3/5&-4/5\\\\4/5&3/5\\end{pmatrix}.\n\\]\n\nEle preserva ρ₁. Por covariância, VPV* pertenceria a S. Mas\n\n\\[\n(PVPV^*-VPV^*P)_{01,10}=12/25\\ne0.\n\\]\n\nAssim P e VPV* não comutam, contradizendo a segunda condição. Nenhum fechamento algébrico extra é necessário para a contradição.\n\nO teorema Lean {{NO_SECTOR}} formaliza essa incompatibilidade para a matriz produto parametrizada por p. O corolário {{NO_EXTENSION}} diz que não existe tal setor que contenha todos os observáveis locais diag(a,a,b,b).\n\n**Alcance:** trata-se de uma seleção que precisa ser invariante sob todos os unitários preservadores do estado considerado. Não se provou impossibilidade de usar dados adicionais, restringir o grupo físico admissível, transportar também um contexto de observação, ou trabalhar com geometria não comutativa. O cociclo relativo merece precisamente essa distinção.\n\n## 4. Um segundo estado resolve a degenerescência neste exemplo\n\n[INPUT — testemunha escolhida, sem alegação de seleção física]\n\nEscolha um segundo estado produto, com pesos 1/4 e 1/5 nos dois sítios:\n\n\\[\n\\sigma=\\operatorname{diag}(1/20,1/5,3/20,3/5).\n\\]\n\n[REAL — aritmética racional] σ é fiel, normalizado e comuta com ρ₁. A densidade relativa é\n\n\\[\nR=\\sigma\\rho_1^{-1}\n=\\operatorname{diag}(9/20,9/10,27/40,27/20).\n\\]\n\nSeus quatro valores são positivos e distintos. O unitário V anterior não preserva σ: a entrada 01,10 de VσV* vale 3/125, enquanto a de σ é zero. Portanto V deixa de pertencer ao estabilizador do par (ρ₁,σ). A obstrução da seção3 não pode ser aplicada ao par simplesmente ignorando esse novo dado.\n\n[DERIVED — prova finita] Defina a família relativa\n\n\\[\nu_t=\\sigma^{it}\\rho_1^{-it}=R^{it}.\n\\]\n\nA igualdade usa a comutatividade das duas densidades. A família é unitária e satisfaz a identidade de cociclo relativa ao fluxo de ρ₁; neste caso ela é também um grupo, pois seus elementos comutam com ρ₁.\n\nComo os valores de R são distintos, seus logaritmos também o são. Para t positivo suficientemente pequeno, os quatro valores exp(it log rj) são distintos. Logo as projeções sobre cada estado da base podem ser recuperadas por interpolação polinomial em u_t. Consequentemente,\n\n\\[\nW^*(u_t:t\\in\\mathbb R)=W^*(R)=\\text{álgebra diagonal completa}.\n\\]\n\nIsso dá uma seleção comutativa capaz de distinguir 01 de 10. Ela retém P e, no exemplo, admite os observáveis diagonais do sítio anterior. A esperança correspondente é a projeção sobre as quatro diagonais.\n\nSob transporte simultâneo (ρ,σ)↦(UρU*,UσU*), R e suas projeções transportam-se por U; a esperança do setor escolhido transporta-se junto. Assim, a construção é covariante **como função do par**. Não se exige que o mesmo setor fique invariável quando σ é mudado sem ser registrado.\n\nEssa é uma realização finita da ideia de que a informação relativa pode selecionar o setor. Ela não prova:\n\n- que o segundo estado seja determinado pelos postulados iniciais;\n- que todos os cortes de uma torre infinita produzam uma escolha compatível, normal e física;\n- que o espectro selecionado seja um círculo ou uma variedade 3+1;\n- que sua métrica, área e calor satisfaçam as hipóteses da reconstrução de Einstein.\n\nNo exemplo finito, o espectro da álgebra diagonal tem quatro pontos. A presença de fases não o transforma automaticamente em S¹.\n\n## 5. Ligação com o acervo existente\n\nA construção não parte da alegação de que “só o estado existe” na TGL. A [densidade de verossimilhança](<C:/IALD/Central de Patentes/Chatgpt/DensityStateUniqueness.lean>) e a [órbita de fase centralizante](<C:/IALD/Central de Patentes/Chatgpt/CentralizerPhaseOrbit.lean>) já são objetos do trabalho anterior.\n\nEsses arquivos foram consultados como fontes existentes. O estado preparado aparece com dados como SummableAmplitude; a fase recebe um gerador. A tarefa subsequente é verificar se os objetos efetivamente escolhidos no modelo fornecem separação espectral e compatibilidade entre cortes, e qual princípio determina a preparação. A testemunha racional desta nota não foi identificada com uma lei física ou com uma rodada canônica desses arquivos.\n\n[OPEN] Mesmo fechando esse setor, continuam necessárias a relação entre distância espectral e angular, a construção geométrica geral, a identificação de área/calor e as hipóteses físicas da reconstrução. O teorema de Einstein já localizado continua sendo uma implicação disponível, não uma conclusão deste lote.\n\n## 6. Evidências, falhas e limites\n\n- [Fonte Lean nova](<{{FOLDER}}/GeometricSectorObstruction.lean>).\n- [Resultado da compilação](<{{BUILD}}/BUILD_RESULT.json>) e [log integral](<{{BUILD}}/GeometricSectorObstruction.log>).\n- [63 verificações racionais e testemunha relativa](<{{FOLDER}}/TESTEMUNHA_EXATA.json>).\n- [Auditor de compilação](<{{FOLDER}}/build_geometric_sector.py>) e [cálculo exato](<{{FOLDER}}/exact_relative_selector.py>).\n- [Inventário final](<{{FOLDER}}/VERIFICACAO_FINAL.json>).\n\nAs tentativas anteriores permanecem na pasta: houve um timeout inicial, um import inexistente e metas de simplificação não resolvidas antes do build identificado acima. Logs com erros ou dependência de sorryAx pertencem às tentativas falhas e não sustentam este resultado. Somente o build PASS e seu hash corrente sustentam a indicação “compilado”.\n\nA completa positividade geral da seção1 e a reconstrução pela família relativa da seção4 são provas matemáticas escritas. O Lean deste lote cobre os enunciados do módulo, incluindo a obstrução universal sob suas hipóteses e as propriedades algébricas indicadas da média 4×4; não se atribui ao compilador uma formalização mais ampla.\n\nO compilador e os imports diretos de Mathlib foram usados por leitura e identificados por hashes. As dependências transitivas da biblioteca não foram todas recompiladas nem todas hasheadas. A inspeção de axiomas está limitada às declarações novas. Não houve revisão científica independente deste lote; ele não é uma custódia canônica nem altera o gate.\n\nTodas as escritas ficaram na nova pasta sob Chatgpt. As revisões dos arquivos novos preservaram backups imediatos de bytes; nenhum original do acervo, Atlas, índice ou memória canônica foi modificado.\n\n**Estatuto final:** avanço matemático delimitado, com uma saída relativa finita e uma obstrução precisa à escolha baseada apenas no estado. Gravidade quântica e reconstrução gravitacional geral permanecem [OPEN].\n"
def declaration_link(name):
    lines=raw.decode("utf-8").splitlines()
    hits=[i for i,line in enumerate(lines,1) if line.startswith("theorem "+name)]
    assert len(hits)==1
    return "["+name+"](<"+source.as_posix()+":"+str(hits[0])+">)"
values={
"THEOREMS":str(result["theorems"]),"DEFINITIONS":str(result["definitions_and_abbreviations"]),
"PRINTS":str(len(matches)),"BUILD_STATUS":result["status"],
"CHECKS":str(exact["check_count"]),"FOLDER":folder.as_posix(),"BUILD":build.as_posix(),
"NO_SECTOR":declaration_link("no_state_covariant_commutative_sector_containing_local_seed"),
"NO_EXTENSION":declaration_link("no_state_covariant_commutative_extension"),
}
for key,value in values.items():template=template.replace("{{"+key+"}}",value)
assert "{{" not in template
def exclusive(path,data):
    assert path.parent==folder and not path.exists()
    temp=path.with_name(path.name+".tmp")
    with temp.open("xb") as f:f.write(data);f.flush();os.fsync(f.fileno())
    assert temp.read_bytes()==data
    os.rename(temp,path)
    assert path.read_bytes()==data
report=folder/"RESULTADO_SETOR_E_COCICLO.md"
exclusive(report,(template.rstrip()+"\n").encode("utf-8"))
links=[]
verification=folder/"VERIFICACAO_FINAL.json"
for link in re.findall(r"\]\(<([A-Za-z]:/[^>]+)>\)",template):
    match=re.match(r"^(.*):(\d+)$",link)
    path=Path(match.group(1) if match else link)
    lineno=int(match.group(2)) if match else None
    if path!=verification:
        assert path.is_file(),str(path)
        if lineno is not None:assert 1<=lineno<=len(path.read_text(encoding="utf-8-sig").splitlines())
    links.append({"path":path.as_posix(),"line":lineno,"status":"VALID_AFTER_EXCLUSIVE_WRITE" if path==verification else "VALID"})
artifacts=[]
for path in sorted(folder.rglob("*")):
    if path.is_file():
        assert ".tmp" not in path.name
        if path.suffix==".py":ast.parse(path.read_text(encoding="utf-8-sig"),filename=str(path))
        artifacts.append(record(path))
assert [record(p) for p in consulted]==consulted_records
final={"status":"PASS_RESULT_PACKAGE","created_utc":datetime.now(timezone.utc).isoformat(),
"report":record(report),"current_source":record(source),"build_result":record(build/"BUILD_RESULT.json"),
"theorems":result["theorems"],"definitions_and_abbreviations":result["definitions_and_abbreviations"],
"printed_declarations":len(matches),"rational_checks":exact["check_count"],"local_links":links,
"consulted_inputs":consulted_records,"direct_external_boundary_rechecked":True,
"build_history":history,"artifacts":artifacts,
"scope":{"quantum_gravity_proved":False,"general_gravity_reconstructed":False,
"independent_scientific_review":False,"canonical_memory_or_gate_changes":False,
"transitive_mathlib_dependencies_rebuilt":False,"transitive_mathlib_dependencies_all_hashed":False},
"own_hash_omitted":True}
exclusive(verification,(json.dumps(final,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
json.loads(verification.read_text(encoding="utf-8"))
print(json.dumps({"status":final["status"],"report":report.as_posix(),"theorems":result["theorems"],
"rational_checks":exact["check_count"],"local_links":len(links),"artifact_count":len(artifacts)},ensure_ascii=False))
