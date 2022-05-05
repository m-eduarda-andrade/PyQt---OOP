from PyQt5 import QtWidgets as qtw

# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

# instanciando um objeto
app = qtw.QApplication([])

# Ein Qt Widget anlegen, es wird unser Fenster sein
window = qtw.QPushButton("Click me")

# Wichtig: Fenster sind defaultmaessig ausgeblendet
window.show()

# Ereignisschleife (event loop) starten
app.exec_()

# Dieser Bereich wird nur erreicht nachdem
# die Anwendung beendet ist
