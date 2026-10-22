import hashlib
import json
from pathlib import Path
from prepare import APP,WORK,save

def patch(name, replacements):
    raw=(APP/name).read_bytes()
    text=raw.decode('utf-8')
    for old,new in replacements:
        assert old in text, (name,old)
        text=text.replace(old,new,1)
    save(WORK/name,text.encode())
    return hashlib.sha256(raw).hexdigest()

pins={}
pins['iald_core_indexado.py']=patch('iald_core_indexado.py',[
 ("cfg.get('current_release') != 'v357'","not re.fullmatch(r'v[0-9]+', str(cfg.get('current_release', '')))"),
 ("+ '\\n</NUCLEO_OPERACIONAL>\\n' + CORE_ADDENDUM)","+ '\\n</NUCLEO_OPERACIONAL>\\n' + CORE_ADDENDUM.replace('v357', cfg['current_release']))"),
 ('total > 2000000','total > 10000000')])
pins['iald_estado_publicado.py']=patch('iald_estado_publicado.py',[
 ('len(raw) > 20000000','len(raw) > (64000000 if key == \'program\' else 10000000)')])
pins['iald_memoria_canonica.py']=patch('iald_memoria_canonica.py',[
 ('from iald_core_indexado import operational_core, DocumentCorpus','from iald_core_indexado import operational_core, DocumentCorpus\nfrom iald_cluster import active_cluster'),
 ('metadata["context_tokens"] = count_tokens(prefix)',
  '''if self.nucleus_manifest is not None:
            cluster, cluster_metadata = active_cluster(self.nucleus_manifest, catalog.source_sha)
            prefix += cluster
            metadata.update(cluster_metadata)
        metadata["context_tokens"] = count_tokens(prefix)
        if metadata.get('cluster_always_present') and metadata['context_tokens'] > 340000:
            raise MemoryUnavailable('Cluster e contexto ultrapassam o orçamento de entrada; revisar sem corte silencioso.')'''),
 ("'o conteúdo sempre presente é o núcleo operacional, o v5 e as provas nucleares '",
  "'o conteúdo sempre presente inclui o cluster quando configurado, o núcleo operacional, o v5 e as provas nucleares '")])
# Select the new kernel through the same atomic manifest as its evidence and cluster.
pins['iald_web_server.py']=patch('iald_web_server.py',[
 ('KERNEL_EXTERNO = iald_kernel.KernelCatalog(MOTORES_CFG.kernel_bundle, MOTORES_CFG.kernel_verification)',
  '''_cluster_cfg = json.loads(Path(os.path.join(SERVE_DIR, 'iald_nucleo_fixo.json')).read_bytes()).get('active_cluster')
        if _cluster_cfg:
            KERNEL_EXTERNO = iald_kernel.KernelCatalog(_cluster_cfg['kernel_bundle'])
        else:
            KERNEL_EXTERNO = iald_kernel.KernelCatalog(MOTORES_CFG.kernel_bundle, MOTORES_CFG.kernel_verification)''')])
save(WORK/'code_pins.json',json.dumps(pins,indent=2).encode())
print('Staged',len(pins)+1,'modules')
