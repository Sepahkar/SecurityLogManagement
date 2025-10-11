from django.forms import widgets
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class RTLCheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    """Custom checkbox widget with RTL support"""
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        # ensure string comparison for safety
        value_set = set(str(v) for v in value)
        final_attrs = self.build_attrs(attrs or {})
        output = []
        options = list(self.choices)
        base_id = final_attrs.get('id', name)
        for i, (option_value, option_label) in enumerate(options):
            checked = str(option_value) in value_set
            checkbox_id = f"{base_id}_{i}"
            output.append(format_html(
                '<div class="checkbox-row" style="direction: rtl; text-align: right; margin: 5px 0;">'
                '<input type="checkbox" name="{}" value="{}" id="{}" {}>'
                '<label for="{}" style="margin-right: 8px;">{}</label>'
                '</div>',
                name, option_value, checkbox_id,
                'checked' if checked else '',
                checkbox_id, option_label
            ))
        return mark_safe('\n'.join(output))


class RTLCheckboxInput(widgets.CheckboxInput):
    """Custom checkbox widget with RTL support"""
    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(attrs or {})
        checkbox_id = final_attrs.get('id', name)
        checked = bool(value)
        label = final_attrs.get('label', '')
        return format_html(
            '<div style="direction: rtl; text-align: right;">'
            '<input type="checkbox" name="{}" value="1" id="{}" {}>'
            '<label for="{}" style="margin-right: 8px;">{}</label>'
            '</div>',
            name, checkbox_id,
            'checked' if checked else '',
            checkbox_id, label
        )


class RTLRadioSelect(widgets.RadioSelect):
    """Custom radio widget with RTL support"""
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs or {})
        output = []
        options = list(self.choices)
        base_id = final_attrs.get('id', name)
        for i, (option_value, option_label) in enumerate(options):
            checked = str(option_value) == str(value)
            radio_id = f"{base_id}_{i}"
            output.append(format_html(
                '<div class="radio-row" style="direction: rtl; text-align: right; margin: 5px 0;">'
                '<input type="radio" name="{}" value="{}" id="{}" {}>'
                '<label for="{}" style="margin-right: 8px;">{}</label>'
                '</div>',
                name, option_value, radio_id,
                'checked' if checked else '',
                radio_id, option_label
            ))
        return mark_safe('\n'.join(output))


class RTLSelect(widgets.Select):
    """Custom select widget with RTL support"""
    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(attrs or {})
        style = final_attrs.get('style', '')
        final_attrs['style'] = (style + '; direction: rtl; text-align: right;').strip('; ')
        return super().render(name, value, final_attrs, renderer)


class RTLTextInput(widgets.TextInput):
    """Custom text input widget with RTL support"""
    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(attrs or {})
        style = final_attrs.get('style', '')
        final_attrs['style'] = (style + '; direction: rtl; text-align: right;').strip('; ')
        return super().render(name, value, final_attrs, renderer)


class RTLTextarea(widgets.Textarea):
    """Custom textarea widget with RTL support"""
    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(attrs or {})
        style = final_attrs.get('style', '')
        final_attrs['style'] = (style + '; direction: rtl; text-align: right;').strip('; ')
        return super().render(name, value, final_attrs, renderer)
