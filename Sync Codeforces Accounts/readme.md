
# Codeforces Problem Synchronization and Submission

## Overview

This Python script allows you to synchronize and submit accepted problems from one Codeforces account to another. It uses the Codeforces API for retrieving problem statuses and Selenium for automating the submission process.

## Features

- Retrieves accepted problems from one Codeforces account (`syncWith`) and marks them for submission to another account (`sync`).
- Logs in to Codeforces using Selenium WebDriver.
- Copies and submits the solution for each accepted problem.

## Prerequisites

- Python 3.x
- `requests` library: `pip install requests`
- Selenium WebDriver for Chrome: Download from [ChromeDriver](https://sites.google.com/chromium.org/driver/)

## Usage

1. Install the required Python libraries:
   ```bash
   pip install requests selenium
   ```

2. Download and configure the ChromeDriver executable: [ChromeDriver](https://sites.google.com/chromium.org/driver/)

3. Update the following variables in the script:
   - `username`: Codeforces handle for the account from which problems will be synced.
   - `password`: Password for the above Codeforces account.
   - `syncWith`: Codeforces handle for the account with accepted problems to be submitted.
   - `sync`: Codeforces handle for the account to which problems will be submitted.

4. Run the script:
   ```bash
   python script_name.py
   ```

## Script Execution Flow

1. Log in to Codeforces using the specified account credentials.
2. Retrieve accepted problems from the source account (`syncWith`).
3. Copy and submit each accepted problem to the target account (`sync`).

## Disclaimer

Use this script responsibly and in compliance with Codeforces terms of service. Automated submissions and scraping may be against the platform's rules.

---

