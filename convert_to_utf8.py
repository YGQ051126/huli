#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件编码转换工具
将指定文件夹内的所有文件转换为UTF-8编码
"""

import os
import sys
import chardet
from pathlib import Path


def detect_file_encoding(file_path):
    """
    检测文件编码
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']


def convert_to_utf8(file_path, backup=True):
    """
    将文件转换为UTF-8编码
    """
    try:
        # 检测文件编码
        encoding = detect_file_encoding(file_path)
        if not encoding:
            print(f"无法检测文件编码: {file_path}")
            return False
        
        # 如果已经是UTF-8编码，跳过
        if encoding.lower() in ['utf-8', 'utf8']:
            print(f"文件已经是UTF-8编码，跳过: {file_path}")
            return True
        
        # 读取文件内容
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        
        # 创建备份
        if backup:
            backup_path = f"{file_path}.backup"
            with open(backup_path, 'w', encoding=encoding) as f:
                f.write(content)
        
        # 写入UTF-8编码
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"转换成功: {file_path} ({encoding} -> UTF-8)")
        return True
    
    except Exception as e:
        print(f"转换失败: {file_path}, 错误: {str(e)}")
        return False


def is_text_file(file_path):
    """
    判断是否为文本文件
    """
    text_extensions = [
        '.txt', '.py', '.js', '.html', '.css', '.json', '.xml', '.md', '.yml', '.yaml',
        '.ini', '.cfg', '.conf', '.log', '.sql', '.sh', '.bat', '.cmd', '.ps1',
        '.c', '.cpp', '.h', '.hpp', '.java', '.php', '.rb', '.go', '.rs', '.swift',
        '.ts', '.jsx', '.tsx', '.vue', '.scss', '.less', '.sass', '.coffee',
        '.dockerfile', '.gitignore', '.env', '.env.example', '.env.local',
        '.readme', '.license', '.changelog', '.contributing', '.authors', '.history'
    ]
    
    # 检查扩展名
    ext = Path(file_path).suffix.lower()
    if ext in text_extensions:
        return True
    
    # 检查文件名
    filename = Path(file_path).name.lower()
    if filename in ['makefile', 'dockerfile', 'readme', 'license', 'changelog']:
        return True
    
    # 检查文件内容
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk:  # 包含空字节，可能是二进制文件
                return False
            return True
    except:
        return False


def convert_directory(directory, recursive=True, backup=True):
    """
    转换目录中的所有文件
    """
    directory = Path(directory)
    if not directory.exists():
        print(f"目录不存在: {directory}")
        return
    
    if not directory.is_dir():
        print(f"不是目录: {directory}")
        return
    
    # 获取所有文件
    if recursive:
        files = directory.rglob('*')
    else:
        files = directory.iterdir()
    
    # 过滤出文件
    files = [f for f in files if f.is_file()]
    
    # 过滤出文本文件
    text_files = [f for f in files if is_text_file(f)]
    
    print(f"找到 {len(text_files)} 个文本文件")
    
    success_count = 0
    for file_path in text_files:
        if convert_to_utf8(file_path, backup):
            success_count += 1
    
    print(f"转换完成: {success_count}/{len(text_files)} 个文件成功转换")


def main():
    """
    主函数
    """
    # 直接指定目录为 D:\Tarot\src  
    directory = r"D:\huli\care_platform"
    recursive = True  # 递归处理子目录
    backup = False     # 创建备份文件
    
    print(f"开始转换目录: {directory}")
    print(f"递归处理: {'是' if recursive else '否'}")
    print(f"创建备份: {'是' if backup else '否'}")
    print("-" * 50)
    
    convert_directory(directory, recursive, backup)
    
    print("-" * 50)
    print("转换完成!")
    
    # 等待用户按键退出  input("按任意键退出...")


if __name__ == "__main__":
    main()