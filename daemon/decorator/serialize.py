import json

from enum import Enum, unique


@unique
class SerializeType(Enum):
    JSON = "JSON"
    XML = "XML"

    def describe(self):
        return self.name, self.value


def serializeController(type):

    def serializeRow(row):
        jsonObj = {}

        for key, value in row.__dict__.items():
            if key.startswith('_'):
                continue

            if(isinstance(value, list)):
                for _row in value:
                    jsonObj[key] = serializeRow(_row)                
            else:
                jsonObj[key] = value

        return jsonObj

    def serialize(function):
        def toJSON():
            entitys = function()

            jsonArray = []

            for row in entitys:
               jsonArray.append(serializeRow(row))

            return json.dumps(jsonArray)

        def toXML():
            pass

        if (type.upper() == SerializeType.JSON.value):
            return toJSON
        elif (type.upper() == SerializeType.XML.value):
            return toXML

    return serialize
