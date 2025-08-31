import cv2
import os
import sys

def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)

    cap.release()

if __name__ == "__main__":
    video_path = r"D:\Desktop\final_yr_project\drowsiness.mp4"
    
    output_folder = r"D:\Desktop\final_yr_project\drowsiness frames"

    extract_frames(video_path, output_folder)