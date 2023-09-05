from pygame import display, init
from pygame.draw import rect
from pygame.font import Font

init()

font = Font(None, 30)


def debug(info, y=10, x=10):
    display_surface = display.get_surface()

    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))

    rect(display_surface, 'Black', debug_rect)

    display_surface.blit(debug_surf, debug_rect)