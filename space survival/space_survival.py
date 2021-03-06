# main
import pygame
import random 
import os

FPS = 60 
WIDTH = 500
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# init game and create screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space survival")
clock = pygame.time.Clock()

# upload images
data = "c:\Programs\Python\pygame\img"
background_img = pygame.image.load(os.path.join(data, "background.png")).convert()
player_img = pygame.image.load(os.path.join(data, "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
bullet_img = pygame.image.load(os.path.join(data, "bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join(data, f"rock{i}.png")).convert())
expl_anim = {}
expl_anim["lg"] = []
expl_anim["sm"] = []
expl_anim["player"] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join(data, f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim["lg"].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim["sm"].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join(data, f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim["player"].append(player_expl_img)
power_imgs = {}
power_imgs["shield"] = pygame.image.load(os.path.join(data, "shield.png")).convert()
power_imgs["gun"] = pygame.image.load(os.path.join(data, "gun.png")).convert()
# upload music
data_1 = "c:\Programs\Python\pygame\sound"
shoot_sound = pygame.mixer.Sound(os.path.join(data_1, "shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join(data_1, "pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join(data_1, "pow0.wav"))
die_sound = pygame.mixer.Sound(os.path.join(data_1, "rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join(data_1, "expl0.wav")),
    pygame.mixer.Sound(os.path.join(data_1, "expl1.wav"))
]
pygame.mixer.music.load(os.path.join(data_1, "background.ogg"))
pygame.mixer.music.set_volume(0.4)

font_name = os.path.join("c:\Programs\Python\pygame", "font.ttf")
def draw_text(surf, text, size, x, y,color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0,0))
    draw_text(screen, "space survival", 64, WIDTH/2, HEIGHT/4,WHITE)
    draw_text(screen, "a s w d to move", 22, WIDTH/2, HEIGHT*3/6,WHITE)
    draw_text(screen, "space to shoot", 18, WIDTH/2, HEIGHT*3/5,WHITE)
    draw_text(screen, "Press any key or click to play",23, WIDTH/2, HEIGHT/2.5,WHITE)
    draw_text(screen, "Try to get over 3500 points", 20, WIDTH/2, HEIGHT*3/4,WHITE)
    pygame.display.update()
    init_waiting = True
    while init_waiting:
        clock.tick(FPS)
        # user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                init_waiting = False
                return False

def draw_choose_level():
    screen.blit(background_img, (0,0))
    draw_text(screen, "Choose your level", 40, WIDTH/2, HEIGHT/4,WHITE)
    draw_text(screen, "Easy : press 1", 15, WIDTH/2, HEIGHT*3/6,WHITE)
    draw_text(screen, "Normal : press 2", 15, WIDTH/2, HEIGHT*3/5.2,WHITE)
    draw_text(screen, "Impossible : press 3",15, WIDTH/2, HEIGHT*3/4.5,WHITE)
    draw_text(screen, "God : press 0 ", 15, WIDTH/2,HEIGHT*3/4,WHITE)
    pygame.display.update()
    chosee_waiting = True
    while chosee_waiting:
        key_pressed = pygame.key.get_pressed()
        clock.tick(FPS)
        # user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        if key_pressed[pygame.K_1]:
            chosee_waiting = False
            player.level = 1
            return False
        elif key_pressed[pygame.K_2]:
            chosee_waiting = False
            player.level = 2
            return False
        elif key_pressed[pygame.K_3]:
            chosee_waiting = False
            player.level = 3
            return False
        elif key_pressed[pygame.K_0]:
            chosee_waiting = False
            player.level = 0
            return False

def draw_choose_mode():
    screen.blit(background_img, (0,0))
    draw_text(screen, "Choose your mode", 40, WIDTH/2, HEIGHT/4,WHITE)
    draw_text(screen, "Infinite mode : press i", 15, WIDTH/2, HEIGHT*3/6,WHITE)
    draw_text(screen, "Other : press o", 15, WIDTH/2, HEIGHT*3/5.2,WHITE)
    pygame.display.update()
    choseemode_waiting = True
    while choseemode_waiting:
        key_pressed = pygame.key.get_pressed()
        clock.tick(FPS)
        # user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        if key_pressed[pygame.K_i]:
            choseemode_waiting = False
            player.mode = "infinite"
            return False
        elif key_pressed[pygame.K_o]:
            choseemode_waiting = False
            player.mode = "other"
            return False

def draw_end():
    screen.blit(background_img, (0,0))
    draw_text(screen, "Your score is "+str(score), 50, WIDTH/2, HEIGHT/4,WHITE)
    if score == 0:
        draw_text(screen,"How !?    Are you serious",13,WIDTH/2,HEIGHT/4.5,WHITE)
    elif score < 0:
        draw_text(screen,"Why did you hack my game!?",13,WIDTH/2,HEIGHT/4.5,WHITE)
    elif score < 3500:
        draw_text(screen, "Noob haha", 13,WIDTH/2,HEIGHT/4.5,WHITE)
    elif score == 3500:
        draw_text(screen,"OMG Exacly 3500",13,WIDTH/2,HEIGHT/4.5,WHITE)
    elif score >= 10000:
        draw_text(screen,"Congragulation You win!",13,WIDTH/2,HEIGHT/4.5,WHITE)
    elif score > 3500:
        draw_text(screen,"Good job You did it Now try to get more",13,WIDTH/2,HEIGHT/4.5,WHITE)
    elif score >= 7000:
        draw_text(screen,"You almost win!",13,WIDTH/2,HEIGHT/4.5,WHITE)
    draw_text(screen, "Play again?", 22, WIDTH/2, HEIGHT/2,WHITE)
    draw_text(screen, "If you want to play again click on the screen", 18, WIDTH/2, HEIGHT*3/4,WHITE)
    pygame.display.update()
    end_waiting = True
    while end_waiting:
        clock.tick(FPS)
        # user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                end_waiting = False
                return False

def draw_cooldown(surf, text, size, x, y):
    if player.cool_down_counter != 0:
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midleft = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
        self.bulletnum = 10
        self.cool_down_counter = 0
        self.cool_down_counter_eachbullet = 0
        self.level = None
        self.mode = None

    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun = 1
            self.gun_time = now

        if self.hidden == True and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speedx
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speedx

        if self.rect.right > WIDTH: 
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if not(self.hidden):
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

    def shoot(self):
        self.cooldown()
        if self.bulletnum <= 0:
            if self.level != 0:
                self.cool_down_counter = 1
            self.bulletnum = 10
        key_pressed = pygame.key.get_pressed()
        if not(self.hidden) and self.cool_down_counter == 0 and key_pressed[pygame.K_SPACE] and self.cool_down_counter_eachbullet == 0:
            if self.level != 0:
                self.cool_down_counter_eachbullet = 1
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.bulletnum -= 1
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >=2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                self.bulletnum -= 1
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def cooldown(self):
        if self.cool_down_counter >= 100:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
        if self.cool_down_counter_eachbullet >= 20:
            self.cool_down_counter_eachbullet = 0
        elif self.cool_down_counter_eachbullet > 0:
            self.cool_down_counter_eachbullet += 2

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs) 
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

pygame.mixer.music.play(-1)

# game while
show_init = True
show_end = False
show_choice = False
show_choicemode = False
running = True
while running:
    if show_init:
        close_init = draw_init()
        if close_init:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        show_choice = True
        score = 0

    if show_choice:
        close_choice = draw_choose_level()
        if close_choice:
            break
        show_choice = False
        if player.level == 1:
            wave_lenth = 15
            for i in range(wave_lenth):
                new_rock()
        elif player.level == 2:
            wave_lenth = 30
            for i in range(wave_lenth):
                new_rock()
        elif player.level == 3 or player.level == 0:
            wave_lenth = 50
            for i in range(wave_lenth):
                new_rock()
        show_choicemode = True
    
    if show_choicemode:
        close_choicemode = draw_choose_mode()
        if close_choicemode:
            break
        show_choicemode = False
    
    clock.tick(FPS)
    # user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.shoot()

    # update game
    all_sprites.update()

    # rock and bullet collision
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        if player.level == 1:
            score += hit.radius*3
        elif player.level == 2:
            score += hit.radius
        elif player.level == 3:
            score += hit.radius
        elif player.level == 0:
            score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    # rock and player collision
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        if player.level == 1:
            player.health -= hit.radius
        else:
            player.health -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()
            
    # power and player collision
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
            shield_sound.play()
        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()
    if score > 10000 and player.mode != "infinite":
        score = 10000
    if (player.lives == 0 and not(death_expl.alive())) or score == 10000:
        show_end = True
    if show_end:
        close_end = draw_end()
        if close_end:
            break
        show_end = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        score = 0
        show_choice = True

    if show_choice:
        close_choice = draw_choose_level()
        if close_choice:
            break
        show_choice = False
        if player.level == 1:
            wave_lenth = 15
            for i in range(wave_lenth):
                new_rock()
        elif player.level == 2:
            wave_lenth = 30
            for i in range(wave_lenth):
                new_rock()
        elif player.level == 3 or player.level == 0:
            wave_lenth = 50
            for i in range(wave_lenth):
                new_rock()
        show_choicemode = True
    
    if show_choicemode:
        close_choicemode = draw_choose_mode()
        if close_choicemode:
            break
        show_choicemode = False

    # update frame
    screen.fill(BLACK)
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 15, WIDTH/2, 10,WHITE)
    draw_cooldown(screen, "Cooldown-ing "+str(player.cool_down_counter/10),15,player.rect.center,player.rect.top)
    if player.cool_down_counter == 0:
        draw_text(screen, "Bullet number: "+str(player.bulletnum), 15, WIDTH - 325,10,RED)
    else:
        draw_text(screen, "Bullet number: 0", 15, WIDTH - 325,10,RED)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 10)
    pygame.display.update()

pygame.quit() 
