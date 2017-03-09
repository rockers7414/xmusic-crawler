import json
import datetime

from enumtype.serializetype import SerializeType
from sqlalchemy.ext.declarative import DeclarativeMeta


def serializeController(type):

    def sqlalchemy_encoder():
        class SqlAlchemyEncoder(json.JSONEncoder):

            def default(self, obj):
                fields = {}
                if isinstance(obj.__class__, DeclarativeMeta):
                    # for sqlalchemy orm
                    for key, value in obj.__dict__.items():
                        if key.startswith('_'):
                            continue

                        if(isinstance(value, list)):
                            inner_jsonObj = []
                            for _row in value:
                                inner_jsonObj.append(self.default(_row))
                            fields[key] = inner_jsonObj
                        elif(isinstance(value, datetime.datetime)):
                            time_str = value.strftime('%Y-%m-%d %H:%M:%S')
                            fields[key] = time_str
                        else:
                            fields[key] = value
                else:
                    # for raw sql
                    for field in obj.keys():
                        fields[field] = str(getattr(obj, field))

                return fields

        return SqlAlchemyEncoder

    def serialize(function):
        def toJSON():
            entitys = function()

            jsonArray = []
            for row in entitys:
                json_str = json.dumps(
                    row, cls=sqlalchemy_encoder(), check_circular=False)
                jsonArray.append(json.loads(json_str))

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
