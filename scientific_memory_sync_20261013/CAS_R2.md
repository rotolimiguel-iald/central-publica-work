# Correção ao lado: CAS ACTIVE — 13/10/2026

O candidato anterior de10testes não vinculava o baselineACTIVE da preparação ao escritor. Esta correção mantém o recibo anterior como história e acrescenta snapshot pinado dos BYTESoriginais deACTIVE à preparação. activate exige esse pin e o passa ao argumento expected_active_sha256 da API existente.

canonical_memory.activate_release conserva require_claim e as identidades anteriores, acrescentando somente a unidade recorrente autorizada. Sob LOCK e process_lock(ACTIVE), confere baseline; alvoexatojáativo só reconhece semreescrever. Avançodeoutroexecutor recusa. save_json/replace_bytes receberam parâmetro expected_old opcional compatível com os callers anteriores: conferem bytesesperados antes debackup e novamente antes deos.replace; backupcorrespondente preservado.

Implantar pela raiz, após parecer/pins, OS DOIS módulos candidatos canonical_memory.py e safe_files.py; helper continua na pasta work. process_lock.py instalado é reaproveitado sem edição. Não reiniciar sessão/app/MCP. Nenhuma ativação ou mudança em produção realizada pelo agente.

15testes descartáveis PASS, inclusive corrida real de2threads nasAPI, avançoslegítimos, injeção entre gate e writer e guard antescommit. Zero remoto. Ressalva técnica: locks coordenam osAPIwriters; escritor externo que ignorelocks não recebe garantia impossível deCASnativo dofilesystem. Helpers/roteiro devem usarAPI existente, nunca escrever ACTIVE avulso.

Check real anterior mediuv392comos13originais eACTIVEv391. Nenhum novo check científicos foi usado para promovergate; cert histórico estatuto_da_prova_v391 nafontev392 jácontémhashdoprogramav392coincidentecomselo. Registro preservado, semrename.

Comando de teste: C:\Python314\python.exe -B -X utf8 C:\IALD\Central de Patentes\work\scientific_memory_sync_20261013\test_scientific_memory_sync.py
