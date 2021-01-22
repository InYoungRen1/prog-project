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

# class
class Player(pygame.sprite.Sprite):
    """ This class represents the player """

    # -- Methods
    def __init__(self):
        """ Constructor function """
        super().__init__()

        self.image = pygame.image.load("./image/oomba.png")
        self.rect = self.image.get_rect()

        # speed vector of player
        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        """move the player"""
        # gravity
        self.calc_grav()

        # left and right
        self.rect.x += self.vel_x

        # hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.vel_x > 0:
                self.rect.right = block.rect_left
            elif self.vel_x < 0:
                self.rect.left = block.rect.right

        # up and down
        self.rect.y += self.vel_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.vel_y > 0:
                self.rect.right = block.rect_top
            elif self.vel_y < 0:
                self.rect.left = block.rect.bottom
            # stop vertical movement
            self.vel_y = 0

    def calc_grav(self):
        """effect of gravity"""
        if self.vel_y == 0:
            self.vel_y = 1
        else:
            self.vel_y += .35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """jump"""
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= -2
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.vel_y = -10

    # player controlled movement
    def go_left(self):
        self.vel_y = -6

    def go_right(self):
        self.vel_x = 6

    def stop(self):
        self.vel_x = 0

def main():
    pygame.init()

    # ----- SCREEN PROPERTIES9+
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    player = Player()
    all_sprite_list = pygame.sprite.Group()
    all_sprite_list.add(player)

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

        # ----- LOGIC

        # ----- DRAW
        screen.fill(WHITE)
        screen.blit(background_image, [0,0])
        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()