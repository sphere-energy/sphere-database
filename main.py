import boto3
import logging
from tqdm import tqdm
from transform.ingest_raw_data import IngestRawData
import os

# ingestor = IngestRawData("csv/1734001334_11_2_OAD-407-2_Cycle951-1100.csv")
# ingestor.ingest_csv()

logging.basicConfig(level=logging.INFO)


bucket_name = 'sphere-arbin-analysis-prd'
s3 = boto3.resource('s3')  # Replace with your keys and region
all_files = []
# Get all objects in the bucket and their date last modified
for obj in s3.Bucket(bucket_name).objects.all():
    all_files.append(obj)

correct_ingested_files_path = "correct_ingested_files.txt"
fail_files_path = "fail_ingested_files.txt"

# Load already ingested files
def load_file_list(file_path):
    """Load a list of files from a text file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return set(f.read().splitlines())
        except IOError as e:
            logging.error(f"Error loading file list from {file_path}: {e}")
    return set()

def update_file_list(file_path, file_name):
    """Append a filename to a list in a file."""
    try:
        with open(file_path, "a") as f:
            f.write(file_name + "\n")
        return True
    except IOError as e:
        logging.error(f"Error updating file list in {file_path}: {e}")
        return False

def update_ingested_files(file_name, success=True):
    """Update the appropriate file list based on ingestion success."""
    path = correct_ingested_files_path if success else fail_files_path
    return update_file_list(path, file_name)

# Load already ingested files
correct_ingested_files = load_file_list(correct_ingested_files_path)
fail_ingested_files = load_file_list(fail_files_path)

# for f in all_files:
#     if f.key in correct_ingested_files or f.key in fail_ingested_files:
#         print(f.key)
# Filter out already ingested files
csv_files = [f.key for f in all_files if f.key not in correct_ingested_files and f.key not in fail_ingested_files]
s3 = boto3.client('s3')

for file in tqdm(csv_files, desc="Processing files...", disable=False if len(csv_files) > 0 else True):
    logging.info(f"Processing file {file}")
    if not "Arbin5" in file:
        continue

    if not os.path.exists(f"raw_data/{file}"):
        s3.download_file(bucket_name, file, f"raw_data/{file}")

    raw_data_path = "raw_data"

    ingestor = IngestRawData(os.path.join(raw_data_path, file))
    id1, id2 = ingestor.ingest_csv()

    if not id1 or not id2:
        logging.info(f"Error processing file {file}")
        update_ingested_files(file, success=False)
    else:
        update_ingested_files(file, success=True)
