from html.parser import HTMLParser

class LyricHTMLParser(HTMLParser):

    # container
    __target_container = None

    # container indentity
    __target_attr = None
    __target_attr_value = None

    # flag for is target
    __is_target = False

    # result
    __result = ""

    def __init__(self, target_container, target_attr, target_attr_value):
        HTMLParser.__init__(self)
        self.__target_container = target_container
        self.__target_attr = target_attr
        self.__target_attr_value = target_attr_value

    def handle_starttag(self, tag, attrs):
        if tag == self.__target_container:
            for key, value in attrs:
                if key == self.__target_attr and value == self.__target_attr_value:
                    self.__is_target = True

    def handle_data(self, data):
        if self.__is_target:
            self.__result += "{0}".format(data)

    def handle_endtag(self, tag):
        if tag == self.__target_container:
            self.__is_target = False

    def get_result(self):
        if self.__result != "":
            return self.__result
        else:
            return None
