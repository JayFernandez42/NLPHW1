# Name(s): Jacob Fernandez, Grant Zhao
# Netid(s): jaf388, gz233

################### IMPORTS - DO NOT ADD, REMOVE, OR MODIFY ####################
import json
import zipfile
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np

## ================ Helper functions for loading data ==========================

def unzip_file(zip_filepath, dest_path):
  """
  Returns boolean indication of whether the file was successfully unzipped.

  Input:
    zip_filepath: String, path to the zip file to be unzipped
    dest_path: String, path to the directory to unzip the file to
  Output:
    result: Boolean, True if file was successfully unzipped, False otherwise
  """
  try:
    with zipfile.ZipFile(zip_filepath, "r") as zip_ref:
        zip_ref.extractall(dest_path)
    return True
  except Exception as e:
    return False


def unzip_data(zipTarget, destPath):
  """
  Unzips a directory, and places the contents in the original zipped
  folder into a folder at destPath. Overwrites contents of destPath if it
  already exists.

  Input:
          None
  Output:
          None

  E.g. if zipTarget = "../dataset/student_dataset.zip" and destPath = "data"
        then the contents of the zip file will be unzipped into a directory
        called "data" in the cwd.
  """
  # First, remove the destPath directory if it exists
  if os.path.exists(destPath):
    shutil.rmtree(destPath)

  unzip_file(zipTarget, destPath)

  # Get the name of the subdirectory
  sub_dir_name = os.path.splitext(os.path.basename(zipTarget))[0]
  sub_dir_path = os.path.join(destPath, sub_dir_name)

  # Move all files from the subdirectory to the parent directory
  for filename in os.listdir(sub_dir_path):
    shutil.move(os.path.join(sub_dir_path, filename), destPath)

  # Remove the subdirectory
  os.rmdir(sub_dir_path)


def read_json(filepath):
  """
  Reads a JSON file and returns the contents of the file as a dictionary.

  Input:
    filepath: String, path to the JSON file to be read
  Output:
    result: Dict, representing the contents of the JSON file
  """
  with open(filepath, "r",encoding = "utf-8") as f:
    return json.load(f)


def load_dataset(data_zip_path, dest_path):
  """
  Returns the training, validation, and test data as dictionaries.

  Input:
    data_zip_path: String, representing the path to the zip file containing the
    data
    dest_path: String, representing the path to the directory to unzip the data
    to
  Output:
    training_data: Dict, representing the training data
    validation_data: Dict, representing the validation data
    test_data: Dict, representing the test data
  """
  unzip_data(data_zip_path, dest_path)
  training_data = read_json(os.path.join(dest_path, "train.json"))
  validation_data = read_json(os.path.join(dest_path, "val.json"))
  test_data = read_json(os.path.join(dest_path, "test.json"))
  return training_data, validation_data, test_data

## =============================================================================

################################################################################
# NOTE: Do NOT change any of the function headers and/or specs!
# The input(s) and output must perfectly match the specs, or else your 
# implementation for any function with changed specs will most likely fail!
################################################################################

## ================== Functions for students to implement ======================

def stringify_labeled_doc(text, ner):
  """
  Returns a string representation of a tagged sentence from the dataset.
  Named entities are grouped and formatted as [TAG token1 token2 ... tokenN].
  BIO prefixes are stripped. 'O' tokens are ignored.
  """
  if not text or not ner:
    return ""

  result = []
  current_entity = []
  current_tag = None

  for token, tag in zip(text, ner):
    if tag.startswith("B-"):  # New entity starts
      if current_entity:
        result.append(f"[{current_tag} {' '.join(current_entity)}]")
      current_entity = [token]
      current_tag = tag[2:]
    elif tag.startswith("I-") and current_tag == tag[2:]:
      current_entity.append(token)
    else:
      if current_entity:  # Close previous entity
        result.append(f"[{current_tag} {' '.join(current_entity)}]")
        current_entity = []
        current_tag = None
      if tag == "O":  # Non-entity word
        result.append(token)

  if current_entity:
    result.append(f"[{current_tag} {' '.join(current_entity)}]")

  return " ".join(result)


def validate_ner_sequence(ner):
  """
  Validates whether a named entity list follows BIO constraints.
  """
  if not ner:
    return True

  previous_tag = "O"

  for tag in ner:
    if tag.startswith("I-"):
      if previous_tag == "O" or (previous_tag.startswith("B-") and previous_tag[2:] != tag[2:]) or (previous_tag.startswith("I-") and previous_tag[2:] != tag[2:]):
        return False
    previous_tag = tag

  return True
