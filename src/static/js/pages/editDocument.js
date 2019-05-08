/*global $ silegismgEditorArticulacaoController ContextualToolbarView DocumentEditorView ValidationModalView InfoMessageView CongressmanAutocompleteView */

var editor = $('.js-textEditor')[0];
silegismgEditorArticulacaoController(editor, {
  rotulo: {
    separadorArtigo: '',
    separadorArtigoSemOrdinal: '.',
    separadorParagrafo: '',
    separadorParagrafoSemOrdinal: '.'
  }
});

var contextualToolbarView = new ContextualToolbarView();
contextualToolbarView.initEvents(editor);

var documentEditorView = new DocumentEditorView();
documentEditorView.initEvents(editor, contextualToolbarView);

var validationModalView = new ValidationModalView();
validationModalView.initEvents();

var infoMessageView = new InfoMessageView();
infoMessageView.initEvents();

var congressmanAutocompleteView = new CongressmanAutocompleteView();
congressmanAutocompleteView.initEvents();
