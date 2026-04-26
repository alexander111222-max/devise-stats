class StatsException(Exception):
    detail = "Произошла неизвестная ошибка"


class ObjectNotFoundException(BaseException):
    detail = "Объект не найден"


class ObjectCreationException(BaseException):
    detail = "Ошибка при создании объекта"


class UniqueConstraintException(ObjectCreationException):
    detail = "Объект с такими данными уже существует"


class DeviceNotFoundException(ObjectNotFoundException):
    detail = "Устройство не найдено"


class DeviceCreationException(ObjectCreationException):
    detail = "Ошибка при создании устройства"


class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь с таким email уже существует"


class UserAlreadyExistsException(BaseException):
    detail = "Пользователь с таким email уже существует"


class UserCreationException(ObjectCreationException):
    detail = "Ошибка при создании пользователя"


class MeasurementCreationException(ObjectCreationException):
    detail = "Ошибка при сохранении измерения"


class MeasurementsNotFoundException(ObjectNotFoundException):
    detail = "Измерения не найдены"


class AnalyticsNotFoundException(ObjectNotFoundException):
    detail = "Данные для аналитики не найдены"
