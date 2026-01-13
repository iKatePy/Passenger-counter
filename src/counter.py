from collections import defaultdict, deque
import cv2
from ultralytics import YOLO

class BusCounter:
    def __init__(self, line_y=120, buffer=40):
        self.line_y = line_y
        self.buffer = buffer
        self.in_count = 0
        self.out_count = 0
        self.track_history = defaultdict(lambda: deque(maxlen=90))
        self.processed_tracks = set()

    def update_count(self, track_id, prev_positions):
        if len(prev_positions) < self.min_track_length::
            return
        pos_list = list(prev_positions)
        y_vals = [pos[2] for pos in pos_list[-5:]]
        if len(y_vals) < 2:
            return
        avg_change = sum(y_vals[i+1] - y_vals[i] for i in range(len(y_vals)-1)) / (len(y_vals)-1)
        if abs(avg_change) < 1.0:
            return
        y_curr = y_vals[-1]
        if abs(y_curr - self.line_y) > self.buffer:
            return
        if avg_change > 0.5:
            direction = "IN"
        elif avg_change < -0.5:
            direction = "OUT"
        else:
            return
        if track_id not in self.processed_tracks:
            if direction == "IN":
                self.in_count += 1
            else:
                self.out_count += 1
            self.processed_tracks.add(track_id)

    def process_video(self, video_path, model, conf=0.5, iou=0.5, tracker="botsort.yaml", max_frames=500):
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        self.in_count = 0
        self.out_count = 0
        self.track_history.clear()
        self.processed_tracks.clear()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = model.track(
                frame,
                classes=[0],
                conf=conf,
                iou=iou,
                tracker=tracker,
                persist=True,
                verbose=False
            )

            if results[0].boxes is not None and results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                track_ids = results[0].boxes.id.cpu().numpy().astype(int)

                for box, track_id in zip(boxes, track_ids):
                    x1, y1, x2, y2 = box
                    height = y2 - y1
                    if height < 30 or height > 500:  # Исключим маленькие обюекты с ложными срабатываниями
                        continue
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    self.track_history[track_id].append((frame_count, center_x, center_y))
                    if len(self.track_history[track_id]) >= 3:
                        self.update_count(track_id, self.track_history[track_id])

            frame_count += 1
            if frame_count > max_frames:
                break

        cap.release()
        return self.in_count, self.out_count
