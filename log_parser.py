import tkinter as tk
from tkinter import filedialog, ttk, simpledialog
import os
import re

class LogFileViewer:
    def __init__(self, root):
        self.root = root
        root.title("Log File Viewer")

        # 로그 파일 선택 버튼
        self.load_button = tk.Button(root, text="Load Log File", command=self.load_log_file)
        self.load_button.pack()

        # 검색 입력 필드와 검색 버튼
        self.search_frame = tk.Frame(root)
        self.search_frame.pack()
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search_logs)
        self.search_button.pack(side=tk.LEFT)

        # 트리뷰와 스크롤바를 담을 프레임 생성
        self.tree_frame = tk.Frame(root)
        self.tree_frame.pack(expand=True, fill=tk.BOTH)

        # 트리뷰 설정
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # 트리뷰 스크롤바 설정
        self.tree_scroll = tk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree_scroll.pack(side=tk.RIGHT, fill="y")
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        # 로그 표시 영역과 스크롤바를 담을 프레임 생성
        self.log_frame = tk.Frame(root, height=15)
        self.log_frame.pack(expand=True, fill=tk.BOTH)

        # 로그 표시 영역
        self.log_display = tk.Text(self.log_frame)
        self.log_display.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # 로그 표시 영역 스크롤바 설정
        self.log_scroll = tk.Scrollbar(self.log_frame, orient="vertical", command=self.log_display.yview)
        self.log_scroll.pack(side=tk.RIGHT, fill="y")
        self.log_display.configure(yscrollcommand=self.log_scroll.set)

        self.log_file_path = ""
        self.last_search_start = "1.0"  # 검색이 시작된 마지막 위치를 저장하기 위한 변수 추가
        
    def load_log_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Log files", "*.log"), ("All files", "*.*")])
        if filepath:
            self.log_file_path = filepath
            self.parse_log_file()

    def parse_log_file(self):
        self.file_paths = []
        with open(self.log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            # GET 또는 POST 뒤의 파일 경로 추출 수정
            for line in file:
                matches = re.findall(r'(GET|POST) (.+?) HTTP', line)
                self.file_paths.extend([match[1] for match in matches])  # 경로 부분만 추출하여 추가
        
        
        # 중복 제거 후 정렬
        self.file_paths = sorted(set(self.file_paths))
        
        # 트리뷰 업데이트
        self.update_tree_view()

    def update_tree_view(self):
        # 트리뷰 초기화
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 루트 노드 추가
        self.tree.insert("", 'end', '/', text="/")

        # 트리에 경로 추가
        for path in self.file_paths:
            self.insert_path_into_tree(path)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def insert_path_into_tree(self, path):
        parts = path.strip('/').split('/')  # 경로 앞의 '/' 제거
        parent_id = '/'
        for part in parts:
            if part:  # 빈 문자열이 아닌 경우에만 처리
                current_id = parent_id + part if parent_id == '/' else parent_id + '/' + part
            else:
                # 루트 경로('/')의 경우
                current_id = '/'
            if not self.tree.exists(current_id):
                self.tree.insert(parent_id, 'end', current_id, text=part)
            parent_id = current_id

                
    def on_tree_select(self, event):
        selected_item = self.tree.selection()[0]
        # 선택된 아이템의 전체 경로를 구성
        file_path = ''
        first_iteration = True
        while selected_item != '':
            # 첫 번째 항목에는 슬래시를 추가하지 않음
            if first_iteration:
                file_path = self.tree.item(selected_item, "text") + file_path
                first_iteration = False
            else:
                file_path = self.tree.item(selected_item, "text") + '/' + file_path
            selected_item = self.tree.parent(selected_item)

        # 맨 앞의 '//'를 '/'로 대체
        file_path = re.sub(r'^//', '/', file_path)
    
        self.display_logs(file_path)
        #print(file_path)  # 디버깅을 위해 최종 경로 출력


    def display_logs(self, file_path):
        self.log_display.delete(1.0, tk.END)  # 로그 영역 초기화
        normalized_path = file_path.replace(os.sep, '/')  # 시스템에 맞는 경로 구분자로 변경
        with open(self.log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                if normalized_path in line:  # 시스템에 맞게 정규화된 경로가 로그에 포함되어 있는지 확인
                    self.log_display.insert(tk.END, line)

    def search_logs(self):
        search_query = self.search_entry.get()
        if search_query:
            self.highlight_text(search_query, reset_search=False)

    def highlight_text(self, search_query, reset_search=True):
        if reset_search:
            self.last_search_start = "1.0"
            self.log_display.tag_remove('found', '1.0', tk.END)

        start = self.last_search_start
        start = self.log_display.search(search_query, start, stopindex=tk.END)
        if not start:
            self.last_search_start = "1.0"  # 검색 결과가 더 이상 없으면 다시 처음부터 시작
            return
        end = f"{start}+{len(search_query)}c"
        self.log_display.tag_add('found', start, end)
        self.log_display.tag_config('found', background='yellow')
        self.log_display.see(start)  # 검색된 위치로 스크롤
        self.last_search_start = end  # 다음 검색을 위해 마지막 검색 위치 업데이트

    def scroll_to_first_search_result(self, search_query):
        start = self.log_display.search(search_query, '1.0', tk.END)
        if start:
            self.log_display.see(start)

def main():
    root = tk.Tk()
    app = LogFileViewer(root)
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    main()