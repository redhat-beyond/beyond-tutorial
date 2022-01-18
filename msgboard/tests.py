import pytest
from django.db.models.query import QuerySet

from accounts.models import Account
from .models import UserMessage
from .forms import UserMessageForm


@pytest.mark.django_db
def test_main_feed():
    out = UserMessage.messages.main_feed()
    assert isinstance(out, QuerySet)
    assert all(isinstance(m, UserMessage) for m in out)
    assert list(out.values_list('author__user__username', 'text')) == [
        ('zombie', 'Braaaiiiinz!'),
        ('robot', 'Beep Beep, Boop Boop!'),
        ('woman1', 'Hi!'),
    ]


@pytest.mark.django_db
def test_main_page_shows_only_feed_when_logged_out(client):
    response = client.get('/')

    assert response.status_code == 200
    assert isinstance(response.context['messages'], QuerySet)
    assert response.context.get("form") is None
    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    assert 'msgboard/board.html' in template_names


@pytest.fixture
def some_author():
    return Account.accounts.first()


@pytest.fixture
def logged_in_client(client, some_author):
    client.force_login(some_author.user)
    return client


@pytest.mark.django_db
def test_main_page_shows_post_form_when_logged_in(logged_in_client):
    response = logged_in_client.get('/')

    assert response.status_code == 200
    assert isinstance(response.context['messages'], QuerySet)
    assert isinstance(response.context.get("form"), UserMessageForm)
    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    assert 'msgboard/board.html' in template_names


@pytest.mark.django_db
def test_post_form_adds_a_new_latest_post(logged_in_client, some_author):
    initial_posts_no = UserMessage.messages.count()
    post_text = '__some_post_text__'

    response = logged_in_client.post('/', {'text': post_text})
    assert response.status_code == 302
    assert response.url == '/'
    assert UserMessage.messages.count() == initial_posts_no + 1
    latest_post = UserMessage.messages.main_feed().first()
    assert latest_post.text == post_text
    assert latest_post.author == some_author


@pytest.mark.django_db
def test_post_rejected_when_logged_out(client):
    initial_posts_no = UserMessage.messages.count()

    response = client.post('/', {'text': "thrown away"})
    assert response.status_code == 302
    assert response.url == '/'
    assert UserMessage.messages.count() == initial_posts_no


@pytest.mark.django_db
def test_empty_post_is_rejected(logged_in_client):
    initial_posts_no = UserMessage.messages.count()

    response = logged_in_client.post('/', {'text': ""})
    assert response.status_code == 200
    assert isinstance(response.context['messages'], QuerySet)
    template_names = set(tmpl.origin.template_name for tmpl in response.templates)
    assert 'msgboard/board.html' in template_names
    form = response.context.get("form")
    assert isinstance(form, UserMessageForm)
    assert not form.is_valid()
    assert UserMessage.messages.count() == initial_posts_no
