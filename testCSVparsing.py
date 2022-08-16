import CSVparsing,unittest


class csvParsingFilenameValidateTest(unittest.TestCase):

    def testReturnType(self):
        """Should return bool true|false"""
        self.assertIsInstance(CSVparsing.validateFilename("testingData"),bool)

class csvParsingValidateDateTimeTest(unittest.TestCase):

    def testReturnType(self):
        """Should return a true/false bool"""
        self.assertIsInstance(CSVparsing.validateDateTime("05082022"), bool)

    def testValidFilename(self):
        self.assertTrue(CSVparsing.validateFilename('MED_DATA_20220605142519.csv'))

    def testInvalidFilename(self):
        self.assertFalse(CSVparsing.validateFilename('MED_DAT_20220605142519.csv'))


class csvParsingDateTimeValidateTest(unittest.TestCase):

    def testReturnType(self):
        """Should return bool true|false"""
        self.assertIsInstance(CSVparsing.validateDateTime("testingData"),bool)

    def testValidDateTime(self):
        self.assertTrue(CSVparsing.validateDateTime("20220804152922"))

    def testInvalidDateTime(self):
        self.assertFalse(CSVparsing.validateDateTime("11111"))

if __name__=='__main__':
    unittest.main(verbosity=2)


