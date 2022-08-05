import CSVparsing,unittest


class csvParsingFilenameValidateTest(unittest.TestCase):

    def testReturnType(self):
        """Should return bool true|false"""
        self.assertIsInstance(CSVparsing.validateFilename("testingData"),bool)





if __name__=='__main__':
    unittest.main(verbosity=2)


