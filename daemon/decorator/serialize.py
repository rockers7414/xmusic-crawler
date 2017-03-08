import json

from enumtype.serializetype import SerializeType


def serializeController(type):

    def serialize(function):
        def toJSON():
            entitys = function()
            jsonArray = []

            for row in entitys:

                # if hasattr(row, '_asdict'):
                #     row_dict = row._asdict()
                # else:
                    # row_dict = row.__dict__
                row_dict = row.__dict__
                row_dict.pop('_sa_instance_state', None)
                jsonArray.append(row_dict)

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
