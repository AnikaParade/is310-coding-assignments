# Fairy-Tale Retellings Data Curator

## What this project does

This project collects interpretive data about fairy-tale retellings and adaptations. Each record includes a title, original tale, creator, year, medium, protagonist agency, gender representation, setting changes, moral message, and interpretation notes. The topic is useful for studying how cultural meanings change when stories are retold.

## Files

- `cli_data_entry.py` — terminal-based Python data-entry program.
- `index.html`, `styles.css`, and `script.js` — browser-based data-entry interface.
- `requirements.txt` — Python package requirement.
- `fairy_tale_data.json` — example structured data file. The CLI also creates/updates this file when entries are confirmed.

## Run the Python CLI on Windows

Open PowerShell and change directory to this folder. For example:

```powershell
cd "$HOME\path\to\is310-coding-assignments\python-libraries"
```

Replace the example path with the actual location of your repository.

Install the dependency:

```powershell
py -m pip install -r requirements.txt
```

Run the program:

```powershell
py cli_data_entry.py
```

The CLI displays example records, asks for each field, displays the completed entry for confirmation, and only saves it after the user confirms. If the user rejects an entry, the program asks them to enter it again. The JSON file is saved next to the Python script. The final message prints the full resolved path.

## Run the HTML interface

Double-click `index.html` to open it in a browser, or use PowerShell from this folder:

```powershell
Start-Process .\index.html
```

Complete the fields and choose **Review record**. Confirm the entry to add it to the on-page collection. Add at least two records to test multiple entries. Choose **Download records as JSON** to save the records as a structured file.

The HTML page keeps records in browser memory while the page is open; download the JSON file before closing or refreshing the page.

## Comparing the interfaces

The CLI is useful for repeatable data entry and saves confirmed records directly to a JSON file beside the script. It is less visual, and users must type into terminal prompts. The HTML interface makes the fields visible together, supports review before adding a record, and displays the collected records in a table. However, the browser version requires the user to download the JSON file, and its in-memory collection is lost if the page is refreshed before downloading.

Both interfaces use the same core fields, but their interfaces encourage different workflows. The CLI asks questions one at a time, which can help a curator focus on each field. The HTML page shows the whole form at once, making it easier to compare fields and revise an entry before confirming. Both require the fields to be completed; the browser uses built-in required-field validation, while the CLI checks each answer for blank input.

AI assistance helped draft and troubleshoot the initial code structure, validation, JSON saving, and comparison of the two interfaces. I reviewed the generated code and adapted it to the fairy-tale retellings topic, selected the interpretive fields, and should test both interfaces with sample records before submission. I should also verify the accuracy of each cultural interpretation rather than treating the sample interpretations as unquestionable facts.

## Testing checklist

- [ ] Install Rich using `requirements.txt`.
- [ ] Run the CLI and confirm the example table appears.
- [ ] Add one record and confirm it; verify the JSON file changes.
- [ ] Reject an entry and check that the CLI asks for the record again.
- [ ] Add a second record.
- [ ] Open `index.html` and try submitting with a required field blank.
- [ ] Add at least two HTML records, then download and open the JSON file.
- [ ] Check the files into the required `python-libraries` folder and push them to GitHub.

## AI use

This project used AI assistance to draft and revise code and documentation. See `ai-chat-log.md` for a summary of the assistance.
