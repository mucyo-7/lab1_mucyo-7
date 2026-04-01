#!/bin/bash
# organizer.sh
# Automates the archiving of grades.csv and logs the operation.

# -------------------------------------------------------
# Step 1: Check if the archive directory exists.
# If it doesn't, create it to store old grade files.
# -------------------------------------------------------
if [ ! -d "archive" ]; then
    mkdir archive
    echo "Created archive directory."
fi

# -------------------------------------------------------
# Step 2: Generate a timestamp string for the filename.
# Format: YYYYMMDD-HHMMSS (e.g., 20251105-170000)
# -------------------------------------------------------
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# -------------------------------------------------------
# Step 3: Check if grades.csv exists before trying to archive it.
# If it doesn't exist, we cannot proceed.
# -------------------------------------------------------
if [ ! -f "grades.csv" ]; then
    echo "Error: grades.csv not found. Nothing to archive."
    exit 1
fi

# -------------------------------------------------------
# Step 4: THE ARCHIVAL PROCESS
# Rename grades.csv by appending the timestamp,
# then move it into the archive directory.
# -------------------------------------------------------
NEW_NAME="grades_${TIMESTAMP}.csv"
mv grades.csv "archive/${NEW_NAME}"
echo "Archived grades.csv as archive/${NEW_NAME}"

# -------------------------------------------------------
# Step 5: WORKSPACE RESET
# Create a fresh empty grades.csv so the environment
# is ready for the next batch of grades.
# -------------------------------------------------------
touch grades.csv
echo "Created new empty grades.csv for next batch."

# -------------------------------------------------------
# Step 6: LOGGING
# Append the details of this operation to organizer.log.
# The log accumulates entries from every run.
# -------------------------------------------------------
LOG_ENTRY="[${TIMESTAMP}] Archived: grades.csv -> archive/${NEW_NAME}"
echo "$LOG_ENTRY" >> organizer.log
echo "Logged operation to organizer.log"
echo "Done."
