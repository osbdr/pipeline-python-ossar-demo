from unittest import TestCase

from pet import Pet


class PetTestCase(TestCase):
    def setUp(self):
        self.pet = Pet("Test")

    def test_name(self):
        self.assertEqual(self.pet.name, "Test")
