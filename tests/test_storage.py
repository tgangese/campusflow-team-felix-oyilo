import unittest
import os
import json
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.path = "data/test_tickets.json"
        # Ensure clean
        if os.path.exists(self.path):
            os.remove(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_missing_file_returns_empty(self):
        # Fresh start — file doesn't exist -> []
        result = load_tickets("data/does_not_exist.json")
        self.assertEqual(result, [])

    def test_save_and_reload(self):
        tickets = []
        create_ticket(tickets, "WiFi down", "Network", "high", 5)
        save_tickets(tickets, self.path)
        loaded = load_tickets(self.path)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["id"], "T001")

    def test_malformed_json_raises(self):
        # Create corrupted file
        os.makedirs("data", exist_ok=True)
        with open(self.path, "w") as f:
            f.write("{ bad json")
        with self.assertRaises(ValueError) as ctx:
            load_tickets(self.path)
        self.assertIn("Malformed JSON", str(ctx.exception))

    def test_id_unique_after_reload(self):
        tickets = []
        create_ticket(tickets, "A", "Network", "low", 1) # T001
        create_ticket(tickets, "B", "Network", "low", 1) # T002
        save_tickets(tickets, self.path)

        loaded = load_tickets(self.path)
        # Next ticket after reload should be T003, not T001 again
        t3 = create_ticket(loaded, "C", "Network", "low", 1)
        self.assertEqual(t3["id"], "T003")

    def test_save_creates_data_dir(self):
        path = "data/new_folder/tickets.json"
        if os.path.exists(path):
            os.remove(path)
        tickets = []
        create_ticket(tickets, "Test", "Other", "low", 1)
        save_tickets(tickets, path)
        self.assertTrue(os.path.exists(path))
        # cleanup
        os.remove(path)
        os.rmdir("data/new_folder")

if __name__ == "__main__":
    unittest.main()