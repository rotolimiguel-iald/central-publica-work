"""Prepare local route and memory-queue records from completed delivery evidence."""
from context import *

check(); stable_seal()
d=read(T/'RESULTADO.json')
assert d==read(H/'CONSTRUCTION_DELIVERY_V404.json')
assert d['delivery']==pin(V.parent/'PUBLIC_DELIVERY_V7.json')
assert read(H/'FINAL_DELIVERY_REVIEW.json')['status']=='PASS_WITH_SCOPE'
text=(f"# Dois filmes V7 — entrega local v404\n\n"
      f"[REAL] ADENDO H concluído e revisto independentemente: {d['public_files']} arquivos públicos pinados, "
      f"{d['media_count']} vídeos e {d['image_count']} imagens validados; filmes de224s e360s, EN/PT, quatro idiomas de legenda. "
      f"{d['audio']['new_units']} sínteses novas, {d['audio']['reused_units']} reutilizadas, "
      f"{d['audio']['requests']} pedidos e {d['audio']['retries']} repetições. Uma sequência de captura; replay integrado61/61.\n\n"
      "[REAL] Negativos e versões anteriores preservados. Voz pessoal fora dos filmes; vozes Andrew/Antonio mantidas. "
      "Nenhum original científico, kernel ou gate alterado. Não repetir capturas ou TTS encerrados.\n\n"
      "[DERIVED] Estimativa direta TTS deUS$0 não é fatura. Custo monetário de CPU/energia não medido. "
      "Verificações de engenharia não equivalem a audição subjetiva integral.\n\n"
      "[OPEN] Integração e publicação são a próxima ação da gerência, já avisada da autorização humana. "
      "Não houve publicação, commit ou push pela sessão do vídeo.\n\n"
      f"Referência própria: {REF}. Entrega: {T/'RESULTADO.json'}.\n")
create(H/'MEMORY_DEPOSIT.md',text)
route={'tipo':'RESULTADO','rota_id':'site.filmes.v7.ordem022','dominio':'SITE_E_PUBLICACAO',
       'titulo':'Filmes V7 v404 construídos e revisados para integração',
       'resultado':f"v404; {d['public_files']} arquivos públicos; {d['media_count']} vídeos; {d['image_count']} imagens; nenhuma divergência numérica não autorizada.",
       'veredito':d['status'],'estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,
       'defeito':'Sem audição subjetiva integral ou custo monetário medido de CPU/energia; publicação não realizada pela sessão.',
       'nao_refazer':'Reutilizar entrega v404 e caches pinados; não repetir captura/TTS encerrados.',
       'proximo_passo':'Gerência integra e publica os dois filmes sob autorização humana já encaminhada.',
       'onde':str(V),'artefatos':[str(T/'RESULTADO.json'),str(T/'RELATORIO.md'),str(H/'FINAL_DELIVERY_REVIEW.json'),str(V.parent/'PUBLIC_DELIVERY_V7.json')],
       'refs':[],'nota':'Construção operacional. Ciência e gate preservados; negativos ao lado.'}
create(H/'FINAL_ROUTE.json',route)
print(json.dumps({'status':'RECORDS_PREPARED','memory':pin(H/'MEMORY_DEPOSIT.md'),'route':pin(H/'FINAL_ROUTE.json')}))
