/*global $ events autosize */

var DocumentEditorView = function() {};

DocumentEditorView.prototype.initEvents = function(editor, toolbarView) {
  this.editor = editor;
  this.toolbarView = toolbarView;
  this.typing = null;

  this.subscribers();
  this.publishers();
};

DocumentEditorView.prototype.subscribers = function() {
  var self = this;

  events.documentTitleEditionEnd.subscribe(function(newTitle) {
    self.endEdition('title', newTitle);
  });

  events.closeContextualToolbox.subscribe(function() {
    self.removeBlur();
  });

  events.documentTextLoaded.subscribe(function(data) {
    self.editor.innerHTML = data.html;
  });
};

DocumentEditorView.prototype.publishers = function() {
  var self = this;

  $(self.editor).on('focus', function() {
    events.closeContextualToolbox.publish();
    $(self.editor).attr('tabindex', 1);
  });

  $(self.editor).on('keydown', function(event) {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == '9') {
      self.toolbarView.show();
      self.highligthCurrentExcerpt();
    }
  });

  $(self.editor).on('keyup', function(event) {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode < 37 || keycode > 40) {
      events.documentChanged.publish();
      clearTimeout(self.typing);
      self.typing = setTimeout(function() {
        events.autoSaveDocument.publish();
      }, 1500);
    }
  })
};

DocumentEditorView.prototype.highligthCurrentExcerpt = function() {
  $(this.editor).addClass('-blur');
  $(this.editor.ctrlArticulacao.contexto.cursor.elemento).addClass('-highlight');
};

DocumentEditorView.prototype.removeBlur = function() {
  $(this.editor).removeClass('-blur');
  $(this.editor).find('p').removeClass('-highlight');
};