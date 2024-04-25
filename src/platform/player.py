import pygame


class Player(pygame.sprite.Sprite):
    COLORKEY = (0, 0, 0)
    SCALE_FACTOR = 4
    TILE_SIZE = 16
    WALK_ANIM_FRAMES = 7
    WALK_ANIM_WIDTH = 29 * SCALE_FACTOR
    WALK_ANIM_HEIGHT = 48 * SCALE_FACTOR
    ANIM_CYCLES_PER_SECOND = 1
    ANIM_RATE = (1/ANIM_CYCLES_PER_SECOND)*1000

    def __init__(self, pos):
        super().__init__()
        self.clock = pygame.time.Clock
        self.last_time = 0
        self.sheet = pygame.transform.scale_by(
            pygame.image.load(f'../art/platforming_sprites/mc_walk_cycle.png'),
            self.SCALE_FACTOR
        )
        self.sheet.set_colorkey((0, 0, 0))
        self.image = None
        self.key_frame = 2  # initial value only
        self._next_in_sheet()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1] - self.TILE_SIZE * self.SCALE_FACTOR * 2
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0.1
        self.speed_x = 8
        self.speed_y = 1
        self.preserve_y = 0  # for jumping purposes
        self.max_jump_height = self.TILE_SIZE * self.SCALE_FACTOR * 5
        self.move_right, self.move_left = False, False
        self.move_up, self.move_down = False, False
        self.jumping = False

    def check_bounds(self, screen):
        if self.rect.x + self.rect.w > screen.get_width():
            self.rect.x = 0
            return 'right'
        if self.rect.x < 0:
            self.rect.x = screen.get_width()
            return 'left'
        if self.rect.y > screen.get_height():
            self.rect.y = 0
            return 'down'
        if self.rect.y < 0:
            self.rect.y = screen.get_height()
            return 'up'
        return None

    def moving(self, direction):
        if direction == 'right':
            self.move_right = True
        elif direction == 'left':
            self.move_left = True
        elif direction == 'up':
            pass  # intentionally left blank
        elif direction == 'down':
            self.move_down = True

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.preserve_y = self.rect.y
            self.speed_y = -37  # don't touch

    def jump_update(self):
        # ascent
        if self.speed_y <= -1:
            self.speed_y *= (1 - self.gravity)
        # apex reached
        if self.rect.y < self.preserve_y - self.max_jump_height:
            self.move_down = True
            self.speed_y = 1
        # descent
        if self.speed_y >= 1:
            self.speed_y *= (1 + self.gravity)

    def halt(self, direction):
        if direction == 'right':
            self.rect.x -= 1
            self.move_right = False
        elif direction == 'left':
            self.rect.x += 1
            self.move_left = False
        elif direction == 'down':
            self.rect.y -= 1
            self.jumping = False
            self.move_down = False
            self.speed_y = 0
        elif direction == 'up':
            self.rect.y += 1
            self.move_down = True
            self.speed_y = 10

    def collide(self, rect):
        if rect.x <= self.rect.x:
            self.halt('right')
        if rect.x <= self.rect.x + self.rect.w:
            self.halt('left')
        if rect.y < self.rect.y + self.rect.height:
            self.halt('down')
        if rect.y < self.rect.y:
            self.halt('up')

    def update(self):
        if self.jumping:
            self.jump_update()
            self.rect.y += self.speed_y
        elif self.move_down: self.rect.y += self.speed_y
        if self.move_right: self.rect.x += self.speed_x
        if self.move_left: self.rect.x -= self.speed_x
        # self._next_in_sheet()

    def get_image(self):
        return self.image

    def _next_in_sheet(self):
        # if (self.clock.tick() - self.last_time) > self.ANIM_RATE:
        #     self.last_time = pygame.time.get_ticks()
        #     self.key_frame += 1

        self.key_frame = (self.key_frame + 1) % self.WALK_ANIM_FRAMES
        rect = pygame.Rect(
            self.key_frame * self.WALK_ANIM_WIDTH,
            0,
            self.WALK_ANIM_WIDTH,
            self.WALK_ANIM_HEIGHT
        )
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(self.COLORKEY, pygame.RLEACCEL)
        self.image = image

    def get_rect(self):
        return self.rect

    def is_jumping(self):
        return self.jumping
