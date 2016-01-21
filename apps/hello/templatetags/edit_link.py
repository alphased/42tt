from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django import template


register = template.Library()


@register.simple_tag(name='edit_link', takes_context=True)
def make_edit_link(context, object):
    content = 'Edit (admin)'

    content_type = ContentType.objects.get_for_model(object.__class__)
    app_name = content_type.app_label
    model_name = content_type.model

    named_url = 'admin:%s_%s_change' % (app_name, model_name)
    url = reverse(named_url, args=(object.id,))

    return '<a href="%s">%s</a>' % (url, content)
