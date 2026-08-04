import csv
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# 자동으로 저장 및 로드할 기본 데이터 파일명
AUTO_SAVE_FILE = "library_data.json"


class BookManager:
    """도서 데이터 및 비즈니스 로직 관리 클래스"""

    def __init__(self):
        self.books = []

    def _reindex_books(self):
        """도서 번호(ID)를 1번부터 순서대로 재정렬"""
        for index, book in enumerate(self.books, start=1):
            book["id"] = index

    def add_book(self, title, author, status="대출 가능"):
        book = {
            "id": len(self.books) + 1,
            "title": title,
            "author": author,
            "status": status,
        }
        self.books.append(book)

    def delete_book(self, book_id):
        self.books = [b for b in self.books if b["id"] != book_id]
        self._reindex_books()

    def toggle_borrow(self, book_id):
        for b in self.books:
            if b["id"] == book_id:
                b["status"] = (
                    "대출 중" if b["status"] == "대출 가능" else "대출 가능"
                )
                return True
        return False

    # JSON 저장 및 불러오기
    def save_json(self, filepath):
        self._reindex_books()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_json(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                self.books = data.get("books", [])
            else:
                self.books = data
            self._reindex_books()

    # CSV 내보내기 및 가져오기 (utf-8-sig 적용)
    def export_csv(self, filepath):
        self._reindex_books()
        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "도서명", "저자", "대출 상태"])
            for b in self.books:
                writer.writerow(
                    [b["id"], b["title"], b["author"], b["status"]]
                )

    def import_csv(self, filepath):
        with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            new_books = []
            for row in reader:
                if len(row) >= 3:
                    title = row[1]
                    author = row[2]
                    status = row[3] if len(row) > 3 else "대출 가능"
                    new_books.append(
                        {"id": 0, "title": title, "author": author, "status": status}
                    )

            if new_books:
                self.books = new_books
                self._reindex_books()


class LibraryApp(tk.Tk):
    """Tkinter 기반 GUI 애플리케이션 클래스"""

    def __init__(self):
        super().__init__()
        self.title("도서관리 시스템 (자동 저장 / 수동 저장 지원)")
        self.geometry("740x580")
        self.resizable(False, False)

        self.manager = BookManager()

        # 1. 실행 시 기존 자동 저장 파일(library_data.json)이 있으면 자동 로드
        if os.path.exists(AUTO_SAVE_FILE):
            try:
                self.manager.load_json(AUTO_SAVE_FILE)
            except Exception:
                self._init_sample_data()
        else:
            self._init_sample_data()

        self._init_ui()
        self._refresh_tree()

        # 2. 창 닫기 버튼(X) 클릭 시 자동 저장 이벤트 연결
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _init_sample_data(self):
        self.manager.add_book("파이썬 정복", "김파이")
        self.manager.add_book("C++ 프로그래밍", "이씨쁠", "대출 중")

    def _init_ui(self):
        # 상단 입력 폼
        input_frame = tk.LabelFrame(self, text="도서 등록", padx=10, pady=10)
        input_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(input_frame, text="도서명:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.entry_title = tk.Entry(input_frame, width=22)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="저자:").grid(
            row=0, column=2, padx=5, pady=5, sticky="e"
        )
        self.entry_author = tk.Entry(input_frame, width=22)
        self.entry_author.grid(row=0, column=3, padx=5, pady=5)

        btn_add = tk.Button(
            input_frame,
            text="추가",
            width=8,
            command=self._on_add,
            bg="#4CAF50",
            fg="white",
        )
        btn_add.grid(row=0, column=4, padx=10, pady=5)

        # 파일 데이터 관리 프레임
        file_frame = tk.LabelFrame(
            self, text="수동 파일 저장 / 불러오기 (JSON / CSV)", padx=10, pady=5
        )
        file_frame.pack(fill="x", padx=15, pady=5)

        btn_save_json = tk.Button(
            file_frame, text="JSON 저장", command=self._on_save_json, width=13
        )
        btn_save_json.pack(side="left", padx=5, pady=5)

        btn_load_json = tk.Button(
            file_frame, text="JSON 불러오기", command=self._on_load_json, width=13
        )
        btn_load_json.pack(side="left", padx=5, pady=5)

        btn_export_csv = tk.Button(
            file_frame,
            text="CSV 내보내기",
            command=self._on_export_csv,
            width=13,
            bg="#2196F3",
            fg="white",
        )
        btn_export_csv.pack(side="left", padx=5, pady=5)

        btn_import_csv = tk.Button(
            file_frame,
            text="CSV 가져오기",
            command=self._on_import_csv,
            width=13,
        )
        btn_import_csv.pack(side="left", padx=5, pady=5)

        # 목록 표시 (Treeview)
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=5)

        columns = ("id", "title", "author", "status")
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", height=10
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="도서명")
        self.tree.heading("author", text="저자")
        self.tree.heading("status", text="대출 상태")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("title", width=320, anchor="w")
        self.tree.column("author", width=190, anchor="w")
        self.tree.column("status", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 하단 기능 버튼
        btn_frame = tk.Frame(self, pady=10)
        btn_frame.pack(fill="x", padx=15)

        btn_borrow = tk.Button(
            btn_frame, text="대출 / 반납 전환", command=self._on_toggle_borrow
        )
        btn_borrow.pack(side="left", padx=5)

        btn_delete = tk.Button(
            btn_frame,
            text="선택 삭제",
            command=self._on_delete,
            bg="#f44336",
            fg="white",
        )
        btn_delete.pack(side="left", padx=5)

        # 3. 수동 즉시 저장 버튼 추가
        btn_quick_save = tk.Button(
            btn_frame,
            text="현재 상태 즉시 저장",
            command=self._on_manual_quick_save,
            bg="#FF9800",
            fg="white",
        )
        btn_quick_save.pack(side="right", padx=5)

    def _refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for book in self.manager.books:
            self.tree.insert(
                "",
                "end",
                values=(
                    book["id"],
                    book["title"],
                    book["author"],
                    book["status"],
                ),
            )

    def _on_add(self):
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        if not title or not author:
            messagebox.showwarning("입력 오류", "도서명과 저자를 모두 입력해주세요.")
            return

        self.manager.add_book(title, author)
        self._refresh_tree()
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        messagebox.showinfo("성공", f"'{title}' 도서가 등록되었습니다.")

    def _get_selected_book_id(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("선택 오류", "목록에서 도서를 먼저 선택해주세요.")
            return None
        item_values = self.tree.item(selected_item[0], "values")
        return int(item_values[0])

    def _on_toggle_borrow(self):
        book_id = self._get_selected_book_id()
        if book_id is None:
            return
        if self.manager.toggle_borrow(book_id):
            self._refresh_tree()

    def _on_delete(self):
        book_id = self._get_selected_book_id()
        if book_id is None:
            return
        if messagebox.askyesno("삭제 확인", "선택한 도서를 삭제하시겠습니까?"):
            self.manager.delete_book(book_id)
            self._refresh_tree()

    def _on_manual_quick_save(self):
        """수동 즉시 저장: 현재 데이터를 library_data.json 파일에 저장"""
        try:
            self.manager.save_json(AUTO_SAVE_FILE)
            messagebox.showinfo("저장 완료", "현재 도서 목록이 저장되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"저장 중 오류가 발생했습니다:\n{e}")

    def _on_save_json(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if filepath:
            try:
                self.manager.save_json(filepath)
                messagebox.showinfo(
                    "저장 완료", "JSON 파일로 성공적으로 저장되었습니다."
                )
            except Exception as e:
                messagebox.showerror(
                    "오류", f"저장 중 오류가 발생했습니다:\n{e}"
                )

    def _on_load_json(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        if filepath:
            try:
                self.manager.load_json(filepath)
                self._refresh_tree()
                messagebox.showinfo(
                    "불러오기 완료", "JSON 파일에서 데이터를 불러왔습니다."
                )
            except Exception as e:
                messagebox.showerror(
                    "오류", f"불러오기 중 오류가 발생했습니다:\n{e}"
                )

    def _on_export_csv(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
        )
        if filepath:
            try:
                self.manager.export_csv(filepath)
                messagebox.showinfo(
                    "내보내기 완료",
                    "CSV 파일로 저장되었습니다.\n(엑셀에서 정상 열림)",
                )
            except Exception as e:
                messagebox.showerror(
                    "오류", f"CSV 저장 중 오류가 발생했습니다:\n{e}"
                )

    def _on_import_csv(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )
        if filepath:
            try:
                self.manager.import_csv(filepath)
                self._refresh_tree()
                messagebox.showinfo(
                    "가져오기 완료",
                    "CSV 파일 데이터를 불러왔습니다.",
                )
            except Exception as e:
                messagebox.showerror(
                    "오류", f"CSV 불러오기 중 오류가 발생했습니다:\n{e}"
                )

    def _on_closing(self):
        """종료 시 자동 저장: 창 닫을 때 library_data.json 파일에 데이터 저장 후 종료"""
        try:
            self.manager.save_json(AUTO_SAVE_FILE)
        except Exception as e:
            print(f"자동 저장 실패: {e}")
        self.destroy()


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()