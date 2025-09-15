$(document).ready(function() {
    // Sidebar navigation
    $('.sidebar-item').click(function() {
        $('.sidebar-item').removeClass('active');
        $(this).addClass('active');
    });

    // Characteristic options
    $('.option-item').click(function() {
        $(this).siblings().removeClass('active');
        $(this).addClass('active');
    });

    // System options
    $('.system-option').click(function() {
        $('.system-option').removeClass('active');
        $(this).addClass('active');
    });

    // Scope options
    $('.scope-option').click(function() {
        $('.scope-option').removeClass('active');
        $(this).addClass('active');
    });

    // Submit button
    $('.submit-btn').click(function() {
        // Add submit logic here
        alert('فرم در حال ارسال...');
    });

    // Initialize form data on page load
    initializeFormData();
});

// Function to initialize form data based on request object
function initializeFormData() {
    // This function will be called to populate the form with data from the request object
    // The data will be passed from Django template to JavaScript
    
    // Get request data from Django template
    const requestData = window.requestData || {};
    
    if (Object.keys(requestData).length === 0) {
        console.log('No request data available');
        return;
    }

    // Initialize risk level
    initializeRiskLevel(requestData.risk_level);
    
    // Initialize priority
    initializePriority(requestData.priority);
    
    // Initialize change level (scope)
    initializeChangeLevel(requestData.change_level);
    
    // Initialize classification
    initializeClassification(requestData.classification);
    
    // Initialize change locations
    initializeChangeLocations(requestData);
    
    // Initialize change domain
    initializeChangeDomain(requestData.change_domain);
    
    // Initialize impact section
    initializeImpactSection(requestData);
    
    // Initialize task assignments
    initializeTaskAssignments(requestData.tasks);
    
    // Initialize selected choices
    initializeSelectedChoices(requestData);
}

// Initialize risk level selection
function initializeRiskLevel(riskLevel) {
    if (!riskLevel || !riskLevel.Code) return;
    
    $('.risk-level .option-item').removeClass('active');
    $('.risk-level .option-item').each(function() {
        const optionText = $(this).find('span').text().trim();
        if (optionText === riskLevel.Caption) {
            $(this).addClass('active');
        }
    });
}

// Initialize priority selection
function initializePriority(priority) {
    if (!priority || !priority.Code) return;
    
    $('.priority .option-item').removeClass('active');
    $('.priority .option-item').each(function() {
        const optionText = $(this).find('span').text().trim();
        if (optionText === priority.Caption) {
            $(this).addClass('active');
        }
    });
}

// Initialize change level (scope) selection
function initializeChangeLevel(changeLevel) {
    if (!changeLevel || !changeLevel.Code) return;
    
    $('.scope .option-item').removeClass('active');
    $('.scope .option-item').each(function() {
        const optionText = $(this).find('span').text().trim();
        if (optionText === changeLevel.Caption) {
            $(this).addClass('active');
        }
    });
}

// Initialize classification selection
function initializeClassification(classification) {
    if (!classification || !classification.Code) return;
    
    $('.classification .option-item').removeClass('active');
    $('.classification .option-item').each(function() {
        const optionText = $(this).find('span').text().trim();
        if (optionText === classification.Caption) {
            $(this).addClass('active');
        }
    });
}

// Initialize change locations
function initializeChangeLocations(requestData) {
    // Data center
    if (requestData.change_location_data_center) {
        $('.system-option').eq(2).addClass('active'); // Data center option
    }
    
    // Database
    if (requestData.change_location_database) {
        $('.system-option').eq(3).addClass('active'); // Database option
    }
    
    // Systems
    if (requestData.change_location_systems) {
        $('.system-option').eq(1).addClass('active'); // Systems option
    }
    
    // Other
    if (requestData.change_location_other) {
        $('.system-option').eq(0).addClass('active'); // Other option
    }
}

// Initialize change domain
function initializeChangeDomain(changeDomain) {
    if (!changeDomain || !changeDomain.Code) return;
    
    $('.scope-option').removeClass('active');
    $('.scope-option').each(function() {
        const optionText = $(this).find('span').text().trim();
        if (optionText === changeDomain.Caption) {
            $(this).addClass('active');
        }
    });
}

// Initialize impact section
function initializeImpactSection(requestData) {
    // This will be handled by Django template conditionals
    // JavaScript can be used for additional dynamic behavior if needed
}

// Initialize task assignments
function initializeTaskAssignments(tasks) {
    if (!tasks || tasks.length === 0) return;
    
    // Tasks are already populated by Django template
    // JavaScript can be used for additional functionality like filtering, sorting, etc.
}

// Initialize selected choices display
function initializeSelectedChoices(requestData) {
    // Update the selected choices display based on the data
    updateSelectedChoices();
}

// Function to update selected choices display
function updateSelectedChoices() {
    const selectedChoices = [];
    
    // Check which locations are selected
    $('.system-option.active').each(function() {
        const icon = $(this).find('i').attr('class');
        const title = $(this).find('span').text();
        selectedChoices.push({
            icon: icon,
            title: title
        });
    });
    
    // Update the display
    const choiceIcons = $('.choice-icons');
    choiceIcons.empty();
    
    selectedChoices.forEach(function(choice) {
        const iconElement = $('<i>').attr('class', choice.icon).attr('title', choice.title);
        choiceIcons.append(iconElement);
    });
    
    // If no choices are selected, show a message
    if (selectedChoices.length === 0) {
        choiceIcons.append('<span style="color: #6c757d; font-size: 0.9rem;">هیچ انتخابی انجام نشده است</span>');
    }
}

// Function to handle form validation
function validateForm() {
    let isValid = true;
    const errors = [];
    
    // Check if at least one characteristic is selected
    if ($('.characteristic-box .option-item.active').length === 0) {
        errors.push('لطفاً حداقل یک ویژگی تغییر را انتخاب کنید');
        isValid = false;
    }
    
    // Check if at least one system location is selected
    if ($('.system-option.active').length === 0) {
        errors.push('لطفاً حداقل یک محل تغییر را انتخاب کنید');
        isValid = false;
    }
    
    // Check if change domain is selected
    if ($('.scope-option.active').length === 0) {
        errors.push('لطفاً محدوده تغییر را انتخاب کنید');
        isValid = false;
    }
    
    if (!isValid) {
        alert('خطاهای زیر را برطرف کنید:\n' + errors.join('\n'));
    }
    
    return isValid;
}

// Function to collect form data
function collectFormData() {
    const formData = {
        // Risk level
        risk_level: $('.risk-level .option-item.active').find('span').text().trim(),
        
        // Priority
        priority: $('.priority .option-item.active').find('span').text().trim(),
        
        // Change level
        change_level: $('.scope .option-item.active').find('span').text().trim(),
        
        // Classification
        classification: $('.classification .option-item.active').find('span').text().trim(),
        
        // Change locations
        change_locations: {
            data_center: $('.system-option').eq(2).hasClass('active'),
            database: $('.system-option').eq(3).hasClass('active'),
            systems: $('.system-option').eq(1).hasClass('active'),
            other: $('.system-option').eq(0).hasClass('active')
        },
        
        // Change domain
        change_domain: $('.scope-option.active').find('span').text().trim(),
        
        // Other description
        other_description: $('.other-input input').val()
    };
    
    return formData;
}

// Function to submit form
function submitForm() {
    if (!validateForm()) {
        return false;
    }
    
    const formData = collectFormData();
    
    // Show loading state
    $('.submit-btn').prop('disabled', true).text('در حال ارسال...');
    
    // Submit form data
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: {
            'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
            'form_data': JSON.stringify(formData)
        },
        success: function(response) {
            if (response.success) {
                alert('فرم با موفقیت ارسال شد');
                // Redirect or update page as needed
            } else {
                alert('خطا در ارسال فرم: ' + response.message);
            }
        },
        error: function(xhr, status, error) {
            alert('خطا در ارسال فرم: ' + error);
        },
        complete: function() {
            // Reset button state
            $('.submit-btn').prop('disabled', false).text('اصلاح فرم');
        }
    });
}

// Update submit button click handler
$(document).ready(function() {
    $('.submit-btn').off('click').on('click', function(e) {
        e.preventDefault();
        submitForm();
    });
    
    // Update selected choices when system options change
    $('.system-option').on('click', function() {
        updateSelectedChoices();
    });
});
