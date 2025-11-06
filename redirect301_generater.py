import tkinter as tk
from tkinter import ttk, messagebox

class RedirectGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("批量301重定向生成器")
        self.root.geometry("800x600")
        self.center_window()
    
    def center_window(self):
        # 更新窗口以获取准确尺寸
        self.root.update_idletasks()
        
        # 获取屏幕宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 获取窗口宽度和高度
        size = tuple(int(_) for _ in self.root.geometry().split('+')[0].split('x'))
        window_width = size[0]
        window_height = size[1]
        
        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # 设置窗口位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nesw")
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
    
        
        # 创建左右两个文本框的框架
        text_frames = ttk.Frame(main_frame)
        text_frames.grid(row=1, column=0, columnspan=2, sticky="nesw")
        text_frames.columnconfigure(0, weight=1)
        text_frames.columnconfigure(1, weight=1)
        text_frames.rowconfigure(0, weight=1)
        
        # 左侧文本框 - 原网址
        left_frame = ttk.LabelFrame(text_frames, text="原网址 (每行一个)", padding="5")
        left_frame.grid(row=0, column=0, sticky="nesw", padx=(0, 5))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        self.source_text = tk.Text(left_frame, wrap=tk.WORD)
        source_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.source_text.yview)
        self.source_text.configure(yscrollcommand=source_scrollbar.set)
        self.source_text.grid(row=0, column=0, sticky="nesw")
        source_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 右侧文本框 - 目标网址
        right_frame = ttk.LabelFrame(text_frames, text="目标网址 (每行一个)", padding="5")
        right_frame.grid(row=0, column=1, sticky="nesw", padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        self.target_text = tk.Text(right_frame, wrap=tk.WORD)
        target_scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.target_text.yview)
        self.target_text.configure(yscrollcommand=target_scrollbar.set)
        self.target_text.grid(row=0, column=0, sticky="nesw")
        target_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # 生成按钮
        generate_button = ttk.Button(button_frame, text="生成301重定向规则", command=self.generate_redirects)
        generate_button.pack()
        
        # 清空按钮
        clear_button = ttk.Button(button_frame, text="清空所有内容", command=self.clear_all)
        clear_button.pack(pady=(5, 0))
        
        # 结果文本框框架
        result_frame = ttk.LabelFrame(main_frame, text="生成的301重定向规则", padding="5")
        result_frame.grid(row=3, column=0, columnspan=2, sticky="nesw", pady=(10, 0))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=2)
        
        # 结果文本框
        self.result_text = tk.Text(result_frame, wrap=tk.WORD)
        result_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        self.result_text.grid(row=0, column=0, sticky="nesw")
        result_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 复制按钮
        copy_button = ttk.Button(main_frame, text="复制结果到剪贴板", command=self.copy_to_clipboard)
        copy_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        # 版权信息
        copyright_label = ttk.Label(main_frame, text="版权所有：速光网络软件开发 suguang.cc 抖音号：dubaishun12", font=("Arial", 10))
        copyright_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
    
    def generate_redirects(self):
        # 获取原网址和目标网址
        source_urls = self.source_text.get("1.0", tk.END).strip().split('\n')
        target_urls = self.target_text.get("1.0", tk.END).strip().split('\n')
        
        # 过滤空行
        source_urls = [url.strip() for url in source_urls if url.strip()]
        target_urls = [url.strip() for url in target_urls if url.strip()]
        
        # 检查网址数量是否匹配
        if len(source_urls) != len(target_urls):
            messagebox.showwarning("警告", f"原网址数量({len(source_urls)})与目标网址数量({len(target_urls)})不匹配！")
            return
        
        if len(source_urls) == 0:
            messagebox.showwarning("警告", "请输入至少一个网址对！")
            return
        
        # 生成301重定向规则
        result = ""
        for i, (source, target) in enumerate(zip(source_urls, target_urls)):
            # 提取路径部分
            source_path = self.extract_path(source)
            result += f"location = {source_path} {{\n"
            result += f"    return 301 {target};\n"
            result += "}\n\n"
        
        # 显示结果
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", result)
    
    def extract_path(self, url):
        # 提取URL路径部分
        if '//' in url:
            path_start = url.find('/', url.find('//') + 2)
            if path_start != -1:
                return url[path_start:]
        # 如果没有协议部分，直接返回
        if url.startswith('/'):
            return url
        return '/' + url
    
    def clear_all(self):
        # 清空所有文本框
        self.source_text.delete("1.0", tk.END)
        self.target_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
    
    def copy_to_clipboard(self):
        # 复制结果到剪贴板
        result = self.result_text.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("成功", "结果已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "没有内容可复制！")

def main():
    root = tk.Tk()
    app = RedirectGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()