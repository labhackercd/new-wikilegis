/*global $ events */

var ContextualToolbarView = function() {};

ContextualToolbarView.prototype.initEvents = function(editorCtrl) {
  this.editorCtrl = editorCtrl;

  this.contextualToolbar = $('.js-contextualToolbar');
  this.typeList = $('.js-contextualToolbar .js-typeList');
  this.excerptTypes = $('.js-contextualToolbar .js-excerptType');

  this.subscribers();
  this.publishers();
};

ContextualToolbarView.prototype.subscribers = function() {
  var self = this;

  self.editorCtrl._elemento.addEventListener('contexto', function (e) {
    self.showAllowedExcerptTypes(e.detail.permissoes);
  });
};

ContextualToolbarView.prototype.publishers = function() {
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