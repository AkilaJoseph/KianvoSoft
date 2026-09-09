"""Picks the generated brand artwork to show when a record has no image.

    {% load brand_art %}
    <img src="{% brand_art 'blog' post.category.slug %}" alt="...">

Looks for `generated/<kind>-<slug>.svg` and falls back to
`generated/fallback-<kind>.svg`, so a new category without its own cover still
renders something on-brand instead of a broken image.

Building the path with `{% static '.../blog-' %}{{ slug }}.svg` would not do:
under `CompressedManifestStaticFilesStorage` a partial path is not in the
manifest and `{% static %}` raises `ValueError` in production.
"""

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()

GENERATED = 'assets/img/generated'
LAST_RESORT = f'{GENERATED}/fallback-blog.svg'

# Resolution is stable for the life of the process, and a listing page asks the
# same question once per row.
_cache = {}


def _exists(path):
    if path in _cache:
        return _cache[path]
    if settings.DEBUG:
        found = finders.find(path) is not None
    else:
        try:
            static(path)
            found = True
        except ValueError:
            found = False
    _cache[path] = found
    return found


@register.simple_tag
def brand_art(kind, slug=None):
    """URL of the brand cover for `kind` (blog, service, project, product,
    announcement), preferring the `slug` variant when one has been generated."""
    candidates = []
    if slug:
        candidates.append(f'{GENERATED}/{kind}-{slug}.svg')
    candidates.append(f'{GENERATED}/fallback-{kind}.svg')
    for path in candidates:
        if _exists(path):
            return static(path)
    return static(LAST_RESORT)


@register.filter
def initials(value, count=2):
    """'Loyce Paul' -> 'LP'. Used for the avatar/logo stand-ins."""
    words = [w for w in str(value or '').split() if w[:1].isalnum()]
    return ''.join(w[0] for w in words[:count]).upper() or '?'


@register.simple_tag
def brand_monogram(kind='partner'):
    """Initials badge used where a real logo or photo is missing — we never
    invent an organisation's mark or a person's face."""
    path = f'{GENERATED}/monogram-{kind}.svg'
    return static(path if _exists(path) else f'{GENERATED}/monogram-partner.svg')
