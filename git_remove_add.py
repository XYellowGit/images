#!/usr/bin/env python3
"""
Script để xóa/thêm thư mục và tự động commit + push lên GitHub
"""

import os
import sys
import argparse
import subprocess
import shutil
from datetime import datetime


def run_command(command, cwd=None):
    """Thực thi lệnh shell và trả về kết quả"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def remove_folder(folder_name):
    """Xóa thư mục - tương thích với cả Windows và Linux"""
    if os.path.exists(folder_name):
        try:
            shutil.rmtree(folder_name)
            print(f"✓ Đã xóa thư mục: {folder_name}")
            return True
        except Exception as e:
            print(f"✗ Lỗi khi xóa thư mục {folder_name}: {e}")
            return False
    else:
        print(f"⚠ Thư mục không tồn tại: {folder_name}")
        return False


def add_folder(folder_name):
    """Tạo thư mục (nếu chưa tồn tại)"""
    if not os.path.exists(folder_name):
        try:
            os.makedirs(folder_name, exist_ok=True)
            # Tạo file .gitkeep để git có thể track thư mục rỗng
            gitkeep_path = os.path.join(folder_name, '.gitkeep')
            with open(gitkeep_path, 'w') as f:
                f.write('')
            print(f"✓ Đã tạo thư mục: {folder_name}")
            return True
        except Exception as e:
            print(f"✗ Lỗi khi tạo thư mục {folder_name}: {e}")
            return False
    else:
        print(f"Thư mục đã tồn tại: {folder_name}")
        return True


def git_commit_and_push(folder_name, mode):
    current_date = datetime.now().strftime("%Y-%m-%d")
    action = "remove" if mode == "remove" else "add"
    commit_message = f"{current_date}: {action} {folder_name}"

    print(f"\n→ Bắt đầu commit cho: {folder_name}")

    # Git add đúng theo mode
    if mode == "remove":
        success, output = run_command('git add -u')
    else:
        success, output = run_command(f'git add "{folder_name}"')

    if not success:
        print(f"✗ Lỗi git add: {output}")
        return False

    # Git commit
    success, output = run_command(f'git commit -m "{commit_message}"')
    if not success:
        if "nothing to commit" in output:
            print(f"⚠ Không có thay đổi để commit cho {folder_name}")
            return False
        else:
            print(f"✗ Lỗi git commit: {output}")
            return False

    print(f"✓ Đã commit: {commit_message}")
    
    # Git push
    success, output = run_command('git push origin main')
    if not success:
        print(f"✗ Lỗi git push: {output}")
        return False
    
    print(f"✓ Đã push lên GitHub")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Xóa/thêm thư mục và tự động commit + push lên GitHub'
    )
    parser.add_argument(
        '--mode',
        required=True,
        choices=['remove', 'add'],
        help='Chế độ: remove (xóa) hoặc add (thêm) thư mục'
    )
    
    args = parser.parse_args()
    
    # Mảng chứa tên các thư mục cần xóa/thêm
    folders = [
        'images/55',
        'images/56',
        'images/57',
        'images/58',
        'images/59',
        'images/60',
        'images/61',
        'images/62',
        'images/63',
        'images/64',
        'images/65',
        'images/66',
        'images/67',
        'images/68',
        'images/69',
        'images/70',
        'images/71',
        'images/72',
        'images/73',
        'images/74',
        'images/75',
        'images/76',
        'images/77',
        'images/78',
        'images/79',
        # Thêm các thư mục khác vào đây
    ]
    
    print(f"=== Chế độ: {args.mode.upper()} ===")
    print(f"Số lượng thư mục: {len(folders)}\n")
    
    # Kiểm tra xem có phải Git repository không
    if not os.path.exists('.git'):
        print("✗ Lỗi: Thư mục hiện tại không phải là Git repository")
        sys.exit(1)
    
    success_count = 0
    failed_count = 0
    
    # Xử lý từng thư mục một
    for i, folder in enumerate(folders, 1):
        print(f"\n[{i}/{len(folders)}] Xử lý thư mục: {folder}")
        print("-" * 50)
        
        # Thực hiện xóa hoặc thêm thư mục
        if args.mode == 'remove':
            operation_success = remove_folder(folder)
        else:  # add
            operation_success = add_folder(folder)
        
        if not operation_success:
            failed_count += 1
            continue
        
        # Commit và push
        if git_commit_and_push(folder, args.mode):
            success_count += 1
            print(f"✓ Hoàn thành xử lý: {folder}")
        else:
            failed_count += 1
            print(f"✗ Thất bại khi xử lý: {folder}")
    
    # Tổng kết
    print("\n" + "=" * 50)
    print("TỔNG KẾT:")
    print(f"  ✓ Thành công: {success_count}/{len(folders)}")
    print(f"  ✗ Thất bại: {failed_count}/{len(folders)}")
    print("=" * 50)
    
    if failed_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()