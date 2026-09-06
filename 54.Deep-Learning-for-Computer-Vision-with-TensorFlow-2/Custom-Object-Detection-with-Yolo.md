# YOLOv2 Custom Object Detection (train, video, webcam)

The course splits this lesson across several steps on Windows: edit a copy of the
cfg, edit `labels.txt`, train with `flow --train`, then write a separate
`yolov2_custom_object_cam.py` for detection. All of that is folded into one file
here: [yolov2_custom_object.py](yolov2_custom_object.py).

The class is **r2d2**, from the course's 200-image annotated dataset in
`resources/14.1 rd2d2/`.

## The commands

```bash
cd 54.Deep-Learning-for-Computer-Vision-with-TensorFlow-2

# 1. build the custom/ layout (cfg, labels.txt, train/images, train/annotations)
.venv/bin/python yolov2_custom_object.py prepare

# 2. train (~3 s/step, ~3600 steps, so budget around 3 hours)
.venv/bin/python yolov2_custom_object.py train --epochs 300 --gpu 0.8

# 3a. detect in a video, writing videos_out/R2D2-custom.mp4
.venv/bin/python yolov2_custom_object.py video --load -1 --threshold 0.3

# 3b. detect from the webcam ('q' in the window quits)
.venv/bin/python yolov2_custom_object.py cam --load -1 --threshold 0.3
```

`--load -1` means "the most recent checkpoint". Pass a specific step
(`--load 3600`, as the course does) to pin one, or a path to a `.weights` file.

`video` defaults to `code/5-Object_Detection/darknetv3/R2D2.avi`; use `--input`
for any other file and `--output` to choose where it lands. `--max-frames 20` is
handy for checking a fresh checkpoint without processing the whole clip.

**About that default clip.** It is the only R2D2 footage in the module, and it is
*already an output* from an earlier darknet run — blue boxes and green
`r2d2 NN%` labels are burned into the pixels. (`code/5-Object_Detection/Yolov2/
R2D2_yolov2.avi` is byte-for-byte the same file.) Detections from this script are
drawn in red with white text, so on that clip you will see two sets of boxes: the
baked-in blue ones and ours. It still demonstrates the model, but for a clean
result pass `--input` with an unannotated video. The clip is an Oscars segment
featuring both R2D2 and C-3PO, so stretches of it legitimately contain no R2D2 —
low scores there are correct, not a failure.

## What `prepare` builds

```
custom/
  cfg/yolov2.cfg       source architecture (copy of darkflow's yolo.cfg)
  cfg/yolov2-1c.cfg    the custom model: classes=1, last filters=30
  labels.txt           r2d2
  train/images         -> resources/14.1 rd2d2/images        (symlink)
  train/annotations    -> resources/14.1 rd2d2/annotations   (symlink)
  ckpt/                training checkpoints
```

Two details are easy to get wrong and are handled for you:

**The filters formula.** The last convolutional layer needs
`5 x (n_classes + 5)` filters — 30 for one class, against 425 for COCO's 80.
`prepare` asserts that `classes=` and the final `filters=` in the cfg agree with
the number of labels, and stops with a clear message if they don't.

**`cfg/yolov2.cfg` must exist.** This one is not in the course notes. When
`--load` points at a `.weights` file, darkflow looks for a cfg of the *same
basename* in the config directory to learn the layout to read the binary with —
so `yolov2.weights` requires `yolov2.cfg`. Without it darkflow silently falls
back to the 1-class cfg and dies on a byte-count assertion, because the file
holds 425-filter weights. With it, every layer but the last is transferred and
the mismatched final layer is randomly initialised — which is exactly the
transfer learning this lesson wants.

The dataset's XML files actually carry two names, `r2d2` (235 boxes) and `car`
(12 boxes). `labels.txt` lists only `r2d2`, and darkflow drops annotations whose
name isn't listed, so this stays a genuine one-class problem.

## A fourth TF2 patch to darkflow

Notebooks 17 and 18 describe three fixes already applied to the vendored
darkflow. Training needed one more, in
[flow.py](darkflow/darkflow/net/flow.py):

`TFNet.train()` runs outside the `with self.graph.as_default()` block that built
the `tf.train.Saver`. Under TF2, eager execution is therefore live when
`_save_ckpt` fires, so `Saver.save` takes its eager branch and raises
`ValueError: Can only save/restore ResourceVariables when executing eagerly`.
Restoring graph mode around the call fixes it. Training itself was fine — only
the checkpoint write failed, at the first save. Restoring needs no equivalent
fix, since `load_from_ckpt` is called from inside `setup_meta_ops`.

## Notes

- `--gpu 0.8` works on Apple Silicon through `tensorflow-metal`, the same as in
  [18.Object-Detection-on-Videos-with-Yolo.md](18.Object-Detection-on-Videos-with-Yolo.md).
  Use `--gpu 0.0` to force CPU.
- Loss starts around 108 and the course reaches ~0.5 by step 3600.
- Detections are drawn in the course's style: a red box plus `label: NN%`.
- Checkpoints are large. `custom/` holds ~5 checkpoints by default (`--keep`),
  and the dataset is symlinked rather than copied.

## Training on your own objects

1. Annotate images to Pascal VOC XML (labelImg, or the course's tool).
2. Point `SRC_DATASET` in the script at them, or replace the two symlinks under
   `custom/train/`.
3. `prepare --labels cat dog` for the class names you used.
4. Edit `custom/cfg/yolov2-1c.cfg`: set `classes=` to your class count and the
   final `filters=` to `5 x (classes + 5)`. `prepare` will refuse to continue if
   these disagree with your labels.
