/*global $ silegismgEditorArticulacaoController ContextualToolbarView
DocumentEditorView ValidationModalView InfoMessageView
CongressmanAutocompleteView PublicFormModalView PublicFormController
ToolBarView ToolBarController SaveMessageView */

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

var documentEditorController = new DocumentEditorController();
documentEditorController.initEvents();

var documentEditorView = new DocumentEditorView();
documentEditorView.initEvents(editor, contextualToolbarView);

var validationModalView = new ValidationModalView();
validationModalView.initEvents();

var infoMessageView = new InfoMessageView();
infoMessageView.initEvents();

var congressmanAutocompleteView = new CongressmanAutocompleteView();
congressmanAutocompleteView.initEvents();

var publicFormModalView = new PublicFormModalView();
publicFormModalView.initEvents();

var publicFormController = new PublicFormController();
publicFormController.initEvents();

var toolBarController = new ToolBarController();
toolBarController.initEvents();

var toolBarView = new ToolBarView();
toolBarView.initEvents(documentEditorView);

var saveMessageView = new SaveMessageView();
saveMessageView.initEvents();

var saveModalView = new SaveModalView();
saveModalView.initEvents();