import pandas as pd

import youengine.settings

PRECISION = getattr(settings, "PRECISION", 8)

# init pandas settings
pd.set_option('precision', PRECISION)
pd.set_option('display.float_format', lambda x: '%.{}f'.format(PRECISION) % x)
