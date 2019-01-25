/*global DocumentExcerptView DocumentBodyView SuggestionInputView
NavBurgerView SuggestionInputController OpinionModalView OpinionModalController
TextHighlightView HighlightTooltipView InfoModalView InfoButtonView 
OpinionOnboardingView TextSelectionOnboardingView */


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

var opinionOnboardingView = new OpinionOnboardingView();
opinionOnboardingView.initEvents(opinionModalView);

var infoButtonView = new InfoButtonView();
infoButtonView.initEvents();

var infoModal = new InfoModalView();
infoModal.initEvents();

var textHighlightView = new TextHighlightView();
textHighlightView.initEvents();

var highlightTooltipView = new HighlightTooltipView();
highlightTooltipView.initEvents();

var textSelectionOnboardingView = new TextSelectionOnboardingView();
textSelectionOnboardingView.initEvents();
