"""Exercise installed tool implementations against staged and prior public data."""
import json
from pathlib import Path
from time import perf_counter
import sys

from verify_installed import W, R, offline_loader_guard

def measure(label, manifest):
    from iald_kernel import KernelCatalog
    from iald_core_indexado import execute_tool
    cluster = json.loads(manifest.read_bytes())['active_cluster']
    start = perf_counter()
    kernel = KernelCatalog(cluster['kernel_bundle'], cluster['kernel_verification'])
    load_seconds = perf_counter() - start
    symbol = 'p_igual_np_nas_classes_do_dicionario'
    measurements = []
    for q in (symbol, 'P = nP nas classes do dicionário', 'projetor núcleo palavra polinomial'):
        start = perf_counter()
        hits = kernel.search(q,limit=5)['results']
        measurements.append({'query':q,'elapsed_s':round(perf_counter()-start,3),
                             'paths':[r['path'] for r in hits],
                             'decl_and_scope': any('theorem '+symbol in r['excerpt']['text']
                                                    and 'Turing' in r['excerpt']['text'] for r in hits)})
    # A full exact reading independently verifies what was recovered in a search.
    path = 'TGLExt/PIgualNP.lean'
    theorem = path in kernel.records
    scope = False
    if theorem:
        ref = json.loads((W/'app/KERNEL_HIGHLIGHTS.json').read_bytes())
        anchor = next(a for a in ref['anchors'] if a['symbol'].endswith('.'+symbol))
        paragraph = kernel.read_file(path, anchor['lines'][0]-4, 10)['text']
        scope = 'theorem '+symbol in paragraph and 'Turing' in paragraph and '[OPEN]' in paragraph
    start = perf_counter()
    hits = execute_tool(manifest,'search_tgl',{'query':symbol,'limit':5})['results']
    article = []
    for r in hits:
        read = execute_tool(manifest,'fetch_tgl',{'id':r['id'],'offset':r['offset'],'max_chars':4500})
        article.append({'document':r['id'],'symbol':symbol in read['text'],'pinned':read['sha256']==r['sha256']})
    return {'label':label,'release':cluster['release'],'kernel_files':len(kernel.records),
            'construction_seconds':round(load_seconds,3),'searches':measurements,
            'file_in_catalog':theorem,'declaration_and_Turing_scope':scope,
            'public_articles_search_and_fetch':article,'documents_probe_seconds':round(perf_counter()-start,3)}

def main():
    attempts = offline_loader_guard()
    results = [measure('baseline',R/'iald_nucleo_fixo.json'),
               measure('candidate', W/'app/science/memory_stage/manifest_staged.json')]
    assert all(v['pinned'] for row in results for v in row['public_articles_search_and_fetch'])
    target = W / 'RETRIEVAL_COMPARISON.json'
    with target.open('x',encoding='utf-8') as out:
        json.dump({'results':results,'audit':attempts,'scope':'Local retrieval, without answer generation.'},out,ensure_ascii=False,indent=2)
    print([(r['release'],r['declaration_and_Turing_scope'],[q['decl_and_scope'] for q in r['searches']]) for r in results])
    assert results[1]['declaration_and_Turing_scope'] and any(r['symbol'] for r in results[1]['public_articles_search_and_fetch'])

if __name__ == '__main__':
    main()
