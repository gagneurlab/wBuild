"""wBuild's utils.py tests"""
import unittest
import wbuild.utils
from yaml import MarkedYAMLError, YAMLError

class UtilsTestCase(unittest.TestCase):

    def test_paramParser_passesSeenRightYaml(self):
        rightYaml="---\n  wb:\n---"
        param, err = wbuild.utils.parseParamFromYAML(rightYaml, False)
        self.assertDictEqual({'wb':None}, param) #, "Got wrong parsement of YAML:" + param

    '''
    def test_paramParser_throwsMarkedYAMLonWrongYAML(self):
        wrongYAML = "---\n      YaMl    \nlol"
        with self.assertRaises(YAMLError):
            wbuild.utils.parseParamFromYAML(wrongYAML, False)
    '''

if __name__ == '__main__':
    unittest.main()
