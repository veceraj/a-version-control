"""Test Scenario 1 Module"""

import os
import unittest
import subprocess
import shutil
import shlex
import config


class TestScenario1(unittest.TestCase):
    """TestScenario1"""

    def setUp(self):
        self.dry_run = False

        if not shutil.which("python3"):
            self.skipTest("Required command python3 not found")

        self.original_dir = os.getcwd()
        self.test_dir = self.original_dir + "/tests"

        self.entry = f"python3 {self.original_dir}/main.py"

        # move to dir
        self.target_dir = "./tests/playground"
        os.makedirs(self.target_dir, exist_ok=True)
        os.chdir(self.target_dir)

        subprocess.run(shlex.split(f"{self.entry} init -v v1"), check=False)

    def tearDown(self):
        os.chdir(self.original_dir)

        # remove the playground directory after the tests
        shutil.rmtree(self.target_dir)

    def runTest(self):
        """Run test"""

        for version_name, paths in self.get_version_files():
            subprocess.run(
                shlex.split(f"{self.entry} checkout -v {version_name}"), check=False
            )

            subprocess.run(shlex.split(f"{self.entry} version"), check=False)

            for file_path in paths:
                with open(
                    self.test_dir + file_path, "r", encoding=config.ENCODING
                ) as file:
                    content = file.read()

                full_file_path = os.path.join(
                    self.target_dir.rstrip("/"), file_path.lstrip("/")
                )

                directory_path = os.path.dirname(full_file_path)
                os.makedirs(directory_path, exist_ok=True)

                with open(full_file_path, "w", encoding=config.ENCODING) as file:
                    file.write(content)

                subprocess.run(
                    shlex.split(f"{self.entry} add -p {full_file_path}"), check=False
                )

            if self.dry_run:
                subprocess.run(
                    shlex.split(f"{self.entry} commit -m 'message' -all --dry-run"),
                    check=False,
                )

            subprocess.run(
                shlex.split(f"{self.entry} commit -m 'message' -all"), check=False
            )

            # with open("main.c", "r") as file:
            #     self.assertEqual(file.read(), content_v1)

    def get_version_files(self) -> list[list[str]]:
        """Get all file paths"""

        version_files = [
            (
                "v1",
                [
                    "/versions/bubble_sort_1.c",
                    "/versions/sorts_1.c",
                ],
            ),
            (
                "v2",
                [
                    "/versions/sorts_2.c",
                ],
            ),
            (
                "v3",
                [
                    "/versions/bubble_sort_2.c",
                    "/versions/sorts_3.c",
                ],
            ),
        ]

        return version_files


if __name__ == "__main__":
    unittest.main()
