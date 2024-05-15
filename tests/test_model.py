import copy
import unittest

from evreka.model import Device


class TestDeviceModel(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_init_without_name(self) -> None:
        device = Device(name= 'test', ip_address='localhost', port=2323)


if __name__ == '__main__':
    unittest.main()
