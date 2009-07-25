# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from kanboard.models import Board

def board(request, slug, template_name='kanboard/board.html'):
    board = get_object_or_404(Board, slug=slug)
    return render_to_response(template_name,
                              dict(board=board),
                              context_instance=RequestContext(request))
