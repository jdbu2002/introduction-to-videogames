from .services import ImagesService, SoundsService


class ServiceLocator:
    images_service = ImagesService()
    sounds_service = SoundsService()
