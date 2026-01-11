import os
import re
from PIL import Image

def natural_sort_key(s):
    """Hàm hỗ trợ sắp xếp số tự nhiên (1, 2, 10) thay vì alphabel (1, 10, 2)"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def process_folder(base_path, direction_name):
    # Đường dẫn tới folder con (ví dụ: arrows/up)
    folder_path = os.path.join(base_path, direction_name)
    
    if not os.path.exists(folder_path):
        print(f"⚠️ Không tìm thấy thư mục: {folder_path}")
        return

    # Lấy danh sách file PNG
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
    
    # Sắp xếp file theo số trong tên (button_1 -> button_2 -> ... -> button_10)
    files.sort(key=natural_sort_key)
    
    if not files:
        print(f"⚠️ Folder '{direction_name}' trống hoặc không có file PNG.")
        return

    print(f"\n📂 Đang xử lý: {direction_name.upper()} ({len(files)} files)...")

    count = 1
    for old_filename in files:
        # Đường dẫn file cũ
        old_path = os.path.join(folder_path, old_filename)
        
        # Tạo tên mới: arrow_up_01.webp, arrow_up_02.webp...
        new_filename = f"arrow_{direction_name}_{count:02d}.webp"
        new_path = os.path.join(folder_path, new_filename)
        
        try:
            # Mở ảnh và convert sang WebP
            with Image.open(old_path) as img:
                # Lưu file WebP (lossless=True cực quan trọng cho Pixel Art)
                img.save(new_path, 'WEBP', lossless=True)
            
            # Xóa file PNG cũ để dọn rác
            os.remove(old_path)
            
            print(f"  ✅ Đã đổi: {old_filename} -> {new_filename}")
            count += 1
            
        except Exception as e:
            print(f"  ❌ Lỗi file {old_filename}: {e}")

def main():
    # Cấu hình đường dẫn gốc chứa các folder hướng
    # Giả sử cấu trúc là: ./arrows/up, ./arrows/down...
    BASE_DIR = 'arrows' 
    
    # Các hướng cần xử lý (tên folder con)
    DIRECTIONS = ['up', 'down', 'left', 'right']

    print("🚀 Bắt đầu tối ưu hóa Assets...")
    
    if not os.path.exists(BASE_DIR):
         print(f"❌ Lỗi: Không tìm thấy thư mục '{BASE_DIR}' tại vị trí chạy tool.")
         return

    for direction in DIRECTIONS:
        process_folder(BASE_DIR, direction)

    print("\n✨ HOÀN TẤT! Tất cả đã được chuyển sang WebP và đổi tên gọn gàng.")

if __name__ == "__main__":
    main()