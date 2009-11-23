from django import forms
from kanboard import models


class AddCard(forms.ModelForm):
    def __init__(self, user, board, *args, **kwargs):
        super(AddCard, self).__init__(*args, **kwargs)
        self.user = user
        self.board = board

    class Meta:
        model = models.Card
        fields = ('title',)

    def save(self, commit=True, *args, **kwargs):
        card = super(AddCard, self).save(commit=False, *args, **kwargs)
        card.created_by = self.user
        card.board = self.board
        phases = self.board.phases
        if self.data.get('pin'):
            card.phase = phases.filter(status=models.Phase.PROGRESS)[0]
        else:
            card.phase = phases.filter(status=models.Phase.UPCOMING)[0]
        if commit:
            card.save()
        return card
