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

        pos = pygame.Vector2(50, 50)
        vel = pygame.Vector2(2.0, 1.5)
        radius = 15

        async def game_loop():
            while True:
                surf = gadget.surface
                w, h = surf.get_size()

                # ---- ordinary pygame code goes here ----
                pos += vel
                if pos.x - radius < 0 or pos.x + radius > w:
                    vel.x *= -1
                if pos.y - radius < 0 or pos.y + radius > h:
                    vel.y *= -1

                surf.fill((10, 10, 20))
                pygame.draw.circle(surf, (255, 90, 90), pos, radius)
                # ---- end pygame code ----

                gadget.blit_surface()
                await asyncio.sleep(1 / 30)

        asyncio.create_task(game_loop())


if __name__ == "__main__":
    PygameApp(title="pygame in batgrl").run()