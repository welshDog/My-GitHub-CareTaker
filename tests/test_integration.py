
import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from caretaker.plugins import get_plugin
from caretaker.core.context import CareContext

class TestPluginSystem(unittest.TestCase):
    def test_get_plugin_monitor(self):
        plugin = get_plugin('monitor')
        self.assertIsNotNone(plugin)
        self.assertEqual(plugin.name, 'monitor')

    def test_get_plugin_invalid(self):
        plugin = get_plugin('non_existent_plugin')
        self.assertIsNone(plugin)

class TestAppIntegration(unittest.TestCase):
    def setUp(self):
        # We need to be careful not to start the server, just import app
        from caretaker.app import app
        self.app = app.test_client()
        self.app.testing = True

    @patch('caretaker.app.ctx')
    def test_index_route(self, mock_ctx):
        # Mock the client response (though index doesn't use it directly in template currently)
        mock_ctx.client.list_user_repos.return_value = [{'name': 'repo1'}]
        mock_ctx.owner = 'test_user'
        
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Run Duplicate Scan', response.data)

    @patch('caretaker.app.ctx')
    def test_repos_route(self, mock_ctx):
        mock_ctx.client.list_user_repos.return_value = [{'name': 'repo1', 'html_url': 'http://github.com/u/repo1'}]
        mock_ctx.owner = 'test_user'
        
        response = self.app.get('/repos')
        self.assertEqual(response.status_code, 200)
        # Assuming repos.html lists the repos
        # We can just check status code for now if we don't know the exact template
        # But let's try to verify content if possible.
        # If repos.html iterates, it likely shows the name.
        self.assertIn(b'repo1', response.data)

if __name__ == '__main__':
    unittest.main()
