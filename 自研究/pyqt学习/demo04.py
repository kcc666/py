from PyQt5.Qt import *
import sys


# 基本结构
app = QApplication(sys.argv)

# 创建窗口
window = QWidget()
# 设置窗口标题
window.setWindowTitle("kcc")
# 设置窗口大小
window.resize(500,500)
# 设置窗口位置
window.move(400,200)


# 创建标签,并把它放入window窗口
label = QLabel(window)
# 设置标签文字
label.setText("Hello kcc")
# 设置标签位置
label.move(200,200)
# 显示窗口
window.show()
# 基本结构
sys.exit(app.exec())
