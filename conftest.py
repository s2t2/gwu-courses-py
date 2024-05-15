

import os


CI_ENV = bool(os.getenv("CI", default="false") == "true")


TEST_DIRPATH = os.path.join(os.path.dirname(__file__), "test")

MOCK_EXPORTS_DIRPATH = os.path.join(TEST_DIRPATH, "mock_exports")
MOCK_DMAP_DIRPATH = os.path.join(TEST_DIRPATH, "mock_dmap")

DASHBOARD_1_FILEPATH = os.path.join(MOCK_DMAP_DIRPATH, "dashboard-1-redacted.mhtml")
DASHBOARD_2_FILEPATH = os.path.join(MOCK_DMAP_DIRPATH, "dashboard-2-redacted.mhtml")
