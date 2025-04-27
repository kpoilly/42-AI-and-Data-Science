# 🍃 LeAffliction

**LeAffliction** is a Streamlit-based application designed for analyzing and visualizing plant leaf imagery. It includes tools for inspecting image distributions, performing augmentations, and applying advanced transformations for further processing.

---

## 🛠 Installation & Usage

### Installation

Make sure you have all necessary dependencies installed. Then simply run:

```bash
make install
```

### Start the Streamlit App

To launch the Streamlit interface, run:

```bash
make start
```

---

### 📦 Programs

#### 1. 📊 Distribution

Visualize the distribution of image data in a folder:

```bash
python3 src/Distribution.py path/to/folder
```

#### 2. 🧪 Augmentation

Visualize augmentations for a single image:

```bash
python3 src/Augmentation.py path/to/file
```

**Supported transformations:**

- Rotate
- Flip
- Crop
- Shear
- Blur
- Contrast

Generate augmented images for all files in a folder:

```bash
python3 src/Augmentation.py path/to/folder
```

_Augmented images will be saved next to the originals._

#### 3. 🔬 Transformation

Visualize transformations applied to a single image:

```bash
python3 src/Transformation.py -src path/to/file
```

**Displays:**

- Original
- Gaussian Blur
- Mask
- ROI Object
- Analyze Object
- Pseudo-landmark
- Color Histogram

Apply transformations to all images in a folder:

```bash
python3 src/Transformation.py -src path/to/folder -dst path/to/destination
```

_Transformed images will be saved in the dst folder._

---

### 📁 Project Structure

```
├── src/
│   ├── pages/
│   │   ├── distribution
│   │   ├── augmentation
│   │   ├── transformation
│   │   ├── train
│   │   └── predict
│   ├── Distribution.py
│   ├── Augmentation.py
│   ├── Transformation.py
│   ├── Train.py
│   └── Predict.py
├── makefile
└── README.md
```

---
