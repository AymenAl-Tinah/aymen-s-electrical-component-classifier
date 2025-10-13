/**
 * Electrical Component Classifier - Professional JavaScript
 * Handles all client-side interactions, animations, and API communication
 */

class ElectricalComponentClassifier {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.initializeApp();
    }

    initializeElements() {
        // Core elements
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.selectFileBtn = document.getElementById('selectFileBtn');
        this.predictBtn = document.getElementById('predictBtn');
        this.predictSpinner = document.getElementById('predictSpinner');
        
        // Sections
        this.previewSection = document.getElementById('previewSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        
        // Preview elements
        this.previewImage = document.getElementById('previewImage');
        this.fileName = document.getElementById('fileName');
        this.fileSize = document.getElementById('fileSize');
        this.removeImageBtn = document.getElementById('removeImageBtn');
        
        // Results elements
        this.predictedClassName = document.getElementById('predictedClassName');
        this.predictedClassDescription = document.getElementById('predictedClassDescription');
        this.confidenceValue = document.getElementById('confidenceValue');
        this.confidenceBadge = document.getElementById('confidenceBadge');
        this.predictionsList = document.getElementById('predictionsList');
        
        // Action buttons
        this.classifyAnotherBtn = document.getElementById('classifyAnotherBtn');
        this.downloadResultsBtn = document.getElementById('downloadResultsBtn');
        this.retryBtn = document.getElementById('retryBtn');
        
        // Loading and notifications
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.toastContainer = document.getElementById('toastContainer');
        
        // Current state
        this.currentFile = null;
        this.currentResults = null;
    }

    bindEvents() {
        // File selection events
        this.selectFileBtn.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Upload area events
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Prediction events
        this.predictBtn.addEventListener('click', () => this.handlePrediction());
        this.removeImageBtn.addEventListener('click', () => this.removeImage());
        this.classifyAnotherBtn.addEventListener('click', () => this.resetApp());
        this.retryBtn.addEventListener('click', () => this.handlePrediction());
        
        // Download results
        this.downloadResultsBtn.addEventListener('click', () => this.downloadResults());
        
        // Prevent default drag behaviors
        document.addEventListener('dragover', (e) => e.preventDefault());
        document.addEventListener('drop', (e) => e.preventDefault());
    }

    initializeApp() {
        this.showToast('Welcome to Electrical Component Classifier!', 'success');
        this.animateOnScroll();
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    handleDragOver(event) {
        event.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave(event) {
        event.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(event) {
        event.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    processFile(file) {
        // Validate file
        if (!this.validateFile(file)) {
            return;
        }

        this.currentFile = file;
        this.displayPreview(file);
        this.predictBtn.disabled = false;
        this.predictBtn.classList.add('pulse');
        
        this.showToast('File ready for classification!', 'success');
    }

    validateFile(file) {
        const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp', 'image/tiff', 'image/webp'];
        const maxSize = 16 * 1024 * 1024; // 16MB

        if (!allowedTypes.includes(file.type)) {
            this.showToast('Invalid file type. Please upload an image file.', 'error');
            return false;
        }

        if (file.size > maxSize) {
            this.showToast('File too large. Maximum size is 16MB.', 'error');
            return false;
        }

        return true;
    }

    displayPreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            this.previewImage.src = e.target.result;
            this.fileName.textContent = file.name;
            this.fileSize.textContent = this.formatFileSize(file.size);
            
            this.previewSection.style.display = 'block';
            this.previewSection.classList.add('fade-in');
            
            // Hide other sections
            this.resultsSection.style.display = 'none';
            this.errorSection.style.display = 'none';
        };
        reader.readAsDataURL(file);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async handlePrediction() {
        if (!this.currentFile) {
            this.showToast('Please select a file first.', 'warning');
            return;
        }

        this.showLoading();
        this.predictBtn.disabled = true;

        try {
            const formData = new FormData();
            formData.append('file', this.currentFile);

            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                this.displayResults(result);
                this.showToast('Classification completed successfully!', 'success');
            } else {
                this.displayError(result.error);
                this.showToast('Classification failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Prediction error:', error);
            this.displayError('Network error. Please check your connection and try again.');
            this.showToast('Network error occurred.', 'error');
        } finally {
            this.hideLoading();
            this.predictBtn.disabled = false;
        }
    }

    displayResults(result) {
        this.currentResults = result;
        
        // Update main prediction
        this.predictedClassName.textContent = result.class_name;
        this.predictedClassDescription.textContent = 'Electrical Component';
        this.confidenceValue.textContent = `${(result.confidence * 100).toFixed(1)}%`;
        
        // Update confidence badge color based on confidence level
        this.updateConfidenceBadge(result.confidence);
        
        // Display top predictions
        this.displayTopPredictions(result.probabilities);
        
        // Show results section
        this.resultsSection.style.display = 'block';
        this.resultsSection.classList.add('fade-in');
        
        // Hide other sections
        this.previewSection.style.display = 'none';
        this.errorSection.style.display = 'none';
    }

    updateConfidenceBadge(confidence) {
        this.confidenceBadge.className = 'confidence-badge';
        
        if (confidence >= 0.9) {
            this.confidenceBadge.style.background = '#10b981'; // Green
        } else if (confidence >= 0.7) {
            this.confidenceBadge.style.background = '#f59e0b'; // Orange
        } else {
            this.confidenceBadge.style.background = '#ef4444'; // Red
        }
    }

    displayTopPredictions(probabilities) {
        this.predictionsList.innerHTML = '';
        
        Object.entries(probabilities).forEach(([className, probability], index) => {
            const predictionItem = document.createElement('div');
            predictionItem.className = 'prediction-item';
            predictionItem.style.animationDelay = `${index * 0.1}s`;
            
            predictionItem.innerHTML = `
                <span class="class-name">${className}</span>
                <span class="confidence">${(probability * 100).toFixed(1)}%</span>
            `;
            
            this.predictionsList.appendChild(predictionItem);
        });
    }

    displayError(errorMessage) {
        const errorMessageElement = document.getElementById('errorMessage');
        errorMessageElement.textContent = errorMessage;
        
        this.errorSection.style.display = 'block';
        this.errorSection.classList.add('fade-in');
        
        // Hide other sections
        this.resultsSection.style.display = 'none';
    }

    removeImage() {
        this.currentFile = null;
        this.fileInput.value = '';
        this.predictBtn.disabled = true;
        this.predictBtn.classList.remove('pulse');
        
        this.previewSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
        this.errorSection.style.display = 'none';
        
        this.showToast('Image removed', 'success');
    }

    resetApp() {
        this.removeImage();
        this.currentResults = null;
        this.showToast('Ready for new classification', 'success');
    }

    downloadResults() {
        if (!this.currentResults) {
            this.showToast('No results to download', 'warning');
            return;
        }

        const results = {
            timestamp: new Date().toISOString(),
            filename: this.currentResults.original_filename,
            prediction: {
                class_name: this.currentResults.class_name,
                confidence: this.currentResults.confidence
            },
            top_predictions: this.currentResults.probabilities
        };

        const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `classification_results_${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showToast('Results downloaded successfully!', 'success');
    }

    showLoading() {
        this.loadingOverlay.classList.add('show');
    }

    hideLoading() {
        this.loadingOverlay.classList.remove('show');
    }

    showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem; color: #f8fafc;">
                <i class="fas ${this.getToastIcon(type)}" style="color: ${this.getToastIconColor(type)};"></i>
                <span style="color: #f8fafc;">${message}</span>
            </div>
        `;
        
        this.toastContainer.appendChild(toast);
        
        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Auto remove
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 4000);
    }

    getToastIcon(type) {
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        return icons[type] || icons.info;
    }

    getToastIconColor(type) {
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#3b82f6'
        };
        return colors[type] || colors.info;
    }

    animateOnScroll() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Observe cards for animation
        const cards = document.querySelectorAll('.upload-card, .preview-card, .results-card, .error-card');
        cards.forEach(card => observer.observe(card));
    }
}

// Utility functions
const utils = {
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.classifier = new ElectricalComponentClassifier();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden, pause any ongoing animations
        document.body.classList.add('paused');
    } else {
        // Page is visible, resume animations
        document.body.classList.remove('paused');
    }
});

// Handle online/offline status
window.addEventListener('online', () => {
    window.classifier?.showToast('Connection restored', 'success');
});

window.addEventListener('offline', () => {
    window.classifier?.showToast('Connection lost', 'warning');
});

// Handle errors
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    if (window.classifier) {
        window.classifier.showToast('An unexpected error occurred', 'error');
    }
});

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    if (window.classifier) {
        window.classifier.showToast('A network error occurred', 'error');
    }
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ElectricalComponentClassifier;
}
