
import unittest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from caretaker.plugins.monitor import MonitorAgent

class TestMonitorAgent(unittest.TestCase):
    def setUp(self):
        self.agent = MonitorAgent()

    def test_validate_message_semantics_missing_fields(self):
        # MonitorAgent.get_required_fields needs to be mocked or we need to know what it expects.
        # Looking at the code, MonitorAgent doesn't implement get_required_fields in the snippet I saw,
        # it calls self.get_required_fields(receiver).
        # I need to mock get_required_fields for this test to work independently.
        
        # Monkey patch for testing
        self.agent.get_required_fields = lambda r: ['action', 'target']
        
        msg = {'target': 'foo'} # Missing 'action'
        validation = self.agent.validate_message_semantics('sender', 'receiver', msg)
        self.assertFalse(validation['valid'])
        self.assertIn('Missing required fields', validation['reason'])

    def test_validate_message_semantics_valid(self):
        self.agent.get_required_fields = lambda r: ['action']
        self.agent.get_valid_actions = lambda r: ['update']
        
        msg = {'action': 'update'}
        validation = self.agent.validate_message_semantics('sender', 'receiver', msg)
        self.assertTrue(validation['valid'])

    def test_track_communication(self):
        self.agent.get_required_fields = lambda r: ['action']
        self.agent.get_valid_actions = lambda r: ['ping']
        
        msg = {'action': 'ping'}
        result = self.agent.track_agent_communication('A', 'B', msg)
        
        self.assertEqual(len(self.agent.communication_history), 1)
        self.assertEqual(self.agent.communication_history[0]['status'], 'success')

if __name__ == '__main__':
    unittest.main()
