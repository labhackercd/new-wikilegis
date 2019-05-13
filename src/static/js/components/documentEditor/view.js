/*global $ events autosize */

var DocumentEditorView = function() {};

DocumentEditorView.prototype.initEvents = function(editor, toolbarView) {
  this.editor = editor;
  this.toolbarView = toolbarView;
  this.documentTitle = $('.js-documentEditor .js-documentHeader .js-title');
  this.documentTitleInput = $('.js-documentEditor .js-documentHeader .js-titleInput');
  this.documentDescription = $('.js-documentEditor .js-documentHeader .js-description');
  this.documentDescriptionInput = $('.js-documentEditor .js-documentHeader .js-descriptionInput');
  this.documentHeaderInputs = $('.js-documentEditor .js-documentHeader .js-input');

  this.infos = {
    'title': {
      'input': this.documentTitleInput,
      'text': this.documentTitle
    },
    'description': {
      'input': this.documentDescriptionInput,
      'text': this.documentDescription
    }
  };

  autosize(this.documentTitleInput);
  autosize(this.documentDescriptionInput);

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

  events.documentTextLoaded.subscribe(function(html) {
    self.editor.innerHTML = html;
  });
};

DocumentEditorView.prototype.publishers = function() {
  var self = this;
  self.documentTitle.on('click', function() {
    self.startEdition('title');
  });

  self.documentDescription.on('click', function() {
    self.startEdition('description');
  });

  self.documentTitleInput.on('focusout', function() {
    events.documentTitleEditionEnd.publish(this.value);
  });

  self.documentDescriptionInput.on('focusout', function() {
    self.endEdition('description', this.value);
  });

  self.documentHeaderInputs.on('keypress', function(event) {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
      self.documentHeaderInputs.focusout();
    }
  });

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
};

DocumentEditorView.prototype.startEdition = function(info) {
  this.infos[info]['text'].addClass('_hidden');
  this.infos[info]['input'].val(this.infos[info]['text'].text());
  this.infos[info]['input'].removeClass('_hidden');
  this.infos[info]['input'].focus();
  this.infos[info]['input'].select();
  autosize.update(this.infos[info]['input']);
};

DocumentEditorView.prototype.endEdition = function(info, newText) {
  if (newText != '') {
    this.infos[info]['text'].text(newText);
  } else {
    this.infos[info]['input'].val(this.infos[info]['text'].text());
  }
  this.infos[info]['text'].removeClass('_hidden');
  this.infos[info]['input'].addClass('_hidden');
};

DocumentEditorView.prototype.highligthCurrentExcerpt = function() {
  $(this.editor).addClass('-blur');
  $(this.editor.ctrlArticulacao.contexto.cursor.elemento).addClass('-highlight');
};

DocumentEditorView.prototype.removeBlur = function() {
  $(this.editor).removeClass('-blur');
  $(this.editor).find('p').removeClass('-highlight');
};