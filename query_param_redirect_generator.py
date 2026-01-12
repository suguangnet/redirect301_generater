#!/usr/bin/env python3
"""
带查询参数的301重定向规则生成器
用于生成 location if 格式的Nginx重定向规则
例如：
location = /new_info.aspx {
    if ($args = 'newsid=12262&AboutCateId=16') {
        return 301 http://www.bjng.gov.cn/article_5157.html;
    }
}
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import urllib.parse


class QueryParamRedirectGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("带查询参数的301重定向规则生成器")
        self.root.geometry("900x700")
        self.center_window()
        
        self.create_widgets()
    
    def center_window(self):
        """居中窗口"""
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
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 标题

        
        # 说明标签
        desc_label = ttk.Label(main_frame, text="输入源URL（包含查询参数）和目标URL，生成location if格式的重定向规则", 
                              foreground="gray")
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # 创建左右两个文本框的框架
        text_frames = ttk.Frame(main_frame)
        text_frames.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        text_frames.columnconfigure(0, weight=1)
        text_frames.columnconfigure(1, weight=1)
        text_frames.rowconfigure(0, weight=1)
        
        # 左侧文本框 - 源URL
        left_frame = ttk.LabelFrame(text_frames, text="源URL (包含查询参数，每行一个)", padding="5")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        self.source_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD)
        self.source_text.grid(row=0, column=0, sticky="nsew")
        
        # 右侧文本框 - 目标URL
        right_frame = ttk.LabelFrame(text_frames, text="目标URL (每行一个)", padding="5")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        self.target_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD)
        self.target_text.grid(row=0, column=0, sticky="nsew")
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # 生成按钮
        generate_button = ttk.Button(button_frame, text="生成301重定向规则", command=self.generate_redirects)
        generate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 清空按钮
        clear_button = ttk.Button(button_frame, text="清空所有内容", command=self.clear_all)
        clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 复制按钮
        copy_button = ttk.Button(button_frame, text="复制结果到剪贴板", command=self.copy_to_clipboard)
        copy_button.pack(side=tk.LEFT)
        
        # 结果文本框框架
        result_frame = ttk.LabelFrame(main_frame, text="生成的301重定向规则", padding="5")
        result_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.NONE, width=80, height=15)
        self.result_text.grid(row=0, column=0, sticky="nsew")
        
        # 版权信息
        copyright_label = ttk.Label(main_frame, text="版权所有：速光网络软件开发 suguang.cc 抖音号：dubaishun12", 
                                   font=("Arial", 10))
        copyright_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
    
    def generate_redirects(self):
        """生成重定向规则"""
        # 获取源URL和目标URL
        source_urls = self.source_text.get("1.0", tk.END).strip().split('\n')
        target_urls = self.target_text.get("1.0", tk.END).strip().split('\n')
        
        # 过滤空行
        source_urls = [url.strip() for url in source_urls if url.strip()]
        target_urls = [url.strip() for url in target_urls if url.strip()]
        
        # 检查URL数量是否匹配
        if len(source_urls) != len(target_urls):
            messagebox.showwarning("警告", f"源URL数量({len(source_urls)})与目标URL数量({len(target_urls)})不匹配！")
            return
        
        if len(source_urls) == 0:
            messagebox.showwarning("警告", "请输入至少一个URL对！")
            return
        
        # 按路径分组URL
        path_groups = {}
        for source, target in zip(source_urls, target_urls):
            try:
                parsed_url = urllib.parse.urlparse(source)
                path = parsed_url.path
                query = parsed_url.query
                
                if not query:
                    # 如果没有查询参数，单独处理
                    if 'no_query' not in path_groups:
                        path_groups['no_query'] = []
                    path_groups['no_query'].append((path, target))
                else:
                    # 按路径分组有查询参数的URL
                    if path not in path_groups:
                        path_groups[path] = []
                    path_groups[path].append((query, target))
            except Exception as e:
                messagebox.showerror("错误", f"解析URL时出错: {str(e)}\nURL: {source}")
                return
        
        # 生成重定向规则
        result = ""
        
        # 处理没有查询参数的URL
        if 'no_query' in path_groups:
            for path, target in path_groups['no_query']:
                result += f"location = {path} {{\n"
                result += f"    return 301 {target};\n"
                result += "}\n\n"
        
        # 处理有查询参数的URL，按路径分组
        for path, items in path_groups.items():
            if path != 'no_query':
                result += f"location = {path} {{\n"
                for query, target in items:
                    result += f"    if ($args = '{query}') {{\n"
                    result += f"        return 301 {target};\n"
                    result += "    }\n"
                result += "}\n\n"
        
        # 显示结果
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", result)
        messagebox.showinfo("成功", f"成功生成了 {len(source_urls)} 条重定向规则！")
    
    def clear_all(self):
        """清空所有文本框"""
        self.source_text.delete("1.0", tk.END)
        self.target_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
    
    def copy_to_clipboard(self):
        """复制结果到剪贴板"""
        result = self.result_text.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("成功", "结果已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "没有内容可复制！")


def main():
    root = tk.Tk()
    app = QueryParamRedirectGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()