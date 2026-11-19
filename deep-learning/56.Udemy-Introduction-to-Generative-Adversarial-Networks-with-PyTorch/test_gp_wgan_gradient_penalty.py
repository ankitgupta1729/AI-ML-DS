"""Run with: python -m unittest discover -s 56.Udemy-Introduction-to-Generative-Adversarial-Networks-with-PyTorch -p 'test_gp_wgan_gradient_penalty.py'."""
import ast
import json
from pathlib import Path
import unittest

import torch


class GradientPenaltyTest(unittest.TestCase):
    def setUp(self):
        notebook = json.loads(
            Path(__file__).with_name('9.Implementation-of-GP-WGAN.ipynb').read_text()
        )
        # Load the actual function without running downloads or GAN training.
        functions = [
            node
            for cell in notebook['cells']
            if cell['cell_type'] == 'code' and 'def calcGradientPenalty(' in ''.join(cell['source'])
            for node in ast.parse(''.join(cell['source'])).body
            if isinstance(node, ast.FunctionDef) and node.name == 'calcGradientPenalty'
        ]
        self.assertEqual(len(functions), 1)
        self.scale = torch.tensor(1.0, requires_grad=True)
        namespace = {
            'torch': torch,
            'device': torch.device('cpu'),
            # This critic has input gradient scale * x.
            'discriminator': lambda x: self.scale * x.square().sum(dim=1, keepdim=True) / 2,
        }
        exec(compile(ast.Module(body=functions, type_ignores=[]), '<notebook>', 'exec'), namespace)
        self.penalty = namespace['calcGradientPenalty']

    def evaluate(self, samples):
        fake = torch.tensor(samples, dtype=torch.float32)
        # Equal endpoints make interpolation deterministic.
        return self.penalty(fake.unsqueeze(1), fake)

    def test_mixed_norms_do_not_cancel_and_support_backward(self):
        penalty = self.evaluate([[0.0, 0.0], [2.0, 0.0]])
        self.assertAlmostEqual(penalty.item(), 1.0)
        penalty.backward()
        self.assertAlmostEqual(self.scale.grad.item(), 2.0)

    def test_unit_norm_has_zero_penalty(self):
        self.assertAlmostEqual(self.evaluate([[1.0, 0.0], [0.0, 1.0]]).item(), 0.0)

    def test_single_sample(self):
        self.assertAlmostEqual(self.evaluate([[2.0, 0.0]]).item(), 1.0)


if __name__ == '__main__':
    unittest.main()
