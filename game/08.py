import pygame
import random
import copy
import gc

WHITE = (255, 255, 255)
pad_width = 1024
pad_height = 512


class Game_Object:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def draw(self):
        gamepad.blit(self.image, (self.x, self.y))


class Player(Game_Object):
    def move_y(self, move_distance):
        self.y += move_distance


class Bullet(Game_Object):
    def move_x(self, move_distance):
        self.x += move_distance

    def on_working(self, move_distance):
        if self.x <= pad_width:
            self.move_x(move_distance)
        else:
            game_object[self.__class__.__name__].remove(self)
            del (self)

    def __del__(self):
        print("Bullet Delete")


class Fire_Position():
    global clock, game_object

    def __init__(self, x, y, bullet_obj):
        self.x = x
        self.y = y
        self.bullet_obj = bullet_obj

    def create_bullet(self):
        new_bullet = copy.copy(self.bullet_obj)
        new_bullet.set_x(game_object['Player'].get_x() + self.x)
        new_bullet.set_y(game_object['Player'].get_y() + self.y)

        game_object[type(self.bullet_obj).__name__].append(new_bullet)


class Enemy(Game_Object):
    global game_object

    def move_x(self, move_distance):
        self.x += move_distance

    def on_working(self, move_distance):
        pass

    def __del__(self):
        print(self.__class__.__name__ + " delete!")


class Bat(Enemy):
    def on_working(self, move_distance):
        if self.x >= 0:
            self.move_x(move_distance)
        else:
            game_object[self.__class__.__name__].remove(self)
            del (self)


class Fire(Enemy):
    def on_working(self, move_distance):
        if self.x >= 0:
            self.move_x(move_distance)
        else:
            game_object[self.__class__.__name__].remove(self)
            del (self)


class Background(Game_Object):
    def move_x(self, move_distance):
        self.x += move_distance
        self.check_area()

    def check_area(self):
        if self.x == -pad_width:
            self.x = pad_width


class Enemy_spawn():
    global clock, game_object

    def __init__(self, min_time, max_time, enemy_obj):
        self.min_time = min_time
        self.max_time = max_time
        self.create_time = random.randrange(self.min_time, self.max_time)
        self.current_time = 0

        self.enemy_obj = enemy_obj

    def create_enemy(self):

        deltatime = clock.get_fps()

        if deltatime == 0:
            self.current_time += deltatime
        else:
            self.current_time += 1 / deltatime

        if self.current_time >= self.create_time:
            new_enemy = copy.copy(self.enemy_obj)
            new_enemy.set_y(random.randrange(0, pad_height))

            game_object[type(self.enemy_obj).__name__].append(new_enemy)

            self.create_time = random.randrange(self.min_time, self.max_time)

            self.current_time = 0


def obj_draw(obj):
    obj.draw()


def obj_create_enemy(obj):
    obj.create_enemy()


def obj_on_working(obj, move_distance):
    obj.on_working(move_distance)


def runGame():
    global gamepad, clock, game_object

    Player_y_move_distance = 0
    Background_x_move_distance = -2
    crashed = False

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Player_y_move_distance = -5

                elif event.key == pygame.K_DOWN:
                    Player_y_move_distance = 5

                if event.key == pygame.K_LCTRL:
                    game_object['Fire_Position'].create_bullet()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    Player_y_move_distance = 0

        game_object['Player'].move_y(Player_y_move_distance)
        game_object['background'][0].move_x(Background_x_move_distance)
        game_object['background'][1].move_x(Background_x_move_distance)
        gamepad.fill(WHITE)

        obj_create_enemy(game_object['bat_spawn'])
        obj_create_enemy(game_object['fire1_spawn'])
        obj_create_enemy(game_object['fire2_spawn'])

        obj_draw(game_object['background'][0])
        obj_draw(game_object['background'][1])

        for obj in game_object['Bat']:
            obj_on_working(obj, -7)
            obj_draw(obj)

        for obj in game_object['Fire']:
            obj_on_working(obj, -15)
            obj_draw(obj)

        for obj in game_object['Bullet']:
            obj_on_working(obj, 15)
            obj_draw(obj)

        obj_draw(game_object['Player'])
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


def initGame():
    global gamepad, clock, game_object

    game_object = dict()
    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('PyFlying')

    aircraft = Player("images/plane.png", pad_width * 0.05, pad_height * 0.8)
    game_object['Player'] = aircraft

    bullet = Bullet("images/bullet.jpg", 0, 0)
    game_object['Bullet'] = list()

    fire_position = Fire_Position(89, 27, bullet)
    game_object['Fire_Position'] = fire_position

    background_1 = Background("images/background.png", 0, 0)
    background_2 = Background("images/background.png", pad_width, 0)
    game_object['background'] = [background_1, background_2]

    enemy_bat = Bat("images/bat.jpg", pad_width, 0)
    enemy_bat_spawn = Enemy_spawn(1, 5, enemy_bat)

    game_object['bat_spawn'] = enemy_bat_spawn

    enemy_fire1 = Fire("images/fire1.jpg", pad_width, 0)
    enemy_fire2 = Fire("images/fire2.jpg", pad_width, 0)

    enemy_fire1_spawn = Enemy_spawn(5, 10, enemy_fire1)
    enemy_fire2_spawn = Enemy_spawn(5, 10, enemy_fire2)

    game_object['fire1_spawn'] = enemy_fire1_spawn
    game_object['fire2_spawn'] = enemy_fire2_spawn

    game_object['Fire'] = list()
    game_object['Bat'] = list()

    clock = pygame.time.Clock()
    runGame()


initGame()