"""Exercise the actual stdio protocol using read-only tools, without model calls."""
import asyncio
import json
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

async def main():
    base=Path(__file__).resolve().parent
    transport=PythonStdioTransport(str(base/'mcp_server.py'),python_cmd=r'C:\Python314\python.exe',cwd=str(base))
    async with Client(transport) as client:
        listing=await client.list_tools()
        result=await client.call_tool('iald_selection_preview',{'task':'Calcule 2 + 2.'})
        data=result.data
        assert data['selected'] in ('local','codex','claude')
        print(json.dumps({'tools':[t.name for t in listing], 'selected':data['selected'], 'status':data['status']},ensure_ascii=False))

if __name__=='__main__':
    asyncio.run(main())
