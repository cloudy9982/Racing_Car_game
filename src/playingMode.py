from .car import *
from .highway import *
from .gameMode import GameMode
from .env import *
import pygame
import random


class PlayingMode(GameMode):
    def __init__(self, user_num: int, car_num, sound_controller):
        super(PlayingMode, self).__init__()
        self.frame = 0
        pygame.font.init()
        self.cars_num = car_num

        '''set groups'''
        self.users = pygame.sprite.Group()
        self.cars = pygame.sprite.Group()
        self.computerCars = pygame.sprite.Group()
        self.lanes = pygame.sprite.Group()
        self.traffic_cones = pygame.sprite.Group()
        self.camera = Camera()

        '''sound'''
        self.sound_controller = sound_controller

        '''image'''
        self.bg_image = pygame.Surface((2000, HEIGHT))
        self.cars_info = []
        self.user_distance = []
        self.maxVel = 0
        self._init_lanes()
        # user數量
        for user in range(user_num):
            self._init_user(user)
        self.eliminated_user = []
        self.winner = []
        '''
        status incloud "GAME_ALIVE"、"GAME_PASS"、"GAME_OVER"
        '''
        self.status = "GAME_ALIVE"
        if user_num == 1:
            self.is_single = True
        else:
            self.is_single = False
        self.line = Line()
        self.lanes.add(self.line)
        self.background_x = 0
        self.bg_x = 0
        self.rel_x = 0
        self.end = False
        self.end_frame = 0
        self.car_lanes = [110, 160, 210, 260, 310, 360, 410, 460, 510]
        for car in self.cars:
            self.cars_info.append(car.get_info())

    def update_sprite(self, command):
        '''update the model of src,call this fuction per frame'''
        self.count_bg()
        self.frame += 1
        self.handle_event()
        self._revise_speed()

        if self.status == "GAME_ALIVE":
            self.cars_info = []
            if self.frame > FPS * 4:
                self._creat_computercar()
            self._is_game_end()

            self.camera.update(self.maxVel)
            self.user_distance = []

            '''update sprite'''
            self.line.update()
            self.computerCars.update(self.cars)
            self.lanes.update(self.camera.position)
            self.line.rect.left = self.line.distance - self.camera.position + 500

            for car in self.users:
                # self.user_out__screen(car)
                self.user_distance.append(car.distance)
                # self.cars_info.append(car.get_info())
                car.update(command["ml_" + str(car.car_no + 1) + "P"])

                '''是否通過終點'''
                self._is_car_arrive_end(car)

            for car in self.cars:
                '''偵測車子的狀態'''
                self._detect_car_status(car)
                self.cars_info.append(car.get_info())

                '''更新車子位置'''
                car.rect.left = car.distance - self.camera.position + 500

        elif self.status == ("GAME_PASS" or "GAME_OVER") and self.close == False:
            self.user_distance = []
            for user in self.users:
                self.user_distance.append(user.distance)
            self.rank()
            self._print_result()
            self.close = True
            # self.running = False
            pass
        else:
            if self.frame - self.end_frame > FPS * 3:
                self.running = False

    def detect_collision(self):
        super(PlayingMode, self).detect_collision()
        for car in self.cars:
            self.cars.remove(car)
            hits = pygame.sprite.spritecollide(car, self.cars, False)
            for hit in hits:
                if (hit.status == True and 0 < hit.rect.centerx < WIDTH):
                    self.sound_controller.play_hit_sound()
                hit.status = False
                car.status = False
            self.cars.add(car)

    # def user_out__screen(self,car):
    #     if car.status:
    #             if car.rect.right < -100 or car.rect.bottom > 550 or car.rect.top < 100:
    #                 self.sound_controller.play_lose_sound()
    #                 car.status = False

    def _print_result(self):
        tem = []
        for user in self.winner:
            tem.append({"player": str(user.car_no + 1) + "P",
                        "distance": str(round(user.distance)) + "m",
                        "rank": self.winner.index(user) + 1
                        })
            print({"player": str(user.car_no + 1) + "P",
                   "distance": str(round(user.distance)) + "m",
                   "rank":self.winner.index(user)+1
                   })
        self.winner = tem

    def _init_user(self, user_no: int):
        self.car = UserCar((user_no) * 100 + 160, 0, user_no)
        self.users.add(self.car)
        self.cars.add(self.car)
        return None

    def _init_lanes(self):
        for i in range(8):
            for j in range(23):
                self.lane = Lane(i * 50 + 150, j * 50 - 150)
                self.lanes.add(self.lane)

    def _detect_car_status(self, car):
        if car.status:
            pass
        else:
            car.velocity = 0
            if car in self.users:
                car.image = car.image_list[1]
                if car not in self.eliminated_user:
                    self.eliminated_user.append(car)
            else:
                car.kill()
                # x = random.choice([650, -700])
                # car.re_create(self.camera.position + x)
                pass

    def _is_game_end(self):
        if len(self.users) - 1 == len(self.eliminated_user) and self.is_single == False:
            eliminated_user_distance = []
            for car in self.eliminated_user:
                eliminated_user_distance.append(car.distance)
            for car in self.users:
                if car not in self.eliminated_user and car.distance > max(eliminated_user_distance) + 100:
                    self.eliminated_user.append(car)
                    self.status = "GAME_PASS"
                    return None
                else:
                    pass
        elif len(self.eliminated_user) == len(self.users):
            self.status = "GAME_OVER"
        else:
            pass

    def _is_car_arrive_end(self, car):
        if car.distance > finish_line:
            for user in self.users:
                if user not in self.eliminated_user:
                    self.eliminated_user.append(user)
            self.status = "GAME_PASS"

    def _revise_speed(self):
        self.user_vel = []
        for car in self.users:
            self.user_vel.append(car.velocity)
        self.maxVel = max(self.user_vel)

    def count_bg(self):
        '''show the background and imformation on screen,call this fuction per frame'''
        super(PlayingMode, self).count_bg()
        self.rel_x = self.background_x % self.bg_image.get_rect().width
        self.bg_x = self.rel_x - self.bg_image.get_rect().width
        self.background_x -= self.maxVel

    def drawAllSprites(self):
        '''show all cars and lanes on screen,call this fuction per frame'''
        super(PlayingMode, self).drawAllSprites()
        self.lanes.draw(self.screen)
        self.cars.draw(self.screen)

    def _creat_computercar(self):

        if len(self.cars) < self.cars_num:
            x = random.choice([650, -700])
            y = random.choice(self.car_lanes)
            computerCar = ComputerCar(y, self.camera.position + x, x + 500)
            self.computerCars.add(computerCar)
            self.cars.add(computerCar)


    def rank(self):
        while len(self.eliminated_user) > 0:
            for car in self.eliminated_user:
                if car.distance == min(self.user_distance):
                    self.winner.append(car)
                    self.user_distance.remove(car.distance)
                    self.eliminated_user.remove(car)
        self.winner.reverse()
