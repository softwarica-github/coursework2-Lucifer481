import unittest
from unittest.mock import patch
from antivirus import scan_file, interpret_scan_results

class TestAntivirus(unittest.TestCase):

    @patch('antivirus.requests.post')
    def test_scan_file_success(self, mock_post):
        # Mocking the API response for a successful file scan
        mock_response = unittest.mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'response_code': 1,
            'scan_id': '123abc',
            'positives': 5,
            'total': 70,
            'scans': {'TestEngine': {'detected': True}}
        }
        mock_post.return_value = mock_response

        response = scan_file(r'C:\Users\devil\OneDrive\Desktop\checker\exe\done.exe')
        self.assertIn('scan_id', response)
        self.assertEqual(response['scan_id'], '123abc')

    def test_interpret_scan_results_high_threat_level(self):
        mock_results = {
            'positives': 50,
            'total': 70,
            'scans': {'TestEngine': {'detected': True}}
        }
        results = interpret_scan_results(mock_results)
        self.assertEqual(results['threat_level'], 'High')

    def test_interpret_scan_results_moderate_threat_level(self):
        mock_results = {
            'positives': 7,
            'total': 70,
            'scans': {'TestEngine': {'detected': True}}
        }
        results = interpret_scan_results(mock_results)
        self.assertEqual(results['threat_level'], 'Moderate')

    def test_interpret_scan_results_no_threat_found(self):
        mock_results = {
            'positives': 0,
            'total': 70,
            'scans': {'TestEngine': {'detected': False}}
        }
        results = interpret_scan_results(mock_results)
        self.assertEqual(results['threat_level'], 'None')

if __name__ == '__main__':
    unittest.main()
