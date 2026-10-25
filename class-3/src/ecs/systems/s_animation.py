from esper import World

from src.ecs.components import CAnimation, CSurface


def system_animation(world: World, delta_time: float):
    components = world.get_components(CSurface, CAnimation)

    for _, (c_s, c_a) in components:
        c_a.current_animation_time -= delta_time

        if c_a.current_animation_time <= 0:
            animation = c_a.animations_list[c_a.current_animation]

            c_a.current_animation_time = animation.framerate
            c_a.current_frame += 1

            if c_a.current_frame > animation.end:
                c_a.current_frame = animation.start

            rect_surf = c_s.surf.get_rect()
            c_s.area.w = rect_surf.w / c_a.number_frames
            c_s.area.x = c_s.area.w * c_a.current_frame
