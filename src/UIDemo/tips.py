import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication
from PyQt5.QtGui import QIcon, QFont

# 如何设置提示，本例为给按钮设置提示
class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()  # 界面绘制交给InitUi方法

    def initUI(self):
        # 这种静态的方法设置一个用于显示工具提示的字体。我们使用10px滑体字体。
        QToolTip.setFont(QFont('SansSerif', 10))
        # 创建一个PushButton并为他设置一个tooltip
        btn = QPushButton('Button', self)
        # 创建一个提示，我们称之为settooltip()方法。我们可以使用丰富的文本格式
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        # btn.sizeHint()显示默认尺寸
        btn.resize(btn.sizeHint())
        # 移动窗口的位置 相对于窗口的位置
        btn.move(50, 50)


        # 设置窗口的位置和大小
        self.setGeometry(300, 300, 300, 220)
        # 设置窗口的标题
        self.setWindowTitle('Network Speed Monitor V1.0')
        # 设置窗口的图标，引用当前目录下的web.png图片
        self.setWindowIcon(QIcon('resources/img/appicon.png'))
        # 显示窗口
        self.show()


if __name__ == '__main__':
    #创建应用程序和对象
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
