// User Management JavaScript

let deleteUserId = null;

// Initialize user management
document.addEventListener('DOMContentLoaded', function() {
    initializeUserManagement();
});

function initializeUserManagement() {
    // Setup form submissions
    document.getElementById('userForm').addEventListener('submit', handleUserFormSubmit);
    document.getElementById('passwordForm').addEventListener('submit', handlePasswordFormSubmit);
    
    // Setup password confirmation validation
    document.getElementById('confirm-password').addEventListener('input', validatePasswordConfirmation);
}

function showAddUserModal() {
    document.getElementById('user-modal-title').textContent = 'Add New User';
    document.getElementById('user-id').value = '';
    document.getElementById('user-name').value = '';
    document.getElementById('user-full-name').value = '';
    document.getElementById('user-company-code').value = '';
    document.getElementById('user-password').value = '';
    document.getElementById('user-password').required = true;
    document.getElementById('user-is-admin').checked = false;
    document.getElementById('password-help').style.display = 'none';
    
    document.getElementById('userModal').style.display = 'block';
}

function editUser(id, name, fullName, companyCode, isAdmin) {
    document.getElementById('user-modal-title').textContent = 'Edit User';
    document.getElementById('user-id').value = id;
    document.getElementById('user-name').value = name;
    document.getElementById('user-full-name').value = fullName || '';
    document.getElementById('user-company-code').value = companyCode;
    document.getElementById('user-password').value = '';
    document.getElementById('user-password').required = false;
    document.getElementById('user-is-admin').checked = isAdmin;
    document.getElementById('password-help').style.display = 'block';
    
    document.getElementById('userModal').style.display = 'block';
}

function editUserFromButton(button) {
    const id = button.dataset.userId;
    const name = button.dataset.userName;
    const fullName = button.dataset.userFullName;
    const companyCode = button.dataset.userCode;
    const isAdmin = button.dataset.userAdmin === 'True';
    
    editUser(id, name, fullName, companyCode, isAdmin);
}

function deleteUser(id, name) {
    deleteUserId = id;
    document.getElementById('delete-user-name').textContent = name;
    document.getElementById('deleteUserModal').style.display = 'block';
}

function deleteUserFromButton(button) {
    const id = button.dataset.userId;
    const name = button.dataset.userName;
    
    deleteUser(id, name);
}

function confirmDeleteUser() {
    if (!deleteUserId) return;
    
    const data = {
        action: 'delete',
        id: deleteUserId
    };
    
    fetch('/manage_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            showMessage('Error: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error deleting user:', error);
        showMessage('Error deleting user', 'error');
    })
    .finally(() => {
        closeDeleteUserModal();
    });
}

function handleUserFormSubmit(e) {
    e.preventDefault();
    
    const userId = document.getElementById('user-id').value;
    const name = document.getElementById('user-name').value;
    const fullName = document.getElementById('user-full-name').value.trim() || null;
    const companyCode = document.getElementById('user-company-code').value;
    const password = document.getElementById('user-password').value;
    const isAdmin = document.getElementById('user-is-admin').checked;
    
    // Validation
    if (!name || !companyCode) {
        showMessage('Please fill in all required fields', 'error');
        return;
    }
    
    if (!userId && !password) {
        showMessage('Password is required for new users', 'error');
        return;
    }
    
    if (password && password.length < 6) {
        showMessage('Password must be at least 6 characters long', 'error');
        return;
    }
    
    const data = {
        action: userId ? 'edit' : 'add',
        id: userId || undefined,
        name: name,
        full_name: fullName,
        company_code: companyCode,
        password: password || undefined,
        is_admin: isAdmin
    };
    
    fetch('/manage_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            closeUserModal();
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            showMessage('Error: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error saving user:', error);
        showMessage('Error saving user', 'error');
    });
}

function showChangePasswordModal() {
    document.getElementById('current-password').value = '';
    document.getElementById('new-password').value = '';
    document.getElementById('confirm-password').value = '';
    document.getElementById('passwordModal').style.display = 'block';
}

function handlePasswordFormSubmit(e) {
    e.preventDefault();
    
    const currentPassword = document.getElementById('current-password').value;
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    // Validation
    if (!currentPassword || !newPassword || !confirmPassword) {
        showMessage('Please fill in all fields', 'error');
        return;
    }
    
    if (newPassword.length < 6) {
        showMessage('New password must be at least 6 characters long', 'error');
        return;
    }
    
    if (newPassword !== confirmPassword) {
        showMessage('New passwords do not match', 'error');
        return;
    }
    
    const data = {
        current_password: currentPassword,
        new_password: newPassword
    };
    
    fetch('/change_admin_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            closePasswordModal();
        } else {
            showMessage('Error: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error changing password:', error);
        showMessage('Error changing password', 'error');
    });
}

function validatePasswordConfirmation() {
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    if (confirmPassword && newPassword !== confirmPassword) {
        document.getElementById('confirm-password').setCustomValidity('Passwords do not match');
    } else {
        document.getElementById('confirm-password').setCustomValidity('');
    }
}

function closeUserModal() {
    document.getElementById('userModal').style.display = 'none';
}

function closePasswordModal() {
    document.getElementById('passwordModal').style.display = 'none';
}

function closeDeleteUserModal() {
    document.getElementById('deleteUserModal').style.display = 'none';
    deleteUserId = null;
}

function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.flash-message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `flash-message alert alert-${type}`;
    messageDiv.textContent = message;
    
    // Insert at top of container
    const container = document.querySelector('.admin-container');
    container.insertBefore(messageDiv, container.firstChild);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            messageDiv.remove();
        }, 300);
    }, 5000);
}

// Close modals when clicking outside
window.addEventListener('click', function(e) {
    const userModal = document.getElementById('userModal');
    const passwordModal = document.getElementById('passwordModal');
    const deleteUserModal = document.getElementById('deleteUserModal');
    
    if (e.target === userModal) {
        closeUserModal();
    }
    
    if (e.target === passwordModal) {
        closePasswordModal();
    }
    
    if (e.target === deleteUserModal) {
        closeDeleteUserModal();
    }
});

// Branches Management
let currentBranchUserId = null;

function showBranchesModal(button) {
    const userId = button.dataset.userId;
    const userName = button.dataset.userName;
    
    currentBranchUserId = userId;
    
    document.getElementById('branches-modal-title').textContent = `Manage Branches for ${userName}`;
    document.getElementById('branchesModal').style.display = 'block';
    
    loadUserBranches(userId);
}

function closeBranchesModal() {
    document.getElementById('branchesModal').style.display = 'none';
    currentBranchUserId = null;
}

function loadUserBranches(userId) {
    fetch(`/get_user_branches/${userId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayCurrentBranches(data.user_branches);
                populateAvailableBranches(data.all_branches, data.user_branches);
            } else {
                showMessage('Error loading branches: ' + data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error loading branches:', error);
            showMessage('Error loading branches', 'error');
        });
}

function displayCurrentBranches(userBranches) {
    const container = document.getElementById('current-branches-list');
    container.innerHTML = '';
    
    if (userBranches.length === 0) {
        container.innerHTML = '<p class="no-branches">No branches assigned</p>';
        return;
    }
    
    userBranches.forEach(branch => {
        const branchElement = document.createElement('div');
        branchElement.className = 'branch-item';
        branchElement.innerHTML = `
            <span class="branch-name">${branch}</span>
            <button class="btn btn-sm btn-danger" onclick="removeBranchFromUser('${branch}')">
                Remove
            </button>
        `;
        container.appendChild(branchElement);
    });
}

function populateAvailableBranches(allBranches, userBranches) {
    const select = document.getElementById('available-branches-select');
    select.innerHTML = '<option value="">Select a branch to add</option>';
    
    // Filter out branches already assigned to user
    const availableBranches = allBranches.filter(branch => !userBranches.includes(branch));
    
    availableBranches.forEach(branch => {
        const option = document.createElement('option');
        option.value = branch;
        option.textContent = branch;
        select.appendChild(option);
    });
    
    if (availableBranches.length === 0) {
        select.innerHTML = '<option value="">All branches already assigned</option>';
    }
}

function addBranchToUser() {
    const select = document.getElementById('available-branches-select');
    const branchName = select.value;
    
    if (!branchName) {
        showMessage('Please select a branch to add', 'error');
        return;
    }
    
    manageBranch('add', branchName);
}

function removeBranchFromUser(branchName) {
    if (confirm(`Are you sure you want to remove "${branchName}" from this user?`)) {
        manageBranch('remove', branchName);
    }
}

function manageBranch(action, branchName) {
    const data = {
        user_id: currentBranchUserId,
        action: action,
        branch_name: branchName
    };
    
    fetch('/manage_user_branches', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            loadUserBranches(currentBranchUserId); // Reload branches
            
            // Refresh the main table to show updated branches
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            showMessage('Error: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error managing branch:', error);
        showMessage('Error managing branch', 'error');
    });
}

// Close modals when clicking outside
window.addEventListener('click', function(e) {
    const branchesModal = document.getElementById('branchesModal');
    
    if (e.target === branchesModal) {
        closeBranchesModal();
    }
});

// Branch Management Functions
let currentManageUserId = null;
let currentAddUserId = null;
let addBranchCounter = 1;

function showManageBranchesModal(button) {
    const userId = button.dataset.userId;
    const userName = button.dataset.userName;
    
    currentManageUserId = userId;
    document.getElementById('manage-branches-user-name').textContent = userName;
    
    // Load current branches
    loadUserBranches(userId);
    

    
    document.getElementById('manageBranchesModal').style.display = 'block';
}

function closeManageBranchesModal() {
    console.log('Closing manage branches modal');
    document.getElementById('manageBranchesModal').style.display = 'none';
    currentManageUserId = null;
    
    // Clear inputs
    document.getElementById('new-branch-name').value = '';
    document.getElementById('new-branch-code').value = '';
}

function showAddBranchesModal(button) {
    const userId = button.dataset.userId;
    const userName = button.dataset.userName;
    
    currentAddUserId = userId;
    document.getElementById('add-branches-user-name').textContent = userName;
    
    // Reset form
    resetAddBranchesForm();
    
    document.getElementById('addBranchesModal').style.display = 'block';
}

function closeAddBranchesModal() {
    document.getElementById('addBranchesModal').style.display = 'none';
    currentAddUserId = null;
    resetAddBranchesForm();
}

function loadUserBranches(userId) {
    const branchesContainer = document.getElementById('current-branches-list');
    branchesContainer.innerHTML = '<div class="loading-branches">Loading branches...</div>';
    
    fetch(`/get_user_branches/${userId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayUserBranches(data.branches);
            } else {
                branchesContainer.innerHTML = '<div class="no-branches-found">Error loading branches</div>';
            }
        })
        .catch(error => {
            console.error('Error loading branches:', error);
            branchesContainer.innerHTML = '<div class="no-branches-found">Error loading branches</div>';
        });
}

function displayUserBranches(branches) {
    const branchesContainer = document.getElementById('current-branches-list');
    const countBadge = document.getElementById('branches-count');
    
    // تحديث عداد الفروع
    countBadge.textContent = `${branches.length} Branch${branches.length !== 1 ? 'es' : ''}`;
    
    if (branches.length === 0) {
        branchesContainer.innerHTML = `
            <div class="no-branches-found">
                <div class="empty-state">
                    <span class="empty-icon">🏢</span>
                    <p>No branches assigned yet</p>
                    <small>Add branches using the form below</small>
                </div>
            </div>
        `;
        return;
    }
    
    let html = '';
    branches.forEach(branch => {
        // تأكد من عرض الكود بشكل صحيح
        const shopCode = branch.shop_code && branch.shop_code !== 'N/A' ? branch.shop_code : 'No Code';
        const codeClass = branch.shop_code && branch.shop_code !== 'N/A' ? 'branch-code' : 'branch-code no-code';
        
        html += `
            <div class="branch-card" data-branch-id="${branch.id}">
                <div class="branch-info">
                    <div class="branch-name">${branch.branch_name}</div>
                    <div class="${codeClass}">${shopCode}</div>
                </div>
                <button class="remove-branch-btn" onclick="removeBranchFromUser(${branch.id}, '${branch.branch_name}')" title="Remove Branch">
                    ×
                </button>
            </div>
        `;
    });
    
    branchesContainer.innerHTML = html;
}

function addBranchToUser() {
    console.log('addBranchToUser function called');
    
    const branchName = document.getElementById('new-branch-name').value.trim();
    const branchCode = document.getElementById('new-branch-code').value.trim();
    
    console.log('Branch Name:', branchName);
    console.log('Branch Code:', branchCode);
    console.log('Current Manage User ID:', currentManageUserId);
    
    if (!currentManageUserId) {
        showMessage('❌ Error: No user selected for branch management', 'error');
        return;
    }
    
    if (!branchName || !branchCode) {
        showMessage('⚠️ Please enter both branch name and code', 'error');
        return;
    }
    
    if (branchName.length < 2) {
        showMessage('⚠️ Branch name must be at least 2 characters long', 'error');
        return;
    }
    
    if (branchCode.length < 2) {
        showMessage('⚠️ Branch code must be at least 2 characters long', 'error');
        return;
    }
    
    // Disable button to prevent double clicks
    const addButton = document.querySelector('.add-branch-btn-modern');
    if (addButton) {
        addButton.disabled = true;
        addButton.innerHTML = '<span class="btn-icon">⏳</span><span class="btn-text">Adding...</span>';
    }
    
    const data = {
        action: 'add_branch',
        user_id: currentManageUserId,
        branch_name: branchName,
        branch_code: branchCode
    };
    
    console.log('Sending request with data:', data);
    
    fetch('/manage_user_branches', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        if (data.success) {
            // Clear inputs
            document.getElementById('new-branch-name').value = '';
            document.getElementById('new-branch-code').value = '';
            
            // Show success message
            showMessage('✅ Branch added successfully!', 'success');
            
            // Reload branches without closing modal
            loadUserBranches(currentManageUserId);
            
            // Update the main page branch count in background
            updateUserBranchCount(currentManageUserId);
            
        } else {
            console.error('Server returned error:', data.message);
            let errorMsg = data.message;
            
            // Make error messages more user-friendly
            if (errorMsg.includes('UNIQUE constraint failed')) {
                errorMsg = '❌ This branch code is already used. Please choose a different code.';
            } else if (errorMsg.includes('already exists')) {
                errorMsg = '❌ This branch already exists for this user.';
            } else if (errorMsg.includes('shop_code')) {
                errorMsg = '❌ Branch code already exists. Please use a different code.';
            } else {
                errorMsg = '❌ ' + errorMsg;
            }
            
            showMessage(errorMsg, 'error');
        }
    })
    .catch(error => {
        console.error('Error adding branch:', error);
        showMessage('❌ Error adding branch: ' + error.message, 'error');
    })
    .finally(() => {
        // Re-enable button
        if (addButton) {
            addButton.disabled = false;
            addButton.innerHTML = '<span class="btn-icon">➕</span><span class="btn-text">Add Branch</span>';
        }
    });
}

function removeBranchFromUser(branchId, branchName) {
    if (!confirm(`Are you sure you want to remove branch "${branchName}"?`)) {
        return;
    }
    
    const data = {
        action: 'remove_branch',
        user_id: currentManageUserId,
        branch_id: branchId
    };
    
    fetch('/manage_user_branches', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message
            showMessage('🗑️ Branch removed successfully!', 'success');
            
            // Reload branches without closing modal
            loadUserBranches(currentManageUserId);
            
            // Update the main page branch count in background
            updateUserBranchCount(currentManageUserId);
            
        } else {
            showMessage('❌ Error removing branch: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error removing branch:', error);
        showMessage('❌ Error removing branch', 'error');
    });
}

function updateUserBranchCount(userId) {
    // Update the branch count in the main table without reloading
    fetch(`/get_user_branches/${userId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Find the user row in the main table
                const userRows = document.querySelectorAll('tbody tr');
                userRows.forEach(row => {
                    const editBtn = row.querySelector('.edit-user-btn');
                    if (editBtn && editBtn.dataset.userId == userId) {
                        const branchesCell = row.querySelector('.branches-cell');
                        if (branchesCell) {
                            const branchCount = data.branches.length;
                            
                            if (branchCount > 0) {
                                // Update branch count display
                                const countBadge = branchesCell.querySelector('.badge-info');
                                if (countBadge) {
                                    countBadge.textContent = `${branchCount} Branch${branchCount !== 1 ? 'es' : ''}`;
                                }
                                
                                // Update branch preview
                                const previewDiv = branchesCell.querySelector('.branches-preview small');
                                if (previewDiv && data.branches.length > 0) {
                                    const branchNames = data.branches.slice(0, 5).map(b => b.branch_name).join(', ');
                                    previewDiv.textContent = branchNames;
                                }
                            }
                        }
                    }
                });
            }
        })
        .catch(error => {
            console.error('Error updating branch count:', error);
        });
}



function resetAddBranchesForm() {
    const container = document.getElementById('add-branches-container');
    container.innerHTML = `
        <div class="branch-entry" data-index="0">
            <div class="branch-row">
                <input type="text" name="branch_names[]" placeholder="Branch Name" required>
                <input type="text" name="branch_codes[]" placeholder="Branch Code" required>
                <button type="button" class="btn btn-danger btn-sm remove-branch-btn" onclick="removeBranchFromAdd(0)" style="display: none;">Remove</button>
            </div>
        </div>
    `;
    addBranchCounter = 1;
}

function addAnotherBranchToAdd() {
    const container = document.getElementById('add-branches-container');
    const newBranch = document.createElement('div');
    newBranch.className = 'branch-entry';
    newBranch.setAttribute('data-index', addBranchCounter);
    
    newBranch.innerHTML = `
        <div class="branch-row">
            <input type="text" name="branch_names[]" placeholder="Branch Name" required>
            <input type="text" name="branch_codes[]" placeholder="Branch Code" required>
            <button type="button" class="btn btn-danger btn-sm remove-branch-btn" onclick="removeBranchFromAdd(${addBranchCounter})">Remove</button>
        </div>
    `;
    
    container.appendChild(newBranch);
    addBranchCounter++;
    
    updateRemoveButtonsInAdd();
}

function removeBranchFromAdd(index) {
    const branchEntry = document.querySelector(`#add-branches-container [data-index="${index}"]`);
    if (branchEntry) {
        branchEntry.remove();
        updateRemoveButtonsInAdd();
    }
}

function updateRemoveButtonsInAdd() {
    const branches = document.querySelectorAll('#add-branches-container .branch-entry');
    branches.forEach((branch, index) => {
        const removeBtn = branch.querySelector('.remove-branch-btn');
        if (branches.length > 1) {
            removeBtn.style.display = 'inline-block';
        } else {
            removeBtn.style.display = 'none';
        }
    });
}

function saveBranchesToUser() {
    const branchNames = Array.from(document.querySelectorAll('#add-branches-container input[name="branch_names[]"]'))
                           .map(input => input.value.trim())
                           .filter(name => name);
    
    const branchCodes = Array.from(document.querySelectorAll('#add-branches-container input[name="branch_codes[]"]'))
                           .map(input => input.value.trim())
                           .filter(code => code);
    
    if (branchNames.length === 0 || branchCodes.length === 0 || branchNames.length !== branchCodes.length) {
        alert('Please fill in all branch names and codes');
        return;
    }
    
    const data = {
        action: 'add_multiple_branches',
        user_id: currentAddUserId,
        branches: branchNames.map((name, index) => ({
            name: name,
            code: branchCodes[index]
        }))
    };
    
    fetch('/manage_user_branches', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            closeAddBranchesModal();
            location.reload();
        } else {
            alert('Error adding branches: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error adding branches:', error);
        alert('Error adding branches');
    });
}

// Close modals when clicking outside
window.onclick = function(event) {
    const manageBranchesModal = document.getElementById('manageBranchesModal');
    const addBranchesModal = document.getElementById('addBranchesModal');
    
    if (event.target === manageBranchesModal) {
        console.log('Clicked outside manage branches modal');
        closeManageBranchesModal();
    }
    if (event.target === addBranchesModal) {
        console.log('Clicked outside add branches modal');
        closeAddBranchesModal();
    }
}

// Prevent modal from closing when clicking inside
document.addEventListener('DOMContentLoaded', function() {
    const manageBranchesModal = document.getElementById('manageBranchesModal');
    const addBranchesModal = document.getElementById('addBranchesModal');
    
    if (manageBranchesModal) {
        const modalContent = manageBranchesModal.querySelector('.modal-content');
        if (modalContent) {
            modalContent.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
    }
    
    if (addBranchesModal) {
        const modalContent = addBranchesModal.querySelector('.modal-content');
        if (modalContent) {
            modalContent.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
    }
});