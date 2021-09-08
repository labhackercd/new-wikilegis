/*global $ events absolutePosition setCookie */

var ContextualToolbarView = function () { };

ContextualToolbarView.prototype.initEvents = function (editor) {
  this.editor = editor;

  this.contextualToolbar = $('.js-contextualToolbar');
  this.contextualToolbarWrapper = $('.js-contextualToolbarErrorAnimationWrapper');
  this.arrow = $('.js-contextualToolbar .js-contextualToolbarArrow');
  this.openContextualToolbarButton = $('.js-openContextualToolbar');
  this.typeList = $('.js-contextualToolbar .js-typeList');
  this.excerptTypes = $('.js-contextualToolbar .js-excerptType');
  this.cookieName = 'modifyExcerptTip';

  this.subscribers();
  this.publishers();
};

ContextualToolbarView.prototype.subscribers = function () {
  var self = this;

  self.editor.addEventListener('contexto', function (e) {
    self.showAllowedExcerptTypes(e.detail.permissoes);
    if (self.editor.ctrlArticulacao.contexto !== undefined) { // If the page has just been loaded, returns undefined
      self.showOpenToolbarButton();
    }
  });

  events.blurEditor.subscribe(function () {
    events.closeContextualToolbar.publish();
    self.hideOpenToolbarButton();
  });

  events.focusEditor.subscribe(function () {
    events.closeContextualToolbar.publish();

    if (self.editor.ctrlArticulacao.contexto !== undefined) { // If the page has just been loaded, returns undefined
      self.showOpenToolbarButton();
    }
  });

  events.openContextualToolbar.subscribe(function () {
    self.show();
  });

  events.closeContextualToolbar.subscribe(function () {
    self.hide();
  });

  events.showModifyExcerptTip.subscribe(function () {
    self.forceShowModifyExcerptTip();
  });
};

ContextualToolbarView.prototype.publishers = function () {
  var self = this;

  self.excerptTypes.on('click', function (e) {
    var target = $(e.target);
    self.updateExcerptType(target.data('excerptType'));
  });

  self.excerptTypes.on('focus', function (e) {
    var target = e.target;
    self.updateEditorTabindex(target);
  });

  self.excerptTypes.on('keydown', function (event) {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    var target = $(event.target);
    var parent = target.closest('.js-typeList');

    if (keycode == '27' || keycode == '38' || keycode == '40') {
      // Esc, Up arrow, Down arrow
      events.closeContextualToolbar.publish();
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
    } else if (keycode == '84') { self.activateShortcut('titulo'); } // "T" Key
    else if (keycode == '67') { self.activateShortcut('capitulo'); } // "C" Key
    else if (keycode == '83') { self.activateShortcut('secao'); } // "S" Key
    else if (keycode == '85') { self.activateShortcut('subsecao'); } // "U" Key
    else if (keycode == '65') { self.activateShortcut('artigo'); } // "A" Key
    else if (keycode == '80') { self.activateShortcut('paragrafo'); } // "P" Key
    else if (keycode == '73') { self.activateShortcut('inciso'); } // "I" Key
    else if (keycode == '76') { self.activateShortcut('alinea'); } // "L" Key
    else if (keycode == '69') { self.activateShortcut('item'); } // "E" Key
    else if (keycode == '79') { self.activateShortcut('continuacao'); } // "O" Key
  });

  self.openContextualToolbarButton.on('click', function () {
    events.blurEditor.publish();
    events.openContextualToolbar.publish();
  });
};

ContextualToolbarView.prototype.activateShortcut = function (excerptType) {
  var self = this;
  if (self.editor.ctrlArticulacao.contexto.permissoes[excerptType]) {
    self.editor.ctrlArticulacao.alterarTipoDispositivoSelecionado(excerptType);
    self.editor.focus();
    event.preventDefault();
  } else {
    self.contextualToolbarWrapper.addClass('-error').one('animationend', function () {
      self.contextualToolbarWrapper.removeClass('-error');
    });
  }
};

ContextualToolbarView.prototype.updateEditorTabindex = function (excerptType) {
  var self = this;
  var typeList = $(excerptType).closest('.js-typeList');
  var last = typeList.find('.js-excerptType:not(._hidden)').last()[0];

  if (last == excerptType) {
    $(self.editor).attr('tabindex', 3);
  } else {
    $(self.editor).attr('tabindex', 1);
  }
};

ContextualToolbarView.prototype.showAllowedExcerptTypes = function (permissions) {
  var self = this;
  self.excerptTypes.addClass('_hidden');

  $.each(permissions, function (excerptType, hasPermission) {
    if (hasPermission) {
      self.excerptTypes.closest('[data-excerpt-type="' + excerptType + '"]').removeClass('_hidden');
    }
  });
};

ContextualToolbarView.prototype.hide = function () {
  this.contextualToolbar.addClass('_hidden');
};

ContextualToolbarView.prototype.show = function () {
  this.contextualToolbar.removeClass('_hidden');
  this.updateToolbarPosition(self.editor.ctrlArticulacao.contexto.cursor.elemento);
  this.openContextualToolbarButton.removeClass('-tip'); // Remove -tip class if 'modifyExcerptTip' cookie was set
};

ContextualToolbarView.prototype.updateExcerptType = function (excerptType) {
  this.editor.ctrlArticulacao.alterarTipoDispositivoSelecionado(excerptType);
  this.editor.focus();
};

ContextualToolbarView.prototype.updateToolbarPosition = function (anchorElement) {
  var anchorPosition = absolutePosition(anchorElement);
  var toolbarOuterHeight = this.contextualToolbar.outerHeight(true);
  var toolbarOuterWidth = this.contextualToolbar.outerWidth(true);
  var editorBBox = this.editor.getBoundingClientRect();
  var arrowWidth = this.arrow.outerWidth(true);
  var beforeWidth = parseInt(window.getComputedStyle(anchorElement, '::before').width);
  var beforeMargin = (parseInt(window.getComputedStyle(anchorElement, '::before').marginLeft)) * 2;

  this.contextualToolbar.css('top', anchorPosition.top - toolbarOuterHeight);

  // If the contextual toolbar is outside the editor, align to the left
  if (((editorBBox.left + ((beforeWidth + beforeMargin) / 2)) - (toolbarOuterWidth / 2)) - editorBBox.left < 0) {

    this.contextualToolbar.css('left', editorBBox.left);
    this.arrow.css('left', (beforeWidth / 2) - (arrowWidth / 2));

    // Else, align to center
  } else {

    this.contextualToolbar.css('left', (editorBBox.left + ((beforeWidth + beforeMargin) / 2)) - (toolbarOuterWidth / 2));
    this.arrow.css('left', (toolbarOuterWidth / 2) - (arrowWidth / 2));
  }

  // XXX 
  // We should define a better positioning behaviour, and specify how to position it whenever the excerpt type 
  // is "citacao", since this type won't render a ::before, which we depend on for positioning.

};

ContextualToolbarView.prototype.showOpenToolbarButton = function () {
  var self = this;
  var button = this.openContextualToolbarButton;

  if (self.editor.ctrlArticulacao.contexto.cursor.elemento == self.editor) { // Sometimes the context is the editor itself. We don't show the button here.
    setTimeout(function () {
      self.hideOpenToolbarButton();
    }, 1);

  } else {

    button.removeClass('-show');

    this.updateOpenToolbarButtonPosition(self.editor.ctrlArticulacao.contexto.cursor.elemento);

    // Small delay in order to remove and then add modifier class and trigger its animation
    setTimeout(function () {
      button.addClass('-show');
    }, 1);
  }
};

ContextualToolbarView.prototype.hideOpenToolbarButton = function () {
  this.openContextualToolbarButton.removeClass('-show');
};

ContextualToolbarView.prototype.updateOpenToolbarButtonPosition = function (anchorElement) {
  var anchorPosition = absolutePosition(anchorElement);
  var editorBBox = this.editor.getBoundingClientRect();
  var beforeHeight = parseInt(window.getComputedStyle(anchorElement, '::before').height);
  var buttonOuterWidth = this.openContextualToolbarButton.outerWidth(true);
  var buttonOuterHeight = this.openContextualToolbarButton.outerHeight(true);

  if ($('.js-body').children('.edem-content-wrapper').length > 0) {
    this.openContextualToolbarButton.css('top', anchorPosition.top - ((buttonOuterHeight - beforeHeight) / 2) - 32);
  } else {
    this.openContextualToolbarButton.css('top', anchorPosition.top - ((buttonOuterHeight - beforeHeight) / 2));
  }

  this.openContextualToolbarButton.css('left', editorBBox.left - buttonOuterWidth);
};

ContextualToolbarView.prototype.forceShowModifyExcerptTip = function () {
  var button = this.openContextualToolbarButton;
  setCookie(this.cookieName, true);

  setTimeout(function () {
    button.addClass('-tip');
  }, 1000);
};