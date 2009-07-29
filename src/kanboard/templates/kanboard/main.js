/*
    // Clean version
    $(function() {
      $('.sortable').sortable({connectWith: '.sortable'}).disableSelection();
    });
//*/
//*
    $(function() {
      var debug = function(mesg) {
        $('#messages').append('<li>' + mesg + '</li>');
      };
      $('.sortable').sortable({
        connectWith: '.sortable',
        stop: function(e, ui) {
          var sender = ui.sender ? ui.sender[0].id : "(none)";
          var item = ui.item[0].id;
          var target = e.target.id;
          debug('ui.sender=' + sender + ', item=' + item + ', target=' + target);
          var data = {};
          $('ul.phase').each(function() {
            data[this.id] = $.map($(this).find('li.card'), function(y) { return y.id})
          });
          // TODO:zjh - add error function to display debug info
          $.post('update/', data);
        }
      }).disableSelection();
    });
//*/

