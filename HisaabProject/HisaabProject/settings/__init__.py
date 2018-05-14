'''
Hisaab App to Handle the Hisaab-Kitab of the
NavGurukul for better use of Donor's Money

'''

from .base import *
from .production import *
try:
    from .local import *
except:
    pass
