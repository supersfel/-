import pygame
import random
import copy
import gc

WHITE = (255, 255, 255)
pad_width = 1024
pad_height = 512


class Game_Object:
    def __init__(self, image, x=0, y=0, collider_x=0, collider_y=0):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y
        self.collider_x = collider_x
        self.collider_y = collider_y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_collider_x(self):
        return self.collider_x

    def get_collider_y(self):
        return self.collider_y

    def delete(self):
        game_object[self.__class__.__name__].remove(self)
        del (self)

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
            self.delete()

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
            self.delete()


class Fire(Enemy):
    def on_working(self, move_distance):
        if self.x >= 0:
            self.move_x(move_distance)
        else:
            self.delete()


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


class Boom_effect(Game_Object):

    def set_time(self, limit_time):
        self.effect_time = 0
        self.effect_limit_time = limit_time

    def draw(self):
        if self.effect_time <= self.effect_limit_time:
            self.effect_time += 1
            gamepad.blit(self.image, (self.x, self.y))

        else:
            self.delete()


class effect_draw():
    global clock, game_object

    def __init__(self, effect_obj):
        self.effect_obj = effect_obj

    def create_effect(self, obj):
        new_effect = copy.copy(self.effect_obj)
        new_effect.set_x(obj.get_x())
        new_effect.set_y(obj.get_y())
        new_effect.set_time(5)

        game_object[type(self.effect_obj).__name__].append(new_effect)


def obj_draw(obj):
    obj.draw()


def obj_create_enemy(obj):
    obj.create_enemy()


def obj_on_working(obj, move_distance):
    obj.on_working(move_distance)


def obj_delete(obj):
    obj.delete()


def crash(obj_a, obj_b):
    obj_a_xy = (obj_a.get_x(), obj_a.get_y())
    obj_a_collider = (obj_a.get_collider_x(), obj_a.get_collider_y())

    obj_a_collider_list = [obj_a_xy, (obj_a_xy[0], obj_a_xy[1] + obj_a_collider[1]), obj_a_collider,
                           (obj_a_xy[0] + obj_a_collider[0], obj_a_xy[1])]

    obj_b_xy = (obj_b.get_x(), obj_b.get_y())
    obj_b_collider = (obj_b.get_collider_x(), obj_b.get_collider_y())

    for a in obj_a_collider_list:
        if (a[0] >= obj_b_xy[0] and a[0] <= obj_b_xy[0] + obj_b_collider[0]) and (
                a[1] >= obj_b_xy[1] and a[1] <= obj_b_xy[1] + obj_b_collider[1]):
            print('crash!')
            return True

    return False


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

        for obj in game_object['Fire']:
            obj_on_working(obj, -15)

        for obj in game_object['Bullet']:
            obj_on_working(obj, 15)

            for mob in game_object['Bat']:
                if crash(obj, mob):
                    game_object['Boom_effect_draw'].create_effect(mob)
                    obj_delete(obj)
                    obj_delete(mob)
                    break

        for key in ['Bat', 'Fire', 'Bullet', 'Boom_effect']:
            for obj in game_object[key]:
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

    plane_png_x = 89
    plane_png_y = 55
    aircraft = Player("images/plane.png", pad_width * 0.05, pad_height * 0.8, plane_png_x, plane_png_y)
    game_object['Player'] = aircraft

    bullet_png_x = 27
    bullet_png_y = 5
    bullet = Bullet("images/bullet.jpg", 0, 0, bullet_png_x, bullet_png_y)
    game_object['Bullet'] = list()

    fire_position = Fire_Position(89, 27, bullet)
    game_object['Fire_Position'] = fire_position

    background_1 = Background("images/background.png")
    background_2 = Background("images/background.png", pad_width, 0)
    game_object['background'] = [background_1, background_2]

    bat_png_x = 108
    bat_png_y = 67
    enemy_bat = Bat("images/bat.jpg", pad_width, 0, bat_png_x, bat_png_y)
    enemy_bat_spawn = Enemy_spawn(1, 5, enemy_bat)

    game_object['bat_spawn'] = enemy_bat_spawn

    fire_1_png_x = 140
    fire_1_png_y = 61
    enemy_fire1 = Fire("images/fire1.jpg", pad_width, 0, fire_1_png_x, fire_1_png_y)

    fire_2_png_x = 86
    fire_2_png_y = 59
    enemy_fire2 = Fire("images/fire2.jpg", pad_width, 0, fire_2_png_x, fire_2_png_y)

    enemy_fire1_spawn = Enemy_spawn(5, 10, enemy_fire1)
    enemy_fire2_spawn = Enemy_spawn(5, 10, enemy_fire2)

    game_object['fire1_spawn'] = enemy_fire1_spawn
    game_object['fire2_spawn'] = enemy_fire2_spawn

    game_object['Fire'] = list()
    game_object['Bat'] = list()

    boom_effect = Boom_effect("images/boom.png")
    boom_effect_draw = effect_draw(boom_effect)
    game_object["Boom_effect_draw"] = boom_effect_draw

    game_object["Boom_effect"] = list()

    clock = pygame.time.Clock()
    runGame()


initGame()