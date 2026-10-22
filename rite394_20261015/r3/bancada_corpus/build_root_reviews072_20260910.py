from pathlib import Path
from datetime import datetime
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / ('REVISOES_RAIZ_072_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
assert OUT.is_relative_to(ROOT) and not OUT.exists()
OUT.mkdir()
source = ROOT / 'PRIMITIVA_COVARIANTE_LOGVOLUME_072_20260910_003839_535005/PRIMITIVA_LOGVOLUME_E_CONTRATO_Q2.md'
raw_source = source.read_bytes()
source_pin = {'path': source.as_posix(), 'bytes': len(raw_source), 'sha256': hashlib.sha256(raw_source).hexdigest()}

content = r'''# Parecer da raiz — primitiva de logvolume 072

10/09/2026. [DERIVED — revisão matemática interna] [REAL — fonte lida e pin medido]. Li integralmente PRIMITIVA_LOGVOLUME_E_CONTRATO_Q2.md e confrontei as identidades com as convenções BV069. Consultei a fonte primária Hollands0705.3340v4 para o contrato de produtos locais; não importo seu resultado de Yang–Mills como prova de anomalias ausentes no Einstein–sigma.

**Resultado:** não identifiquei erro material na família de primitivas apresentada. O resultado é efetivo na subclasse indicada e não substitui o cálculo geral da quebra de Q2. Uma remissão de seção tem precisão abaixo.

## Identidade e sinais

Com b=log(mu_g/mu_barg), sb=div_g C porque s preserva a métrica de fundo. A identidade de divergências dá sb−C·db=div_barg C. Para uma densidade completa ell com sell=partial_mu(C^mu ell), Leibniz produz

s(b ell)−partial_mu(C^mu b ell)=(div_barg C)ell.

Não falta a ação do ghost no numerador nem aparece uma variação indevida do denominador. A igualdade é de componentes; ao converter a formas com grau total, o descendente deve conservar a mesma convenção. A extensão F'(b)=f(b) segue diretamente da cadeia e conserva a constante de integração como termo fechado modulo d.

Integrando contra chi, o termo total é −integral(dchi wedge D). A equação6.1 mantém esse sinal. Na troca de referência sigma=log(mu_bar1/mu_bar2), temos b2−b1=sigma, a2−a1=−C·d sigma L, o que confere com s(sigma L)−d i_C(sigma L). Essa igualdade não é um mapa entre álgebras quânticas, como o autor corretamente distingue.

## Classe admissível e finitude

A razão de densidades é um escalar positivo sob transporte simultâneo das métricas. Seu logaritmo é real-analítico nas componentes não degeneradas. A expressão tr log(I+tH) é apenas a expansão perto da diagonal e não exige um logaritmo matricial real global para qualquer par de métricas Lorentzianas. Os coeficientes 1/2 trH, −1/4 trH² e 1/6 trH³ seguem da expansão escalar/formal do determinante.

F(b) tem ordem diferencial zero. Multiplicá-lo pela densidade L não aumenta a ordem de jatos; em cada coeficiente perturbativo há somente somas finitas. A quase homogeneidade de escala é preservada porque b não muda na rescalagem geométrica simultânea. Isso não equivale a rescalagem arbitrária de campos isolados: os pesos dos campos normalizados e dos acoplamentos continuam nas hipóteses de L.

O produto por b conserva suporte e regularidade local dos coeficientes das derivadas de delta. Como não envolve o mapa phi, não cria um problema de cartas no alvo. As afirmações de analiticidade exigem que a densidade de entrada também tenha essa propriedade; o texto mantém essa condição. Não há passagem de C∞ a analítico por uma partição de unidade.

O autor separa corretamente uma densidade permitida de uma transformação completa dos produtos T_n: esta última exige polarização, identidades funcionais, contatos e a reconstrução da prescrição. A nota não deve ser citada como demonstração dessa hierarquia inteira nem como identificação da anomalia de grafos com a família (div_barg C)L.

## Alcance cohomológico

Na álgebra básica do único campo completo, um elemento de ghost4 sem ghosts de Lorentz tem antifield zero e quatro ghosts de translação; seu diferencial básico não produz ghost5, pois só há quatro desses geradores. Esse controle explica por que a manobra de retirar ghosts no grau2 não resolve por si a naturalidade da primitiva de grau4. A covariância da família de fundos é uma condição distinta, materializada aqui pela transformação inhomogênea de b.

O setor construído inclui L natural dos campos completos, com seus acoplamentos constantes. Coeficientes espectadores de fundo arbitrários em L podem violar a hipótese sL=L_C L; não devem ser incluídos sem novos termos. A ausência de anomalias de todos os setores, a Ward de variação do fundo e a QME não foram demonstradas por esta família.

## Precisão de remissão e evidência

A seção1 remete ao dicionário BV069, §5. O arquivo consultado possui quatro seções; o gauge não linear e sg=L_Cg estão na **seção4**. Esta é uma correção de remissão, não de equação. A fonte congelada permanece intacta e a observação foi enviada ao autor para seu adendo.

Nenhum CAS, Lean, um.py ou teste de natureza foi executado nesta revisão. Trata-se de revisão interna por agente, distinta de revisão externa e de verificação formal por máquina. O pin da fonte consta no registro JSON desta pasta.
'''

def write_new(name, raw):
    dest = OUT / name
    assert not dest.exists()
    temp = OUT / (name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(dest)
    assert dest.read_bytes() == raw
    return {'path': dest.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

review_pin = write_new('PARECER_PRIMITIVA_LOGVOLUME.md', content.encode('utf-8'))
assert source.read_bytes() == raw_source
record = {'source': source_pin, 'review': review_pin,
          'status': 'NO_MATERIAL_ERROR_FOUND_IN_DECLARED_SECTOR__SECTION_REFERENCE_PRECISION',
          'new_cas': 0, 'new_lean': 0, 'qme_claimed': False, 'originals_written': False}
record_pin = write_new('REGISTRO_PARECER_LOGVOLUME_072.json', (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'directory': OUT.as_posix(), 'review': review_pin, 'record': record_pin}, ensure_ascii=True))
