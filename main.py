from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QLabel, QHBoxLayout, QHeaderView
from PyQt5.QtCore import Qt, QDate
from PyQt5.uic import loadUi
from covid import getCovid
import sys
import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# matplotlib 한글 폰트
path = 'C:/windows/Fonts/malgun.ttf'
font = fm.FontProperties(fname=path, size=8).get_name()
plt.rc('font', family=font)

#QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class Form(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('form.ui', self)
        self.setWindowTitle('코로나')
        self.setFixedSize(1600, 800)

        # python 날짜 -> QDate -> QDateEdit
        t = datetime.datetime.now()
        qdt = QDate(t.year, t.month, t.day)
        self.dt.setDate(qdt)

        # 차트 컨트롤 widget에 붙이기
        hbox = QHBoxLayout()
        label = QLabel('항목선택')
        self.cmb = QComboBox()
        hbox.addWidget(label)
        hbox.addWidget(self.cmb)

        self.fig = plt.Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.canvas)
        self.gb.setLayout(vbox)

        self.clickBtn()

        self.btn.clicked.connect(self.clickBtn)
        self.cmb.currentIndexChanged.connect(self.cmbChanged)


    def cmbChanged(self, idx):
        self.initChart(self.info, idx)


    def clickBtn(self):
        qdt = self.dt.date()
        dt = qdt.toString('yyyyMMdd')

        self.info = getCovid(dt)
        self.initTable(self.info)
        self.initChart(self.info)


    def initTable(self, info):
        # table 초기화
        label = ('날짜', '사망자 수', '누적 확진자 수', '지역', '확진자 수', '격리 해제 수', '격리중', '지역발생 수', '해외유입 수', '발생률(10만명당)')

        # 콤보박스 초기화
        content = [v for k, v in enumerate(label) if k!=0 and k!=3]
        self.cmb.addItems(content)
        self.cmb.setCurrentIndex(2)

        if info:
            col = len(info[0])
            row = len(info)
        else:
            col = len(label)
            row = 0
        
        self.table.setColumnCount(col)
        self.table.setRowCount(row)


        self.table.setHorizontalHeaderLabels(label)

        # table 데이터 추가하기
        for r in range(row):
            for c in range(col):
                item = QTableWidgetItem(info[r][c])
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(r, c, item)

        self.table.setAlternatingRowColors(True)
        h = self.table.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.Stretch)


    def initChart(self, info, idx=2):
        c = ('darkred', 'orange', 'gold', 'forestgreen', 'royalblue', 'navy', 'slateblue', 'pink')
        c = c[idx]
        self.fig.clear()
        # 콤보박스 항목설정 인덱스 맞추기
        if idx <= 1:
            idx += 1
        else:
            idx += 2

        if idx != 9:
            info = info[:-1]

        x = [v[3] for v in info]
        y = [float(v[idx]) for v in info]


        ax = self.fig.subplots()
        ax.bar(x, y, color=c)
        ax.grid(True, which='major', axis='y', color='gray', linestyle='--')
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())
