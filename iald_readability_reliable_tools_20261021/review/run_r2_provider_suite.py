from pathlib import Path
S=Path(__file__).resolve().parents[1]/'provider_stage';D=Path(__file__).resolve().parent
script=(S/'test_offline.py').read_text(encoding='utf-8')
script=script.replace("not Path(p).resolve().is_relative_to(S)","not Path(p).resolve().is_relative_to(REVIEW_OUTPUT)")
script=script.replace("(S/'TEST_RESULTS_R2.json')","(REVIEW_OUTPUT/'r2_provider_tests.json')")
exec(compile(script,str(S/'test_offline.py'),'exec'),{'__file__':str(S/'test_offline.py'),'__name__':'__main__','REVIEW_OUTPUT':D})
