import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import os
# 字符映射表
character_maps = {
    'a': [4, 3, 3, 3, 0, 3, 3, 3, 3],# 塔塔
    'b': [4, 3, 0, 3, 0, 0, 3, 0, 0],
    'c': [4, 3, 0, 3, 0, 0, 2, 1, 3],# 草草
    'd': [4, 3, 0, 3, 2, 0, 1, 1, 1],# 梓卿
    'e': [4, 3, 0, 3, 0, 0, 0, 1, 0],
    'f': [4, 3, 0, 3, 0, 0, 0, 0, 1],
    'g': [4, 3, 0, 3, 0, 2, 0, 0, 0],
    'h': [4, 3, 0, 3, 0, 0, 2, 0, 0],
    'i': [4, 3, 0, 3, 0, 0, 0, 2, 0],
    'j': [4, 3, 0, 3, 1, 0, 0, 0, 3],
    'k': [4, 3, 0, 3, 1, 1, 0, 2, 0],
    'l': [4, 3, 0, 3, 0, 3, 0, 1, 0],# kagaminori
    'm': [4, 3, 0, 3, 0, 0, 0, 0, 3],
    'n': [4, 3, 0, 3, 0, 2, 0, 0, 1],
    'o': [4, 3, 2, 3, 0, 2, 0, 3, 0],
    'p': [4, 3, 2, 3, 0, 2, 0, 0, 2],
    'q': [4, 3, 0, 3, 0, 2, 1, 3, 3],
    'r': [4, 3, 0, 3, 2, 2, 2, 1, 3],# 若尘
    's': [4, 3, 1, 3, 1, 1, 1, 1, 1],# UNKNOWNTIMER
    't': [4, 3, 1, 3, 0, 3, 0, 1, 2],# 乔爽<(**)>
    'u': [4, 3, 0, 3, 0, 3, 0, 1, 0],# 16
    'v': [4, 3, 0, 3, 0, 0, 3, 1, 2],
    'w': [4, 3, 0, 3, 0, 0, 0, 2, 2],
    'x': [4, 3, 3, 3, 3, 0, 3, 0, 3],
    'y': [4, 3, 0, 3, 0, 1, 0, 2, 0],# 不画
    'z': [4, 3, 0, 3, 0, 3, 0, 2, 1],
    ',': [4, 3, 1, 3, 0, 1, 0, 3, 0],# whatbug
    '.': [4, 3, 0, 3, 3, 3, 0, 3, 0],# SA
    '?': [4, 3, 0, 3, 0, 0, 0, 2, 0],# 凯
    '!': [4, 3, 1, 3, 0, 0, 2, 0, 1],
    '0': [4, 3, 0, 3, 0, 0, 0, 0, 0],# 断片黑线
    ' ': [4, 3, 3, 3, 0, 0, 3, 0, 0],
    '1': [4, 3, 2, 3, 0, 0, 0, 0, 3],
    '2': [4, 3, 1, 3, 0, 0, 0, 0, 3],
    '3': [4, 3, 0, 3, 2, 0, 0, 0, 3],
    '4': [4, 3, 0, 3, 1, 0, 0, 0, 3],
    '5': [4, 3, 0, 3, 0, 0, 2, 0, 3],
    '6': [4, 3, 0, 3, 0, 0, 1, 0, 3],
    '7': [4, 3, 0, 3, 0, 2, 0, 0, 3],
    '8': [4, 3, 0, 3, 0, 1, 0, 0, 3],
    '9': [4, 3, 0, 3, 0, 0, 0, 2, 3],
}
# 定义字符对应的绘制颜色
color_map = {
    0: (0, 0, 0, 0),    # 空白部分，透明
    1: (0, 0, 0, 255),  # ▄ ，黑色，代表完整方块的下半部分
    2: (0, 0, 0, 255),  # ▌，黑色，代表完整方块的左半部分
    3: (0, 0, 0, 255),  # █ ，黑色方块
    4: (0, 0, 0, 255)   # 空心黑色正方形（□）
}
# 创建图像
def create_image(text, max_chars_per_line):
    lines = [text[i:i + max_chars_per_line] for i in range(0, len(text), max_chars_per_line)]
    scale = 40
    image_width = max_chars_per_line * 9 * scale + (max_chars_per_line - 1) * 3 * scale  # 每个字符后有一个间隔
    image_height = len(lines) * 9 * scale + (len(lines) - 1) * scale  # 每行后有一个间隔
    img = Image.new('RGBA', (image_width, image_height), color=(0, 0, 0, 0))  # 使用透明背景
    draw = ImageDraw.Draw(img)

    for line_index, line in enumerate(lines):
        for index, char in enumerate(line.lower()):
            if char in character_maps:
                char_map = character_maps[char]
                for i in range(9):
                    x_offset = index * (9 * scale + 1 * scale)  # 每个字符后有一个间隔
                    x = x_offset + (i % 3) * 3 * scale
                    y = (i // 3) * 3 * scale + line_index * (9 * scale + scale)  # 每行后有一个间隔
                    
                    color = color_map.get(char_map[i], (0, 0, 0, 0))
                    if char_map[i] == 1:
                        draw.rectangle([x + 0.2, y + 1.7 * scale, x + 2.8 * scale, y + 2.8 * scale], fill=color)  # 下半部分
                    elif char_map[i] == 2:
                        draw.rectangle([x + 0.2, y + 0.2, x + 1.3 * scale, y + 2.8 * scale], fill=color)  # 左半部分
                    elif char_map[i] == 3:
                        draw.rectangle([x + 0.2, y + 0.2, x + 2.8 * scale, y + 2.8 * scale], fill=color)
                    elif char_map[i] == 4:
                        draw.rectangle([x + 0.2, y + 0.2, x + 2.8 * scale, y + 2.8 * scale], outline=(0, 0, 0, 255), width=10)  # 空心正方形
    return img
# GUI界面
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("计时器文字翻译软件")
        self.root.geometry("600x300")
        self.root.configure(bg='#222222')  # 暗色主题

        self.text_input = tk.Entry(self.root, font=("SimHei", 14), width=40)
        self.text_input.pack(pady=10)

        self.max_chars_label = tk.Label(self.root, text="每行字符数", font=("SimHei", 14), bg='#222222', fg='white')
        self.max_chars_label.pack()
        
        self.max_chars_input = tk.Entry(self.root, font=("SimHei", 14), width=5)
        self.max_chars_input.pack(pady=5)

        self.convert_button = tk.Button(self.root, text="生成图片", command=self.convert, font=("SimHei", 14), bg='#008000', fg='white', width=20)
        self.convert_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="选择保存位置", command=self.save_image, font=("SimHei", 14), bg='#800000', fg='white', width=20)
        self.save_button.pack(pady=10)

        self.image = None

    def convert(self):
        text = self.text_input.get()
        if not text:
            messagebox.showwarning("输入错误", "请输入要转换的文本！")
            return

        try:
            max_chars_per_line = int(self.max_chars_input.get())
        except ValueError:
            messagebox.showwarning("输入错误", "请输入有效的每行最大字符数！")
            return

        self.image = create_image(text, max_chars_per_line)
        self.image.show()

    def save_image(self):
        if not self.image:
            messagebox.showwarning("未生成图片", "请先生成图片！")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            self.image.save(save_path)
            messagebox.showinfo("保存成功", f"图片已保存到 {save_path}")
# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()  
