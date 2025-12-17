// Data Entry JavaScript functionality

// Model data structure
const modelData = {
    'OLED': ['S95F', 'S90F', 'S85F'],
    'Neo QLED': ['QN90', 'QN85F', 'QN80F', 'QN70F'],
    'QLED': ['Q8F', 'Q7F'],
    'UHD': ['U8000', '100"/98"'],
    'LTV': ['The Frame'],
    'BESPOKE COMBO': ['WD25DB8995', 'WD21D6400'],
    'BESPOKE Front': ['WW11B1944DGB'],
    'Front': ['WW11B1534D', 'WW90CGC', 'WW4040', 'WW4020'],
    'TL': ['WA19CG6886', 'Local TL'],
    'SBS': ['RS70F'],
    'TMF': ['Bespoke', 'TMF Non-Bespoke', 'TMF'],
    'BMF': ['(Bespoke, BMF)', '(Non-Bespoke, BMF)'],
    'Local TMF': ['Local TMF']
};

// Display type options based on category
const displayTypes = {
    // For TV categories
    'OLED': ['Highlight Zone', 'Fixtures', 'Multi Brand Zone with Space', 'SIS (Endcap)'],
    'Neo QLED': ['Highlight Zone', 'Fixtures', 'Multi Brand Zone with Space', 'SIS (Endcap)'],
    'QLED': ['Highlight Zone', 'Fixtures', 'Multi Brand Zone with Space', 'SIS (Endcap)'],
    'UHD': ['Highlight Zone', 'Fixtures', 'Multi Brand Zone with Space', 'SIS (Endcap)'],
    'LTV': ['Highlight Zone', 'Fixtures', 'Multi Brand Zone with Space', 'SIS (Endcap)'],

    // For Appliance categories
    'BESPOKE COMBO': ['POP Out', 'POP Inner', 'POP'],
    'BESPOKE Front': ['POP Out', 'POP Inner', 'POP'],
    'Front': ['POP Out', 'POP Inner', 'POP'],
    'TL': ['POP Out', 'POP Inner', 'POP'],
    'SBS': ['POP Out', 'POP Inner', 'POP'],
    'TMF': ['POP Out', 'POP Inner', 'POP'],
    'BMF': ['POP Out', 'POP Inner', 'POP'],
    'Local TMF': ['POP Out', 'POP Inner', 'POP']
};

// POP Material checklist items based on category
const popMaterials = {
    'OLED': [
        'AI topper',
        'Oled Topper',
        'Glare Free',
        'New Topper',
        '165 HZ Side POP',
        'Category POP',
        'Samsung OLED Topper',
        '165 HZ & joy stick indicator',
        'AI Topper Gaming',
        'Side POP',
        'Specs Card',
        'OLED Topper',
        'Why Oled side POP'
    ],

    'Neo QLED': [
        'AI topper',
        'Lockup Topper',
        'Screen POP',
        'New Topper',
        'Glare Free',
        'Specs Card'
    ],

    'QLED': [
        'AI topper',
        'Samsung QLED Topper',
        'Screen POP',
        'New Topper',
        'Specs Card',
        'QLED Topper'
    ],

    'UHD': [
        'UHD topper',
        'Samsung UHD topper',
        'Screen POP',
        'New Topper',
        'Specs Card',
        'AI topper',
        'Samsung Lockup Topper',
        'Inch Logo side POP'
    ],

    'LTV': [
        'Side POP',
        'Matte Display',
        'Category POP',
        'Frame Bezel'
    ],

    'BESPOKE COMBO': [
        'PODs (Door)',
        'POD (Top)',
        'POD (Front)',
        '3 PODs (Top)',
        'AI Home POP',
        'AI Home',
        'AI control panel',
        'Capacity (Kg)',
        'Capacity Dryer',
        'Filter',
        'Ecobuble POP',
        'Ecco Buble',
        'AI Ecco Buble',
        '20 Years Warranty',
        'New Arrival',
        'Samsung Brand/Tech Topper'
    ],

    'BESPOKE Front': [
        'PODs (Door)',
        'POD (Top)',
        'POD (Front)',
        '3 PODs (Top)',
        'AI Home POP',
        'AI Home',
        'AI control panel',
        'Capacity (Kg)',
        'Capacity Dryer',
        'Filter',
        'Ecobuble POP',
        'Ecco Buble',
        'AI Ecco Buble',
        '20 Years Warranty',
        'New Arrival',
        'Samsung Brand/Tech Topper'
    ],

    'Front': [
        'PODs (Door)',
        'POD (Top)',
        'POD (Front)',
        '3 PODs (Top)',
        'AI Home POP',
        'AI Home',
        'AI control panel',
        'Capacity (Kg)',
        'Capacity Dryer',
        'Filter',
        'Ecobuble POP',
        'Ecco Buble',
        'AI Ecco Buble',
        '20 Years Warranty',
        'New Arrival',
        'Samsung Brand/Tech Topper'
    ],

    'TL': [
        'PODs (Door)',
        'POD (Top)',
        'POD (Front)',
        '3 PODs (Top)',
        'AI Home POP',
        'AI Home',
        'AI control panel',
        'Capacity (Kg)',
        'Capacity Dryer',
        'Filter',
        'Ecobuble POP',
        'Ecco Buble',
        'AI Ecco Buble',
        '20 Years Warranty',
        'New Arrival',
        'Samsung Brand/Tech Topper'
    ],

    'SBS': [
        'Samsung Brand/Tech Topper',
        'Main POD',
        '20 Years Warranty',
        'Twin Cooling Plus™',
        'Smart Conversion™',
        'Digital Inverter™',
        'SpaceMax™',
        'Tempered Glass',
        'Power Freeze',
        'Big Vegetable Box',
        'Organize Big Bin'
    ],

    'TMF': [
        'Samsung Brand/Tech Topper',
        '20 Years Warranty',
        'Key features POP',
        'Side POP',
        'Global No.1',
        'Freshness POP',
        'Bacteria Safe Ionizer POP',
        'Gallon Guard POP',
        'Big Vegetables Box POP',
        'Adjustable Pin & Organize POP',
        'Optimal Fresh',
        'Tempered Glass',
        'Gallon Guard',
        'Veg Box',
        'Internal Display',
        'Multi Tray',
        'Foldable Shelf',
        'Active Fresh Filter'
    ],

    'BMF': [
        'Samsung Brand/Tech Topper',
        '20 Years Warranty',
        'Key features POP',
        'Side POP',
        'Global No.1',
        'Led Lighting POP',
        'Full Open Box POP',
        'Big Guard POP',
        'Adjustable Pin',
        'Saves Energy POP',
        'Gentle Lighting',
        'Multi Tray',
        'All-Around Cooling',
        '2 Step Foldable Shelf',
        'Big Fresh Box'
    ],

    'Local TMF': [
        'Samsung Brand/Tech Topper',
        'Key features POP',
        'Side POP',
        'Big Vegetables Box POP'
    ]
};

let modelCounter = 1;

// Initialize data entry functionality
document.addEventListener('DOMContentLoaded', function () {
    initializeDataEntry();
});

function initializeDataEntry() {
    // Load categories first
    loadCategories();

    // Set up event listeners for the first model entry
    setupModelEntry(0);

    // Add model button functionality
    const addModelBtn = document.getElementById('addModelBtn');
    if (addModelBtn) {
        addModelBtn.addEventListener('click', addNewModelEntry);
    }

    // Form submission handling
    const dataEntryForm = document.getElementById('dataEntryForm');
    if (dataEntryForm) {
        dataEntryForm.addEventListener('submit', handleFormSubmission);
    }
}

function loadCategories() {
    fetch('/get_dynamic_data/categories')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const categorySelects = document.querySelectorAll('.category-select');
                categorySelects.forEach(select => {
                    // Keep the default option
                    const defaultOption = select.querySelector('option[value=""]');
                    select.innerHTML = '';
                    if (defaultOption) {
                        select.appendChild(defaultOption);
                    } else {
                        const option = document.createElement('option');
                        option.value = '';
                        option.textContent = 'Select Category';
                        select.appendChild(option);
                    }

                    // Add categories from database
                    data.data.forEach(category => {
                        const option = document.createElement('option');
                        option.value = category;
                        option.textContent = category;
                        select.appendChild(option);
                    });
                });
            }
        })
        .catch(error => {
            console.error('Error loading categories:', error);
        });
}

function setupModelEntry(index) {
    const categorySelect = document.getElementById(`category_${index}`);
    const modelSelect = document.getElementById(`model_${index}`);

    if (categorySelect) {
        categorySelect.addEventListener('change', function () {
            handleCategoryChange(index, this.value);
        });
    }

    if (modelSelect) {
        modelSelect.addEventListener('change', function () {
            handleModelChange(index, this.value);
        });
    }

    // Setup branch autocomplete
    setupBranchAutocomplete(index);

    // Setup image upload preview
    setupImageUpload(index);

    // Setup comment functionality for new models
    setupCommentFunctionality(index);

    // Note: setupModelImageDisplay will be called when category is selected
}

function handleCategoryChange(index, category) {
    const modelSelect = document.getElementById(`model_${index}`);

    // Clear model dropdown
    modelSelect.innerHTML = '<option value="">Select Model</option>';
    modelSelect.disabled = true;

    if (category) {
        // Fetch models from database
        fetch(`/get_dynamic_data/models?category=${encodeURIComponent(category)}`)
            .then(response => response.json())
            .then(data => {
                if (data.success && data.data.length > 0) {
                    data.data.forEach(model => {
                        const option = document.createElement('option');
                        option.value = model;
                        option.textContent = model;
                        modelSelect.appendChild(option);
                    });
                    modelSelect.disabled = false;

                    // Add model image functionality after models are loaded
                    setupModelImageDisplay(index, category);
                }
            })
            .catch(error => {
                console.error('Error loading models:', error);
            });
    }

    // Hide subsequent sections when category changes
    hideSubsequentSections(index);
}

function handleModelChange(index, model) {
    if (model) {
        showDisplayTypeSection(index);
        showPopMaterialSection(index);
        showCommentSection(index);
        showImageUploadSection(index);
    } else {
        hideSubsequentSections(index);
    }
}

function showDisplayTypeSection(index) {
    const section = document.querySelector(`[data-index="${index}"] .display-type-section`);
    const select = document.querySelector(`[data-index="${index}"] .display-type-select`);
    const categorySelect = document.getElementById(`category_${index}`);

    if (section && select && categorySelect) {
        const selectedCategory = categorySelect.value;

        // Clear display type options
        select.innerHTML = '<option value="">Select Display Type</option>';

        if (selectedCategory) {
            // Fetch display types from database
            fetch(`/get_dynamic_data/display_types?category=${encodeURIComponent(selectedCategory)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.data.length > 0) {
                        data.data.forEach(type => {
                            const option = document.createElement('option');
                            option.value = type;
                            option.textContent = type;
                            select.appendChild(option);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error loading display types:', error);
                });
        }

        section.style.display = 'block';
    }
}

function showPopMaterialSection(index) {
    const section = document.querySelector(`[data-index="${index}"] .pop-material-section`);
    const container = document.querySelector(`[data-index="${index}"] .checklist-container`);
    const modelSelect = document.getElementById(`model_${index}`);

    if (section && container && modelSelect) {
        const selectedModel = modelSelect.value;

        // Clear existing items
        container.innerHTML = '';

        if (selectedModel) {
            // Fetch POP materials from database by model
            fetch(`/get_dynamic_data/pop_materials?model=${encodeURIComponent(selectedModel)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.data.length > 0) {
                        // Create checklist items
                        data.data.forEach((material, materialIndex) => {
                            const checkboxDiv = document.createElement('div');
                            checkboxDiv.className = 'checkbox-item';

                            const checkbox = document.createElement('input');
                            checkbox.type = 'checkbox';
                            checkbox.id = `pop_${index}_${materialIndex}`;
                            checkbox.name = `pop_materials_${index}`;
                            checkbox.value = material;

                            const label = document.createElement('label');
                            label.htmlFor = `pop_${index}_${materialIndex}`;
                            label.textContent = material;

                            checkboxDiv.appendChild(checkbox);
                            checkboxDiv.appendChild(label);
                            container.appendChild(checkboxDiv);
                        });
                    } else {
                        // Show message if no materials found for this model
                        const noMaterialsDiv = document.createElement('div');
                        noMaterialsDiv.className = 'no-materials-message';
                        noMaterialsDiv.textContent = 'No POP materials configured for this model yet.';
                        container.appendChild(noMaterialsDiv);
                    }
                })
                .catch(error => {
                    console.error('Error loading POP materials:', error);
                });
        }

        section.style.display = 'block';
    }
}

function showCommentSection(index) {
    const section = document.querySelector(`[data-index="${index}"] .comment-section`);
    if (section) {
        section.style.display = 'block';
        setupCommentFunctionality(index);
    }
}

function showImageUploadSection(index) {
    const section = document.querySelector(`[data-index="${index}"] .image-upload-section`);
    if (section) {
        section.style.display = 'block';
    }
}

function hideSubsequentSections(index) {
    const modelEntry = document.querySelector(`[data-index="${index}"]`);
    if (modelEntry) {
        const sections = ['.display-type-section', '.pop-material-section', '.comment-section', '.image-upload-section'];
        sections.forEach(sectionClass => {
            const section = modelEntry.querySelector(sectionClass);
            if (section) {
                section.style.display = 'none';
            }
        });
    }
}

function setupBranchAutocomplete(index) {
    const branchInput = document.getElementById(`branch_${index}`);
    const shopCodeInput = document.getElementById(`shop_code_${index}`);
    const suggestionsContainer = document.getElementById(`suggestions_${index}`);

    if (!branchInput || !shopCodeInput || !suggestionsContainer) return;

    let currentSuggestions = [];
    let selectedIndex = -1;

    // Handle branch input changes
    branchInput.addEventListener('input', function () {
        const searchTerm = this.value.trim();

        if (searchTerm.length >= 1) {
            fetchBranches(searchTerm, index);
        } else {
            hideSuggestions(index);
            // إذا تم مسح النص، إلغاء قفل كود الفرع
            shopCodeInput.disabled = false;
            shopCodeInput.classList.remove('locked-input');
            shopCodeInput.title = '';
        }
    });

    // Handle shop code input changes
    shopCodeInput.addEventListener('input', function () {
        const shopCode = this.value.trim();

        if (shopCode.length >= 2) {
            // Search for branch by shop code
            fetchBranchByCode(shopCode, index);
        }
    });

    // Handle keyboard navigation for branch input
    branchInput.addEventListener('keydown', function (e) {
        const suggestions = suggestionsContainer.querySelectorAll('.autocomplete-suggestion');

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, suggestions.length - 1);
                updateHighlight(suggestions);
                break;

            case 'ArrowUp':
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, -1);
                updateHighlight(suggestions);
                break;

            case 'Enter':
                e.preventDefault();
                if (selectedIndex >= 0 && suggestions[selectedIndex]) {
                    const suggestionData = suggestions[selectedIndex].dataset;
                    selectBranch(suggestionData.name, suggestionData.code, index);
                }
                break;

            case 'Escape':
                hideSuggestions(index);
                break;
        }
    });

    // Handle focus and blur
    branchInput.addEventListener('focus', function () {
        if (this.value.trim().length >= 1) {
            fetchBranches(this.value.trim(), index);
        }
    });

    branchInput.addEventListener('blur', function () {
        // Delay hiding to allow clicking on suggestions
        setTimeout(() => hideSuggestions(index), 200);
    });

    function updateHighlight(suggestions) {
        suggestions.forEach((suggestion, idx) => {
            suggestion.classList.toggle('highlighted', idx === selectedIndex);
        });
    }
}

function fetchBranches(searchTerm, index) {
    fetch(`/get_branches?search=${encodeURIComponent(searchTerm)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSuggestions(data.branches, index);
            }
        })
        .catch(error => {
            console.error('Error fetching branches:', error);
        });
}

function showSuggestions(branches, index) {
    const suggestionsContainer = document.getElementById(`suggestions_${index}`);
    if (!suggestionsContainer) return;

    suggestionsContainer.innerHTML = '';

    if (branches.length === 0) {
        // لا تظهر أي رسالة عند عدم وجود فروع
        suggestionsContainer.style.display = 'none';
        return;
    } else {
        branches.forEach(branch => {
            const suggestion = document.createElement('div');
            suggestion.className = 'autocomplete-suggestion';
            suggestion.dataset.name = branch.name;
            suggestion.dataset.code = branch.code;
            suggestion.innerHTML = `<strong>${branch.name}</strong><br><small>Code: ${branch.code}</small>`;

            suggestion.addEventListener('click', function () {
                selectBranch(branch.name, branch.code, true, index); // إضافة معامل isLocked
            });

            suggestionsContainer.appendChild(suggestion);
        });
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
        if (isLocked) {
            // 🔧 الحل: استخدام readonly بدلاً من disabled لضمان إرسال القيمة مع النموذج
            shopCodeInput.readOnly = true;
            shopCodeInput.disabled = false; // تأكد من عدم التعطيل
            shopCodeInput.classList.add('locked-input');
            shopCodeInput.title = 'This branch is saved - code cannot be edited';

            // إظهار رسالة للمستخدم
            // رسالة القفل تم إزالتها
        } else {
            shopCodeInput.disabled = false;
            shopCodeInput.classList.remove('locked-input');
            shopCodeInput.title = '';
        }

        hideSuggestions(index);
    }
}

function fetchBranchByCode(shopCode, index) {
    fetch(`/get_branch_by_code?code=${encodeURIComponent(shopCode)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // اختيار الفرع مع تفعيل القفل
                selectBranch(data.branch.name, data.branch.code, true, index);
            }
        })
        .catch(error => {
            console.error('Error fetching branch by code:', error);
        });
}

function hideSuggestions(index) {
    const suggestionsContainer = document.getElementById(`suggestions_${index}`);
    if (suggestionsContainer) {
        suggestionsContainer.style.display = 'none';
    }
}

function setupImageUpload(index) {
    const imageInput = document.querySelector(`[data-index="${index}"] .image-upload`);
    const previewContainer = document.querySelector(`[data-index="${index}"] .image-preview`);

    if (imageInput && previewContainer) {
        imageInput.addEventListener('change', function (e) {
            const files = e.target.files;

            if (validateImageFiles(files)) {
                handleImagePreview(files, previewContainer, index);
            } else {
                // Clear the input if validation fails
                e.target.value = '';
            }
        });
    }
}

// Global array to store selected files for each model entry
let selectedFiles = {};

function handleImagePreview(files, previewContainer, modelIndex) {
    // Initialize array for this model if not exists
    if (!selectedFiles[modelIndex]) {
        selectedFiles[modelIndex] = [];
    }

    // Add new files to existing ones
    Array.from(files).forEach(file => {
        if (file.type.startsWith('image/')) {
            selectedFiles[modelIndex].push(file);
        }
    });

    // Check total count limit
    if (selectedFiles[modelIndex].length > 10) {
        alert('Maximum 10 images allowed. Keeping first 10 images.');
        selectedFiles[modelIndex] = selectedFiles[modelIndex].slice(0, 10);
    }

    // Clear and rebuild preview
    previewContainer.innerHTML = '';

    // Add header with count
    if (selectedFiles[modelIndex].length > 0) {
        const header = document.createElement('div');
        header.className = 'preview-header';
        header.innerHTML = `<h5>📷 Selected Images (${selectedFiles[modelIndex].length}/10)</h5>`;
        previewContainer.appendChild(header);

        // Create grid container
        const gridContainer = document.createElement('div');
        gridContainer.className = 'image-preview-grid';
        previewContainer.appendChild(gridContainer);

        selectedFiles[modelIndex].forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = function (e) {
                const previewDiv = document.createElement('div');
                previewDiv.className = 'image-preview-item';
                previewDiv.dataset.fileIndex = index;

                const img = document.createElement('img');
                img.src = e.target.result;
                img.alt = `Preview ${index + 1}`;
                img.loading = 'lazy';

                const fileName = document.createElement('span');
                fileName.textContent = `${index + 1}. ${file.name}`;
                fileName.className = 'file-name';

                const fileSize = document.createElement('span');
                fileSize.textContent = `(${(file.size / 1024 / 1024).toFixed(2)} MB)`;
                fileSize.className = 'file-size';

                const removeBtn = document.createElement('button');
                removeBtn.textContent = '×';
                removeBtn.className = 'remove-image-btn';
                removeBtn.type = 'button';
                removeBtn.onclick = () => removeImageFromSelection(modelIndex, index, previewContainer);

                previewDiv.appendChild(img);
                previewDiv.appendChild(fileName);
                previewDiv.appendChild(fileSize);
                previewDiv.appendChild(removeBtn);
                gridContainer.appendChild(previewDiv);
            };
            reader.readAsDataURL(file);
        });
    }

    // Update the file input with current selection
    updateFileInput(modelIndex);
}

function removeImageFromSelection(modelIndex, fileIndex, previewContainer) {
    if (selectedFiles[modelIndex]) {
        selectedFiles[modelIndex].splice(fileIndex, 1);
        handleImagePreview([], previewContainer, modelIndex);
    }
}

function updateFileInput(modelIndex) {
    const fileInput = document.querySelector(`[data-index="${modelIndex}"] .image-upload`);
    if (fileInput && selectedFiles[modelIndex]) {
        // Create new FileList from selected files
        const dt = new DataTransfer();
        selectedFiles[modelIndex].forEach(file => {
            dt.items.add(file);
        });
        fileInput.files = dt.files;
    }
}

function addNewModelEntry() {
    const container = document.getElementById('modelsContainer');
    const newModelEntry = createModelEntryHTML(modelCounter);

    container.insertAdjacentHTML('beforeend', newModelEntry);
    setupModelEntry(modelCounter);

    modelCounter++;

    // Scroll to the new entry
    const newEntry = document.querySelector(`[data-index="${modelCounter - 1}"]`);
    if (newEntry) {
        newEntry.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}



function removeModelEntry(index) {
    const modelEntry = document.querySelector(`[data-index="${index}"]`);
    if (modelEntry && document.querySelectorAll('.model-entry').length > 1) {
        modelEntry.remove();
    } else {
        alert('At least one model entry is required.');
    }
}

function handleFormSubmission(e) {
    e.preventDefault();

    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');

    // Show loading state
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Saving...';
    submitBtn.disabled = true;

    // Show saving popup
    showSavePopup('⏳ Saving...');

    // Validate form
    if (!validateForm(form)) {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        return;
    }

    // Create FormData object
    const formData = new FormData(form);

    // Log form data for debugging
    console.log('📋 Form data being submitted:');
    for (let [key, value] of formData.entries()) {
        console.log(`   ${key}: ${value}`);
    }

    // Submit form
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
        .then(response => {
            console.log('📡 Response status:', response.status);
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(errorData => {
                    throw new Error(errorData.message || `Server error: ${response.status}`);
                });
            }
        })
        .then(data => {
            console.log('📋 Response data:', data);
            if (data.success) {
                // Show success popup
                showSavePopup('✅ Saved successfully!', true);

                showSuccessMessage(data.message || 'Data saved successfully!');

                // إعادة تعيين النموذج بالكامل
                form.reset();
                resetFormState();

                // إعادة تحميل الصفحة للتأكد من التعيين الكامل (اختياري)
                setTimeout(() => {
                    // يمكن إلغاء التعليق للإعادة التحميل الكامل
                    // window.location.reload();
                }, 1000);
            } else {
                throw new Error(data.message || 'Failed to save data');
            }
        })
        .catch(error => {
            console.error('❌ Submission error:', error);
            // Hide saving popup and show error
            hideSavePopup();
            showErrorMessage(error.message || 'Failed to save data. Please try again.');
        })
        .finally(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
}

function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });

    if (!isValid) {
        showErrorMessage('Please fill in all required fields.');
    }

    return isValid;
}

function resetFormState() {
    console.log('🔄 إعادة تعيين النموذج بالكامل...');

    // Reset to single model entry
    const container = document.getElementById('modelsContainer');
    const firstEntry = container.querySelector('.model-entry');

    // Remove all entries except the first one
    const allEntries = container.querySelectorAll('.model-entry');
    allEntries.forEach((entry, index) => {
        if (index > 0) {
            entry.remove();
        }
    });

    // إعادة تعيين الإدخال الأول بالكامل
    if (firstEntry) {
        // إعادة تعيين جميع الحقول
        const branchInput = firstEntry.querySelector('#branch_0');
        const shopCodeInput = firstEntry.querySelector('#shop_code_0');
        const categorySelect = firstEntry.querySelector('.category-select');
        const modelSelect = firstEntry.querySelector('.model-select');
        const displayTypeSelect = firstEntry.querySelector('.display-type-select');
        const imageInput = firstEntry.querySelector('.image-upload');
        const imagePreview = firstEntry.querySelector('.image-preview');

        // إعادة تعيين حقول الفرع
        if (branchInput) {
            branchInput.value = '';
        }

        if (shopCodeInput) {
            shopCodeInput.value = '';
            shopCodeInput.readOnly = false;
            shopCodeInput.disabled = false;
            shopCodeInput.classList.remove('locked-input');
            shopCodeInput.title = '';
            shopCodeInput.style.backgroundColor = '';
            shopCodeInput.style.cursor = '';
        }

        // إعادة تعيين القوائم المنسدلة
        if (categorySelect) {
            categorySelect.selectedIndex = 0;
        }

        if (modelSelect) {
            modelSelect.disabled = true;
            modelSelect.innerHTML = '<option value="">Select Model</option>';
            modelSelect.selectedIndex = 0;
        }

        if (displayTypeSelect) {
            displayTypeSelect.innerHTML = '<option value="">Select Display Type</option>';
            displayTypeSelect.selectedIndex = 0;
        }

        // إعادة تعيين رفع الصور
        if (imageInput) {
            imageInput.value = '';
        }

        if (imagePreview) {
            imagePreview.innerHTML = '';
        }

        // مسح الصور المحددة من المتغير العام
        if (typeof selectedFiles !== 'undefined') {
            selectedFiles[0] = [];
        }

        // إخفاء الأقسام
        hideSubsequentSections(0);

        // إزالة أي حقول مخفية
        const hiddenInputs = firstEntry.querySelectorAll('input[type="hidden"]');
        hiddenInputs.forEach(input => {
            if (input.id && input.id.includes('shop_code_hidden')) {
                input.remove();
            }
        });

        // إزالة أي رسائل قفل
        const lockMessages = firstEntry.querySelectorAll('.branch-lock-message');
        lockMessages.forEach(msg => msg.remove());

        // إخفاء اقتراحات الفروع
        hideSuggestions(0);
    }

    // إعادة تعيين العداد
    modelCounter = 1;

    console.log('✅ تم إعادة تعيين النموذج بالكامل');
}

function showSuccessMessage(message) {
    showMessage(message, 'success');
}

function showErrorMessage(message) {
    showMessage(message, 'error');
}

function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.flash-message');
    existingMessages.forEach(msg => msg.remove());

    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `flash-message alert alert-${type}`;
    messageDiv.textContent = message;

    // Insert at top of form
    const form = document.getElementById('dataEntryForm');
    form.insertBefore(messageDiv, form.firstChild);

    // Auto-hide after 5 seconds
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            messageDiv.remove();
        }, 300);
    }, 5000);
}

// This function is now replaced by removeImageFromSelection

function validateImageFiles(files) {
    const maxFiles = 10;
    const maxSize = 10 * 1024 * 1024; // 10MB per file
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/avif'];

    if (files.length > maxFiles) {
        alert(`Maximum ${maxFiles} images allowed. Please select fewer images.`);
        return false;
    }

    for (let file of files) {
        if (!allowedTypes.includes(file.type)) {
            alert(`File "${file.name}" is not a supported image format. Please use JPG, PNG, WEBP, or AVIF.`);
            return false;
        }

        if (file.size > maxSize) {
            alert(`File "${file.name}" is too large (${(file.size / 1024 / 1024).toFixed(2)}MB). Maximum size is 10MB per image.`);
            return false;
        }
    }

    return true;
}

// setupImageUpload function is defined above with the new functionality
// Drag and Drop functionality for images
function setupDragAndDrop(index) {
    const uploadLabel = document.querySelector(`[data-index="${index}"] .file-upload-label`);
    const fileInput = document.querySelector(`[data-index="${index}"] .image-upload`);
    const previewContainer = document.querySelector(`[data-index="${index}"] .image-preview`);

    if (!uploadLabel || !fileInput || !previewContainer) return;

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadLabel.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadLabel.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadLabel.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    uploadLabel.addEventListener('drop', handleDrop, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        uploadLabel.style.borderColor = '#007bff';
        uploadLabel.style.backgroundColor = 'rgba(0, 123, 255, 0.1)';
    }

    function unhighlight(e) {
        uploadLabel.style.borderColor = 'transparent';
        uploadLabel.style.backgroundColor = '';
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (validateImageFiles(files)) {
            handleImagePreview(files, previewContainer, index);
        }
    }
}

function setupModelEntry(index) {
    const categorySelect = document.getElementById(`category_${index}`);
    const modelSelect = document.getElementById(`model_${index}`);

    if (categorySelect) {
        categorySelect.addEventListener('change', function () {
            handleCategoryChange(index, this.value);
        });
    }

    if (modelSelect) {
        modelSelect.addEventListener('change', function () {
            handleModelChange(index, this.value);
        });
    }

    // Setup branch autocomplete
    setupBranchAutocomplete(index);

    // Setup image upload preview
    setupImageUpload(index);

    // Setup drag and drop for images
    setupDragAndDrop(index);
}
// دوال إدارة الفروع المحسنة
function fetchBranches(searchTerm, index) {
    fetch(`/get_branches?search=${encodeURIComponent(searchTerm)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSuggestions(data.branches, index);
            }
        })
        .catch(error => {
            console.error('Error fetching branches:', error);
        });
}

function showSuggestions(branches, index) {
    const suggestionsContainer = document.getElementById(`suggestions_${index}`);
    if (!suggestionsContainer) return;

    suggestionsContainer.innerHTML = '';

    if (branches.length === 0) {
        // لا تظهر أي رسالة عند عدم وجود فروع محفوظة
        suggestionsContainer.style.display = 'none';
        return;
    } else {
        branches.forEach(branch => {
            const suggestion = document.createElement('div');
            suggestion.className = 'autocomplete-suggestion';
            suggestion.innerHTML = `
                    <div class="branch-suggestion">
                        <strong>${branch.name}</strong>
                        <small>كود: ${branch.code}</small>
                    </div>
                `;

            suggestion.addEventListener('click', function () {
                selectBranch(branch.name, branch.code, true, index);
            });

            suggestionsContainer.appendChild(suggestion);
        });
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
        if (isLocked) {
            // 🔧 الحل: استخدام readonly بدلاً من disabled لضمان إرسال القيمة مع النموذج
            shopCodeInput.readOnly = true;
            shopCodeInput.disabled = false; // تأكد من عدم التعطيل
            shopCodeInput.classList.add('locked-input');
            shopCodeInput.title = 'This branch is saved - code cannot be edited';

            // إظهار رسالة للمستخدم
            // رسالة القفل تم إزالتها
        } else {
            shopCodeInput.disabled = false;
            shopCodeInput.classList.remove('locked-input');
            shopCodeInput.title = '';
        }

        hideSuggestions(index);
    }
}

function showBranchLockedMessage(index) {
    // إنشاء رسالة تنبيه مؤقتة
    const messageDiv = document.createElement('div');
    messageDiv.className = 'branch-locked-message';
    // Remove the saved branch message - no longer needed
    return; // Skip showing the message

    // إضافة الرسالة بجانب حقل كود الفرع
    const shopCodeInput = document.getElementById(`shop_code_${index}`);
    if (shopCodeInput && shopCodeInput.parentNode) {
        shopCodeInput.parentNode.appendChild(messageDiv);

        // إزالة الرسالة بعد 3 ثوان
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 3000);
    }
}

// تحسين دالة fetchBranchByCode لتفعيل القفل
function fetchBranchByCode(shopCode, index) {
    fetch(`/get_branch_by_code?code=${encodeURIComponent(shopCode)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const branchInput = document.getElementById(`branch_${index}`);
                if (branchInput) {
                    // اختيار الفرع مع تفعيل القفل
                    selectBranch(data.branch.name, data.branch.code, true, index);
                }
            }
        })
        .catch(error => {
            console.error('Error fetching branch by code:', error);
        });
}
// دالة إضافية للتأكد من إرسال shop_code مع النموذج
function ensureShopCodeSubmission() {
    const form = document.getElementById('dataEntryForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            // التأكد من أن جميع حقول shop_code تحتوي على قيم
            const shopCodeInputs = form.querySelectorAll('input[name^="shop_code_"]');

            shopCodeInputs.forEach(input => {
                if (input.readOnly && input.value) {
                    console.log(`✅ shop_code سيتم إرساله: ${input.name} = ${input.value}`);

                    // إضافة حقل مخفي إضافي كضمان
                    const hiddenBackup = document.createElement('input');
                    hiddenBackup.type = 'hidden';
                    hiddenBackup.name = input.name + '_readonly_backup';
                    hiddenBackup.value = input.value;
                    form.appendChild(hiddenBackup);
                }
            });
        });
    }
}

// تشغيل الدالة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function () {
    ensureShopCodeSubmission();
});


// دالة لمسح جميع البيانات المؤقتة والحالة
function clearAllTempData() {
    console.log('🧹 مسح جميع البيانات المؤقتة...');

    // مسح الصور المحددة
    if (typeof selectedFiles !== 'undefined') {
        selectedFiles = {};
    }

    // مسح أي متغيرات مؤقتة أخرى
    if (typeof currentSuggestions !== 'undefined') {
        currentSuggestions = [];
    }

    // إزالة جميع الرسائل المؤقتة
    const tempMessages = document.querySelectorAll('.branch-lock-message, .flash-message');
    tempMessages.forEach(msg => msg.remove());

    // إزالة جميع الحقول المخفية المؤقتة
    const hiddenInputs = document.querySelectorAll('input[type="hidden"][id*="shop_code_hidden"]');
    hiddenInputs.forEach(input => input.remove());

    console.log('✅ تم مسح جميع البيانات المؤقتة');
}

// استدعاء مسح البيانات المؤقتة عند إعادة التعيين
document.addEventListener('DOMContentLoaded', function () {
    // إضافة مستمع لزر إعادة التعيين إذا كان موجوداً
    const resetButtons = document.querySelectorAll('button[type="reset"], .reset-btn');
    resetButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            clearAllTempData();
            resetFormState();
        });
    });
});

// Comment functionality
function setupCommentFunctionality(index) {
    setTimeout(function () {
        const addCommentBtn = document.querySelector(`[data-index="${index}"] .add-comment-btn`);
        const commentContainer = document.querySelector(`[data-index="${index}"] .comment-input-container`);
        const removeCommentBtn = document.querySelector(`[data-index="${index}"] .remove-comment-btn`);
        const commentTextarea = document.querySelector(`[data-index="${index}"] .comment-textarea`);

        if (addCommentBtn && commentContainer && removeCommentBtn) {
            // Add comment button click
            addCommentBtn.addEventListener('click', function () {
                commentContainer.style.display = 'block';
                addCommentBtn.style.display = 'none';
                if (commentTextarea) {
                    commentTextarea.focus();
                }
            });

            // Remove comment button click
            removeCommentBtn.addEventListener('click', function () {
                commentContainer.style.display = 'none';
                addCommentBtn.style.display = 'inline-flex';
                if (commentTextarea) {
                    commentTextarea.value = '';
                }
            });

            // Auto-resize textarea
            if (commentTextarea) {
                commentTextarea.addEventListener('input', function () {
                    this.style.height = 'auto';
                    this.style.height = this.scrollHeight + 'px';
                });
            }
        }
    }, 100);
}

// Add new model entry
function addNewModelEntry() {
    const container = document.getElementById('modelsContainer');
    const newModelEntry = createModelEntryHTML(modelCounter);

    container.insertAdjacentHTML('beforeend', newModelEntry);
    setupModelEntry(modelCounter);

    // Load categories for the new model entry
    loadCategoriesForNewModel(modelCounter);

    modelCounter++;

    // Scroll to the new entry
    const newEntry = document.querySelector(`[data-index="${modelCounter - 1}"]`);
    if (newEntry) {
        newEntry.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Create HTML for new model entry
function createModelEntryHTML(index) {
    return `
        <div class="model-entry" data-index="${index}">
            <div class="model-entry-header">
                <h3>Model Entry ${index + 1}</h3>
                <button type="button" class="admin-btn admin-btn-logout" style="height: 40px; min-width: 70px;" onclick="removeModelEntry(${index})" title="Remove Model">
                    <span class="btn-icon" style="font-size: 16px; margin-bottom: 2px;">🗑️</span>
                    <span class="btn-text" style="font-size: 10px;">Remove</span>
                </button>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label for="branch_${index}">Branch Name:</label>
                    <div class="autocomplete-container">
                        <input type="text" id="branch_${index}" name="branch_${index}" class="branch-input" 
                            placeholder="Type branch name or shop code..." required autocomplete="off">
                        <div class="autocomplete-suggestions" id="suggestions_${index}"></div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="shop_code_${index}">Shop Code:</label>
                    <input type="text" id="shop_code_${index}" name="shop_code_${index}" class="shop-code-input" 
                        placeholder="Enter shop code..." required autocomplete="off">
                </div>
            </div>
            
            <div class="form-group">
                <label for="category_${index}">Category:</label>
                <select id="category_${index}" name="category_${index}" class="category-select" required>
                    <option value="">Select Category</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="model_${index}">Model:</label>
                <select id="model_${index}" name="model_${index}" class="model-select" required disabled>
                    <option value="">Select Model</option>
                </select>
            </div>
            
            <div class="display-type-section" style="display: none;">
                <h4>Display Type</h4>
                <div class="form-group">
                    <select name="display_type_${index}" class="display-type-select" required>
                        <option value="">Select Display Type</option>
                    </select>
                </div>
            </div>
            
            <div class="pop-material-section" style="display: none;">
                <h4>POP Material</h4>
                <div class="checklist-container">
                    <!-- Checklist items will be populated by JavaScript -->
                </div>
            </div>
            
            <div class="comment-section" style="display: none;">
                <h4>💬 Comments (Optional)</h4>
                <div class="form-group">
                    <button type="button" class="admin-btn add-comment-btn" data-index="${index}" title="Add Comment">
                        <span class="btn-icon">💬</span>
                        <span class="btn-text">Comment</span>
                    </button>
                    <div class="comment-input-container" style="display: none;">
                        <label for="comment_${index}">Comment:</label>
                        <textarea id="comment_${index}" name="comment_${index}" class="comment-textarea" 
                            placeholder="Add your comment here... (unlimited characters)" 
                            rows="4"></textarea>
                        <div class="comment-actions">
                            <button type="button" class="admin-btn admin-btn-logout remove-comment-btn" style="height: 35px; min-width: 60px;">
                                <span class="btn-icon" style="font-size: 14px; margin-bottom: 2px;">🗑️</span>
                                <span class="btn-text" style="font-size: 9px;">Remove</span>
                            </button>
                            <small class="comment-info">💡 Comments will appear in reports</small>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="image-upload-section" style="display: none;">
                <h4>📸 Image Upload</h4>
                <div class="form-group">
                    <label for="images_${index}" class="file-upload-label">
                        <span class="upload-icon">📁</span>
                        <span class="upload-text">Choose Images</span>
                        <span class="upload-hint">(Max 10 images)</span>
                    </label>
                    <input type="file" id="images_${index}" name="images_${index}" multiple accept="image/*,.webp,.avif"
                        class="image-upload" style="display: none;" max="10">
                    <div class="upload-info">
                        <small>💡 You can select multiple images at once</small>
                    </div>
                    <div class="image-preview"></div>
                </div>
            </div>
        </div>
    `;
}

// Remove model entry
function removeModelEntry(index) {
    const modelEntry = document.querySelector(`[data-index="${index}"]`);
    if (modelEntry) {
        // Clean up selected files for this model
        if (selectedFiles && selectedFiles[index]) {
            delete selectedFiles[index];
        }

        modelEntry.remove();

        // Update remaining model entry headers
        updateModelEntryHeaders();
    }
}

// Update model entry headers after removal
function updateModelEntryHeaders() {
    const modelEntries = document.querySelectorAll('.model-entry');
    modelEntries.forEach((entry, index) => {
        const header = entry.querySelector('h3');
        if (header) {
            header.textContent = `Model Entry ${index + 1}`;
        }
    });
}

// Load categories for a specific new model entry
function loadCategoriesForNewModel(index) {
    fetch('/get_dynamic_data/categories')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const categorySelect = document.getElementById(`category_${index}`);
                if (categorySelect) {
                    // Clear existing options
                    categorySelect.innerHTML = '';

                    // Add default option
                    const defaultOption = document.createElement('option');
                    defaultOption.value = '';
                    defaultOption.textContent = 'Select Category';
                    categorySelect.appendChild(defaultOption);

                    // Add categories from database
                    data.data.forEach(category => {
                        const option = document.createElement('option');
                        option.value = category;
                        option.textContent = category;
                        categorySelect.appendChild(option);
                    });
                }
            }
        })
        .catch(error => {
            console.error('Error loading categories for new model:', error);
        });
}

// Model Image Display Functions
function setupModelImageDisplay(index, category) {
    const modelSelect = document.getElementById(`model_${index}`);

    if (!modelSelect) return;

    // Create image icon container if it doesn't exist
    let imageContainer = document.querySelector(`[data-index="${index}"] .model-image-container`);
    if (!imageContainer) {
        imageContainer = document.createElement('div');
        imageContainer.className = 'model-image-container';
        imageContainer.style.display = 'inline-block';
        imageContainer.style.marginLeft = '10px';

        // Insert after the model select
        modelSelect.parentNode.appendChild(imageContainer);
    }

    // Remove existing event listener to avoid duplicates
    const existingHandler = modelSelect.getAttribute('data-image-handler');
    if (existingHandler) {
        modelSelect.removeEventListener('change', window[existingHandler]);
    }

    // Create unique handler function
    const handlerName = `modelImageHandler_${index}`;
    window[handlerName] = function () {
        const selectedModel = this.value;
        updateModelImageIcon(index, category, selectedModel, imageContainer);
    };

    // Add event listener and mark it
    modelSelect.addEventListener('change', window[handlerName]);
    modelSelect.setAttribute('data-image-handler', handlerName);
}

function updateModelImageIcon(index, category, model, container) {
    // Clear existing content
    container.innerHTML = '';

    if (!model) return;

    // Check if model has an image
    fetch(`/get_model_image/${encodeURIComponent(category)}/${encodeURIComponent(model)}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.image_url) {
                // Create image icon with text
                const imageIcon = document.createElement('span');
                imageIcon.className = 'model-image-icon';
                imageIcon.innerHTML = '📖 View Guide';
                imageIcon.style.cursor = 'pointer';
                imageIcon.style.fontSize = '13px';
                imageIcon.style.color = 'white';
                imageIcon.style.marginLeft = '12px';
                imageIcon.style.padding = '8px 16px';
                imageIcon.style.borderRadius = '8px';
                imageIcon.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                imageIcon.style.border = 'none';
                imageIcon.style.fontWeight = '600';
                imageIcon.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.3)';
                imageIcon.style.transition = 'all 0.3s ease';
                imageIcon.title = 'Click to view model guide image';

                // Add hover effect
                imageIcon.addEventListener('mouseenter', function () {
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 6px 20px rgba(118, 75, 162, 0.4)';
                });

                imageIcon.addEventListener('mouseleave', function () {
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.3)';
                });

                // Add click event to show popup
                imageIcon.addEventListener('click', function () {
                    showModelImagePopup(model, data.image_url);
                });

                container.appendChild(imageIcon);
            }
        })
        .catch(error => {
            console.error('Error checking model image:', error);
        });
}

function showModelImagePopup(modelName, imageUrl) {
    // Create popup overlay
    const overlay = document.createElement('div');
    overlay.className = 'model-image-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        cursor: pointer;
    `;

    // Create popup content
    const popup = document.createElement('div');
    popup.className = 'model-image-popup';
    popup.style.cssText = `
        background: white;
        border-radius: 10px;
        padding: 20px;
        max-width: 90%;
        max-height: 90%;
        position: relative;
        cursor: default;
    `;

    // Prevent popup from closing when clicking on content
    popup.addEventListener('click', function (e) {
        e.stopPropagation();
    });

    // Create close button
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '×';
    closeBtn.style.cssText = `
        position: absolute;
        top: 10px;
        right: 15px;
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
        color: #666;
    `;
    closeBtn.addEventListener('click', function () {
        document.body.removeChild(overlay);
    });

    // Create title
    const title = document.createElement('h3');
    title.textContent = `Model Guide: ${modelName}`;
    title.style.cssText = `
        margin: 0 0 15px 0;
        color: #333;
        text-align: center;
    `;

    // Create image
    const img = document.createElement('img');
    img.src = imageUrl;
    img.alt = `${modelName} Guide Image`;
    img.style.cssText = `
        max-width: 100%;
        max-height: 70vh;
        display: block;
        margin: 0 auto;
        border-radius: 5px;
        cursor: grab;
        transition: transform 0.3s ease;
    `;

    // Add zoom and pan functionality
    addImageZoomPan(img);

    // Handle image load error
    img.addEventListener('error', function () {
        this.style.display = 'none';
        const errorMsg = document.createElement('p');
        errorMsg.textContent = 'Failed to load image';
        errorMsg.style.cssText = 'text-align: center; color: #666; padding: 20px;';
        popup.appendChild(errorMsg);
    });

    // Assemble popup
    popup.appendChild(closeBtn);
    popup.appendChild(title);
    popup.appendChild(img);
    overlay.appendChild(popup);

    // Close on overlay click
    overlay.addEventListener('click', function () {
        document.body.removeChild(overlay);
    });

    // Close on Escape key
    const handleEscape = function (e) {
        if (e.key === 'Escape') {
            document.body.removeChild(overlay);
            document.removeEventListener('keydown', handleEscape);
        }
    };
    document.addEventListener('keydown', handleEscape);

    // Add to page
    document.body.appendChild(overlay);
}

// Image Zoom and Pan Functionality - Enhanced Version
function addImageZoomPan(img) {
    let scale = 1;
    let panning = false;
    let zooming = false;
    let pointX = 0;
    let pointY = 0;
    let start = { x: 0, y: 0 };

    // Touch tracking for better mobile experience
    let initialDistance = 0;
    let initialScale = 1;
    let initialCenter = { x: 0, y: 0 };

    // Set transform origin to center
    img.style.transformOrigin = 'center center';
    img.style.transition = 'none'; // Remove any CSS transitions that might interfere

    // Apply transform function with safety checks
    function applyTransform() {
        // Safety checks to prevent invalid values
        if (isNaN(scale) || scale <= 0) {
            scale = 1;
        }
        if (isNaN(pointX)) {
            pointX = 0;
        }
        if (isNaN(pointY)) {
            pointY = 0;
        }

        // Limit extreme positions to keep image visible
        const maxOffset = 500;
        pointX = Math.max(-maxOffset, Math.min(maxOffset, pointX));
        pointY = Math.max(-maxOffset, Math.min(maxOffset, pointY));

        img.style.transform = `translate(${pointX}px, ${pointY}px) scale(${scale})`;
        img.style.cursor = scale > 1 ? 'grab' : 'grab';
    }

    // Mouse wheel zoom (desktop)
    img.addEventListener('wheel', function (e) {
        e.preventDefault();

        const delta = e.deltaY > 0 ? 0.9 : 1.1;
        const oldScale = scale;
        scale *= delta;

        // Limit zoom range
        scale = Math.min(Math.max(0.5, scale), 5);

        // Zoom towards mouse position
        const rect = img.getBoundingClientRect();
        const mouseX = e.clientX - rect.left - rect.width / 2;
        const mouseY = e.clientY - rect.top - rect.height / 2;

        const scaleChange = scale / oldScale;
        pointX = mouseX - (mouseX - pointX) * scaleChange;
        pointY = mouseY - (mouseY - pointY) * scaleChange;

        applyTransform();
    });

    // Touch start
    img.addEventListener('touchstart', function (e) {
        e.preventDefault();

        if (e.touches.length === 2) {
            // Two finger pinch start
            zooming = true;
            panning = false;

            initialDistance = getDistance(e.touches[0], e.touches[1]);

            // Safety check: ensure we have a valid distance
            if (initialDistance < 10) {
                initialDistance = 50; // Set a minimum distance
            }

            initialScale = scale;

            // Calculate center point between two fingers
            initialCenter = {
                x: (e.touches[0].clientX + e.touches[1].clientX) / 2,
                y: (e.touches[0].clientY + e.touches[1].clientY) / 2
            };

        } else if (e.touches.length === 1 && !zooming) {
            // Single finger pan start
            panning = true;
            start = {
                x: e.touches[0].clientX - pointX,
                y: e.touches[0].clientY - pointY
            };
            img.style.cursor = 'grabbing';
        }
    });

    // Touch move
    img.addEventListener('touchmove', function (e) {
        e.preventDefault();

        if (e.touches.length === 2 && zooming) {
            // Two finger pinch zoom - SIMPLIFIED to prevent disappearing
            const currentDistance = getDistance(e.touches[0], e.touches[1]);

            // Prevent division by zero or very small numbers
            if (initialDistance > 10) {
                const scaleChange = currentDistance / initialDistance;
                const newScale = initialScale * scaleChange;

                // Limit zoom range with safety checks
                scale = Math.min(Math.max(0.5, newScale), 5);

                // Simple zoom without complex position calculations
                // This prevents the image from disappearing
                applyTransform();
            }

        } else if (e.touches.length === 1 && panning && !zooming) {
            // Single finger pan
            pointX = e.touches[0].clientX - start.x;
            pointY = e.touches[0].clientY - start.y;
            applyTransform();
        }
    });

    // Touch end - IMPROVED: Preserve zoom level
    img.addEventListener('touchend', function (e) {
        if (e.touches.length === 0) {
            // All fingers lifted - preserve current state
            zooming = false;
            panning = false;
            img.style.cursor = scale > 1 ? 'grab' : 'grab';

            // Smooth transition back to normal cursor
            setTimeout(() => {
                img.style.cursor = scale > 1 ? 'grab' : 'grab';
            }, 100);

        } else if (e.touches.length === 1 && zooming) {
            // Switched from two fingers to one - stop zooming, allow panning
            zooming = false;
            if (scale > 1) {
                panning = true;
                start = {
                    x: e.touches[0].clientX - pointX,
                    y: e.touches[0].clientY - pointY
                };
            }
        }
    });

    // Mouse events for desktop pan
    img.addEventListener('mousedown', function (e) {
        if (scale > 1) {
            e.preventDefault();
            panning = true;
            start = { x: e.clientX - pointX, y: e.clientY - pointY };
            img.style.cursor = 'grabbing';
        }
    });

    document.addEventListener('mousemove', function (e) {
        if (panning && !zooming) {
            e.preventDefault();
            pointX = e.clientX - start.x;
            pointY = e.clientY - start.y;
            applyTransform();
        }
    });

    document.addEventListener('mouseup', function () {
        if (panning) {
            panning = false;
            img.style.cursor = scale > 1 ? 'grab' : 'grab';
        }
    });

    // Double-tap to reset zoom (mobile) - Enhanced
    let lastTap = 0;
    let tapCount = 0;

    img.addEventListener('touchend', function (e) {
        if (e.touches.length === 0) {
            const currentTime = new Date().getTime();
            const tapLength = currentTime - lastTap;

            if (tapLength < 300 && tapLength > 0) {
                tapCount++;
                if (tapCount === 2) {
                    // Double tap detected
                    e.preventDefault();
                    if (scale > 1) {
                        resetZoom();
                    } else {
                        // Zoom in to 2x on double tap
                        scale = 2;
                        applyTransform();
                    }
                    tapCount = 0;
                }
            } else {
                tapCount = 1;
            }

            lastTap = currentTime;

            // Reset tap count after delay
            setTimeout(() => {
                tapCount = 0;
            }, 300);
        }
    });

    // Double-click to reset zoom (desktop)
    img.addEventListener('dblclick', function (e) {
        e.preventDefault();
        if (scale > 1) {
            resetZoom();
        } else {
            scale = 2;
            applyTransform();
        }
    });

    // Reset zoom function
    function resetZoom() {
        scale = 1;
        pointX = 0;
        pointY = 0;
        img.style.transition = 'transform 0.3s ease';
        applyTransform();

        setTimeout(() => {
            img.style.transition = 'none';
        }, 300);
    }

    // Calculate distance between two touch points
    function getDistance(touch1, touch2) {
        const dx = touch1.clientX - touch2.clientX;
        const dy = touch1.clientY - touch2.clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    // Prevent context menu on long press
    img.addEventListener('contextmenu', function (e) {
        e.preventDefault();
    });

    // Prevent image drag
    img.addEventListener('dragstart', function (e) {
        e.preventDefault();
    });
}

// Save Popup Functions
function showSavePopup(message, isSuccess = false) {
    // Remove existing popup if any
    hideSavePopup();

    // Create popup overlay
    const overlay = document.createElement('div');
    overlay.id = 'savePopupOverlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;

    // Create popup card
    const popup = document.createElement('div');
    popup.style.cssText = `
        background: white;
        padding: 30px 40px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 18px;
        font-weight: 600;
        color: #333;
        min-width: 200px;
        transform: scale(0.8);
        transition: transform 0.3s ease;
    `;

    popup.textContent = message;
    overlay.appendChild(popup);
    document.body.appendChild(overlay);

    // Animate in
    setTimeout(() => {
        overlay.style.opacity = '1';
        popup.style.transform = 'scale(1)';
    }, 10);

    // Auto-hide success message after 2 seconds
    if (isSuccess) {
        setTimeout(() => {
            hideSavePopup();
        }, 2000);
    }
}

function hideSavePopup() {
    const overlay = document.getElementById('savePopupOverlay');
    if (overlay) {
        overlay.style.opacity = '0';
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.parentNode.removeChild(overlay);
            }
        }, 300);
    }
}