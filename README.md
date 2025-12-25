# 🌱 Plant Disease Detection - AI Challenge 2025

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.0.0](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Ứng dụng web AI phát hiện và phân loại **15 loại bệnh cây trồng** từ hình ảnh lá cây bằng Deep Learning (MobileNetV2).

![Demo](https://via.placeholder.com/800x400/4CAF50/FFFFFF?text=Plant+Disease+Detection+Demo)

---

## ✨ Tính năng chính

### 🎯 Core Features
- 🏠 **Trang chủ hiện đại**: UI responsive, gradient design
- 📸 **Upload ảnh đa dạng**: File picker + drag-drop + webcam capture
- 🔍 **AI Prediction**: Phát hiện bệnh với độ tin cậy cao (85-95%)
- 💊 **Gợi ý điều trị**: 15 loại bệnh với phương án xử lý chi tiết (Vietnamese)
- 📊 **Top-3 predictions**: Hiển thị 3 khả năng cao nhất với confidence bars
- 📈 **Circular progress**: Biểu đồ tròn trực quan độ tin cậy
- 📜 **Upload history**: Theo dõi lịch sử dự đoán với thumbnails
- 🎨 **Modern UI**: CSS animations, hover effects, responsive design

### 🤖 AI/ML Features
- **Model**: MobileNetV2 (transfer learning from ImageNet)
- **Architecture**: Lightweight (2.5M params) cho deployment hiệu quả
- **Accuracy**: 85-95% (depending on dataset quality)
- **Classes**: 15 loại bệnh cây trồng phổ biến tại Việt Nam
- **Data Augmentation**: Rotation, flip, zoom, shift, shear
- **Training**: Custom script với callbacks (early stopping, LR scheduling)

---

## 🚀 Quick Start (3 bước!)

### 1️⃣ Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Chạy ứng dụng
```bash
python app.py
```

### 3️⃣ Mở trình duyệt
```
http://localhost:5000
```

✅ **Xong!** App chạy ở **demo mode** với dummy predictions.

---

## 📦 Cài đặt đầy đủ

### Bước 1: Clone repository
```bash
git clone <repository-url>
cd PlantDiseaseDetection_AIChallenge2025
```

### Bước 2: Tạo virtual environment (khuyến nghị)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Bước 3: Cài đặt dependencies

**Cơ bản (chỉ chạy web app):**
```bash
pip install -r requirements.txt
```

**Đầy đủ (bao gồm training model):**
```bash
pip install -r requirements.txt
pip install tensorflow matplotlib
```

### Bước 4: Kiểm tra hệ thống
```bash
python check_system.py
```

Script này sẽ kiểm tra:
- ✅ Dependencies đã cài
- ✅ Project structure
- ✅ Dataset status
- ✅ Model status

---

## 🎓 Training Model (Production Mode)

### Option A: Tự train model

#### 1. Setup dataset
```bash
python download_dataset.py
```

Chọn:
- **Option 1**: Download từ Kaggle (PlantVillage - 54K images)
- **Option 2**: Download từ Google Drive
- **Option 3**: Setup thủ công

#### 2. Organize images
Thêm ảnh vào:
```
data/plant_diseases/
├── benh_dom_la/       (100+ images)
├── benh_gia_phan/     (100+ images)
├── benh_heo_xanh/     (100+ images)
└── ... (15 classes total)
```

**Khuyến nghị:**
- Tối thiểu: 100 ảnh/class
- Tốt: 500+ ảnh/class  
- Xuất sắc: 1000+ ảnh/class

#### 3. Train model
```bash
python train_model.py
```

**Training time:**
- GPU: 30-60 phút
- CPU: 2-5 giờ

**Output:**
- Model: `models/disease_model.h5`
- History: `models/training_history.png`

#### 4. Test model
```bash
# Test 1 ảnh
python test_model.py --image path/to/image.jpg

# Test folder
python test_model.py --folder path/to/folder/

# Evaluate full dataset
python test_model.py --evaluate
```

### Option B: Sử dụng pre-trained model

**Download PlantVillage model:**
1. Truy cập: [PlantVillage on Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease)
2. Download pretrained weights
3. Copy vào: `models/disease_model.h5`

**Hoặc train với dataset khác:**
- Tham khảo: [TRAINING_GUIDE.md](TRAINING_GUIDE.md)

---

## 📚 Documentation

| File | Description |
|------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Quick start guide với troubleshooting |
| [TRAINING_GUIDE.md](TRAINING_GUIDE.md) | Chi tiết training workflow |
| [MODEL_IMPROVEMENTS.md](MODEL_IMPROVEMENTS.md) | Summary features & improvements |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Current project status |

---

## 🗂️ Project Structure

```
PlantDiseaseDetection_AIChallenge2025/
│
├── 📄 app.py                      # Main Flask application
├── 📄 config.py                   # Configuration
├── 📄 requirements.txt            # Dependencies
├── 📄 train_model.py             # Training script
├── 📄 download_dataset.py        # Dataset utility
├── 📄 test_model.py              # Testing script
├── 📄 check_system.py            # System diagnostics ⭐NEW
│
├── 📁 templates/
│   └── index.html                 # Main UI
│
├── 📁 static/
│   ├── css/style.css             # Modern styles
│   ├── js/
│   │   ├── main.js               # Upload/prediction
│   │   └── chart_handler.js      # Visualizations
│   └── uploads/                   # Uploaded images
│
├── 📁 utils/
│   ├── model_handler.py          # Model inference
│   ├── preprocessing.py          # Image preprocessing
│   └── treatment_data.py         # 15 disease treatments
│
├── 📁 models/
│   ├── class_indices.json        # Class mappings
│   └── disease_model.h5          # Trained model (after training)
│
├── 📁 data/
│   └── plant_diseases/           # Dataset (to be created)
│       ├── benh_dom_la/
│       ├── benh_gia_phan/
│       └── ... (15 classes)
│
└── 📁 Documentation/
    ├── QUICKSTART.md
    ├── TRAINING_GUIDE.md
    ├── MODEL_IMPROVEMENTS.md
    └── PROJECT_STATUS.md

```

---

## 🎯 15 Loại bệnh được hỗ trợ

| # | Tên bệnh | English | Severity |
|---|----------|---------|----------|
| 1 | Bệnh đốm lá | Leaf spot | Medium |
| 2 | Bệnh giả phấn | Downy mildew | High |
| 3 | Bệnh héo xanh | Bacterial wilt | Critical |
| 4 | Bệnh khảm virus | Mosaic virus | Medium |
| 5 | Bệnh thán thư | Anthracnose | High |
| 6 | Bệnh thối rễ | Root rot | Critical |
| 7 | Bệnh đạo ôn | Blast disease | High |
| 8 | Bệnh xoăn lá | Leaf curl | Medium |
| 9 | Bệnh phấn trắng | Powdery mildew | Medium |
| 10 | Bệnh đốm vòng | Ring spot | Medium |
| 11 | Bệnh khảm lá | Leaf mosaic | Low |
| 12 | Bệnh thối quả | Fruit rot | High |
| 13 | Bệnh héo rũ | Wilting | High |
| 14 | Bệnh vàng lá | Leaf yellowing | Medium |
| 15 | Khỏe mạnh | Healthy | - |

**Mỗi bệnh bao gồm:**
- 🔬 Chuẩn đoán chi tiết
- 💊 Phương pháp điều trị (thuốc cụ thể)
- 🛡️ Biện pháp phòng ngừa
- ⚠️ Mức độ nguy hiểm

---

## 🛠️ Tech Stack

### Backend
- **Flask 3.0.0** - Web framework
- **TensorFlow/Keras** - Deep learning
- **Pillow 10.1.0** - Image processing
- **NumPy 1.24.3** - Numerical operations

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling (variables, animations)
- **JavaScript ES6+** - Vanilla JS
- **Chart.js 4.4.0** - Visualization

### AI/ML
- **MobileNetV2** - Transfer learning base
- **ImageNet** - Pretrained weights
- **Custom head** - Classification layers
- **Data augmentation** - Built-in

---

## 📊 Performance

### Model Specs
- **Parameters**: ~2.5M (lightweight)
- **Input**: 224x224x3 RGB
- **Output**: 15 classes
- **Inference**: 20-50ms (GPU) / 200-300ms (CPU)

### Expected Accuracy
| Dataset Size | Validation Acc |
|--------------|----------------|
| 1,500 images | 80-85% |
| 3,000 images | 85-90% |
| 7,500+ images | 90-95% |

---

## 🔧 Troubleshooting

### Common Issues

**TensorFlow not installed**
```bash
pip install tensorflow
```

**Dataset not found**
```bash
python download_dataset.py
```

**Model not found (demo mode)**
- Normal! App works without model
- Train with: `python train_model.py`

**Training too slow**
- Use GPU / Reduce epochs / Smaller batch

**Low accuracy**
- Add more images (100+/class)
- Check image quality
- Balance dataset
- Enable fine-tuning

**Full diagnostics:**
```bash
python check_system.py
```

---

## 📖 Resources

### Datasets
- [PlantVillage](https://www.kaggle.com/datasets/emmarex/plantdisease) - 54K images
- [Plant Pathology](https://www.kaggle.com/c/plant-pathology-2021-fgvc8) - Kaggle competition

### Documentation
- [Transfer Learning](https://www.tensorflow.org/tutorials/images/transfer_learning)
- [MobileNetV2 Paper](https://arxiv.org/abs/1801.04381)

---

## 🚀 Deployment

### Local
```bash
python app.py
```

### Production

**Heroku:**
```bash
# Procfile
web: gunicorn app:app

# Deploy
heroku create your-app-name
git push heroku main
```

**Docker:**
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

---

## 👥 Team

**Đội thi**: [Your Team Name]  
**Thành viên**: [Team Members]  
**Mục tiêu**: Hỗ trợ nông dân phát hiện sớm bệnh cây trồng, giảm thiệt hại mùa màng 🌾

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- PlantVillage Dataset
- TensorFlow & Keras teams
- Flask framework
- Vietnamese agricultural community

---

**Made with ❤️ for AI Challenge 2025**

🌱 **Happy Farming!** 🚜

