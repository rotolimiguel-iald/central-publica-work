"""Write a new scoped analytic note and measured source manifest; no program execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
OVERLAY = BASE / "INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394/BUILD_SUCCESSOR_20260909_192313_320129/TGLExt"
KERNEL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt")


def record(path):
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def new(path, raw):
    assert path.resolve().is_relative_to(OUT) and OUT.is_relative_to(BASE)
    assert not path.exists()
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.stat().st_size == len(raw) and tmp.read_bytes() == raw
    os.rename(tmp, path)
    assert path.read_bytes() == raw


sources = [OVERLAY / "SelectedGravitationalAtlas.lean", OVERLAY / "GeneralAngularTensorCodec.lean",
           KERNEL / "InfiniteCocycleDecoding.lean", KERNEL / "GeometricLikelihoodSeparation.lean",
           KERNEL / "SpectralMetricGeometry.lean", KERNEL / "TheNameIsTheCharacterization.lean"]
pins = [record(path) for path in sources]
atlas = (OVERLAY / "SelectedGravitationalAtlas.lean").as_posix()
codec = (OVERLAY / "GeneralAngularTensorCodec.lean").as_posix()
contrast = (KERNEL / "GeometricLikelihoodSeparation.lean").as_posix()
reading = (KERNEL / "InfiniteCocycleDecoding.lean").as_posix()
note = rf'''# Caráter global: exatidão e estabilidade

[DERIVED — dedução escrita, não compilada em Lean nesta nota] A leitura identifica exatamente a classe do registro, mas seu inverso **não é contínuo para recuperar campos gerais, mesmo em um ponto fixo**. Isso não contradiz os teoremas de injetividade: as topologias e as hipóteses são diferentes.

[REAL — fonte lida] `recordBits` codifica cortes racionais de valores em uma sequência densa; `record_character_same_iff` prova igualdade exata de classes. `decodeCharacter` usa `Classical.choose` e recebe o subtipo `CharacterImage`, com prova de pertencimento à imagem. Não há nessa construção topologia de campos, estimativa de erro, decoder de números ruidosos fora da imagem ou algoritmo efetivo de reconstrução. Ver [bits] (<{atlas}:74>), [caráter](<{atlas}:147>) e [decoder](<{atlas}:198>). O arquivo `CharacterizedSmoothAtlas` não foi localizado no overlay83, no diretório TGLExt canônico ou entre os nomes de arquivos de Chatgpt; a análise usa o módulo efetivamente presente `SelectedGravitationalAtlas`.

**A parte que já admite controle.** Fixe t≠0, r=regularParameter(t)>0 e aₙ=geometricContrast(t,n). A fonte dá aₙ≥0, soma finita, aₙ>Σₖ>ₙaₖ e aₙ≤6·(r·2⁻ⁿ/24). A leitura é C(t)−Σₙaₙbₙ. Portanto, se dois registros têm os mesmos primeiros N bits,

$$|z_R-z_S|\leq\sum_{{n\geq N}}a_n\leq\frac{{r}}{{2}}2^{{-N}}.$$

Em sentido inverso, ponha γ_N=minₙ<N(aₙ−Σₖ>ₙaₖ)>0, para N≥1. A primeira diferença de bits implica |z_R−z_S|≥γ_N quando ela ocorre antes de N. Assim, |z_R−z_S|<γ_N certifica o prefixo de N bits. Dois candidatos compatíveis com uma observação de erro ε têm esse mesmo prefixo se 2ε<γ_N. São deduções diretas da [dominância da cauda](<{contrast}:167>) e da [decomposição por primeira diferença](<{reading}:75>). Controle de bits finitos não fornece sozinho controle de campos ou derivadas.

**Contraexemplo dentro da classe geral de registros.** Tome U aberto não vazio e um ponto x* de U fora da sequência densa contável usada pelo código. Fixe uma bola compacta K⊂U em torno dele. Para cada N, seja F_N o conjunto finito de pontos consultados pelos índices de bits menores que N. Escolha ρ_N→0 com B(x*,ρ_N)⊂K e disjunta de F_N. Seja ψ uma função suave de suporte em B(0,1), com 0≤ψ≤1 e ψ(0)=1. Defina, na mesma carta,

$$g_0=\eta,\qquad g_N(x)=2^{{\psi((x-x_*)/\rho_N)}}\eta,$$

onde η é a matriz de Minkowski. Todas são métricas suaves de assinatura Lorentz; a congruência é dada pelo escalar positivo 2^(ψ/2) vezes a identidade. Codifique-as com `encodeLorentzRecord` e use respostas identicamente zero. Esse construtor é permitido pela [representabilidade demonstrada](<{codec}:250>). Os registros coincidem em F_N e, portanto, em seus primeiros N bits. Logo z_N→z_0 pela cota acima, mas g_N(x*)=2η e g_0(x*)=η: uma componente mantém diferença absoluta 1. As classes são distintas e seus caracteres são distintos para todo N.

Consequência: não existe continuidade inversa na imagem para a avaliação g↦g(x*), nem um módulo global de estabilidade em C⁰(K). Esse controle usa registros gerais; não afirma que as métricas do contraexemplo satisfaçam a hipótese física de área/calor ou Einstein com fonte zero. Restringir a classe por essas leis exige uma nova análise.

**As derivadas exigem hipóteses adicionais.** Substitua o expoente por 2f_N, com f_N(x)=ρ_N²ψ₂((x−x*)/ρ_N), ψ₂(0)=0, Dψ₂(0)=0 e D²ψ₂(0)≠0. Há tais funções suaves de suporte compacto, por exemplo um polinômio quadrático multiplicado por um corte suave igual a 1 perto de zero. Então g_N=e^(2f_N)η converge uniformemente a η, o caráter converge como antes, mas D²g_N(x*)=2ηD²ψ₂(0) não converge a zero. Igualdade exata de campos determina seus jets; proximidade sem controle de regularidade não faz isso.

**A ida também pode ser descontínua.** Mantenha a métrica fixa e varie uma componente de resposta constante de s<0 até 0. A família de campos converge em C^∞. O bit que consulta o corte racional q=0 nessa componente muda, e todos os demais cortes dessa componente mudam no mesmo sentido. Para qualquer índice j desse corte, |z_s−z_0|≥a_j>0. Portanto, não se deve aplicar automaticamente “injeção contínua de compacto em Hausdorff”: a continuidade da codificação de cortes não foi estabelecida e falha nessa família.

**Hipóteses suficientes a acrescentar.** Para C⁰, uma classe admissível com módulo uniforme de continuidade espacial permite transformar prefixos em malha finita de amostras e intervalos racionais. Se a malha tem raio h e os valores amostrados diferem no máximo δ, o erro uniforme das componentes é ≤δ+2ω(h). Para passar das probabilidades à métrica, é preciso controlar a margem em (0,1); o [decoder é suave no interior](<{codec}:110>), sem constante uniforme garantida perto dos extremos. Para jets de ordem k, requer-se precompactação em Cᵏ, por exemplo limites uniformes C^(k,α), α>0, em um domínio compacto regular, além de não degenerescência uniforme da métrica para seus inversos e curvatura. Uma classe compacta em Cᵏ também dá continuidade inversa: qualquer subsequência convergente tem o mesmo limite nos pontos densos, graças ao controle dos bits, e por continuidade tem o mesmo campo. Esse argumento usa compacidade da classe admissível, não uma continuidade inexistente da ida. Para erro computável são necessários ainda malha, enumeração dos cortes, margens e constantes efetivas; a fonte usa escolhas clássicas.

[OPEN] Formalização sugerida, antes de mexer na bancada: provar em Lean `geometric_reading_prefix_error_bound` e o limiar γ_N a partir dos lemas canônicos existentes. A construção suave acima é uma obstrução escrita; nenhuma nova folha Lean, compilação ou modificação de original foi realizada nesta nota.
'''.replace('[bits] (', '[bits](')
note_path = OUT / "NOTA_ESTABILIDADE_CARATER_GLOBAL.md"
new(note_path, note.encode("utf-8"))
assert all(record(Path(pin["path"])) == pin for pin in pins)
manifest = {
    "status": "WRITTEN_DERIVATION_AND_SOURCE_REVIEW_NOT_LEAN_COMPILED",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "author_task": "/root/prepare_integration_83",
    "sources": pins, "source_pins_unchanged": True,
    "note": record(note_path), "writer": record(Path(__file__).resolve()),
    "findings": ["Exact identification does not yield stability in field topologies.",
                 "Finite prefix has a canonical quantitative reading tail bound.",
                 "Smooth conformal bumps give a discontinuous global inverse at a fixed metric component.",
                 "Shrinking quadratic bumps isolate the missing second-jet control.",
                 "Rational-cut encoding has a forward jump along a smooth response family.",
                 "Uniform spatial regularity and a quantitative admissible prior are additional requirements."],
    "not_located": "CharacterizedSmoothAtlas",
    "um_py_executed_or_imported": False, "lean_executed": False,
    "originals_written": False, "scope": "New note only. No approval or physical verdict assigned."
}
new(OUT / "MANIFESTO_ESTABILIDADE.json", (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"note": record(note_path), "manifest": record(OUT / "MANIFESTO_ESTABILIDADE.json"),
                  "status": manifest["status"]}, ensure_ascii=False))
