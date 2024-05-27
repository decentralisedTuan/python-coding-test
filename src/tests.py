# Write your tests here
import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAPI(unittest.TestCase):
    def test_read_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    def test_compare_pdf_valid(self):
        file_path = "assets/financellc.pdf"
        company_name = "FinanceLLC"

        with open(file_path, "rb") as file:
            response = client.post("/compare", data={"company_name": company_name},  files={"file": file})
        self.assertEqual(response.status_code, 200)

        result = response.json()

        self.assertIn("existing_data", result)
        self.assertIn("extracted_data", result)
        self.assertIn("discrepancies", result)

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


if __name__ == '__main__':
    unittest.main()
