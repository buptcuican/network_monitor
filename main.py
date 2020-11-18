import NetworkMonitor
import sys
from PyQt5.Qt import QApplication


if __name__ == '__main__':
    #创建应用程序和对象
    app = QApplication(sys.argv)
    ex = NetworkMonitor.NM()
    sys.exit(app.exec_())
