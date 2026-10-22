import json,hashlib
D=r"C:\IALD\Central de Patentes\work\organismo_iald_12out\3_AUD_ESTATUTO"
rep=D+r"\AUDITORIA_ESTATUTO.md"
h=hashlib.sha256(open(rep,"rb").read()).hexdigest()
ch={"records":[{"id":"aud_estatuto_12out_r1","kind":"fact","statute":"REAL","text":"Auditoria de estatuto e regua do organismo e da prova distintiva: 3 ALTA (homonimo defasagem na pedra; Agape inflada; juiz erra o livro de cobrancas), 5 MEDIA, 5 BAIXA; pedra nao entra na v392 como esta; gate intocado; nenhum veredito.","sources":[{"kind":"document","ref":rep}]}],
"flow":{"phase":"audit_estatuto_delivered","next_action":"gerencia: corrigir ao lado ALTA-1..3 e MEDIA-4..8 antes da v392; podar perguntas ao operador"}}
p=D+r"\memoria\changes_t1.json"
b=json.dumps(ch,ensure_ascii=False,indent=1).encode("utf-8"); open(p,"wb").write(b)
req={"operation":"transition","reference":D+r"\memoria\REFERENCIA_SESSAO.json","expected_revision":0,"event_id":"aud_estatuto_organismo_12out_t1","changes_file":p,"changes_sha256":hashlib.sha256(b).hexdigest(),"actor":{"id":"claude-c1-aud-estatuto-organismo-12out","kind":"agent"}}
json.dump(req,open(D+r"\memoria\transition_request.json","w",encoding="utf-8"),ensure_ascii=False)
print(h)
