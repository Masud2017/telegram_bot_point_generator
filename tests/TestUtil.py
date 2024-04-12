import unittest
from src.Util import extract_message

class TestSessionHandler(unittest.TestCase):
    def test_extract_message(self):
        expected_with_space_sperated_name = (1,"sample name")
        expected_with_single_name = (1,"name")

        actual_with_space_separated_name = extract_message("/command 1 sample name","unlistitem")
        actual_with_single_name = extract_message("/command 1 name","unlistitem")

        self.assertEqual(expected_with_space_sperated_name,actual_with_space_separated_name)
        self.assertEqual(expected_with_single_name,actual_with_single_name)


        expected_with_space_sperated_name_withdrawitem = (1,"sample name",3)
        expected_with_single_name_withdrawitem = (1,"name",3)
        actual_with_space_separated_name_withdrawitem = extract_message("/command 1 sample name 3","withdrawitem")
        actual_with_single_name_withdrawitem = extract_message("/command 1 name 3","withdrawitem")

        self.assertEqual(expected_with_space_sperated_name_withdrawitem,actual_with_space_separated_name_withdrawitem)
        self.assertEqual(expected_with_single_name_withdrawitem,actual_with_single_name_withdrawitem)


        expected_with_space_sperated_name_editprob = (1,"sample name",3)
        expected_with_single_name_editprob = (1,"name",3)
        actual_with_space_separated_name_editprob = extract_message("/command 1 sample name 3","editprobability")
        actual_with_single_name_editprob = extract_message("/command 1 name 3","editprobability")

        self.assertEqual(expected_with_space_sperated_name_editprob,actual_with_space_separated_name_editprob)
        self.assertEqual(expected_with_single_name_editprob,actual_with_single_name_editprob)