# IMPORTANT
# Must have structure: 
#   - namespace: <studioName>_<projectName>
#   - directory example: .../<projectNameCamel>-BP/items/<studioName>/<projectName>/...
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
        contents = f.read()
        
        if contents[-1] != '\n': f.write('\n')
        writeNames(f, item_files, namespace, "item")
        writeNames(f, block_files, namespace, "block")
        writeNames(f, entity_files, namespace, "entity")



def writeNames(lang_file: TextIO, files: list[str], namespace: str, mode: str):
    if not files: return

    match mode:
        case "item":
            for file in files:
                identifier, natural_name = formatFileName(file)
                lang_file.write(f"item.{namespace}:{identifier}=" + natural_name + '\n')

        case "block":
            for file in files:
                identifier, natural_name = formatFileName(file)
                lang_file.write(f"tile.{namespace}:{identifier}.name=" + natural_name + '\n')

        case "entity":
            for file in files:
                identifier, natural_name = formatFileName(file)
                lang_file.write(f"entity.{namespace}:{identifier}.name=" + natural_name + '\n')

        case _:
            return


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

# AI slop here, can't be bothered to format strings lol
def formatFileName(filename: str):
    # Remove extension(s)
    name = os.path.splitext(filename)[0]  # removes last extension
    name = name.replace('.', '_')  # replace any remaining dots with underscores

    parts = name.split('_')
    if parts[0].lower() == "tnt":
        # TNT at start: move to end for formatted, keep in name
        formatted = " ".join(word.capitalize() for word in parts[1:]) + " TNT"
    else:
        # TNT elsewhere: move to end for formatted, keep in name
        if "tnt" in parts:
            tnt_index = parts.index("tnt")
            formatted = " ".join(word.capitalize() for i, word in enumerate(parts) if i != tnt_index) + " TNT"
        else:
            formatted = " ".join(word.capitalize() for word in parts)
    return name, formatted


if __name__ == "__main__":
    main()
