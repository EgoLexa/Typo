#!/usr/bin/python
"""
Simple app for typing exercises
"""
import typo_ui
import sys
import time
import random
from PyQt5 import QtWidgets


class TypoApp(QtWidgets.QMainWindow, typo_ui.Ui_MainWindow):
    def __init__(self, texts, stat_entries_number):
        super().__init__()
        self.setupUi(self)  # design initialization
        self.stat_len = stat_entries_number
        self.statButton.setEnabled(self.stat_len > 10)
        self.statButton.clicked.connect(self.show_statistics)
        self.NextButton.clicked.connect(self.set_source_text)
        self.ResetButton.clicked.connect(self.reset)
        self.TargetText.textChanged.connect(self.update_cpm)
        self.txt = texts
        self.log = []
        self.cpm_str = self.label_cpm.text()
        self.typos_str = self.label_typos.text()
        self.start_time = time.time()
        self.stop_time = time.time()
        self.err = 0
        self.typed = 0
        self.add_to_log = False
        self.log_string = ''

    def set_source_text(self):
        if self.add_to_log:
            self.log.append(self.log_string)
            self.stat_len+= 1
        self.SourceText.setPlainText(random.choice(self.txt))
        self.statButton.setEnabled(self.stat_len > 10)
        self.reset()

    def reset(self):
        self.label_err.setText('Start typing.')
        self.label_typos.setText(self.typos_str)
        self.label_cpm.setText(self.cpm_str)
        self.start_time = time.time()
        self.err = 0
        self.TargetText.clear()
        self.TargetText.setFocus()

    def show_statistics(self):
        with open("stats.csv", "a") as f:
            f.writelines( self.log )
        self.log = []
        import stats
        stats.show()

    def update_cpm(self):
        t_txt = self.TargetText.toPlainText()
        source_txt = self.SourceText.toPlainText()
        tt_len = len(t_txt)
        if tt_len > 30: self.add_to_log = True
        else: self.add_to_log = False
        if tt_len < self.typed:
            self.typed=tt_len
            self.label_err.setText('')
            return
        if tt_len > len(source_txt): return
        if tt_len < 2:
            self.label_cpm.setText(self.cpm_str)
            self.label_typos.setText(self.typos_str)
            self.start_time = time.time()
            if source_txt[:tt_len]==t_txt:
                self.err = 0
            else: self.err = 1
            return
        s_txt = source_txt[:tt_len]
        if s_txt[-1] == t_txt[-1]:
            err_str = ''
        else:
            err_str = f'Typo:  {t_txt[-1]} <=> {s_txt[-1]}'
            self.err = self.err + 1
        self.stop_time = time.time()
        ep = round(100 * self.err / tt_len, ndigits=2)
        cpm = round(12 * tt_len / (self.stop_time - self.start_time), ndigits=1)
        self.label_cpm.setText(self.cpm_str + str(cpm))
        self.label_typos.setText(self.typos_str + f' {self.err}  ( {ep}% )')
        self.label_err.setText(err_str)
        self.typed = tt_len
        self.log_string = f"{round(time.time(), ndigits=1)},{cpm},{ep},{float(tt_len)}\n" # .csv format string

    def closeEvent(self, event):
        if self.add_to_log: self.log.append(self.log_string)
        with open("stats.csv", "a") as f:
            f.writelines( self.log )
        super().closeEvent(event)

if __name__ == '__main__':
    table = {8216:39, 8217:39, 8220:34, 8221:34, 8211:45, 8212:45, 8230:95}
    try:
        with open("lines.txt", "r") as file:
            text = [line.translate(table).strip() for line in file if len(line)>40]
    except IOError:
        text = ["The file comprising training text lines (lines.txt) should be in your working directory"]
    print(f'\033[34m number of lines: \033[0m{len(text)}')

    try:
        with open("stats.csv", "r") as file:
            stats_len = len(file.readlines()) - 1
    except IOError:
        stats_len = 0
        with open("stats.csv", "w") as file:
            file.write("time,Words per minute,Typos percentage,len_txt\n") # .csv header

    t = time.time()
    random.seed(int((t - int(t))*1000))
    app = QtWidgets.QApplication(sys.argv)
    window = TypoApp(text, stats_len)
    window.SourceText.setPlainText(random.choice(text))
    window.show()
    sys.exit(app.exec_())
