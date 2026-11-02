from typing import TypedDict

from .common import Color, ColorAlpha, Position
from .window import Size


class Text(TypedDict):
    font: str
    size: int
    color: Color
    text: str
    position: Position
    anchor: str


class SpecialStatus(Text):
    text_ready: str
    color_ready: Color


class SpecialBar(TypedDict):
    position: Position
    size: Size
    color_bg: Color
    color_fill: Color
    color_ready: Color
    color_denied: Color


class SpecialHud(TypedDict):
    label: Text
    status: SpecialStatus
    bar: SpecialBar


class Interface(TypedDict):
    title: Text
    instructions: Text
    paused: Text
    paused_hint: Text
    pause_overlay: ColorAlpha
    special: SpecialHud
