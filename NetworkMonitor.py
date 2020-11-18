import sys
import os
import time
from psutil import net_io_counters
from threading import Thread
from PyQt5.QtGui import *
from PyQt5.Qt import *


# 网络数据读取+格式化
# return: [receiveBytes/s, sendBytes/s]
def getNetworkSpeed():
    netInfoBefore = []
    netInfoAfter = []
    # 获取流量统计信息 后-前 = 结果
    # 前
    networkInfo = net_io_counters()
    receiveBytes = networkInfo.bytes_recv
    sendBytes = networkInfo.bytes_sent
    netInfoBefore.append(receiveBytes)
    netInfoBefore.append(sendBytes)
    # 等一秒的积累
    time.sleep(1)
    # 后
    networkInfo = net_io_counters()
    receiveBytes = networkInfo.bytes_recv
    sendBytes = networkInfo.bytes_sent
    netInfoAfter.append(receiveBytes)
    netInfoAfter.append(sendBytes)
    # 出结果
    info = []
    for i in range(2):
        info.append(netInfoAfter[i] - netInfoBefore[i])
    return info


def networkSpeedFormat(speed):
    if speed < 1024:
        return "%.2f B/s" % speed
    speed >>= 10
    if speed < 1024:
        return "%.2f KB/s" % speed
    speed >>= 10
    if speed < 1024:
        return "%.2f MB/s" % speed
    speed >>= 10
    return "%.2f GB/s" % speed
# 网络数据读取+格式化end


#生成资源文件目录访问路径 为了打包之后仍能运行
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class NM(QWidget):
    sendText = None
    receiveText = None
    totalText = None
    uploadIcon = None
    downloadIcon = None
    all_bytes = 0


    def __init__(self):
        super().__init__()

        # 界面绘制交给InitUi方法
        self.initUI()
        # 启动获取网络信息方法
        self.start()

    def initUI(self):
        #窗口设置
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        # 使用 网格布局
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # 初始化文本组件
        self.sendText = QLabel("上传：")
        self.receiveText = QLabel("下载：")
        self.totalText = QLabel("流量使用总量：")
        self.uploadIcon = QLabel("")
        self.downloadIcon = QLabel("")
        uploadImg = QPixmap(resource_path(os.path.join("resources/img", "upload.png")))
        downloadImg = QPixmap(resource_path(os.path.join("resources/img", "download.png")))
        self.uploadIcon.setPixmap(uploadImg)
        self.downloadIcon.setPixmap(downloadImg)

        # 设置文本对齐方式
        self.totalText.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)

        # 设置文本位置
        grid_layout.addWidget(self.uploadIcon, 0, 0, 1, 1)
        grid_layout.addWidget(self.sendText, 0, 1, 1, 3)
        grid_layout.addWidget(self.downloadIcon, 1, 0, 1, 1)
        grid_layout.addWidget(self.receiveText, 1, 1, 1, 3)
        grid_layout.addWidget(self.totalText, 2, 0, 1, -1)

        grid_layout.setRowStretch(0, 0)

        # 设置窗口的位置和大小
        self.setGeometry(300, 300, 160, 100)
        # 设置窗口的标题
        self.setWindowTitle('网速监控V1.0')
        # 设置窗口的图标
        self.setWindowIcon(QIcon(resource_path(os.path.join("resources/img", "icon.png"))))
        # 禁用窗口尺寸变化
        self.setFixedSize(self.width(), self.height())
        # 显示窗口
        self.show()

    # 调用网络信息方法
    def setSpeed(self):
        while True:
            info = getNetworkSpeed()
            recv_bytes_str = networkSpeedFormat(info[0])  # 每秒接收的字节
            sent_bytes_str = networkSpeedFormat(info[1])  # 每秒发送的字节
            self.all_bytes += sum(info)
            if self.all_bytes < 1073741824:
                all_bytes = self.all_bytes / 1048576
                total_bytes_str = "%.2f Mb" % all_bytes
            else:
                all_bytes = self.all_bytes / 1073741824
                total_bytes_str = "%.2f Gb" % all_bytes
            # 设置 显示数值的文本
            self.sendText.setText("上传：" + sent_bytes_str)
            self.receiveText.setText("下载：" + recv_bytes_str)
            self.totalText.setText("流量使用总量：" + total_bytes_str)

    # 启动方法
    def start(self):
        Thread(target=self.setSpeed, daemon=True).start()


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
