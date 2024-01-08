import random
import time

import pygame

x = {'right': [0, 0, 0], 'down': [0, 300, 345], 'left': [0, 710, 710], 'up': [0, 420, 380]}
y = {'right': [0, 420, 380], 'down': [0, 0, 0], 'left': [0, 310, 345], 'up': [0, 700, 700]}
rotateAngle = {'right': -90, 'forward': 0, 'left': 90}
on_road = {'right': {1: 0, 2: 0}, 'down': {1: 0, 2: 0},
           'left': {1: 0, 2: 0}, 'up': {1: 0, 2: 0}}
turnMoment_right = {'right': {1: 290, 2: 325}, 'left': {1: 400, 2: 360}}
turnMoment_left = {'right': {1: 400, 2: 360}, 'left': {1: 280, 2: 320}}
turnMoment_up = {'right': {1: 400, 2: 360}, 'left': {1: 290, 2: 320}}
turnMoment_down = {'right': {1: 290, 2: 320}, 'left': {1: 390, 2: 360}}
speed_y = {'down': 5, 'up': -5}
speed_x = {'left': -5, 'right': 5}
sem1 = 260  # st jos
sem2 = 250  # st sus
sem3 = 460  # dr jos
sem4 = 480  # st sus
lungimeMasina = 50
masini = []
# care semafor e in momentul ala verde si care e in momentul ala galben(stanga jos sem1,dr jos sem2...)
currentGreen = 0
# currentYellow = 0
all_sprites_list = pygame.sprite.Group()


class Sem(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        if color == 'yellow':
            path = "yellow.jpg"
        elif color == 'green':
            path = "green.png"
        else:
            path = "red.jpg"

        super().__init__()

        # self.image = pygame.Surface([200, 420])
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()

    def changeColor(self, nr):
        if nr == 1:
            path = "green.png"
            self.image = pygame.image.load(path)
            self.rect = self.image.get_rect()
        elif nr == 2:
            path = "yellow.jpg"
            self.image = pygame.image.load(path)
            self.rect = self.image.get_rect()
        elif nr == 3:
            path = "red.jpg"
            self.image = pygame.image.load(path)
            self.rect = self.image.get_rect()


def sincronizeazaCulori(sem11, sem22, sem33, sem44, curr):
    if curr == 0:
        sem11.changeColor(1)
    else:
        sem11.changeColor(3)

    if curr == 1:
        sem22.changeColor(1)
    else:
        sem22.changeColor(3)

    if curr == 2:
        sem33.changeColor(1)
    else:
        sem33.changeColor(3)

    if curr == 3:
        sem44.changeColor(1)
    else:
        sem44.changeColor(3)


class Car(pygame.sprite.Sprite):
    def __init__(self, band, directie, rotire, rotateAngle=0, speed=0):
        pygame.sprite.Sprite.__init__(self)
        if (directie == 'right'):
            path = "car_right.png"
        elif (directie == 'up'):
            path = "car_up.png"
        elif (directie == 'down'):
            path = "car_down.png"
        elif (directie == 'left'):
            path = "car_left.png"

        super().__init__()

        # self.image = pygame.Surface([200, 420])
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.band = band
        self.face = directie
        self.rect.x = x[directie][band]
        self.rect.y = y[directie][band]
        # self.trecut = 0
        self.rotit = 0
        self.rotire = rotire
        self.speed = speed
        self.rotateAngle = rotateAngle
        on_road[self.face][self.band] += lungimeMasina
        # self.index = len(vehicles[directie][band]) - 1
        pygame.sprite.Sprite.__init__(self)

    def moveCar(self):
        if self.face == 'right':
            if (self.rotire == 0 and (self.rect.x < 200 - on_road[self.face][self.band] + lungimeMasina
                                      or currentGreen == 0 or self.rotit == 2)):
                self.rect.x += 5
                if self.rect.x >= sem1:
                    if on_road[self.face][self.band] >= 50:
                        on_road[self.face][self.band] -= lungimeMasina
                    else:
                        on_road[self.face][self.band] = 0
                    self.rotit = 2
            else:
                if self.rotateAngle == 90:
                    var = 'left'
                else:
                    var = 'right'
                if self.rotit == 0:
                    if self.rect.x < 200 - on_road[self.face][self.band] + lungimeMasina:
                        self.rect.x += 5
                    elif self.rect.x >= turnMoment_right[var][self.band]:
                        self.image = pygame.transform.rotate(self.image, self.rotateAngle / 2)
                        self.rotit = 1
                        if on_road[self.face][self.band] >= 50:
                            on_road[self.face][self.band] -= lungimeMasina
                        else:
                            on_road[self.face][self.band] = 0
                        # on_road[self.face]['crossed'] += 1
                    elif currentGreen == 0:
                        self.rect.x += 5
                elif self.rotit == 1:
                    self.image = pygame.transform.rotate(self.image, self.rotateAngle / 2)
                    if self.rotateAngle > 0: self.rect.y -= 20
                    self.rotit = 2
                elif self.rotit == 2:
                    self.rect.y += self.speed
        elif self.face == 'left':
            if (self.rotire == 0 and (self.rect.x > 500 + on_road[self.face][self.band] - lungimeMasina
                                      or currentGreen == 2 or self.rotit == 2)):
                self.rect.x -= 5
                if self.rect.x < sem4:
                    if on_road[self.face][self.band] >= 50:
                        on_road[self.face][self.band] -= lungimeMasina
                    else:
                        on_road[self.face][self.band] = 0
                    self.rotit = 2
            else:
                if self.rotateAngle == 90:
                    var = 'left'
                else:
                    var = 'right'
                if self.rotit == 0:
                    if self.rect.x > 500 + on_road[self.face][self.band] - lungimeMasina:
                        self.rect.x -= 5
                    elif self.rect.x <= turnMoment_left[var][self.band]:
                        self.image = pygame.transform.rotate(self.image, self.rotateAngle / 2)
                        self.rotit = 1
                        # if self.rotateAngle > 0: self.rect.x += 10
                        if on_road[self.face][self.band] >= 50:
                            on_road[self.face][self.band] -= lungimeMasina
                        else:
                            on_road[self.face][self.band] = 0
                        # on_road[self.face]['crossed'] += 1
                    elif currentGreen == 2:
                        self.rect.x -= 5
                    # elif self.rect.x < 530 and self.rect.x >= turnMoment_left[var][self.band]:
                    #     self.rect.x -= 5
                elif self.rotit == 1:
                    self.image = pygame.transform.rotate(self.image, self.rotateAngle / 2)
                    if self.rotateAngle < 0: self.rect.y -= 20
                    self.rotit = 2
                elif self.rotit == 2:
                    self.rect.y += self.speed
        elif self.face == 'up':
            if self.rotire == 0 and (self.rect.y > 500 + on_road[self.face][self.band] - lungimeMasina
                                     or currentGreen == 3 or self.rotit == 2):
                self.rect.y -= 5
                if self.rect.y < sem3:
                    if on_road[self.face][self.band] >= 50:
                        on_road[self.face][self.band] -= lungimeMasina
                    else:
                        on_road[self.face][self.band] = 0
                    self.rotit = 2
            else:
                if self.rotateAngle == 90:
                    var = 'left'
                else:
                    var = 'right'
                if self.rotit == 0:
                    if self.rect.y > 500 + on_road[self.face][self.band] - lungimeMasina:
                        self.rect.y -= 5
                    elif self.rect.y <= turnMoment_up[var][self.band]:
                        self.image = pygame.transform.rotate(self.image, self.rotateAngle / 2)
                        self.rotit = 1
                        if on_road[self.face][self.band] >= 50:
                            on_road[self.face][self.band] -= lungimeMasina
                        else:
                            on_road[self.face][self.band] = 0
                    elif currentGreen == 3:
                        self.rect.y -= 5
                elif self.rotit == 1:
                    self.image = pygame.transform.rotate(self.image, self.rotateAngle / 2)
                    # if (self.rotateAngle > 0): self.rect.y -= 20
                    self.rotit = 2
                elif self.rotit == 2:
                    self.rect.x += self.speed
        elif self.face == 'down':
            if self.rotire == 0 and (self.rect.y < 210 - on_road[self.face][self.band] + lungimeMasina
                                     or currentGreen == 1 or self.rotit == 2):
                self.rect.y += 5
                if self.rect.y > sem2:
                    if on_road[self.face][self.band] >= 50:
                        on_road[self.face][self.band] -= lungimeMasina
                    else:
                        on_road[self.face][self.band] = 0
                    self.rotit = 2
            else:
                if self.rotateAngle == 90:
                    var = 'left'
                else:
                    var = 'right'
                if self.rotit == 0:
                    if self.rect.y < 210 - on_road[self.face][self.band] + lungimeMasina:
                        self.rect.y += 5
                    elif self.rect.y >= turnMoment_down[var][self.band]:
                        self.image = pygame.transform.rotate(self.image, self.rotateAngle / 2)
                        self.rotit = 1
                        if on_road[self.face][self.band] >= 50:
                            on_road[self.face][self.band] -= lungimeMasina
                        else:
                            on_road[self.face][self.band] = 0
                    elif currentGreen == 1:
                        self.rect.y += 5
                elif self.rotit == 1:
                    self.image = pygame.transform.rotate(self.image, self.rotateAngle / 2)
                    # if (self.rotateAngle > 0): self.rect.y -= 20
                    self.rotit = 2
                elif self.rotit == 2:
                    self.rect.x += self.speed


def generareRand():
    banda = random.randint(1, 2)
    myList = ['right', 'left', 'up', 'down']
    directie = random.choice(myList)
    rotire = random.randint(0, 1)
    if rotire == 0:
        car = Car(banda, directie, rotire)
        masini.append(car)
        time.sleep(1)
        return car
    else:
        rot = ['left', 'right']
        art = random.choice(rot)
        ang = rotateAngle[art]
        if directie == 'down' and ang > 0:
            sp = speed_x['right']
        elif directie == 'down' and ang < 0:
            sp = speed_x['left']
        elif directie == 'up':
            sp = speed_x[art]
        elif directie == 'left' and ang < 0:
            sp = speed_y['up']
        elif directie == 'left' and ang > 0:
            sp = speed_y['down']
        elif directie == 'right' and ang < 0:
            sp = speed_y['down']
        elif directie == 'right' and ang > 0:
            sp = speed_y['up']
        car = Car(banda, directie, rotire, ang, sp)
        masini.append(car)
        time.sleep(1)
        return car


pygame.init()

RED = (255, 0, 0)

surface = pygame.display.set_mode((750, 750))
# color=(32,32,32)
# surface.fill(color)


image = pygame.image.load('r2.jpg')
surface.blit(image, (0, 0))

pygame.display.flip()
pygame.display.set_caption('Traffic Lights')

interval_in_seconds = 4  # 2 seconds

timer_interval = interval_in_seconds * 1000  # 1000 milliseconds = 1 second
timer_event_id = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event_id, timer_interval)

reloaded_event = pygame.USEREVENT + 2
pygame.time.set_timer(reloaded_event, 150)

sem_event = pygame.USEREVENT + 3
pygame.time.set_timer(sem_event, 15000)
running = True

# car = Vehicle(2, 'right', 1, rotateAngle['right'], speed_y['down']);

# car2=Vehicle(1,'right',0);

sem = Sem('green')
sem.rect.x = 250
sem.rect.y = 460
sem_st_s = Sem('red')
sem_st_s.rect.x = 250
sem_st_s.rect.y = 230

sem_dr_s = Sem('red')
sem_dr_s.rect.x = 470
sem_dr_s.rect.y = 235

sem_dr_j = Sem('red')
sem_dr_j.rect.x = 470
sem_dr_j.rect.y = 460

all_sprites_list.add(sem, sem_st_s, sem_dr_s, sem_dr_j)
# all_sprites_list.add(sem2)
clock = pygame.time.Clock()

# keep game running till running is true
while running:
    # Check for event if user has pushed
    # any event in queue
    for event in pygame.event.get():
        # print(pygame.mouse.get_pos())
        # if event is of type quit then
        # set running bool to false

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                running = False
        elif event.type == sem_event:
            currentGreen = (currentGreen + 1) % 4
            # print(currentGreen)
            sincronizeazaCulori(sem, sem_st_s, sem_dr_s, sem_dr_j, currentGreen)
            sem.rect.x = 250
            sem.rect.y = 460
            sem_st_s.rect.x = 250
            sem_st_s.rect.y = 230
            sem_dr_s.rect.x = 470
            sem_dr_s.rect.y = 235
            sem_dr_j.rect.x = 470
            sem_dr_j.rect.y = 460
            all_sprites_list.add(sem, sem_st_s, sem_dr_s, sem_dr_j)
        elif event.type == timer_event_id:
            # call function
            car = generareRand()
            masini.append(car)
            all_sprites_list.add(car)

        elif event.type == reloaded_event:
            for masina in masini:
                if masina.rect.x > 750 or masina.rect.y > 750 or (masina.rect.x < (-50) and masina.face != 'right') or (
                        masina.rect.y < (-50) and masina.face != 'down'):
                    masini.remove(masina)
                else:
                    #if masina.face == 'left':
                        #print(on_road[masina.face][masina.band])
                    masina.moveCar()
            # all_sprites_list.update()

        all_sprites_list.update()
        surface.blit(image, (0, 0))

        # pygame.display.flip()
        # pygame.display.update()
        all_sprites_list.draw(surface)
        pygame.display.flip()
        clock.tick(10)

        pygame.display.update()

pygame.quit()
