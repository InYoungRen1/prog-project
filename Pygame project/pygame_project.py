import pygame
import random

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "<Escape>"

background_image = pygame.image.load("./image/background.png")
background_image = pygame.transform.scale(background_image, (800, 600))

# class
class Player(pygame.sprite.Sprite):
    """ This class represents the player """

    # -- Methods
    def __init__(self):
        """ Constructor function """
        super().__init__()

        self.image = pygame.image.load("./image/oomba.png")
        self.image = pygame.transform.scale(self.image, (85,85))
        self.rect = self.image.get_rect()

        # speed vector of player
        self.vel_x = 0
        self.vel_y = 0

        self.jump_count = 0

        self.level = None

    def update(self):
        """move the player"""
        # gravity
        self.calc_grav()

        # left and right
        self.rect.x += self.vel_x

        # up and down
        self.rect.y += self.vel_y

    def calc_grav(self):
        """effect of gravity"""
        if self.vel_y == 0:
            self.vel_y = 1
        else:
            self.vel_y += .35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.jump_count = 0

    def jump(self):
        """jump"""
        # set jump to 1
        # if jump count is 1, then don't jump
        if self.jump_count != 1:
            self.jump_count += 1
            self.vel_y = -10

    # player controlled movement
    def go_left(self):
        self.vel_x = -6

    def go_right(self):
        self.vel_x = 6

    def stop(self):
        self.vel_x = 0

class Mario(pygame.sprite.Sprite):
    """Enemy what walks at the bottom"""
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./image/mario.png.jpg")
        self.image = pygame.transform.scale(self.image, (85, 85))
        self.rect = self.image.get_rect()
        self.x_vel = 3

    def update(self):
        self.rect.x += self.x_vel
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.x_vel *= -1

class Gold_coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./image/gold_coin.png")
        self.image = pygame.transform.scale(self.image, (21, 36))
        self.rect = self.image.get_rect()

      # random location
        self.rect.x = random.randrange(0, SCREEN_WIDTH)
        self.rect.y = random.randrange(50, SCREEN_HEIGHT)
        self.y_vel = random.randrange(1, 3)

    def update(self):
        """move gold coin down"""
        self.rect.y += self.y_vel



def main():
    pygame.init()

    # ----- SCREEN PROPERTIES9+
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

   # sprite groups
    all_sprite = pygame.sprite.Group()
    mario_sprite = pygame.sprite.Group()
    gold_coin_sprites = pygame.sprite.Group()
    # popular sprite Groups
    mario = Mario()
    mario.rect.y = SCREEN_HEIGHT - mario.rect.height
    all_sprite.add(mario)
    player = Player()
    all_sprite.add(player)


    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.vel_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.vel_x > 0:
                    player.stop()

            if len(gold_coin_sprites) <= 6:
                gold_coin = Gold_coin()
                all_sprite.add(gold_coin)
                gold_coin_sprites.add(gold_coin)

        # ----- LOGIC
        all_sprite.update()
        # ----- DRAW
        screen.fill(WHITE)
        screen.blit(background_image, [0,0])
        all_sprite.draw(screen)
        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

        # remove gold coin
        for gold_coin in gold_coin_sprites:
            if gold_coin.rect.y < 0:
                gold_coin.kill()
        # collision
        mario_hit_group = pygame.sprite.spritecollide(player, mario_sprite, True)
        if len(mario_hit_group) > 0:
            player.kill()
    pygame.quit()


if __name__ == "__main__":
    main()