# Write your tests here
import unittest
from fastapi.testclient import TestClient
from main import app
from utils import compare_data

client = TestClient(app)


class TestAPI(unittest.TestCase):
    def test_read_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'Hello': 'Data discrepancies checker'})

    def test_compare_pdf_valid(self):
        file_path = "assets/financellc.pdf"
        company_name = "FinanceLLC"

        with open(file_path, "rb") as file:
            response = client.post("/compare", data={"company_name": company_name}, files={"file": file})

        self.assertEqual(response.status_code, 200)

        result = response.json()

        self.assertIn("existing_data", result)
        self.assertIn("extracted_data", result)
        self.assertIn("discrepancies", result)
        self.assertIsInstance(result["existing_data"], dict)
        self.assertIsInstance(result["extracted_data"], dict)
        self.assertIsInstance(result["discrepancies"], dict)

    def test_compare_pdf_invalid_file_type(self):
        company_name = "FinanceLLC"
        response = client.post(
            "/compare",
            files={"file": ("test.txt", b"dummy content", "text/plain")},
            data={"company_name": company_name}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid file type. Please upload a PDF file."})

    def test_compare_pdf_file_not_found(self):
        company_name = "FinanceLLC"
        response = client.post(
            "/compare",
            files={"file": ("nonexistent.pdf", b"", "application/pdf")},
            data={"company_name": company_name}
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Cannot extract data. Invalid file provided.")

    def test_compare_pdf_company_not_found(self):
        file_path = "assets/financellc.pdf"
        company_name = "NonExistentCompany"

        with open(file_path, "rb") as file:
            response = client.post(
                "/compare",
                files={"file": ("financellc.pdf", file, "application/pdf")},
                data={"company_name": company_name}
            )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Company not found in database."})

    def test_compare_pdf_missing_fields(self):
        file_path = "assets/financellc.pdf"

        with open(file_path, "rb") as file:
            response = client.post("/compare", files={"file": file})

        self.assertEqual(response.status_code, 422)

    def test_compare_pdf_partial_data(self):
        existing_data = {"key1": "value1", "key2": "value2", "key4": "value4"}
        extracted_data = {"key1": "value1", "key3": "value3", "key4": "value5"}

        discrepancies = {
            "key2": {"existing": "value2", "extracted": None},
            "key3": {"existing": None, "extracted": "value3"},
            "key4": {"existing": "value4", "extracted": "value5"}
        }

        self.assertEqual(compare_data(existing_data, extracted_data), discrepancies)


if __name__ == '__main__':
    unittest.main()
