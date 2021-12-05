import sys
import os
import csv
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget, QApplication
from PyQt5 import QtCore
import files_name

# QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

class FilesName(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.path = ""
        self.initUI()

    def initUI(self):
        self.ui = files_name.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('批量修改文件名小程序')
        self.method_fn()
        self.re_ledit()

    def re_ledit(self):
        self.ui.lineEdit.setText(self.path)

    def method_fn(self):
        self.ui.lineEdit.editingFinished.connect(self.l_edit_finish)
        self.ui.input_Button.clicked.connect(self.in_button)
        self.ui.names_Button.clicked.connect(self.fliesname)
        self.ui.out_Button.clicked.connect(self.changed_name)

    def l_edit_finish(self):
        l_edit = self.sender()
        self.path = l_edit.text()

    def in_button(self):
        dname = QFileDialog.getExistingDirectory(self, "选择文件夹", ".")
        self.path = dname
        self.re_ledit()

    def fliesname(self):
        files_l = [["文件类型(不可修改)", "原文件名(不可修改)", "修改后文件名（可使用多格修改,空为不修改）"]]
        try:
            fileslist = os.listdir(self.path)
            for i in fileslist:
                path = self.path+"/"+str(i)
                if os.path.isdir(path):
                    file_type_name = "文件夹"
                    file_name = i
                else:
                    file_name, file_type_name = os.path.splitext(i)
                files_l.append([file_type_name, file_name, ""])
            with open(self.path+"/FliesName.csv", "w") as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerows(files_l)
            QMessageBox.about(
                self, '成功', "成功获取目录下文件名称列表，\n请修改文件夹下FliesName.csv文件")
            os.startfile(self.path)
        except:
            QMessageBox.warning(self, "错误", "路径错误请从新填写")

    def changed_name(self):
        try:
            with open(self.path+"/FliesName.csv", "r") as f:
                files_l = csv.reader(f)
                for i, row in enumerate(files_l):
                    new_name = ''.join(row[2:])
                    if i == 0:
                        continue
                    elif new_name == "":
                        continue
                    else:
                        try:
                            new_name += row[0]
                            os.rename(
                                f"{self.path}/{row[1]+row[0]}", f"{self.path}/{new_name}")
                        except:
                            pass
                QMessageBox.about(self, '成功', "批量修改文件名成功")
        except:
            QMessageBox.warning(self, "错误", "FliesName.csv读取错误")


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    files = FilesName()
    files.show()
    sys.exit(app.exec())
