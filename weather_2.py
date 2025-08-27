import sys
import requests
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLineEdit, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from requests import RequestException


class Weather(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter a city",self)
        self.emoji_label = QLabel(self)
        self.temperature_label = QLabel(self)
        self.pushButton = QPushButton("Enter",self)
        self.input_text = QLineEdit(self)
        self.weather_text = QLabel(self)
        self.setWindowIcon(QIcon("happy_sun.png"))
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather app")
        self.setGeometry(300, 300, 300, 300)

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.input_text)
        vbox.addWidget(self.pushButton)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.weather_text)

        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.input_text.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.weather_text.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName('city_label')
        self.emoji_label.setObjectName('emoji_label')
        self.temperature_label.setObjectName('temperature_label')
        self.weather_text.setObjectName('weather_text')
        self.input_text.setObjectName('input_text')

        self.setStyleSheet("""
            QLabel {
                font-family: Calibri;
                font-size: 25px;
            }

            QLabel#emoji_label {
                font-size: 125px;
                font-family: Segoe UI emoji;
            }

            QLabel#temperature_label {
                font-size: 75px;
            }

            QLineEdit#input_text {
                font-family: Calibri;
                font-size: 20px;
            }
            
            QLabel#weather_text {
                font-size: 75px;
            }
            
            QLabel#city_label {
                font-size: 50px;
            }
            """)

        self.pushButton.clicked.connect(self.get_weather)



    def get_weather(self):
        api_key = "e362b848b39fdd7cd5faecfc5a321aea" #my personal key
        city = self.input_text.text() #we get the text that we entered in input
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}" #api creates request

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.show_weather(data)
            else:
                print(data)
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nPlease check input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess Denied")
                case 404:
                    self.display_error("Not found:\nPlease check input")
                case 500:
                    self.display_error("Internal server:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error("Server returned an error")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nPlease check your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout error:\nThe request timed out")

        except requests.exceptions.RequestException:
            self.display_error("Unknown error:\nPlease check your internet connection")


    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size: 25px;")
        self.temperature_label.setText(message)

    def show_weather(self,data):
        temperature_c = data["main"]["temp"] - 273.15
        self.temperature_label.setStyleSheet("font-size: 25px;")
        self.temperature_label.setText(f"{temperature_c:.0f}°C")

        weather_description = data["weather"][0]["description"]
        self.weather_text.setStyleSheet("font-size: 25px;")
        self.weather_text.setText(weather_description)

        weather_id = data["weather"][0]["id"]
        self.emoji_label.setText(self.get_weather_emoji(weather_id))

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "🌩"  # grmljavina
        elif 300 <= weather_id <= 321:
            return "🌦"  # sitna kiša
        elif 500 <= weather_id <= 531:
            return "🌧"  # kiša
        elif 600 <= weather_id <= 622:
            return "❄"  # sneg
        elif 700 <= weather_id <= 741:
            return "💨"  # magla/vetar
        elif weather_id == 762:
            return "🌋"  # vulkan
        elif weather_id == 781:
            return "🌪"  # tornado
        elif weather_id == 800:
            return "☀"  # vedro
        elif 801 <= weather_id <= 804:
            return "☁"  # oblačno
        else:
            return "❓"





if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Weather()
    w.show()
    sys.exit(app.exec_())