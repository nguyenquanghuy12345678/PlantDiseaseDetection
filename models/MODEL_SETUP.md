# Model Setup Instructions

## Cách lấy/train model cho ứng dụng

### Option 1: Download Pre-trained Model (Khuyến nghị)

1. **PlantVillage Dataset Model**
   - Dataset: https://www.kaggle.com/datasets/emmarex/plantdisease
   - Pre-trained models: https://www.kaggle.com/models
   - Download model file `.h5` hoặc `.keras`
   - Đặt vào folder `models/disease_model.h5`

2. **TensorFlow Hub Models**
   ```python
   import tensorflow_hub as hub
   model = hub.load("https://tfhub.dev/...")
   # Export to .h5 format
   ```

### Option 2: Train Model của bạn

#### Bước 1: Chuẩn bị Dataset
```
data/
├── train/
│   ├── Lá khỏe mạnh/
│   ├── Bệnh đốm lá/
│   ├── Bệnh héo xanh/
│   └── ...
└── validation/
    ├── Lá khỏe mạnh/
    └── ...
```

#### Bước 2: Train Model (Example Code)

```python
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2
)

val_datagen = ImageDataGenerator(rescale=1./255)

# Load data
train_generator = train_datagen.flow_from_directory(
    'data/train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    'data/validation',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Build model with transfer learning
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False  # Freeze base model

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Compile
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(
    train_generator,
    epochs=20,
    validation_data=val_generator
)

# Save model
model.save('models/disease_model.h5')

# Save class indices
import json
class_indices = train_generator.class_indices
with open('models/class_indices.json', 'w', encoding='utf-8') as f:
    json.dump(class_indices, f, ensure_ascii=False, indent=2)
```

#### Bước 3: Fine-tune (Optional)
```python
# Unfreeze some layers and train with lower learning rate
base_model.trainable = True
for layer in base_model.layers[:-20]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    train_generator,
    epochs=10,
    validation_data=val_generator
)

model.save('models/disease_model_finetuned.h5')
```

### Option 3: Use Dummy Model for Testing

Ứng dụng đã có sẵn dummy predictions nếu không có model. Để test:
1. Không cần đặt file model
2. Chạy app, sẽ có warning nhưng vẫn chạy được
3. Predictions sẽ là random (cho mục đích demo UI)

### Class Indices Format

File `class_indices.json` phải có format:
```json
{
  "Class Name 1": 0,
  "Class Name 2": 1,
  ...
}
```

Hoặc ngược lại:
```json
{
  "0": "Class Name 1",
  "1": "Class Name 2",
  ...
}
```

### Recommended Datasets

1. **PlantVillage** (38 classes)
   - https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
   - 54,000+ images
   - Multiple crops: tomato, potato, corn, etc.

2. **Plant Disease Recognition** (KAIST)
   - https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset
   - 87,000+ images
   - 38 classes

3. **Custom Vietnamese Crops**
   - Collect local crop images
   - Focus on Vietnam-specific diseases
   - More relevant for local farmers

### Model Requirements

- Input shape: (224, 224, 3) RGB images
- Output: Softmax probabilities for each class
- Format: `.h5` (Keras) or `.keras` (TensorFlow 2.x)
- Size: Khuyến nghị < 100MB để deploy dễ

### Test Model

```python
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Load model
model = load_model('models/disease_model.h5')

# Load and preprocess test image
img = Image.open('test_image.jpg').resize((224, 224))
img_array = np.array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
predictions = model.predict(img_array)
print(f"Predictions: {predictions}")
print(f"Top class: {np.argmax(predictions)}")
print(f"Confidence: {np.max(predictions) * 100:.2f}%")
```

### Troubleshooting

**Lỗi: Model file not found**
- Đảm bảo file model ở đúng path: `models/disease_model.h5`
- Check quyền truy cập file

**Lỗi: Class indices mismatch**
- Số classes trong model phải khớp với `class_indices.json`
- Check output layer của model

**Lỗi: Out of memory**
- Reduce batch size khi train
- Use model quantization
- Resize images nhỏ hơn

**Model accuracy thấp**
- Tăng số epoch
- Data augmentation nhiều hơn
- Fine-tune base model
- Thử architecture khác (ResNet, EfficientNet)
