// Main JavaScript for Plant Disease Detection App

let webcamStream = null;
let currentImageData = null;

// DOM Elements
const fileInput = document.getElementById('fileInput');
const fileUploadArea = document.getElementById('fileUploadArea');
const previewSection = document.getElementById('previewSection');
const previewImage = document.getElementById('previewImage');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsSection = document.getElementById('resultsSection');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');

// Webcam elements
const webcam = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const startWebcamBtn = document.getElementById('startWebcamBtn');
const captureBtn = document.getElementById('captureBtn');
const stopWebcamBtn = document.getElementById('stopWebcamBtn');

// History
const historyList = document.getElementById('historyList');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');

// ===== FILE UPLOAD =====

// Drag and drop handlers
fileUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUploadArea.classList.add('dragover');
});

fileUploadArea.addEventListener('dragleave', () => {
    fileUploadArea.classList.remove('dragover');
});

fileUploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
        alert('Vui lòng chọn file ảnh (PNG, JPG, JPEG)');
        return;
    }
    
    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        alert('File quá lớn. Kích thước tối đa là 16MB');
        return;
    }
    
    // Store file for upload
    currentImageData = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewSection.hidden = false;
        resultsSection.hidden = true;
    };
    reader.readAsDataURL(file);
}

// ===== WEBCAM =====

startWebcamBtn.addEventListener('click', async () => {
    try {
        webcamStream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'environment' } 
        });
        webcam.srcObject = webcamStream;
        webcam.hidden = false;
        
        startWebcamBtn.disabled = true;
        captureBtn.disabled = false;
        stopWebcamBtn.disabled = false;
    } catch (error) {
        console.error('Error accessing webcam:', error);
        alert('Không thể truy cập webcam. Vui lòng kiểm tra quyền truy cập.');
    }
});

captureBtn.addEventListener('click', () => {
    // Set canvas size to match video
    canvas.width = webcam.videoWidth;
    canvas.height = webcam.videoHeight;
    
    // Draw current frame to canvas
    const ctx = canvas.getContext('2d');
    ctx.drawImage(webcam, 0, 0);
    
    // Get image as base64
    const imageDataUrl = canvas.toDataURL('image/jpeg');
    currentImageData = imageDataUrl;
    
    // Show preview
    previewImage.src = imageDataUrl;
    previewSection.hidden = false;
    resultsSection.hidden = true;
    
    // Stop webcam
    stopWebcam();
});

stopWebcamBtn.addEventListener('click', stopWebcam);

function stopWebcam() {
    if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
        webcamStream = null;
        webcam.srcObject = null;
        webcam.hidden = true;
        
        startWebcamBtn.disabled = false;
        captureBtn.disabled = true;
        stopWebcamBtn.disabled = true;
    }
}

// ===== ANALYZE IMAGE =====

analyzeBtn.addEventListener('click', async () => {
    if (!currentImageData) {
        alert('Vui lòng chọn ảnh trước');
        return;
    }
    
    // Show loading
    loadingIndicator.hidden = false;
    previewSection.hidden = true;
    resultsSection.hidden = true;
    
    try {
        let response;
        
        if (typeof currentImageData === 'string') {
            // Webcam base64 data
            response = await fetch('/api/predict/webcam', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image: currentImageData })
            });
        } else {
            // File upload
            const formData = new FormData();
            formData.append('file', currentImageData);
            
            response = await fetch('/api/predict/upload', {
                method: 'POST',
                body: formData
            });
        }
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Prediction failed');
        }
        
        const result = await response.json();
        displayResults(result);
        loadHistory();
        
    } catch (error) {
        console.error('Error:', error);
        alert('Lỗi khi phân tích ảnh: ' + error.message);
    } finally {
        loadingIndicator.hidden = true;
    }
});

// ===== DISPLAY RESULTS =====

function displayResults(result) {
    // Show results section
    resultsSection.hidden = false;
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Display image
    document.getElementById('resultImage').src = result.image_url;
    
    // Main prediction
    const topPrediction = result.top_prediction;
    document.getElementById('diseaseName').textContent = topPrediction.class;
    
    // Update circular progress
    const confidenceValue = topPrediction.confidence;
    const circle = document.getElementById('confidenceCircle');
    const text = document.getElementById('confidenceText');
    
    circle.style.strokeDasharray = `${confidenceValue}, 100`;
    text.textContent = confidenceValue.toFixed(1) + '%';
    
    // Severity indicator
    const severityIndicator = document.getElementById('severityIndicator');
    const severity = result.treatment.severity;
    const severityText = {
        'none': '✅ Lá khỏe mạnh',
        'low': '🟢 Mức độ nhẹ',
        'medium': '🟡 Trung bình',
        'high': '🔴 Nghiêm trọng',
        'unknown': '⚪ Chưa xác định'
    };
    severityIndicator.textContent = severityText[severity] || severityText['unknown'];
    severityIndicator.className = 'severity-badge ' + severity;
    
    // Top 3 predictions
    displayTop3Predictions(result.all_predictions);
    
    // Chart
    displayConfidenceChart(result.all_predictions);
    
    // Treatment info
    displayTreatment(result.treatment);
}

function displayTop3Predictions(predictions) {
    const container = document.getElementById('top3Predictions');
    container.innerHTML = '';
    
    predictions.forEach((pred, index) => {
        const item = document.createElement('div');
        item.className = 'prediction-item';
        item.innerHTML = `
            <div class="prediction-rank">#${index + 1}</div>
            <div class="prediction-details">
                <div class="prediction-name">${pred.class}</div>
                <div class="prediction-bar">
                    <div class="prediction-fill" style="width: ${pred.confidence}%"></div>
                </div>
                <div class="prediction-confidence">${pred.confidence.toFixed(1)}%</div>
            </div>
        `;
        container.appendChild(item);
    });
}

function displayTreatment(treatment) {
    document.getElementById('diagnosis').textContent = treatment.diagnosis;
    document.getElementById('treatment').textContent = treatment.treatment;
    
    const preventionList = document.getElementById('preventionList');
    preventionList.innerHTML = '';
    
    treatment.prevention.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        preventionList.appendChild(li);
    });
}

// ===== NEW ANALYSIS =====

newAnalysisBtn.addEventListener('click', () => {
    currentImageData = null;
    previewSection.hidden = true;
    resultsSection.hidden = true;
    previewImage.src = '';
    fileInput.value = '';
});

// ===== HISTORY =====

async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        displayHistory(data.history);
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function displayHistory(history) {
    if (!history || history.length === 0) {
        historyList.innerHTML = '<p class="empty-message">Chưa có lịch sử dự đoán</p>';
        return;
    }
    
    historyList.innerHTML = '';
    
    history.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
            <img src="${item.image_url}" alt="${item.disease}">
            <div class="history-info">
                <div class="history-disease">${item.disease}</div>
                <div class="history-confidence">${item.confidence.toFixed(1)}%</div>
                <div class="history-time">${item.timestamp}</div>
            </div>
        `;
        historyList.appendChild(historyItem);
    });
}

clearHistoryBtn.addEventListener('click', async () => {
    if (!confirm('Bạn có chắc muốn xóa toàn bộ lịch sử?')) {
        return;
    }
    
    try {
        await fetch('/api/clear-history', { method: 'POST' });
        loadHistory();
    } catch (error) {
        console.error('Error clearing history:', error);
    }
});

// Load history on page load
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
});
