import pandas as pd
import subprocess
import os
import shutil


print("*** Running Script by Pritish ***")

print("Reading JSON Data...")

df = pd.read_json("inhibitors.json")

print("Building files from Data...")

directory = "smiles"

if os.path.exists(directory):
    print("directory exists")
else:
    os.makedirs(directory)

for index, row in df.iterrows():
    value = row["SMILES"]

    file_name = f"{index}_{row['name']}.can"

    file_path = f"{directory}/{file_name}"

    with open(file_path, "w") as file:
        file.write(str(value))
print("Files created!")

if shutil.which("avogadro"):
    command = f"avogadro {directory}/*.can"
    subprocess.run(command, shell=True)
else:
    if (
        shutil.which("flatpak")
        and subprocess.run(
            "flatpak list | grep org.openchemistry.Avogadro2",
            shell=True,
            stdout=subprocess.DEVNULL,
        ).returncode
        == 0
    ):
        flatpak_command = f"flatpak run org.openchemistry.Avogadro2 {directory}/*.can"
        subprocess.run(flatpak_command, shell=True)
    else:
        print("Avogadro or Avogadro Flatpak is not available on the system.")
