var VideoHelperModalView = function() {};

VideoHelperModalView.prototype.initEvents = function() {
		this.videoHelper = $('.js-videoHelperModal');
    this.subscribers();
};

VideoHelperModalView.prototype.subscribers = function() {
	var self = this;
  events.openVideoHelperModal.subscribe(function() {
    self.videoHelper.addClass('-show');
  });
}
