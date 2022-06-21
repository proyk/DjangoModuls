from django import template
register = template.Library()
def css_classes_for_field(field, custom_classes):
    orig_class = field.field.widget.attrs.get('class', '')
    required = 'required' if field.field.required else ''
    classes = field.css_classes(' '.join([orig_class, custom_classes, required]))
    return classes
@register.filter(name="add_class")
def add_class(field, custom_classes=''):
    classes = css_classes_for_field(field, custom_classes)
    try:
        field.field.widget.widget.attrs.update({'class': classes})
    except:
        field.field.widget.attrs.update({'class': classes})
        return field