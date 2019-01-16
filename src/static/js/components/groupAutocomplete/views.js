/*global $ Urls */

var GroupAutocompleteView = function() {};

GroupAutocompleteView.prototype.initEvents = function() {
  this.groupAutocompleteElement = $('.js-groupAutocomplete');
  this.selectedGroupsElement = $('.js-groupAutocomplete .js-themes');
  this.inputElement = $('.js-groupAutocomplete .js-input');
  this.groupsElement = $('.js-groupAutocomplete .js-groups');
  this.groupTitleElement = $('.js-groupAutocomplete .js-groupTitle');

  this.publishers();
};

GroupAutocompleteView.prototype.publishers = function() {
  var self = this;

  self.groupsElement.on('click', '.js-group', function(e) {
    self.removeGroup($(e.target));
  });

  var autocomplete = self.inputElement.autocomplete({
    source: function(request, response) {
      $.ajax({
        url: Urls.thematicgroup_list() + '?name__icontains=' + request.term,
        dataType: 'json',
        success: function(data) {
          response(data.results);
        }
      });
    },
    focus: function(event, ui) {
      $('.js-autocompleteList .js-groupTag').removeClass('-active');
      $('.js-autocompleteList .js-groupTag[data-value="' + ui.item.slug + '"]')
        .addClass('-active');
    },
    appendTo: '.js-groupAutocomplete',
    messages: {
      noResults: '',
      results: function() {}
    },
    minLength: 0,
    select: function(event, ui) {
      self.addGroupsInput(ui.item);
    }
  });

  autocomplete.autocomplete('instance')._renderItem = function(ul, item) {
    var li = $('<li>')
      .attr('data-value', item.slug)
      .removeClass()
      .addClass('theme-tag')
      .addClass('js-groupTag')
      .text(item.name);

    // $('<span>').addClass('dot')
    //   .css('background-color', 'crimson')
    //   .prependTo(li);

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

GroupAutocompleteView.prototype.addGroup = function(group) {
  var li = $('<li class="theme-tag js-group">')
    .addClass('-selected')
    .data('groupId', group.id)
    .text(group.name);

  // $('<span>').addClass('dot')
  //   .css('background-color', 'crimson')
  //   .prependTo(li);

  this.groupsElement.append(li);
  this.toggleTitle();
};

GroupAutocompleteView.prototype.removeGroup = function(groupElement) {
  var groupId = groupElement.data('groupId');
  var groupInput = $('input[name="groups"][value="' + groupId + '"]');
  groupInput.remove();
  groupElement.remove();
  this.toggleTitle();
};

GroupAutocompleteView.prototype.addGroupsInput = function(group) {
  var groupInput = $('input[name="groups"][value="' + group.id + '"]');
  if (groupInput.length === 0) {
    var input = $('<input type="hidden" name="groups" value="' + group.id + '">');
    this.groupAutocompleteElement.append(input);
    this.addGroup(group);
  }
};

GroupAutocompleteView.prototype.toggleTitle = function() {
  if ($('input[name="groups"]').length > 0) {
    this.groupTitleElement.removeClass('_hidden');
  } else {
    this.groupTitleElement.addClass('_hidden');
  }
};
