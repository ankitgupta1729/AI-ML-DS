# Restoring what was deleted (disk cleanup, 2026-09-06)

A cleanup pass removed ~7 GB of regenerable files from this module: training
checkpoints, downloaded pretrained models, a third-party repo clone, and caches.
Nothing that was deleted is lost for good — this file is the recipe for each.

**Nothing here is needed until you actually run the notebook that uses it.** Run
only the section you need.

All commands assume you are in the module root:

```bash
cd 54.Deep-Learning-for-Computer-Vision-with-TensorFlow-2
```

## Quick reference

| Deleted | Size | Needed by | Section |
| --- | --- | --- | --- |
| `custom/ckpt/` | 3.9 GB | notebook 18, `yolov2_custom_object.py` | [1](#1-yolov2-custom-checkpoints) |
| `models/` | 769 MB | notebooks 15, 16 | [2](#2-models--the-tensorflow-models-repo) |
| `TF2ODAPI/training/faster_rcnn_resnet50_v1_bccd/` | 664 MB | notebook 15 (BCCD) | [3](#3-bccd-training-checkpoints) |
| `TF2ODAPI/pre-trained-models/` | 225 MB | notebook 15 (BCCD) | [4](#4-odapi-pretrained-model) |
| `openimagesv6/` + `~/fiftyone` | 82 MB | notebook 14 | [5](#5-open-images-v6-via-fiftyone) |
| `darkflow/build/` | 3 MB | nothing — see note | [6](#6-darkflow-cython-extensions) |
| `videos_out/*-yolov2.mp4` | 55 MB | nothing — they were outputs | [7](#7-detection-output-videos) |
| various `resources/*.zip` | 1.3 GB | nothing — see [8](#8-the-deleted-resources-archives) | [8](#8-the-deleted-resources-archives) |
| `__pycache__`, `.ipynb_checkpoints` | 150 MB | nothing — regenerate themselves | — |

---

## 1. YOLOv2 custom checkpoints

Deleted: everything under `custom/ckpt/` (the directory itself was kept). The
run had reached step 1750 at loss ~0.66.

Retrain from the pretrained COCO weights. `prepare` rebuilds the cfg/labels/
dataset layout first and is idempotent:

```bash
.venv/bin/python yolov2_custom_object.py prepare
.venv/bin/python yolov2_custom_object.py train --epochs 300 --gpu 0.8
```

Roughly 3 s/step, ~3600 steps, so budget about 3 hours. It is usable much
earlier — loss was already ~0.66 by step 1750 (~1.5 h), past the course's
step-1200 checkpoint.

To watch it without tying up the terminal:

```bash
nohup .venv/bin/python yolov2_custom_object.py train --epochs 300 --gpu 0.8 > /tmp/r2d2-train.log 2>&1 &
tail -f /tmp/r2d2-train.log
```

**Checkpoints are big:** ~810 MB per save (a 606 MB data file plus a 204 MB
`.meta` graph), and `--keep 5` holds five of them, so `custom/ckpt/` settles
around 4 GB. Use `--keep 2` if disk is tight.

Once trained, notebook 18 and the CLI both pick it up with `load: -1`.

## 2. `models/` — the TensorFlow Models repo

Deleted: the whole clone. Notebooks 15 and 16 import `object_detection` from it.

```bash
git clone https://github.com/tensorflow/models.git
```

Then run the **"Installing the TF2 Object Detection API locally"** cells in
[15.Tensorflow-Object-Detection-API.ipynb](15.Tensorflow-Object-Detection-API.ipynb),
which compile the protos and install the package. They matter — do not
substitute a plain `protoc` from Homebrew. The notebook runs protoc through
`grpcio-tools` so the generated `*_pb2.py` matches the protobuf 5.29 runtime
that TF 2.19 pins; Homebrew's protoc 36.x produces
`Detected incompatible Protobuf Gencode/Runtime versions` at import time.

The shell equivalent of those cells:

```bash
.venv/bin/python -c "
from importlib.resources import files
from grpc_tools import protoc
from pathlib import Path
research = Path('models/research').resolve()
od = research / 'object_detection'
well_known = str(files('grpc_tools').joinpath('_proto'))
protos = sorted(str(p.relative_to(research)) for p in od.glob('protos/*.proto'))
rc = protoc.main(['protoc', f'-I{research}', f'-I{well_known}',
                  f'--python_out={research}', *protos])
assert rc == 0, rc
print('protos compiled')
"
cp models/research/object_detection/packages/tf2/setup.py models/research/
cd models/research && ../../.venv/bin/python -m pip install --no-deps -e . && cd ../..
```

## 3. BCCD training checkpoints

Deleted: `code/5-Object_Detection/TF2ODAPI/training/faster_rcnn_resnet50_v1_bccd/`
— the Faster R-CNN checkpoints from the BCCD blood-cell run.

This one is **your own training output**, so it only comes back by retraining.
Everything needed to do that survived: `pipeline_bccd_local.config`, the
`BCCD/` dataset, and the tfrecords. Requires sections 2 and 4 first.

```bash
cd code/5-Object_Detection/TF2ODAPI
../../../.venv/bin/python ../../../models/research/object_detection/model_main_tf2.py \
  --pipeline_config_path=pipeline_bccd_local.config \
  --model_dir=training/faster_rcnn_resnet50_v1_bccd \
  --alsologtostderr
```

`pipeline_bccd_local.config` sets `num_steps: 1500`. The exported saved_model in
`TF2ODAPI/exported-models/faster_rcnn_resnet50_v1_bccd/` was **not** deleted, so
if you only want to run inference, use that and skip retraining entirely.

## 4. ODAPI pretrained model

Deleted: `code/5-Object_Detection/TF2ODAPI/pre-trained-models/`.

`pipeline_bccd_local.config` line 113 expects it at exactly
`pre-trained-models/faster_rcnn_resnet50_v1_640x640_coco17_tpu-8/checkpoint/ckpt-0`,
so extract it in place:

```bash
cd code/5-Object_Detection/TF2ODAPI
mkdir -p pre-trained-models && cd pre-trained-models
curl -O http://download.tensorflow.org/models/object_detection/tf2/20200711/faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.tar.gz
tar -xzf faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.tar.gz
rm faster_rcnn_resnet50_v1_640x640_coco17_tpu-8.tar.gz
```

Any other TF2 detection model works the same way — same base URL,
`http://download.tensorflow.org/models/object_detection/tf2/20200711/`, with the
model name plus `.tar.gz`.

## 5. Open Images v6 (via FiftyOne)

Deleted: `openimagesv6/` in this folder. FiftyOne's own cache under `~/fiftyone`
and `~/.fiftyone` (69 MB) was left in place — delete it separately if you want.

**This one is tracked in git** — 87 files — so the fastest restore is not a
re-download at all:

```bash
git checkout -- 54.Deep-Learning-for-Computer-Vision-with-TensorFlow-2/openimagesv6
```

(`models/` and `pre-trained-models/` were untracked, so they do need the
re-clone and re-download described above.)

Otherwise notebook 14 re-downloads on demand; just run its cells. The call it
makes:

```python
import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset(
    "open-images-v6",
    split="validation",
    label_types=["detections"],
    classes=["Motorcycle", "Car"],
    max_samples=20,
)
```

## 6. darkflow Cython extensions

Deleted: `darkflow/build/` — the intermediate build tree only.

**Nothing is broken.** The compiled `.so` files live in
`darkflow/darkflow/cython_utils/` and are still there, so darkflow imports fine.
Only rebuild if you change a `.pyx`:

```bash
cd darkflow && ../.venv/bin/python setup.py build_ext --inplace && cd ..
```

## 7. Detection output videos

Deleted: the seven `videos_out/*-yolov2.mp4` files. These were outputs, not
inputs — the source `.mp4` files in the module root are untouched.
`videos_out/R2D2-coco-output.mp4` was left alone.

Regenerate with the pretrained COCO model (no custom training needed):

```bash
cd darkflow
for v in cars bikes people motorbikes ppe-1 ppe-2 ppe-3; do
  ../.venv/bin/python flow \
    --model cfg/yolo.cfg --load bin/yolo.weights \
    --demo "../$v.mp4" \
    --saveVideo --saveVideoPath "../videos_out/$v-yolov2.mp4" \
    --threshold 0.4 --gpu 0.8
done
cd ..
```

`darkflow/bin/yolo.weights` is a symlink into `resources/12.4 yolo/`; if it ever
goes missing:

```bash
mkdir -p darkflow/bin
ln -sf "../../resources/12.4 yolo/yolo.weights" darkflow/bin/yolo.weights
```

See [Object-Detection-on-Videos-with-Yolo.md](Object-Detection-on-Videos-with-Yolo.md).

## 8. The deleted `resources/` archives

These were Udemy course downloads. **Nothing currently needs them**, which is why
they went. If you do want one back, it is a re-download from the course page —
or, for the weights, from the original source.

| Deleted | Why it was safe |
| --- | --- |
| `12.4 yolo.zip`, `14.1 rd2d2.zip`, `14.4 yolov2_weights.zip` | Their extracted directories are still present — the zips were pure duplicates. |
| `16.1 cudnn-10.0-linux-x64-v7.5.0.56.tgz` | A Linux/CUDA library. It cannot run on Apple Silicon at all. |
| `16.2 darknet53.conv.74.zip` | YOLOv3 backbone. Re-fetch: `curl -O https://pjreddie.com/media/files/darknet53.conv.74` |
| `20.2 yolov4.conv.137.zip` | YOLOv4 backbone. Re-fetch: `curl -LO https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137` |
| `20.3 yolov4.zip` | Contained `yolov4.weights`, which is **still present** at `resources/yolov4.weights`. |

The two backbone files are only needed to *train* YOLOv3/v4 from scratch
(notebook 19). Inference uses the full weights, which survived.

### One thing to know about the YOLO weights

`resources/14.4 yolov2_weights/yolov2.weights` and
`resources/12.4 yolo/yolo.weights` were byte-identical 194 MB copies, so one is
now a **hardlink** to the other. Both paths work exactly as before and both
still read as normal files. The only consequence: editing one edits the other.
They are immutable weight blobs, so this does not matter in practice. To undo:

```bash
cp "resources/12.4 yolo/yolo.weights" /tmp/w && mv /tmp/w "resources/14.4 yolov2_weights/yolov2.weights"
```

## Kept deliberately

Not deleted, and worth not deleting later either:

- `resources/` (525 MB) — course material, only re-obtainable from Udemy.
- `data/15.1 covid19` (162 MB) — dataset for notebook 9.
- `images/` (1 GB) — the `Note.md` screenshots.
- `.venv` (2.5 GB) — rebuildable with `uv sync`, but needed to run anything.
- `TF2ODAPI/exported-models/` (221 MB) — the exported BCCD saved_model, a final
  artifact rather than a checkpoint.
- `darkflow/` source, including the four TF2 patches described in
  [Custom-Object-Detection-with-Yolo.md](Custom-Object-Detection-with-Yolo.md).

If the environment itself ever needs rebuilding:

```bash
uv sync
```
