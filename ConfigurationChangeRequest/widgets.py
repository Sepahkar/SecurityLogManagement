"""
Custom widgets for admin forms
"""

from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import ForeignKeyRawIdWidget, ManyToManyRawIdWidget


class EnhancedSelectWidget(forms.Select):
    """
    Enhanced select widget with better styling and search functionality
    """
    
    def __init__(self, attrs=None, choices=(), searchable=False):
        super().__init__(attrs, choices)
        self.searchable = searchable
        
        if attrs is None:
            attrs = {}
        
        # Add custom CSS class
        if 'class' in attrs:
            attrs['class'] += ' enhanced-select'
        else:
            attrs['class'] = 'enhanced-select'
            
        if self.searchable:
            attrs['data-searchable'] = 'true'
            
        self.attrs = attrs

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        
        if self.searchable:
            # Add search functionality
            search_script = """
            <script>
            document.addEventListener('DOMContentLoaded', function() {
                const select = document.querySelector('select[name="{}"]');
                if (select && select.getAttribute('data-searchable') === 'true') {{
                    const wrapper = document.createElement('div');
                    wrapper.className = 'enhanced-select-wrapper';
                    wrapper.style.position = 'relative';
                    
                    const searchInput = document.createElement('input');
                    searchInput.type = 'text';
                    searchInput.placeholder = 'جستجو...';
                    searchInput.className = 'enhanced-select-search';
                    searchInput.style.cssText = `
                        width: 100%;
                        padding: 8px 12px;
                        border: 2px solid var(--border-color);
                        border-radius: 6px;
                        background-color: var(--bg-color);
                        color: var(--text-color);
                        font-size: 14px;
                        margin-bottom: 8px;
                    `;
                    
                    select.style.display = 'none';
                    select.parentNode.insertBefore(wrapper, select);
                    wrapper.appendChild(searchInput);
                    wrapper.appendChild(select);
                    
                    const options = Array.from(select.options);
                    
                    searchInput.addEventListener('input', function() {{
                        const searchTerm = this.value.toLowerCase();
                        options.forEach(option => {{
                            const text = option.textContent.toLowerCase();
                            option.style.display = text.includes(searchTerm) ? 'block' : 'none';
                        }});
                    }});
                }}
            }});
            </script>
            """.format(name)
            
            html += search_script
        
        return mark_safe(html)


class PersianDateWidget(forms.TextInput):
    """
    Persian date input widget with date picker
    """
    
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        
        attrs.update({
            'class': 'persian-date',
            'placeholder': '1403/01/01',
            'maxlength': '10',
        })
        
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        
        # Add Persian date picker functionality
        script = """
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const input = document.querySelector('input[name="{}"]');
            if (input && input.classList.contains('persian-date')) {{
                input.addEventListener('input', function() {{
                    let value = this.value.replace(/\\D/g, '');
                    if (value.length >= 8) {{
                        value = value.substring(0, 4) + '/' + 
                               value.substring(4, 6) + '/' + 
                               value.substring(6, 8);
                        this.value = value;
                    }}
                }});
                
                input.addEventListener('keypress', function(e) {{
                    if (!/\\d/.test(e.key) && !['Backspace', 'Delete', 'Tab', 'Enter'].includes(e.key)) {{
                        e.preventDefault();
                    }}
                }});
                
                // Add date picker button
                const wrapper = document.createElement('div');
                wrapper.style.position = 'relative';
                wrapper.style.display = 'inline-block';
                wrapper.style.width = '100%';
                
                this.parentNode.insertBefore(wrapper, this);
                wrapper.appendChild(this);
                
                const pickerBtn = document.createElement('button');
                pickerBtn.type = 'button';
                pickerBtn.innerHTML = '📅';
                pickerBtn.title = 'انتخاب تاریخ';
                pickerBtn.style.cssText = `
                    position: absolute;
                    left: 10px;
                    top: 50%;
                    transform: translateY(-50%);
                    background: none;
                    border: none;
                    font-size: 16px;
                    cursor: pointer;
                    padding: 5px;
                    border-radius: 4px;
                    transition: background-color 0.3s ease;
                `;
                
                pickerBtn.addEventListener('mouseenter', function() {{
                    this.style.backgroundColor = 'var(--light-color)';
                }});
                
                pickerBtn.addEventListener('mouseleave', function() {{
                    this.style.backgroundColor = 'transparent';
                }});
                
                wrapper.appendChild(pickerBtn);
            }}
        }});
        </script>
        """.format(name)
        
        return mark_safe(html + script)


class TimeWidget(forms.TextInput):
    """
    Time input widget with time picker
    """
    
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        
        attrs.update({
            'class': 'time-input',
            'placeholder': '14:30',
            'maxlength': '5',
        })
        
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        
        # Add time picker functionality
        script = """
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const input = document.querySelector('input[name="{}"]');
            if (input && input.classList.contains('time-input')) {{
                input.addEventListener('input', function() {{
                    let value = this.value.replace(/\\D/g, '');
                    if (value.length >= 4) {{
                        value = value.substring(0, 2) + ':' + value.substring(2, 4);
                        this.value = value;
                    }}
                }});
                
                input.addEventListener('keypress', function(e) {{
                    if (!/\\d/.test(e.key) && !['Backspace', 'Delete', 'Tab', 'Enter'].includes(e.key)) {{
                        e.preventDefault();
                    }}
                }});
                
                // Add time picker button
                const wrapper = document.createElement('div');
                wrapper.style.position = 'relative';
                wrapper.style.display = 'inline-block';
                wrapper.style.width = '100%';
                
                this.parentNode.insertBefore(wrapper, this);
                wrapper.appendChild(this);
                
                const pickerBtn = document.createElement('button');
                pickerBtn.type = 'button';
                pickerBtn.innerHTML = '🕐';
                pickerBtn.title = 'انتخاب زمان';
                pickerBtn.style.cssText = `
                    position: absolute;
                    left: 10px;
                    top: 50%;
                    transform: translateY(-50%);
                    background: none;
                    border: none;
                    font-size: 16px;
                    cursor: pointer;
                    padding: 5px;
                    border-radius: 4px;
                    transition: background-color 0.3s ease;
                `;
                
                pickerBtn.addEventListener('mouseenter', function() {{
                    this.style.backgroundColor = 'var(--light-color)';
                }});
                
                pickerBtn.addEventListener('mouseleave', function() {{
                    this.style.backgroundColor = 'transparent';
                }});
                
                wrapper.appendChild(pickerBtn);
            }}
        }});
        </script>
        """.format(name)
        
        return mark_safe(html + script)


class RichTextWidget(forms.Textarea):
    """
    Rich text editor widget
    """
    
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        
        attrs.update({
            'class': 'rich-text-editor',
            'rows': 4,
        })
        
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        
        # Add rich text editor functionality
        script = """
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const textarea = document.querySelector('textarea[name="{}"]');
            if (textarea && textarea.classList.contains('rich-text-editor')) {{
                // Create toolbar
                const toolbar = document.createElement('div');
                toolbar.className = 'rich-text-toolbar';
                toolbar.style.cssText = `
                    background: var(--light-color);
                    border: 1px solid var(--border-color);
                    border-bottom: none;
                    padding: 8px;
                    border-radius: 6px 6px 0 0;
                    display: flex;
                    gap: 5px;
                `;
                
                const buttons = [
                    {{'icon': 'B', 'title': 'پررنگ', 'action': 'bold'}},
                    {{'icon': 'I', 'title': 'ایتالیک', 'action': 'italic'}},
                    {{'icon': 'U', 'title': 'زیرخط', 'action': 'underline'}},
                    {{'icon': '📝', 'title': 'لیست', 'action': 'insertUnorderedList'}},
                    {{'icon': '🔗', 'title': 'لینک', 'action': 'createLink'}},
                ];
                
                buttons.forEach(btn => {{
                    const button = document.createElement('button');
                    button.type = 'button';
                    button.innerHTML = btn.icon;
                    button.title = btn.title;
                    button.style.cssText = `
                        background: var(--bg-color);
                        border: 1px solid var(--border-color);
                        border-radius: 4px;
                        padding: 6px 10px;
                        cursor: pointer;
                        font-size: 14px;
                        transition: all 0.3s ease;
                    `;
                    
                    button.addEventListener('click', function() {{
                        document.execCommand(btn.action, false, null);
                        textarea.focus();
                    }});
                    
                    button.addEventListener('mouseenter', function() {{
                        this.style.backgroundColor = 'var(--primary-color)';
                        this.style.color = 'white';
                        this.style.borderColor = 'var(--primary-color)';
                    }});
                    
                    button.addEventListener('mouseleave', function() {{
                        this.style.backgroundColor = 'var(--bg-color)';
                        this.style.color = 'var(--text-color)';
                        this.style.borderColor = 'var(--border-color)';
                    }});
                    
                    toolbar.appendChild(button);
                }});
                
                textarea.parentNode.insertBefore(toolbar, textarea);
                textarea.style.borderRadius = '0 0 6px 6px';
                textarea.style.borderTop = 'none';
            }}
        }});
        </script>
        """.format(name)
        
        return mark_safe(html + script)


class FileUploadWidget(forms.FileInput):
    """
    Enhanced file upload widget with drag and drop
    """
    
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        
        attrs.update({
            'class': 'enhanced-file-input',
        })
        
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        
        # Add drag and drop functionality
        script = """
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const fileInput = document.querySelector('input[name="{}"]');
            if (fileInput && fileInput.classList.contains('enhanced-file-input')) {{
                const wrapper = document.createElement('div');
                wrapper.className = 'file-upload-wrapper';
                wrapper.style.cssText = `
                    border: 2px dashed var(--border-color);
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    background: var(--light-color);
                    transition: all 0.3s ease;
                    cursor: pointer;
                `;
                
                wrapper.innerHTML = `
                    <div class="upload-icon" style="font-size: 48px; margin-bottom: 10px;">📁</div>
                    <div class="upload-text" style="color: var(--text-color); font-weight: 500;">
                        فایل را اینجا بکشید یا کلیک کنید
                    </div>
                    <div class="upload-hint" style="color: var(--secondary-color); font-size: 12px; margin-top: 5px;">
                        حداکثر اندازه فایل: 10MB
                    </div>
                `;
                
                fileInput.style.display = 'none';
                fileInput.parentNode.insertBefore(wrapper, fileInput);
                wrapper.appendChild(fileInput);
                
                // Click to upload
                wrapper.addEventListener('click', function() {{
                    fileInput.click();
                }});
                
                // Drag and drop
                ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {{
                    wrapper.addEventListener(eventName, preventDefaults, false);
                }});
                
                function preventDefaults(e) {{
                    e.preventDefault();
                    e.stopPropagation();
                }}
                
                ['dragenter', 'dragover'].forEach(eventName => {{
                    wrapper.addEventListener(eventName, highlight, false);
                }});
                
                ['dragleave', 'drop'].forEach(eventName => {{
                    wrapper.addEventListener(eventName, unhighlight, false);
                }});
                
                function highlight() {{
                    wrapper.style.borderColor = 'var(--primary-color)';
                    wrapper.style.backgroundColor = 'rgba(0, 123, 255, 0.1)';
                }}
                
                function unhighlight() {{
                    wrapper.style.borderColor = 'var(--border-color)';
                    wrapper.style.backgroundColor = 'var(--light-color)';
                }}
                
                wrapper.addEventListener('drop', handleDrop, false);
                
                function handleDrop(e) {{
                    const dt = e.dataTransfer;
                    const files = dt.files;
                    fileInput.files = files;
                    
                    // Update display
                    if (files.length > 0) {{
                        wrapper.querySelector('.upload-text').textContent = 
                            files.length === 1 ? files[0].name : `${{files.length}} فایل انتخاب شد`;
                    }}
                    
                    // Trigger change event
                    const event = new Event('change', {{ bubbles: true }});
                    fileInput.dispatchEvent(event);
                }}
                
                // File input change
                fileInput.addEventListener('change', function() {{
                    if (this.files.length > 0) {{
                        wrapper.querySelector('.upload-text').textContent = 
                            this.files.length === 1 ? this.files[0].name : `${{this.files.length}} فایل انتخاب شد`;
                    }}
                }});
            }}
        }});
        </script>
        """.format(name)
        
        return mark_safe(html + script)


class StatusDisplayWidget(forms.Widget):
    """
    Widget for displaying status with badges
    """
    
    def render(self, name, value, attrs=None, renderer=None):
        status_map = {
            'DRAFTD': ('📝 پیش نویس', 'status-draft'),
            'DIRMAN': ('👨‍💼 مدیر مستقیم', 'status-active'),
            'RELMAN': ('👨‍💻 مدیر مربوطه', 'status-active'),
            'COMITE': ('👥 کمیته', 'status-active'),
            'DOTASK': ('⚙️ انجام تسک‌ها', 'status-active'),
            'FINISH': ('✅ خاتمه یافته', 'status-completed'),
            'FAILED': ('❌ ناموفق', 'status-failed'),
            'ERRORF': ('⚠️ خطا', 'status-failed'),
        }
        
        if value in status_map:
            text, css_class = status_map[value]
            return format_html(
                '<span class="status-badge {}">{}</span>',
                css_class, text
            )
        
        return value or '-'


class PriorityDisplayWidget(forms.Widget):
    """
    Widget for displaying priority with badges
    """
    
    def render(self, name, value, attrs=None, renderer=None):
        if not value:
            return '-'
        
        priority_text = value.Caption if hasattr(value, 'Caption') else str(value)
        
        if 'Standard' in priority_text:
            return format_html('<span class="priority-badge priority-standard">⚡ استاندارد</span>')
        elif 'Urgent' in priority_text:
            return format_html('<span class="priority-badge priority-urgent">🔥 فوری</span>')
        elif 'Emergency' in priority_text:
            return format_html('<span class="priority-badge priority-emergency">🚨 اضطراری</span>')
        
        return priority_text
