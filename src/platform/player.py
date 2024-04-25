import pygame


class Player(pygame.sprite.Sprite):
    COLORKEY = (0, 0, 0)
    SCALE_FACTOR = 4
    TILE_SIZE = 16
    WALK_ANIM_FRAMES = 7
    WALK_ANIM_WIDTH = TILE_SIZE * 3 * SCALE_FACTOR

    def __init__(self, pos):
        super().__init__()
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
        self.gravity = 0.15
        self.speed_x = 8
        self.speed_y = 3
        self.preserve_y = 0  # for jumping purposes
        self.max_jump_height = self.TILE_SIZE * self.SCALE_FACTOR * 5
        self.move_right, self.move_left = False, False
        self.jumping = False

    def update(self):
        if self.jumping: self.jump_update()
        if self.move_right: self.rect.x += self.speed_x
        if self.move_left: self.rect.x -= self.speed_x
        self.rect.y += self.speed_y

    def collide(self, rect):
        if rect.x <= self.rect.x: self.halt('right')
        if rect.x >= self.rect.x + self.rect.w: self.halt('left')
        if rect.y < self.rect.y + self.rect.height: self.halt('down')

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.preserve_y = self.rect.y
            self.speed_y = -30

    def jump_update(self):
        if self.rect.y < self.preserve_y + self.max_jump_height: pass

    def moving(self, direction):
        if direction == 'right': self.move_right = True
        elif direction == 'left': self.move_left = True

    def halt(self, direction):
        if direction == 'right':
            self.rect.x -= self.speed_x
            self.move_right = False
        elif direction == 'left':
            self.rect.x += self.speed_x
            self.move_left = False
        elif direction == 'down':
            self.rect.y -= self.speed_y
            self.jumping = False
            self.speed_y = 0

    def get_image(self):
        return self.image

    def _next_in_sheet(self):
        self.key_frame = (self.key_frame + 1) % self.WALK_ANIM_FRAMES
        rect = pygame.Rect(
            self.key_frame * self.WALK_ANIM_WIDTH,
            0,
            self.WALK_ANIM_WIDTH,
            self.WALK_ANIM_WIDTH
        )
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(self.COLORKEY, pygame.RLEACCEL)
        self.image = image

    def get_rect(self):
        return self.rect

    def is_jumping(self):
        return self.jumping
