/*global DocumentExcerptView DocumentBodyView SuggestionInputView
NavBurgerView SuggestionInputController OpinionModalView OpinionModalController InfoButtonView InfoModalView */


var documentExcerptView = new DocumentExcerptView();
documentExcerptView.initEvents();

var documentBodyView = new DocumentBodyView();
documentBodyView.initEvents();

var suggestionInputView = new SuggestionInputView();
suggestionInputView.initEvents();

var suggestionInputController = new SuggestionInputController();
suggestionInputController.initEvents();

var navBurgerView = new NavBurgerView();
navBurgerView.initEvents();

var opinionModalView = new OpinionModalView();
opinionModalView.initEvents();

var opinionModalController = new OpinionModalController();
opinionModalController.initEvents();

var infoButtonView = new InfoButtonView();
infoButtonView.initEvents();

var infoModal = new InfoModalView();
infoModal.initEvents();
