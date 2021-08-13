from os import path

'''width and height'''
WIDTH = 1000
HEIGHT = 700

'''environment data'''
FPS = 30
ceiling = 600
finish_line = 20000

'''color'''
BLACK = "#000000"
WHITE = "#ffffff"
RED = "#ff0000"
YELLOW = "#ffff00"
GREEN = "#00ff00"
GREY = "#8c8c8c"
BLUE = "#0000ff"
LIGHT_BLUE = "##21A1F1"

'''object size'''
car_size = (60, 30)
coin_size = (30,31)
lane_size = (20,3)

'''command'''
LEFT_cmd = "MOVE_LEFT"
RIGHT_cmd = "MOVE_RIGHT"
SPEED_cmd = "SPEED"
BRAKE_cmd = "BRAKE"

'''data path'''
ASSET_IMAGE_DIR = path.join(path.dirname(__file__), "../asset/image")
IMAGE_DIR = path.join(path.dirname(__file__), 'image')
SOUND_DIR = path.join(path.dirname(__file__), 'sound')
BACKGROUND_IMAGE = ["ground0.jpg"]
COIN_IMAGE = "logo.png"
RANKING_IMAGE = ["info_coin.png", "info_km.png"]

START_LINE_IMAGE = ["start.png", "finish.png"]
# FINISH_LINE_IMAGE =
USER_IMAGE = [["car1.png","car1-bad.png"],["car2.png","car2-bad.png"],
              ["car3.png","car3-bad.png"], ["car4.png","car4-bad.png"]]
COMPUTER_CAR_IMAGE = ["computer_car.png","computer_die.png"]
USER_COLOR = [WHITE, YELLOW, BLUE, RED]

'''image url'''
COMPUTER_CAR_URL = "https://raw.githubusercontent.com/yen900611/RacingCar/master/game/image/computer_car.png"
USER_CAR_URL = ["https://github.com/yen900611/RacingCar/blob/master/game/image/car1.png?raw=true",
                "https://github.com/yen900611/RacingCar/blob/master/game/image/car2.png?raw=true",
                "https://github.com/yen900611/RacingCar/blob/master/game/image/car3.png?raw=true",
                "https://github.com/yen900611/RacingCar/blob/master/game/image/car4.png?raw=true"]
BACKGROUND_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/ground0.jpg?raw=true"
INFO_COIN_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/info_coin.png?raw=true"
INFO_KM_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/info_km.png?raw=true"
FINISH_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/finish.png?raw=true"
START_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/start.png?raw=true"
COIN_URL = "https://github.com/yen900611/RacingCar/blob/master/game/image/logo.png?raw=true"



