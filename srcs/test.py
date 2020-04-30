#!/usr/bin/env python3
import unittest
from csv_merger import *

class TestStringMethods(unittest.TestCase):
    def test_name_is_same(self):
        self.assertTrue(name_is_same("a", "a"))
        self.assertTrue(name_is_same("aaaaa", "baaaa"))
        self.assertFalse(name_is_same("a", "b"))
        self.assertFalse(name_is_same("aaaa", "baaa"))

    def test_get_columns(self):
        with open("test.txt", "w") as f:
            f.write("siret;numero\nphone\nkey;siret")
        self.assertEqual(get_columns("test.txt"), {'siret': ('numero',), 'phone': (), 'key': ('siret',)})
        os.remove("test.txt")

    def test_check_key(self):
        columns = {'First Name': (), 'Last Name': (), 'Number': (), "key": ("First Name",)}
        column_name = ["First Name", "Last Name", "Number"]
        df = pd.DataFrame(columns = column_name)
        df.loc[len(df)] = ["Michel", "Faure", "0672312589"]
        new_row = ["Michel", "Pablo", "06421523569"]
        self.assertFalse(check_key(columns, column_name, new_row, df, "source"))
        new_row = ["Paul", "Pablo", "06421523569"]
        self.assertTrue(check_key(columns, column_name, new_row, df, "source"))

    def test_file_to_utf(self):
        if os.path.isfile(".source_test.csv") == False:
            print("cannot test this function, missing test file: .source_test.csv")
            return False
        file_to_utf(["test", "model", ".source_test.csv"])
        self.assertTrue(os.path.isfile("final_.source_test.csv"))
        os.remove("final_.source_test.csv")
    
    def test_cut_path(self):
        self.assertEqual(cut_path("../lala"), "lala")
        self.assertEqual(cut_path("../../lala"), "lala")
        self.assertEqual(cut_path("./lala"), "lala")

if __name__ == "__main__":
    unittest.main()