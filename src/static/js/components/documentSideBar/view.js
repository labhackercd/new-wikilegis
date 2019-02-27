/*global $ events */

var DocumentSideBarView = function() {};

DocumentSideBarView.prototype.initEvents = function () {
  this.documentBody = $('.js-documentEditor');
  this.toggleButton = $('.js-documentEditor .js-toggleButton');

  this.subscribers();
  this.publishers();
};

DocumentSideBarView.prototype.subscribers = function () {
  var self = this;

  events.toggleSideBar.subscribe(function () {
    self.toggle();
  });
};

DocumentSideBarView.prototype.publishers = function () {
  var self = this;

  self.toggleButton.on('click', function() {
    events.toggleSideBar.publish();
  });
};

DocumentSideBarView.prototype.toggle = function () {
  var self = this;
  self.documentBody.toggleClass('-active');
};
