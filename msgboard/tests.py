import pytest
from django.db.models.query import QuerySet

from .models import UserMessage


@pytest.mark.django_db()
def test_main_feed():
    out = UserMessage.messages.main_feed()
    assert isinstance(out, QuerySet)
    assert all(isinstance(m, UserMessage) for m in out)
    assert list(out.values_list('author__user__username', 'text')) == [
        ('zombie', 'Braaaiiiinz!'),
        ('robot', 'Beep Beep, Boop Boop!'),
        ('woman1', 'Hi!'),
    ]
