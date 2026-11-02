import math

from esper import World
from pygame import Color, Rect

from src.ecs.components import CSpecial, CSurface, CText, CTransform
from src.ecs.components.tags import CTagSpecialBar, CTagSpecialText
from src.types import Interface
from src.types.common import Color as ColorCfg


def _color(cfg: ColorCfg):
    return Color(cfg["r"], cfg["g"], cfg["b"])


def system_special_hud(world: World, interface_cfg: Interface):
    hud = interface_cfg["special"]
    bar_cfg = hud["bar"]
    status_cfg = hud["status"]

    for _, c_sp in world.get_component(CSpecial):
        if c_sp.denied_time > 0:
            fill_color = _color(bar_cfg["color_denied"])
        elif c_sp.is_ready:
            pulse = (math.sin(c_sp.elapsed * 8) + 1) / 2
            fill_color = _color(bar_cfg["color_fill"]).lerp(
                _color(bar_cfg["color_ready"]), 0.5 + pulse / 2
            )
            if c_sp.ready_flash_time > 0:
                fill_color = Color(255, 255, 255)
        else:
            fill_color = _color(bar_cfg["color_fill"])

        for _, (c_s, _) in world.get_components(CSurface, CTagSpecialBar):
            c_s.surf.fill(_color(bar_cfg["color_bg"]))
            fill = Rect(0, 0, round(c_s.area.w * c_sp.charge), c_s.area.h)
            c_s.surf.fill(fill_color, fill)

        if c_sp.is_ready:
            text = status_cfg["text_ready"]
            text_color = _color(status_cfg["color_ready"])
        else:
            text = status_cfg["text"].format(c_sp.time_left)
            text_color = _color(status_cfg["color"])

        for _, (c_t, c_s, c_txt, _) in world.get_components(
            CTransform, CSurface, CText, CTagSpecialText
        ):
            c_s.surf = c_txt.font.render(text, False, text_color)
            c_s.area = c_s.surf.get_rect()
            c_t.pos = c_txt.get_anchored_pos(c_s.area)
