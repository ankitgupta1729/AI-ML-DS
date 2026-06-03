# GATE DA — Data Science & AI Quick Reference

Dense reference for the GATE Data Science & AI syllabus: probability,
linear algebra, ML, DL and AI. Use it to ground concept explanations.

## Probability & Statistics
- **Basics:** sample space, conditional probability `P(A|B)=P(A∩B)/P(B)`,
  **Bayes' theorem** `P(A|B)=P(B|A)P(A)/P(B)`, independence.
- **Distributions:** Bernoulli, Binomial, Poisson, Uniform, Normal,
  Exponential. Mean/variance of each (e.g. Binomial: `np`, `np(1-p)`).
- **Descriptive stats:** mean, median, mode, variance, std dev, covariance,
  correlation (Pearson).
- **Inference:** CLT, confidence intervals, hypothesis testing (z/t-tests,
  p-value, Type I/II errors), MLE & MAP estimation.

## Linear Algebra
- Vectors, matrices, rank, determinant, inverse; systems `Ax=b`
  (Gaussian elimination). Vector spaces, basis, dimension, null space.
- **Eigenvalues/eigenvectors:** `Av=λv`; `det(A-λI)=0`. Diagonalisation
  `A=PDP⁻¹`. Symmetric matrices → orthogonal eigenvectors (spectral theorem).
- **Decompositions:** LU, QR, **SVD** `A=UΣVᵀ` (basis of PCA, low-rank approx).
- Positive-definite matrices; quadratic forms.

## Calculus & Optimisation
- Limits, derivatives, partial derivatives, gradient `∇f`, Hessian.
- Maxima/minima, Lagrange multipliers (constrained optimisation).
- **Gradient descent:** `θ ← θ − η∇L(θ)`; learning rate η; convex vs non-convex.
  Variants: SGD, momentum, RMSProp, Adam.

## Machine Learning
- **Supervised:** regression (linear, ridge/lasso) & classification (logistic
  regression, k-NN, SVM with kernels, decision trees, random forests,
  gradient boosting, naïve Bayes).
- **Unsupervised:** k-means, hierarchical clustering, GMM (EM algorithm),
  PCA (dimensionality reduction via top eigenvectors of covariance).
- **Bias–variance trade-off:** underfit (high bias) vs overfit (high variance);
  regularisation (L1/L2), cross-validation, train/val/test split.
- **Evaluation:** accuracy, precision, recall, F1, ROC-AUC, confusion matrix;
  for regression MSE/RMSE/MAE, R².
- **Loss functions:** MSE (regression), cross-entropy (classification),
  hinge (SVM).

## Deep Learning
- **Perceptron → MLP:** layers, weights, biases, activations (sigmoid, tanh,
  **ReLU**, softmax). Universal approximation.
- **Backpropagation:** chain rule to compute gradients layer by layer.
- **Training issues:** vanishing/exploding gradients, dropout, batch norm,
  weight initialisation, early stopping.
- **CNNs:** convolution, filters/kernels, stride, padding, pooling; great for
  images. **RNN/LSTM/GRU:** sequences; **Transformers:** self-attention
  `softmax(QKᵀ/√d)V`, the basis of modern LLMs.

## Artificial Intelligence
- **Search:** uninformed (BFS, DFS, UCS) vs informed (greedy best-first, **A***
  with admissible/consistent heuristics). Adversarial: minimax, alpha-beta.
- **Logic:** propositional & first-order logic, resolution, inference.
- **Knowledge & reasoning:** Bayesian networks, probabilistic inference.
- **Markov models:** Markov chains, HMMs (forward/Viterbi), MDPs &
  reinforcement learning (value/policy iteration, Q-learning).

## Data Science Practice
- Data wrangling, feature engineering & scaling (standardisation/normalisation),
  handling missing data & class imbalance.
- The ML workflow: define problem → collect/clean data → EDA → model → evaluate
  → deploy → monitor.
