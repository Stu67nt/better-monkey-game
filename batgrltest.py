"""Render a pygame scene into a batgrl Graphics gadget (i.e. show pygame in your terminal).

The trick: pygame doesn't need a real window. We give it an offscreen
pygame.Surface, draw to that surface with normal pygame calls, then copy its
pixels (as a numpy array) into the Graphics gadget's `texture` array every
frame. batgrl takes care of turning that pixel array into terminal output.

Install:
    pip install pygame batgrl

Run:
    python pygame_in_batgrl.py
"""

import asyncio
import os

# Tell SDL not to open a real window/display -- we only need pygame's
# software rendering, not an actual GUI window.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from batgrl.app import App
from batgrl.gadgets.graphics import Graphics


class PygameSurfaceGadget(Graphics):
    """A Graphics gadget backed by an offscreen pygame.Surface.

    Draw onto `gadget.surface` with normal pygame drawing calls, then call
    `gadget.blit_surface()` to push those pixels into the terminal texture.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pg_surface: pygame.Surface | None = None
        self._sync_surface_size()

    def _sync_surface_size(self) -> None:
        h, w, _ = self.texture.shape  # texture is already sized for the blitter
        self._pg_surface = pygame.Surface((w, h))

    def on_size(self) -> None:
        super().on_size()
        self._sync_surface_size()

    @property
    def surface(self) -> pygame.Surface:
        return self._pg_surface

    def blit_surface(self) -> None:
        """Copy the pygame surface's pixels into the gadget's texture."""
        rgb = pygame.surfarray.array3d(self._pg_surface)  # shape (W, H, 3)
        rgb = rgb.transpose(1, 0, 2)  # -> (H, W, 3) to match texture layout
        self.texture[..., :3] = rgb
        self.texture[..., 3] = 255  # fully opaque


class PygameApp(App):
    async def on_start(self):
        pygame.init()

        # "sextant" blitter = 2x3 sub-pixels per terminal cell, decent
        # resolution/compatibility tradeoff. Try "sixel" for true pixel
        # graphics if your terminal supports it, or "half" for max
        # compatibility.
        gadget = PygameSurfaceGadget(size=(24, 60), blitter="half")
        self.add_gadget(gadget)

        player = Player((WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
        players = Group()
        players.add(player)

        enemies = Group()

        player_bullets = Group()
        test_bullet = PlayerBullet((WIDTH / 2, HEIGHT / 2), (0, 1))
        player_bullets.add(test_bullet)

        for _ in range(20):
            e = Enemy((
                random.randint(0, WIDTH), random.randint(0, HEIGHT)
            ))
            enemies.add(e)

        async def game_loop():

            while running:
                # poll for events
                # pygame.QUIT event means the user clicked X to close your window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        player.throw_banana(player_bullets)

                e = Enemy((
                    random.randint(0, WIDTH), random.randint(0, HEIGHT)
                ))
                enemies.add(e)

                players.update(dt=dt)
                enemies.update(player=player, dt=dt)
                player_bullets.update(dt=dt, enemies=enemies)

                hits = pygame.sprite.spritecollide(player, enemies, dokill=False)
                for monkey in hits: player.hit(0.01)

                #    hits =

                # fill the screen with a color to wipe away anything from last frame
                screen.fill("green")
                env.tileBackground(screen, env.bg)
                # pygame.draw.circle(screen, "orange", player_pos, 40)

                players.draw(screen)
                enemies.draw(screen)
                player_bullets.draw(screen)

                env.frame_count += 1
                screen.blit(env.get_time_text(screen), (0, 0))

                # flip() the display to put your work on screen
                pygame.display.flip()

                # limits FPS to 60
                # dt is delta time in seconds since last frame, used for framerate-
                # independent physics.

                dt = clock.tick(FPS) / 1000

        asyncio.create_task(game_loop())


if __name__ == "__main__":
    PygameApp(title="pygame in batgrl").run()