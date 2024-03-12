import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class MainWindow(QMainWindow):
    g_map: QLabel
    press_delta = 0.1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('main_window.ui', self)

        self.map_zoom = 5
        self.map_ll = [37.977751, 55.757718]
        self.map_l = 'map'
        self.map_key = ''

        self.refresh_map()

    def keyPressEvent(self, event):
        try:
            key = event.key()
            if key == Qt.Key_PageUp and self.map_zoom < 17:
                self.map_zoom += 1
            if key == Qt.Key_PageDown and self.map_zoom > 0:
                self.map_zoom -= 1
            if key == Qt.Key_Left:
                self.map_ll[0] -= self.press_delta
            if key == Qt.Key_Right:
                self.map_ll[0] += self.press_delta
            if key == Qt.Key_Up:
                self.map_ll[1] += self.press_delta
            if key == Qt.Key_Down:
                self.map_ll[1] -= self.press_delta

            self.refresh_map()
        except BaseException as e:
            print(e)


    def refresh_map(self):
        map_params = {
            "ll": f'{self.map_ll[0]},{self.map_ll[1]}',
            "l": self.map_l,
            'z': self.map_zoom,
        }
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get('https://static-maps.yandex.ru/1.x/',
                                params=map_params)
        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')

        self.g_map.setPixmap(pixmap)


def clip(a, b, c):
    if a < b:
        return b
    if a > c:
        return c
    return a


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
