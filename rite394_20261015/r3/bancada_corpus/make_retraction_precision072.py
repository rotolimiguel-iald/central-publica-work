from pathlib import Path
import hashlib
import json
import os

root = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
folder = root / 'RETRACAO_BRST_FUNDOS_072_20260910_003743_284187'
path = folder / 'PRECISAO_FONTES_CONJUGADAS_E_REFERENCIA.md'
assert path.is_relative_to(root) and not path.exists()
raw = '''# Precisão: domínio da conjugação e referência causal

10/09/2026, arco 072. [DERIVED — precisão aditiva]. A nota principal permanece intacta. Esta precisão acompanha a revisão independente da retração.

Na seção6, os conjugados BV de B e Omega podem ser introduzidos para escrever uma ação forte no espaço ampliado. A homotopia h e a retração das seções2–5 estão, porém, definidas na subálgebra A[B,Omega] **sem os antifields de fundos externos B* e Omega***. É nessa subálgebra que se deve ler a identidade transportada por C_Psi. A férmion Psi(fields,B), sem dependência de B* ou Omega*, preserva essa subálgebra: desloca os antifields dinâmicos por funções de fields,B e deixa B,Omega como geradores externos. O diferencial ampliado também a preserva. Portanto sua restrição é exatamente o D usado na prova, e a conjugação D_Psi=C_Psi D C_Psi⁻¹ nela é válida.

O deslocamento de B* na apresentação forte continua necessário para produzir o termo de fonte Omega correto na ação restrita. Isso não exige que B* apareça como argumento das inserções causais. Se fossem desejadas a homotopia e as inserções na álgebra que também contém B*,Omega*, seria necessário definir a contração do par conjugado e um dicionário adicional para essas inserções. Esse domínio maior não é afirmado nesta entrega.

Uma realização causal auxiliar pode fixar uma referência B0, conservar seus propagadores e tratar todos os desvios B−B0 e parceiros como fontes centrais formais, incluindo mudanças de cinética, termos lineares e termos Omega na interação. Nesse esquema, a derivação das fontes não diferencia o kernel livre. A construção de Ward com anomalia precisa ser demonstrada com esse contrato, e não confundida com a variação da família de propagadores em B.

Mesmo quando esse levantamento é construído, a retração B→fields não elimina automaticamente B0 dos coeficientes de renormalização. Uma anomalia a_ext(B,B0) pode projetar-se numa expressão ainda dependente de B0. A comparação com A_sm sem espectadores, a naturalidade da primitiva e a identificação com a família causal variável continuam exigindo suas próprias provas. Acrescentar uma referência fixa não deve esconder um segundo fundo inerte dentro da frase “campos completos”.

Nenhum resultado de QME, estado físico interagente ou UV é acrescentado por esta precisão. Nenhum arquivo original, fonte congelada ou memória canônica foi alterado.
'''.encode('utf-8')
temp = path.with_suffix(path.suffix + '.tmp')
with temp.open('xb') as stream:
    stream.write(raw)
    stream.flush()
    os.fsync(stream.fileno())
assert temp.read_bytes() == raw
temp.rename(path)
assert path.read_bytes() == raw
print(json.dumps({'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}, ensure_ascii=True))
