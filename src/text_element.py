import pygame

import src.static_sprite


class TextSprite(src.static_sprite.StaticSprite):
    """
    Any menu box item in the dating sim - dialog boxes, menu boxes, etc.
    MenuBox instances may include a listener, or may be static elements on the screen.
    """
    def __init__(self, x, y, width, height, path, consequence=0, content=None, visible=True, image='default'):
        super().__init__(path)
        self.wrapped_text = None
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_color = (0, 0, 0)
        self.text_antialias = True
        self.image = pygame.transform.scale(pygame.image.load(path), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.set_content(content)
        self.consequence = consequence

    def offset_text(self, offset):
        if self.content:
            text_surface = self.font.render(str(self.content), self.text_antialias, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.rect.x + offset[0], self.rect.y + offset[1])
            return text_surface, text_rect
        else:
            return None, None

    def get_content(self):
        return self.content

    def get_content_pos(self):
        return self.rect.x + self.rect.w/4, self.rect.y + self.rect.h/4

    def get_consequence(self):
        return self.consequence

    def set_content(self, content):
        self.content = str(content) if content else ""
        self.wrapped_text = self.content.split("\n")

    def render_wrapped(self, offset):
        if self.wrapped_text:
            rendered = []
            for i, line in enumerate(self.wrapped_text):
                text_surface = self.font.render(line, self.text_antialias, self.text_color)
                text_rect = text_surface.get_rect()
                text_rect.topleft = (self.rect.x + offset[0], self.rect.y + offset[1] + i * self.font.get_linesize())
                rendered.append((text_surface, text_rect))
            return rendered
        else:
            text_surface = self.font.render(str(self.content), self.text_antialias, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.rect.x + offset[0], self.rect.y + offset[1])
            return text_surface, text_rect


