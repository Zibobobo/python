import pygame
import os
import random

FPS = 60
HEIGHT = 500
WIDTH = 1000
i = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
pygame.init()
clock = pygame.time.Clock()

path = "c:\\Programs\\Python\\pygame\\img"
win = pygame.display.set_mode((WIDTH,HEIGHT))
# backgroud
bg_img = pygame.image.load("c:\\Programs\\Python\\pygame\\img\\desert_BG.png")
bg = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))
# bullet
bullet_img = pygame.transform.scale(pygame.image.load(os.path.join(path,"bleu_light_bullet.png")), (10,10))
enemy_bullet_img = pygame.transform.scale(pygame.image.load(os.path.join(path,"green_light_bullet.png")), (10,10))
boss_bullet_img = pygame.transform.scale(pygame.image.load(os.path.join(path,"green_yellow_light_bullet.png")), (10,10))
# laser
laser_img = pygame.transform.scale(pygame.image.load(os.path.join(path,"yellow_light_bullet.png")), (10,10))
# tower
tower = pygame.transform.scale(pygame.image.load(os.path.join(path,"Tower.png")), ((200,200)))
# music/sound
path1 = "c:\\Programs\\Python\\pygame\\sound"
pop_sound = pygame.mixer.Sound(os.path.join(path1, "pop.ogg"))
music = pygame.mixer.music.load(os.path.join(path1, "music.ogg"))
pygame.mixer.music.set_volume(0.4)

# Load images of the Character (there are two popular ways)
# one way to do it - using the sprites that face left
standing = pygame.transform.scale(pygame.image.load(os.path.join(path, "standing.png")),(70,70))
left = [pygame.image.load(os.path.join(path, "L1.png")),
        pygame.image.load(os.path.join(path, "L2.png")),
        pygame.image.load(os.path.join(path, "L3.png")),
        pygame.image.load(os.path.join(path, "L4.png")),
        pygame.image.load(os.path.join(path, "L5.png")),
        pygame.image.load(os.path.join(path, "L6.png")),
        pygame.image.load(os.path.join(path, "L7.png")),
        pygame.image.load(os.path.join(path, "L8.png")),
        pygame.image.load(os.path.join(path, "L9.png"))
        ]
left_enemy = [pygame.image.load(os.path.join(path, "L1E.png")),
        pygame.image.load(os.path.join(path, "L2E.png")),
        pygame.image.load(os.path.join(path, "L3E.png")),
        pygame.image.load(os.path.join(path, "L4E.png")),
        pygame.image.load(os.path.join(path, "L5E.png")),
        pygame.image.load(os.path.join(path, "L6E.png")),
        pygame.image.load(os.path.join(path, "L7E.png")),
        pygame.image.load(os.path.join(path, "L8E.png")),
        pygame.image.load(os.path.join(path, "L9P.png")),
        pygame.image.load(os.path.join(path, "L10P.png")),
        pygame.image.load(os.path.join(path, "L11P.png"))
        ]
right_enemy = [pygame.image.load(os.path.join(path, "R1E.png")),
        pygame.image.load(os.path.join(path, "R2E.png")),
        pygame.image.load(os.path.join(path, "R3E.png")),
        pygame.image.load(os.path.join(path, "R4E.png")),
        pygame.image.load(os.path.join(path, "R5E.png")),
        pygame.image.load(os.path.join(path, "R6E.png")),
        pygame.image.load(os.path.join(path, "R7E.png")),
        pygame.image.load(os.path.join(path, "R8E.png")),
        pygame.image.load(os.path.join(path, "R9P.png")),
        pygame.image.load(os.path.join(path, "R10P.png")),
        pygame.image.load(os.path.join(path, "R11P.png"))
        ]
boss_img = [pygame.transform.scale(pygame.image.load(os.path.join(path,"R1B.png")),(60,60)),
            pygame.transform.scale(pygame.image.load(os.path.join(path,"R2B.png")),(60,60)),
            pygame.transform.scale(pygame.image.load(os.path.join(path,"R3B.png")),(60,60))]
# another (faster) way to do it - using the sprites that face right
right = []
for i in range(1,10):
    right.append(pygame.image.load(os.path.join(path,f"R{i}.png")))

pygame.display.set_caption("Tower defence")
pygame.display.set_icon(standing)

def draw_text(surf, text, size, x, y,color):
    font = pygame.font.Font("freesansbold.ttf", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_init():
    win.blit(bg,(0,0))
    draw_text(win, "Tower defence", 64, WIDTH/2, HEIGHT/4,WHITE)
    draw_text(win, "left and right to move", 22, WIDTH/2, HEIGHT*3/6,WHITE)
    draw_text(win, "f to shoot", 18, WIDTH/2, HEIGHT*3/5,WHITE)
    draw_text(win, "z to laser",18,WIDTH/2,HEIGHT/2.5,WHITE)
    draw_text(win, "space to jump",23, WIDTH/2, HEIGHT*3/4,WHITE)
    draw_text(win, "Press any key to start or click on screen", 20, WIDTH/2, HEIGHT*3/3.5,WHITE)
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

def draw_end():
    global kills,round
    win.blit(bg,(0,0))
    if round <= 6:
        draw_text(win,"You lost",70,WIDTH/2,HEIGHT/4,WHITE)
    elif round > 6:
        draw_text(win,"You won",70,WIDTH/2,HEIGHT/4,WHITE)
    draw_text(win, "Your kills: "+ str(kills), 64, WIDTH/2, HEIGHT/2,WHITE)
    draw_text(win, "Press R or click on the screen to restart", 22, WIDTH/2, HEIGHT*3/4,WHITE)
    pygame.display.update()
    end_waiting = True
    while end_waiting:
        userinput = pygame.key.get_pressed()
        clock.tick(FPS)
        # user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                end_waiting = False
                return False
        if userinput[pygame.K_r]:
            end_waiting = False
            return False

def draw_bosscoming():
    cooldown_counter = 1
    draw_text(win,"Boss coming!",60,WIDTH/2,HEIGHT/2,RED)
    pygame.display.update()
    while cooldown_counter!=0:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        if cooldown_counter >= 60:
            cooldown_counter = 0
        elif cooldown_counter > 0:
            cooldown_counter += 1
        if cooldown_counter == 0:
            return False

def draw_game():
    # bg
    global i, tower_health, round
    win.blit(bg, (0,0))
    #win.blit(bg, (i, 0))
    #print(i)
    #win.blit(bg,(WIDTH+i,0))
    #if i == WIDTH:
     #   win.blit(bg,(WIDTH+i,0))
      #  i = 0
    #i -= 1
    # player
    player.draw(win)
    # bullet
    for bullet in player.bullets:
        bullet.draw_bullet()
    for enemy in enemies:
        for bullet in enemy.bullets:
            bullet.draw_bullet()
    # laser cool down
    if player.cool_down_counter_laser == 0:
        draw_text(win,"Laser : Ready",20,100,25,GREEN)
    elif player.cool_down_counter_laser != 0:
        draw_text(win,"Laser : Not ready",20,100,25,RED)
    # round
    draw_text(win,"Round : "+ str(round),29,880,20,BLACK)
    # enemy
    for enemy in enemies:
        enemy.draw(win)
    # tower
    win.blit(tower,(350,240))
    # player health
    draw_text(win,"Lives: "+str(player.lives)+" |Tower health: "+str(tower_health)+" |Kills: "+str(kills), 32,500,20, BLACK)
    # delay and display
    pygame.time.delay(30)
    pygame.display.update()

class Hero:
    def __init__(self, x, y):
        # walk
        self.x = x
        self.y = y 
        self.velx = 8
        self.vely = 6
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        # jump
        self.jump = False
        # shoot
        self.bullets = []
        # cooldown
        self.cool_down_counter_bullet = 0
        self.cool_down_counter_laser = 0
        # health
        self.hitbox = (self.x, self.y, 64, 64)
        self.health = 30
        self.lives = 1
        self.alive = True
    
    def move_hero(self, userinput):
        if userinput[pygame.K_RIGHT] and self.x <= WIDTH - 62:
            self.face_right = True
            self.face_left = False
            self.x += self.velx
        elif userinput[pygame.K_LEFT] and self.x >= 1:
            self.face_left = True
            self.face_right = False
            self.x -= self.velx
        else:
            self.stepIndex = 0
    
    def jump_motion(self, userinput):
        if userinput[pygame.K_SPACE] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vely*4
            self.vely -= 1
        if self.vely == -7:
            self.jump = False
            self.vely = 6

    def draw(self, screen):
        self.hitbox = (self.x +15, self.y +15, 30, 40)
        pygame.draw.rect(win, (RED), (self.x +15, self.y,30,10))
        if player.health >= 0:
            pygame.draw.rect(win, (GREEN), (self.x +15, self.y,self.health,10))
        if self.face_right:
            screen.blit(right[self.stepIndex], (self.x,self.y))
            self.stepIndex += 1
        if self.face_left:
            screen.blit(left[self.stepIndex],(self.x,self.y))
            self.stepIndex += 1
        if self.stepIndex >= 9:
            self.stepIndex = 0

    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1

    def shoot(self):
        self.hit()
        self.cooldown()
        if userinput[pygame.K_f] and self.cool_down_counter_bullet == 0 and self.alive:
            pop_sound.play()
            bullet = Bullet(self.x,self.y,self.direction(),False,False)
            self.bullets.append(bullet)
            self.cool_down_counter_bullet = 1
        elif userinput[pygame.K_z] and self.cool_down_counter_laser == 0 and self.alive:
            pop_sound.play()
            laser = Bullet(self.x,self.y,self.direction(),True,False)
            self.cool_down_counter_laser = 1
            self.bullets.append(laser)
            
        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)
    
    def cooldown(self):
        if self.cool_down_counter_bullet >= 10:
            self.cool_down_counter_bullet = 0
        elif self.cool_down_counter_bullet > 0:
            self.cool_down_counter_bullet += 1
        if self.cool_down_counter_laser >= 300:
            self.cool_down_counter_laser = 0
        elif self.cool_down_counter_laser > 0:
            self.cool_down_counter_laser += 1
        

    def hit(self):
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2] and enemy.hitbox[1] < bullet.y < enemy.hitbox[1] + enemy.hitbox[3]:
                    if not(bullet.laser):
                        if enemy.boss:
                            enemy.health -= 1
                        else:
                            enemy.health -= 6

                    if bullet.laser:
                        if enemy.boss:
                            enemy.health -= 5
                        else:
                            enemy.health = 0
                    else:
                        self.bullets.remove(bullet)              

class Bullet:
    def __init__(self,x,y,direction,laser,enemy):
        self.x = x + 15
        self.y = y + 30
        self.direction = direction
        self.laser = laser
        self.enemy = enemy
        if not(self.enemy):
            if self.laser:
                self.speedx = 10
            else:
                self.speedx = 15
        elif self.enemy:
            self.speedx = 9

    def draw_bullet(self):
        if self.laser and not(self.enemy):
            win.blit(laser_img, (self.x,self.y))
        elif not(self.laser) and not(self.enemy):
            win.blit(bullet_img, (self.x,self.y))
        elif not(self.laser) and self.enemy:
            win.blit(enemy_bullet_img, (self.x,self.y))
        else:
            win.blit(boss_bullet_img,(self.x,self.y))
    
    def move(self):
        if self.direction == 1:
            self.x += self.speedx
        if self.direction == -1:
            self.x -= self.speedx

    def off_screen(self):
        return not(self.x >= 0 and self.x <= WIDTH)

class Enemy:
    def __init__(self,x,y,speed,direction,boss):
        self.x = x
        self.y = y
        self.speed = speed
        self.stepindex = 0
        self.direction = direction
        # health
        self.hitbox = (self.x,self.y,64,64)
        self.boss = boss
        self.health = 30
        # bullet
        self.bullets = []
        # cooldown
        self.cool_down_counter_bullet = 0
        self.cool_down_counter_laser = 0

    def step(self):
        if not(self.boss):
            if self.stepindex >= 33:
                self.stepindex = 0
        else:
            if self.stepindex >= 9:
                self.stepindex = 0

    def draw(self,win):
        self.hitbox = (self.x +20,self.y+10,30,45)
        if not(self.boss):
            pygame.draw.rect(win, (RED), (self.x +15, self.y,30,10))
            if self.health >= 0:
                pygame.draw.rect(win, (GREEN), (self.x +15, self.y,self.health,10))
        else:
            pygame.draw.rect(win, (RED), (self.x +15, self.y-10,30,10))
            if self.health >= 0:
                pygame.draw.rect(win, (GREEN), (self.x +15, self.y-10,self.health,10))
        if not(self.boss):
            self.step()
            if self.direction == -1:
                win.blit(left_enemy[self.stepindex//3],(self.x, self.y))
            elif self.direction == 1:
                win.blit(right_enemy[self.stepindex//3],(self.x, self.y))
        else:
            self.step()
            win.blit(boss_img[self.stepindex//3],(self.x,self.y))
        self.stepindex += 1

    def move(self):
        self.hit()
        if self.direction == -1:
            self.x -= self.speed
        if self.direction == 1:
            self.x += self.speed

    def cooldown(self):
        cooldonw_num = random.random()*3000
        if self.cool_down_counter_bullet >= cooldonw_num:
            self.cool_down_counter_bullet = 0
        elif self.cool_down_counter_bullet > 0:
            self.cool_down_counter_bullet += 1
        if self.cool_down_counter_laser >= 50:
            self.cool_down_counter_laser = 0
        elif self.cool_down_counter_laser > 0:
            self.cool_down_counter_laser += 1

    def shoot(self):
        self.hit()
        self.cooldown()
        if self.cool_down_counter_bullet == 0 and not(self.boss):
            bullet = Bullet(self.x,self.y,self.direction,False,True)
            self.bullets.append(bullet)
            self.cool_down_counter_bullet = 1
        elif self.cool_down_counter_laser == 0 and self.boss:
            laser = Bullet(self.x,self.y,self.direction,True,True)
            self.bullets.append(laser)
            self.cool_down_counter_laser = 1

        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)
    
    def hit(self):
        if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < enemy.y + 32 < player.hitbox[1] + player.hitbox[3]:
            if player.health > 0:
                if enemy.boss:
                    player.health = 0
                else:
                    player.health -= 0.1

        for bullet in self.bullets:
                if player.hitbox[0] < bullet.x < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < bullet.y < player.hitbox[1] + player.hitbox[3]:
                    if bullet.laser:
                        player.health -= 10
                    else:
                        player.health -= 1.5
                    self.bullets.remove(bullet)
        
        if player.health <= 0 and player.lives > 0:
                player.lives -= 1
                player.health = 30
        elif player.health <= 0 and player.lives == 0:
                player.alive = False

pygame.mixer.music.play(-1)
# Main loop
run = True
show_init = True
show_end = False
while run:
    if show_init:
        close_init = draw_init()
        if close_init:
            break                               
        show_init = False
        player = Hero(250,350)
        enemies = []
        speed = 2
        kills = 0
        tower_health = 5
        wavelenth = 0
        round = 0

    # update
    clock.tick(FPS)
    # quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # User input
    userinput = pygame.key.get_pressed()

    # Movements
    player.move_hero(userinput)
    player.jump_motion(userinput)

    # Shoot
    player.shoot()
    for enemy in enemies:
        enemy.shoot()

    # enemy
    if len(enemies) == 0:
        round += 1
        wavelenth += 2
        if round == 6:
            close_draw_bosscoming = draw_bosscoming()
            print(close_draw_bosscoming)
            if close_draw_bosscoming:
                break
            boss = Enemy(1020,355,1,-1,True)
            enemies.append(boss)
        else:
            for i in range(wavelenth):
                speed = random.randrange(2,3)
                spawn_point_left = random.randrange(1000,1200)
                spawn_point_right = random.randrange(1,100)
                rand_nr = random.randint(0,1)
                if rand_nr == 0:
                    enemy = Enemy(spawn_point_left,355,speed,-1,False)
                    enemies.append(enemy)
                elif rand_nr == 1:
                    enemy = Enemy(-spawn_point_right,355,speed,1,False)
                    enemies.append(enemy)
    for enemy in enemies:
        enemy.move()
        if enemy.x > 350 and enemy.x < 450:
            enemies.remove(enemy)
            if enemy.boss:
                tower_health -= 3
            else:
                tower_health -= 1
        if enemy.health <= 0:
            kills += 1
            enemies.remove(enemy)
    
    # Tower health
    if tower_health == 0:
        player.alive = False
    if player.alive == False or round == 7:
        enemies = []
        show_end = True
        if show_end:
            close_end = draw_end()
        if close_end:
            break
        show_end = False
        tower_health = 5
        player = Hero(250,350)
        player.cool_down_counter_laser = 0
        wavelenth = 0
        kills = 0
        round = 0


    # draw game
    draw_game()

pygame.quit()