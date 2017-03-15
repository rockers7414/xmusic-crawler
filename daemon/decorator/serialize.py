import json
import datetime
import inspect
import types

from sqlalchemy.ext.declarative import DeclarativeMeta


class SqlAlchemyEncoder(json.JSONEncoder):

    def type_convert(self, value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(value)

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
                        inner_jsonObj.append(
                            self.default(_row))
                    fields[key] = inner_jsonObj
                else:
                    fields[key] = self.type_convert(value)
        else:
            # for raw sql
            for field in obj.keys():
                fields[field] = self.type_convert(
                    str(getattr(obj, field)))
        return fields


class serialize(object):

    def __init__(self):
        pass

    def __call__(self, cls):
        for name, method in inspect.getmembers(cls):
            if isinstance(method, types.FunctionType):
                setattr(cls, name, self.json_serialize(method))
        return cls

    def json_serialize(self, func):
        def wrapper(*args, **kwargs):
            entitys = func(*args, **kwargs)
            json_array = []
            for row in entitys:
                json_str = json.dumps(
                    row, cls=SqlAlchemyEncoder)
                json_array.append(json.loads(json_str))
            return json_array
        return wrapper
