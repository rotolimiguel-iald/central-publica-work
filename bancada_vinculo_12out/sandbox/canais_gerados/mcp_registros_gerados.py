# -*- coding: utf-8 -*-
"""mcp_registros_gerados.py -- GERADO por gerar_canais_mcp.py (CANAIS_v391 ddd46f9be8bad589). Uma ferramenta por registro selado; cada uma
chama GET /api/registro/<nome> na Bancada (que confere a identidade e os hashes). NAO EDITAR A MAO."""
import json, os, urllib.request
from mcp.server.fastmcp import FastMCP
URL = os.environ.get("BANCADA_UM_URL", "http://127.0.0.1:18777")
mcp = FastMCP("bancada-um-registros")


def _req(caminho):
    try:
        with urllib.request.urlopen(URL + caminho, timeout=120) as f:
            return json.loads(f.read().decode("utf-8"))
    except Exception as e:
        return dict(erro="Bancada Um fora do ar ou recusou: %r" % (e,))


@mcp.tool(description='As Fases 5, 6 e 7 da Bancada Um, o banco de GW e as erratas ao lado, lidos por hash do cache do rito (v380).')
def registro_bancada_fases_5_6_7_v380() -> dict:
    """Leitura por hash do registro selado bancada_fases_5_6_7_v380 (v391). Nunca recalcula; gate NONE."""
    return _req('/api/registro/bancada_fases_5_6_7_v380')


if __name__ == "__main__":
    mcp.run()
