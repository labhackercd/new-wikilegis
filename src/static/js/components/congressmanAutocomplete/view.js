/*global $ */

var CongressmanAutocompleteView = function() {};

CongressmanAutocompleteView.prototype.initEvents = function() {
  this.inputElement = $('.js-congressman .js-inputAutocomplete');
  this.publishers();
};

CongressmanAutocompleteView.prototype.publishers = function() {
  var self = this;
  var apiUrl = $('.js-congressman').data('apiUrl');
  var legislature = $('.js-congressman').data('legislature');

  self.inputElement.autocomplete({
    source: function( request, response ) {
      $.ajax( {
        url: apiUrl + 'deputados',
        dataType: 'json',
        data: {
          idLegislatura: legislature,
          ordem: 'ASC',
          ordenarPor: 'nome',
          nome: request.term
        },
        success: function( data ) {
          response( data.dados );
        }
      } );
    },
    appendTo: '.js-congressman',
    messages: {
      noResults: '',
      results: function() {}
    },
    minLength: 2,
    create: function () {
      $(this).data('ui-autocomplete')._renderItem = function (ul, item) {
        return $('<li class="item">')
          .append('<img class="avatar" src=' + item.urlFoto + ' alt="img" />')
          .append('<div class="name">' + item.nome + '( ' + item.siglaPartido + ' )' + '</div>')
          .appendTo(ul);
      };},
    select: function( event, ui ) {
      $('.js-inputAutocomplete').val(ui.item.nome + ' ( ' + ui.item.siglaPartido + ' ) ');
      var input = $('<input type="hidden" name="congressman-id" class="js-congressmanId" value="' + ui.item.id + '">');
      $('.js-congressman').append(input);
      return false;
    }
  });
};
