# MLP vs. CNN for MNIST Classification

This project implements and compares two fundamental types of neural networks—a **Multi-Layer Perceptron (MLP)**, also known as a Feed-Forward Neural Network (FFNN), and a **Convolutional Neural Network (CNN)**—for classifying images in the **MNIST dataset**.

The goal is to illustrate the architectural differences, implementation complexity, and performance trade-offs between these two network types when applied to a standard image classification task.

---

### ✨ Features

* **Two Network Architectures:** Full implementations of both a standard **FFNN/MLP** and a **CNN**.
* **MNIST Dataset:** Utilizes the built-in MNIST dataset for image classification (handwritten digits 0-9).
* **Performance Comparison:** Directly compares the final accuracy and training dynamics (loss curves) of the FFNN and CNN models.
* **PyTorch Implementation:** All models and training loops are implemented using the **PyTorch** deep learning framework.

---

### 💻 Implementation Details

The Jupyter Notebook (`MLP_Using_FFNN_vs_CNN.ipynb`) covers the following steps:

1.  **Data Loading and Preprocessing:**
    * Loading the MNIST dataset using `torchvision.datasets`.
    * Applying standard image transformations (e.g., converting to tensor, normalization).
    * Creating DataLoaders for batch processing.

2.  **FFNN Model Definition (MLP):**
    * Defines a simple Feed-Forward Network architecture.
    * Crucially, demonstrates the need to **flatten** the $28 \times 28$ image input into a 784-dimensional vector before passing it to the linear layers.

3.  **CNN Model Definition:**
    * Defines a Convolutional Network architecture consisting of convolutional layers, pooling layers, and final linear layers.
    * Illustrates how CNNs natively process the 2D spatial structure of the image.

4.  **Training Loop:**
    * A generic training function is defined and reused for both models.
    * Uses the **Adam optimizer** and **Cross-Entropy Loss**.

5.  **Evaluation and Visualization:**
    * Evaluates the final test accuracy of both models.
    * Plots the **loss vs. epoch** for both networks to compare training stability and convergence speed.

---

### 🚀 Key Takeaways (MLP vs. CNN)

| Feature | FFNN (MLP) | CNN |
| :--- | :--- | :--- |
| **Input Handling** | Requires input images to be **flattened** (loses spatial information). | Processes input images in their native **2D format**. |
| **Key Operation** | Linear transformations (matrix multiplication) on flattened data. | **Convolution** (feature extraction) and **Pooling** (downsampling). |
| **Parameter Efficiency** | Generally high number of parameters for large images. | Uses **shared weights** (convolutional kernels), leading to fewer parameters and better efficiency. |
| **Performance on Images**| Generally lower accuracy and slower convergence. | **Superior accuracy** and faster convergence due to effective feature learning. |

---

### 🛠️ Dependencies

This project requires Python and the following libraries:

```bash
# Recommended environment setup
conda create -n mlp-cnn python=3.10
conda activate mlp-cnn

# Install PyTorch and related packages
pip install torch torchvision
pip install matplotlib
pip install numpy
