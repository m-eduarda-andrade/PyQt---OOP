from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QMainWindow, QApplication
import pyqtgraph as pg  # PyQtGraph nach Qt importieren
from numpy.random import randint


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("w")
        self.setCentralWidget(self.plot_widget)
        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        self.plot_widget.setBackground("w")  # r, g, b, c, m, y, k
        self.plot_widget.setBackground("#1457f8")  # hex
        self.plot_widget.setBackground((100, 50, 255))  # RGB

        # default Fenster Hintergrundfarbe
        color = self.palette().color(QPalette.Window)
        self.plot_widget.setBackground(color)  # Ein QColor

        # plot data: x, y Werte
        self.plot_widget.plot(hour, temperature)


        # self.plot_widget.clear()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_widget = pg.PlotWidget()
        self.setCentralWidget(self.plot_widget)
        self.plot_widget.setYRange(0, 50)

        self.x = list(range(100))
        self.y = [randint(0, 100) for _ in range(100)]

        self.data_curve = self.plot_widget.plot(self.x, self.y, pen=pg.mkPen(width=4))

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)
        self.y = self.y[1:]
        self.y.append(randint(0, 100))

        self.data_curve.setData(self.x, self.y)


if __name__ == "__main__":
    app = QApplication([])
    window = Main()
    window.show()
    app.exec_()


