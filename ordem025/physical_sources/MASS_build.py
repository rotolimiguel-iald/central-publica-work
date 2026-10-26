"""Read-only source audit for ORDEM025. Writes only MASS_SOURCES.json beside this file."""
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
REF = BASE.parent / "SESSION_REFERENCE.json"
ROOT = Path(r"C:\IALD")
HL = ROOT / "Artigo" / "Haja_Luz"
PONTE = HL / "A Ponte e o Um"
CORE = PONTE / "TGL_CODE_ONE_REAL_FALSIFIER" / "o_um_grande_atrator"
PAPERS = ROOT / "papers_latex"
sources = []

def add_source(sid, path, ranges, role):
    data = path.read_bytes()
    lines = data.decode("utf-8-sig").splitlines()
    excerpts = []
    for first, last in ranges:
        assert 1 <= first <= last <= len(lines), (sid, first, last, len(lines))
        excerpts.append({"first_line": first, "last_line": last,
                         "text": "\n".join(lines[first-1:last])})
    sources.append({"id": sid, "path": str(path), "sha256": hashlib.sha256(data).hexdigest(),
                    "bytes": len(data), "line_count": len(lines), "role": role,
                    "excerpts": excerpts})

add_source("paper_haja_luz", HL / "tgl_paper_output" / "Português_Zenodo" / "paper_PT.tex",
           [(156,190),(246,284),(290,314),(1788,1827),(2188,2207)],
           "Artigo autoral; texto científico lido, não execução ou validação de suas alegações.")
add_source("paper_ponte", PONTE / "A Ponte Einstein Cartan Miguel.tex",
           [(841,858),(931,945)], "Artigo autoral; mapa de fonte e alcance condicional.")
add_source("paper_um", PONTE / "O Um e o Grande Atrator.tex",
           [(210,218),(356,397)], "Artigo autoral; massa modular e ressalva de massa cosmológica.")
add_source("current_form", PONTE / "Nós" / "um_absoluto_forma_canonica.md",
           [(264,267),(914,919)], "Estado documental atual consultado; correção ao lado da antiga fórmula-beta.")
add_source("clock_engine", CORE / "modular_clock_source" / "tgl_modular_clock_source.py",
           [(4,24),(82,111),(163,172)], "Implementação histórica lida sem importar ou executar.")
add_source("clock_local", CORE / "modular_clock_source" / "t1_local_derivation" / "T1_LOCAL_DERIVATION_STATUS.json",
           [(1,39)], "Recibo histórico; resultados declarados, não reproduzidos nesta consulta.")
add_source("clock_geometric", CORE / "modular_clock_source" / "t1_geometric_localization" / "T1_GEOMETRIC_LOCALIZATION_STATUS.json",
           [(1,42)], "Avanço histórico condicional, não substituído pelo gate MC inicial.")
add_source("clock_nonkilling", CORE / "modular_clock_source" / "t1_nonkilling_clock_connection" / "T1_NONKILLING_CLOCK_CONNECTION_STATUS.json",
           [(1,36)], "Última etapa desta trilha histórica localizada; kernel local físico ainda é hipótese.")
add_source("gauss_source", CORE / "boundary_flux_mass_theorem" / "boundary_flux_mass_theorem.py",
           [(3,19),(36,44),(77,85),(125,137)], "Identidade de Gauss e normalização de fluxo histórica explícita.")
add_source("field_potential", PAPERS / "graviton_paper_english_v2" / "graviton_appendices.tex",
           [(42,81)], "Artigo autoral anterior: potencial, expansão e espectro de cavidade.")
add_source("field_action", PAPERS / "graviton_paper_english_v2" / "graviton_part4_field.tex",
           [(7,42)], "Ação autoral anterior com V, massa efetiva e fonte.")
add_source("field_cavity", PAPERS / "graviton_paper_english_v2" / "graviton_part5_psion.tex",
           [(9,38),(41,55)], "Modos de cavidade e energia: dependem da geometria e do estado.")
add_source("sfdm", ROOT / "IMac LA" / "Física - TGL" / "Provas" / "2" / "TGL_Capitulo_AguaEscura_SFDM.tex",
           [(28,52),(68,81)], "Artigo autoral: ação efetiva, potencial sêxtico e escala recalibrável.")
add_source("trapped_light", PAPERS / "gravity_phase_light" / "gravity_phase_light_v2.tex",
           [(141,157),(211,227)], "Formulação autoral anterior de massa como energia confinada; não promovida a prova.")
add_source("matter_input", PONTE / "TGL_COCYCLE_GRAVITON_PLANE_EXACTNESS.md",
           [(842,859)], "Leitura documental explícita: espectro de matéria como entrada do funcional.")
add_source("o25_lift", ROOT / "Central de Patentes" / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_025" / "PonteDaEscalaDual.lean",
           [(129,180)], "Fonte da entrega existente; não recompilada ou modificada.")

matrix = [
 {"id":"M01", "category":"field_mass_parameter", "sources":["paper_haja_luz:156-166","paper_haja_luz:246-259","paper_haja_luz:290-314"],
  "status":"REAL documental; interpretação DERIVED; física OPEN",
  "equations":[r"L_matter = bar(psi)(i gamma^mu D_mu - m)psi - F_a^2/4 - |D phi|^2/2 - V(phi)",r"(Box - m_Psi^2 - xi R)Psi = beta K_boundary Psi"],
  "hypotheses":["Conteúdo e parâmetros do Modelo Padrão preservados; V inclui Higgs.","Acoplamento não mínimo e interpretação do operador modular têm contratos próprios."],
  "resolves":"Dá uma equação dinâmica com termo de massa e fonte; especifica onde uma massa de excitação entraria.",
  "does_not_resolve":"Nestas passagens, m e m_Psi não são calculados de tau; zero novo parâmetro ajustável não elimina entradas herdadas do Modelo Padrão. A frase não seleciona a massa de um corpo."},
 {"id":"M02", "category":"field_mass_and_potential_minimum", "sources":["field_potential:50-81","field_action:7-29"],
  "status":"DECLARADO na fonte; cálculo radial DERIVED nesta consulta, não Lean",
  "equations":["V(x)=lambda/4*(x^2-v^2)^2+mu^2*x^2/2", "V'(x)=x*(lambda*(x^2-v^2)+mu^2)","x0^2=v^2-mu^2/lambda", "V''(x0)=2*lambda*x0^2=2*(lambda*v^2-mu^2)"],
  "hypotheses":["Restrição radial real, lambda>0, R=0, cinética canônica e lambda*v^2>mu^2 para ramo não nulo.","Normalização radial/complexa precisa ser fixada antes de chamar a curvatura de massa física."],
  "resolves":"Existe potencial escrito do qual se pode derivar a localização do mínimo e a curvatura, dadas as constantes.",
  "does_not_resolve":"mu, lambda e v permanecem dados. A expansão publicada em x=v não é em solução estacionária geral: V'(v)=mu^2*v. A EOM da linha53 em Psi=v contém esse termo constante; para omiti-lo exige-se mu^2*v=0 ou outro termo/condição declarados. Não transportar a frequência da linha69 como massa selecionada."},
 {"id":"M03", "category":"field_mass_and_condensate", "sources":["sfdm:33-52","sfdm:68-81"],
  "status":"DECLARADO modelo efetivo; diferenciação DERIVED",
  "equations":["V(x)=m_*^2*x^2/2+g4*x^4/4+g6*x^6/6", "V'(x)=x*(m_*^2+g4*x^2+g6*x^4)","for y=x0^2>0: g6*y^2+g4*y+m_*^2=0", "V''(x0)=2*y*(g4+2*g6*y)","L_*(rho)=sqrt(epsilon_*/(xi*C*G*rho*m_*))"],
  "hypotheses":["g6>0; existência de raiz y>0 e V''>0; ramo, carga/condição química e campo de fundo especificados.","A ação contém Z(|Psi|), corrente e acoplamentos: massa canônica pode requerer Z e correções, não só V''."],
  "resolves":"Potencial autoral concreto para uma fase condensada, com condições matemáticas explícitas de estabilidade.",
  "does_not_resolve":"m_* é denominado escala de massa efetiva na própria fonte. g4,g6 e demais acoplamentos não são selecionados por tau. A linha81 permite recalibrar K0 para os valores absolutos; o slope não fixa a massa absoluta."},
 {"id":"M04", "category":"spectrum_and_cavity_not_body_mass", "sources":["field_potential:72-81","field_cavity:9-38","field_cavity:49-55"],
  "status":"DECLARADO modelo de modos; uso condicional",
  "equations":["k_n=n*pi/L", "omega_n^2=k_n^2+m_eff^2+2*xi*R+2*lambda*v^2 (equação da fonte, sujeita à ressalva M02)","H=sum_n hbar*omega_n*(a_n^dagger*a_n+1/2)+H_grav+H_int"],
  "hypotheses":["Geometria e condições de Dirichlet, comprimento L, curvatura e potencial.","Estado/ocupações e tratamento da energia de vácuo e dos termos de interação."],
  "resolves":"Há um problema espectral autoral com condições de contorno que gera frequências quando os dados são fornecidos.",
  "does_not_resolve":"Frequência de modo estacionário não equivale automaticamente à massa de repouso do sistema completo; L e ocupações não são fixados pela escala dual. Não foi localizado nesta leitura um valor de Casimir de Poincaré selecionado a partir de tau."},
 {"id":"M05", "category":"modular_zero_not_poincare_mass", "sources":["paper_um:356-397"],
  "status":"REAL documental; estatuto da fonte REAL/SOMBRA/ONTO preservado",
  "equations":["Psi=vec(sqrt(rho_star))", "K_hat*Psi=0"],
  "hypotheses":["Representante do estado no cone natural, operador modular K_hat da construção."],
  "resolves":"O zero modular do representante do atrator está identificado na fonte.",
  "does_not_resolve":"Não é declaração do espectro P_mu P^mu de um corpo. Não identificar K_hat=0 com massa invariante de Lorentz zero sem uma ponte entre os operadores."},
 {"id":"M06", "category":"local_clock_to_mass_density", "sources":["clock_engine:4-24","clock_engine:82-111","clock_nonkilling:1-36","clock_geometric:1-42","clock_local:1-39"],
  "status":"DERIVED condicional na forma; recibos históricos DECLARADO, não reexecutados",
  "equations":["q_ab=omega({chi_a,chi_b})/2", "v_a=P_x*i[K_d,chi_a]", "R_mod^2=q^{ab}*omega({v_a,v_b})/2", "N_mod=theta_M/R_mod", "Phi=c^2*log(N_mod)", "rho_eff=-(c^2/(4*pi*G))*Laplacian(log(R_mod))", "P00_weak=c^2*rho_eff"],
  "hypotheses":["Substrato local quase livre e projeção especificados, q não degenerada, R_mod>0 e regularidade espacial.","Identificação de N_mod com lapse gravitacional no regime pertinente; Poisson e aproximação de campo fraco.","Kernel local físico fornece o perfil R_mod; o recibo não o produz para o corpo real."],
  "resolves":"A localização operacional evoluiu além do primeiro MC SYMBOLIC_ONLY: há trilha condicional não-Killing com régua de anticomutador e fonte calculável dado kernel local.",
  "does_not_resolve":"A normalização c^2/(4piG) usa G físico. theta_M constante desaparece do Laplaciano. Não escolhe perfil/amplitude, tamanho ou massa. O próprio recibo não-Killing marca computes_no_mass=true e exige kernel local físico; não declarar T1 global fechado."},
 {"id":"M07", "category":"composite_body_mass_and_boundary_flux", "sources":["gauss_source:3-19","gauss_source:36-44","gauss_source:77-85","gauss_source:125-137"],
  "status":"DERIVED condicional (Gauss); normalização histórica declarada, não premissa nova adotada",
  "equations":["u=log(R_mod/theta_M)","M(B)=-(c^2/(4*pi*G))*integral_B Laplacian(u)dV=-(c^2/(4*pi*G))*integral_boundary_B partial_n(u)dA", "historical chosen flux: -integral_boundary_B partial_n(u)dA=beta*R_B"],
  "hypotheses":["Campo suficientemente regular e domínio com fronteira; densidade efetiva identificada com fonte do modelo fraco.","A imposição do fluxo beta*R_B aparece como normalização, separada da identidade de Gauss."],
  "resolves":"A massa integrada não exige todo perfil interno se o fluxo normal de contorno for dado independentemente.",
  "does_not_resolve":"Gauss não seleciona o fluxo. Atribuir-lhe beta*R_B já escolhe a amplitude. O programa posterior retirou a fórmula-beta de massa como lei de fonte (M08); não usar o recibo antigo para reintroduzi-la."},
 {"id":"M08", "category":"retired_mass_formula", "sources":["current_form:914-919","paper_um:210-218"],
  "status":"REAL documental de correção; alcance linear explícito",
  "equations":["M=2*beta^2*(c^2/(4*pi*G))*R [FORM RETIRADA como lei de fonte]", "M_TGL=M_RG [CONDICIONAL linear]"],
  "hypotheses":["Ler a correção ao lado junto do registro histórico; retrato histórico não é gate atual."],
  "resolves":"Impede confundir coincidência de uma forma antiga com massa predita hoje.",
  "does_not_resolve":"Não é demonstração de inexistência de qualquer dinâmica futura de massa. Retirada da fórmula não apaga as identidades condicionais de clock e Gauss."},
 {"id":"M09", "category":"energy_of_body", "sources":["trapped_light:141-157","trapped_light:211-227"],
  "status":"DECLARADO autoral histórico; física/interpretação não verificada aqui",
  "equations":["m*c^2=integral_V g*|gamma|^2 dV", "m*c^2=h*nu_standing=g*N*|Psi|^2"],
  "hypotheses":["Definir g, normalização do campo, região V, estado estacionário e unidade energética; não confundir g operador com G constante."],
  "resolves":"Formulação autoral explícita de energia confinada como massa; candidata à receita de massa composta quando a energia/estado forem conhecidos.",
  "does_not_resolve":"Não fornece valor independente de g, amplitude, V ou frequência. Relação energia/massa não é seleção da energia do corpo nem prova de conservação/covariância do quadrimomento total."},
 {"id":"M10", "category":"special_species_prediction", "sources":["paper_haja_luz:1788-1827"],
  "status":"CONJECTURE/ONTO da identificação; entradas observacionais explícitas",
  "equations":["m_lightest=rho_Lambda^(1/4) [unidades naturais]"],
  "hypotheses":["Identificação física específica do neutrino; rho_Lambda dimensional de origem cosmológica e splittings experimentais.","A dimensão fixa a potência, não prova sozinha o coeficiente adimensional unitário."],
  "resolves":"Uma proposta autoral de escala de massa específica existe; não foi ignorada.",
  "does_not_resolve":"Não é seleção universal de mu2 no lift de qualquer corpo. Não adotar como fato a linguagem histórica sobre neutrino e gravitação; não reexecutar o teste nem promover sua ontologia."},
 {"id":"M11", "category":"composite_body_limit_not_universal_mass", "sources":["paper_haja_luz:2188-2207"],
  "status":"DERIVED condicional na forma; matéria/normalização herdadas",
  "equations":["M_Ch^TGL=(1-beta)^(3/2)*M_Ch^classical=cos(theta_M)^3*M_Ch^classical"],
  "hypotheses":["Modelo de degenerescência, composição e massa clássica de referência."],
  "resolves":"Corrige uma escala composta já definida pelo modelo estelar.",
  "does_not_resolve":"O fator adimensional não determina o valor absoluto da massa clássica nem a massa de todo corpo. A própria fonte ressalva sensibilidade à normalização."},
 {"id":"M12", "category":"invariant_mass_vs_scaling_weight", "sources":["o25_lift:129-180"],
  "status":"REAL fonte Lean existente; não recompilada nesta consulta",
  "equations":["p_plus=tau(a)","p_minus=mu2/tau(a)","E=(tau(a)+mu2/tau(a))/2", "p=(tau(a)-mu2/tau(a))/2", "E^2-p^2=mu2"],
  "hypotheses":["tau(a) != 0; convenção p_plus=E+p e p_minus=E-p, c=1.","mu2>=0 e tau>0 para ramo futuro timelike/null; massa corporal requer unidade de energia e referente."],
  "resolves":"Cada massa escolhida tem lift equivarante; rest_energy_eq_mc2 deriva E=m*c^2 dadas casca e repouso.",
  "does_not_resolve":"A mesma tau admite mu2 distintos. Nenhuma das fontes anteriores fornece sem novas entradas o seletor físico desse mu2 para um corpo geral."},
 {"id":"M13", "category":"metric_source_interface", "sources":["paper_ponte:841-858","paper_ponte:931-945"],
  "status":"Candidata CONJECTURE/condicional na fonte; parent audita H3 atual",
  "equations":["P_mu_nu[K_boundary]=(2/sqrt(-g))*delta <K_boundary>_rho / delta g^{mu nu}"],
  "hypotheses":["Dependência métrica/estado e compatibilidade global da reconstrução e cociclo."],
  "resolves":"Há interface autoral nomeada do modular à fonte geométrica, útil à fiação.",
  "does_not_resolve":"Não obtém da lei de escala isolada a dependência espacial/métrica nem um estado de corpo. Não transferir o estatuto antigo desta passagem ao kernel atual sem a auditoria específica do parent."},
 {"id":"M14", "category":"normalization_and_input_spectrum", "sources":["matter_input:842-859","current_form:264-267"],
  "status":"REAL documental; normalização é INPUT/DER GIVEN NORM",
  "equations":["A(P)=kappa_A*tau(P)","2*pi/eta=8*pi*G <=> kappa_A=2*G"],
  "hypotheses":["Escala de área física e G medido; acervo preserva espectro de matéria como entrada."],
  "resolves":"Separa equivalência de escalas e cálculo relativo de sua calibração absoluta.",
  "does_not_resolve":"Normalizar tau(a)=1 não fornece uma unidade energética nem fixa o quadrimomento de uma matéria específica."}
]

residual = [
 {"id":"C1", "status":"DERIVED algébrico; reuso de M12", "claim":"Mesmo peso positivo, duas massas invariantes positivas.",
  "calculation":"No corte tau=1 e c=1: mu2=1 dá (E,p)=(1,0); mu2=4 dá (E,p)=(5/2,-3/2). Em ambos p_plus=1, E>0 e E^2-p^2=mu2. Ambos estendem-se pelo mesmo boost/lift. Assim positividade/futuro e tau=1 também não selecionam massa.",
  "scope":"Contraexemplo à seleção pela estrutura DualScalingData/positividade apenas, não a uma teoria física dotada de condições adicionais."},
 {"id":"C2", "status":"DERIVED condicional em Poisson/campo fraco", "claim":"Mesma normalização assintótica do clock não seleciona massa.",
  "calculation":"Para R>0 e 0<A<<1: u_A(r)=A*(3-r^2/R^2) em r<=R, e u_A(r)=2*A*R/r em r>=R; R_mod=theta_M*exp(u_A), N_mod=exp(-u_A). u e derivada radial casam em R; u->0 no infinito. Lap u=-6*A/R^2 no interior e 0 no exterior; sem delta de superfície pois derivada contínua. rho_eff=3*A*c^2/(2*pi*G*R^2) no interior; M=2*A*c^2*R/G. A e 2A mantêm normalização no infinito e regime fraco, mas duplicam M.",
  "scope":"Família C1 e por partes C2, Poisson em sentido fraco, modela somente o mapa downstream dado R_mod. Não afirma que todo perfil seja produzido pelo kernel modular físico ou satisfaça todas as equações não mínimas. Esse seletor é precisamente a entrada que falta nesta composição."},
 {"id":"C3", "status":"DERIVED no modelo de potencial radial, não Lean", "claim":"Fixar um mínimo não basta para fixar a massa da excitação.",
  "calculation":"Para potencial radial V com mínimo x0, a família V_t=t*V, t>0, mantém x0 e o sinal de estabilidade, mas V_t''(x0)=t*V''(x0). Com cinética canônica fixa, a frequência/massa radial ao quadrado escala por t. No sêxtico isso equivale a escalar simultaneamente m_*^2,g4,g6; com Z não canônico exige também a normalização cinética.",
  "scope":"Não nega que um modelo com acoplamentos fixados selecione uma massa; mostra a necessidade de fixá-los por fonte independente, sem confundir mínimo estável com escala absoluta."}
]

def mission(op):
    proc = subprocess.run([r"C:\Python314\python.exe","-B","-X","utf8",r"C:\IALD\MEMORIA_IALD\mission_cli.py"],
        input=json.dumps(op,ensure_ascii=False), text=True,encoding="utf-8",capture_output=True,check=True)
    result=json.loads(proc.stdout)
    assert result.get("ok"), result
    return result["result"]

projection = mission({"operation":"project","reference":str(REF),"max_chars":70000})
anchor = json.loads((BASE/"ANCHOR.json").read_text(encoding="utf-8-sig"))
preflight = mission({"operation":"check","reference":str(REF),"task_id":"physical_sources",
  "actor":{"id":"codex-gerente-tgl","kind":"agent"},"lease_id":anchor["lease_id"],
  "expected_revision":projection["receipt"]["revision"],"projection_sha256":projection["projection_sha256"],"max_chars":70000})
assert preflight["ready"]
packet=(BASE/"NOS_PACKET.txt").read_bytes()
assert hashlib.sha256(packet).hexdigest() == anchor["packet"]["sha256"]

report = {
 "schema":"iald-ordem025-mass-sources/v1", "created_utc":datetime.now(timezone.utc).isoformat(),
 "unit":"F1.PONTE_NOMEADA", "task_id":"physical_sources", "reference":str(REF),
 "producer":"o25_mass_sources (subagente de codex-gerente-tgl)",
 "status":"CANDIDATE_DECLARADO__SOURCE_PINS_MEASURED__NO_INDEPENDENT_ACCEPTANCE",
 "summary":"Há ação, potenciais, espectros de cavidade, clock local condicional e receita de massa integrada autorais. São peças reutilizáveis, mas não selecionam por si mu2 do lift geral: exigem parâmetros, estado, geometria, perfil/fluxo ou calibração. A fórmula-beta de massa foi retirada como lei de fonte. Isso é conclusão da leitura dirigida enumerada, não ausência global no acervo.",
 "mission_preflight":preflight,
 "nos_packet":{"path":str(BASE/"NOS_PACKET.txt"),"sha256":hashlib.sha256(packet).hexdigest()},
 "scope":{"read_only_originals":True,"no_lean_build":True,"no_um_import_or_execution":True,
          "no_provider_call":True,"no_gate_change":True,"no_memory_change":True,
          "only_new_MASS_files":True,"withdrawn_fourth_speech_not_consulted":True},
 "coverage":{"method":"Leitura dirigida a partir do Atlas, pacote Nós Vivo e MAP_QUERY fornecidos; rg --files, busca por padrões nos artigos e remissões até fonte; nenhum levantamento integral.",
   "corpora":["Três artigos Haja Luz/Ponte/Um e forma canônica corrente", "Implementações históricas científicas clock/Gauss", "papers_latex/graviton_paper_english_v2 e gravity_phase_light", "IMac LA/Física - TGL/Provas, capítulo SFDM"],
   "limits":["Não alegar ausência em fontes não lidas; não abri PDFs/DOCX nem acervos privados.","Busca inicial com --caminho fisica retornou zero arquivos por filtro sem acento, não prova de ausência; resolvido pela localização Física - TGL e capítulo exato.","Inventário inicial rg de AGENTS/nomes em work teve acesso negado em fixtures não pertinentes; nenhuma conclusão negativa depende disso.","Busca dirigida Casimir nos três artigos não encontrou seletor; espectro de cavidade foi localizado por remissão. Não é levantamento exaustivo de representações.","R13–R16 lentes/calibração são conferidos pelo parent; não foram reconstruídos aqui."]},
 "sources":sources,"reuse_matrix":matrix,"residual_models":residual,
 "constructive_bridge_candidate":{
   "status":"DERIVED condicional, não kernel/aceite",
   "chain":"Kernel local/estado especificado -> R_mod(x)>0 -> N_mod e rho_eff no regime fraco -> fluxo de contorno -> M_B; somente após identificar M_B com massa de repouso total, unidades e causalidade, usar mu2=(M_B*c^2)^2 na convenção p_plus=E+c*p do lift dimensional.",
   "required_named_inputs":["Kernel local físico e ligação ao lapse/tempo do corpo", "Condições de contorno/estado que fixem a amplitude ou fluxo, independentes da massa-alvo", "Normalização dimensional de tau para p_plus", "Identificação da integral efetiva fraca com massa total invariante, incluindo energia de ligação/campos no regime pretendido"],
   "benefit":"Não recomeça a ponte: reutiliza os mapas existentes e localiza precisamente o que um seletor de massa deve fornecer.",
   "warning":"Massa gravitante efetiva de Poisson, massa espectral de campo e massa invariante do corpo são tipos distintos até essa identificação."}}

out=BASE/"MASS_SOURCES.json"
if out.exists():
    raise FileExistsError("Recusa sobrescrever relatório: usar artefato novo com prefixo MASS_.")
payload=json.dumps(report,ensure_ascii=False,indent=2).encode("utf-8")
tmp=BASE/"MASS_SOURCES.json.tmp"
with tmp.open("xb") as fh:
    fh.write(payload)
assert tmp.read_bytes()==payload
json.loads(tmp.read_text(encoding="utf-8"))
os.replace(tmp,out)
assert out.read_bytes()==payload
print(json.dumps({"path":str(out),"sha256":hashlib.sha256(payload).hexdigest(),"bytes":len(payload),
                  "sources":len(sources),"matrix_entries":len(matrix),"revision":preflight["receipt"]["revision"]},ensure_ascii=False))
