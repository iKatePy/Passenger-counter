# Passenger Counter

Проект для подсчета пассажиров в общественном транспорте

Автоматическая система на основе YOLOv11l и трекинга BoT-SORT для подсчёта числа людей, входящих и выходящих через дверь автобуса. 

Разработана для анализа видео с фиксированной камерой над дверью.

Для тестирования работы применялся датасет https://github.com/shijieS/people-counting-dataset

10% от всех протестированных видео (151) содержали сложные условия - плохое освещение (практически нулевая видимость, толпа людей (более 10 человек одновременно), зеркальные отражения

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
1. Создайте окружение: python3 -m venv myenv (где myenv — имя папки с окружением, можно любое)
2. Запустите окружение source myenv/bin/activate
3. Установите зависимости для работы с проектом pip install -r requirements.txt
4. Запустите блокнот jupyter notebook (если не установлен, воспользуйтесь командой pip install notebook)
5. Положите все .avi видео в data/videos/
6. Убедитесь, что label.txt находится в data/ и в нем присутствует маркировка название видео кол-во входящих людей, кол-во выходящих людей, тип видео (если нужно). Пример "FrontDoorCam.mp4 3 4 0"
7. Запуск файла Launch.ipynb в среде jupyter notebook

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
## Лицензия
Данный MVP-проект предназначен исключительно для **исследовательских и образовательных целей**.
### Используемые сторонние компоненты:
- **YOLOv11** от Ultralytics — [AGPL-3.0 License](https://github.com/ultralytics/ultralytics/blob/main/LICENSE)
- **BoT-SORT tracker** — [MIT License](https://github.com/NirAharon/BoT-SORT/blob/main/LICENSE)
- **OpenCV** — [Apache 2.0 License](https://opencv.org/license/)
- **PyTorch** — [BSD-3-Clause License](https://github.com/pytorch/pytorch/blob/main/LICENSE)

## Примеры скринов видео из датасета 

В датасете присутствовали видео с одиночными пассажирами (uncrowd) толпой (crowd до 50 человек), с плохим освещением, с шумом (noisy)
<img width="668" height="545" alt="image" src="https://github.com/user-attachments/assets/57fe08d8-7132-4448-867e-8a470e2b4a6d" />

<img width="405" height="293" alt="image" src="https://github.com/user-attachments/assets/38d4244f-c798-4cc4-8b18-f4a1f699ff87" />

<img width="406" height="291" alt="image" src="https://github.com/user-attachments/assets/3ecf079a-3022-4738-87c3-7337720f6d28" />

<img width="476" height="402" alt="image" src="https://github.com/user-attachments/assets/f17db094-e6f8-458f-bf1d-c4f5657457b8" />
<img width="408" height="284" alt="image" src="https://github.com/user-attachments/assets/f3aca9de-bcd3-46f4-bc07-434bddb36107" />
## Презентация
https://docs.google.com/presentation/d/1OuHqYcCUH6xZkh-90wlfyzrCOvIj1zIN36CGi_pS5WQ/edit?usp=sharing
