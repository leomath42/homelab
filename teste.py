# import unittest
#
#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)
#
#
# if __name__ == '__main__':
#     unittest.main()
if __name__ == '__main__':
    from HomeLab import *
    # d = {'id': 1, 'descriptor': 'FFFF', 'connect_type': 'serial'}
    # aux = controller.Device(**d)
    # aux.model_class = model.Dispositivo(id=1)
    # print(aux.__dict__)
    # lista = util.parse_xml_to_object_list('config.xml', controller.Device)
    aux = controller.devices
    print(aux)