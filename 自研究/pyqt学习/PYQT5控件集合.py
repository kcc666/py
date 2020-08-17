from PyQt5.Qt import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("学习")
        self.resize(500,500)
        self.setup_ui()
    def setup_ui(self):
        # 按钮类
        self.ButtonType()
        self.InputType()

    def ButtonType(self):

        # 普通按钮
        普通按钮 = QPushButton(self)
        普通按钮.setText('普通按钮')
        普通按钮.move(10,0)

        # 命令链接按钮
        命令链接按钮 = QCommandLinkButton(self)
        命令链接按钮.setText('命令链接按钮')
        命令链接按钮.move(10,25)

        # 单选框
        单选框 = QRadioButton(self)
        单选框.setText("单选框按钮1")
        单选框.move(10, 70)

        单选框1 = QRadioButton(self)
        单选框1.setText("单选框按钮2")
        单选框1.move(110, 70)

        # 复选框
        复选框 = QCheckBox(self)
        复选框.setText("复选框按钮1")
        复选框.move(10, 90)

        # 复选框
        复选框1 = QCheckBox(self)
        复选框1.setText("复选框按钮2")
        复选框1.move(110, 90)

    def InputType(self):

        单行输入 = QLineEdit(self)
        单行输入.move(10,110)
        单行输入.setText("单行输入框")

        多行富文本输入 = QTextEdit(self)
        多行富文本输入.move(10,140)
        多行富文本输入.setText("<a href='www.baidu.com'>富文本输入</a>")
        多行富文本输入.resize(135,65)

        多行普通文本输入 = QPlainTextEdit(self)
        多行普通文本输入.setPlainText("普通多行文本")
        多行普通文本输入.move(10,210)
        多行普通文本输入.resize(135,65)

        快捷方式采集 = QKeySequenceEdit(self)
        快捷方式采集.move(10, 280)

        日期采集 = QDateTimeEdit(self)
        日期采集.move(10, 310)

        数字步长 = QSpinBox(self)
        数字步长.move(10, 340)

        组合框 = QComboBox(self)
        组合框.move(10, 370)

        字体组合框 = QFontComboBox(self)
        字体组合框.move(10,400)

        圆滑块 = QDial(self)
        圆滑块.move(200,0)

        条滑块 = QSlider(self)
        条滑块.move(300, 0)

        滚动条 = QScrollBar(self)
        滚动条.move(350, 0)

        日期对话框 = QCalendarWidget(self)
        日期对话框.move(200,100)

        lcd = QLCDNumber(self)
        lcd.move(200,300)

        



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    window = Window()
    window.show()


    sys.exit(app.exec_())