import unittest
import cloudping as cp

class TestParseOptions(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_clientMode(self):
        cloudping = cp.CloudPing(['program.py', '-c', '-a', '1.1.1.1', '-p', '5500'])
        cloudping.parseArgs()
        self.assertEqual(cloudping.mode, 'client')
        self.assertEqual(cloudping.addr, '1.1.1.1')
        self.assertEqual(cloudping.port, '5500')

        cloudping = cp.CloudPing(['program.py', '--client', '--addr=1.1.1.1', '--port=5500'])
        cloudping.parseArgs()
        self.assertEqual(cloudping.mode, 'client')
        self.assertEqual(cloudping.addr, '1.1.1.1')
        self.assertEqual(cloudping.port, '5500')

    def test_serverMode(self):
        cloudping = cp.CloudPing(['program.py', '-s', '-p', '5500'])
        cloudping.parseArgs()
        self.assertEqual(cloudping.mode, 'server')
        self.assertEqual(cloudping.port, '5500')

        cloudping = cp.CloudPing(['program.py', '--server', '--port=5500'])
        cloudping.parseArgs()
        self.assertEqual(cloudping.mode, 'server')
        self.assertEqual(cloudping.port, '5500')

    def test_invalidArgs(self):
        cloudping = cp.CloudPing(['program.py', '--NoSuchOption'])
        self.assertRaises(cp.InvalidInvocation, cloudping.parseArgs)

if __name__ == '__main__':
    unittest.main()
