import CSVparsing,unittest


class csvParsingFilenameValidateTest(unittest.TestCase):

    def testReturnType(self):
        """Should return bool true|false"""
        self.assertIsInstance(CSVparsing.validateFilename("testingData"),bool)

class csvParsingValidateDateTimeTest(unittest.TestCase):

    def testReturnType(self):
        """Should return a true/false bool"""
        self.assertIsInstance(CSVparsing.validateDateTime("05082022"), bool)



if __name__=='__main__':
    unittest.main(verbosity=2)


