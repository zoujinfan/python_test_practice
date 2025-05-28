# book_manager.py

# 导入模块
import os
import datetime

# -------------------------------
# 装饰器：用于记录函数调用日志
# 装饰器作用：在函数执行前/后增加操作（记录日志，打印时间，做权限检查）
def log_action(func):
    def wrapper(*args, **kwargs): #任意位置 任意关键字参数
        print(f"[LOG] 正在执行：{func.__name__} at {datetime.datetime.now()}")
        return func(*args, **kwargs)
    return wrapper

# -------------------------------
# 类定义：图书和图书馆

# __init__（）构造函数，初始化
class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author
# _repr__（）特殊方法，字符串的“官方”表示
    def __repr__(self):
        return f"{self.title} - {self.author}"

class Library:
    def __init__(self):
        # 列表用于存储图书对象
        self.books = []

    @log_action
    def add_book(self, book: Book):
        self.books.append(book)

    @log_action
    def remove_book(self, title: str):
        # 条件语句 + 异常处理
        for b in self.books:
            if b.title == title:
                self.books.remove(b)
                print(f"《{title}》已被删除。")
                return
        raise ValueError("找不到该图书。")

    @log_action
    def find_books(self, keyword: str):
        # 列表推导 + 条件语句
        results = [book for book in self.books if keyword.lower() in book.title.lower()]
        return results

    # 把所有书的信息保存到文本文件里，方便读取和备份
    def save_to_file(self, filename="books.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for book in self.books:
                f.write(f"{book.title},{book.author}\n")

    def load_from_file(self, filename="books.txt"):
        if not os.path.exists(filename):
            return
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                title, author = line.strip().split(",")
                self.books.append(Book(title, author))

# -------------------------------
# 函数：用户交互主逻辑

def run_library():
    lib = Library()
    lib.load_from_file()

    while True:
        print("\n📚 图书管理系统")
        print("1. 添加图书")
        print("2. 查找图书")
        print("3. 删除图书")
        print("4. 显示所有图书")
        print("5. 保存并退出")

        choice = input("请输入选项（1-5）：")

        if choice == "1":
            title = input("书名：")
            author = input("作者：")
            lib.add_book(Book(title, author))
        elif choice == "2":
            keyword = input("请输入搜索关键词：")
            results = lib.find_books(keyword)
            print("搜索结果：", results)
        elif choice == "3":
            title = input("请输入要删除的书名：")
            try:
                lib.remove_book(title)
            except ValueError as e:
                print(f"错误：{e}")
        elif choice == "4":
            print("所有图书：", lib.books)
        elif choice == "5":
            lib.save_to_file()
            print("已保存到文件。")
            break
        else:
            print("无效的选项，请重新输入。")

# -------------------------------
# 主程序入口
if __name__ == "__main__":
    run_library()
