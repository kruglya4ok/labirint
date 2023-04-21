from pygame import *

#клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y): 
        # Викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)

        #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    #метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#клас головного гравця
class Player(GameSprite):
    #метод, у якому реалізовано управління спрайтом за кнопками стрілочкам клавіатури
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    ''' переміщає персонажа, застосовуючи поточну горизонтальну та вертикальну швидкість'''
    def update(self):  
        # Спершу рух по горизонталі
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: # йдемо праворуч, правий край персонажа - впритул до лівого краю стіни
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # якщо торкнулися відразу кількох, то правий край - мінімальний із можливих
        elif self.x_speed < 0: # йдемо ліворуч, ставимо лівий край персонажа впритул до правого краю стіни
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # якщо торкнулися кількох стін, то лівий край - максимальний
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # йдемо вниз
            for p in platforms_touched:
                # Перевіряємо, яка з платформ знизу найвища, вирівнюємося по ній, запам'ятовуємо її як свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: # йдемо вгору
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) # вирівнюємо верхній край по нижніх краях стінок, на які наїхали
    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet('bulrt.png', self.rect.centerx, self.rect.top, 20, 30, 15)
        bullets.add(bullet)

#клас спрайту-ворога
class Enemy1(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, x1, x2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.x1 = x1
        self.x2 = x2
   #рух ворога
    def update(self):
        if self.rect.x <= self.x2: #w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.x >= self.x1:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy2(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, y1, y2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.y1 = y1
        self.y2 = y2
   #рух ворога
    def update(self):
        if self.rect.y <= self.y2: #w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.y >= self.y1:
            self.side = "left"
        if self.side == "left":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

# клас спрайту-кулі
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    #рух ворога
    def update(self):
        self.rect.x += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.x > win_width+10:
            self.kill()

#Створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Stalker")
window = display.set_mode((win_width, win_height))
back=transform.scale(image.load("fon.png"), (win_width, win_height))# задаємо колір відповідно до колірної схеми RGB

#Створюємо групу для стін
barriers = sprite.Group()

#створюємо групу для куль
bullets = sprite.Group()

#Створюємо групу для монстрів
monsters = sprite.Group()
fin = sprite.Group()
#Створюємо стіни картинки
w1 = GameSprite('plato_v_new.png', 350, 90, 30, 80)#
w2 = GameSprite('plato_h_new.png', 0, 60, 380, 30)#
w3 = GameSprite('plato_h_new.png', 400, 380, 300, 30)#
w4 = GameSprite('plato_h_new.png', 150, 165, 230, 30)
w5 = GameSprite('plato_h_new.png', 0, 270, 600, 30)####
w6 = GameSprite('plato_h_new.png', 140, 395, 120, 30)
w7 = GameSprite('plato_v_new.png', 400, 380, 30, 60)
w8 = GameSprite('plato_v_new.png', 510, 0, 30, 195)
w9 = GameSprite('plato_h_new.png', 540, 165, 60, 30)

#додаємо стіни до групи
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)

#створюємо спрайти
packman = Player('hero_new.png', 5, win_height - 80, 70, 70, 0, 0)
monster1 = Enemy1('monster_new.png', win_width - 70, 300, 70, 70, 5, 630, 450)
monster2 = Enemy2('monster_new.png', 300, 390, 80, 80, 5, 420, 300)
monster3 = Enemy1('monster_new.png', 0, 100, 70, 65, 5, 200, 0)
monster4 = Enemy2('monster_new.png', 390, 0, 70, 70, 5, 195, 0)
final_sprite = GameSprite('w2.png', win_width - 155, 0, 90, 90)
final_sprite2 = GameSprite('f2.png', 260, 100, 70, 70)
#додаємо монстра до групи
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
fin.add(final_sprite2)
#змінна, що відповідає за те, як закінчилася гра
ok = 0
finish = False
#ігровий цикл
run = True
while run:
    #цикл спрацьовує кожну 0.05 секунд
    time.delay(50)
        #перебираємо всі події, які могли статися
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -7
            elif e.key == K_RIGHT:
                packman.x_speed = 7
            elif e.key == K_UP:
                packman.y_speed = -7
            elif e.key == K_DOWN:
                packman.y_speed = 7
            elif e.key == K_SPACE:
                packman.fire()


        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0 
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0

#перевірка, що гра ще не завершена
    if not finish:
        #оновлюємо фон кожну ітерацію
        window.blit(back, (0,0))#зафарбовуємо вікно кольором

        #запускаємо рухи спрайтів
        packman.update()
        bullets.update()

        #оновлюємо їх у новому місці при кожній ітерації циклу
        packman.reset()
        #рисуємо стіни 2
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()
        fin.draw(window)
        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
        if sprite.spritecollide(packman, fin, True):
            ok += 1
        #Перевірка зіткнення героя з ворогом та стінами
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            # обчислюємо ставлення
            img = image.load('gameover.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        if sprite.collide_rect(packman, final_sprite) and ok == 1:
            finish = True
            img = image.load('win.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

    display.update()