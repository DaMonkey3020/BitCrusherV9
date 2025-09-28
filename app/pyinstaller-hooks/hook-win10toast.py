# Ensures win10toast metadata import doesn’t break frozen app
from PyInstaller.utils.hooks import copy_metadata
datas = []
try:
    datas += copy_metadata('win10toast')
except Exception:
    pass
