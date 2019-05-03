/*global $ events */

var DocumentEditorView = function() {};

DocumentEditorView.prototype.initEvents = function(editorCtrl) {
  this.editorCtrl = editorCtrl;
  this.documentTitle = $('.js-documentEditor .js-documentHeader .js-title');
  this.documentTitleInput = $('.js-documentEditor .js-documentHeader .js-titleInput');
  this.documentDescription = $('.js-documentEditor .js-documentHeader .js-description');
  this.documentDescriptionInput = $('.js-documentEditor .js-documentHeader .js-descriptionInput');

  this.subscribers();
  this.publishers();
};

DocumentEditorView.prototype.subscribers = function() {
  var self = this;

  events.documentTitleEditionEnd.subscribe(function(newTitle) {
    self.endTitleEdition(newTitle);
  });
};

DocumentEditorView.prototype.publishers = function() {
  var self = this;
  self.documentTitle.on('click', function() {
    self.startTitleEdition();
  });

  self.documentDescription.on('click', function() {
    self.startDescriptionEdition();
  });

  self.documentTitleInput.on('focusout', function() {
    events.documentTitleEditionEnd.publish(this.value);
  });

  self.documentDescriptionInput.on('focusout', function() {
    self.endDescriptionEdition(this.value);
  });
};

DocumentEditorView.prototype.startTitleEdition = function() {
  this.documentTitle.addClass('_hidden');
  this.documentTitleInput.attr('type', 'text');
  this.documentTitleInput.focus();
  this.documentTitleInput.select();
};

DocumentEditorView.prototype.startDescriptionEdition = function() {
  this.documentDescription.addClass('_hidden');
  this.documentDescriptionInput.attr('type', 'text');
  this.documentDescriptionInput.focus();
  this.documentDescriptionInput.select();
};

DocumentEditorView.prototype.endTitleEdition = function(newTitle) {
  this.documentTitle.text(newTitle);
  this.documentTitle.removeClass('_hidden');
  this.documentTitleInput.attr('type', 'hidden');
};

DocumentEditorView.prototype.endDescriptionEdition = function(newDescription) {
  this.documentDescription.text(newDescription);
  this.documentDescription.removeClass('_hidden');
  this.documentDescriptionInput.attr('type', 'hidden');
};