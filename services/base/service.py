from types import FunctionType


class Config:
    """Пример класса конфигурации для сервисов.

    decorators - кортеж/список декораторов, которые будут применены к методам
    include - кортеж/список методов, будут декорированы только эти методы
    exclude - кортеж/список методов, будут декорированы все методы, кроме них
    """

    decorators = []
    include = []
    exclude = []


class Meta(type):
    """Метакласс для массового декорирования методов в классе сервиса.

    Чтобы метакласс сработал, нужно определить внутри класса сервиса класс Config
    (см. пример в модуле).
    """

    def __new__(cls, name, base, attrs):
        functions = [key for key in attrs if type(attrs[key]) == FunctionType]

        config = attrs.get("Config", Config)
        if config:
            if hasattr(config, "include"):
                functions = [key for key in functions if key in config.include]
            else:
                functions = [
                    key
                    for key in functions
                    if not key.startswith("__") and not key.endswith("__")
                ]
                if hasattr(config, "exclude"):
                    functions = [key for key in functions if key not in config.exclude]

            for func in functions:
                for dec in config.decorators:
                    attrs[func] = dec(attrs[func])

        return super().__new__(cls, name, base, attrs)


class BaseService(metaclass=Meta):
    """Базовый шаблон сервиса."""

    pass
