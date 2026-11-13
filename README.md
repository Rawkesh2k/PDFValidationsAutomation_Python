<div align="center">

# 📄 PDF Validations Automation

### 🧪 Validate PDF text, dynamic data, logos, and signatures with Python

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/Tests-pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Allure](https://img.shields.io/badge/Reports-Allure-FF6A00?style=for-the-badge)](https://allurereport.org/)
[![PDF](https://img.shields.io/badge/Focus-PDF%20validation-EF476F?style=for-the-badge)](#-what-it-checks)

**A data-driven test suite for checking PDF content and visual assets.**

[✨ What it checks](#-what-it-checks) · [🚀 Quick start](#-quick-start) · [🧭 Run tests](#-run-tests) · [⚙️ Configure](#️-configure-your-test-data) · [📊 Reports](#-allure-reports)

</div>

---

## ✨ What it checks

| Validation | What happens |
|---|---|
| 📝 Static text | Checks expected text from Excel against the extracted text on a PDF page. |
| 🔄 Dynamic text | Checks mapped values on a page against expected data in the workbook. |
| 🖼️ Logos and images | Extracts PDF images and compares them with expected image files. |
| ✍️ Signatures | Compares extracted PDF signature images with the configured reference signatures. |
| 📎 Attachments | Attaches the source PDF to the Allure test report. |

<details>
<summary><strong>🗂️ Example scenarios included</strong></summary>

- **Simple:** BOT letter — text and logo validations.
- **Medium:** Brokerage account opening — text and logo validations.
- **Complex:** Annuity certificate — text and signature validations.

</details>

## 🚀 Quick start

> Run commands from the repository root. The configured PDF, Excel, and image fixtures must be present at the paths in `configurations.ini`.

1. **Clone the repository**

   ```bash
   git clone https://github.com/Rawkesh2k/PDFValidationsAutomation_Python.git
   cd PDFValidationsAutomation_Python
   ```

2. **Create and activate a virtual environment** *(recommended)*

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   macOS / Linux:

   ```bash
   source .venv/bin/activate
   ```

3. **Install the Python packages used by the tests**

   ```bash
   python -m pip install pytest pandas openpyxl pdfminer.six opencv-python numpy Pillow allure-pytest
   ```

4. **Run the suite**

   ```bash
   python -m pytest
   ```

## 🧭 Run tests

Run all PDF validation tests and save Allure result files:

```bash
python -m pytest --alluredir=Reports
```

Run one scenario at a time:

```bash
python -m pytest test_Simple_BOT_Letter_PDF_Validations.py
python -m pytest test_medium_Brokerage_Account_Opening_PDF_Validations.py
python -m pytest test_Complex_Annuity_Certificate_PDF_Validations.py
```

<details>
<summary><strong>🎛️ Handy pytest options</strong></summary>

```bash
# Show each test name and its result
python -m pytest -v

# Stop after the first failure
python -m pytest -x

# Run tests whose names match a keyword
python -m pytest -k Simple
```

</details>

## ⚙️ Configure your test data

The project reads its PDF, workbook, image, and signature locations from [`configurations.ini`](configurations.ini). Update those values to match your local fixture layout before running tests. Paths are currently written in Windows-style format, so check separators and paths if running on another operating system.

The repository is organized around these fixture groups:

- `pdf/` — sample PDFs, grouped into `Simple`, `Medium`, and `Complex` scenarios.
- `TextData/` — Excel workbooks containing expected text and dynamic data mappings.
- `Images/` — expected and extracted image folders for each scenario.
- `TextData/Signatures/` — reference signatures used by the complex scenario.

Workbook rows are read using fields such as `TextType`, `Page`, and `Content`; dynamic rows also use `DynamicDataMapping`. Keep the workbook values and configured fixture paths in sync with the PDF you are testing.

<details>
<summary><strong>📋 Current scenario-to-config mapping</strong></summary>

| Scenario | Configuration sections |
|---|---|
| Simple / BOT letter | `PDFPath_Simple`, `TextValidation_Simple`, `ImageValidation_Simple` |
| Medium / brokerage account opening | `PDFPath_Medium`, `TextValidation_Medium`, `ImageValidation_Medium` |
| Complex / annuity certificate | `PDFPath_Complex`, `TextValidation_Complex`, `ImageValidation_Complex`, `General` |

</details>

## 📊 Allure reports

The tests are instrumented with Allure steps and attachments. After running pytest with `--alluredir`, install the [Allure command-line tool](https://allurereport.org/docs/) and open the results locally:

```bash
allure serve Reports
```

Or generate a static report:

```bash
allure generate --clean --output Reports-html Reports
```

## 🧰 Project layout

```text
.
├── configurations.ini
├── Images/
├── pdf/
├── src/
│   ├── ExtractFigures.py       # PDF image extraction and visual comparison
│   └── ValidateText.py         # PDF text checks and report attachments
├── TextData/
├── test/
├── test_Simple_BOT_Letter_PDF_Validations.py
├── test_medium_Brokerage_Account_Opening_PDF_Validations.py
└── test_Complex_Annuity_Certificate_PDF_Validations.py
```

## 💡 Troubleshooting

<details>
<summary><strong>Tests cannot find a PDF, workbook, or image</strong></summary>

Check that you launched pytest from the repository root and that every path in `configurations.ini` points to an existing fixture. The test scripts build paths from the current working directory.

</details>

<details>
<summary><strong>Image validation fails</strong></summary>

Confirm that the expected image folder contains matching image filenames for the images extracted from the PDF. Image comparisons are exact, so even a visual difference can fail the check.

</details>

<details>
<summary><strong>Allure command is unavailable</strong></summary>

The pytest plugin writes result data, but the `allure` command is a separate CLI tool. Install the Allure CLI using its official [installation guide](https://allurereport.org/docs/install/), or run the tests without generating a report using `python -m pytest`.

</details>

## 🤝 Contributing

Have an improvement in mind? Open an issue or submit a pull request. Please include the scenario or fixture affected and the command you used to verify your change.

---

<div align="center">

Made for more confident PDF checks ✨

</div>
