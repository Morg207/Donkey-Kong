import random
import sys
import pygame

pygame.init()

clock = pygame.time.Clock()
running = True
display_width = 800
display_height = 820
pygame.display.set_caption("Donkey Kong")
display = pygame.display.set_mode((display_width,display_height))
total_tiles = 32
tile_width = display_width // total_tiles
tile_height = display_height // total_tiles
pygame.mouse.set_visible(False)
fps = 60
delta_time = 0
dk_image1 = pygame.transform.scale(pygame.image.load("images/dk1.png"),(tile_width * 3.4, tile_height * 4.2)).convert_alpha()
dk_image1_flipped = pygame.transform.flip(dk_image1,True,False)
dk_image2 = pygame.transform.scale(pygame.image.load("images/dk2.png"),(tile_width * 3.4, tile_height * 4.2)).convert_alpha()
dk_image3 = pygame.transform.scale(pygame.image.load("images/dk3.png"),(tile_width * 3.4, tile_height * 4.2)).convert_alpha()
mario_standing = pygame.transform.scale(pygame.image.load("images/standing.png"),(tile_width * 2.2,tile_height * 2)).convert_alpha()
mario_standing_left = pygame.transform.flip(mario_standing,True,False)
mario_climbing1 = pygame.transform.scale(pygame.image.load("images/climbing1.png"),(tile_width * 2.2,tile_height * 2)).convert_alpha()
mario_climbing2 = pygame.transform.scale(pygame.image.load("images/climbing2.png"),(tile_width * 2.2,tile_height * 2)).convert_alpha()
mario_jumping = pygame.transform.scale(pygame.image.load("images/jumping.png"),(tile_width * 2.2,tile_height * 2)).convert_alpha()
mario_jumping_left = pygame.transform.flip(mario_jumping,True,False)
mario_running = pygame.transform.scale(pygame.image.load("images/running.png"),(tile_width * 2.2,tile_height * 2)).convert_alpha()
mario_running_left = pygame.transform.flip(mario_running,True,False)
mario_hammer = pygame.transform.scale(pygame.image.load("images/hammer_stand.png"),(tile_width * 3,tile_height * 2)).convert_alpha()
mario_hammer_left = pygame.transform.flip(mario_hammer,True,False)
mario_hammer_jump = pygame.transform.scale(pygame.image.load("images/hammer_jump.png"),(tile_width * 3,tile_height * 2)).convert_alpha()
mario_hammer_jump_left = pygame.transform.flip(mario_hammer_jump,True,False)
mario_hammer_overhead = pygame.transform.scale(pygame.image.load("images/hammer_overhead.png"),(tile_width * 3,tile_height * 2)).convert_alpha()
mario_hammer_overhead_left = pygame.transform.flip(mario_hammer_overhead,True,False)
hammer = pygame.transform.scale(pygame.image.load("images/hammer.png"),(tile_width * 2.2,tile_height * 2.5)).convert_alpha()
barrel1 = pygame.transform.scale(pygame.image.load("images/barrel.png"),(30, 30)).convert_alpha()
barrel2 = pygame.transform.scale(pygame.image.load("images/barrel2.png"),(tile_width * 1.3,tile_height * 2.5)).convert_alpha()
barrel2 = pygame.transform.rotate(barrel2,90)
barrel3 = pygame.transform.scale(pygame.image.load("images/barrel3.png"),(tile_width * 1.5,tile_height * 2)).convert_alpha()
peach1 = pygame.transform.scale(pygame.image.load("images/peach1.png"),(tile_width * 1.9,tile_height * 2.1)).convert_alpha()
peach2 = pygame.transform.scale(pygame.image.load("images/peach2.png"),(tile_width * 1.9, tile_height * 2.1)).convert_alpha()
fire = pygame.transform.scale(pygame.image.load("images/fire.png"),(50,25)).convert_alpha()
fire_flipped = pygame.transform.flip(fire,True,False)
fire_ball = pygame.transform.scale(pygame.image.load("images/fireball.png"),(tile_width * 1.5,tile_height*1.2)).convert_alpha()
fire_ball_flipped = pygame.transform.flip(fire_ball,True,False)
fire_ball2 = pygame.transform.scale(pygame.image.load("images/fireball2.png"),(tile_width * 1.5,tile_height*1.2)).convert_alpha()
fire_ball2_flipped = pygame.transform.flip(fire_ball2,True,False)
row6_y = ((total_tiles-25)-0.4) * tile_height
row5_y = (total_tiles-23) * tile_height
row4_y = (total_tiles-18) * tile_height
row3_y = (total_tiles-12) * tile_height
row2_y = (total_tiles-8+2) * tile_height
platform_colour = (240,97,97)
oil_colour = (66,135,245)
oil_lip_colour = (22,62,128)
oil_stripe_colour = (107,240,242)
fire_balls = pygame.sprite.Group()
barrel_font = pygame.font.Font("fonts/pixel.ttf",20)
score = 0
highscore = 0
level = 1
joysticks = []

def reset_game():
    global score, highscore
    if score > highscore:
        highscore = score
    score = 0
    kong.reset()
    player.reset(8,total_tiles-2)
    peach.reset()
    oil_drum.reset()
    fire_balls.empty()
    oil_drum.fire_ball_timer = pygame.time.get_ticks()/1000

def draw_text(text,x,y,size,colour=(255,255,255)):
    font = pygame.font.Font("fonts/pixel.ttf",size)
    text_image = font.render(text,True,colour)
    text_rect = text_image.get_rect()
    text_rect.center = (x,y)
    display.blit(text_image,text_rect)

def draw_ladders():
    for ladder in ladders:
        ladder.draw()

def draw_background_ladders():
    for background_ladder in background_ladders:
        background_ladder.draw()

def draw_platforms():
    for platform in platforms:
        platform.draw()

def draw_barrels():
    display.blit(barrel2,(100,93))
    display.blit(barrel2,(100,63))
    display.blit(barrel2,(63,93))
    display.blit(barrel2,(63,63))

class FireBall(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = fire_ball
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        self.x_max = 4
        self.x_count = 0
        self.x_speed = 3
        self.y_speed = 0
        self.count = 0
        self.flip_pos = 1
        self.climbing = False

    def climb(self):
        for ladder in ladders:
            if self.rect.colliderect(ladder.rect) and not self.climbing and not ladder.broken:
                if random.randint(0,50) == 50:
                    self.climbing = True
                    self.y_speed = -4

    def destroy(self):
        if self.rect.top > display_height or self.rect.bottom < 0:
            oil_drum.fire_ball_timer = pygame.time.get_ticks()/1000
            self.kill()
        if self.rect.colliderect(player.hitbox):
            reset_game()

    def update(self):
        if self.y_speed < 3 and not self.climbing:
            self.y_speed += 0.25
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                self.climbing = False
                self.y_speed = -4
        if self.count < 20:
            self.count += 1
        else:
            self.flip_pos *= -1
            self.count = 0
            if self.x_count < self.x_max:
                self.x_count += 1
            else:
                self.x_count = 0
                self.x_speed *= -1
                self.x_max = random.randint(3,6)    
        if self.flip_pos == 1:
            if self.x_speed > 0:
                self.image = fire_ball
            else:
                self.image = fire_ball_flipped
        else:
            if self.x_speed > 0:
                self.image = fire_ball2
            else:
                self.image = fire_ball2_flipped
        self.climb()
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.destroy()
            
    def draw(self):
        display.blit(self.image,self.rect)

class OilDrum():
    def __init__(self):
       self.reset()
       self.frames = (fire,fire_flipped)
       self.fire_ball_timer = 0
       self.fire_ball_time = 4

    def reset(self):
       self.count = 0
       self.image = fire
       self.index = 0

    def update(self):
        if pygame.time.get_ticks()/1000 - self.fire_ball_timer > self.fire_ball_time and len(fire_balls)== 0:
            fire_ball = FireBall(140,740)
            fire_balls.add(fire_ball)
        self.count += 1
        if self.count > 75:
            self.index += 1
            if self.index > len(self.frames)-1:
                self.index = 0
            self.image = self.frames[self.index]
            self.count = 0
    
    def draw(self):
        display.blit(self.image,(110,700))
        top_lip = pygame.Rect(110,726,50,3)
        body = pygame.Rect(top_lip.left+4,top_lip.top,top_lip.width-8,47)
        bottom_lip = pygame.Rect(top_lip.left,body.bottom-3,top_lip.width,3)
        vertical_stripe = pygame.Rect(body.left+4,top_lip.bottom,2,body.height-8)
        hor_stripe1 = pygame.Rect(body.left,body.top+(body.height/3),body.width,2)
        hor_stripe2 = pygame.Rect(body.left,body.top+((body.height/3)*2),body.width,2)
        i_letter_rect = pygame.Rect(134,745,3,9)
        l_letter_rect1 = pygame.Rect(139,745,3,9)
        l_letter_rect2 = pygame.Rect(l_letter_rect1.left,l_letter_rect1.bottom-3,9,3)
        pygame.draw.rect(display,oil_colour,body)
        pygame.draw.rect(display,oil_lip_colour,top_lip)
        pygame.draw.rect(display,oil_lip_colour,bottom_lip)
        pygame.draw.rect(display,oil_stripe_colour,vertical_stripe)
        pygame.draw.rect(display,oil_stripe_colour,hor_stripe1)
        pygame.draw.rect(display,oil_stripe_colour,hor_stripe2)
        pygame.draw.circle(display,oil_stripe_colour,(127,749),5,width=3)
        pygame.draw.rect(display,oil_stripe_colour,i_letter_rect)
        pygame.draw.rect(display,oil_stripe_colour,l_letter_rect1)
        pygame.draw.rect(display,oil_stripe_colour,l_letter_rect2)
        pygame.draw.circle(display,platform_colour,(127,765),1)
        pygame.draw.circle(display,platform_colour,(133,765),1)
        pygame.draw.circle(display,platform_colour,(139,765),1)
        pygame.draw.circle(display,platform_colour,(145,765),1)

class Platform():
    def __init__(self,tile_x,tile_y,length):
        self.x = tile_x * tile_width
        self.y = tile_y * tile_height
        self.length = length
        self.rect = self.draw()

    def draw(self):
        line_width = 4
        for x_tile in range(self.length):
            left_side = self.x + x_tile * tile_width
            right_side = left_side + tile_width
            top_side = self.y
            bottom_side = self.y + tile_height
            mid_top = right_side - (tile_width * 0.5)
            pygame.draw.line(display,platform_colour,(left_side,top_side),(right_side,top_side),width=line_width)
            pygame.draw.line(display,platform_colour,(left_side,bottom_side),(right_side,bottom_side),width=line_width)
            pygame.draw.line(display,platform_colour,(left_side,bottom_side),(mid_top,top_side),width=line_width)
            pygame.draw.line(display,platform_colour,(right_side,bottom_side),(mid_top,top_side),width=line_width)
        return pygame.Rect(self.x,self.y,tile_width * self.length,tile_height)
        
class Ladder():
    def __init__(self,tile_x,tile_y,length,broken=False):
        self.x = tile_x * tile_width
        self.y = tile_y * tile_height
        self.length = length
        self.rect = self.draw()
        self.broken = broken

    def draw(self):
        ladder_colour = "light blue"
        ladder_thickness = 3
        ladder_factor = 0.8
        for y_tile in range(self.length):
            left_side = self.x
            right_side = self.x + (tile_width * ladder_factor)
            top_side = self.y + y_tile * tile_height * ladder_factor
            bottom_side = top_side + tile_height * ladder_factor
            middle = bottom_side - (tile_height * 0.5)
            pygame.draw.line(display,ladder_colour,(left_side,top_side),(left_side,bottom_side),width=ladder_thickness)
            pygame.draw.line(display,ladder_colour,(right_side,top_side),(right_side,bottom_side),width=ladder_thickness)
            pygame.draw.line(display,ladder_colour,(left_side,middle),(right_side,middle),width=ladder_thickness)
        return pygame.Rect(self.x,self.y,tile_width * ladder_factor,tile_height * self.length * ladder_factor)

class Peach():
    def __init__(self):
        self.frames = (peach1,peach2)
        self.reset()

    def reset(self):
        self.index = 0
        self.count = 0
        self.image = peach1

    def update(self):
        self.count += 1
        if self.count > 100:
            self.index += 1
            if self.index > len(self.frames)-1:
                self.index = 0
            self.image = self.frames[self.index]
            self.count = 0
            
    def draw(self):
        display.blit(self.image,(270,25))

class Barrel():
    def __init__(self,x,y):
        self.image = barrel1
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        self.below = pygame.Rect(self.rect.left,self.rect.bottom-3,self.rect.width,3)
        self.above = pygame.Rect(self.rect.left,self.rect.top-70,self.rect.width,40)
        self.x_speed = 1.5
        self.y_speed = 0
        self.rotate_dir = 1
        self.angle = 0
        self.rotate_state = 0
        self.count = 0

    def handle_collision(self):
        for platform in platforms:
            if self.below.colliderect(platform.rect):
                if self.y > row6_y and self.y < row5_y:
                    self.x_speed = -2
                if self.y > row5_y and self.y < row4_y:
                    self.x_speed = 2
                if self.y > row4_y and self.y < row3_y:
                    self.x_speed = -2
                if self.y > row3_y and self.y < row2_y:
                    self.x_speed = 2
                if self.y > row2_y:
                    self.x_speed = -2
                self.y_speed = 0
                self.y = platform.rect.top - self.rect.height / 2 + 1
        self.y_speed += 1
        self.x += self.x_speed
        self.y += self.y_speed
        self.above.center = (self.x,self.y-50)

    def rotate(self):
        if self.rotate_dir == 1:
            self.angle = self.rotate_state * 90
            self.count += 1
            if self.count > 35:
                self.rotate_state += 1
                if self.rotate_state > 4:
                    self.rotate_state = 1
                self.count = 0
            self.image = pygame.transform.rotate(barrel1,self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = (self.x,self.y)
            self.below = pygame.Rect(self.rect.left,self.rect.bottom-2,self.rect.width,2)

    def update(self):
        self.handle_collision()
        self.rotate()
    
    def draw(self):
        display.blit(self.image,self.rect)
                
class Kong():
    def __init__(self):
        self.reset()

    def reset(self):
        self.image = dk_image2
        self.barrel_spawn_time = 360
        self.barrel_count = self.barrel_spawn_time / 2
        self.barrel_time = 360
        self.barrels = []
        self.victory_rect = pygame.Rect(300,25,50,50)
        self.level_passed = False
        self.level_timer = 0
        self.level_load_time = 5
        
    def update(self):
        if not self.level_passed:
            self.pickup_barrel()
            self.throw_barrel()
        else:
            self.image = dk_image2
        if player.hitbox.colliderect(self.victory_rect) and not self.level_passed:
            self.level_passed = True
            self.level_timer = pygame.time.get_ticks()/1000
            self.barrels.clear()
            fire_balls.empty()

    def throw_barrel(self):
        if self.barrel_count < self.barrel_spawn_time:
            self.barrel_count += 1
        else:
            self.barrel_count = random.randint(0,93)
            barrel = Barrel(220,98)
            self.barrels.append(barrel)
            self.barrel_time = self.barrel_spawn_time - self.barrel_count

    def pickup_barrel(self):
        barrel_time_fraction = self.barrel_time // 4
        if self.barrel_spawn_time - self.barrel_count > 3 * barrel_time_fraction:
            self.image = dk_image2
        elif self.barrel_spawn_time - self.barrel_count > 2 * barrel_time_fraction:
            self.image = dk_image1
        elif self.barrel_spawn_time - self.barrel_count > barrel_time_fraction:
            self.image = dk_image3
        else:
            self.image = dk_image1_flipped
            display.blit(barrel1,(220,98))
        for barrel in self.barrels[:]:
            barrel.update()
            if barrel.rect.top > total_tiles * tile_height:
                self.barrels.remove(barrel)
            
    def draw(self):
        draw_text("{0:06}".format(score),115,40,24)
        draw_text("HIGH SCORE",705,20,24,(255,0,0))
        draw_text("{0:06}".format(highscore),703,50,24)
        draw_text("L="+"{0:02}".format(level),600,40,24,(0,0,255))
        for barrel in self.barrels:
            barrel.draw()
        display.blit(self.image,(150,20))
        if self.level_passed:
            oil_drum.fire_ball_timer = pygame.time.get_ticks()/100
            draw_text("Victory!",380,400,55)
            if pygame.time.get_ticks()/1000 - self.level_timer > self.level_load_time:
                reset_game()
            

class Hammer():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = hammer
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

    def draw(self):
        display.blit(self.image,self.rect)
        

class Player():
    def __init__(self,x_tile,y_tile):
        pygame.sprite.Sprite.__init__(self)
        self.animations = {"standing_right":(mario_standing,),"standing_left":(mario_standing_left,),
                           "running_right":(mario_standing,mario_running),
                           "running_left":(mario_standing_left,mario_running_left),
                           "climbing":(mario_climbing1,mario_climbing2),"jumping_right":(mario_jumping,),"jumping_left":(mario_jumping_left,),
                           "hammer":(mario_hammer,mario_hammer_overhead),"hammer_left":(mario_hammer_left,mario_hammer_overhead_left),
                           "hammer_jump":(mario_hammer_jump,),"hammer_jump_left":(mario_hammer_jump_left,)}
        self.jump_power = 7.35
        self.hammer_dur = 8
        self.score_vel = 1
        self.show_time = 0.5
        self.reset(x_tile,y_tile)

    def reset(self,x_tile,y_tile):
        self.x = x_tile * tile_width
        self.y = y_tile * tile_height
        self.index = 0
        self.count = 0
        self.image = self.animations["running_right"][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.hitbox = pygame.Rect(self.rect.left+15,self.rect.top,self.rect.width-25,self.rect.height-20)
        self.bottom = pygame.Rect(self.rect.left,self.rect.bottom-6,self.rect.width,6)
        self.x_speed = 160
        self.y_speed = 0
        self.dir = 1
        self.on_ground = False
        self.running = False
        self.climbing = False
        self.jumping = False
        self.has_hammer = False
        self.draw_score = False
        self.hammers = [Hammer(110,375),Hammer(115,185)]
        self.hammer_time = 0
        self.score_x = self.rect.centerx
        self.score_y = self.rect.centery
        self.score_time = 0
        
    def move_keyboard(self,keys):
        if keys[pygame.K_d] and not self.climbing:
            self.dir = 1
            self.running = True
            self.x += self.x_speed * delta_time
            if not self.jumping and not self.has_hammer:
                self.start_animation("running_right")
        elif keys[pygame.K_a] and not self.climbing:
            self.dir = -1
            self.running = True
            self.x -= self.x_speed * delta_time
            if not self.jumping and not self.has_hammer:
                self.start_animation("running_left")
        self.jump_keyboard(keys)

    def jump_keyboard(self,keys):
        if keys[pygame.K_SPACE] and not self.jumping:
            self.on_ground = False
            self.jumping = True
            self.y_speed = -self.jump_power
        if self.jumping and not self.has_hammer:
            if self.dir == 1:
               self.start_animation("jumping_right")
            else:
               self.start_animation("jumping_left")

    def climb_keyboard(self,keys):
        for ladder in ladders:
            if ladder.rect.colliderect(self.rect) and not ladder.broken and not self.jumping \
               and not self.has_hammer:
                if keys[pygame.K_w]:
                    self.climb(ladder)

    def move_controller(self):
        for joystick in joysticks:
            horizontal = joystick.get_axis(0)
            if horizontal < -0.4 and not self.climbing:
                self.dir = -1
                self.running = True
                self.x -= self.x_speed * delta_time
                if not self.jumping and not self.has_hammer:
                   self.start_animation("running_left")
            elif horizontal > 0.4 and not self.climbing:
                self.dir = 1
                self.running = True
                self.x += self.x_speed * delta_time
                if not self.jumping and not self.has_hammer:
                   self.start_animation("running_right")
            self.jump_controller(joystick)

    def jump_controller(self,joystick):
        if joystick.get_button(0) and not self.jumping:
            self.on_ground = False
            self.jumping = True
            self.y_speed = -self.jump_power
        if self.jumping and not self.has_hammer:
            if self.dir == 1:
               self.start_animation("jumping_right")
            else:
               self.start_animation("jumping_left")

    def climb_controller(self):
        for joystick in joysticks:
            vertical = joystick.get_axis(1)
            for ladder in ladders:
                if ladder.rect.colliderect(self.rect) and not ladder.broken and not self.jumping \
                   and not self.has_hammer:
                    if vertical < -0.4:
                       self.climb(ladder)
                       
    def climb(self,ladder):
        self.climbing = True
        self.x = ladder.rect.centerx
        self.y -= 2
        self.rect.center = (self.x,self.y)
        self.hitbox.center = (self.x,self.y)
        self.bottom = pygame.Rect(self.rect.left,self.rect.bottom-6,self.rect.width,6)
        self.start_animation("climbing")
                
    def start_animation(self,animation, max_count=5):
        self.count += 1
        if self.count > max_count:
            self.index += 1
            if self.index > len(self.animations[animation])-1:
                self.index = 0
            self.image = self.animations[animation][self.index]
            self.rect = self.image.get_rect()
            self.rect.center = (self.x,self.y)
            self.bottom = pygame.Rect(self.rect.left,self.rect.bottom-6,self.rect.width,6)
            self.count = 0
            
    def handle_platform_collisions(self):
        for platform in platforms:
            if self.bottom.colliderect(platform.rect) and self.y_speed >= 0:
                self.on_ground = True
                self.climbing = False
                self.jumping = False
                self.y_speed = 0
                self.y = platform.rect.top - self.rect.height / 2 + 1

    def handle_hammer_collisions(self):
        for hammer in self.hammers[:]:
            if hammer.rect.colliderect(player.rect) and not self.climbing:
                self.has_hammer = True
                self.hammer_time = pygame.time.get_ticks()/1000
                self.hammers.remove(hammer)
        if pygame.time.get_ticks()/1000 - self.hammer_time > self.hammer_dur:
            self.has_hammer = False
            self.hammer_time = pygame.time.get_ticks()/1000
                
    def generate_score_text(self):
        global score
        player_rect = None
        for barrel in kong.barrels[:]:
            if self.has_hammer:
                if self.jumping:
                    player_rect = self.hitbox
                    if barrel.rect.bottom > self.hitbox.top+25:
                        score_rect = barrel.above
                    else:
                        score_rect = barrel.rect
                else:
                    player_rect = self.rect
                    score_rect = barrel.rect
            else:
                score_rect = barrel.above
                player_rect = self.hitbox
            if score_rect.colliderect(player_rect) and not self.draw_score and not self.climbing:
                self.score_x = barrel.rect.centerx
                self.score_y = barrel.rect.centery-30
                self.score_time = pygame.time.get_ticks()/1000
                score += 100
                self.draw_score = True
                if score_rect == barrel.rect:
                    kong.barrels.remove(barrel)
        for barrel in kong.barrels[:]:
           if player_rect != None:
              if player_rect.colliderect(barrel.rect):
                    reset_game()
        if pygame.time.get_ticks()/1000 - self.score_time > self.show_time:
            self.draw_score = False
            self.score_time = pygame.time.get_ticks()/1000

    def run_animations(self):
        if not self.running and not self.climbing and not self.jumping and not self.has_hammer:
            if self.dir == 1:
                self.start_animation("standing_right")
            elif self.dir == -1:
                self.start_animation("standing_left")
        elif self.has_hammer and not self.climbing:
            if self.dir == 1:
                self.start_animation("hammer",10)
            elif self.dir == -1:
                self.start_animation("hammer_left",10)

    def add_gravity(self):
        if not self.on_ground and not self.climbing:
            self.y_speed += 0.5
            self.y += self.y_speed

    def draw_hammers(self):
        for hammer in self.hammers:
            hammer.draw()

    def draw_barrel_text(self):
        if self.draw_score:
            score_text_image = barrel_font.render("100",True,(255,255,255))
            score_text_rect = score_text_image.get_rect()
            self.score_y -= self.score_vel
            score_text_rect.center = (self.score_x,self.score_y)
            display.blit(score_text_image,score_text_rect)

    def detect_off_screen(self):
        if self.rect.top > display_height + 400:
            reset_game()
                
    def update(self):
        self.on_ground = False
        self.running = False
        keys = pygame.key.get_pressed()
        self.climb_keyboard(keys)
        self.climb_controller()
        self.handle_platform_collisions()
        self.move_keyboard(keys)
        self.move_controller()
        self.generate_score_text()
        self.handle_hammer_collisions()
        self.run_animations()
        self.add_gravity()
        self.rect.center = (self.x,self.y)
        self.hitbox.center = (self.x,self.y)
        self.bottom = pygame.Rect(self.rect.left,self.rect.bottom-6,self.rect.width,6)
        self.detect_off_screen()

    def draw(self):
        self.draw_hammers()
        display.blit(self.image,self.rect)
        self.draw_barrel_text()

platforms = (Platform(2,total_tiles-1,13),Platform(15,total_tiles-1.2,3),
                          Platform(18,total_tiles-1.4,3),Platform(21,total_tiles-1.6,3),Platform(24,total_tiles-1.9,3),Platform(27,total_tiles-2.2,3),
                          Platform(2,total_tiles-8,2),Platform(4,total_tiles-8+0.2,3),Platform(7,total_tiles-8+0.4,3),Platform(10,total_tiles-8+0.8,3),
                          Platform(13,total_tiles-8+1.2,3),Platform(16,total_tiles-8+1.4,3),Platform(19,total_tiles-8+1.6,3),Platform(22,total_tiles-8+1.8,3),Platform(25,total_tiles-8+2,3),
                          Platform(4,total_tiles-12,3),Platform(7,total_tiles-12-0.2,3),Platform(10,total_tiles-12-0.4,3),Platform(13,total_tiles-12-0.6,3),Platform(16,total_tiles-12-0.8,3),
                          Platform(19,total_tiles-12-1,3),Platform(22,total_tiles-12-1.2,3),Platform(25,total_tiles-12-1.4,3),Platform(28,total_tiles-12-1.6,2),Platform(25,total_tiles-18,3),
                          Platform(22,total_tiles-18-0.2,3),Platform(19,total_tiles-18-0.4,3),Platform(16,total_tiles-18-0.6,3),Platform(13,total_tiles-18-0.8,3),Platform(10,total_tiles-18-1,3),Platform(7,total_tiles-18-1.2,3),
                          Platform(4,total_tiles-18-1.4,3),Platform(2,total_tiles-18-1.6,2),Platform(4,total_tiles-23,6),Platform(10,total_tiles-23-0.2,6),Platform(16,total_tiles-23-0.4,6),Platform(22,total_tiles-23-0.6,7),
                          Platform(2,total_tiles-27,18),Platform(20,total_tiles-27+0.2,7),Platform(11,total_tiles-29,3))
ladders = (Ladder(25,total_tiles-8+2.9,4),Ladder(6,total_tiles-13+2,4),Ladder(12,total_tiles-6.3,2,True),Ladder(12,total_tiles-3+0.4,2,True),
           Ladder(14,total_tiles-12+0.4,6),Ladder(25,total_tiles-17+0.25,4),Ladder(16,total_tiles-18+0.3,6),Ladder(10,total_tiles-18,1,True),
           Ladder(10,total_tiles-15+0.2,3,True),Ladder(23,total_tiles-23+0.4,1,True),Ladder(23,total_tiles-20+0.2,2,True),Ladder(6,total_tiles-22+0.1,3),Ladder(12,total_tiles-22-0.3,4),
           Ladder(25,total_tiles-26,3),Ladder(14,total_tiles-26,1,True),Ladder(14,total_tiles-24,1,True))
kong = Kong()
player = Player(8,total_tiles-2)
peach = Peach()
background_ladders = (Ladder(9+0.1,0+0.1,6,True),Ladder(11+0.1,0+0.1,6,True))
oil_drum = OilDrum()

while running:
    delta_time = clock.tick(fps) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        if event.type == pygame.JOYDEVICEADDED:
            joystick = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joystick)
    display.fill("black")
    draw_background_ladders()
    draw_platforms()
    draw_ladders()
    fire_balls.update()
    player.update()
    oil_drum.update()
    draw_barrels()
    oil_drum.draw()
    peach.update()
    peach.draw()
    kong.update()
    player.draw()
    kong.draw()
    fire_balls.draw(display)
    pygame.display.flip()
pygame.quit()          
sys.exit()

