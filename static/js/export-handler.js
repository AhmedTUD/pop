/**
 * Export Handler with Live Toast Notifications
 * Handles Excel export operations with real-time feedback
 */

class ExportHandler {
    constructor() {
        this.activeExports = new Map();
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.setupExportButtons();
        });
    }

    setupExportButtons() {
        // Find all export buttons
        const exportButtons = document.querySelectorAll('a[href*="export_excel"]');
        
        exportButtons.forEach(button => {
            // Convert to button element for better control
            const newButton = document.createElement('button');
            newButton.className = button.className;
            newButton.title = button.title;
            newButton.innerHTML = button.innerHTML;
            
            // Store original URL and determine export type
            const originalUrl = button.href;
            const isSimple = originalUrl.includes('export_excel_simple');
            
            // Add click handler
            newButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleExport(originalUrl, isSimple);
            });
            
            // Replace original link
            button.parentNode.replaceChild(newButton, button);
        });
    }

    async handleExport(url, isSimple = false) {
        const exportType = isSimple ? 'البسيط' : 'المحسن (مع الصور)';
        const exportId = `export-${Date.now()}`;
        
        // Show loading toast
        const loadingToastId = window.toastSystem.loading(
            `جاري تصدير التقرير ${exportType}...`,
            'يرجى الانتظار حتى اكتمال العملية',
            { id: exportId }
        );

        try {
            // Make the export request
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            // Check if response is actually an Excel file
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('spreadsheet')) {
                // If not Excel, it might be a redirect to dashboard with error
                const text = await response.text();
                if (text.includes('لا توجد بيانات للتصدير')) {
                    throw new Error('لا توجد بيانات للتصدير مع الفلاتر المحددة');
                } else {
                    throw new Error('فشل في إنشاء ملف Excel');
                }
            }

            // Get the blob for download
            const blob = await response.blob();
            
            if (blob.size === 0) {
                throw new Error('الملف المُنشأ فارغ');
            }

            // Extract filename from response headers or create default
            let filename = 'pop_materials_report.xlsx';
            const contentDisposition = response.headers.get('content-disposition');
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                if (filenameMatch && filenameMatch[1]) {
                    filename = filenameMatch[1].replace(/['"]/g, '');
                }
            } else {
                // Create filename based on export type and timestamp
                const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '');
                filename = isSimple 
                    ? `pop_materials_simple_${timestamp}.xlsx`
                    : `pop_materials_enhanced_${timestamp}.xlsx`;
            }

            // Download the file
            this.downloadBlob(blob, filename);

            // Update toast to success
            window.toastSystem.update(exportId, {
                type: 'success',
                title: isSimple ? 'تم إنشاء التقرير بنجاح!' : 'تم إنشاء التقرير المحسن بنجاح!',
                message: `تم تحميل الملف: ${filename}`
            });

            // Auto-hide success toast after 4 seconds
            setTimeout(() => {
                window.toastSystem.hide(exportId);
            }, 4000);

        } catch (error) {
            console.error('Export error:', error);
            
            // Update toast to error
            window.toastSystem.update(exportId, {
                type: 'error',
                title: 'فشل في تصدير التقرير',
                message: error.message || 'حدث خطأ غير متوقع أثناء التصدير'
            });

            // Auto-hide error toast after 6 seconds
            setTimeout(() => {
                window.toastSystem.hide(exportId);
            }, 6000);
        }
    }

    downloadBlob(blob, filename) {
        try {
            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = filename;
            
            // Add to DOM and trigger download
            document.body.appendChild(a);
            a.click();
            
            // Cleanup
            setTimeout(() => {
                window.URL.revokeObjectURL(url);
                if (a.parentNode) {
                    a.parentNode.removeChild(a);
                }
            }, 100);

        } catch (error) {
            console.error('Download error:', error);
            throw new Error('فشل في تحميل الملف');
        }
    }

    // Method to handle export with filters (for programmatic use)
    async exportWithFilters(isSimple = false, filters = {}) {
        const baseUrl = isSimple ? '/export_excel_simple' : '/export_excel';
        const params = new URLSearchParams();
        
        // Add filters to URL
        Object.keys(filters).forEach(key => {
            if (filters[key]) {
                params.append(key, filters[key]);
            }
        });
        
        const url = params.toString() ? `${baseUrl}?${params.toString()}` : baseUrl;
        return this.handleExport(url, isSimple);
    }

    // Method to get current filters from the page
    getCurrentFilters() {
        const filters = {};
        
        // Get filter values from form elements
        const employeeSelect = document.getElementById('employee');
        const branchSelect = document.getElementById('branch');
        const modelSelect = document.getElementById('model');
        const dateFromInput = document.getElementById('date_from');
        const dateToInput = document.getElementById('date_to');
        
        if (employeeSelect && employeeSelect.value) {
            filters.employee = employeeSelect.value;
        }
        if (branchSelect && branchSelect.value) {
            filters.branch = branchSelect.value;
        }
        if (modelSelect && modelSelect.value) {
            filters.model = modelSelect.value;
        }
        if (dateFromInput && dateFromInput.value) {
            filters.date_from = dateFromInput.value;
        }
        if (dateToInput && dateToInput.value) {
            filters.date_to = dateToInput.value;
        }
        
        return filters;
    }
}

// Initialize export handler
window.exportHandler = new ExportHandler();

// Expose methods for global use
window.exportExcel = (isSimple = false) => {
    const filters = window.exportHandler.getCurrentFilters();
    return window.exportHandler.exportWithFilters(isSimple, filters);
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ExportHandler;
}