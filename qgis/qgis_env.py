import os
import sys

QGIS_BASE = r"C:\Program Files\QGIS 3.40.12"

QGIS_BIN = os.path.join(QGIS_BASE, "bin")
QGIS_APP = os.path.join(QGIS_BASE, "apps", "qgis")
QGIS_PYTHONPATH = os.path.join(QGIS_BASE, "apps", "qgis", "python")
QT_PLUGINS = os.path.join(QGIS_BASE, "apps", "Qt5", "plugins")

os.environ["PATH"] = f"{QGIS_BIN};{os.path.join(QGIS_BASE, 'apps', 'qgis', 'bin')};{os.environ.get('PATH', '')}"
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QT_PLUGINS
os.environ["GDAL_DATA"] = os.path.join(QGIS_BASE, 'apps', 'gdal', 'share', 'gdal')
os.environ["PROJ_LIB"] = os.path.join(QGIS_BASE, 'apps', 'PROJ', 'share', 'proj')

if QGIS_PYTHONPATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHONPATH)
QGIS_PLUGINS=os.path.join(QGIS_PYTHONPATH, 'plugins')
if QGIS_PLUGINS not in sys.path:
    sys.path.insert(1, QGIS_PLUGINS)

from qgis.core import QgsApplication

global_qgs_app = QgsApplication([], False)
global_qgs_app.setPrefixPath(QGIS_APP, True)
global_qgs_app.initQgis()

def exitQgis():
    global_qgs_app.exitQgis()