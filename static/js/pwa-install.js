// 📱 إدارة تثبيت PWA
class PWAInstaller {
    constructor() {
        this.deferredPrompt = null;
        this.installButton = null;
        this.isInstalled = false;
        this.init();
    }

    init() {
        // إنشاء زر التثبيت فوراً
        this.createInstallButton();
        
        // الاستماع لأحداث PWA
        this.setupEventListeners();
        
        // فحص حالة التثبيت
        this.checkInstallStatus();
        
        // تسجيل Service Worker (بدون انتظار)
        this.registerServiceWorker();
        
        // فحص فوري لإمكانية التثبيت
        this.checkInstallPromptAvailability();
    }

    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/static/sw.js');
                console.log('✅ Service Worker registered successfully:', registration);
                
                // التحقق من التحديثات
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            this.showUpdateNotification();
                        }
                    });
                });
            } catch (error) {
                console.error('❌ Service Worker registration failed:', error);
            }
        }
    }

    createInstallButton() {
        // إنشاء زر التثبيت
        this.installButton = document.createElement('button');
        this.installButton.className = 'pwa-install-btn';
        this.installButton.innerHTML = `
            <div class="install-icon">📱</div>
            <div class="install-text">
                <div class="install-title">Install App</div>
                <div class="install-subtitle">For quick and easy access</div>
            </div>
            <div class="install-arrow">⬇️</div>
        `;
        
        // إخفاء الزر افتراضياً
        this.installButton.style.display = 'none';
        
        // إضافة الزر لصفحة تسجيل الدخول
        const loginForm = document.querySelector('.login-form');
        if (loginForm) {
            loginForm.appendChild(this.installButton);
        }
    }

    setupEventListeners() {
        // الاستماع لحدث beforeinstallprompt
        window.addEventListener('beforeinstallprompt', (e) => {
            console.log('🎯 PWA install prompt available');
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallButton();
        });

        // فحص فوري عند تحميل الصفحة
        if (document.readyState === 'complete') {
            this.checkInstallPromptAvailability();
        } else {
            window.addEventListener('load', () => {
                this.checkInstallPromptAvailability();
            });
        }

        // الاستماع لحدث appinstalled
        window.addEventListener('appinstalled', () => {
            console.log('✅ PWA installed successfully');
            this.isInstalled = true;
            this.hideInstallButton();
            this.showInstalledMessage();
        });

        // النقر على زر التثبيت
        if (this.installButton) {
            this.installButton.addEventListener('click', () => {
                this.installApp();
            });
        }

        // فحص دوري لإمكانية التثبيت (للمتصفحات البطيئة)
        let checkCount = 0;
        const intervalCheck = setInterval(() => {
            checkCount++;
            if (checkCount > 10) { // توقف بعد 10 ثواني
                clearInterval(intervalCheck);
                return;
            }
            
            if (!this.deferredPrompt && !this.isInstalled) {
                // إظهار الزر للمتصفحات التي تدعم PWA
                const supportsPWA = 'serviceWorker' in navigator;
                if (supportsPWA && this.installButton && this.installButton.style.display === 'none') {
                    this.showInstallButton();
                    console.log('🎯 PWA install button shown (periodic check)');
                }
            } else {
                clearInterval(intervalCheck);
            }
        }, 1000);

        // فحص تغيير حالة الاتصال
        window.addEventListener('online', () => {
            this.showConnectionStatus('Online', 'success');
        });

        window.addEventListener('offline', () => {
            this.showConnectionStatus('Offline - Working in offline mode', 'warning');
        });
    }

    showInstallButton() {
        if (this.installButton && !this.isInstalled) {
            this.installButton.style.display = 'flex';
            
            // تأثير الظهور فوري
            requestAnimationFrame(() => {
                this.installButton.classList.add('show');
            });
        }
    }

    hideInstallButton() {
        if (this.installButton) {
            this.installButton.classList.remove('show');
            setTimeout(() => {
                this.installButton.style.display = 'none';
            }, 300);
        }
    }

    async installApp() {
        if (!this.deferredPrompt) {
            this.showManualInstallInstructions();
            return;
        }

        try {
            // إظهار نافذة التثبيت
            this.deferredPrompt.prompt();
            
            // انتظار اختيار المستخدم
            const { outcome } = await this.deferredPrompt.userChoice;
            
            if (outcome === 'accepted') {
                console.log('✅ User accepted PWA install');
                this.showInstallProgress();
            } else {
                console.log('❌ User dismissed PWA install');
                this.showInstallTips();
            }
            
            // إعادة تعيين المتغير
            this.deferredPrompt = null;
            
        } catch (error) {
            console.error('❌ PWA install error:', error);
            this.showManualInstallInstructions();
        }
    }

    checkInstallStatus() {
        // فحص إذا كان التطبيق مثبت بالفعل
        if (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) {
            this.isInstalled = true;
            console.log('✅ App is running in standalone mode');
            return;
        }

        // فحص إذا كان مضاف للشاشة الرئيسية (iOS)
        if (window.navigator.standalone === true) {
            this.isInstalled = true;
            console.log('✅ App is running in standalone mode (iOS)');
            return;
        }

        // فحص User Agent للتطبيقات المثبتة
        if (document.referrer.includes('android-app://')) {
            this.isInstalled = true;
            console.log('✅ App opened from installed PWA (Android)');
            return;
        }
    }

    checkInstallPromptAvailability() {
        // فحص فوري لإمكانية التثبيت
        if (!this.isInstalled) {
            // إظهار الزر بعد تأخير قصير للمتصفحات التي تدعم PWA
            const supportsPWA = 'serviceWorker' in navigator && 'PushManager' in window;
            
            if (supportsPWA) {
                // تأخير قصير لإعطاء المتصفح وقت لتحضير beforeinstallprompt
                setTimeout(() => {
                    if (!this.deferredPrompt && !this.isInstalled) {
                        // إظهار الزر حتى لو لم يتم تشغيل beforeinstallprompt بعد
                        this.showInstallButton();
                        console.log('🎯 PWA install button shown (fallback)');
                    }
                }, 1000); // تقليل التأخير إلى ثانية واحدة
            }
        }
    }

    showInstallProgress() {
        const progressDiv = document.createElement('div');
        progressDiv.className = 'install-progress';
        progressDiv.innerHTML = `
            <div class="progress-content">
                <div class="progress-icon">⏳</div>
                <div class="progress-text">Installing app...</div>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
            </div>
        `;
        
        document.body.appendChild(progressDiv);
        
        // إزالة الرسالة بعد 3 ثواني
        setTimeout(() => {
            progressDiv.remove();
        }, 3000);
    }

    showInstalledMessage() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'install-success';
        messageDiv.innerHTML = `
            <div class="success-content">
                <div class="success-icon">✅</div>
                <div class="success-text">App installed successfully!</div>
                <div class="success-subtitle">You can now access it from your home screen</div>
            </div>
        `;
        
        document.body.appendChild(messageDiv);
        
        // إزالة الرسالة بعد 5 ثواني
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }

    showManualInstallInstructions() {
        const browser = this.detectBrowser();
        let instructions = '';
        
        switch (browser) {
            case 'chrome':
                instructions = 'Click menu (⋮) → "Install app"';
                break;
            case 'firefox':
                instructions = 'Click menu (☰) → "Install"';
                break;
            case 'safari':
                instructions = 'Click share (⎋) → "Add to Home Screen"';
                break;
            case 'edge':
                instructions = 'Click menu (⋯) → "Install this site as an app"';
                break;
            default:
                instructions = 'Look for "Install app" or "Add to Home Screen" option in browser menu';
        }

        const instructionsDiv = document.createElement('div');
        instructionsDiv.className = 'install-instructions';
        instructionsDiv.innerHTML = `
            <div class="instructions-content">
                <div class="instructions-icon">💡</div>
                <div class="instructions-title">How to Install App</div>
                <div class="instructions-text">${instructions}</div>
                <button class="instructions-close" onclick="this.parentElement.parentElement.remove()">Got it</button>
            </div>
        `;
        
        document.body.appendChild(instructionsDiv);
    }

    showInstallTips() {
        const tipsDiv = document.createElement('div');
        tipsDiv.className = 'install-tips';
        tipsDiv.innerHTML = `
            <div class="tips-content">
                <div class="tips-icon">💡</div>
                <div class="tips-title">Benefits of Installing App</div>
                <ul class="tips-list">
                    <li>🚀 Faster app access</li>
                    <li>📱 Works offline</li>
                    <li>🔔 Instant notifications</li>
                    <li>💾 Saves data usage</li>
                </ul>
                <button class="tips-close" onclick="this.parentElement.parentElement.remove()">OK</button>
            </div>
        `;
        
        document.body.appendChild(tipsDiv);
    }

    showConnectionStatus(message, type) {
        const statusDiv = document.createElement('div');
        statusDiv.className = `connection-status ${type}`;
        statusDiv.innerHTML = `
            <div class="status-content">
                <div class="status-icon">${type === 'success' ? '🟢' : '🟡'}</div>
                <div class="status-text">${message}</div>
            </div>
        `;
        
        document.body.appendChild(statusDiv);
        
        // إزالة الرسالة بعد 3 ثواني
        setTimeout(() => {
            statusDiv.remove();
        }, 3000);
    }

    showUpdateNotification() {
        const updateDiv = document.createElement('div');
        updateDiv.className = 'update-notification';
        updateDiv.innerHTML = `
            <div class="update-content">
                <div class="update-icon">🔄</div>
                <div class="update-text">New update available</div>
                <button class="update-btn" onclick="window.location.reload()">Update now</button>
                <button class="update-close" onclick="this.parentElement.parentElement.remove()">Later</button>
            </div>
        `;
        
        document.body.appendChild(updateDiv);
    }

    detectBrowser() {
        const userAgent = navigator.userAgent.toLowerCase();
        
        if (userAgent.includes('chrome') && !userAgent.includes('edg')) {
            return 'chrome';
        } else if (userAgent.includes('firefox')) {
            return 'firefox';
        } else if (userAgent.includes('safari') && !userAgent.includes('chrome')) {
            return 'safari';
        } else if (userAgent.includes('edg')) {
            return 'edge';
        }
        
        return 'unknown';
    }
}

// تشغيل PWA Installer عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    new PWAInstaller();
});

// تصدير للاستخدام العام
window.PWAInstaller = PWAInstaller;