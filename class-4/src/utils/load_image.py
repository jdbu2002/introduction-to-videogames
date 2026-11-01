from os import path

from pygame.image import load


def load_image(rel_path: str):
    """
    This function is only to ensure path resolves, because i'm working in
    a shared environment with all the classes and exercises, so the
    `assets/img/path.png` does not resolve correctly by putting it directly.
    """
    file_path = path.dirname(path.abspath(__file__))
    image_path = path.join(file_path, "../..", rel_path)

    return load(image_path).convert_alpha()
