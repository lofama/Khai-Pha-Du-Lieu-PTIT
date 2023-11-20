import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = 'D:/KPDL/envs/env_name/Library/plugins'
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('PyQt5 Test')
window.show()
sys.exit(app.exec_())
