from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if not isinstance(dictionary, dict):
        return 0
    return dictionary.get(key, 0)


@register.filter
def get_display_value(obj, field_name):
    """Return a display-friendly value for a field of an object."""
    if not obj or not field_name:
        return ''
    # Choice field display (get_FOO_display)
    get_display = getattr(obj, f'get_{field_name}_display', None)
    if get_display:
        return get_display()
    val = getattr(obj, field_name, None)
    if val is None:
        return ''
    if isinstance(val, bool):
        return val
    s = str(val)
    return s[:60] + '...' if len(s) > 60 else s


@register.filter
def get_image_url(obj, meta):
    """Return the first image URL from an object based on meta's img field list."""
    if not obj or not meta:
        return None
    for fname in meta.get('img', []):
        f = getattr(obj, fname, None)
        if f and hasattr(f, 'url'):
            try:
                return f.url
            except Exception:
                pass
    return None
