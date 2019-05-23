/*global AppModalView NavBarView BodyView TextInputView AlertMessageView
AlertMessageController NotificationButtonView */

var appModalView = new AppModalView();
appModalView.initEvents();

var navBarView = new NavBarView();
navBarView.initEvents();

var bodyView = new BodyView();
bodyView.initEvents();

var textInputView = new TextInputView();
textInputView.initEvents();

var alertMessageView = new AlertMessageView();
alertMessageView.initEvents();

var alertMessageController = new AlertMessageController();
alertMessageController.initEvents();

var notificationButtonView = new NotificationButtonView();
notificationButtonView.initEvents();

var notificationController = new NotificationController();
notificationController.initEvents();
