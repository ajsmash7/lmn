from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, EditNoteForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from __future__ import unicode_literals

import re

from django import template

from django.db.models import Model
from django.template.defaultfilters import urlencode
from django.utils.safestring import mark_safe

try:
    from django_bitly.templatetags.bitly import bitlify
    DJANGO_BITLY = True
except ImportError:
    DJANGO_BITLY = False


@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':

        form = NewNoteForm(request.POST, instance=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user

            note.show = show
            note.posted_date = timezone.now()
            note.save()
            return redirect('lmn:note_detail', note_pk=note.pk)

    else :
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html' , { 'form' : form , 'show':show })



def latest_notes(request):
    notes = Note.objects.all().order_by('posted_date').reverse()
    return render(request, 'lmn/notes/note_list.html', {'notes':notes})


def notes_for_show(request, show_pk):   # pk = show pk

    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('posted_date').reverse()
    show = Show.objects.get(pk=show_pk)  # Contains artist, venue

    return render(request, 'lmn/notes/note_list.html', {'show': show, 'notes':notes } )



def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    return render(request, 'lmn/notes/note_detail.html' , {'note' : note })

@login_required
def edit_note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)

    if note.user.pk != request.user:
        raise PermissionError("User Is not Authorized to change this note")

    if request.method == 'POST':

        form = EditNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('lmn:note_detail', note_pk)

        else:
            message = 'Please check the changes you entered'
            args = {'form': form, 'message': message}
            return render(request, 'lmn/notes/edit_note_detail.html', args)

    else:
        form = EditNoteForm(instance=request.user)
        args = {'form': form}
        return render(request, 'lmn/notes/edit_note_detail.html', args)

register = template.Library()

TWITTER_ENDPOINT = 'https://twitter.com/intent/tweet?text=%s'
FACEBOOK_ENDPOINT = 'https://www.facebook.com/sharer/sharer.php?u=%s'

BITLY_REGEX = re.compile(r'^https?://bit\.ly/')

def compile_text(context, text):
    ctx = template.context.Context(context)
    return template.Template(text).render(ctx)


def _build_url(request, obj_or_url):
    if obj_or_url is not None:
        if isinstance(obj_or_url, Model):
            if DJANGO_BITLY:
                url = bitlify(obj_or_url)  # type: str
                if not BITLY_REGEX.match(url):
                    return request.build_absolute_uri(
                        obj_or_url.get_absolute_url()
                    )
                else:
                    return url
            else:
                return request.build_absolute_uri(obj_or_url.get_absolute_url())
        else:
            return request.build_absolute_uri(obj_or_url)
    return ''


def _compose_tweet(text, url=None):
    TWITTER_MAX_NUMBER_OF_CHARACTERS = 140
    TWITTER_LINK_LENGTH = 23  # "A URL of any length will be altered to 23 characters, even if the link itself is less than 23 characters long.

    # Compute length of the tweet
    url_length = len(' ') + TWITTER_LINK_LENGTH if url else 0
    total_length = len(text) + url_length

    # Check that the text respects the max number of characters for a tweet
    if total_length > TWITTER_MAX_NUMBER_OF_CHARACTERS:
        text = text[:(TWITTER_MAX_NUMBER_OF_CHARACTERS - url_length - 1)] + "…"  # len("…") == 1
    return "%s %s" % (text, url) if url else text





@register.simple_tag(takes_context=True)
def post_to_twitter_url(context, text, obj_or_url=None):
    text = compile_text(context, text)
    request = context['request']
    url = _build_url(request, obj_or_url)
    tweet = _compose_tweet(text, url)
    context['tweet_url'] = TWITTER_ENDPOINT % urlencode(tweet)
    return context


@register.inclusion_tag('django_social_share/templatetags/post_to_twitter.html', takes_context=True)
def post_to_twitter(context, text, obj_or_url=None, link_text='Post to Twitter'):
    context = post_to_twitter_url(context, text, obj_or_url)
    request = context['request']
    url = _build_url(request, obj_or_url)
    tweet = _compose_tweet(text, url)
    context['link_text'] = link_text
    context['full_text'] = tweet
    return context


@register.simple_tag(takes_context=True)
def post_to_facebook_url(context, obj_or_url=None):
    request = context['request']
    url = _build_url(request, obj_or_url)
    context['facebook_url'] = FACEBOOK_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('django_social_share/templatetags/post_to_facebook.html', takes_context=True)
def post_to_facebook(context, obj_or_url=None, link_text='Post to Facebook'):
    context = post_to_facebook_url(context, obj_or_url)
    context['link_text'] = link_text
    return context