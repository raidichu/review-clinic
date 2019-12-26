from django import template

from ..models import Reply

register = template.Library()


@register.simple_tag
def get_status(comment_id, status):
    num = len(Reply.objects.filter(comment_id=comment_id, status=status))
    return num



