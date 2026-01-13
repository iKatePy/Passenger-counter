import os
import csv
import yaml
from pathlib import Path
from tqdm import tqdm
from .utils import parse_label_file
from .counter import BusCounter
from ultralytics import YOLO


def run_evaluation(config_path="config.yaml"):
    # Загрузка конфигурации
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)

    label_file = cfg['label_file']
    video_dir = cfg['video_dir']
    output_csv = cfg['output_csv']

    # Парсинг разметки
    labels = parse_label_file(label_file)  # [(name, gt_in, gt_out, cat), ...]
    total_videos = len(labels)
    print(f"Найдено {total_videos} видео для обработки.")

    # Загрузка модели
    model = YOLO(cfg['model_path'])

    # Подготовка результатов
    results = []

    # Обработка с прогресс-баром
    for depth_name, gt_in, gt_out, cat in tqdm(labels, desc="Обработка видео", unit="видео"):
        color_name = depth_name.replace("FrontDepth.avi", "FrontColor.avi")
        video_path = os.path.join(video_dir, color_name)

        if not Path(video_path).exists():
            tqdm.write(f"Пропущено: {color_name} не найден")
            continue

        try:
            counter = BusCounter(line_y=cfg['line_y'], buffer=cfg['buffer'])
            pred_in, pred_out = counter.process_video(
                video_path,
                model,
                conf=cfg['conf'],
                iou=cfg['iou'],
                tracker=cfg['tracker'],
                max_frames=cfg['max_frames']
            )

            # Абсолютные ошибки
            err_in = abs(pred_in - gt_in)
            err_out = abs(pred_out - gt_out)

            # Процентные ошибки 
            if gt_in == 0:
                err_in_pct = 0.0 if pred_in == 0 else 100.0
            else:
                err_in_pct = (err_in / gt_in * 100)

            if gt_out == 0:
                err_out_pct = 0.0 if pred_out == 0 else 100.0
            else:
                err_out_pct = (err_out / gt_out * 100)

            results.append({
                "video": color_name,
                "gt_in": gt_in,
                "pred_in": pred_in,
                "err_in": err_in,
                "err_in_pct": err_in_pct,
                "gt_out": gt_out,
                "pred_out": pred_out,
                "err_out": err_out,
                "err_out_pct": err_out_pct,
                "category": cat
            })

            in_str = f"{err_in_pct:.1f}%"
            out_str = f"{err_out_pct:.1f}%"
            tqdm.write(f"{color_name}: IN={pred_in}/{gt_in} ({in_str}), OUT={pred_out}/{gt_out} ({out_str})")

        except Exception as e:
            tqdm.write(f"Ошибка при обработке {color_name}: {e}")
            results.append({
                "video": color_name,
                "gt_in": gt_in,
                "pred_in": -1,
                "err_in": -1,
                "err_in_pct": None,
                "gt_out": gt_out,
                "pred_out": -1,
                "err_out": -1,
                "err_out_pct": None,
                "category": cat
            })

    # Сохранение в CSV
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "video", "gt_in", "pred_in", "err_in", "err_in_pct",
            "gt_out", "pred_out", "err_out", "err_out_pct", "category"
        ])
        writer.writeheader()
        writer.writerows(results)

    # Расчёт итоговых метрик
    valid_in = [r for r in results if r["err_in_pct"] is not None]
    valid_out = [r for r in results if r["err_out_pct"] is not None]

    # Средняя процентная ошибка по входу
    if valid_in:
        avg_err_in_pct = sum(r["err_in_pct"] for r in valid_in) / len(valid_in)
        accuracy_in = 100.0 - avg_err_in_pct
    else:
        avg_err_in_pct = 0.0
        accuracy_in = 100.0

    # Средняя процентная ошибка по выходу
    if valid_out:
        avg_err_out_pct = sum(r["err_out_pct"] for r in valid_out) / len(valid_out)
        accuracy_out = 100.0 - avg_err_out_pct
    else:
        avg_err_out_pct = 0.0
        accuracy_out = 100.0

    # Общая точность: среднее по двум направлениям
    total_accuracy = (accuracy_in + accuracy_out) / 2.0

    #Вывод итоговых метрик 
    print("Итоговые метрики точности:")
    print(f"   % in error = {avg_err_in_pct:.2f}%  точность входа = {accuracy_in:.2f}%")
    print(f"   % out error = {avg_err_out_pct:.2f}% точность выхода = {accuracy_out:.2f}%")
    print(f"   Общая точность = {total_accuracy:.2f}%")
    
    return results
