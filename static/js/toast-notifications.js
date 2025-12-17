/**
 * Toast Notification System for Export Messages
 * Provides real-time feedback for export operations
 */

class ToastNotification {
    constructor() {
        this.container = null;
        this.activeToasts = new Map();
        this.init();
    }

    init() {
        // Create toast container
        this.container = document.createElement('div');
        this.container.id = 'toast-container';
        this.container.className = 'toast-container';
        document.body.appendChild(this.container);

        // Add CSS styles
        this.addStyles();
    }

    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .toast-container {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                pointer-events: none;
            }

            .toast {
                background: white;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
                margin-bottom: 12px;
                padding: 16px 20px;
                min-width: 320px;
                max-width: 450px;
                pointer-events: auto;
                transform: translateX(100%);
                opacity: 0;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                border-left: 4px solid #007bff;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                direction: rtl;
                text-align: right;
            }

            .toast.show {
                transform: translateX(0);
                opacity: 1;
            }

            .toast.hide {
                transform: translateX(100%);
                opacity: 0;
            }

            .toast-loading {
                border-left-color: #007bff;
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            }

            .toast-success {
                border-left-color: #28a745;
                background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            }

            .toast-error {
                border-left-color: #dc3545;
                background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            }

            .toast-warning {
                border-left-color: #ffc107;
                background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            }

            .toast-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 8px;
            }

            .toast-icon {
                font-size: 20px;
                margin-left: 12px;
                animation: pulse 2s infinite;
            }

            .toast-loading .toast-icon {
                animation: spin 1s linear infinite;
            }

            .toast-title {
                font-weight: 600;
                font-size: 14px;
                color: #2c3e50;
                flex: 1;
            }

            .toast-close {
                background: none;
                border: none;
                font-size: 18px;
                cursor: pointer;
                color: #6c757d;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: all 0.2s ease;
            }

            .toast-close:hover {
                background: rgba(0, 0, 0, 0.1);
                color: #495057;
            }

            .toast-message {
                font-size: 13px;
                color: #495057;
                line-height: 1.4;
                margin: 0;
            }

            .toast-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                height: 3px;
                background: rgba(0, 123, 255, 0.3);
                border-radius: 0 0 12px 12px;
                transition: width 0.1s ease;
            }

            .toast-progress-bar {
                height: 100%;
                background: #007bff;
                border-radius: 0 0 12px 12px;
                transition: width 0.1s ease;
            }

            .toast-success .toast-progress-bar {
                background: #28a745;
            }

            .toast-error .toast-progress-bar {
                background: #dc3545;
            }

            .toast-warning .toast-progress-bar {
                background: #ffc107;
            }

            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }

            @media (max-width: 480px) {
                .toast-container {
                    top: 10px;
                    right: 10px;
                    left: 10px;
                }

                .toast {
                    min-width: auto;
                    max-width: none;
                    margin-bottom: 8px;
                }
            }
        `;
        document.head.appendChild(style);
    }

    show(options) {
        const {
            type = 'info',
            title = '',
            message = '',
            duration = 5000,
            id = null,
            showProgress = true,
            closable = true
        } = options;

        // Remove existing toast with same ID
        if (id && this.activeToasts.has(id)) {
            this.hide(id);
        }

        // Create toast element
        const toast = document.createElement('div');
        const toastId = id || `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        toast.id = toastId;
        toast.className = `toast toast-${type}`;

        // Get icon based on type
        const icons = {
            loading: '⏳',
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };

        // Build toast HTML
        toast.innerHTML = `
            <div class="toast-header">
                <div class="toast-icon">${icons[type] || icons.info}</div>
                <div class="toast-title">${title}</div>
                ${closable ? '<button class="toast-close" onclick="window.toastSystem.hide(\'' + toastId + '\')">&times;</button>' : ''}
            </div>
            ${message ? `<div class="toast-message">${message}</div>` : ''}
            ${showProgress && duration > 0 ? '<div class="toast-progress"><div class="toast-progress-bar"></div></div>' : ''}
        `;

        // Add to container
        this.container.appendChild(toast);
        this.activeToasts.set(toastId, toast);

        // Show toast with animation
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        // Handle progress bar
        if (showProgress && duration > 0) {
            const progressBar = toast.querySelector('.toast-progress-bar');
            if (progressBar) {
                let progress = 100;
                const interval = 50;
                const decrement = (100 / duration) * interval;

                const progressInterval = setInterval(() => {
                    progress -= decrement;
                    if (progress <= 0) {
                        clearInterval(progressInterval);
                        this.hide(toastId);
                    } else {
                        progressBar.style.width = `${progress}%`;
                    }
                }, interval);

                // Store interval for cleanup
                toast.progressInterval = progressInterval;
            }
        }

        // Auto-hide after duration
        if (duration > 0) {
            setTimeout(() => {
                this.hide(toastId);
            }, duration);
        }

        return toastId;
    }

    hide(toastId) {
        const toast = this.activeToasts.get(toastId);
        if (!toast) return;

        // Clear progress interval if exists
        if (toast.progressInterval) {
            clearInterval(toast.progressInterval);
        }

        // Hide with animation
        toast.classList.remove('show');
        toast.classList.add('hide');

        // Remove from DOM after animation
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
            this.activeToasts.delete(toastId);
        }, 400);
    }

    hideAll() {
        this.activeToasts.forEach((toast, id) => {
            this.hide(id);
        });
    }

    update(toastId, options) {
        const toast = this.activeToasts.get(toastId);
        if (!toast) return;

        const { type, title, message } = options;

        if (type) {
            // Update toast class
            toast.className = `toast toast-${type} show`;
            
            // Update icon
            const icons = {
                loading: '⏳',
                success: '✅',
                error: '❌',
                warning: '⚠️',
                info: 'ℹ️'
            };
            const iconElement = toast.querySelector('.toast-icon');
            if (iconElement) {
                iconElement.textContent = icons[type] || icons.info;
            }
        }

        if (title) {
            const titleElement = toast.querySelector('.toast-title');
            if (titleElement) {
                titleElement.textContent = title;
            }
        }

        if (message) {
            const messageElement = toast.querySelector('.toast-message');
            if (messageElement) {
                messageElement.textContent = message;
            }
        }
    }

    // Convenience methods
    loading(title, message, options = {}) {
        return this.show({
            type: 'loading',
            title,
            message,
            duration: 0, // Don't auto-hide loading toasts
            showProgress: false,
            ...options
        });
    }

    success(title, message, options = {}) {
        return this.show({
            type: 'success',
            title,
            message,
            duration: 4000,
            ...options
        });
    }

    error(title, message, options = {}) {
        return this.show({
            type: 'error',
            title,
            message,
            duration: 6000,
            ...options
        });
    }

    warning(title, message, options = {}) {
        return this.show({
            type: 'warning',
            title,
            message,
            duration: 5000,
            ...options
        });
    }

    info(title, message, options = {}) {
        return this.show({
            type: 'info',
            title,
            message,
            duration: 4000,
            ...options
        });
    }
}

// Initialize global toast system
window.toastSystem = new ToastNotification();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ToastNotification;
}