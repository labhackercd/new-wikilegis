/*global $ events */

var ToolBarView = function() {};

ToolBarView.prototype.initEvents = function(documentEditorView) {
  this.documentEditorView = documentEditorView;
  this.toolBarElement = $('.js-toolBar');
  this.saveButton = $('.js-toolBar .js-saveButton');

  this.subscribers();
  this.publishers();
};

ToolBarView.prototype.subscribers = function() {
};

ToolBarView.prototype.publishers = function() {
  var self = this;

  self.saveButton.on('click', function() {
    self.saveDocument();
  });
};

ToolBarView.prototype.saveDocument = function() {
  var html = ''
  if (this.documentEditorView.editor.innerText.length >= 2) {
    html = this.documentEditorView.editor.innerHTML;
  }

  var data = {
    'pk': $('.js-documentEditor').data('documentId'),
    'title': this.documentEditorView.documentTitleInput.val(),
    'description': this.documentEditorView.documentDescriptionInput.val(),
    'html': html
  }
  events.saveDocument.publish(data);
};