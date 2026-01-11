import os
import re
import json
from PIL import Image

def natural_sort_key(s):
    """Hàm hỗ trợ sắp xếp số tự nhiên (1, 2, 10) thay vì alphabel (1, 10, 2)"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

def to_snake_case(filename):
    """Chuyển tên file sang snake_case (bỏ đuôi mở rộng)"""
    name, _ = os.path.splitext(filename)
    name = name.lower()
    # Thay khoảng trắng, gạch ngang thành gạch dưới
    name = re.sub(r'[\s\-]+', '_', name)
    # Chỉ giữ lại a-z, 0-9 và gạch dưới
    name = re.sub(r'[^a-z0-9_]', '', name)
    return name.strip('_')

def process_fish_folder():
    target_dir = 'fish'
    mapping_file = 'fish_mapping.json'

    if not os.path.exists(target_dir):
        print(f"⚠️  Không tìm thấy thư mục: {target_dir}")
        return

    # Lấy danh sách PNG
    files = [f for f in os.listdir(target_dir) if f.lower().endswith('.png')]
    # Sắp xếp để ID ổn định (A->Z)
    files.sort(key=natural_sort_key)

    if not files:
        print(f"⚠️  Folder '{target_dir}' không có file PNG nào để xử lý.")
        return

    print(f"\n🐟 Đang xử lý: FISH ({len(files)} files)...")
    
    mapping_data = {}
    
    # Bắt đầu vòng lặp, count đóng vai trò là 'numid'
    for count, old_filename in enumerate(files, start=1):
        old_path = os.path.join(target_dir, old_filename)
        
        # 1. Tạo code-name
        code_name = to_snake_case(old_filename)
        
        # 2. Tạo tên mới theo cú pháp: numid_[code-name].webp
        # numid để 2 số (01, 02...) cho đẹp và dễ sort
        new_filename = f"{count:02d}_{code_name}.webp"
        new_path = os.path.join(target_dir, new_filename)
        
        try:
            # Convert WebP
            with Image.open(old_path) as img:
                img.save(new_path, 'WEBP', lossless=True)
            
            # Lưu mapping
            mapping_data[old_filename] = {
                "id": count,
                "code_name": code_name,
                "new_file": new_filename
            }
            
            # Xóa file cũ
            os.remove(old_path)
            print(f"  ✅ [{count:02d}] {old_filename} -> {new_filename}")
            
        except Exception as e:
            print(f"  ❌ Lỗi file {old_filename}: {e}")

    # Xuất file JSON mapping để tiện tra cứu sau này
    if mapping_data:
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping_data, f, indent=4, ensure_ascii=False)
        print(f"📝 Đã lưu file map ID tại: {mapping_file}")

def process_arrow_folder(base_path, direction_name):
    folder_path = os.path.join(base_path, direction_name)
    
    if not os.path.exists(folder_path):
        return # Bỏ qua im lặng nếu không thấy folder con

    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
    files.sort(key=natural_sort_key)
    
    if not files:
        return

    print(f"\n📂 Đang xử lý Arrows: {direction_name.upper()} ({len(files)} files)...")

    count = 1
    for old_filename in files:
        old_path = os.path.join(folder_path, old_filename)
        new_filename = f"arrow_{direction_name}_{count:02d}.webp"
        new_path = os.path.join(folder_path, new_filename)
        
        try:
            with Image.open(old_path) as img:
                img.save(new_path, 'WEBP', lossless=True)
            os.remove(old_path)
            print(f"  ✅ {old_filename} -> {new_filename}")
            count += 1
        except Exception as e:
            print(f"  ❌ Lỗi {old_filename}: {e}")

def main():
    print("🚀 Bắt đầu tối ưu hóa Assets...")
    
    # 1. Xử lý cá (Fish)
    process_fish_folder()

    # 2. Xử lý mũi tên (Arrows)
    ARROW_DIR = 'arrows'
    DIRECTIONS = ['up', 'down', 'left', 'right']
    
    if os.path.exists(ARROW_DIR):
        for direction in DIRECTIONS:
            process_arrow_folder(ARROW_DIR, direction)
    else:
        print(f"⚠️  Không tìm thấy folder '{ARROW_DIR}', bỏ qua xử lý arrows.")

    print("\n✨ HOÀN TẤT! Đẩy lên Git được rồi đấy Trương Khuynh Hàn.")

if __name__ == "__main__":
    main()