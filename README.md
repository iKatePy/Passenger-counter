# Passenger Counter

Проект для подсчета пассажиров в общественном транспорте

Автоматическая система на основе YOLOv11 и трекинга BoT-SORT для подсчёта числа людей, входящих и выходящих через дверь автобуса. 
Разработана для анализа видео с фиксированной камерой над дверью.
Для тестирования работы применялся датасет https://github.com/shijieS/people-counting-dataset

## Возможности

- Детекция и трекинг людей в реальном времени
- Подсчёт входящих/выходящих на основе направления движения
- Поддержка видео с разными условиями: нормальное освещение, толпа, плохая видимость
- Гибкая настройка зоны подсчёта и порогов
- Автоматическая оценка точности по ground truth

## Структура проекта
```markdown
```text

├── data/
│   ├── videos/                 # Видеофайлы (*.avi)
│   └── label.txt               # Имя файла и информация о кол-ве входов и выходов (задается пользователем для тестовых видео)
├── src/
│   ├── counter.py              # Логика подсчёта и трекинга
│   ├── utils.py                # Вспомогательные функции 
│   └── evaluate.py             # Основной скрипт оценки
├── config.yaml                 # Параметры модели и подсчёта
├── requirements.txt            # Зависимости
└── Launch.ipynb                # Jupyter Notebook для запуска
```
## Установка и запуск

pip install -r requirements.txt
Положите все .avi видео в data/videos/
Убедитесь, что label.txt находится в data/
Запуск файла Launch.ipynb в среде jupyter notebook

## Требования 
```text
numpy==2.2.6
opencv-python==4.12.0.88
PyYAML==6.0.3
torch==2.9.1
torchvision==0.24.1
tqdm==4.67.1
ultralytics==8.3.251
*Для работы с GPU требуется CUDA-совместимая видеокарта и установленные драйверы NVIDIA. 
```
## Примеры скринов видео из датасета 

В датасете присутствовали видео с одиночными пассажирами (uncrowd) толпой (crowd до 50 человек), с плохим освещением, с шумом (noisy)
<img width="668" height="545" alt="image" src="https://github.com/user-attachments/assets/57fe08d8-7132-4448-867e-8a470e2b4a6d" />

<img width="405" height="293" alt="image" src="https://github.com/user-attachments/assets/38d4244f-c798-4cc4-8b18-f4a1f699ff87" />

<img width="406" height="291" alt="image" src="https://github.com/user-attachments/assets/3ecf079a-3022-4738-87c3-7337720f6d28" />

<img width="476" height="402" alt="image" src="https://github.com/user-attachments/assets/f17db094-e6f8-458f-bf1d-c4f5657457b8" />
<img width="408" height="284" alt="image" src="https://github.com/user-attachments/assets/f3aca9de-bcd3-46f4-bc07-434bddb36107" />
