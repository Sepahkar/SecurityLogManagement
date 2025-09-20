// مدیریت نشان‌های کاربر (نسخه jQuery با delegation)
// توضیح: هندلرها به صورت delegated ثبت می‌شوند تا برای عناصر دینامیک هم کار کنند و از چندباره‌سازی جلوگیری شود.
// توجه: نسخه قدیمی مبتنی بر querySelectorAll غیر فعال شد تا از دوباره‌بایند شدن جلوگیری شود.
// function initializeUserBadges() { ... } — غیرفعال شد

// Function to get all removed users
function getRemovedUsers() {
    const removedUsers = [];
    document.querySelectorAll('.remove-user-btn[data-delete="true"]').forEach(function(btn) {
        const userBadge = btn.closest('.user-badge');
        const userId = userBadge.getAttribute('data-user-id');
        removedUsers.push(userId);
    });
    return removedUsers;
}

// Function to restore all hidden users
function restoreAllUsers() {
    document.querySelectorAll('.user-badge.hidden').forEach(function(badge) {
        badge.classList.remove('hidden');
        badge.style.display = 'inline-block';
        const removeBtn = badge.querySelector('.remove-user-btn');
        if (removeBtn) {
            removeBtn.setAttribute('data-delete', 'false');
        }
    });
}

// مدیریت دکمه‌های افزودن کاربر (نسخه jQuery با delegation)
// function initializeAddUserButtons() { ... } — غیرفعال شد

function addUserBadge(userId, username, fullname, taskId, role) {
    const container = document.querySelector(`.users-container[data-task-id="${taskId}"][data-role="${role}"]`);
    
    // Check if user already exists
    const existingBadge = container.querySelector(`.user-badge[data-user-id="${userId}"]`);
    if (existingBadge) {
        // If user exists but is hidden, restore it
        if (existingBadge.classList.contains('hidden')) {
            existingBadge.classList.remove('hidden');
            existingBadge.style.display = 'inline-block';
            const removeBtn = existingBadge.querySelector('.remove-user-btn');
            if (removeBtn) {
                removeBtn.setAttribute('data-delete', 'false');
            }
        }
        return;
    }
    
    // Create new user badge
    const userBadge = document.createElement('div');
    userBadge.className = 'user-badge adding';
    userBadge.setAttribute('data-user-id', userId);
    userBadge.setAttribute('data-new-user', 'true');
    
    userBadge.innerHTML = `
        <img class="person-small-avatar" src="/static/ConfigurationChangeRequest/images/personnel/${username.split('@')[0]}.jpg" 
        alt="${fullname}" title="${fullname}" 
        onerror="this.src='/static/ConfigurationChangeRequest/images/Avatar.png';" />
        <i class="fas fa-times remove-user-btn" data-delete="false" title="حذف کاربر"></i>
    `;
    
    // Insert before add button
    const addBtn = container.querySelector('.add-user-btn');
    container.insertBefore(userBadge, addBtn);
    
    // توجه: رویداد حذف به‌صورت delegated در $(document).ready ثبت شده است
    
    // Remove "no users" message if exists
    const noUsersMsg = container.querySelector('.text-muted');
    if (noUsersMsg) {
        noUsersMsg.remove();
    }
    
    // Remove adding class after animation completes
    setTimeout(function() {
        userBadge.classList.remove('adding');
    }, 800);
    
    // Update task data
    addUserToTaskData(taskId, role, userId, fullname, 'added');
    
    console.log('User added:', fullname, 'to task:', taskId, 'role:', role);
}

// Function to get all users for a specific task and role
function getUsersForTask(taskId, role) {
    const container = document.querySelector(`.users-container[data-task-id="${taskId}"][data-role="${role}"]`);
    const users = [];
    
    container.querySelectorAll('.user-badge:not(.hidden)').forEach(function(badge) {
        const userId = badge.getAttribute('data-user-id');
        const img = badge.querySelector('.person-small-avatar');
        const fullname = img.getAttribute('alt');
        users.push({
            id: userId,
            fullname: fullname
        });
    });
    
    return users;
}

// Function to get all changes (added/removed users) for all tasks
function getAllUserChanges() {
    const changes = {};
    
    document.querySelectorAll('.users-container').forEach(function(container) {
        const taskId = container.getAttribute('data-task-id');
        const role = container.getAttribute('data-role');
        const key = `${taskId}_${role}`;
        
        changes[key] = {
            taskId: taskId,
            role: role,
            added: [],
            removed: []
        };
        
        // Get added users (newly created badges)
        container.querySelectorAll('.user-badge:not(.hidden)').forEach(function(badge) {
            const userId = badge.getAttribute('data-user-id');
            const img = badge.querySelector('.person-small-avatar');
            const fullname = img.getAttribute('alt');
            
            changes[key].added.push({
                id: userId,
                fullname: fullname
            });
        });
        
        // Get removed users (hidden badges)
        container.querySelectorAll('.user-badge.hidden').forEach(function(badge) {
            const userId = badge.getAttribute('data-user-id');
            const img = badge.querySelector('.person-small-avatar');
            const fullname = img.getAttribute('alt');
            
            changes[key].removed.push({
                id: userId,
                fullname: fullname
            });
        });
    });
    
    return changes;
}

// Task Data Management Functions
function initializeTaskData() {
    // Initialize task data from existing table
    updateTaskData();
}

function updateTaskData() {
    const taskData = {
        tasks: [],
        changes: {
            tasksAdded: [],
            tasksRemoved: [],
            usersAdded: [],
            usersRemoved: [],
            tasksDeactivated: [],
            tasksReactivated: []
        }
    };
    
    // Get all tasks from table
    document.querySelectorAll('tbody tr').forEach(function(row) {
        const taskName = row.querySelector('td:first-child').textContent.trim();
        const taskId = row.getAttribute('data-task-id');
        const isActive = !row.classList.contains('inactive');
        const isNewTask = row.hasAttribute('data-new-task');
        
        // Get executors
        const executors = [];
        const executorContainer = row.querySelector('.users-container[data-role="E"]');
        if (executorContainer) {
            executorContainer.querySelectorAll('.user-badge:not(.hidden)').forEach(function(badge) {
                const userId = badge.getAttribute('data-user-id');
                const img = badge.querySelector('.person-small-avatar');
                const fullname = img.getAttribute('alt');
                const isNewUser = badge.hasAttribute('data-new-user');
                executors.push({
                    id: userId,
                    fullname: fullname,
                    action: isNewUser ? 'added' : 'existing'
                });
            });
        }
        
        // Get testers
        const testers = [];
        const testerContainer = row.querySelector('.users-container[data-role="T"]');
        if (testerContainer) {
            testerContainer.querySelectorAll('.user-badge:not(.hidden)').forEach(function(badge) {
                const userId = badge.getAttribute('data-user-id');
                const img = badge.querySelector('.person-small-avatar');
                const fullname = img.getAttribute('alt');
                const isNewUser = badge.hasAttribute('data-new-user');
                testers.push({
                    id: userId,
                    fullname: fullname,
                    action: isNewUser ? 'added' : 'existing'
                });
            });
        }
        
        const task = {
            id: taskId,
            name: taskName,
            isActive: isActive,
            isNew: isNewTask,
            executors: executors,
            testers: testers
        };
        
        taskData.tasks.push(task);
        
        // Track changes
        if (isNewTask) {
            taskData.changes.tasksAdded.push({
                id: taskId,
                name: taskName
            });
        }
        
        if (!isActive && !isNewTask) {
            taskData.changes.tasksDeactivated.push({
                id: taskId,
                name: taskName
            });
        }
    });
    
    // Track removed users
    document.querySelectorAll('.user-badge.hidden').forEach(function(badge) {
        const userId = badge.getAttribute('data-user-id');
        const img = badge.querySelector('.person-small-avatar');
        const fullname = img.getAttribute('alt');
        const container = badge.closest('.users-container');
        const taskId = container.getAttribute('data-task-id');
        const role = container.getAttribute('data-role');
        
        taskData.changes.usersRemoved.push({
            taskId: taskId,
            role: role,
            userId: userId,
            fullname: fullname
        });
    });
    
    // Update hidden input
    const taskDataInput = document.getElementById('task-data');
    if (taskDataInput) {
        taskDataInput.value = JSON.stringify(taskData);
    }
    
    console.log('Task data updated:', taskData);
    return taskData;
}

function addUserToTaskData(taskId, role, userId, fullname, action = 'added') {
    const taskDataInput = document.getElementById('task-data');
    if (!taskDataInput) return;
    
    let taskData = JSON.parse(taskDataInput.value || '{"tasks":[],"users":{"added":[],"removed":[]}}');
    
    // Find or create task
    let task = taskData.tasks.find(t => t.id == taskId);
    if (!task) {
        task = {
            id: taskId,
            name: '',
            isActive: true,
            executors: [],
            testers: []
        };
        taskData.tasks.push(task);
    }
    
    // Add user to appropriate role
    const userArray = role === 'E' ? task.executors : task.testers;
    const existingUser = userArray.find(u => u.id === userId);
    
    if (existingUser) {
        existingUser.action = action;
    } else {
        userArray.push({
            id: userId,
            fullname: fullname,
            action: action
        });
    }
    
    // Update input
    taskDataInput.value = JSON.stringify(taskData);
    console.log('User added to task data:', {taskId, role, userId, fullname, action});
}

function removeUserFromTaskData(taskId, role, userId) {
    const taskDataInput = document.getElementById('task-data');
    if (!taskDataInput) return;
    
    let taskData = JSON.parse(taskDataInput.value || '{"tasks":[],"users":{"added":[],"removed":[]}}');
    
    // Find task
    const task = taskData.tasks.find(t => t.id == taskId);
    if (!task) return;
    
    // Remove user from appropriate role
    const userArray = role === 'E' ? task.executors : task.testers;
    const userIndex = userArray.findIndex(u => u.id === userId);
    
    if (userIndex !== -1) {
        const user = userArray[userIndex];
        if (user.action === 'added') {
            // If user was just added, remove completely
            userArray.splice(userIndex, 1);
        } else {
            // If user was existing, mark as removed
            user.action = 'removed';
        }
    }
    
    // Update input
    taskDataInput.value = JSON.stringify(taskData);
    console.log('User removed from task data:', {taskId, role, userId});
}

// Add Task Management Functions
function initializeAddTaskButton() {
    const addTaskBtn = document.getElementById('add-task-btn');
    if (addTaskBtn) {
        addTaskBtn.addEventListener('click', function() {
            showTaskSelector();
        });
    }
}

function showTaskSelector() {
    // Get available tasks (this should come from server)
    const availableTasks = getAvailableTasks();
    
    if (availableTasks.length === 0) {
        alert('هیچ تسک جدیدی برای اضافه کردن وجود ندارد');
        return;
    }
    
    // Create modal or dropdown for task selection
    const modal = document.createElement('div');
    modal.className = 'task-selector-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h5>انتخاب تسک جدید</h5>
                <button type="button" class="close-btn">&times;</button>
            </div>
            <div class="modal-body">
                <select class="form-select" id="new-task-select">
                    <option value="">انتخاب تسک...</option>
                    ${availableTasks.map(task => 
                        `<option value="${task.id}">${task.title}</option>`
                    ).join('')}
                </select>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="confirm-add-task">اضافه کردن</button>
                <button type="button" class="btn btn-secondary" id="cancel-add-task">انصراف</button>
            </div>
        </div>
    `;
    
    // Add modal styles
    const style = document.createElement('style');
    style.textContent = `
        .task-selector-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .modal-content {
            background: white;
            padding: 20px;
            border-radius: 8px;
            min-width: 300px;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .close-btn {
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
        }
        .modal-footer {
            margin-top: 15px;
            text-align: left;
        }
        .modal-footer button {
            margin-left: 10px;
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(modal);
    
    // Add event listeners
    modal.querySelector('.close-btn').addEventListener('click', function() {
        document.body.removeChild(modal);
        document.head.removeChild(style);
    });
    
    modal.querySelector('#cancel-add-task').addEventListener('click', function() {
        document.body.removeChild(modal);
        document.head.removeChild(style);
    });
    
    modal.querySelector('#confirm-add-task').addEventListener('click', function() {
        const selectedTaskId = modal.querySelector('#new-task-select').value;
        if (selectedTaskId) {
            const selectedTask = availableTasks.find(t => t.id == selectedTaskId);
            addNewTask(selectedTask);
            document.body.removeChild(modal);
            document.head.removeChild(style);
        }
    });
}

function getAvailableTasks() {
    // This should be populated from server data
    // For now, return a sample list
    return [
        { id: 5, title: 'تست نهایی سیستم' },
        { id: 6, title: 'مستندسازی تغییرات' },
        { id: 7, title: 'آموزش کاربران' },
        { id: 8, title: 'پشتیبان‌گیری از داده‌ها' }
    ].filter(task => {
        // Filter out tasks that are already in the table
        const existingTaskIds = Array.from(document.querySelectorAll('tbody tr')).map(row => 
            row.getAttribute('data-task-id')
        );
        return !existingTaskIds.includes(task.id.toString());
    });
}

function addNewTask(task) {
    const tbody = document.querySelector('tbody');
    const newRow = document.createElement('tr');
    newRow.setAttribute('data-task-id', task.id);
    newRow.setAttribute('data-new-task', 'true');
    newRow.innerHTML = `
        <td>${task.title}</td>
        <td>
            <div class="users-container" data-task-id="${task.id}" data-role="E">
                <span class="text-muted">هیچ مجری تعریف نشده</span>
                <div class="add-user-btn" data-task-id="${task.id}" data-role="E" title="اضافه کردن مجری">
                    <i class="fas fa-plus"></i>
                </div>
                <div class="user-selector" style="display: none;">
                    <select class="form-select user-combo" data-task-id="${task.id}" data-role="E">
                        <option value="">انتخاب کاربر...</option>
                        ${getUsersForCombo()}
                    </select>
                </div>
            </div>
        </td>
        <td>
            <div class="users-container" data-task-id="${task.id}" data-role="T">
                <span class="text-muted">هیچ تستری تعریف نشده</span>
                <div class="add-user-btn" data-task-id="${task.id}" data-role="T" title="اضافه کردن تستر">
                    <i class="fas fa-plus"></i>
                </div>
                <div class="user-selector" style="display: none;">
                    <select class="form-select user-combo" data-task-id="${task.id}" data-role="T">
                        <option value="">انتخاب کاربر...</option>
                        ${getUsersForCombo()}
                    </select>
                </div>
            </div>
        </td>
        <td>
            <div class="task-actions">
                <button type="button" class="btn btn-sm btn-outline-danger deactivate-task-btn" data-task-id="${task.id}">
                    <i class="fas fa-eye-slash"></i>
                </button>
            </div>
        </td>
    `;
    
    tbody.appendChild(newRow);
    
    // Re-initialize event listeners for new elements
    initializeUserBadges();
    initializeAddUserButtons();
    initializeTaskActions();
    
    // Update task data
    updateTaskData();
    
    console.log('New task added:', task);
}

function getUsersForCombo() {
    // This should get users from the template context
    // For now, return empty string
    return '';
}

// مدیریت اکشن‌های تسک (نسخه jQuery با delegation)
// function initializeTaskActions() { ... } — غیرفعال شد

function toggleTaskStatus(taskId, row) {
    const isCurrentlyInactive = row.classList.contains('inactive');
    
    if (isCurrentlyInactive) {
        // Reactivate task
        row.classList.remove('inactive');
        const btn = row.querySelector('.deactivate-task-btn');
        btn.innerHTML = '<i class="fas fa-eye-slash"></i>';
        btn.className = 'btn btn-sm btn-outline-danger deactivate-task-btn';
        updateTaskStatusInData(taskId, true);
    } else {
        // Deactivate task
        row.classList.add('inactive');
        const btn = row.querySelector('.deactivate-task-btn');
        btn.innerHTML = '<i class="fas fa-eye"></i>';
        btn.className = 'btn btn-sm btn-outline-success deactivate-task-btn';
        updateTaskStatusInData(taskId, false);
    }
    
    // Update task data
    updateTaskData();
}

function updateTaskStatusInData(taskId, isActive) {
    const taskDataInput = document.getElementById('task-data');
    if (!taskDataInput) return;
    
    let taskData = JSON.parse(taskDataInput.value || '{"tasks":[],"users":{"added":[],"removed":[]}}');
    
    // Find or create task
    let task = taskData.tasks.find(t => t.id == taskId);
    if (!task) {
        task = {
            id: taskId,
            name: '',
            isActive: isActive,
            executors: [],
            testers: []
        };
        taskData.tasks.push(task);
    } else {
        task.isActive = isActive;
    }
    
    // Update input
    taskDataInput.value = JSON.stringify(taskData);
    console.log('Task status updated:', {taskId, isActive});
}

// Helper function to get summary of all changes
function getChangesSummary() {
    const taskDataInput = document.getElementById('task-data');
    if (!taskDataInput) return null;
    
    const taskData = JSON.parse(taskDataInput.value || '{"tasks":[],"changes":{"tasksAdded":[],"tasksRemoved":[],"usersAdded":[],"usersRemoved":[],"tasksDeactivated":[],"tasksReactivated":[]}}');
    
    const summary = {
        totalTasks: taskData.tasks.length,
        newTasks: taskData.changes.tasksAdded.length,
        deactivatedTasks: taskData.changes.tasksDeactivated.length,
        totalUsers: 0,
        newUsers: 0,
        removedUsers: taskData.changes.usersRemoved.length
    };
    
    // Count users
    taskData.tasks.forEach(task => {
        summary.totalUsers += task.executors.length + task.testers.length;
        task.executors.forEach(user => {
            if (user.action === 'added') summary.newUsers++;
        });
        task.testers.forEach(user => {
            if (user.action === 'added') summary.newUsers++;
        });
    });
    
    return summary;
}

// Function to validate before form submission
function validateTaskData() {
    const summary = getChangesSummary();
    if (!summary) return true;
    
    console.log('Changes Summary:', summary);
    
    // You can add validation rules here
    // For example: if (summary.newTasks > 5) { alert('تعداد تسک‌های جدید زیاد است'); return false; }
    
    return true;
}

// Function to validate notification data
function validateNotificationData() {
    const changes = getNotificationChanges();
    
    // Check if at least one notification method is enabled for each group
    const groups = {};
    changes.forEach(change => {
        if (!groups[change.notifyGroupId]) {
            groups[change.notifyGroupId] = [];
        }
        groups[change.notifyGroupId].push(change);
    });
    
    for (const groupId in groups) {
        const groupChanges = groups[groupId];
        const hasActiveNotification = groupChanges.some(change => change.isActive);
        
        if (!hasActiveNotification) {
            alert('حداقل یک روش اطلاع‌رسانی باید برای هر گروه فعال باشد');
            return false;
        }
    }
    
    return true;
}

// Function to validate all form data
function validateAllFormData() {
    const taskValidation = validateTaskData();
    const notificationValidation = validateNotificationData();
    
    return taskValidation && notificationValidation;
}

// مدیریت آیکون‌های اعلان (نسخه jQuery با delegation)
// function initializeNotificationIcons() { ... } — غیرفعال شد


function updateNotificationData(notifyGroupId, notificationType, isActive) {
    // Update notification data in form
    updateNotificationDataInForm();
    
    console.log('Updating notification data:', {
        notifyGroupId: notifyGroupId,
        type: notificationType,
        isActive: isActive
    });
}

// Function to get all notification changes
function getNotificationChanges() {
    const changes = [];
    
    document.querySelectorAll('.notification-icon').forEach(function(icon) {
        const notifyGroupId = icon.getAttribute('data-notify-group-id');
        const notificationType = icon.getAttribute('data-notification-type');
        const currentSrc = icon.getAttribute('src');
        const isActive = !currentSrc.includes('-gray');
        
        changes.push({
            notifyGroupId: notifyGroupId,
            type: notificationType,
            isActive: isActive
        });
    });
    
    return changes;
}

// Function to update notification data in hidden input
function updateNotificationDataInForm() {
    const changes = getNotificationChanges();
    const notificationDataInput = document.getElementById('notification-data');
    
    if (notificationDataInput) {
        notificationDataInput.value = JSON.stringify(changes);
    }
    
    console.log('Notification data updated:', changes);
}

// Function to get complete form summary
function getCompleteFormSummary() {
    const taskSummary = getChangesSummary();
    const notificationChanges = getNotificationChanges();
    
    return {
        tasks: taskSummary,
        notifications: {
            totalGroups: new Set(notificationChanges.map(c => c.notifyGroupId)).size,
            totalChanges: notificationChanges.length,
            activeNotifications: notificationChanges.filter(c => c.isActive).length
        }
    };
}

// Final summary function
function getFinalFormSummary() {
    const taskData = JSON.parse(document.getElementById('task-data').value || '{}');
    const notificationData = JSON.parse(document.getElementById('notification-data').value || '[]');
    
    return {
        tasks: {
            total: taskData.tasks ? taskData.tasks.length : 0,
            new: taskData.changes ? taskData.changes.tasksAdded.length : 0,
            deactivated: taskData.changes ? taskData.changes.tasksDeactivated.length : 0
        },
        notifications: {
            totalGroups: new Set(notificationData.map(n => n.notifyGroupId)).size,
            totalMethods: notificationData.length,
            activeMethods: notificationData.filter(n => n.isActive).length
        },
        users: {
            total: taskData.tasks ? taskData.tasks.reduce((sum, task) => sum + task.executors.length + task.testers.length, 0) : 0,
            new: taskData.tasks ? taskData.tasks.reduce((sum, task) => 
                sum + task.executors.filter(u => u.action === 'added').length + 
                task.testers.filter(u => u.action === 'added').length, 0) : 0
        }
    };
}

// نمایش خلاصه نهایی در کنسول
function displayFinalSummary() {
    const summary = getFinalFormSummary();
    console.log('=== FINAL FORM SUMMARY ===');
    console.log('Tasks:', summary.tasks);
    console.log('Notifications:', summary.notifications);
    console.log('Users:', summary.users);
    console.log('========================');
    return summary;
}

// Complete form validation
function validateCompleteForm() {
    const errors = [];
    
    // Validate tasks
    if (!validateTaskData()) {
        errors.push('خطا در اعتبارسنجی تسک‌ها');
    }
    
    // Validate notifications
    if (!validateNotificationData()) {
        errors.push('خطا در اعتبارسنجی اطلاع‌رسانی‌ها');
    }
    
    // Validate required fields
    const requiredFields = document.querySelectorAll('.required');
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            errors.push(`فیلد ${field.getAttribute('data-field-name') || field.name} الزامی است`);
        }
    });
    
    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

// Auto-save function
function autoSaveFormData() {
    updateTaskData();
    updateNotificationDataInForm();
    console.log('Form data auto-saved');
}

// Debug function to show all form data
function showFormDataDebug() {
    const summary = getCompleteFormSummary();
    console.log('=== FORM DATA DEBUG ===');
    console.log('Task Data:', document.getElementById('task-data').value);
    console.log('Notification Data:', document.getElementById('notification-data').value);
    console.log('Summary:', summary);
    console.log('=======================');
    
    return summary;
}

// مقداردهی اولیه قدیمی مبتنی بر DOMContentLoaded غیرفعال شد تا دوباره‌سازی رخ ندهد
// document.addEventListener('DOMContentLoaded', function() { ... });

function toBoolean(value) {
    return value === true || value === 'True' || value === 1;
}
function toString(value) {
    return (value === null || value === undefined || value === 'None') ? '' : value;
}
// تابع برای تبدیل رشته به آرایه
function parseList(listString) {
    if (listString != undefined &&  listString.length>0) {
        listString = listString.replace(/'/g, '"'); // حذف / های اضافی
        return JSON.parse(listString); // تبدیل به آرایه
    }
    return [];
}
function toJalaali(year, month, day) {
    // محاسبه تعداد روزهای سال‌های میلادی تا سال مورد نظر
    var g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if (year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0)) {
        g_days_in_month[1] = 29; // سال کبیسه
    }

    var g_day_no = day;
    for (var i = 0; i < month - 1; i++) {
        g_day_no += g_days_in_month[i];
    }
    g_day_no += (year - 1) * 365 + Math.floor((year - 1) / 4) - Math.floor((year - 1) / 100) + Math.floor((year - 1) / 400);

    // محاسبه سال جلالی
    var j_year = 1348 + Math.floor((g_day_no - 226899) / 1029983);
    var j_day_no = g_day_no - (j_year - 1348) * 1029983 + 226899;
    var j_month = 0;

    // محاسبه ماه و روز جلالی
    var j_days_in_month = [31, 31, 31, 31, 30, 30, 30, 30, 30, 30, 30, 29];
    if (j_year % 4 === 3) {
        j_days_in_month[11] = 30; // سال کبیسه جلالی
    }

    for (var j = 0; j < 12; j++) {
        if (j_day_no <= j_days_in_month[j]) {
            j_month = j + 1;
            break;
        }
        j_day_no -= j_days_in_month[j];
    }

    // اصلاح تاریخ جلالی
    j_year = j_year + 621; // تبدیل سال میلادی به جلالی
    return [j_year, j_month, j_day_no]; // بازگشت تاریخ جلالی
}
function IsValidPersianDate(dateString) {
    // الگوی عبارات منظم برای بررسی فرمت YYYY/MM/DD
    var regex = /^(140[0-3]|139[0-9])\/(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])$/;

    // بررسی فرمت تاریخ
    if (!regex.test(dateString)) {
        return false; // فرمت نامعتبر
    }

    // جدا کردن سال، ماه و روز
    var parts = dateString.split('/');
    var year = parseInt(parts[0], 10);
    var month = parseInt(parts[1], 10);
    var day = parseInt(parts[2], 10);

    // بررسی تعداد روزهای ماه
    var daysInMonth = [31, 31, 31, 31, 30, 30, 30, 30, 30, 30, 30, 29]; // سال جلالی
    if (month === 12) {
        // اگر سال کبیسه باشد، اسفند 30 روز دارد
        if (year % 4 === 3) {
            daysInMonth[11] = 30; // سال کبیسه
        } else {
            daysInMonth[11] = 29; // سال غیر کبیسه
        }
    }

    // بررسی روز
    return day <= daysInMonth[month - 1] && day > 0; // بررسی روز
}
function IsValidTime(timeString) {
    // الگوی عبارات منظم برای بررسی فرمت HH:MM
    var regex = /^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$/;

    // بررسی فرمت زمان
    return regex.test(timeString); // بازگشت true یا false
}
function compare_persian_date(date1, date2) {
    // date1 و date2 باید به صورت آرایه [year, month, day] باشند
    var year1 = date1[0], month1 = date1[1], day1 = date1[2];
    var year2 = date2[0], month2 = date2[1], day2 = date2[2];

    // مقایسه سال‌ها
    if (year1 < year2) {
        return -1; // date1 قبل از date2
    } else if (year1 > year2) {
        return 1; // date1 بعد از date2
    }

    // اگر سال‌ها برابر بودند، ماه‌ها را مقایسه می‌کنیم
    if (month1 < month2) {
        return -1; // date1 قبل از date2
    } else if (month1 > month2) {
        return 1; // date1 بعد از date2
    }

    // اگر سال‌ها و ماه‌ها برابر بودند، روزها را مقایسه می‌کنیم
    if (day1 < day2) {
        return -1; // date1 قبل از date2
    } else if (day1 > day2) {
        return 1; // date1 بعد از date2
    }

    return 0; // date1 و date2 برابر هستند
}
function ActiveInActiveImages(imgs, active_inactive) {
    if (active_inactive=='inactive')
    {
        imgs.each(
            //چون مسیر تصویر هر آیکون متفاوت است نمی توانیم از یک دستور واحد استفاده کنیم
            //و باید حلقه استفاده شود
            function() {
                //تصویر عنصر فعال فعلی را غیرفعال می کنیم
                inactive_src = $(this).attr('src').split('.')[0] + '_Gray.png';
                $(this).attr('src', inactive_src)
            })    
    }
    else
    {
        imgs.each(
            //چون مسیر تصویر هر آیکون متفاوت است نمی توانیم از یک دستور واحد استفاده کنیم
            //
            function() {
                active_src = $(this).attr('src').replace('_Gray','')
                $(this).attr('src', active_src)
            })                
    }
}
function check_location(eleman_name) {
    var selector = $('input[name="'+ eleman_name +'"]')
    // بررسی اینکه آیا چک باکس مربوطه تیک خورده است
    if (selector.is(':checked')) {
        //بررسی اینکه آیا زیر مجموعه ای دارد؟
        if (selector.parent().parent().find('.check-list-box').length > 0) {
            //اگر از گزینه های زیرمجموعه هیچ موردی انتخاب نشده باشد
            if (selector.parent().parent().find('.check-list-box.active').length===0)
                return "با توجه به انتخاب گزینه " + selector.parent().find('label').text() + " لطفا یکی از گزینه های زیرمجموعه آن را انتخاب کنید.";
        }
    }
    return null; // اگر خطایی وجود نداشته باشد
}
function form_validation() {
    var errors = [];

    $('.required').removeClass('error'); // حذف کلاس error
    $('.required').each(function() {
        // حذف علامت ستاره قرمز از فیلدها
        $(this).prev('.red-star').remove(); // حذف ستاره قرمز
    });
    
    // بررسی فیلدهای اجباری
    $('.required').each(function() {
        if (!$(this).val()) {
            // اضافه کردن کلاس خطا
            $(this).addClass('error'); // اضافه کردن کلاس error
            errors.push($(this).data('field-name') + " الزامی است.");
            // اضافه کردن علامت ستاره قرمز
            $(this).before('<span class="red-star">*</span>'); // اضافه کردن ستاره قرمز
        }
    });
    /*-------------------------------------صفحه اول----------------------------------------------/
    /***************************************سطر اول********************************************* */
    //////////////////////////////////بخش اول//////////////////////////
    // افراد درگیر

    //////////////////////////////////بخش دوم//////////////////////////
    // ویژگی های تغییر


    /***************************************سطر دوم********************************************* */
    //////////////////////////////////بخش اول//////////////////////////
    //اطلاعات تغییر
    if (!$('select[name="change_type"]').val()) {
        errors.push("لطفا نوع تغییر را مشخص کنید.");
    }

    if (!$('input[name="change_location_data_center"]').is(':checked') && 
        !$('input[name="change_location_database"]').is(':checked') && 
        !$('input[name="change_location_systems"]').is(':checked') &&
        !$('input[name="change_location_other"]').is(':checked')) {
        errors.push("لطفا یکی از گزینه های محل تغییر را انتخاب کنید");
    }

    // بررسی محل تغییر: مرکز داده
    var dataCenterError = check_location('change_location_data_center');
    if (dataCenterError) {
        errors.push(dataCenterError);
    }

    // بررسی محل تغییر: پایگاه داده
    var databaseError = check_location('change_location_database');
    if (databaseError) {
        errors.push(databaseError);
    }

    // بررسی محل تغییر: سیستم‌ها
    var systemsError = check_location('change_location_systems');
    if (systemsError) {
        errors.push(systemsError);
    }

    //////////////////////////////////بخش دوم//////////////////////////
    //حوزه و ارتباطات تغییر
    //اگر گزینه نیاز به کمیته دارد انتخاب شده باشد باید کمیته هم انتخاب شده باشد
    if ($('input[name="need_committee"]:checked').val() === 1
        && $('select[name="committee"]').val() < 0)
        errors.push("با توجه به اینکه گزینه نیاز به کمیته دارد انتخاب شده است، باید کمیته مربوطه را انتخاب نمایید")

    //دامنه تغییر
    //باید یکی از گزینه های دامنه تغییر انتخاب شده باشد
    if (!$('.change-team-corp input[name="domain"]:checked'))
        errors.push("لطفا یکی از گزینه های 'درون سازمانی' یا 'بین سازمانی' یا 'برون سازمانی' را برای دامنه تغییرات انتخاب کنید")
    //در غیر این صورت باید کنترل کنیم با توجه به حوزه مربوطه، تیم یا شرکت را انتخاب کرده باشد
    else
    {
        //اگر گزینه درون سازمانی یا بین سازمانی انتخاب شده باشد
        if ($('.change-team-corp .radio-box.Domain_Inside').hasClass('active') ||
            $('.change-team-corp .radio-box.Domain_Between').hasClass('active'))
        {
            //باید حداقل یک تیم انتخاب شده باشد
            if ($('.change-team-corp .team-icons img.active').length === 0)
                errors.push("در قسمت دامنه تغییر، حداقل یک تیم را انتخاب کنید")
        }
        if ($('.change-team-corp .radio-box.Domain_Outside').hasClass('active') ||
            $('.change-team-corp .radio-box.Domain_Between').hasClass('active'))
        {
            //باید حداقل یک تیم انتخاب شده باشد
            if ($('.change-team-corp .corp-icons img.active').length === 0)
                errors.push("در قسمت دامنه تغییر، حداقل یک شرکت را انتخاب کنید")
        }
    }

    /*-------------------------------------صفحه دوم----------------------------------------------/
    /***************************************سطر اول********************************************* */
    //////////////////////////////////بخش اول//////////////////////////
    // زمانبندی تغییرات
    if ($('input[name="request_date"]').val() === '') {
        errors.push("لطفا زمان انجام تغییرات را مشخص کنید")
    }
    //اگر زمان معلوم شده باشد، باید مربوط به آینده باشد
    else
    {
        var persianDate = $('input[name="request_date"]').val();
        var requestTime = $('input[name="request_time"]').val();
        var today = new Date();
        var persianToday = toJalaali(today.getFullYear(), today.getMonth() + 1, today.getDate());
        // if (!IsValidPersianDate(persianDate)) {
        //     errors.push("تاریخ شمسی وارد شده معتبر نیست.");
        
        // } else if (compare_persian_date(persianDate, persianToday) <= 0) {
        //     errors.push("زمان درخواست تغییرات نمی تواند مربوط به گذشته باشد.");
        // }
        if (!IsValidTime(requestTime)) {
            errors.push("زمان درخواست باید در فرمت HH:MM باشد.");
        }
    }

    if ($('input[name="duration_hour"]').val() == 0
        && $('input[name="duration_minute"]').val() == 0) {
        errors.push("مدت زمان لازم برای انجام کار نمی‌تواند صفر باشد.");
    }
    var downtime = parseInt($('input[name="estimate_downtime_hour"]').val()) * 60 + parseInt($('input[name="estimate_downtime_minute"]').val())
    var worstcase = parseInt($('input[name="worstcase_downtime_hour"]').val()) * 60 + parseInt($('input[name="worstcase_downtime_minute"]').val())
    //بدترین زمان تخمین نمی تواند از زمان تخمینی اصلی کمتر باشد
    if (downtime > worstcase) {
        errors.push("بدترین تخمین قطعی سیستم باید بزرگتر یا مساوی میزان تخمین قطعی سیستم باشد.");
    }


    //////////////////////////////////بخش دوم//////////////////////////
    // حوزه اثرگذاری
    if ($('input[name="ImpactOnCriticalService"]').is(':checked') && !$('[name="ImpactOnCriticalServiceDescription"]').val()) {
        errors.push("با توجه به اینکه گزینه قطعی سرویس‌های حیاتی را انتخاب کرده اید، باید توضیحات مربوطه را وارد کنید.");
    }
    if ($('input[name="ImpactOnSensitiveService"]').is(':checked') && !$('[name="ImpactOnSensitiveServiceDescription"]').val()) {
        errors.push("با توجه به اینکه گزینه قطعی سرویس‌های حساس را انتخاب کرده اید، باید توضیحات مربوطه را وارد کنید.");
    }
    if (!$('input[name="ImpactOnSensitiveService"]').is(':checked') && !$('input[name="ImpactOnCriticalService"]').is(':checked') && !$('input[name="ImpactNotOnAnyService"]').is(':checked')) {
        errors.push("حداقل یکی از گزینه‌های منجر به قطعی سرویس‌های حساس، حیاتی یا عدم قطعی سرویس‌ها باید انتخاب شود.");
    }
    
    if (($('input[name="ImpactOnSensitiveService"]').is(':checked') || $('input[name="ImpactOnCriticalService"]').is(':checked')) && $('input[name="ImpactNotOnAnyService"]').is(':checked')) {
        errors.push("اگر گزینه عدم قطعی سرویس‌ها انتخاب شده باشد، نمی‌توانید گزینه‌های منجر به قطعی سرویس‌های حساس یا حیاتی را انتخاب کنید.");
    }


    /***************************************سطر دوم********************************************* */
    //////////////////////////////////بخش اول//////////////////////////
    // الزام به تغییر
    if ($('.reason-table input[type="checkbox"]:checked').length === 0) {
        errors.push("حداقل یکی از گزینه‌های الزام به تغییر باید انتخاب شود.");
    }

    //اگز گزینه سایر انتخاب شده باشد باید توضیحات بیان شود
    if ($('.reason-table input[name="ReasonOther"]').is(':checked')
        && $('.reason-table input[name="ReasonOtherDescription"]').val() === "")
    {
        errors.push("با توجه به اینکه برای دلایل الزام به تغییر گزینه 'سایر'' انتخاب شده است، باید در قسمت مربوطه توضیحات لازم را درج نمایید.");
    }

    //////////////////////////////////بخش دوم//////////////////////////
    // بازگشت تغییرات
    //باید حداقل یک گزینه را انتخاب کرده باشد
    if ($('input[name="Rollback"]:checked').length === 0) {
        errors.push("لطفا مشخص کنید که طرحی برای بازگشت تغییرات وجود دارد یا خیر")
    }
    else
    {
        //اگر طرح تغییری وجود دارد باید بیان شود
        if ($('input[name="Rollback"]:checked').val() == 1 
            && $('textarea[name="RollbackPlan"]').val() === '')
            errors.push("لطفاً طرح بازگشت را تکمیل کنید.");
    }


    return errors;
}


function ChangeLocation(list, list_class)
{
    if (list.length > 0)
        {

            // پیدا کردن div با کلاس data-center-list
            $('.'+list_class+' .check-list-box').each(function() {
                var box = $(this);
                var code =box.find('input[type="checkbox"').val()
                var img = box.find('img')
                // برای هر کد در changeLocation_datacenter_list
                list.forEach(function(item) {
                    // اگر قبلا انتخاب نشده باشد باید انتخاب شود
                    if (code == item && img.parents('.check-list-box').hasClass('inactive'))                
                        img.trigger('click');
                });
            });             

        }        
}
function SetTeamCorp(list, TeamCorp)
{
    if (list.length > 0)
    {
        
        //اگر مربوط به تیم ها باشد
        var div = $(".team-icons")
        // اگر مربوط به شرکت ها باشد
        if (TeamCorp === 'C')
            div = $(".corp-icons")

        div.find('.icon-list img').each(function() {
            var code = $(this).data("code")
            var img = $(this)

            list.forEach(function(item) {
                // اگر قبلا انتخاب نشده باشد باید انتخاب شود
                if (code == item && img.hasClass('inactive'))
                {
                    img.trigger("click")
                }
            });
        });
        //حالا می خواهیم گزینه طبقه بندی تغییر را تنظیم کنیم
        //ابتدا مقدار فعلی را به دست می آوریم
        domain = $("input[name='domain']:checked").val()
        //اگر این گزینه مربوط به تیم باشد و قبلا شرکتی انتخاب شده باشد
        //یا اینکه این گزینه شرکت باشد و قبلا تیمی انتخاب شده باشد
        //باید گزینه بین سازمانی انتخاب شود
        if ((TeamCorp === 'T' && (domain === 'Domain_Between' || domain === 'Domain_Outside')) ||
            (TeamCorp === 'C' && (domain === 'Domain_Between' || domain === 'Domain_Inside')))
            {
                $('.change-team-corp .radio-list img.Domain_Between').click()
            }
        //در غیر این صورت
        else
        {
            if (TeamCorp === 'T')
            {
                //اگر فقط تیم انتخاب شود، گزینه درون سازمانی را باید انتخاب کنیم
                $('.change-team-corp .radio-list img.Domain_Inside').click()
            }
            else 
            {
                //اگر فقط شرکت انتخاب شود، گزینه برون سازمانی را باید انتخاب کنیم
                $('.change-team-corp .radio-list img.Domain_Outside').click()
            }
        }
    }
}
function form_validation_committee()
{

}
function form_validation_executor() {
    var errors = [];

    // دریافت مقادیر از المان‌ها
    var operationResult = $('input[name="operation_result"]:checked').val();
    var operationDate = $('#operation_date').val();
    var operationTime = $('#operation_time').val();
    var operationReport = $('#operation_report').val();
    var changingDurationHour = $('input[name="changing_duration_actual_hour"]').val();
    var changingDurationMinute = $('input[name="changing_duration_actual_minute"]').val();
    var downtimeDurationHour = $('input[name="downtime_duration_actual_hour"]').val();
    var downtimeDurationMinute = $('input[name="downtime_duration_actual_minute"]').val();

    // بررسی المان‌های اجباری
    if (!operationResult) {
        errors.push("لطفاً نتیجه انجام تغییرات را انتخاب کنید.");
    }
    if (!operationDate) {
        errors.push("لطفاً تاریخ انجام تغییرات را وارد کنید.");
    } 
    // else if (!IsValidPersianDate(operationDate)) {
    //     errors.push("تاریخ وارد شده باید در فرمت YYYY/MM/DD باشد.");
    // }
    if (!operationTime) {
        errors.push("لطفاً زمان انجام تغییرات را وارد کنید.");
    } else if (!IsValidTime(operationTime)) {
        errors.push("زمان وارد شده باید در فرمت HH:MM باشد.");
    }
    if (!operationReport) {
        errors.push("لطفاً گزارش انجام تغییرات را وارد کنید.");
    }

    // بررسی المان‌های عددی
    if (!changingDurationHour || isNaN(changingDurationHour) || changingDurationHour < 0) {
        errors.push("لطفاً مدت زمان انجام تغییرات (ساعت) را وارد کنید.");
    }
    if (!changingDurationMinute || isNaN(changingDurationMinute) || changingDurationMinute < 0 || changingDurationMinute > 59) {
        errors.push("لطفاً مدت زمان انجام تغییرات (دقیقه) را وارد کنید.");
    }
    if (!downtimeDurationHour || isNaN(downtimeDurationHour) || downtimeDurationHour < 0) {
        errors.push("لطفاً مدت زمان قطعی سیستم (ساعت) را وارد کنید.");
    }
    if (!downtimeDurationMinute || isNaN(downtimeDurationMinute) || downtimeDurationMinute < 0 || downtimeDurationMinute > 59) {
        errors.push("لطفاً مدت زمان قطعی سیستم (دقیقه) را وارد کنید.");
    }

    return errors; // بازگشت آرایه خطاها
}
function form_validation_tester()
{
    var errors = [];

    // دریافت مقادیر از المان‌ها
    var operationResult = $('input[name="operation_result"]:checked').val();
    var operationDate = $('#operation_date').val();
    var operationTime = $('#operation_time').val();
    var operationReport = $('#operation_report').val();

    // بررسی المان‌های اجباری
    if (!operationResult) {
        errors.push("لطفاً نتیجه تست را انتخاب کنید.");
    }
    if (!operationDate) {
        errors.push("لطفاً تاریخ انجام تست را وارد کنید.");
    } 
    // else if (!IsValidPersianDate(operationDate)) {
    //     errors.push("تاریخ وارد شده باید در فرمت YYYY/MM/DD باشد.");
    // }
    if (!operationTime) {
        errors.push("لطفاً زمان انجام تست را وارد کنید.");
    } else if (!IsValidTime(operationTime)) {
        errors.push("زمان وارد شده باید در فرمت HH:MM باشد.");
    }
    if (!operationReport) {
        errors.push("لطفاً گزارش تست را وارد کنید.");
    }

    return errors; // بازگشت آرایه خطاها


}
function confirm(request_status) {
    return new Promise(function(on_success,  on_failure) 
    {
    var error_message = []
    //اگر مدیر باشد نیازی به ورود اطلاعات ندارد
    //اگر کاربر کمیته باشد باید فیلدهای کاربر کمیته بررسی شوند
    // if (request_status == 'COMITE')
    // {
    //     error_message = form_validation_committee()
    // }
    //اگر کاربر مجری باشد، باید فیلدهای کاربر مجری بررسی شوند
    if (request_status == 'EXECUT')
    {
        error_message = form_validation_executor()
    }
    //اگر کاربر تستر باشد، باید فیلدهای کاربر تستر بررسی شوند
    else if (request_status == 'TESTER')
    {
        error_message = form_validation_tester()
    }
    

    // اگر خطا وجود دارد، نمایش پیام خطا
    if (error_message.length > 0) {
        $.alert({
            title: 'خطا',
            content: error_message.join('<br>'),
        });
        $('html, body').animate({
            scrollTop: $(document).height()
        }, 1000);
        on_failure()
        return; // جلوگیری از ادامه
    }
    
    //شناسه درخواست را به دست می آوریم
    var requestId = $('input[name="request_id"]').val();
    
    //به سراغ مرحله بعدی می رویم
    var url = '/ConfigurationChangeRequest/request/next_step/' + requestId + '/CON/';

    // جمع‌آوری داده‌های فرم
    var formData = $('form').serialize();

    // ارسال درخواست AJAX
    $.ajax({
        url: url,
        method: 'POST',
        data: formData,
        success: function(response) 
        {
            if (response.success) 
            {
                if (response.message)
                    msg = response.message
                else
                    msg = 'اطلاعات با موفقیت ذخیره شده و فرم به مرحله بعدی ارسال شد'
                
                $.alert({
                    title: 'ارسال موفقیت آمیز',
                    content: msg,
                    buttons: {
                        confirm: {
                            text: 'بستن',
                            btnClass: 'btn-blue',
                            action: function() {
                                window.location.href = '/ConfigurationChangeRequest/request/view/'+response.request_id+'/';
                            }
                        }
                    }});                                
            } 
            else 
            {
                // در صورت بروز خطا، پیام‌های خطا را نمایش دهید
                var errorMessage = response.message;
                $.alert({
                    title: 'خطا',
                    content: errorMessage,
                });
                on_failure()
            }
        },
        error: function(xhr) 
        {
            // در صورت بروز خطا، پیام خطا را نمایش می‌دهیم
            // ایجاد یک عنصر موقتی
            var tempDiv = $('<div>').html(xhr.responseText);

            // استخراج متن از div با شناسه summary
            var errorMessage = tempDiv.find('#summary').text().trim(); // استفاده از #summary
            $.alert({
                title: 'خطا',
                content: errorMessage,
            });
            on_failure()
        }
        });
    
    //در صورت موفقیت آمیز بودن
    on_success
})}

/**
* @param {number} duration - مقدار زمان به دقیقه (باید عدد صحیح مثبت باشد)
* @param {jQuery} row - سلکتور jQuery که شامل input های مربوطه است
*/ 
function SetDuration(duration, row)
{
    // تبدیل به عدد صحیح
    duration = parseInt(duration);
    
    // محاسبه ساعت با تقسیم بر 60 و گرفتن قسمت صحیح
    var hours = Math.floor(duration / 60);
    
    // محاسبه دقیقه با گرفتن باقیمانده تقسیم بر 60 
    var minutes = duration % 60;
    
    // مقداردهی به input های مربوطه در row
    row.find('.hours').val(hours);
    row.find('.minutes').val(minutes);
}

function LoadData(selector) {
    var data = {};

    // 1- اطلاعات افراد درگیر
    data.executorNationalCode = toString($(selector).data('executor-nationalcode')); // کد ملی کاربر مجری
    data.testerNationalCode = toString($(selector).data('tester-nationalcode')); // کد ملی کاربر تست کننده
    data.testRequired = toBoolean($(selector).data('test-required')); // نیاز به تست

    // 2- ویژگی های تغییر
    data.changeLevel = toString($(selector).data('change-level')); // گستردگی تغییر
    data.classification = toString($(selector).data('classification')); // طبقه‌بندی
    data.priority = toString($(selector).data('priority')); // اولویت
    data.riskLevel = toString($(selector).data('risk-level')); // سطح ریسک

    // 3- اطلاعات تغییر
    data.changeTitle = toString($(selector).data('change-title')); // عنوان تغییر
    data.changeDescription = toString($(selector).data('change-description')); // توضیحات تغییر
    data.changeLocationDataCenter = toBoolean($(selector).data('change-location-data-center')); // محل تغییر: مرکز داده
    data.changeLocationDataCenterList = parseList($(selector).data('change-location-data-center-list')); // لیست محل تغییر: مرکز داده
    data.changeLocationDatabase = toBoolean($(selector).data('change-location-database')); // محل تغییر: پایگاه داده
    data.changeLocationDatabaseList = parseList($(selector).data('change-location-database-list')); // لیست محل تغییر: پایگاه داده
    data.changeLocationSystems = toBoolean($(selector).data('change-location-systems')); // محل تغییر: سیستم‌ها
    data.changeLocationSystemsList = parseList($(selector).data('change-location-systems-list')); // لیست محل تغییر: سیستم‌ها
    data.changeLocationOther = toBoolean($(selector).data('change-location-other')); // محل تغییر: سایر
    data.changeLocationOtherDescription = toString($(selector).data('change-location-other-description')); // توضیحات محل تغییر

    // 4- حوزه و ارتباطات تغییر
    data.needCommittee = toBoolean($(selector).data('need-committee')); // نیاز به کمیته
    data.committeeId = toString($(selector).data('committee-id')); // شناسه کمیته
    data.team_list = parseList($(selector).data('teams')) //لیست تیم های انتخاب شده
    data.corp_list  = parseList($(selector).data('corps')) //لیست شرکت های انتخاب شده

    // 5- زمانبندی تغییر
    data.changingDuration = parseInt($(selector).data('changing-duration')) || 0; // مدت زمان تغییرات
    data.downtimeDuration = parseInt($(selector).data('downtime-duration')) || 0; // مدت زمان توقف
    data.downtimeDurationWorstCase = parseInt($(selector).data('downtime-duration-worstcase')) || 0; // بدترین مدت زمان توقف

    // 6- اثرگذاری
    data.stopCriticalService = toBoolean($(selector).data('stop-critical-service')); // توقف خدمات بحرانی
    data.criticalServiceTitle = toString($(selector).data('critical-service-title')); // عنوان خدمات بحرانی
    data.stopSensitiveService = toBoolean($(selector).data('stop-sensitive-service')); // توقف خدمات حساس
    data.stopServiceTitle = toString($(selector).data('stop-service-title')); // عنوان خدمات متوقف شده
    data.notStopAnyService = toBoolean($(selector).data('not-stop-any-service')); // عدم توقف هیچ خدماتی

    // 7- برنامه بازگشت
    data.hasRoleBackPlan = toBoolean($(selector).data('has-role-back-plan')); // وجود برنامه بازگشت
    data.roleBackPlanDescription = toString($(selector).data('role-back-plan-description')); // توضیحات برنامه بازگشت

    // 8- الزامات
    data.reasonRegulatory = toBoolean($(selector).data('reason-regulatory')); // الزام قانونی
    data.reasonTechnical = toBoolean($(selector).data('reason-technical')); // الزام فنی
    data.reasonSecurity = toBoolean($(selector).data('reason-security')); // الزام امنیتی
    data.reasonBusiness = toBoolean($(selector).data('reason-business')); // الزام کسب و کاری
    data.reasonOther = toBoolean($(selector).data('reason-other')); // سایر الزامات
    data.reasonOtherDescription = toString($(selector).data('reason-other-description')); // توضیحات الزامات دیگر

    return data;
}

function FetchData(jsonData) {
    // 1- اطلاعات افراد درگیر
    if (jsonData.executorNationalCode) {
        $('select[name="executor_user_nationalcode"]').val(jsonData.executorNationalCode).change();
    }
    if (jsonData.testerNationalCode) {
        $('select[name="tester_user_nationalcode"]').val(jsonData.testerNationalCode).change();
    }
    $('input[name="need_test"][value=' + (jsonData.testRequired ? 1 : 0) + ']').prop('checked', true).change();

    // 2- ویژگی های تغییر
    if (jsonData.changeLevel) {
        $('input[name="change_level"][value="' + jsonData.changeLevel + '"]').parents('.radio-box').click();
    }
    if (jsonData.classification) {
        $('input[name="classification"][value="' + jsonData.classification + '"]').parents('.radio-box').click();
    }
    if (jsonData.priority) {
        $('input[name="priority"][value="' + jsonData.priority + '"]').parents('.radio-box').click();
    }
    if (jsonData.riskLevel) {
        $('input[name="risk_level"][value="' + jsonData.riskLevel + '"]').parents('.radio-box').click();
    }

    // 3- اطلاعات تغییر
    if (jsonData.changeTitle) {
        $('input[name="change_title"]').val(jsonData.changeTitle);
    }
    if (jsonData.changeDescription) {
        $('textarea[name="change_description"]').val(jsonData.changeDescription);
    }
    $('input[name="change_location_data_center"]').prop('checked', jsonData.changeLocationDataCenter);
    ChangeLocation(jsonData.changeLocationDataCenterList, 'data-center-list');
    $('input[name="change_location_database"]').prop('checked', jsonData.changeLocationDatabase);
    ChangeLocation(jsonData.changeLocationDatabaseList, 'database-list');
    $('input[name="change_location_systems"]').prop('checked', jsonData.changeLocationSystems);
    ChangeLocation(jsonData.changeLocationSystemsList, 'systems-list');
    $('input[name="change_location_other"]').prop('checked', jsonData.changeLocationOther);
    if (jsonData.changeLocationOtherDescription) {
        $('input[name="change_location_other_description"]').val(jsonData.changeLocationOtherDescription);
    }

    // 4- حوزه و ارتباطات تغییر
    $('input[name="need_committee"]').prop('checked', jsonData.needCommittee);
    if (jsonData.committeeId > 0) {
        $('select[name="committee"]').val(jsonData.committeeId);
    }
    SetTeamCorp(jsonData.team_list, 'T')
    SetTeamCorp(jsonData.corp_list, 'C')

    // 5- زمانبندی تغییر
    SetDuration(jsonData.changingDuration, $('.scheduling-table tr.duration'));
    SetDuration(jsonData.downtimeDuration, $('.scheduling-table tr.downtime'));
    SetDuration(jsonData.downtimeDurationWorstCase, $('.scheduling-table tr.downtime-worstcase'));

    // 6- اثرگذاری
    if (jsonData.stopCriticalService) 
    {
        $('input[name="ImpactOnCriticalService"]').prop('checked', true);
        if (jsonData.criticalServiceTitle) {
            $('input[name="ImpactOnCriticalServiceDescription"]').val(jsonData.criticalServiceTitle);
        }
    
    }
    if (jsonData.stopSensitiveService) 
    {
        $('input[name="ImpactOnSensitiveService"]').prop('checked', true);
        if (jsonData.stopServiceTitle) {
            $('input[name="ImpactOnSensitiveServiceDescription"]').val(jsonData.stopServiceTitle);
        }
    }
    //در صورتی که دو گزینه ی فوق انتخاب نشده باشد این گزینه انتخاب می شود
    if (!jsonData.stopCriticalService && !jsonData.stopSensitiveService && jsonData.notStopAnyService) 
        $('input[name="ImpactNotOnAnyService"]').prop('checked', true);

    // 7- برنامه بازگشت
    if (jsonData.hasRoleBackPlan) {
        $('input[name="Rollback"].has').prop('checked', true);
        
        if (jsonData.roleBackPlanDescription !== '') {
            $('textarea[name="RollbackPlan"]').val(jsonData.roleBackPlanDescription);
        }            
    }
    else
    {
        $('input[name="Rollback"].has-not').prop('checked', true);
        $('textarea[name="RollbackPlan"]').val('');
    }

    // 8- الزامات
    $('input[name="ReasonRegulatory"]').prop('checked', jsonData.reasonRegulatory);
    $('input[name="ReasonTechnical"]').prop('checked', jsonData.reasonTechnical);
    $('input[name="ReasonSecurity"]').prop('checked', jsonData.reasonSecurity);
    $('input[name="ReasonBusiness"]').prop('checked', jsonData.reasonBusiness);
    $('input[name="ReasonOther"]').prop('checked', jsonData.reasonOther);
    if (jsonData.reasonOtherDescription!=='') {
        $('input[name="ReasonOtherDescription"]').val(jsonData.reasonOtherDescription);
    }
}

$(document).ready(function() {
    // مقداردهی سبک و سریع: داده‌ها را همگام می‌کنیم تا ورودی‌های مخفی به‌روز باشند
    try { updateTaskData(); updateNotificationDataInForm(); } catch (e) {}

    // اضافه کردن رویداد برای Ctrl + S
    $(document).on('keydown', function(e) {
        if (e.altKey && e.key === 's') {
            e.preventDefault(); // جلوگیری از رفتار پیش‌فرض مرورگر
            $('#save').click(); // صدا زدن رخداد کلیک روی دکمه save
        }
    });

    // رویداد حذف کاربر از نشان (delegated)
    // توضیح: برای عناصر جدید نیز کار خواهد کرد و فقط یک‌بار بایند می‌شود
    $(document).on('click', '.remove-user-btn', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const $badge = $(this).closest('.user-badge');
        const userId = $badge.data('user-id');
        $badge.addClass('hidden');
        $(this).attr('data-delete', 'true');
        setTimeout(function() { $badge.css('display', 'none'); }, 1000);
        const $container = $badge.closest('.users-container');
        const taskId = $container.data('task-id');
        const role = $container.data('role');
        removeUserFromTaskData(taskId, role, userId);
    });

    // رویداد نمایش سلکتور افزودن کاربر (delegated)
    $(document).on('click', '.add-user-btn', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const $container = $(this).closest('.users-container');
        const $selector = $container.find('.user-selector');
        const $combo = $container.find('.user-combo');
        $selector.show();
        $combo.focus();
        $(this).hide();
    });

    // رویداد تغییر کاربر انتخابی (delegated)
    $(document).on('change', '.user-combo', function() {
        const selectedValue = $(this).val();
        if (selectedValue) {
            const $opt = $(this).find('option:selected');
            const username = $opt.data('username');
            const fullname = $opt.data('fullname');
            const taskId = $(this).data('task-id');
            const role = $(this).data('role');
            addUserBadge(selectedValue, username, fullname, taskId, role);
            const $container = $(this).closest('.users-container');
            $container.find('.user-selector').hide();
            $container.find('.add-user-btn').css('display', 'inline-block');
            $(this).val('');
        }
    });

    // رویداد blur برای بستن سلکتور (delegated)
    $(document).on('blur', '.user-combo', function() {
        const combo = this;
        setTimeout(function() {
            const $container = $(combo).closest('.users-container');
            const $selector = $container.find('.user-selector');
            const $addBtn = $container.find('.add-user-btn');
            if (document.activeElement !== combo) {
                $selector.hide();
                $addBtn.css('display', 'inline-block');
                $(combo).val('');
            }
        }, 200);
    });

    // رویداد تغییر وضعیت تسک (delegated)
    $(document).on('click', '.deactivate-task-btn', function() {
        const taskId = $(this).data('task-id');
        const row = this.closest('tr');
        toggleTaskStatus(taskId, row);
    });

    $('.radio-box').click(
        function()
        {
            //پدر رادیوی جاری را به دست می آوریم که همه رادیوهای آن گروه را دسترسی پیدا کنیم
            parent = $(this).parent()
            ActiveInActiveImages(parent.find('.active img'), 'inactive')

            //دکمه فعال قبلی را غیرفعال می کنیم
            parent.find('input[type="radio"]').prop('checked', false);
            parent.find('.active').removeClass('active').addClass('inactive');

            //حالا دکمه فعلی را فعال می کنیم
            ActiveInActiveImages($(this).find('img'), 'active')
            $(this).removeClass('inactive').addClass('active')
            $(this).find('input[type="radio"]').prop('checked', true);
        })


    $('.check-list-detail img').click(
        function()
        {
            check_list_box = $(this).parents('.check-list-box')
            //در اینجا هر عنصر یک آیکون است
            //در صورتی که آیکون فعال باشد آن را غیرفعال می کنیم
            //در غیر این صورت آن را فعال می کنیم
            if (check_list_box.hasClass('active'))
            {
                check_list_box.removeClass('active').addClass('inactive')
                check_list_box.find('input[type="checkbox"]').prop('checked', false);
                ActiveInActiveImages($(this), 'inactive')
                // اگر این آخرین مورد باشد، باید آیکون اصلی را غبرفعال کنیم
                if (check_list_box.parent().find('input[type="checkbox"]:checked').length == 0)
                    check_list_box.parents('.content-row').find('.check-list-main-checkbox input[type="checkbox"]').prop('checked', false);
            }
            else
            {
                check_list_box.removeClass('inactive').addClass('active')
                check_list_box.find('input[type="checkbox"]').prop('checked', true);
                ActiveInActiveImages($(this), 'active')
                check_list_box.parents('.content-row').find('.check-list-main-checkbox input[type="checkbox"]').prop('checked', true);
            }
        });
        // مربوط به لیست شرکت ها و لیست تیم ها
    $('.change-team-corp .icon-list img').click(
        function()
        {
            
            if ($(this).hasClass('active'))
                {
                    $(this).removeClass('active').addClass('inactive')
                    $(this).prev('input[type="checkbox"]').prop('checked', false);
                }
                else
                {
                    $(this).removeClass('inactive').addClass('active')
                    $(this).prev('input[type="checkbox"]').prop('checked', true);
                } 
            // در پایان باید کنترل کنیم که اگر تیمی/شرکتی انتخاب نشده باشد، چک باکس مربوطه را انتخاب کرده و یا از حالت انتخاب خارج کنیم
            if ($('.change-team-corp .icon-list img.inactive').length == 0)
                $(this).parent().parent().find('.team-corp-checkbox').prop('checked', true)
            else
                $(this).parent().parent().find('.team-corp-checkbox').prop('checked', false)
        });

    $('.change-team-corp .team-corp-checkbox').click(function()
    {
        //اگر مربوط به تیم ها باشد
        var icon_list = $(this).parent().parent().find('.icon-list')
        if ($(this).prop('checked'))
            icon_list.find('img.inactive').click()
        else
            icon_list.find('img.active').click()

    })
    $(".all-icon").click(function() {
        if (! $(this).prop('checked'))
        {
            $(this).parents('.content-row').find('img').removeClass('active').addClass('inactive')
            $(this).parents('.content-row').find('input[type="checkbox"]').prop('checked', false);
        }

        else
        {
            $(this).parents('.content-row').find('img').removeClass('inactive').addClass('active')
            $(this).parents('.content-row').find('input[type="checkbox"]').prop('checked', true);

        }

    });
    // هنگامی که بر روی هر یک از input های رادیویی یا label کلیک می‌شود
    $('.need-committee-box input').on('click', function() {
        // انتخاب گزینه رادیویی
        $(this).prop('checked', true);

        // بررسی اینکه آیا گزینه "دارد" انتخاب شده است
        if ($(this).val() == 1) {
            $('#committee').show(); // نمایش کومبو
        } else {
            $('#committee').hide(); // پنهان کردن کومبو
            $('#committee').val(-1)
        }
    });
    $('.need-committee-box label').on('click', function() {
        $(this).prev().click()
    });
    $('.change-team-corp .radio-list .radio-box').click(
        function()
        {
            //ابتدا همه پنل ها را مخفی می کنیم
            $('.change-team-corp .content-row.team-icons').hide()
            $('.change-team-corp .content-row.corp-icons').hide()

            // بررسی می کنیم که کدام گزینه انتخاب شده است
            var val = $(this).data('code')
            $(this).addClass('active')
            $("input[name='domain']:checked").val(val);

            // اگر گزینه داخلی و یا هر دو انتحاب شده باشد پنل تیم ها را نمایش می دهیم
            if (val == 'Domain_Inside' || val == 'Domain_Between')
                $('.change-team-corp .content-row.team-icons').show()

            // اگر گزینه خارجی و یا هر دو انتحاب شده باشد پنل شرکت ها را نمایش می دهیم
            if (val == 'Domain_Outside' || val == 'Domain_Between')
                $('.change-team-corp .content-row.corp-icons').show()

            // اگر گزینه تیم ها انتخاب شود، باید شرکت های انتخاب شده از حالت انتخاب خارج شوند
            if (val == 'Domain_Inside')
            {
                $('.change-team-corp .content-row.corp-icons input[type="checkbox"]').prop('checked', false);
                // شرکت هایی که انتخاب شده است را حذف می کنیم
                $('.change-team-corp .content-row.corp-icons img.active').each(function () {  
                    $(this).click()
                })
                $(this).find('.team-corp-checkbox.corp').prop('checked', false)

            }
            // اگر گزینه شرکت ها انتخاب شود، باید تیم های انتخاب شده از حالت انتخاب خارج شوند   
            if (val == 'Domain_Outside')
            {
                $('.change-team-corp .content-row.team-icons input[type="checkbox"]').prop('checked', false);
                // تیم هایی که انتخاب شده است را حذف می کنیم
                $('.change-team-corp .content-row.team-icons img.active').each(function () {  
                    $(this).click()
                })
                $(this).find('.team-corp-checkbox.team').prop('checked', false)
            }
        });
    $('.corp-icons img').click(function () {
        if ($(this).hasClass('active'))
            ActiveInActiveImages($(this), 'active')
        else
            ActiveInActiveImages($(this), 'inactive')
    })



    $('#save').click(function(event) {
        event.preventDefault(); // جلوگیری از ارسال فرم به صورت پیش‌فرض

        // گرفتن مقدار request_id
        var requestId = $('input[name="request_id"]').val();
        var url;
        var method;

        // اعتبارسنجی داده‌ها
        var errors = form_validation();

        // اگر خطا وجود دارد، نمایش پیام خطا
        if (errors.length > 0) {
            $.alert({
                title: 'خطا',
                content: errors.join('<br>'),
            });
            return; // جلوگیری از ادامه
        }

        // بررسی اینکه آیا request_id وجود دارد یا خیر
        if (requestId) {
            // اگر request_id وجود دارد، از سرویس update استفاده می‌کنیم
            url = '/ConfigurationChangeRequest/request/' + requestId + '/';
        } else {
            // اگر request_id وجود ندارد، از سرویس create استفاده می‌کنیم
            url = '/ConfigurationChangeRequest/request/0/';
        }

        // جمع‌آوری داده‌های فرم
        var formData = $('form').serialize(); // یا می‌توانید داده‌های خاصی را جمع‌آوری کنید

        // ارسال درخواست AJAX
        $.ajax({
            url: url,
            method: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    //شناسه درخواست را مقداردهی می کنیم
                    //به این دلیل که اگر به هر دلیل شروع فرآیند به مشکل خورد، مشخص باشد که رکورد ایجاد شده است
                    $('#request_id').val(response.request_id)
                    //اگر فراخوانی موفقیت آمیز باشد، باید تابعی برای رفتن به مرحله بعد فراخوانی کنیم
                    url = '/ConfigurationChangeRequest/request/next_step/'+response.request_id+'/CON/';
                    data = {'request_id':response.request_id, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()}

                    $.ajax({
                        url: url,
                        method: 'POST',
                        data: data,
                        success: function(response) {
                            if (response.success) {
                                if (response.message)
                                    msg = response.message
                                else
                                    msg = 'اطلاعات با موفقیت ذخیره شده و فرم به مرحله بعدی ارسال شد'
            
                                $.alert({
                                    title: 'ارسال موفقیت آمیز',
                                    content: msg,
                                    buttons: {
                                        confirm: {
                                            text: 'بستن',
                                            btnClass: 'btn-blue',
                                            action: function() {
                                                window.location.href = '/ConfigurationChangeRequest/request/view/'+response.request_id+'/';
                                            }
                                        }
                                    }
                                    });                                
                            } else {
                                // در صورت بروز خطا، پیام‌های خطا را نمایش دهید
                                var errorMessage = response.message;
                                $.alert({
                                    title: 'خطا',
                                    content: errorMessage,
                                });
                            }
                        },
                        error: function(xhr) {
                            // در صورت بروز خطا، پیام خطا را نمایش می‌دهیم
                            // ایجاد یک عنصر موقتی
                            var tempDiv = $('<div>').html(xhr.responseText);

                            // استخراج متن از div با شناسه summary
                            var errorMessage = tempDiv.find('#summary').text().trim(); // استفاده از #summary
                            $.alert({
                                title: 'خطا',
                                content: errorMessage,
                            });
                        }
                    });
            

                } else {
                    // در صورت بروز خطا، پیام‌های خطا را نمایش دهید
                    var errorMessage = response.errors;
                    $.alert({
                        title: 'خطا',
                        content: errorMessage,
                    });
                }
            },
            error: function(xhr) {
                // در صورت بروز خطا، پیام خطا را نمایش می‌دهیم
                // ایجاد یک عنصر موقتی
                var tempDiv = $('<div>').html(xhr.responseText);

                // استخراج متن از div با شناسه summary
                var errorMessage = tempDiv.find('#summary').text().trim(); // استفاده از #summary
                $.alert({
                    title: 'خطا',
                    content: errorMessage,
                    buttons: {
                        confirm: {
                            text: 'بستن',
                            btnClass: 'btn-red',
                            action: function() {
                                // در اینجا می‌توانید اقدامات اضافی انجام دهید
                            }
                        }
                    }
                });
            }
        });
    });

    $('button.confirm').click(function() {
        var statusClass = $(this).data('status');
        var $button = $(this); // ذخیره دکمه برای استفاده بعدی

        // غیرفعال کردن دکمه
        $button.prop('disabled', true);

        // فراخوانی تابع confirm
        confirm(statusClass).then(function() {
            // در اینجا می‌توانید کدهایی که بعد از اتمام تابع confirm باید اجرا شوند را قرار دهید
            // فعال کردن دکمه دوباره
            $button.prop('disabled', false);
        }).catch(function() {
            // در صورت بروز خطا، دکمه را دوباره فعال کنید
            $button.prop('disabled', false);
        });
    });

    // آیکون‌های اعلان (delegated) + رفع باگ شناسه‌های ناموجود
    $(document).on('click', '.notification-icon', function() {
        const icon = $(this);
        let newStatus = 'active';
        if (icon.hasClass('active')) {
            icon.removeClass('active').addClass('inactive');
            ActiveInActiveImages(icon, 'inactive');
            newStatus = 'inactive';
        } else {
            icon.removeClass('inactive').addClass('active');
            ActiveInActiveImages(icon, 'active');
        }
        const notifyGroupId = icon.data('notify-group-id');
        const notificationType = icon.data('notification-type');
        updateNotificationData(notifyGroupId, notificationType, newStatus === 'active');
        console.log('Notification toggled:', {
            notifyGroupId: notifyGroupId,
            type: notificationType,
            status: newStatus
        });
    });
    
    
    $('#reject').click(function()
    {
        reject()        
    })
});
