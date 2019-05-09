/*global $ silegismgEditorArticulacaoController ContextualToolbarView DocumentEditorView */

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
