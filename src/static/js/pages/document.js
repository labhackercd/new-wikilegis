/*global DocumentExcerptView BodyView DocumentBodyView SuggestionInputView
NavBurgerView NavBarView SuggestionInputController OpinionModalView */


var documentExcerptView = new DocumentExcerptView();
documentExcerptView.initEvents();

var bodyView = new BodyView();
bodyView.initEvents();

var documentBodyView = new DocumentBodyView();
documentBodyView.initEvents();

var suggestionInputView = new SuggestionInputView();
suggestionInputView.initEvents();

var suggestionInputController = new SuggestionInputController();
suggestionInputController.initEvents();

var navBurgerView = new NavBurgerView();
navBurgerView.initEvents();

var navBarView = new NavBarView();
navBarView.initEvents();

var opinionModalView = new OpinionModalView();
opinionModalView.initEvents();
