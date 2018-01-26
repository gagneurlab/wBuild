"""wBuild's utils.py tests"""
import unittest
from unittest.mock import patch, mock_open

from wbuild.utils import *

class UtilsTestCase(unittest.TestCase):

    def test_checksFilename(self):
        spacedName = "ProgramFiles \\Job Materials"
        with self.assertRaises(ValueError):
            checkFilename(spacedName)
        minusInName = "ProgramFiles\\JobMaterials\\yesterday-sheets"
        with self.assertRaises(ValueError):
            checkFilename(minusInName)
        allowedName = "ProgramFiles\\JobMaterials\\yesterdaySheets"
        self.assertTrue(checkFilename(allowedName))

    def test_paramParser_passesSeenRightYaml(self):
        rightYaml="---\n  wb:\n---"
        param= parseYamlParams(rightYaml, "dummyFile.R")
        self.assertDictEqual({'wb':None}, param) #, "Got wrong parsement of YAML:" + param

    def test_paramParser_returnsNoneOnWrongYAML(self):
        wrongYAML = "---\n-dfs:\ndsa:dsasdf\n---"
        print("Testing wrong YAML parsing. The output is:\n")
        self.assertEqual(parseYamlParams(wrongYAML, "dummyFile.R"), None)

    def test_inDocYamlIsParsed(self):
        with patch('builtins.open', mock_open(read_data="#'---\n#' wb:\n#' -iris: \"Data\"\n#'---\n")) as mo:
            yamlRead = parseYAMLHeader(".")
            mo.assert_called_with('.')
            self.assertEqual("---\n wb:\n -iris: \"Data\"\n---", yamlRead)


if __name__ == '__main__':
    unittest.main()
