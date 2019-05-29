/*global $ events */

var DocumentEditorView = function() {};

DocumentEditorView.prototype.initEvents = function(editor, toolbarView) {
  this.editor = editor;
  this.toolbarView = toolbarView;
  this.typing = null;
  this.documentEditorElement = $('.js-documentEditor');
  this.closeDiffButton = $('.js-closeDiff');
  this.textEditorWrapper = $('.js-documentEditor .js-textEditorWrapper');
  this.mergelyWrapper = $('.js-mergelyWrapper');

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

  events.showDiff.subscribe(function(text1, text2) {
    self.documentEditorElement.addClass('-compare');
    self.textEditorWrapper.addClass('_hidden');
    self.closeDiffButton.addClass('-show');

    self.mergelyWrapper.append('<div id="mergely"></div>');

    $('#mergely').mergely({
      cmsettings: {
        readOnly: true,
        lineWrapping: true
      },
      wrap_lines: true,

      autoresize: true,
      ignorews: true,
      license: 'gpl',
      line_numbers: false,
      sidebar: false,

      editor_width: 'calc(50% - 25px)',
      editor_height: '100%',
      lhs: function(setValue) {
        setValue(text1.html);
      },
      rhs: function(setValue) {
        setValue(text2.html);
      },
      loaded: function() {
        setTimeout(function() {
          $('#mergely').mergely('resize');
        }, 300)
      },
    });
  });

  events.closeDiff.subscribe(function() {
    $('.js-documentEditor .js-documentDiff').remove();
    self.textEditorWrapper.removeClass('_hidden');
    self.documentEditorElement.removeClass('-compare');
    self.closeDiffButton.removeClass('-show');
    self.mergelyWrapper.html('');
  })
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
  });

  self.closeDiffButton.on('click', function() {
    events.closeDiff.publish();
  });
};

DocumentEditorView.prototype.highligthCurrentExcerpt = function() {
  $(this.editor).addClass('-blur');
  $(this.editor.ctrlArticulacao.contexto.cursor.elemento).addClass('-highlight');
};

DocumentEditorView.prototype.removeBlur = function() {
  $(this.editor).removeClass('-blur');
  $(this.editor).find('p').removeClass('-highlight');
};

DocumentEditorView.prototype.createDiffDocument = function(data) {
  var versionName = data.versionName;
  if (data.autoSave) {
    versionName = 'Versão Atual';
  }
  var article = `
  <article class="js-textEditorWrapper js-documentDiff">
    <header class="-editable js-documentHeader">
      <h1 class="js-title">${versionName}</h1>
      <p class="description js-description">${data.date}</p>
      <hr>
    </header>

    <div tabindex="1" class="js-textEditor">
      ${data.html}
    </div>
  </article>
  `

  this.documentEditorElement.append($(article));
};