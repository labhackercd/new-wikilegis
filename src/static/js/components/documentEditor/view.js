/*global $ events */

var DocumentEditorView = function() {};

DocumentEditorView.prototype.initEvents = function(editorCtrl) {
  this.editorCtrl = editorCtrl;
  this.documentTitle = $('.js-documentEditor .js-documentHeader .js-title');
  this.documentTitleInput = $('.js-documentEditor .js-documentHeader .js-titleInput');
  this.documentDescription = $('.js-documentEditor .js-documentHeader .js-description');
  this.documentDescriptionInput = $('.js-documentEditor .js-documentHeader .js-descriptionInput');

  autosize(this.documentTitleInput);
  autosize(this.documentDescriptionInput);

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
  this.documentTitleInput.val(this.documentTitle.text());
  this.documentTitleInput.removeClass('_hidden');;
  this.documentTitleInput.focus();
  this.documentTitleInput.select();
  autosize.update(this.documentTitleInput);
};

DocumentEditorView.prototype.startDescriptionEdition = function() {
  this.documentDescription.addClass('_hidden');
  this.documentDescriptionInput.val(this.documentDescription.text());
  this.documentDescriptionInput.removeClass('_hidden');
  this.documentDescriptionInput.focus();
  this.documentDescriptionInput.select();
  autosize.update(this.documentDescriptionInput);
};

DocumentEditorView.prototype.endTitleEdition = function(newTitle) {
  this.documentTitle.text(newTitle);
  this.documentTitle.removeClass('_hidden');
  this.documentTitleInput.addClass('_hidden');
};

DocumentEditorView.prototype.endDescriptionEdition = function(newDescription) {
  this.documentDescription.text(newDescription);
  this.documentDescription.removeClass('_hidden');
  this.documentDescriptionInput.addClass('_hidden');
};
