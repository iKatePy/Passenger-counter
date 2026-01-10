import os
from pathlib import Path

def parse_label_file(label_path):
    """
    Читает label.txt и возвращает список кортежей:
    [(video_name, gt_in, gt_out, category), ...]
    """
    with open(label_path, 'r') as f:
        lines = f.readlines()
    
    # Пропускаем первые 4 строки (параметры камера)
    video_data = []
    for line in lines[4:]:
        parts = line.strip().split()
        if len(parts) >= 3:
            video_name = parts[0]
            gt_in = int(parts[1])
            gt_out = int(parts[2])
            category = int(parts[3]) if len(parts) > 3 else -1
            video_data.append((video_name, gt_in, gt_out, category))
    return video_data

