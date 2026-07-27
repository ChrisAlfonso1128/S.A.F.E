from pathlib import Path
from datetime import datetime
import shutil


class ArchiveManager:
    """
    Handles archiving files into timestamped ZIP archives.
    """

    def __init__(self, archive_folder="SAFE_Data/Archive"):

        self.archive_folder = Path(archive_folder)

        self.archive_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    def archive_files(self, file_list):

        if not file_list:
            print("No files selected.")
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        temp_folder = self.archive_folder / f"Archive_{timestamp}"

        temp_folder.mkdir(exist_ok=True)

        copied = 0

        for file in file_list:

            try:

                source = Path(file)

                if source.exists():

                    destination = temp_folder / source.name

                    shutil.copy2(source, destination)

                    copied += 1

            except Exception as e:

                print(f"Could not archive {file}")

                print(e)

        zip_name = shutil.make_archive(
            str(temp_folder),
            "zip",
            root_dir=temp_folder
        )

        shutil.rmtree(temp_folder)

        print(f"\nArchived {copied} files.")
        print(zip_name)

        return zip_name
