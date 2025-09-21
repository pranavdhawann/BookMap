// BookMap Web Application JavaScript

let currentSessionId = null;
let statusCheckInterval = null;
let isProcessing = false;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadButton');
const filePreview = document.getElementById('filePreview');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const processBtn = document.getElementById('processBtn');
const progressSection = document.getElementById('progressSection');
const progressBar = document.getElementById('progressBar');
const progressMessage = document.getElementById('progressMessage');
const progressPercent = document.getElementById('progressPercent');
const resultsSection = document.getElementById('resultsSection');
const indexTableBody = document.getElementById('indexTableBody');
const errorAlert = document.getElementById('errorAlert');
const errorMessage = document.getElementById('errorMessage');
const successAlert = document.getElementById('successAlert');
const successMessage = document.getElementById('successMessage');
const downloadDropdown = document.getElementById('downloadDropdown');
const downloadJson = document.getElementById('downloadJson');
const downloadCsv = document.getElementById('downloadCsv');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    // File input change
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
    
    // Drag and drop
    if (uploadArea) {
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('dragleave', handleDragLeave);
        uploadArea.addEventListener('drop', handleDrop);
    }
    
    // FIXED: Only the upload button triggers file input
    const button = uploadButton || document.querySelector('#uploadButton') || document.querySelector('button[class*="btn-primary"]');
    if (button) {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (fileInput) {
                fileInput.click();
            }
        });
    }
    
    // Process button
    if (processBtn) {
        processBtn.addEventListener('click', processFile);
    }
    
    // Download buttons
    if (downloadJson) {
        downloadJson.addEventListener('click', () => downloadIndex('json'));
    }
    if (downloadCsv) {
        downloadCsv.addEventListener('click', () => downloadIndex('csv'));
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    // Validate file type
    if (file.type !== 'application/pdf') {
        showError('Please select a PDF file.');
        return;
    }
    
    // Validate file size (50MB)
    if (file.size > 50 * 1024 * 1024) {
        showError('File size must be less than 50MB.');
        return;
    }
    
    // Show file preview
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    uploadArea.style.display = 'none';
    filePreview.style.display = 'block';
    
    // Store file for processing
    window.selectedFile = file;
}

function clearFile() {
    fileInput.value = '';
    window.selectedFile = null;
    uploadArea.style.display = 'block';
    filePreview.style.display = 'none';
    hideAllSections();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function processFile() {
    if (isProcessing) {
        return; // Prevent double processing
    }
    
    if (!window.selectedFile) {
        showError('Please select a file first.');
        return;
    }
    
    isProcessing = true;
    
    try {
        // Show progress section
        hideAllSections();
        progressSection.style.display = 'block';
        
        // Upload file
        const formData = new FormData();
        formData.append('file', window.selectedFile);
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Upload failed');
        }
        
        currentSessionId = result.session_id;
        startStatusCheck();
        
    } catch (error) {
        showError('Upload failed: ' + error.message);
        hideAllSections();
        isProcessing = false;
    }
}

function startStatusCheck() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }
    
    statusCheckInterval = setInterval(checkStatus, 1000);
}

async function checkStatus() {
    if (!currentSessionId) return;
    
    try {
        const response = await fetch(`/status/${currentSessionId}`);
        const status = await response.json();
        
        if (!response.ok) {
            throw new Error(status.error || 'Status check failed');
        }
        
        updateProgress(status);
        
        if (status.status === 'completed') {
            clearInterval(statusCheckInterval);
            isProcessing = false;
            await loadResults();
        } else if (status.status === 'error') {
            clearInterval(statusCheckInterval);
            isProcessing = false;
            showError(status.message);
            hideAllSections();
        }
        
    } catch (error) {
        clearInterval(statusCheckInterval);
        isProcessing = false;
        showError('Status check failed: ' + error.message);
        hideAllSections();
    }
}

function updateProgress(status) {
    progressBar.style.width = status.progress + '%';
    progressPercent.textContent = status.progress + '%';
    progressMessage.textContent = status.message;
}

async function loadResults() {
    try {
        const response = await fetch(`/index/${currentSessionId}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to load results');
        }
        
        displayResults(data);
        showSuccess('Document processed successfully!');
        
    } catch (error) {
        showError('Failed to load results: ' + error.message);
    }
}

function displayResults(data) {
    hideAllSections();
    resultsSection.style.display = 'block';
    downloadDropdown.style.display = 'block';
    
    // Clear existing table content
    indexTableBody.innerHTML = '';
    
    // Populate table
    data.index.forEach((item, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="fw-bold text-primary">${item.page}</td>
            <td>${item.title}</td>
            <td class="text-center">
                <button class="btn btn-outline-primary btn-sm" onclick="jumpToPage(${item.page})">
                    <i class="fas fa-eye me-1"></i>View
                </button>
            </td>
        `;
        indexTableBody.appendChild(row);
    });
    
    // Add summary
    const summaryRow = document.createElement('tr');
    summaryRow.className = 'table-info';
    summaryRow.innerHTML = `
        <td colspan="3" class="text-center fw-bold">
            <i class="fas fa-info-circle me-2"></i>
            Found ${data.index.length} sections across ${data.num_pages} pages
        </td>
    `;
    indexTableBody.appendChild(summaryRow);
}

function jumpToPage(pageNumber) {
    // Add visual feedback
    const button = event.target.closest('button');
    button.classList.add('page-jump');
    
    setTimeout(() => {
        button.classList.remove('page-jump');
    }, 600);
    
    // Create a PDF viewer modal
    showPDFViewer(pageNumber);
}

function showPDFViewer(pageNumber) {
    // Create modal HTML
    const modalHTML = `
        <div class="modal fade" id="pdfViewerModal" tabindex="-1" aria-labelledby="pdfViewerModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="pdfViewerModalLabel">
                            <i class="fas fa-file-pdf me-2"></i>PDF Viewer - Page ${pageNumber}
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="text-center">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <p class="mt-2">Loading page ${pageNumber}...</p>
                        </div>
                        <div id="pdfContent" style="display: none;">
                            <div class="pdf-page-container">
                                <img id="pdfPageImage" class="img-fluid" alt="PDF Page ${pageNumber}">
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" onclick="downloadPageImage(${pageNumber})">
                            <i class="fas fa-download me-1"></i>Download Page
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('pdfViewerModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('pdfViewerModal'));
    modal.show();
    
    // Load the page image
    loadPageImage(pageNumber);
}

async function loadPageImage(pageNumber) {
    try {
        // Get the processed image from the server
        const response = await fetch(`/get-page-image/${currentSessionId}/${pageNumber}`);
        
        if (response.ok) {
            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);
            
            const pdfImage = document.getElementById('pdfPageImage');
            const pdfContent = document.getElementById('pdfContent');
            const loadingDiv = pdfContent.previousElementSibling;
            
            pdfImage.src = imageUrl;
            pdfImage.onload = () => {
                loadingDiv.style.display = 'none';
                pdfContent.style.display = 'block';
            };
        } else {
            throw new Error('Failed to load page image');
        }
    } catch (error) {
        console.error('Error loading page image:', error);
        const loadingDiv = document.querySelector('#pdfViewerModal .spinner-border').parentElement;
        loadingDiv.innerHTML = `
            <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Could not load page image. The page may not be available.
            </div>
        `;
    }
}

function downloadPageImage(pageNumber) {
    const pdfImage = document.getElementById('pdfPageImage');
    if (pdfImage && pdfImage.src) {
        const link = document.createElement('a');
        link.href = pdfImage.src;
        link.download = `page_${pageNumber}.jpg`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

async function downloadIndex(format) {
    if (!currentSessionId) {
        showError('No index available for download.');
        return;
    }
    
    try {
        const response = await fetch(`/download/${currentSessionId}/${format}`);
        
        if (!response.ok) {
            throw new Error('Download failed');
        }
        
        // Create download link
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `index_${currentSessionId}.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showSuccess(`Index downloaded as ${format.toUpperCase()}`);
        
    } catch (error) {
        showError('Download failed: ' + error.message);
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorAlert.style.display = 'block';
    errorAlert.classList.add('show');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorAlert.classList.remove('show');
    setTimeout(() => {
        errorAlert.style.display = 'none';
    }, 300);
}

function showSuccess(message) {
    successMessage.textContent = message;
    successAlert.style.display = 'block';
    successAlert.classList.add('show');
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        hideSuccess();
    }, 3000);
}

function hideSuccess() {
    successAlert.classList.remove('show');
    setTimeout(() => {
        successAlert.style.display = 'none';
    }, 300);
}

function hideAllSections() {
    progressSection.style.display = 'none';
    resultsSection.style.display = 'none';
    downloadDropdown.style.display = 'none';
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add smooth scrolling for better UX
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading states to buttons
function setButtonLoading(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.innerHTML = '<span class="loading-spinner me-2"></span>Processing...';
    } else {
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-magic me-2"></i>Generate Index';
    }
}

// Handle window resize for responsive design
window.addEventListener('resize', debounce(() => {
    // Adjust layout if needed
}, 250));

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + O to open file
    if ((e.ctrlKey || e.metaKey) && e.key === 'o') {
        e.preventDefault();
        fileInput.click();
    }
    
    // Escape to clear file
    if (e.key === 'Escape') {
        clearFile();
    }
});

// Add tooltips for better UX
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Performance monitoring
function logPerformance(label, startTime) {
    const endTime = performance.now();
    console.log(`${label}: ${endTime - startTime} milliseconds`);
}

// Error handling for unhandled promises
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    showError('An unexpected error occurred. Please try again.');
});
