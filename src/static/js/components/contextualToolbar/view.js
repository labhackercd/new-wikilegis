/*global $ events absolutePosition */

var ContextualToolbarView = function() {};

ContextualToolbarView.prototype.initEvents = function(editor) {
  this.editor = editor;

  this.contextualToolbar = $('.js-contextualToolbar');
  this.typeList = $('.js-contextualToolbar .js-typeList');
  this.excerptTypes = $('.js-contextualToolbar .js-excerptType');

  this.subscribers();
  this.publishers();
};

ContextualToolbarView.prototype.subscribers = function() {
  var self = this;

  self.editor.addEventListener('contexto', function (e) {
    self.showAllowedExcerptTypes(e.detail.permissoes);
  });

  events.closeContextualToolbox.subscribe(function() {
    self.hide();
  });
};

ContextualToolbarView.prototype.publishers = function() {
  var self = this;

  self.excerptTypes.on('click', function(e) {
    var target = $(e.target);
    self.updateExcerptType(target.data('excerptType'));
  });

  self.excerptTypes.on('focus', function(e) {
    var target = e.target;
    self.updateEditorTabindex(target);
  });

  self.excerptTypes.on('keydown', function(event) {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    var target = $(event.target);
    var parent = target.closest('.js-typeList');

    if (keycode == '27' || keycode == '38' || keycode == '40') {
      // Esc, Up arrow, Down arrow
      self.hide();
      self.editor.focus();
    } else if (keycode == '37') {
      // Left arrow
      var previous = target.prevAll(':not(._hidden)');

      if (previous.length > 0) {
        previous.first().focus();
      } else {
        parent.children(':not(._hidden)').last().focus();
      }
    } else if (keycode == '39') {
      // Rigth arrow
      var next = target.nextAll(':not(._hidden)');

      if (next.length > 0) {
        next.first().focus();
      } else {
        parent.children(':not(._hidden)').first().focus();
      }
    }
  });
};

ContextualToolbarView.prototype.updateEditorTabindex = function(excerptType) {
  var self = this;
  var typeList = $(excerptType).closest('.js-typeList');
  var last = typeList.find('.js-excerptType:not(._hidden)').last()[0];

  if (last == excerptType) {
    $(self.editor).attr('tabindex', 3);
  } else {
    $(self.editor).attr('tabindex', 1);
  }
};

ContextualToolbarView.prototype.showAllowedExcerptTypes = function(permissions) {
  var self = this;
  self.excerptTypes.addClass('_hidden');

  $.each(permissions, function(excerptType, hasPermission) {
    if (hasPermission) {
      self.excerptTypes.closest('[data-excerpt-type="' + excerptType + '"]').removeClass('_hidden');
    }
  });
};

ContextualToolbarView.prototype.hide = function() {
  this.contextualToolbar.addClass('_hidden');
};

ContextualToolbarView.prototype.show = function() {
  this.contextualToolbar.removeClass('_hidden');
  this.updateToolbarPosition(self.editor.ctrlArticulacao.contexto.cursor.elemento);
};

ContextualToolbarView.prototype.updateExcerptType = function(excerptType) {
  this.editor.ctrlArticulacao.alterarTipoDispositivoSelecionado(excerptType);
  this.editor.focus();
};

ContextualToolbarView.prototype.updateToolbarPosition = function(anchorElement) {
  var navbarHeight = $('.js-navbar').outerHeight();
  var anchorPosition = absolutePosition(anchorElement);
  var toolbarBBox = absolutePosition(this.contextualToolbar[0]);
  var editorBBox = this.editor.getBoundingClientRect();

  this.contextualToolbar.css('top', anchorPosition.top + anchorPosition.height - navbarHeight);
  this.contextualToolbar.css('left', editorBBox.left + (editorBBox.width / 2) - (toolbarBBox.width / 2));
};