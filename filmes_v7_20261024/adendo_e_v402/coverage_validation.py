"""Validate the recorded 1 Hz opaque-object mask, not encoded-video pixels."""
import math

def validate_samples(kind, metadata, rows, timeline_duration):
 duration=metadata['duration'];fps=metadata['fps'];total=metadata['total']
 assert isinstance(duration,(int,float)) and math.isfinite(duration) and duration>0 and duration==int(duration)
 assert fps==60 and total==duration*fps and metadata['startTime']==0
 assert metadata['kind']==kind and len(rows)==int(duration)
 for index,row in enumerate(rows):
  # studio.mjs maps the 16-second loop to one 24-second geometric cycle.
  expected_time=index*fps/(total-1)*24 if kind=='loop' else float(index)
  t=row['time'];width=row['width_fraction']
  assert type(t) in (int,float) and math.isfinite(t) and math.isclose(t,expected_time,rel_tol=0,abs_tol=1e-12)
  assert type(width) in (int,float) and math.isfinite(width) and 0<=width<=1
  assert row['film']==metadata['film']
  expected_transition=t<2 or t>timeline_duration-3
  assert type(row['transition']) is bool and row['transition']==expected_transition
  if not expected_transition:assert width>=.6
 active=[r for r in rows if not r['transition']]
 assert active
 return {'samples':len(rows),'minimum_width_fraction':min(r['width_fraction'] for r in active),
  'method':'Recorded opaque-object mask at 480x270, sampled once per encoded second; not a pixel audit of the MP4.',
  'timestamp_grid':'24-second geometric cycle sampled over 16-second loop' if kind=='loop' else 'Integer seconds from zero',
  'transition_mask_verified':True,'all_widths_finite':True}
