from pathlib import Path
import sys,json
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(W/'stage'),str(R)]
import iald_auto_router as router

if __name__=='__main__':
    marker=W/'jev_probe_started.json'
    with marker.open('x') as f:json.dump({'purpose':'new operator-authorized routing pilot','generation_calls':0},f)
    try:
        chosen,receipt=router.choose('Desenvolva a lagrangiana e a equação mestra da TGL com as hipóteses e as fontes. Prefiro uma resposta detalhada com ferramentas de consulta.',
            ['openai','mimo','kimi','claude-haiku','claude-sonnet'],root=R)
        report={'selected':chosen,'receipt':receipt,'generation_calls':0}
    except Exception as exc:
        report={'status':'failed_or_uncertain','error_type':type(exc).__name__,'generation_calls':0,
            'receipt':router.report(R)[:1]}
    with (W/'jev_probe.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
    print(json.dumps(report,ensure_ascii=False))
