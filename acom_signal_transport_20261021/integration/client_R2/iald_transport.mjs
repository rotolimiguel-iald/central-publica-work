// Browser-only integration. The pinned codec owns the wire format.
import {PROTOCOL,CODEC,QUERY,IDENTITY_PAGE_LIMIT,codecAvailable,prepareRequest,
        decodePage,identityPageJSON,WireError} from './chat_wire_codec.mjs';

async function boundedResponse(response) {
  if (!response.body?.getReader) throw new WireError('response_stream_unavailable');
  const reader=response.body.getReader(), parts=[];
  let size=0;
  try {
    while (true) {
      const {value,done}=await reader.read();
      if (done) break;
      size+=value.byteLength;
      if (size>IDENTITY_PAGE_LIMIT) throw new WireError('page_wire_limit');
      parts.push(value);
    }
  } catch (error) {
    try { await reader.cancel(error); } catch {}
    throw error;
  } finally { reader.releaseLock(); }
  const raw=new Uint8Array(size);
  let offset=0;
  for (const part of parts) { raw.set(part,offset); offset+=part.byteLength; }
  return raw;
}

export async function createSessionTransport(session) {
  const cap=session?.transport;
  if (cap?.protocol!==PROTOCOL || cap.codec!==CODEC || cap.bases!==false ||
      cap.query!==QUERY || !await codecAvailable()) return null;
  // Session data is scoped by the existing authenticated account check.
  const snapshot={account:session.account,transport:{...cap}};
  return Object.freeze({
    query:QUERY,
    prepare:raw=>prepareRequest(raw,snapshot),
    async readPage(response,binding) {
      const wire=await boundedResponse(response);
      const raw=await decodePage(wire,snapshot.account,binding);
      return identityPageJSON(raw);
    },
  });
}
