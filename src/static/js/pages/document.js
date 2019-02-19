/*global DocumentExcerptView DocumentBodyView SuggestionInputView
NavBurgerView SuggestionInputController OpinionModalView OpinionModalController
TextHighlightView HighlightTooltipView InfoModalView InfoButtonView AppOnboardingView HowtoButtonView */


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

var textHighlightView = new TextHighlightView();
textHighlightView.initEvents();

var highlightTooltipView = new HighlightTooltipView();
highlightTooltipView.initEvents();

var appOnboardingView = new AppOnboardingView();
appOnboardingView.initEvents('document');

var howtoButton = new HowtoButtonView();
howtoButton.initEvents();
