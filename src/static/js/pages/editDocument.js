var editorCtrl = silegismgEditorArticulacaoController($('.js-textEditor')[0], {
  rotulo: {
    separadorArtigo: '',
    separadorArtigoSemOrdinal: '.',
    separadorParagrafo: '',
    separadorParagrafoSemOrdinal: '.'
  }
});

var documentEditorView = new DocumentEditorView();
documentEditorView.initEvents(editorCtrl);

var contextualToolbarView = new ContextualToolbarView();
contextualToolbarView.initEvents(editorCtrl);