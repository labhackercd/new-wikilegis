/*global $ events */

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
};

ContextualToolbarView.prototype.publishers = function() {
  var self = this;

  self.excerptTypes.on('click', function(e) {
    var target = $(e.target);
    self.updateExcerptType(target.data('excerptType'));
  });
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

ContextualToolbarView.prototype.updateExcerptType = function(excerptType) {
  this.editor.ctrlArticulacao.alterarTipoDispositivoSelecionado(excerptType);
  $('.js-textEditor')[0].focus()
};