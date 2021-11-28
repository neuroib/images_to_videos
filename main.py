from tkinter.filedialog import askdirectory
import progressbar
import sys, os
import cv2

print('select directory for input frames')
frames_dir = askdirectory()
outbasename = os.path.basename(frames_dir)
FPS = float(input('enter FPS for video: '))


print('select directory for output video')
outdir = askdirectory()

frames = {}
writers = {}
fourcc = cv2.VideoWriter_fourcc(*"XVID")
for view in ['top', 'side']:
    frames[view] = [f for f in sorted(os.listdir(frames_dir), key=lambda f: int(f.split('-')[-1][:-4])) if view in f]
    h, w, _ = cv2.imread(os.path.join(frames_dir, frames[view][0])).shape
    writers[view] = cv2.VideoWriter(os.path.join(outdir, '{}_{}.avi'.format(outbasename, view)), fourcc, FPS, (w, h))

    frames_saved = 0
    with progressbar.ProgressBar(max_value=len(frames[view])) as pbar:
        for frame in frames[view]:
            writers[view].write(cv2.imread(os.path.join(frames_dir, frame)))
            frames_saved += 1
            pbar.update(frames_saved)
    writers[view].release