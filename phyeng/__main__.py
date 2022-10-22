import random
import typing as T

import pygame

GRAVITY = pygame.Vector2(0, 1)


class Ball(pygame.sprite.Sprite):
    radius = 25

    def __init__(self, pos: T.Tuple[int, int], velocity: pygame.Vector2,
                 color: pygame.Color, others: pygame.sprite.Group):
        super().__init__()
        self.fx, self.fy = float(pos[0]), float(pos[1])
        self.velocity = velocity
        self.new_velocity = velocity
        self.others = others

        self.image = pygame.Surface((self.radius * 2, self.radius * 2),
                                    pygame.SRCALPHA)
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])
        pygame.draw.circle(self.image, color, (self.radius, self.radius),
                           self.radius)

        self.area = pygame.display.get_surface().get_rect()

    def update(self):
        self.new_velocity = self.velocity + GRAVITY

        tl = not self.area.collidepoint(self.rect.topleft)
        tr = not self.area.collidepoint(self.rect.topright)
        bl = not self.area.collidepoint(self.rect.bottomleft)
        br = not self.area.collidepoint(self.rect.bottomright)

        if tl and bl or (tr and br):
            self.new_velocity = self.velocity.reflect(pygame.Vector2(1, 0)) / 2
        if bl and br:
            self.new_velocity = self.velocity.reflect(pygame.Vector2(0, 1)) / 2

        collides = pygame.sprite.spritecollide(self, self.others, False,
                                               pygame.sprite.collide_circle)
        collides.remove(self)
        for collide in collides:
            # https://stackoverflow.com/a/63187016
            v = self.velocity - collide.velocity
            try:
                self.new_velocity = self.velocity.reflect(v) / 2
                collide.new_velocity = collide.velocity.reflect(v) / 2
            except ValueError:
                # ValueError: Normal must not be of length zero.
                pass

    def update_state(self):
        self.velocity = self.new_velocity

        self.fx += self.velocity.x
        self.fy += self.velocity.y
        self.rect.x, self.rect.y = round(self.fx), round(self.fy)


def random_color() -> pygame.Color:
    return random.choice(list(pygame.colordict.THECOLORS.keys()))


def main() -> None:
    pygame.init()

    scr = pygame.display.set_mode((640, 480))
    bg = pygame.Surface(scr.get_size())
    bg.fill(pygame.Color('white'))

    balls_group = pygame.sprite.RenderUpdates()

    scr.blit(bg, (0, 0))
    pygame.display.flip()

    click_begin = (0, 0)

    balls_group.add(
        Ball((0, 0), pygame.Vector2(5, 0), random_color(), balls_group))
    balls_group.add(
        Ball((400, 0), pygame.Vector2(-5, 0), random_color(), balls_group))

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # reset
                    balls_group.empty()
                    pygame.display.update()
                    scr.blit(bg, bg.get_rect())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_begin = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                vx = (x - click_begin[0]) * 0.25
                vy = (y - click_begin[1]) * 0.25
                ball = Ball((x, y), pygame.Vector2(vx, vy), random_color(),
                            balls_group)
                balls_group.add(ball)

        for ball in balls_group:  # type: ignore
            scr.blit(bg, ball.rect)  # type: ignore

        balls_group.update()
        for i in balls_group:
            i.update_state()  # type: ignore
        balls_group.draw(scr)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
