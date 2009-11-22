import re
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from kanboard import models

def _debug(board, message):
    print "DEBUG (%s): %s" % (board.slug, message)

def board(request, board_slug, template_name='kanboard/board.html'):
    board = get_object_or_404(models.Board, slug=board_slug)
    return render_to_response(template_name,
                              dict(board=board),
                              context_instance=RequestContext(request))

PHASE_RE = re.compile('^phase-([\d]+)$')
CARD_RE = re.compile('^card-([\d]+)$')

def update(request, board_slug):
    updates = []
    try:
        board = get_object_or_404(models.Board, slug=board_slug)
        for phase_name, card_names in request.POST.lists():
            cards = []
            phase_match = PHASE_RE.match(phase_name)
            if not phase_match:
                raise Exception("Malformed phase_name: <%s>" % phase_name)
            phase = get_object_or_404(models.Phase, board=board,
                                      pk=int(phase_match.group(1)))
            for card_name in card_names:
                card_match = CARD_RE.match(card_name)
                if not card_match:
                    raise Exception("Malformed card_name: <%s>" % card_name)
                card = get_object_or_404(models.Card, phase__board=board,
                                         pk=int(card_match.group(1)))
                cards.append(card)
            updates.append((phase, cards))
            updates.sort(cmp=lambda x,y: cmp(x[0].order, y[0].order))

            for phase, cards in updates:
                for card in cards:
                    if card.phase != phase:
                        card.change_phase(phase)
            for phase, cards in updates:
                for i, card in enumerate(cards):
                    card.order = i
                    card.save()

    except Exception, e:
        print "Exception: %s, %r" % (e, e)
        raise

    return HttpResponse() # nothing exciting...

