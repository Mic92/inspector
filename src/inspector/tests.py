import os
import unittest
import tempfile
import inspector
from inspector import cgroups

TEST_ROOT = os.path.realpath(os.path.dirname(__file__))


class CgroupTest(unittest.TestCase):
    def test_create(self):
        with cgroups.PerfEvent("inspector-test") as c:
            pid = str(os.getpid())
            c.addPids(pid)
            f = open(os.path.join(c.mountpoint, "tasks"))
            line = f.readline()
            f.close()
            self.assertEqual(pid + "\n", line)


def perf_cmd():
    return os.getenv("PERF_COMMAND", "perf")


class PerfTest(unittest.TestCase):
    def test_run(self):
        sample_app = os.path.join(TEST_ROOT, "../../test/usage-test")

        with tempfile.NamedTemporaryFile() as log_file:
            process = inspector.run([sample_app],
                                    perf_command=perf_cmd(),
                                    perf_log=log_file.name)
            (rc, perf_rc) = process.wait()
            self.assertEqual(0, rc)
            self.assertEqual(-15, perf_rc)  # SIGTERM == 15
            self.assertGreater(os.path.getsize(log_file.name), 1000)

if __name__ == '__main__':
    unittest.main()
