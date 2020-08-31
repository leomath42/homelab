import random
import time as lib_time
import xml.etree.ElementTree as ET
import os
import jinja2
from HomeLab import config

_chr_inicio = 33
_chr_fim = 126


def generate_random_sequence(num):
    aux = ""
    for i in range(num):
        aux += chr(random.randint(_chr_inicio, _chr_fim))

    return aux


def format_time(time, string_format=None):
    # formatando a data
    string_format = string_format if string_format else "{0} de {1} de {2}"
    mouth = {
        1: 'jan',
        2: 'fev',
        3: 'mar',
        4: 'abr',
        5: 'mai',
        6: 'jun',
        7: 'jul',
        8: 'ago',
        9: 'set',
        10: 'out',
        11: 'nov',
        12: 'dez',
    }
    struct_time = lib_time.localtime(time)
    return string_format.format(struct_time[2], mouth[struct_time[1]], struct_time[0])


def format_file(file):
    # call format file
    file.date = format_time(file.time)
    # outras formatações do arquivo que serão utilizadas.


def parse_xml_to_object_list(file, cls, func=None):
    """

    @param file: um arquivo xml de configuração
                 ex.: config.xml
    @param cls: uma classe
                 ex.: HomeLab.controller.Device
    @param func: função recebe um obj da classe 'cls',
                 executa comandos opcionais do obj antes do @return
                 ex.: lambda obj: return obj.start()
    @return: lista de obj da classe 'cls'
    """
    # assert type(cls) == type
    assert type(file) == str

    tree = ET.parse(file)
    root = tree.getroot()
    _list = list()

    for xml_cls in root.findall(cls.__name__):
        dic = dict()
        for element in xml_cls:
            dic[element.tag] = element.attrib.get('value')

        obj = cls.__new__(cls)
        obj.__init__(**dic)
        if func:
            func(obj)

        _list.append(obj)

    return _list


def generate_device_template_from_xml(file, _id):
    tree = ET.parse(file)
    root = tree.getroot()
    _list = list()
    template = "<{0} id='{1}' class= '{2}' ></{0}>"
    for xml in root.findall("DeviceTemplate"):
        if _id == int(xml.attrib['_id']):
            template = template.format(xml.attrib['type'], xml.attrib['id'], xml.attrib['class'])

    return jinja2.Markup(template)


def save_device_template_to_xml(file):
    pass


class Device(object):
    '''

    '''
    pass


class Printer(object):

    def __init__(self, *args, **kwargs):
        def __getargs(name, index, *args, **kwargs):
            return kwargs.get(name) if kwargs.get(name) else args[index] if len(args) > index else None

        self.id = __getargs('id', 0, *args, **kwargs)
        self.host = __getargs('host', 1, *args, **kwargs)
        self.printerName = __getargs('printerName', 2, *args, **kwargs)
        self.commandFormat = __getargs('commandFormat', 3, *args, **kwargs)
        self.message = __getargs('message', 4, *args, **kwargs)

    def do_print(self, file_name, **kwargs):
        command = self.commandFormat.format(self.host, self.printerName, file_name)
        print(command)
        os.popen(command)

    def cancel_print(self):
        pass

    def format_print(self, *args, **kwargs):
        pass


# class Template:
#     """
#         classe que gera um template baseado nos templates pré definidos no projeto.
#         Utilizado com objetos do tipo model.Device ou model.Printer
#     """
#     _button = "<button id='{1}-{0}' class='{1}-{2} btn btn-primary'> " \
#               '<svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="microchip" ' \
#               'class="svg-inline--fa fa-microchip fa-w-16" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '\
#               '512 512"><path fill="currentColor" d="M416 48v416c0 26.51-21.49 48-48 48H144c-26.51 ' \
#               '0-48-21.49-48-48V48c0-26.51 21.49-48 48-48h224c26.51 0 48 21.49 48 48zm96 58v12a6 6 0 0 1-6 6h-18v6a6 ' \
#               '6 0 0 1-6 6h-42V88h42a6 6 0 0 1 6 6v6h18a6 6 0 0 1 6 6zm0 96v12a6 6 0 0 1-6 6h-18v6a6 6 0 0 1-6 ' \
#               '6h-42v-48h42a6 6 0 0 1 6 6v6h18a6 6 0 0 1 6 6zm0 96v12a6 6 0 0 1-6 6h-18v6a6 6 0 0 1-6 6h-42v-48h42a6 ' \
#               '6 0 0 1 6 6v6h18a6 6 0 0 1 6 6zm0 96v12a6 6 0 0 1-6 6h-18v6a6 6 0 0 1-6 6h-42v-48h42a6 6 0 0 1 6 ' \
#               '6v6h18a6 6 0 0 1 6 6zM30 376h42v48H30a6 6 0 0 1-6-6v-6H6a6 6 0 0 1-6-6v-12a6 6 0 0 1 6-6h18v-6a6 6 0 0 '\
#               '1 6-6zm0-96h42v48H30a6 6 0 0 1-6-6v-6H6a6 6 0 0 1-6-6v-12a6 6 0 0 1 6-6h18v-6a6 6 0 0 1 ' \
#               '6-6zm0-96h42v48H30a6 6 0 0 1-6-6v-6H6a6 6 0 0 1-6-6v-12a6 6 0 0 1 6-6h18v-6a6 6 0 0 1 ' \
#               '6-6zm0-96h42v48H30a6 6 0 0 1-6-6v-6H6a6 6 0 0 1-6-6v-12a6 6 0 0 1 6-6h18v-6a6 6 0 0 1 ' \
#               '6-6z"></path></svg>' \
#               "</button>"
#     _slide = ""
#     _graphic = ""
#     _file = "/template.xml"
#
#     @classmethod
#     def __template_from_xml(cls, string):
#         tree = ET.parse(config.get('homelab_path') + cls._file)
#         root = tree.getroot()
#         return root.find(string).get('value')
#
#     @classmethod
#     def __parse(cls, string):
#         """
#         um parse simples para remover substrings(class, <, >, .)
#         e retornar como lower();
#         @return: str
#         """
#         return string.replace("<", "").replace(">", "").replace("class", "").replace(".", "-").lower()
#
#     def __new__(cls, model, *args, **kwargs):
#         template_name = model.__dict__.get('template')
#         _type = Template.__dict__.get("_" + template_name)
#         # _type = cls.__template_from_xml(template_name)
#         template = _type.format(model.id, cls.__parse(model.__class__.__name__), model.template)
#
#         return jinja2.Markup(template)


if __name__ == "__main__":
    print(type(eval(dir()[0])))
    print(parse_xml_to_object_list('config.xml', Printer))
    p = parse_xml_to_object_list('config.xml', Printer)[0]
    p.do_print('config.xml')
