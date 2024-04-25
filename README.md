* * *

Bank Statement Analyzer
=======================

Overview
--------

The Bank Statement Analyzer is a work-in-progress program designed to help users categorize their expenses based on descriptions in their TRUIST bank statements. The program features a graphical user interface (GUI) that allows users to select a TRUIST bank statement file, extract its contents, and store them in a database. Using artificial intelligence (AI), the program attempts to predict the category to which each expense description belongs.

Features
--------

*   **File Selection:** Users can select a TRUIST bank statement file using the GUI.
*   **Data Extraction:** The program extracts the contents of the bank statement file for processing.
*   **Database Entry:** Extracted data is stored in a database for future reference.
*   **AI Prediction:** Utilizing AI algorithms, the program predicts the category of each expense description.

Usage
-----

1.  **Select File:** Click the "Select File" button to choose a TRUIST bank statement file.
2.  **Read Contents:** After selecting the file, click the "Read Contents" button to extract and display its contents.
3.  **Database Entry:** Click the "Enter Into Database" button to store the extracted data in a database.
4.  **AI Prediction:** Finally, click the "Predict Categories" button to categorize expense descriptions using AI.

Getting Started
---------------

To get started with the Bank Statement Analyzer, follow these steps:

1.  Clone the repository to your local machine.
2.  Install the required packages listed below.
3.  Run the `toFile.py` file to initialize the database.
4.  Manually categorize entries in the `items.json` file for better AI accuracy.
5.  Run the main program to begin analyzing TRUIST bank statements.

Note
----

*   This program is currently in development, and almost all commits will be done in the development branch. For contributions, it is recommended to download from the development branch.
*   The program currently only supports TRUIST bank statements due to a lack of access to other bank statements for development purposes.
*   **Important:** The more entries you categorize in the `items.json` file, the better and more accurate the AI model will be.

Packages Required
-----------------

*   `tkinter`
*   `pypdf`
*   `os`
*   `re`
*   `json`
*   `nltk`
*   `sklearn`

*** 