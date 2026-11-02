from .services import ConfigsService, FontsService, ImagesService, SoundsService


class ServiceLocator:
    configs_service = ConfigsService()
    fonts_service = FontsService()
    images_service = ImagesService()
    sounds_service = SoundsService()
