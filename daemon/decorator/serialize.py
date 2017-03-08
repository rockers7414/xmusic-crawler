import json
import datetime

from enumtype.serializetype import SerializeType


def serializeController(type):

    def serializeRow(row):
        jsonObj = {}

        for key, value in row.__dict__.items():
            if key.startswith('_'):
                continue

            if(isinstance(value, list)):
                inner_jsonObj = []
                for _row in value:
                     inner_jsonObj.append(serializeRow(_row))
                jsonObj[key] = inner_jsonObj
            elif(isinstance(value, datetime.datetime)):
                time_str = value.strftime('%Y-%m-%d %H:%M:%S')
                jsonObj[key] = time_str
            else:
                jsonObj[key] = value

        return jsonObj

    def serialize(function):
        def toJSON():
            entitys = function()

            jsonArray = []

            for row in entitys:
                jsonArray.append(serializeRow(row))

            # return json.dumps(jsonArray)
            return jsonArray

        def toXML():
            pass

        if (type.upper() == SerializeType.JSON.value):
            return toJSON
        elif (type.upper() == SerializeType.XML.value):
            return toXML
        else:
            raise NotImplementedError(
                'the serialize type "' + type + '" is unsupported.')

    return serialize
