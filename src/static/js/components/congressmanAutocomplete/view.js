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

  var autocomplete = self.inputElement.autocomplete({
    source: function( request, response ) {
      $.ajax( {
        url: apiUrl + "deputados",
        dataType: "json",
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
    minLength: 2,
    create: function (event, ui) {
      $(this).data('ui-autocomplete')._renderItem = function (ul, item) {
      return $('<li>')
      .append("<img src=" + item.urlFoto + " alt='img' style='width: 50px; height: 50px;' />")
      .append("<a style='font-size: 16px; color: #000; position: absolute; margin: 5px;'>" + item.nome +
           '<span style="margin: 15px;">' + '( ' + item.siglaPartido + ' )' + "</a>")
      .appendTo(ul);
    };},
    select: function( event, ui ) {
      setInput(ui.item.nome + " ( " + ui.item.siglaPartido + " ) ");
      return false;
    }
  });
};

