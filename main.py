from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QDate
from PyQt5.uic import loadUi
from covid import getCovid
import sys
import datetime

class Form(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('form.ui', self)

        # python 날짜 -> QDate -> QDateEdit
        t = datetime.datetime.now()
        qdt = QDate(t.year, t.month, t.day)
        self.dt.setDate(qdt)

        self.clickBtn()

        self.btn.clicked.connect(self.clickBtn)


    def clickBtn(self):
        qdt = self.dt.date()
        dt = qdt.toString('yyyyMMdd')

        info = getCovid(dt)
        self.initTable(info)


    def initTable(self, info):
        # table 초기화
        col = len(info[0])
        row = len(info)

        self.table.setColumnCount(col)
        self.table.setRowCount(row)

        label = ('날짜', '사망자 수', '누적 확진자 수', '지역', '확진자 수', '격리 해제 수', '격리중', '지역발생 수', '해외유입 수', '발생률(10만명당)')

        self.table.setHorizontalHeaderLabels(label)

        # table 데이터 추가하기
        for r in range(row):
            for c in range(col):
                item = QTableWidgetItem(info[r][c])
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(r, c, item)

        self.table.setAlternatingRowColors(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
