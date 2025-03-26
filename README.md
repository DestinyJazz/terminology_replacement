# Terminology Replacement Tool

A **Flask-based web application** that replaces terminology in uploaded Excel files and text input based on predefined product-specific terminology mappings.

## Features
- Upload an Excel file and replace terms based on product-specific terminology mappings.
- Support for multiple products with dedicated terminology files.
- API endpoint for replacing terminology in text dynamically.
- Supports **both** forward and reverse terminology replacement.
- Web interface for easy interaction.

1. It can be used as any **Wording** replacement scenario to streamline or align the known and correct wording after translation or AI generation.
2. Rename or add new Excel files and edit the HTML file to tailor the web interface to your specific use case.


## Installation
### 1. Clone the Repository
```sh
git clone https://github.com/DestinyJazz/terminology_replacement.git
cd terminology_replacement
```

## Folder Structure
terminology_replacement/
│── terminology_files/        # Product terminology files
│── uploads/                 # Uploaded files
│── outputs/                 # Processed files
│── templates/               # Web templates
│── app.py                   # Flask app
│── README.md                # Documentation
