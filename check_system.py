"""
Quick demo to test dataset structure and training readiness
"""

import os
from pathlib import Path

def check_environment():
    """Check if environment is ready"""
    print("🔍 Checking environment...")
    
    # Check Python packages
    packages = {
        'flask': False,
        'numpy': False,
        'PIL': False,
        'tensorflow': False,
        'matplotlib': False,
    }
    
    for package in packages.keys():
        try:
            if package == 'PIL':
                __import__('PIL')
            else:
                __import__(package)
            packages[package] = True
        except ImportError:
            pass
    
    print("\n📦 Package Status:")
    print("-" * 50)
    for package, installed in packages.items():
        status = "✅" if installed else "❌"
        note = ""
        if not installed:
            if package == 'tensorflow':
                note = " (optional - needed for training)"
            elif package == 'matplotlib':
                note = " (optional - for visualization)"
            else:
                note = " (required - install: pip install -r requirements.txt)"
        print(f"{status} {package}{note}")
    
    return packages

def check_project_structure():
    """Check project file structure"""
    print("\n\n📁 Checking project structure...")
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'templates/index.html',
        'static/css/style.css',
        'static/js/main.js',
        'utils/model_handler.py',
        'utils/preprocessing.py',
        'utils/treatment_data.py',
        'models/class_indices.json',
        'train_model.py',
        'download_dataset.py',
        'test_model.py',
    ]
    
    print("\n📄 Required Files:")
    print("-" * 50)
    all_exist = True
    for file_path in required_files:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}")
        if not exists:
            all_exist = False
    
    return all_exist

def check_dataset():
    """Check dataset structure"""
    print("\n\n🗂️ Checking dataset...")
    
    data_dir = Path('data/plant_diseases')
    
    if not data_dir.exists():
        print("❌ Dataset directory not found: data/plant_diseases/")
        print("\n💡 Run this to create structure:")
        print("   python download_dataset.py")
        return False
    
    # Count classes and images
    classes = [d for d in data_dir.iterdir() if d.is_dir()]
    
    print(f"\n📊 Dataset Statistics:")
    print("-" * 50)
    print(f"Classes found: {len(classes)}")
    
    if len(classes) == 0:
        print("\n⚠️  No disease classes found!")
        print("Please organize images into folders by disease name")
        return False
    
    total_images = 0
    for class_dir in classes:
        image_files = list(class_dir.glob('*.jpg')) + \
                     list(class_dir.glob('*.jpeg')) + \
                     list(class_dir.glob('*.png'))
        count = len(image_files)
        total_images += count
        
        status = "✅" if count >= 100 else "⚠️ " if count > 0 else "❌"
        print(f"{status} {class_dir.name}: {count} images")
    
    print("-" * 50)
    print(f"Total images: {total_images}")
    
    if total_images == 0:
        print("\n❌ No images found in dataset!")
        print("Please add images to the class folders")
        return False
    elif total_images < 500:
        print("\n⚠️  Dataset is small. Consider adding more images.")
        print("   Recommended: 500+ images total, 100+ per class")
        return True
    else:
        print("\n✅ Dataset looks good!")
        return True

def check_model():
    """Check if trained model exists"""
    print("\n\n🤖 Checking model...")
    
    model_path = Path('models/disease_model.h5')
    
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"✅ Model found: {model_path}")
        print(f"   Size: {size_mb:.2f} MB")
        return True
    else:
        print("❌ Model not found: models/disease_model.h5")
        print("\n💡 To train a model:")
        print("   1. Setup dataset: python download_dataset.py")
        print("   2. Add images to data/plant_diseases/<disease>/")
        print("   3. Train: python train_model.py")
        print("\n⚠️  App will run in DEMO MODE without model")
        return False

def show_next_steps(packages, dataset_ready, model_exists):
    """Show recommended next steps"""
    print("\n\n" + "=" * 70)
    print("📋 RECOMMENDED NEXT STEPS")
    print("=" * 70)
    
    steps = []
    
    # Check what needs to be done
    if not packages.get('flask') or not packages.get('numpy') or not packages.get('PIL'):
        steps.append({
            'num': len(steps) + 1,
            'title': 'Install required packages',
            'command': 'pip install -r requirements.txt',
            'priority': 'HIGH'
        })
    
    if not dataset_ready:
        steps.append({
            'num': len(steps) + 1,
            'title': 'Setup dataset structure',
            'command': 'python download_dataset.py',
            'priority': 'HIGH'
        })
    
    if dataset_ready and not model_exists:
        if not packages.get('tensorflow'):
            steps.append({
                'num': len(steps) + 1,
                'title': 'Install TensorFlow for training',
                'command': 'pip install tensorflow matplotlib',
                'priority': 'MEDIUM'
            })
        
        steps.append({
            'num': len(steps) + 1,
            'title': 'Train the model',
            'command': 'python train_model.py',
            'priority': 'MEDIUM'
        })
    
    if model_exists:
        steps.append({
            'num': len(steps) + 1,
            'title': 'Test model accuracy',
            'command': 'python test_model.py',
            'priority': 'LOW'
        })
    
    steps.append({
        'num': len(steps) + 1,
        'title': 'Run web application',
        'command': 'python app.py',
        'priority': 'MEDIUM'
    })
    
    # Display steps
    for step in steps:
        priority_icon = {
            'HIGH': '🔴',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }[step['priority']]
        
        print(f"\n{priority_icon} Step {step['num']}: {step['title']}")
        print(f"   Command: {step['command']}")

def main():
    print("=" * 70)
    print("🌱 PLANT DISEASE DETECTION - SYSTEM CHECK")
    print("=" * 70)
    
    # Run checks
    packages = check_environment()
    structure_ok = check_project_structure()
    dataset_ready = check_dataset()
    model_exists = check_model()
    
    # Summary
    print("\n\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    core_ready = packages.get('flask') and packages.get('numpy') and packages.get('PIL')
    train_ready = packages.get('tensorflow')
    
    print(f"{'✅' if core_ready else '❌'} Web app dependencies")
    print(f"{'✅' if train_ready else '⚠️ '} Training dependencies (TensorFlow)")
    print(f"{'✅' if structure_ok else '❌'} Project structure")
    print(f"{'✅' if dataset_ready else '⚠️ '} Dataset ready")
    print(f"{'✅' if model_exists else '⚠️ '} Trained model")
    
    if core_ready and structure_ok:
        print("\n✅ Web app can run! (demo mode if no model)")
    
    if train_ready and dataset_ready:
        print("✅ Ready to train model!")
    
    if model_exists:
        print("✅ Ready for production use!")
    
    # Show next steps
    show_next_steps(packages, dataset_ready, model_exists)
    
    print("\n" + "=" * 70)
    print("📚 Documentation:")
    print("   - QUICKSTART.md - Quick start guide")
    print("   - TRAINING_GUIDE.md - Model training guide")
    print("   - MODEL_IMPROVEMENTS.md - Complete feature list")
    print("=" * 70)

if __name__ == "__main__":
    main()
