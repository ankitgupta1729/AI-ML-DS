"""Real-time object detection from the webcam with YOLOv2 (darkflow).

The course runs this on Windows with `cv2.VideoCapture(1)` and a CUDA GPU. Here
darkflow is vendored and patched for TF2/NumPy 2 (see
17.Object-Detection-on-Images-with-Yolo.ipynb), and the TF1 graph runs on the
Metal GPU, so the only real changes are the camera index and the paths.

    ../.venv/bin/python yolov2_od_webcam.py

Press [q] or [ESC] in the preview window to stop.
"""

import argparse
import os
import sys
import time

# darkflow is vendored, not pip-installed, so its repo root goes on sys.path.
# Everything is resolved relative to this file, so the script can be run from
# any working directory.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'darkflow'))

os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')  # darkflow is chatty enough

import cv2
import numpy as np

from darkflow.net.build import TFNet


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--camera', type=int, default=0,
                   help='capture device index; 0 is the built-in camera on a Mac '
                        '(the course uses 1 for an external one). Default: 0')
    p.add_argument('--threshold', type=float, default=0.4,
                   help="minimum confidence. darkflow's default is low enough to "
                        'produce duplicate and spurious boxes. Default: 0.4')
    p.add_argument('--gpu', type=float, default=0.8,
                   help='fraction of GPU memory to reserve; 0.0 forces CPU. Default: 0.8')
    p.add_argument('--width', type=int, default=1280, help='capture width. Default: 1280')
    p.add_argument('--height', type=int, default=720, help='capture height. Default: 720')
    p.add_argument('--save', metavar='PATH', default=None,
                   help='also record the annotated stream to this .mp4')
    return p.parse_args()


def build_net(args):
    options = {
        'model': os.path.join(HERE, 'resources/12.4 yolo/yolo.cfg'),
        'load': os.path.join(HERE, 'resources/12.4 yolo/yolo.weights'),
        # darkflow looks for coco.names under './cfg/' relative to the *current*
        # working directory, so point it at the vendored copy explicitly.
        'config': os.path.join(HERE, 'darkflow/cfg/'),
        'threshold': args.threshold,
        'gpu': args.gpu,
    }
    return TFNet(options)


def open_camera(args):
    # AVFoundation is the backend that actually works on macOS; without it
    # OpenCV can fall back to a stub that opens and then yields empty frames.
    backend = cv2.CAP_AVFOUNDATION if sys.platform == 'darwin' else cv2.CAP_ANY
    capture = cv2.VideoCapture(args.camera, backend)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    if not capture.isOpened():
        sys.exit(
            'Could not open camera {}.\n'
            '  - On macOS the *terminal app* needs camera access: System Settings > '
            'Privacy & Security > Camera.\n'
            '  - Try a different index with --camera 1.'.format(args.camera)
        )
    return capture


def main():
    args = parse_args()
    tfnet = build_net(args)
    capture = open_camera(args)

    # One colour per COCO class, fixed across frames so a given label keeps its
    # colour. The course draws from a 10-colour list zipped against the results,
    # which silently drops every box past the tenth.
    rng = np.random.default_rng(1)
    colors = [tuple(int(c) for c in rng.integers(60, 256, 3)) for _ in range(80)]
    labels = {}

    writer = None
    if args.save:
        w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # avc1 (H.264) rather than mp4v, so the recording plays in QuickTime and
        # in the VS Code preview.
        writer = cv2.VideoWriter(args.save, cv2.VideoWriter_fourcc(*'avc1'), 20.0, (w, h))

    print('Camera {} open at {}x{}. Press [q] or [ESC] to quit.'.format(
        args.camera,
        int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    fps = 0.0
    try:
        while True:
            stime = time.time()
            ret, frame = capture.read()
            if not ret:
                print('Dropped frame from the camera, stopping.')
                break

            results = tfnet.return_predict(frame)

            for r in results:
                tl = (r['topleft']['x'], r['topleft']['y'])
                br = (r['bottomright']['x'], r['bottomright']['y'])
                label = r['label']
                color = colors[labels.setdefault(label, len(labels)) % len(colors)]
                text = '{}: {:.0f}%'.format(label, r['confidence'] * 100)

                cv2.rectangle(frame, tl, br, color, 3)
                cv2.putText(frame, text, (tl[0], max(tl[1] - 8, 14)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Smoothed so the number is readable rather than flickering.
            fps = 0.9 * fps + 0.1 / max(time.time() - stime, 1e-6)
            cv2.putText(frame, 'FPS {:.1f}'.format(fps), (12, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            if writer is not None:
                writer.write(frame)

            cv2.imshow('YOLOv2 - webcam', frame)
            if cv2.waitKey(1) & 0xFF in (ord('q'), 27):  # q or ESC
                break
    except KeyboardInterrupt:
        print('\nInterrupted.')
    finally:
        capture.release()
        if writer is not None:
            writer.release()
            print('Saved {}'.format(args.save))
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
