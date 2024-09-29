import os

class FileSelector:
    def __init__(self):
        self.csv_files = self.find_csv_files()
        self.current_index = 0


    def find_csv_files(self):
        csv_files = []
        for file in os.listdir('.'):
            if file.startswith("data_") and file.endswith(".csv") and len(file) == 24:
                csv_files.append(file)
        return csv_files

    def prev_file(self):
        if self.current_index > 0:
            self.current_index -= 1
            # self.plot_current_file()

    def next_file(self):
        if self.current_index < len(self.csv_files) - 1:
            self.current_index += 1
            # self.plot_current_file()

if __name__ == "__main__":
    file_selector = FileSelector()
    print(file_selector.csv_files)

