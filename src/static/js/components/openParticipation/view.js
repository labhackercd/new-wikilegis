/*global $ Urls */

var AutocompleteInputView = function() {};

AutocompleteInputView.prototype.initEvents = function() {
  this.inputNameElement = $('.js-name');
  this.themeElement = $('.js-theme');
  this.initAutocomplete();
  this.initAddNotUser();
  this.setThemes();
};

AutocompleteInputView.prototype.initAddNotUser= function () {
  self = this;

  self.inputNameElement.keypress(function (e) {
    if (e.which == 13) {
      var email = self.inputNameElement.val();
      if (self.validateEmail(email)) {
        $("<div>").text(email)
          .addClass('js-email')
          .attr('data-email', email)
          .prependTo("#log");
        $("#log").scrollTop(0);
      }
      return false;
    }
  });
};

AutocompleteInputView.prototype.setThemes= function () {
  self = this;

  self.themeElement.on("click", function(e) {
    var currentValue = localStorage.getItem('theme');
    var key = 'theme';
    var value = $(e.target).data('themeId').toString();
    if (currentValue) {
      var currentArray = currentValue.split(',');
      var i = currentArray.indexOf(value);
      if (i < 0) {
        currentArray = currentArray.concat(value);
        localStorage.setItem(key, currentArray);
        self.inputNameElement.focus();
      } else {
        currentArray.splice(i, 1);
        if (currentArray.length > 0) {
          localStorage.setItem(key, currentArray);
          self.inputNameElement.focus();
        } else {
          localStorage.removeItem(key);
        }
      }
    } else {
      localStorage.setItem(key, value);
      self.inputNameElement.focus();
    }
  });

  $(window).on("unload", function() {
    localStorage.clear();
  });
};

AutocompleteInputView.prototype.initAutocomplete= function () {
  var self = this;

  self.inputNameElement.autocomplete({
    source: function(request, response) {
      var theme = undefined;
      if (localStorage.getItem('theme')) {
        theme = localStorage.getItem('theme').split(',');
      }
      $.ajax({
        url: Urls.autocomplete(),
        dataType: "json",
        traditional: true,
        data: {
          name: request.term,
          theme: theme
        },
        success: function(data) {
          response(data);
        }
      });
    },
    minLength: 0,
    select: function(event, ui) {
      $("<div>").text(ui.item.first_name)
        .addClass('js-user')
        .attr('data-user-id', ui.item.id)
        .prependTo("#log");
      $("#log").scrollTop(0);
    }
  })
  .bind('focus', function(){ $(this).autocomplete("search");})
  .data("ui-autocomplete")._renderItem = self.listItem;
};

AutocompleteInputView.prototype.listItem = function (ul, item) {
  return $("<li>").append("<a>" + item.first_name + "</a>").appendTo(ul);
};

AutocompleteInputView.prototype.validateEmail = function (email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
};