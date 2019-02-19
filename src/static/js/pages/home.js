/*global NavBurgerView NavBarView SearchInputView BackgroundParticle
AnimateScrollView HowtoButtonView AppOnboardingView */

var navBurgerView = new NavBurgerView();
navBurgerView.initEvents();

var navBarView = new NavBarView();
navBarView.initEvents();

var searchInputView = new SearchInputView();
searchInputView.initEvents();

var backgroundParticle = new BackgroundParticle();
backgroundParticle.initEvents();

var animateScrollView = new AnimateScrollView();
animateScrollView.initEvents();

var appOnboardingView = new AppOnboardingView();
appOnboardingView.initEvents('home');

var howtoButton = new HowtoButtonView();
howtoButton.initEvents();
