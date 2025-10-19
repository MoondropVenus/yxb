#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def view_file_content(filename):
    """查看文件内容"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"文件 {filename} 的内容:")
            print(content)
    except Exception as e:
        print(f"读取文件 {filename} 时出错: {e}")

if __name__ == "__main__":
    view_file_content("online_exam_answers.txt")
    print("\n" + "="*50 + "\n")
    view_file_content("online_exam_content.txt")