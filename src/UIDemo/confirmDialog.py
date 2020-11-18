import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMessageBox
from PyQt5.QtGui import QIcon, QFont

# 默认情况下,如果我们单击x按钮窗口就关门了。有时我们想修改这个默认的行为。例如我们在编辑器中修改了一个文件,
# 当关闭他的时候，我们显示一个消息框确认。
class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()  # 界面绘制交给InitUi方法

    def initUI(self):
        # 设置窗口的位置和大小
        self.setGeometry(300, 300, 300, 220)
        # 设置窗口的标题
        self.setWindowTitle('Network Speed Monitor V1.0')
        # 设置窗口的图标，引用当前目录下的web.png图片
        self.setWindowIcon(QIcon('resources/img/appicon.png'))
        # 显示窗口
        self.show()
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    #创建应用程序和对象
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
