"""Stand-ins for the two `tf.contrib.slim` functions darkflow uses.

`tf.contrib` was removed in TensorFlow 2, and the standalone `tf_slim`
package no longer imports against TF >= 2.16 (it reaches for
`tensorflow.python.framework.ops.Tensor`, which moved). darkflow only ever
calls `slim.batch_norm` and `slim.flatten`, so both are reimplemented here on
top of public `tf.compat.v1` ops with the same signatures and semantics.
"""
import tensorflow.compat.v1 as tf


def flatten(inputs, scope=None):
    """Flatten everything but the batch dimension, like slim.flatten."""
    dims = inputs.get_shape().as_list()[1:]
    if any(d is None for d in dims):
        return tf.reshape(inputs, [tf.shape(inputs)[0], -1], name=scope)
    size = 1
    for d in dims:
        size *= d
    return tf.reshape(inputs, [-1, size], name=scope)


def batch_norm(inputs, center=True, scale=True, epsilon=1e-5, scope=None,
               is_training=True, param_initializers=None,
               updates_collections=None, decay=0.999):
    """slim.batch_norm over the last axis.

    `updates_collections` is accepted for signature compatibility; the moving
    averages are always updated in-place under a control dependency, which is
    what darkflow asks for by passing `updates_collections=None`.
    """
    param_initializers = param_initializers or {}
    channels = inputs.get_shape().as_list()[-1]

    def _param(name, default, trainable):
        return tf.get_variable(
            name, shape=[channels], dtype=tf.float32, trainable=trainable,
            initializer=param_initializers.get(name, default))

    with tf.variable_scope(scope, default_name='BatchNorm',
                           reuse=tf.AUTO_REUSE):
        moving_mean = _param('moving_mean', tf.zeros_initializer(), False)
        moving_variance = _param('moving_variance', tf.ones_initializer(), False)
        gamma = _param('gamma', tf.ones_initializer(), True) if scale else None
        beta = _param('beta', tf.zeros_initializer(), True) if center else None

        def _normalize(mean, variance):
            return tf.nn.batch_normalization(
                inputs, mean, variance, beta, gamma, epsilon)

        def _train():
            axes = list(range(len(inputs.get_shape()) - 1))
            mean, variance = tf.nn.moments(inputs, axes)
            updates = [
                tf.assign(moving_mean,
                          moving_mean * decay + mean * (1 - decay)),
                tf.assign(moving_variance,
                          moving_variance * decay + variance * (1 - decay)),
            ]
            with tf.control_dependencies(updates):
                return _normalize(mean, variance)

        def _infer():
            return _normalize(moving_mean, moving_variance)

        if isinstance(is_training, bool):
            return _train() if is_training else _infer()
        return tf.cond(is_training, _train, _infer)
