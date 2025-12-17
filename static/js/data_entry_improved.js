// تحسين نظام إدخال البيانات - إدارة الفروع المبسطة

// تخزين الفروع المحفوظة للموظف الحالي
let savedBranches = new Map(); // Map<branchName, {code: string, isLocked: boolean}>

// تحميل الفروع المحفوظة عند بدء التطبيق
document.addEventListener('DOMContentLoaded', function() {
    loadSavedBranches();
    initializeDataEntry();
});

function loadSavedBranches() {
    fetch('/get_branches')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                data.branches.forEach(branch => {
                    savedBranches.set(branch.name, {
                        code: branch.code,
                        isLocked: true // الفروع المحفوظة مسبقاً تكون مقفلة
                    });
                });
                console.log('تم تحميل الفروع المحفوظة:', savedBranches.size);
            }
        })
        .catch(error => {
            console.error('خطأ في تحميل الفروع:', error);
        });
}

function setupBranchAutocomplete(index) {
    const branchInput = document.getElementById(`branch_${index}`);
    const shopCodeInput = document.getElementById(`shop_code_${index}`);
    const suggestionsContainer = document.getElementById(`suggestions_${index}`);

    if (!branchInput || !shopCodeInput || !suggestionsContainer) return;

    // إعداد البحث في الفروع
    branchInput.addEventListener('input', function() {
        const searchTerm = this.value.trim();
        
        if (searchTerm.length >= 1) {
            showBranchSuggestions(searchTerm, index);
        } else {
            hideSuggestions(index);
            // إذا تم مسح النص، إلغاء قفل كود الفرع
            shopCodeInput.disabled = false;
            shopCodeInput.value = '';
        }
    });

    // إعداد البحث بكود الفرع
    shopCodeInput.addEventListener('input', function() {
        const shopCode = this.value.trim();
        
        if (shopCode.length >= 2) {
            searchBranchByCode(shopCode, index);
        }
    });

    // التعامل مع التنقل بالكيبورد
    branchInput.addEventListener('keydown', function(e) {
        handleKeyboardNavigation(e, index);
    });

    // إخفاء الاقتراحات عند فقدان التركيز
    branchInput.addEventListener('blur', function() {
        setTimeout(() => hideSuggestions(index), 200);
    });
}

function showBranchSuggestions(searchTerm, index) {
    const suggestionsContainer = document.getElementById(`suggestions_${index}`);
    if (!suggestionsContainer) return;

    // البحث في الفروع المحفوظة محلياً أولاً
    const localMatches = [];
    savedBranches.forEach((branchData, branchName) => {
        if (branchName.toLowerCase().includes(searchTerm.toLowerCase()) ||
            branchData.code.toLowerCase().includes(searchTerm.toLowerCase())) {
            localMatches.push({
                name: branchName,
                code: branchData.code,
                isLocked: branchData.isLocked
            });
        }
    });

    // عرض النتائج
    suggestionsContainer.innerHTML = '';

    if (localMatches.length > 0) {
        localMatches.forEach(branch => {
            const suggestion = document.createElement('div');
            suggestion.className = 'autocomplete-suggestion';
            suggestion.innerHTML = `
                <div class="branch-suggestion">
                    <strong>${branch.name}</strong>
                    <small>كود: ${branch.code}</small>
                    ${branch.isLocked ? '<span class="locked-badge">محفوظ</span>' : ''}
                </div>
            `;
            
            suggestion.addEventListener('click', function() {
                selectBranch(branch.name, branch.code, branch.isLocked, index);
            });
            
            suggestionsContainer.appendChild(suggestion);
        });
    } else {
        // إظهار رسالة لإنشاء فرع جديد
        const newBranchSuggestion = document.createElement('div');
        newBranchSuggestion.className = 'new-branch-suggestion';
        newBranchSuggestion.innerHTML = `
            <div class="new-branch-hint">
                <span class="new-icon">➕</span>
                <span>فرع جديد: "${searchTerm}"</span>
                <small>أدخل كود الفرع لحفظه</small>
            </div>
        `;
        suggestionsContainer.appendChild(newBranchSuggestion);
    }

    suggestionsContainer.style.display = 'block';
}

function selectBranch(branchName, shopCode, isLocked, index) {
    const branchInput = document.getElementById(`branch_${index}`);
    const shopCodeInput = document.getElementById(`shop_code_${index}`);

    if (branchInput && shopCodeInput) {
        branchInput.value = branchName;
        shopCodeInput.value = shopCode;
        
        // قفل كود الفرع إذا كان محفوظاً مسبقاً
        shopCodeInput.disabled = isLocked;
        
        if (isLocked) {
            shopCodeInput.title = 'هذا الفرع محفوظ مسبقاً - لا يمكن تعديل الكود';
            shopCodeInput.classList.add('locked-input');
        } else {
            shopCodeInput.title = '';
            shopCodeInput.classList.remove('locked-input');
        }
        
        hideSuggestions(index);
    }
}

function searchBranchByCode(shopCode, index) {
    // البحث في الفروع المحفوظة محلياً
    for (let [branchName, branchData] of savedBranches) {
        if (branchData.code === shopCode) {
            const branchInput = document.getElementById(`branch_${index}`);
            if (branchInput) {
                branchInput.value = branchName;
                selectBranch(branchName, shopCode, branchData.isLocked, index);
            }
            return;
        }
    }
}

function handleKeyboardNavigation(e, index) {
    const suggestionsContainer = document.getElementById(`suggestions_${index}`);
    const suggestions = suggestionsContainer.querySelectorAll('.autocomplete-suggestion');
    
    // منطق التنقل بالكيبورد (مثل الكود الأصلي)
    // يمكن إضافة المزيد من التفاصيل هنا
}

function hideSuggestions(index) {
    const suggestionsContainer = document.getElementById(`suggestions_${index}`);
    if (suggestionsContainer) {
        suggestionsContainer.style.display = 'none';
    }
}

// دالة لحفظ فرع جديد عند إرسال النموذج
function saveBranchIfNew(branchName, shopCode) {
    if (branchName && shopCode && !savedBranches.has(branchName)) {
        savedBranches.set(branchName, {
            code: shopCode,
            isLocked: false // الفروع الجديدة تكون غير مقفلة في البداية
        });
        
        console.log(`تم حفظ فرع جديد: ${branchName} - ${shopCode}`);
    }
}

// تحسين دالة إرسال النموذج
function handleFormSubmission(e) {
    e.preventDefault();
    
    // التحقق من صحة البيانات وحفظ الفروع الجديدة
    let modelIndex = 0;
    const formData = new FormData(e.target);
    
    while (formData.get(`branch_${modelIndex}`) !== null) {
        const branchName = formData.get(`branch_${modelIndex}`);
        const shopCode = formData.get(`shop_code_${modelIndex}`);
        
        if (branchName && shopCode) {
            saveBranchIfNew(branchName, shopCode);
        }
        
        modelIndex++;
    }
    
    // إرسال النموذج
    submitFormData(formData);
}

function submitFormData(formData) {
    // عرض مؤشر التحميل
    showLoadingIndicator();
    
    fetch('/submit_data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoadingIndicator();
        
        if (data.success) {
            showSuccessMessage(data.message);
            
            // تحديث الفروع المحفوظة لتصبح مقفلة
            updateSavedBranchesStatus();
            
            // إعادة تعيين النموذج
            resetForm();
        } else {
            showErrorMessage(data.message);
        }
    })
    .catch(error => {
        hideLoadingIndicator();
        showErrorMessage('حدث خطأ في إرسال البيانات: ' + error.message);
    });
}

function updateSavedBranchesStatus() {
    // تحديث حالة الفروع لتصبح مقفلة بعد الحفظ
    savedBranches.forEach((branchData, branchName) => {
        if (!branchData.isLocked) {
            branchData.isLocked = true;
        }
    });
}

function showLoadingIndicator() {
    // إظهار مؤشر التحميل
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading-spinner"></span> جاري الحفظ...';
    }
}

function hideLoadingIndicator() {
    // إخفاء مؤشر التحميل
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'حفظ البيانات';
    }
}

function showSuccessMessage(message) {
    // إظهار رسالة نجاح
    const messageDiv = document.createElement('div');
    messageDiv.className = 'success-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <span class="success-icon">✅</span>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

function showErrorMessage(message) {
    // إظهار رسالة خطأ
    const messageDiv = document.createElement('div');
    messageDiv.className = 'error-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <span class="error-icon">❌</span>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

function resetForm() {
    // إعادة تعيين النموذج
    const form = document.getElementById('dataEntryForm');
    if (form) {
        form.reset();
        
        // إعادة تعيين حالة حقول الفروع
        const shopCodeInputs = form.querySelectorAll('.shop-code-input');
        shopCodeInputs.forEach(input => {
            input.disabled = false;
            input.classList.remove('locked-input');
            input.title = '';
        });
        
        // إخفاء الأقسام
        const sections = form.querySelectorAll('.display-type-section, .pop-material-section, .image-upload-section');
        sections.forEach(section => {
            section.style.display = 'none';
        });
    }
}

// تصدير الدوال للاستخدام العام
window.setupBranchAutocomplete = setupBranchAutocomplete;
window.handleFormSubmission = handleFormSubmission;