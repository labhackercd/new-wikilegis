/*global DocumentSideBarView OpinionMetricsView TextHighlightView ReduceExcerptsView
ValidationModalView CongressmanAutocompleteView PublicFormModalView
PublicFormController PageMinimap DocumentOpinionsBodyView */

var documentSideBarView = new DocumentSideBarView();
documentSideBarView.initEvents();

var opinionMetricsView = new OpinionMetricsView();
opinionMetricsView.initEvents();

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

var documentOpinionsBodyView = new DocumentOpinionsBodyView();
documentOpinionsBodyView.initEvents();
