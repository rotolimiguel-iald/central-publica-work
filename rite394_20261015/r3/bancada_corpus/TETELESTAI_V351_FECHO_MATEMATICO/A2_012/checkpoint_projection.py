from pathlib import Path
import json, os, subprocess
R = Path(__file__).resolve().parent
B = R.parent / 'RETOMADA_A1B_012'
p = B / 'status_a2_projecao_finita_20260915.json'
assert not p.exists()
d = json.loads((B / 'status_inicio_a2_adendo001_20260915.json').read_text(encoding='utf8'))
d['title'] = 'A2: projeção finita não nula construída no mesmo traço de A1'
d['text'] = '''[REAL — DEV kernel, ainda sem revisão independente] V354FiniteTraceSupport compilou em attempts/20260915_122154_993374; V354SpectralThreshold completo em attempts/20260915_123314_079969, todos os nomes auditados apenas no trio. regularTrace_finite_positive_below extrai positivo finito não nulo pelo próprio contrato A1; kernel_projection_mem_vonNeumann reutiliza o critério mathlib do comutante; positive_operator_has_threshold_projection obtém corte como projeção do núcleo da parte negativa de X-epsilon I. scalarTrace_finite_subprojection_exists obtém projeção finita não nula em qualquer canto projetivo não nulo; scalarTrace_finite_projection_exists é aplicação à unidade. Sem dimensão finita de Hilbert, sem receber projeção finita ou testemunha como premissa. [DEV] V354RegularMatrixCorner em desenvolvimento: siteMark e unidade matricial do primeiro sítio representados na mesma álgebra; preparação do split ortogonal. Tentativas falhadas preservadas; sorryAx de tentativa falhada não é prova. O orçamento600000 é LOCAL no teorema CFC e responde ao timeout observado de200000; sem relaxar kernel. [REAL — autoral] Poincare entregou B1′ em Chatgpt/B1_PRIME_012; 27 declarações e9 controles conforme recibo autoral, ainda aguardam revisão. Carver01a0a5b5-e12d-70c1-a68a-c6f13373e3c0 revisa em REVISAO_B1_PRIME_012, Poincare saneia5.4b/c/d/f/g/h em SANEAMENTO_ADENDO_001_012. Nenhum deles altera A2. [OPEN] A2 ainda requer split finito igual, calibração, operador/domínios/afiliação/gap e compatibilidade com traço TOTAL legado de ContinuousCoreData; A1 é traço no cone positivo, não presumir tau(x*x) como adaptação. A1 permanece pago; objetivo ADENDO001 ACTIVE, gate eD1 intocados. ErrataLACUNAS e explicação namespace já pagas. Esta entrada supera processos/status DEV anteriores, não rerodar escritores antigos.'''
d['artifacts'] += [
 '../A2_012/src/TGLExt/V354FiniteTraceSupport.lean',
 '../A2_012/src/TGLExt/V354SpectralThreshold.lean',
 '../A2_012/attempts/20260915_122154_993374/RESULT.json',
 '../A2_012/attempts/20260915_123314_079969/RESULT.json']
b=json.dumps(d,ensure_ascii=False,indent=2).encode('utf8')
t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
subprocess.run([r'C:\Python314\python.exe','-X','utf8','-B',str(B/'checkpoint_status_v2.py'),p.name],cwd=B,check=True)
