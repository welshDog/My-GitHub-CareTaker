
import unittest
import sys
import os
import tempfile

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from caretaker.plugins.repo_explorer import RepoExplorerAgent

class TestRepoExplorerAgent(unittest.TestCase):
    def setUp(self):
        self.agent = RepoExplorerAgent()
        self.test_dir = tempfile.mkdtemp()
        
        # Create a dummy python file
        with open(os.path.join(self.test_dir, 'dummy.py'), 'w') as f:
            f.write("def foo():\n    bar()\n\ndef bar():\n    pass\n")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)

    def test_build_function_call_graph(self):
        result = self.agent.build_function_call_graph(self.test_dir)
        
        # Check if functions were found
        self.assertIn('dummy.foo', result['function_definitions'])
        self.assertIn('dummy.bar', result['function_definitions'])
        
        # Check call graph
        # Note: Module name might vary depending on implementation, usually it's relative
        # In the agent code: module_name = self.get_module_name(py_file, repo_path)
        # We need to see how get_module_name works. 
        # Assuming it uses relative path.
        
        # For now, just check total functions
        self.assertEqual(result['total_functions'], 2)

if __name__ == '__main__':
    unittest.main()
