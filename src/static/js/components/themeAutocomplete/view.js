/*global $ Urls slug */

var ThemeAutocompleteView = function() {};

ThemeAutocompleteView.prototype.initEvents = function() {
  this.themeAutocompleteElement = $('.js-themeAutocomplete');
  this.selectedThemesElement = $('.js-themeAutocomplete .js-themes');
  this.inputElement = $('.js-themeAutocomplete .js-input');
  this.tagsElement = $('.js-themeAutocomplete .js-tags');
  this.titleElement = $('.js-themeAutocomplete .js-title');

  this.publishers();
};

ThemeAutocompleteView.prototype.publishers = function() {
  var self = this;

  self.tagsElement.on('click', '.js-tag', function(e) {
    self.removeTag($(e.target));
  });

  var autocomplete = self.inputElement.autocomplete({
    source: function(request, response) {
      var query = slug(request.term);
      $.ajax({
        url: Urls.theme_list() + '?slug__icontains=' + query,
        dataType: 'json',
        success: function(data) {
          response(data.results);
        }
      });
    },
    focus: function(event, ui) {
      $('.js-autocompleteList .js-themeTag').removeClass('-active');
      $('.js-autocompleteList .js-themeTag[data-value="' + ui.item.slug + '"]')
        .addClass('-active');
    },
    appendTo: '.js-themeAutocomplete',
    messages: {
      noResults: '',
      results: function() {}
    },
    minLength: 0,
    autoFocus: true,
    select: function(event, ui) {
      self.addTheme(ui.item);
    }
  });

  self.inputElement.on('click', function() {
    $(this).autocomplete('search', '');
  });

  autocomplete.autocomplete('instance')._renderItem = function(ul, item) {
    var li = $('<li>')
      .attr('data-value', item.slug)
      .removeClass()
      .addClass('theme-tag')
      .addClass('js-themeTag')
      .text(item.name);

    if (self.tagsElement.find(`.js-tag[data-theme-id="${item.id}"]`).length) {
      li.addClass('-choosed');
    }

    $('<span>').addClass('dot')
      .css('background-color', item.color)
      .prependTo(li);

    return li.appendTo(ul);
  };

  autocomplete.autocomplete('instance')._renderMenu = function(ul, items) {
    ul.addClass('autocomplete-list js-autocompleteList');

    var autocomplete = this;
    $.each( items, function( index, item ) {
      autocomplete._renderItemData( ul, item );
    });
  };
};

ThemeAutocompleteView.prototype.addTag = function(theme) {
  var li = $('<li class="theme-tag js-tag">')
    .addClass('-selected')
    .attr('data-theme-id', theme.id)
    .text(theme.name);

  $('<span>').addClass('dot')
    .css('background-color', theme.color)
    .prependTo(li);

  this.tagsElement.append(li);
  this.toggleTitle();
};

ThemeAutocompleteView.prototype.removeTag = function(tagElement) {
  var themeId = tagElement.data('themeId');
  var themeInput = $('input[name="themes"][value="' + themeId + '"]');
  themeInput.remove();
  tagElement.remove();
  this.toggleTitle();
};

ThemeAutocompleteView.prototype.addTheme = function(theme) {
  var themeInput = $('input[name="themes"][value="' + theme.id + '"]');
  if (themeInput.length === 0) {
    var input = $('<input type="hidden" name="themes" value="' + theme.id + '">');
    this.themeAutocompleteElement.append(input);
    this.addTag(theme);
  }
};

ThemeAutocompleteView.prototype.toggleTitle = function() {
  if ($('input[name="themes"]').length > 0) {
    this.titleElement.parent().removeClass('_hidden');
  } else {
    this.titleElement.parent().addClass('_hidden');
  }
};
