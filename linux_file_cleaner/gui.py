import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from .core import (
    bytes_to_human,
    cleanup_preview,
    disk_usage,
    find_empty_folders,
    find_large_files,
)


class LinuxFileCleanerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Linux File Cleaner")
        self.root.geometry("900x620")
        self.root.minsize(800, 520)

        self.selected_folder = tk.StringVar(value=str(Path.home()))

        self.build_ui()

    def build_ui(self) -> None:
        header = tk.Frame(self.root, padx=14, pady=12)
        header.pack(fill="x")

        title = tk.Label(header, text="Linux File Cleaner", font=("Arial", 20, "bold"))
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="GUI утилита для анализа диска, поиска больших файлов и проверки мусора в Linux",
            font=("Arial", 11),
        )
        subtitle.pack(anchor="w")

        controls = tk.Frame(self.root, padx=14, pady=8)
        controls.pack(fill="x")

        tk.Label(controls, text="Папка:").pack(side="left")
        entry = tk.Entry(controls, textvariable=self.selected_folder)
        entry.pack(side="left", fill="x", expand=True, padx=8)

        tk.Button(controls, text="Выбрать", command=self.choose_folder).pack(side="left", padx=4)
        tk.Button(controls, text="Большие файлы", command=self.show_large_files).pack(side="left", padx=4)
        tk.Button(controls, text="Пустые папки", command=self.show_empty_folders).pack(side="left", padx=4)
        tk.Button(controls, text="Диск", command=self.show_disk_usage).pack(side="left", padx=4)
        tk.Button(controls, text="Мусор", command=self.show_cleanup_preview).pack(side="left", padx=4)

        self.output = tk.Text(self.root, wrap="word", font=("Consolas", 11), padx=10, pady=10)
        self.output.pack(fill="both", expand=True, padx=14, pady=10)

        footer = tk.Frame(self.root, padx=14, pady=8)
        footer.pack(fill="x")
        ttk.Button(footer, text="Очистить вывод", command=self.clear_output).pack(side="right")

        self.write("Готово. Выбери папку и нажми нужную кнопку.\n")

    def write(self, text: str) -> None:
        self.output.insert("end", text)
        self.output.see("end")

    def clear_output(self) -> None:
        self.output.delete("1.0", "end")

    def choose_folder(self) -> None:
        folder = filedialog.askdirectory(initialdir=self.selected_folder.get())
        if folder:
            self.selected_folder.set(folder)

    def get_folder(self) -> str:
        folder = self.selected_folder.get().strip()
        if not folder:
            messagebox.showerror("Ошибка", "Выбери папку")
            return str(Path.home())
        return folder

    def show_large_files(self) -> None:
        folder = self.get_folder()
        self.clear_output()
        self.write(f"Поиск больших файлов в папке: {folder}\n\n")
        files = find_large_files(folder, limit=25)
        if not files:
            self.write("Файлы не найдены или нет доступа к папке.\n")
            return
        for index, (path, size) in enumerate(files, start=1):
            self.write(f"{index:02d}. {bytes_to_human(size):>10}  {path}\n")

    def show_empty_folders(self) -> None:
        folder = self.get_folder()
        self.clear_output()
        self.write(f"Поиск пустых папок в: {folder}\n\n")
        folders = find_empty_folders(folder, limit=50)
        if not folders:
            self.write("Пустые папки не найдены.\n")
            return
        for index, path in enumerate(folders, start=1):
            self.write(f"{index:02d}. {path}\n")

    def show_disk_usage(self) -> None:
        folder = self.get_folder()
        self.clear_output()
        info = disk_usage(folder)
        self.write("Использование диска:\n\n")
        self.write(f"Всего:     {info['total_human']}\n")
        self.write(f"Занято:    {info['used_human']}\n")
        self.write(f"Свободно:  {info['free_human']}\n")

    def show_cleanup_preview(self) -> None:
        self.clear_output()
        self.write("Предпросмотр папок, где часто хранится временный мусор:\n\n")
        items = cleanup_preview()
        if not items:
            self.write("Папки для анализа не найдены.\n")
            return
        for path, size in items:
            self.write(f"{bytes_to_human(size):>10}  {path}\n")
        self.write("\nПрограмма показывает размер, но специально не удаляет файлы автоматически, чтобы не сломать систему.\n")


def main() -> None:
    root = tk.Tk()
    app = LinuxFileCleanerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
