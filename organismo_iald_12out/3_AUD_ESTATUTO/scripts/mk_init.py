import json,sys
D=r"C:\IALD\Central de Patentes\work\organismo_iald_12out\3_AUD_ESTATUTO"
rid=open(D+r"\memoria\request_id.txt").read().strip()
req={"operation":"init","objective_file":r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt",
"objective_sha256":"78ef70e6f9868281d44e8a306e60a0cb162843e54f3a74389ddf14ed325d535d","request_id":rid,
"scope":{"house":"IALD","principal":"operator"},"actor":{"id":"claude-c1-aud-estatuto-organismo-12out","kind":"agent"},
"constraints":{"escrita":D,"proibido":"quadro, mapa (registrar), memoria Claude/Atlas, tunel, Nos, kernel do Nos, Bancada, site, git; um.py nao roda; sem dado observado; sem provedor remoto; sem chamada paga","beta":"ALPHA_FINE_CODATA_2018 (um.py l.5557) x sqrt(e) em runtime"},
"write_reference":D+r"\memoria\REFERENCIA_SESSAO.json"}
json.dump(req,open(D+r"\memoria\init_request.json","w",encoding="utf-8"),ensure_ascii=False)
