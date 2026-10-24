#!/usr/bin/env python
"""YOLOv2 custom object detection with darkflow: train, then run on video or webcam.

This is the macOS / TensorFlow 2 equivalent of the course's Windows workflow. It
folds the three course steps -- edit cfg, train with `flow --train`, and run
`yolov2_custom_object_cam.py` -- into one file.

    python yolov2_custom_object.py prepare
    python yolov2_custom_object.py train --epochs 300 --gpu 0.8
    python yolov2_custom_object.py video --input code/5-Object_Detection/darknetv3/R2D2.avi
    python yolov2_custom_object.py cam

Run `python yolov2_custom_object.py <command> --help` for the full flag list.

Layout built by `prepare` (mirrors the course's darkflow/train folder):

    custom/
      cfg/yolov2.cfg       source architecture, must match the .weights file
      cfg/yolov2-1c.cfg    the custom model: classes=1, filters=30
      labels.txt           one class name per line
      train/images         Pascal VOC images    (symlink into resources/)
      train/annotations    Pascal VOC xml       (symlink into resources/)
      ckpt/                training checkpoints
"""

import argparse
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

# --- paths -----------------------------------------------------------------
DARKFLOW_DIR = os.path.join(HERE, 'darkflow')
CUSTOM_DIR = os.path.join(HERE, 'custom')
CFG_DIR = os.path.join(CUSTOM_DIR, 'cfg')
MODEL_CFG = os.path.join(CFG_DIR, 'yolov2-1c.cfg')
LABELS_TXT = os.path.join(CUSTOM_DIR, 'labels.txt')
TRAIN_IMAGES = os.path.join(CUSTOM_DIR, 'train', 'images')
TRAIN_ANNOTATIONS = os.path.join(CUSTOM_DIR, 'train', 'annotations')
CKPT_DIR = os.path.join(CUSTOM_DIR, 'ckpt')
VIDEOS_OUT = os.path.join(HERE, 'videos_out')

# Course resources this workflow is built from.
SRC_DATASET = os.path.join(HERE, 'resources', '14.1 rd2d2')
SRC_MODEL_CFG = os.path.join(HERE, 'resources', '14.4 yolov2_weights', 'yolov2-1c.cfg')
SRC_WEIGHTS = os.path.join(HERE, 'resources', '14.4 yolov2_weights', 'yolov2.weights')
# yolov2.weights is COCO YOLOv2, whose architecture is darkflow's own yolo.cfg.
# darkflow looks for <weights basename>.cfg next to the model cfg to know the
# layer layout it should read the binary with, so yolov2.cfg has to exist too.
SRC_ARCH_CFG = os.path.join(DARKFLOW_DIR, 'cfg', 'yolo.cfg')

DEFAULT_LABELS = ['r2d2']
DEFAULT_VIDEO = os.path.join(HERE, 'code', '5-Object_Detection', 'darknetv3', 'R2D2.avi')


def load_tfnet():
    """Import darkflow's TFNet from the vendored, TF2-patched copy."""
    if DARKFLOW_DIR not in sys.path:
        sys.path.insert(0, DARKFLOW_DIR)
    # A stale darkflow in sys.modules would keep serving pre-patch source.
    for name in [m for m in sys.modules if m == 'darkflow' or m.startswith('darkflow.')]:
        del sys.modules[name]
    os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')
    from darkflow.net.build import TFNet
    return TFNet


# --- prepare ---------------------------------------------------------------

def _link(src, dst):
    """Symlink src -> dst, leaving an existing correct link alone."""
    if os.path.islink(dst):
        if os.path.realpath(dst) == os.path.realpath(src):
            return 'ok'
        os.unlink(dst)
    elif os.path.exists(dst):
        return 'kept (real directory, not touched)'
    os.symlink(os.path.relpath(src, os.path.dirname(dst)), dst)
    return 'linked'


def prepare(labels=None):
    """Build the custom/ layout. Idempotent -- safe to re-run."""
    labels = labels or DEFAULT_LABELS

    for missing in [p for p in (SRC_DATASET, SRC_MODEL_CFG, SRC_WEIGHTS, SRC_ARCH_CFG)
                    if not os.path.exists(p)]:
        raise SystemExit('missing course resource: {}'.format(missing))

    for d in (CFG_DIR, os.path.join(CUSTOM_DIR, 'train'), CKPT_DIR, VIDEOS_OUT):
        os.makedirs(d, exist_ok=True)

    # The model cfg, and the source architecture the .weights file was saved from.
    shutil.copyfile(SRC_MODEL_CFG, MODEL_CFG)
    shutil.copyfile(SRC_ARCH_CFG, os.path.join(CFG_DIR, 'yolov2.cfg'))
    print('cfg      : {} (+ yolov2.cfg source arch)'.format(MODEL_CFG))

    with open(LABELS_TXT, 'w') as f:
        f.write('\n'.join(labels) + '\n')
    print('labels   : {} -> {}'.format(LABELS_TXT, ', '.join(labels)))

    print('images   : {}'.format(_link(os.path.join(SRC_DATASET, 'images'), TRAIN_IMAGES)))
    print('annots   : {}'.format(_link(os.path.join(SRC_DATASET, 'annotations'), TRAIN_ANNOTATIONS)))

    n_img = len([f for f in os.listdir(TRAIN_IMAGES) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    n_ann = len([f for f in os.listdir(TRAIN_ANNOTATIONS) if f.endswith('.xml')])
    print('dataset  : {} images, {} annotations'.format(n_img, n_ann))

    _check_cfg(len(labels))
    return n_img


def _check_cfg(n_classes):
    """The last conv layer must have 5 x (n_classes + 5) filters."""
    want = 5 * (n_classes + 5)
    with open(MODEL_CFG) as f:
        lines = [l.strip() for l in f]
    got_classes = next((int(l.split('=')[1]) for l in lines if l.startswith('classes=')), None)
    filters = [int(l.split('=')[1]) for l in lines if l.startswith('filters=')]
    got_filters = filters[-1] if filters else None
    if got_classes != n_classes or got_filters != want:
        raise SystemExit(
            'cfg mismatch: {} has classes={} and last filters={}, '
            'but {} label(s) need classes={} and filters={}'.format(
                os.path.basename(MODEL_CFG), got_classes, got_filters,
                n_classes, n_classes, want))
    print('cfg check: classes={}, last filters={} (5 x ({} + 5))'.format(
        got_classes, got_filters, n_classes))


# --- shared net construction ----------------------------------------------

def build_net(load, threshold, gpu, train=False, **extra):
    """Construct a TFNet. `load` is a .weights path, or an int checkpoint step
    (-1 = most recent)."""
    TFNet = load_tfnet()
    options = {
        'model': MODEL_CFG,
        'config': CFG_DIR,
        'labels': LABELS_TXT,
        'backup': CKPT_DIR,
        'binary': os.path.join(DARKFLOW_DIR, 'bin') + os.sep,
        'load': load,
        'threshold': threshold,
        'gpu': gpu,
        'train': train,
    }
    options.update(extra)
    return TFNet(options)


def _resolve_load(value):
    """--load takes an int step, -1 for latest, or a path to .weights."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return value


# --- train -----------------------------------------------------------------

def cmd_train(args):
    n_img = prepare()

    if args.save < args.batch:
        raise SystemExit('--save ({}) must be >= --batch ({}): darkflow checkpoints '
                         'every (save // batch) steps'.format(args.save, args.batch))

    load = _resolve_load(args.load) if args.load is not None else SRC_WEIGHTS
    if isinstance(load, str):
        print('starting from pretrained weights: {}'.format(load))
    else:
        print('resuming from checkpoint step: {}'.format(load))

    steps_per_epoch = max(n_img // args.batch, 1)
    print('~{} steps/epoch x {} epochs = ~{} steps\n'.format(
        steps_per_epoch, args.epochs, steps_per_epoch * args.epochs))

    net = build_net(
        load=load, threshold=args.threshold, gpu=args.gpu, train=True,
        annotation=TRAIN_ANNOTATIONS, dataset=TRAIN_IMAGES,
        epoch=args.epochs, batch=args.batch, lr=args.lr,
        save=args.save, keep=args.keep, trainer=args.trainer,
    )
    started = time.time()
    net.train()
    print('\nTraining finished in {:.1f} min. Checkpoints in {}'.format(
        (time.time() - started) / 60, CKPT_DIR))
    print('Run detection with:  python {} video --load -1'.format(
        os.path.basename(__file__)))


# --- detection -------------------------------------------------------------

def _draw(frame, results):
    """Draw the course's box + 'label: NN%' overlay. Mutates and returns frame."""
    import cv2
    for r in results:
        tl = (r['topleft']['x'], r['topleft']['y'])
        br = (r['bottomright']['x'], r['bottomright']['y'])
        text = '{}: {:.0f}%'.format(r['label'], r['confidence'] * 100)
        cv2.rectangle(frame, tl, br, (0, 0, 255), 5)
        cv2.putText(frame, text, (tl[0], max(tl[1] - 10, 15)),
                    cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
    return frame


def cmd_video(args):
    import cv2

    source = args.input or DEFAULT_VIDEO
    if not os.path.isfile(source):
        raise SystemExit('input video not found: {}'.format(source))

    output = args.output or os.path.join(
        VIDEOS_OUT, os.path.splitext(os.path.basename(source))[0] + '-custom.mp4')
    os.makedirs(os.path.dirname(output) or '.', exist_ok=True)

    net = build_net(load=_resolve_load(args.load), threshold=args.threshold, gpu=args.gpu)

    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise SystemExit('cannot open {}'.format(source))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS) or 25.0

    writer = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    if not writer.isOpened():
        raise SystemExit('cannot open {} for writing'.format(output))
    print('\n{} ({}x{} @ {:.0f} fps) -> {}\n'.format(source, width, height, fps, output))

    frames = hits = 0
    started = time.time()
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        results = net.return_predict(frame)   # darkflow expects BGR, as cv2 reads it
        hits += len(results)
        writer.write(_draw(frame, results))
        frames += 1
        if frames % 10 == 0:
            sys.stdout.write('\r{} frames, {} detections, {:.1f} FPS'.format(
                frames, hits, frames / (time.time() - started)))
            sys.stdout.flush()
        if args.max_frames and frames >= args.max_frames:
            break

    writer.release()
    capture.release()
    print('\n\nWrote {} ({} frames, {} detections)'.format(output, frames, hits))


def cmd_cam(args):
    import cv2

    net = build_net(load=_resolve_load(args.load), threshold=args.threshold, gpu=args.gpu)

    capture = cv2.VideoCapture(args.camera)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    if not capture.isOpened():
        raise SystemExit('cannot open camera {}. On macOS, grant the terminal app '
                         'Camera access in System Settings > Privacy & Security.'.format(args.camera))

    print("\nPress 'q' in the video window to quit.\n")
    while True:
        started = time.time()
        ok, frame = capture.read()
        if not ok:
            break
        frame = _draw(frame, net.return_predict(frame))
        cv2.imshow('custom object detection', frame)
        print('FPS {:.1f}'.format(1 / max(time.time() - started, 1e-6)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


# --- cli -------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)

    def detect_flags(p, default_threshold):
        p.add_argument('--load', default='-1',
                       help='checkpoint step, -1 for the most recent (default), '
                            'or a path to a .weights file')
        p.add_argument('--threshold', type=float, default=default_threshold,
                       help='minimum confidence (default: %(default)s)')
        p.add_argument('--gpu', type=float, default=0.8,
                       help='fraction of GPU memory, 0.0 for CPU (default: %(default)s)')

    p = sub.add_parser('prepare', help='build the custom/ training layout')
    p.add_argument('--labels', nargs='+', default=DEFAULT_LABELS,
                   help='class names (default: %(default)s)')
    p.set_defaults(func=lambda a: prepare(a.labels))

    p = sub.add_parser('train', help='train the custom model')
    p.add_argument('--epochs', type=int, default=300, help='(default: %(default)s)')
    p.add_argument('--batch', type=int, default=16, help='(default: %(default)s)')
    p.add_argument('--lr', type=float, default=1e-5, help='(default: %(default)s)')
    p.add_argument('--save', type=int, default=2000,
                   help='checkpoint every N examples (default: %(default)s)')
    p.add_argument('--keep', type=int, default=5,
                   help='checkpoints to keep (default: %(default)s)')
    p.add_argument('--trainer', default='rmsprop', help='(default: %(default)s)')
    p.add_argument('--threshold', type=float, default=0.1)
    p.add_argument('--gpu', type=float, default=0.8,
                   help='fraction of GPU memory, 0.0 for CPU (default: %(default)s)')
    p.add_argument('--load', default=None,
                   help='resume from this checkpoint step (-1 = latest); '
                        'default is to start from the pretrained yolov2.weights')
    p.set_defaults(func=cmd_train)

    p = sub.add_parser('video', help='detect in a video file and save the result')
    p.add_argument('--input', default=None,
                   help='source video (default: {})'.format(os.path.relpath(DEFAULT_VIDEO, HERE)))
    p.add_argument('--output', default=None, help='default: videos_out/<name>-custom.mp4')
    p.add_argument('--max-frames', type=int, default=0, help='stop early, for a quick check')
    detect_flags(p, 0.1)
    p.set_defaults(func=cmd_video)

    p = sub.add_parser('cam', help='detect from the webcam')
    p.add_argument('--camera', type=int, default=0, help='device index (default: %(default)s)')
    p.add_argument('--width', type=int, default=1280)
    p.add_argument('--height', type=int, default=720)
    detect_flags(p, 0.1)
    p.set_defaults(func=cmd_cam)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
