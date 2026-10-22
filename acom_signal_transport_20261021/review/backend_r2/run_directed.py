import sitecustomize
import json,unittest
from pathlib import Path
from test_backend import Routes
names=['test_trusted_public_https_behind_http_proxy','test_forwarded_headers_cannot_grant_origin','test_outer_parser_scope_is_explicit','test_old_query_name_not_negotiated_duplicate_query_not_negotiated','test_missing_trusted_callback_fails_closed','test_cookie_missing_origin_refused','test_cookie_cross_site_refused','test_pages_exact_cursor_scope_and_plain_clients']
r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Routes(n) for n in names))
report={'status':'PASS' if r.wasSuccessful() else 'BLOCK','tests':r.testsRun,'names':names,'errors':[(str(t),s) for t,s in r.errors],'failures':[(str(t),s) for t,s in r.failures],'scope':'Only changed R2 controls; byte-identical isolated sources; no full codec regression rerun.'}
(Path(__file__).parent/'REVIEW_TEST_RESULTS.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
raise SystemExit(0 if r.wasSuccessful() else 1)
