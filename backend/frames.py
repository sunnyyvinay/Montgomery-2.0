# split the mp4 of the video that we get into many frames

import cv2
import os

video_path = 'example1.mp4'
output_dir = './animation_assets/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

cap = cv2.VideoCapture(video_path)

frame_count = 0

while True: 
    # loop through each frame of the video
    ret, frame = cap.read()

    if not ret: 
        break

    frame_name = os.path.join(output_dir, f'frame_{frame_count:04d}.png')
    cv2.imwrite(frame_name, frame)

    print(f'saved {frame_name}')

    frame_count += 1

cap.release()

print("all frames extracted successfully")




