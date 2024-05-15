

import os

CI_ENV = bool(os.getenv("CI", default="false") == "true")


TEST_DIRPATH = os.path.join(os.path.dirname(__file__), "test")
MOCK_EXPORTS_DIRPATH = os.path.join(TEST_DIRPATH, "mock_exports")
