# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from kanboard.models import Board

def _debug(board, message):
    print "DEBUG (%s): %s" % (board.slug, message)

def board(request, board_slug, template_name='kanboard/board.html'):
    board = get_object_or_404(Board, slug=board_slug)
    return render_to_response(template_name,
                              dict(board=board),
                              context_instance=RequestContext(request))

def update(request, board_slug):
    board = get_object_or_404(Board, slug=board_slug)
    _debug(board, "Got an update: %s" % request.POST)
    return HttpResponse() # nothing exciting…
