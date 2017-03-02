from enum import Enum, unique


@unique
class SerializeType(Enum):
    JSON = "JSON"
    XML = "XML"

    def describe(self):
        return self.name, self.value
