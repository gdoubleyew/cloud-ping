#!/user/bin/env python3

import unittest
import subprocess
import threading
import cloudping as cp

TEST_ADDR = '1.1.1.1'
TEST_PORT = 5500

class TestParseOptions(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_clientMode(self):
        # test short form options
        cloudping = cp.CloudPing(['program.py', '-c', '-a', TEST_ADDR, '-p', str(TEST_PORT)])
        self.assertEqual(cloudping.mode, 'client')
        self.assertEqual(cloudping.addr, TEST_ADDR)
        self.assertEqual(cloudping.port, TEST_PORT)
        # test long form options
        cloudping = cp.CloudPing(['program.py', '--client', '--addr='+TEST_ADDR, '--port='+str(TEST_PORT)])
        self.assertEqual(cloudping.mode, 'client')
        self.assertEqual(cloudping.addr, TEST_ADDR)
        self.assertEqual(cloudping.port, TEST_PORT)

    def test_serverMode(self):
        cloudping = cp.CloudPing(['program.py', '-s', '-p', '5500'])
        self.assertEqual(cloudping.mode, 'server')
        self.assertEqual(cloudping.port, TEST_PORT)
        # test long form options
        cloudping = cp.CloudPing(['program.py', '--server', '--port=5500'])
        self.assertEqual(cloudping.mode, 'server')
        self.assertEqual(cloudping.port, TEST_PORT)

    def test_invalidArgs(self):
        with self.assertRaises(cp.InvalidInvocation):
            cp.CloudPing(['program.py', '--NoSuchOption'])


class TestClientServer(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_server(self):
        server = cp.CloudPing(['program.py', '-s'])
        def listener():
            server.listen()
        server_thread = threading.Thread(name='server', target=listener)
        server_thread.setDaemon(True)
        server_thread.start()
        result = subprocess.run("echo hello | netcat localhost 5500", shell=True, stdout=subprocess.PIPE)
        self.assertEqual(result.stdout.decode('utf-8'), 'hello')


if __name__ == '__main__':
    unittest.main()
