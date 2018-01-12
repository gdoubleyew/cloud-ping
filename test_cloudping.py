#!/user/bin/env python3

import unittest
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
        print("ParseOptions: test_clientMode")
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
        print("ParseOptions: test_serverMode")
        cloudping = cp.CloudPing(['program.py', '-s', '-p', '5500'])
        self.assertEqual(cloudping.mode, 'server')
        self.assertEqual(cloudping.port, TEST_PORT)
        # test long form options
        cloudping = cp.CloudPing(['program.py', '--server', '--port=5500'])
        self.assertEqual(cloudping.mode, 'server')
        self.assertEqual(cloudping.port, TEST_PORT)
    def test_invalidArgs(self):
        print("ParseOptions: test_invalidArgs")
        with self.assertRaises(cp.InvalidInvocation):
            cp.CloudPing(['program.py', '--NoSuchOption'])


class TestClientServer(unittest.TestCase):
    def setUp(self):
        server = cp.CloudPing(['program.py', '-s'])
        def listener():
            server.listen()
        server_thread = threading.Thread(name='server', target=listener)
        server_thread.setDaemon(True)
        server_thread.start()
    def tearDown(self):
        pass
    def test_server(self):
        # send hello to server using netcat
        # result = subprocess.run("echo hello | netcat localhost 5500", shell=True, stdout=subprocess.PIPE)
        # self.assertEqual(result.stdout.decode('utf-8'), 'hello')
        pass
    def test_client(self):
        print("TestClientServer")
        client = cp.CloudPing(['program.py', '-c', '-a', 'localhost'])
        for _ in range(5):
            elapsed_time = client.ping()
            self.assertTrue(elapsed_time > 0)

if __name__ == '__main__':
    unittest.main()
