from pathlib import Path

from archive_manager import ArchiveManager
from cleanup_manager import CleanupManager
from history_logger import HistoryLogger


class UserInterface:
    """
    Command-line menu for S.A.F.E — lets the user browse a folder,
    pick files, and archive or trash them.
    """

    def __init__(self):

        self.archive = ArchiveManager()

        self.cleanup = CleanupManager()

        self.logger = HistoryLogger()

    def run(self):

        while True:

            self.show_menu()

            choice = input("Select an option: ").strip()

            if choice == "1":
                self.handle_archive()

            elif choice == "2":
                self.handle_trash()

            elif choice == "3":
                self.show_history()

            elif choice == "4":
                print("\nExiting S.A.F.E. Goodbye!")
                break

            else:
                print("\nInvalid option, try again.")

    def show_menu(self):

        print("\n===== S.A.F.E Menu =====")
        print("1. Archive files")
        print("2. Move files to Trash")
        print("3. View history")
        print("4. Exit")

    def handle_archive(self):

        files = self.pick_files()

        if not files:
            return

        result = self.archive.archive_files(files)

        if result:
            for file in files:
                self.logger.log("Archived", file)

    def handle_trash(self):

        files = self.pick_files()

        if not files:
            return

        moved, failed = self.cleanup.move_to_trash(files)

        for file in moved:
            self.logger.log("Moved to Trash", file)

        if failed:
            print("\nSome files could not be moved:")
            for entry in failed:
                print(f"  {entry['file']} — {entry['error']}")

    def show_history(self):

        import json

        if not self.logger.log_file.exists():
            print("\nNo history yet.")
            return

        with open(self.logger.log_file, "r") as f:
            history = json.load(f)

        if not history:
            print("\nNo history yet.")
            return

        print("\n===== History =====")

        for entry in history:
            print(f"{entry['date']}  {entry['action']:<15}  {entry['file']}")

    def pick_files(self):
        """
        Prompts for a folder, lists its files, and lets the user
        pick which ones to act on. Returns a list of file paths.
        """

        folder_input = input(
            "\nEnter a folder path (or press Enter to cancel): "
        ).strip()

        if not folder_input:
            return []

        folder = Path(folder_input)

        if not folder.is_dir():
            print("That folder doesn't exist.")
            return []

        files = [f for f in folder.iterdir() if f.is_file()]

        if not files:
            print("No files found in that folder.")
            return []

        print("\nFiles found:")

        for i, file in enumerate(files, start=1):
            print(f"  {i}. {file.name}")

        selection = input(
            "\nEnter file numbers separated by commas, or 'all': "
        ).strip()

        if selection.lower() == "all":
            return [str(f) for f in files]

        chosen = []

        for part in selection.split(","):

            part = part.strip()

            if not part.isdigit():
                continue

            index = int(part) - 1

            if 0 <= index < len(files):
                chosen.append(str(files[index]))

        if not chosen:
            print("No valid files selected.")

        return chosen


if __name__ == "__main__":

    ui = UserInterface()

    ui.run()
