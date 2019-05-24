/*global DocumentSideBarView ClustersView TextHighlightView ReduceExcerptsView
ValidationModalView CongressmanAutocompleteView PublicFormModalView
PublicFormController PageMinimap */

var documentSideBarView = new DocumentSideBarView();
documentSideBarView.initEvents();

var clustersView = new ClustersView();
clustersView.initEvents();

var textHighlightView = new TextHighlightView();
textHighlightView.initEvents();

var reduceExcerptsView = new ReduceExcerptsView();
reduceExcerptsView.initEvents();

var validationModalView = new ValidationModalView();
validationModalView.initEvents();

var congressmanAutocompleteView = new CongressmanAutocompleteView();
congressmanAutocompleteView.initEvents();

var publicFormModalView = new PublicFormModalView();
publicFormModalView.initEvents();

var publicFormController = new PublicFormController();
publicFormController.initEvents();

var pageMinimap = new PageMinimap();
pageMinimap.initEvents();
