"""Temporary, deliberately failing test for branch-protection verification.

This file belongs only to the isolated negative-test branch.
Do not merge this file into main.
"""
import unittest


class BranchProtectionNegativeTest(unittest.TestCase):
    def test_required_ci_blocks_a_failed_check(self):
        self.fail(
            "EXPECTED FAILURE: verify that branch rules prevent merging this PR."
        )


if __name__ == "__main__":
    unittest.main()
