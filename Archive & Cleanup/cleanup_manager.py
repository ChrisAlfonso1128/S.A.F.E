from pathlib import Path
import shutil


class CleanupManager:

    def __init__(self):

        self.trash_folder = Path("Trash")

        self.trash_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    def move_to_trash(self, file_list):

        moved = []

        failed = []

        for file in file_list:

            try:

                source = Path(file)

                if source.exists():

                    destination = self.trash_folder / source.name

                    shutil.move(source, destination)

                    moved.append(source.name)

            except Exception as e:

                failed.append({
                    "file": file,
                    "error": str(e)
                })

        return moved, failed
