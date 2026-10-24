"""Make the TF2 Object Detection API importable on TensorFlow >= 2.16.

Two things broke between the version of the API on PyPI and modern TensorFlow:

1. `tf.compat.v1.estimator` was removed in TF 2.16. `object_detection.inputs`
   imports it, but on the TF2 code path it only ever reads
   `ModeKeys.{TRAIN,EVAL,PREDICT}` -- three string constants. We install a tiny
   stand-in providing exactly those.
2. TF >= 2.16 makes `tf.keras` point at Keras 3, which the API is not written
   against. Setting TF_USE_LEGACY_KERAS=1 points it back at Keras 2 (`tf_keras`).

Import this module BEFORE importing anything from `object_detection`.
"""
import os
import sys
import types

os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")
# Keep the console readable; the API is very chatty.
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import tensorflow as tf


def _install_estimator_shim():
    v1 = tf.compat.v1
    if hasattr(v1, "estimator"):
        return "already present"

    class ModeKeys:
        TRAIN = "train"
        EVAL = "eval"
        PREDICT = "infer"

    shim = types.ModuleType("tensorflow.compat.v1.estimator")
    shim.ModeKeys = ModeKeys
    v1.estimator = shim
    sys.modules["tensorflow.compat.v1.estimator"] = shim
    return "installed"


def _install_control_flow_shim():
    """tf_slim (used by the API's TFRecord decoder) calls
    `control_flow_ops.case` / `.cond` / `.while_loop`. Those moved out of
    `control_flow_ops` into their own modules in newer TensorFlow. Alias them
    back so the decoder keeps working."""
    import importlib
    import inspect

    from tensorflow.python.ops import control_flow_ops

    sources = []
    for name in ("control_flow_case", "cond", "while_loop"):
        try:
            sources.append(importlib.import_module(f"tensorflow.python.ops.{name}"))
        except ImportError:
            pass

    restored = []
    for name in ("case", "case_v2", "cond", "cond_v2", "while_loop"):
        if hasattr(control_flow_ops, name):
            continue
        for src in sources:
            candidate = getattr(src, name, None)
            # Several of these modules are themselves named `cond`/`while_loop`
            # and re-export each other, so insist on an actual function.
            if callable(candidate) and not inspect.ismodule(candidate):
                setattr(control_flow_ops, name, candidate)
                restored.append(name)
                break
    return restored


status = _install_estimator_shim()
restored_ops = _install_control_flow_shim()


def check():
    """Import the API and report versions -- call once from the notebook."""
    from object_detection import model_lib_v2  # noqa: F401
    from object_detection.utils import label_map_util  # noqa: F401
    print(f"tensorflow      {tf.__version__}")
    import tf_keras
    print(f"tf.keras        {tf_keras.__version__} (legacy Keras 2)")
    print(f"estimator shim  {status}")
    print(f"control_flow     restored {restored_ops or 'nothing needed'}")
    print(f"GPUs            {tf.config.list_physical_devices('GPU')}")
