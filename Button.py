import pygame
from pygame.locals import *

pygame.font.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (64, 64, 64)
GRAY = (128, 128, 128)
LIGHTGRAY = (62, 65, 73)
YELLOW = (209, 190, 0)
GREEN = (114, 192, 83)
RED = (218, 87, 102)
PYGBUTTON_FONT = pygame.font.Font('Comfortaa-Medium.ttf', 60)


class Button:
    def __init__(self, surface, rect=(30, 30, 30, 30), bg_color=WHITE, fg_color=BLACK, caption="", hover_effect=True,
                 click_effect=True, hover_color_bg=LIGHTGRAY, click_color=DARKGRAY, visible=True, active=True,
                 displacement_fg_x=0, displacement_fg_y=0, border_rounding=8, border=True, border_width=2,
                 border_color=DARKGRAY, font=PYGBUTTON_FONT, only_fg=False, hover_color_fg=LIGHTGRAY,
                 clicked_color_bg=DARKGRAY, clicked_color_fg=GRAY, bg_clarity=255, border_clarity=255):
        self.rect = rect
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.caption = caption
        self.hover_effect = hover_effect
        self.click_effect = click_effect
        self.hover_color_bg = hover_color_bg
        self.click_color = click_color
        self.visible = visible
        self.active = active
        self.displacement_fg_x = displacement_fg_x
        self.displacement_fg_y = displacement_fg_y
        self.border_rounding = border_rounding
        self.border = border
        self.border_color = border_color
        self.border_width = border_width
        self.surface = surface
        self.font = font
        self._circle_cache = {}
        self.only_fg = only_fg
        self.mouseOverButton = False
        self.buttonDown = False
        self.hover_color_fg = hover_color_fg
        self.bg_color_copy = self.bg_color
        self.fg_color_copy = self.fg_color
        self.clicked_color_bg = clicked_color_bg
        self.clicked_color_fg = clicked_color_fg
        self.click = False
        self.bg_clarity = bg_clarity
        self.border_clarity = border_clarity
        self.state_hover = False

    def set_rect(self, rect):
        self.rect = rect

    def get_rect(self):
        return self.rect

    def set_bg_color(self, color):
        self.bg_color = color

    def get_bg_color(self):
        return self.bg_color

    def set_fg_color(self, color):
        self.fg_color = color

    def get_fg_color(self):
        return self.fg_color

    def set_caption(self, caption):
        self.caption = caption

    def get_caption(self):
        return self.caption

    def set_hover_effect(self, True_or_False):
        self.hover_effect = True_or_False

    def get_hover_effect(self):
        return self.hover_effect

    def set_click_effect(self, True_or_False):
        self.click_effect = True_or_False

    def get_click_effect(self):
        return self.click_effect

    def set_visible(self, True_or_False):
        self.visible = True_or_False

    def get_visible(self):
        return self.visible

    def set_active(self, True_or_False):
        self.active = True_or_False

    def get_active(self):
        return self.active

    def set_displacement_fg_x(self, displacement_fg_x):
        self.displacement_fg_x = displacement_fg_x

    def get_displacement_fg_x(self):
        return self.displacement_fg_x

    def set_displacement_fg_y(self, displacement_fg_y):
        self.displacement_fg_y = displacement_fg_y

    def get_displacement_fg_y(self):
        return self.displacement_fg_y

    def set_border_rounding(self, border_rounding):
        self.border_rounding = border_rounding

    def get_border_border_rounding(self):
        return self.border_rounding

    def set_border(self, True_or_False):
        self.border = True_or_False

    def get_border(self):
        return self.border

    def set_bg_clarity(self, bg_clarity):
        self.bg_clarity = bg_clarity

    def get_bg_clarity(self):
        return self.bg_clarity

    def set_border_clarity(self, border_clarity):
        self.border_clarity = border_clarity

    def get_border_clarity(self):
        return self.border_clarity

    def set_border_color(self, border_color):
        self.border_color = border_color

    def get_border_color(self):
        return self.border_color

    def set_border_width(self, border_width):
        self.border_width = border_width

    def get_border_width(self):
        return self.border_width

    def set_surface(self, surface):
        self.surface = surface

    def get_surface(self):
        return self.surface

    def set_font(self, font):
        self.font = font

    def get_font(self):
        return self.font

    def set_only_fg(self, True_or_False):
        self.only_fg = True_or_False

    def get_only_fg(self):
        return self.only_fg

    def set_hover_color_bg(self, hover_color_bg):
        self.hover_color_bg = hover_color_bg

    def get_hover_color_bg(self):
        return self.hover_color_bg

    def set_hover_color_fg(self, hover_color_fg):
        self.hover_color_fg = hover_color_fg

    def get_hover_color_fg(self):
        return self.hover_color_fg

    def set_clicked_color_bg(self, clicked_color_bg):
        self.clicked_color_bg = clicked_color_bg

    def get_clicked_color_bg(self):
        return self.clicked_color_bg

    def set_clicked_color_fg(self, clicked_color_fg):
        self.clicked_color_fg = clicked_color_fg

    def get_clicked_color_fg(self):
        return self.clicked_color_fg

    def get_click(self):
        return self.click

    def get_hover(self):
        return self.state_hover

    def set_state_hover(self, state_hover):
        self.state_hover = state_hover

    def _circlepoints(self, r):
        r = int(round(r))
        if r in self._circle_cache:
            return self._circle_cache[r]
        x, y, e = r, 0, 1 - r
        self._circle_cache[r] = points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points

    def render(self, text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(0, 0, 0), opx=5):
        textsurface = font.render(text, True, gfcolor).convert_alpha()
        w = textsurface.get_width() + 2 * opx
        h = font.get_height()

        osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
        osurf.fill((0, 0, 0, 0))

        surf = osurf.copy()

        osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

        for dx, dy in self._circlepoints(opx):
            surf.blit(osurf, (dx + opx, dy + opx))

        surf.blit(textsurface, (opx, opx))
        return surf

    def draw(self):
        if not self.visible:
            return

        background = pygame.rect.Rect(self.rect)
        self.background = background
        if not self.only_fg:
            pygame.draw.rect(self.surface, self.bg_color, background, 0, self.border_rounding)

            if self.border:
                border = pygame.rect.Rect(self.rect[0] - self.border_width, self.rect[1] - self.border_width,
                                          self.rect[2] + 2 * self.border_width, self.rect[3] + 2 * self.border_width)
                pygame.draw.rect(self.surface, self.border_color, border, self.border_width,
                                 self.border_rounding + self.border_width)

        caption = self.render(self.caption, self.font, opx=1, gfcolor=self.fg_color)
        self.surface.blit(caption, (self.rect[0] + self.displacement_fg_x, self.rect[1] + self.displacement_fg_y))

    def events(self, event):
        self.click = False
        if self.visible == True and self.active == True and self.background:
            if event.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                return
            if not self.mouseOverButton and self.background.collidepoint(event.pos):
                self.mouseOverButton = True
                self.mouseEnter()
                if self.hover_effect:
                    self.hover()
            elif self.mouseOverButton and not self.background.collidepoint(event.pos):
                self.mouseOverButton = False
                self.mouseExit()
                if self.hover_effect:
                    self.normal()

            if self.background.collidepoint(event.pos):
                if event.type == MOUSEBUTTONDOWN:
                    self.buttonDown = True
                    self.button_down()
                    self.clicked()
            if self.buttonDown and event.type == MOUSEBUTTONUP:
                self.buttonDown = False
                self.normal()
                self.button_up(event)

    def mouseEnter(self):
        self.set_state_hover(True)

    def normal(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.bg_color = self.bg_color_copy
        self.fg_color = self.fg_color_copy

    def hover(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        self.bg_color = self.hover_color_bg
        self.fg_color = self.hover_color_fg

    def clicked(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        self.bg_color = self.clicked_color_bg
        self.fg_color = self.clicked_color_fg

    def mouseExit(self):
        self.set_state_hover(False)

    def button_down(self):
        return self.buttonDown

    def button_up(self, event):
        if self.background.collidepoint(event.pos):
            self.hover()
            self.set_click()

    def set_click(self):
        self.click = True

    def get_state_hover(self):
        return self.state_hover
