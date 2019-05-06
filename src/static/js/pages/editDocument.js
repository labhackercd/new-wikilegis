var editor = $('.js-textEditor')[0];silegismgEditorArticulacaoController(editor, {
  rotulo: {
    separadorArtigo: '',
    separadorArtigoSemOrdinal: '.',
    separadorParagrafo: '',
    separadorParagrafoSemOrdinal: '.'
  }
});

var documentEditorView = new DocumentEditorView();
documentEditorView.initEvents(editor);

var contextualToolbarView = new ContextualToolbarView();
contextualToolbarView.initEvents(editor);