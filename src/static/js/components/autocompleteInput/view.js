/*global $ Urls */

var AutocompleteInputView = function() {};

AutocompleteInputView.prototype.initEvents = function() {
  this.inputNameElement = $('.js-name');
  this.initAutocomplete();
  this.initAddNotUser();
};

AutocompleteInputView.prototype.initAddNotUser= function () {
  self = this;

  self.inputNameElement.keypress(function (e) {
    if (e.which == 13) {
      var email = self.inputNameElement.val();
      if (self.validateEmail(email)) {
        self.log("Selecionado: " + email)
      }
      return false;
    }
  });
};

AutocompleteInputView.prototype.initAutocomplete= function () {
  var self = this;

  self.inputNameElement.autocomplete({
    source: function(request, response) {
      $.ajax({
        url: Urls.autocomplete(),
        dataType: "json",
        data: {
          name: request.term
        },
        success: function(data) {
          response(data);
        }
      });
    },
    minLength: 2,
    select: function(event, ui) {
      self.log("Selecionado: " + ui.item.first_name);
    }
  })
  .data("ui-autocomplete")._renderItem = self.listItem;
};

AutocompleteInputView.prototype.log = function (message) {
  $("<div>").text(message).prependTo("#log");
  $("#log").scrollTop(0);
};

AutocompleteInputView.prototype.listItem = function (ul, item) {
  return $("<li>").append("<a>" + item.first_name + "</a>").appendTo(ul);
};

AutocompleteInputView.prototype.validateEmail = function (email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
};