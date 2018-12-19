/*global $ Urls */

var ThemeAutocomplete = function() {};

ThemeAutocomplete.prototype.initEvents = function() {
  this.themeAutocompleteElement = $('.js-themeAutocomplete');
  this.selectedThemesElement = $('.js-themeAutocomplete .js-themes');
  this.inputElement = $('.js-themeAutocomplete .js-input');
  this.tagsElement = $('.js-themeAutocomplete .js-tags');

  this.publishers();
};

ThemeAutocomplete.prototype.publishers = function() {
  var self = this;

  self.tagsElement.on('click', '.js-tag', function(e) {
    self.removeTag($(e.target));
  });

  var autocomplete = self.inputElement.autocomplete({
    source: function(request, response) {
      $.ajax({
        url: Urls.theme_list() + '?slug__icontains=' + request.term,
        dataType: 'json',
        success: function(data) {
          response(data.results);
        }
      });
    },
    appendTo: '.js-themeAutocomplete',
    minLength: 0,
    select: function(event, ui) {
      self.addTheme(ui.item);
    }
  });

  autocomplete.autocomplete('instance')._renderItem = function(ul, item) {
    var li = $('<li>')
      .attr('data-value', item.slug)
      .removeClass()
      .addClass('theme-tag')
      .text(item.name);

    $('<span>').addClass('dot')
      .css('background-color', item.color)
      .prependTo(li);

    return li.appendTo(ul);
  };

  autocomplete.autocomplete('instance')._renderMenu = function(ul, items) {
    ul.addClass('autocomplete-list');

    var autocomplete = this;
    $.each( items, function( index, item ) {
      autocomplete._renderItemData( ul, item );
    });
  };
};

ThemeAutocomplete.prototype.addTag = function(theme) {
  var li = $('<li class="theme-tag js-tag">')
    .text(theme.name);

  $('<span>').addClass('dot')
    .css('background-color', theme.color)
    .prependTo(li);

  this.tagsElement.append(li);
};

ThemeAutocomplete.prototype.removeTag = function(tagElement) {
  var themeId = tagElement.data('themeId');
  var themeInput = $('input[name="themes"][value="' + themeId + '"]');
  themeInput.remove();
  tagElement.remove();
};

ThemeAutocomplete.prototype.addTheme = function(theme) {
  var themeInput = $('input[name="themes"][value="' + theme.id + '"]');
  if (themeInput.length === 0) {
    var input = $('<input type="hidden" name="themes" value="' + theme.id + '">');
    this.themeAutocompleteElement.append(input);
    this.addTag(theme);
  }
};
