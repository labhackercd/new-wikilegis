/*global $ events */

var ToolBarView = function() {};

ToolBarView.prototype.initEvents = function(documentEditorView) {
  this.documentEditorView = documentEditorView;
  this.toolBarElement = $('.js-toolBar');
  this.saveButton = $('.js-toolBar .js-saveButton');
  this.videoHelperButton = $('.js-toolBar .js-videoHelper');
  this.subscribers();
  this.publishers();
};

ToolBarView.prototype.subscribers = function() {
  var self = this;

  events.autoSaveDocument.subscribe(function() {
    self.saveDocument(true);
  });
};

ToolBarView.prototype.publishers = function() {
  var self = this;

  self.videoHelperButton.on('click', function() {
    console.log("pegou o clique");
  });

  self.saveButton.on('click', function() {
    events.openModal.publish();
    events.openSaveModal.publish();
  });
};

ToolBarView.prototype.saveDocument = function(autoSave) {
  var html = '';
  if (this.documentEditorView.editor.innerText.length >= 2) {
    html = this.documentEditorView.editor.innerHTML;
  }

  var data = {
    'pk': $('.js-documentEditor').data('documentId'),
    'html': html,
    'autoSave': autoSave
  };
  events.saveDocument.publish(data);
};