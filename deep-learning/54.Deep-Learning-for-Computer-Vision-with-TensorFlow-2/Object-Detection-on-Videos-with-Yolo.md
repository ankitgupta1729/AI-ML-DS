# Object Detection on Videos with YOLO (darkflow, from the terminal)

The course runs this lesson from an Anaconda prompt on Windows with a CUDA GPU:

```bat
python flow --model cfg/yolo.cfg --load bin/yolo.weights --demo Miami.mp4 --saveVideo --gpu 0.8
```

The same command works here. This note records what had to be set up so that it
does, and how the videos in this folder were processed.

## Setup (one-time, already done)

1. **Cython extensions.** darkflow's box-finding and NMS code is Cython and has
   to be compiled for this interpreter:

   ```bash
   cd darkflow && ../.venv/bin/python setup.py build_ext --inplace
   ```

2. **TF2 / NumPy 2 patches.** darkflow targets TensorFlow 1.x. The vendored copy
   in `darkflow/` already carries the three fixes described at the top of
   [17.Object-Detection-on-Images-with-Yolo.ipynb](17.Object-Detection-on-Images-with-Yolo.ipynb)
   (`tensorflow.compat.v1`, a `slim_compat` shim, and the `.weights` memmap
   reader).

3. **Weights in the place the course expects.** The course drops `yolo.weights`
   into `darkflow/bin/`. Here the file ships in `resources/12.4 yolo/`, so
   `bin/` holds a symlink to it rather than a second 200 MB copy:

   ```bash
   mkdir -p darkflow/bin
   ln -sf "../../resources/12.4 yolo/yolo.weights" darkflow/bin/yolo.weights
   ```

   `darkflow/cfg/yolo.cfg` is byte-identical to `resources/12.4 yolo/yolo.cfg`
   (the two differ only in line endings), so the repo's own cfg is fine.

4. **An output path.** Upstream darkflow hard-codes its output to `./video.avi`
   with the XVID codec, which QuickTime will not play and which every run
   overwrites. `darkflow/net/help.py` and `darkflow/defaults.py` now take a
   `--saveVideoPath`; the file extension picks the codec, so `.mp4` gets `mp4v`.
   Omitting the flag keeps the original `video.avi` behaviour.

## `--gpu 0.8` on Apple Silicon

It works. darkflow's TF1 graph runs on the Metal GPU through `tensorflow-metal`,
and the `--gpu 0.8` fraction from the video (reserve 80% of memory, leave the
rest so nothing else is starved) is honoured — roughly **19 FPS** on 1280x720
YOLOv2 at 608x608. Note this is the opposite of notebook 17, which pins
`'gpu': 0.0`; that was a workaround, and the GPU path is the faster choice here.

## Running it

Always run from inside `darkflow/`, because darkflow resolves `--config`
(where `coco.names` lives) relative to the current working directory.

```bash
cd darkflow

../.venv/bin/python flow \
  --model cfg/yolo.cfg \
  --load bin/yolo.weights \
  --demo ../cars.mp4 \
  --saveVideo --saveVideoPath ../videos_out/cars-yolov2.mp4 \
  --threshold 0.4 \
  --gpu 0.8
```

All seven videos in the folder at once:

```bash
cd darkflow
for v in cars bikes people motorbikes ppe-1 ppe-2 ppe-3; do
  ../.venv/bin/python flow \
    --model cfg/yolo.cfg --load bin/yolo.weights \
    --demo "../$v.mp4" \
    --saveVideo --saveVideoPath "../videos_out/$v-yolov2.mp4" \
    --threshold 0.4 --gpu 0.8
done
```

### Webcam

The second half of the lesson. `--demo camera` opens a preview window; press
`[ESC]` to stop. macOS will ask for camera permission for the terminal app the
first time. Untested here — the file path above is what was actually run.

```bash
cd darkflow
../.venv/bin/python flow --model cfg/yolo.cfg --load bin/yolo.weights \
  --demo camera --gpu 0.8
```

The course does the same thing from a standalone script rather than through
`flow`, which is what [yolov2_od_webcam.py](yolov2_od_webcam.py) is. It builds
`TFNet` directly, so it runs from this folder and takes no `cd`:

```bash
.venv/bin/python yolov2_od_webcam.py
```

`--camera 0` (the Mac's built-in camera) is the default; the video uses index 1
for an external one. `--threshold`, `--gpu`, `--width`/`--height` and an optional
`--save out.mp4` are the other flags. Quit with `[q]` or `[ESC]`.

macOS gates the camera on the *terminal application*, not on Python: the first
run raises a permission prompt, and if it was ever declined the script sees an
unopenable device. System Settings > Privacy & Security > Camera.

## Flags worth knowing

| Flag | Effect |
| --- | --- |
| `--demo <file>` | Video to run on; `camera` for the webcam. |
| `--saveVideo` | Record the annotated result instead of only displaying it. |
| `--saveVideoPath <path>` | Local addition — where to write it; extension picks the codec. |
| `--threshold 0.4` | Minimum confidence. The default is very low and produces duplicate and spurious boxes (a car labelled `boat`). 0.4 is a good working value. |
| `--gpu 0.8` | Fraction of GPU memory to reserve. `0.0` forces CPU. |
| `--queue N` | Batch N frames per session run. Higher is faster but delays the preview window. |

## Results

`videos_out/` now holds one annotated mp4 per source video:

| Output | Frames | FPS |
| --- | --- | --- |
| `cars-yolov2.mp4` | 367 | 30 |
| `bikes-yolov2.mp4` | 457 | 50 |
| `people-yolov2.mp4` | 631 | 30 |
| `motorbikes-yolov2.mp4` | 685 | 25 |
| `ppe-1-yolov2.mp4` | 342 | 30 |
| `ppe-2-yolov2.mp4` | 205 | 25 |
| `ppe-3-yolov2.mp4` | 348 | 30 |

Each is one frame shorter than its source: darkflow reads the first frame before
the loop to learn the frame size and never writes it back out. That is upstream
behaviour, left alone.

`videos_out/*.mp4` is covered by the repo `.gitignore`, so the outputs stay local.
