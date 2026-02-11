
import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from caretaker.plugins.link_recovery import LinkRecoveryAgent

class TestLinkRecoveryAgent(unittest.TestCase):
    def setUp(self):
        self.agent = LinkRecoveryAgent()

    def test_extract_issue_references(self):
        text = "Fixes #42 and resolves GH-10"
        issues = self.agent.extract_issue_references(text)
        self.assertEqual(issues, [10, 42])

    def test_normalize_text(self):
        text = "  Hello,   World!  "
        norm = self.agent.normalize_text(text)
        self.assertEqual(norm, "hello world")

    def test_semantic_similarity_exact(self):
        score = self.agent.calculate_semantic_similarity("Fix login bug", "Fix login bug")
        self.assertGreaterEqual(score, 1.0)

    def test_semantic_similarity_partial(self):
        score = self.agent.calculate_semantic_similarity("Fix login bug", "Corrected login error")
        self.assertGreater(score, 0.0)
        self.assertLess(score, 1.0)

if __name__ == '__main__':
    unittest.main()
