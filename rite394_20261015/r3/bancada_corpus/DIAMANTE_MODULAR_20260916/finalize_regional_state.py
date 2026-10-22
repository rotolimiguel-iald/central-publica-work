"""Publish the scoped research handoff inside Chatgpt, with byte custody."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
NOW = datetime.now().astimezone().isoformat()


def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def atomic(path, data, allow_replace=False):
    path.resolve().relative_to(WORK.resolve())
    if isinstance(data, str):
        data = data.encode("utf-8")
    if path.exists() and not allow_replace:
        raise FileExistsError(path)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
    assert Path(temporary).read_bytes() == data
    os.replace(temporary, path)
    assert path.read_bytes() == data


def replace_with_backup(path, new):
    previous = path.read_bytes()
    backup = path.with_name(path.name + ".bak_" + STAMP)
    atomic(backup, previous)
    assert backup.read_bytes() == previous
    data = new.encode("utf-8") if isinstance(new, str) else new
    assert len(data) >= len(previous), "This delivery only adds text or expands the draft."
    atomic(path, data, allow_replace=True)
    return pin(backup)


def json_new(path, value):
    atomic(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    sources = [
        WORK / "QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md",
        WORK / "HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912/ESTADO_FISICO_HADAMARD_E_CONTRATOS.md",
        WORK / "REDUCAO_ESCALAR_VETOR_SIGMA_20260909_212531/REDUCAO_ADM_MODOS_FISICOS.md",
        WORK / "MODOS_TENSORIAIS_EXATOS_20260909/ACAO_TT_E_MODOS_EXATOS.md",
        WORK / "CONVENCAO_ACAO_ESTADO_LOCAL_20260909_214710_215498/CONVENCAO_SINAL_E_TRANSPORTE.md",
        WORK / "CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md",
        WORK / "CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md",
        WORK / "RELOGIOS_RELACIONAIS_FUNDO_FISICO_088_20260910/RELOGIOS_X_SIGMA_E_RETRACAO_DE_JATOS.md",
        WORK / "TUNEL/PARA_CHATGPT/RECIBO_DIAMANTE_MODULAR_v358.md",
    ]
    before = [pin(path) for path in sources]
    canonical_audit = json.loads((ROOT / "CANONICAL_DIAMOND_SOURCE_AUDIT.json").read_text(encoding="utf-8"))
    old_canonical = canonical_audit["canonical_um"]
    assert Path(old_canonical["path"]).name == "um.py"
    canonical_now = pin(Path(old_canonical["path"]))
    assert canonical_now["sha256"] == old_canonical["sha256"]

    proof = ROOT / "ESTADO_EINSTEIN_SIGMA_E_MODULAR_LOCAL.md"
    reviewed = pin(proof)
    text = proof.read_bytes().decode("utf-8")
    marker = "**Prova.** Escolha um compacto temporal interior"
    assert text.count(marker) == 1
    clarification = r"""**Objeto da estimativa.** Se \(u^+_{A,n}=R_A(f_{p_{A,n}}e_{A,n})\), escreva \(h^+_{A,n}=[P u^+_{A,n}]_h\). Em uma trivialização real analítica, o vetor-kernel é \(\Psi_H(x)=(\sqrt\hbar\,\overline{h^+_{A,n}(x)})_{A,n}\), com a contração tensorial e a medida da fonte 067. Assim \(kP^*(q,0)=\int\langle q(x),\Psi_H(x)\rangle\,d\mu_g(x)\). Sua continuação usa \(P R_A(g_p e_{A,n})\), onde todos os coeficientes de fundo são continuados analiticamente; (A) é a estimativa da norma desse vetor, componente tensorial por componente.

"""
    text = text.replace(marker, clarification + marker)
    text = text.replace("O teorema de valor de fronteira holomorfo coloca", "O [Corolário 2.9 de Strohmaier–Verch–Wollenberg](https://arxiv.org/pdf/math-ph/0202003), para distribuições com valores em Hilbert e o tubo acima, coloca")
    text = text.replace("Esta prova escrita precisa de revisão adversarial específica antes de receber estatuto de trabalho selado; controles numéricos de modos não substituem a análise funcional acima.",
                        "Esta prova escrita recebeu revisão adversarial independente favorável dos §§2–6, registrada em REVISAO_INDEPENDENTE_ESTADO_LOCAL.md; as duas explicitações menores solicitadas foram incorporadas. O parecer não revisa uma conclusão interagente/UV e não equivale a verificação em Lean. Controles numéricos de modos não substituem a análise funcional acima.")
    backups = [replace_with_backup(proof, text)]

    review = f"""# Revisão independente — estado modular local

{NOW}. Revisor delegado Goodall, id `01a0abfc-54d8-7e31-a623-32bc927ed3a2`, separado do autor da construção. Parecer recebido por ferramenta; nenhum arquivo-fonte alterado pelo revisor. [DERIVED — revisão matemática escrita, não Lean].

**Veredito:** favorável aos §§2–6 no alcance declarado. O revisor não identificou correção substancial necessária nem pré-requisito analítico/de gauge ainda não pago nas fontes examinadas.

Revisou: P* e preservação de suporte; suficiência da estimativa holomorfa após reconstruções S/V/TT; continuação única; argumento pelo complemento simplético; Gram/Fock e segunda quantização. Explicitou que a separação usa inclusão do subespaço espacialmente separado no complemento simplético, sem supor dualidade de Haag.

Pediu duas explicitações menores: nomear o vetor de modos reconstruídos após P ao qual se aplica a estimativa (A), e citar nominalmente o Corolário 2.9 de SVW para a passagem do tubo ao cone dual com valores em Hilbert. Ambas foram incorporadas depois do parecer. O manifesto conserva o pin da versão revisada e da versão entregue.

**Fora do parecer:** compilação Lean, completude UV, estado interagente, geometricidade física do fluxo modular e o cálculo separado de corrente conforme. Não atribuir a esta revisão um resultado nesses assuntos.

Fonte revisada: `{reviewed['path']}`; bytes {reviewed['bytes']}; SHA256 medido `{reviewed['sha256']}`. A versão entregue tem adições de explicitação e registro do parecer, sem alteração da conclusão.
"""
    atomic(ROOT / "REVISAO_INDEPENDENTE_ESTADO_LOCAL.md", review)
    json_new(ROOT / "REGIONAL_STATE_SOURCE_AUDIT.json", {"timestamp": NOW,
             "sources_before_finalize": before, "canonical_current": canonical_now,
             "canonical_matches_previous_audit": True,
             "reviewed_proof": reviewed, "delivered_proof": pin(proof),
             "reviewer_id": "01a0abfc-54d8-7e31-a623-32bc927ed3a2",
             "literature": [
                 {"url": "https://arxiv.org/pdf/math-ph/0202003", "read": "Cor2.9, Prop5.3, Thm5.4, Remarks5.6–5.7"},
                 {"url": "https://arxiv.org/pdf/2305.07606", "read": "Section2, standard subspaces and second quantization"},
                 {"url": "https://arxiv.org/html/1709.08020v1", "read": "spherical harmonic sectors and eigenvalues"}],
             "sources_after_finalize": [pin(path) for path in sources]})
    assert before == [pin(path) for path in sources]

    addition = f"""## {NOW} — estado Einstein–sigma recuperado e operador modular local

[REAL — leitura] Ação066, estado físico linear067, reconstruções S/V/TT, ação com sinal reconciliado, álgebra auxiliar perturbativa069 e projetor local088 recuperados em Chatgpt. Corrige a lacuna de recuperação anterior: existe ação e existe estado linear explícito no fundo escolhido. A pergunta por um estado físico INTERAGENTE/UV não foi respondida pelas fontes; a mera ausência de ação/estado linear não deve voltar a ser alegada. WedgeNet e a rede induzida por testes físicos são construções distintas; o teorema scalarAlg anterior continua restrito à primeira.

[DERIVED — revisão independente favorável; não Lean] Com P=Id−K_gF da088, P* gera exatamente os testes físicos locais. Modos explícitos067 e harmônicos da esfera fornecem estimativa de tubo holomorfo; continuação única dá densidade local e localidade dá separação em diamantes com complemento causal aberto. L(D) é standard; Delta_D=Gamma(s_D* s_D), K_omega,D=dGamma(−log(s_D* s_D)). A prova está em ESTADO_EINSTEIN_SIGMA_E_MODULAR_LOCAL.md, com parecer independente registrado. Não foi diagonalizado Delta_D nem demonstrada geometricidade.

[DERIVED/REAL — diagnóstico clássico] Corrente do fundo: div(T xi)=3c psi/a²; derivada central da carga =−24 pi² c a0² tanh(eta0) I(L), I=(2+cos²L)/6−L cot(L)/2. Três verificações por quadratura/diferenças passaram e traço-zero falso foi recusado. Isso é uma contribuição escalar de fundo, NÃO o primeiro coeficiente não central do resto modular. Sem taxa de Lindblad inferida desse sinal.

[OPEN] k T_t f = delta_D^(it) kf para a ação geométrica renormalizada; primeiro coeficiente não central físico; estado físico interagente e completude UV. Meta ampla ativa, com progresso nesta rodada. Sem alteração de um.py, gate ou originais. Handoff vigente desta etapa: HANDOFF_PONTE_REGIONAL_EINSTEIN_SIGMA.md; manifesto REGIONAL_STATE_MANIFEST.json. Memórias canônicas recebem proposta pelo túnel; escritas desta bancada ficam em Chatgpt.
"""
    for name in ["MEMORIA_CENTRAL.md", "REGISTRO_DAS_CONVERSAS.md", "PROPOSTA_MEMORIA_ATLAS.md"]:
        path = ROOT / name
        backups.append(replace_with_backup(path, path.read_bytes() + ("\r\n\r\n" + addition + "\r\n").encode("utf-8")))

    requirements = {"timestamp": NOW, "classification": "PROGRESS", "goal_status": "ACTIVE",
                    "new_result": "standardness and local modular construction from existing linear Einstein-sigma state",
                    "independent_review": "FAVORABLE_SCOPED",
                    "linear_action_and_state_available": True,
                    "physical_interacting_state_available": False,
                    "geometric_modular_identity": "OPEN",
                    "first_physical_noncentral_coefficient": "OPEN",
                    "UV_completion": "NOT_ESTABLISHED",
                    "new_lean_theorems": 0, "gate_changed": False,
                    "no_progress_streak": 0, "blocked_declared": False}
    json_new(ROOT / "REQUISITOS_ESTADO_REGIONAL.json", requirements)
    tunnel = WORK / "TUNEL/DO_CHATGPT/ENTREGA_ESTADO_MODULAR_REGIONAL_20260916.md"
    atomic(tunnel, f"""# Entrega — estado Einstein–sigma e modularidade regional

{NOW}. Responde ao alvo do diamante físico após a V2 incorporada no v358.

**[DERIVED, revisão independente, não Lean]** O estado linear067 e o projetor local088 fornecem um subespaço real standard no diamante interior com complemento causal aberto. Há construção dos objetos modulares da mesma realização física linear. Identificação geométrica, estado interagente e UV permanecem OPEN.

- [Handoff para o motor](../../DIAMANTE_MODULAR_20260916/HANDOFF_PONTE_REGIONAL_EINSTEIN_SIGMA.md)
- [Demonstração regional](../../DIAMANTE_MODULAR_20260916/ESTADO_EINSTEIN_SIGMA_E_MODULAR_LOCAL.md)
- [Revisão independente](../../DIAMANTE_MODULAR_20260916/REVISAO_INDEPENDENTE_ESTADO_LOCAL.md)
- [Corrente clássica, separada do resto modular](../../DIAMANTE_MODULAR_20260916/CARGA_CONFORME_DO_FUNDO_SIGMA.md)
- [Manifesto](../../DIAMANTE_MODULAR_20260916/REGIONAL_STATE_MANIFEST.json)

Não criar outro pinching nem atribuir selo KERNEL à prova escrita. Não reabrir PRODUCT_TOWER; não identificar a rede física com WedgeNet. Ação e estado LINEAR já existem em Chatgpt: corrigir a recuperação de memória. Nenhum gate ou original alterado. Proposta de adendo ao Atlas/índice/linhagem/desenho no handoff e em PROPOSTA_MEMORIA_ATLAS.md.
""")
    artifacts = [ROOT / name for name in [
        "ESTADO_EINSTEIN_SIGMA_E_MODULAR_LOCAL.md", "CARGA_CONFORME_DO_FUNDO_SIGMA.md",
        "REVISAO_INDEPENDENTE_ESTADO_LOCAL.md", "HANDOFF_PONTE_REGIONAL_EINSTEIN_SIGMA.md",
        "verify_sigma_conformal_current.py", "SIGMA_CONFORMAL_CURRENT_CHECKS.json",
        "REGIONAL_STATE_SOURCE_AUDIT.json", "REQUISITOS_ESTADO_REGIONAL.json",
        "MEMORIA_CENTRAL.md", "REGISTRO_DAS_CONVERSAS.md", "PROPOSTA_MEMORIA_ATLAS.md",
        "finalize_regional_state.py"]] + [tunnel]
    json_new(ROOT / "REGIONAL_STATE_MANIFEST.json", {
        "timestamp": NOW, "artifacts": [pin(path) for path in artifacts],
        "backups": backups, "external_sources_unchanged_during_finalize": before == [pin(path) for path in sources],
        "canonical_matches_previous_audit": True, "review_scope": "PROOF_SECTIONS_2_TO_6_NOT_LEAN",
        "status": requirements})
    print(json.dumps({"status": "DELIVERED", "files": len(artifacts), "byte_backups": len(backups),
                      "canonical_matches": True, "handoff": str(artifacts[3]),
                      "goal_status": "ACTIVE"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
