# IMPORTANT
# Must have structure: 
#   - namespace: <studioName>_<projectName>
#   - directory example: ...<projectNameCamel>/<projectNameCamel>-BP/...
#   - file name, identifier and actual name are similar: awesome_sword.item.json --> <namespace>:awesome_sword --> Awesome Sword
#
# Created by QuantumNek0

import os
import tkinter as tk
from tkinter import filedialog
from typing import TextIO


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    directory_path = filedialog.askdirectory(title="Select project location.")
    if not directory_path: return
        
    project_name = os.path.basename(directory_path)

    lang_path = directory_path + f"/{project_name}-RP/texts/en_US.lang"
    if not os.path.exists(lang_path): return

    item_files, block_files, entity_files = getAllFiles(directory_path + f"/{project_name}-BP")
    namespace = input("namespace: ")

    with open(lang_path, 'r+', encoding='utf-8') as f:        
        writeKeys(f, item_files, namespace, "item")
        writeKeys(f, block_files, namespace, "block")
        writeKeys(f, entity_files, namespace, "entity")


def writeKeys(lang_file: TextIO, files: list[str], namespace: str, mode: str):
    if not files: return
    contents = lang_file.read()

    if not contents.endswith('\n'):
        lang_file.write('\n')
        contents += '\n'

    for file in files:
        identifier, natural_name = formatFileName(file)
        
        match mode:

            case "item":
                key = f"item.{namespace}:{identifier}="

            case "block":
                key = f"tile.{namespace}:{identifier}.name="

            case "entity":
                key = f"entity.{namespace}:{identifier}.name="

            case _:
                raise ValueError("Invalid mode.")
        
        if (key not in contents): lang_file.write(key + natural_name + '\n')


def getAllFiles(directory: str) -> tuple[list[str], list[str], list[str]]:

    item_files = getFiles(directory + "/items", ".json")
    entity_files = getFiles(directory + "/entities", ".json")
    block_files = getFiles(directory + "/blocks", ".json")

    return item_files, block_files, entity_files


def getFiles(directory: str, extension: str) -> list[str]:
    files: list[str] = []

    for _, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(extension):
                files.append(filename)

    return files


def formatFileName(filename: str) -> tuple[str, str]:
    natural_name = filename
    
    # remove the file extension (probably .json)
    natural_name = os.path.splitext(natural_name)[0]
    # remove the second extension if any (either .item or .block)
    natural_name = os.path.splitext(natural_name)[0]
    identifier = natural_name

    natural_name = natural_name.replace('_', ' ')    
    natural_name = natural_name.title()
    
    return identifier, natural_name


if __name__ == "__main__":
    main()
