/*global $ events */

var DocumentSideBarView = function() {};

DocumentSideBarView.prototype.initEvents = function () {
  this.documentBody = $('.js-documentEditor');
  this.toggleButton = $('.js-documentEditor .js-toggleButton');
  this.suggestionClusters = $('.js-documentEditor .js-suggestionCluster');

  this.subscribers();
  this.publishers();
};

DocumentSideBarView.prototype.subscribers = function () {
  var self = this;

  events.toggleSideBar.subscribe(function () {
    self.toggle();
  });

  events.selectSuggestion.subscribe(function (suggestionCluster) {
    self.select(suggestionCluster);
  });
};

DocumentSideBarView.prototype.publishers = function () {
  var self = this;

  self.toggleButton.on('click', function() {
    events.toggleSideBar.publish();
  });

  self.suggestionClusters.on('click', function(e) {

    events.selectSuggestion.publish(e.target.closest('.js-suggestionCluster'));
  });
};

DocumentSideBarView.prototype.toggle = function () {
  var self = this;
  self.documentBody.toggleClass('-active');
};

DocumentSideBarView.prototype.select = function (suggestionCluster) {
  var self = this;
  if ($(suggestionCluster).hasClass('-active')) {
    self.suggestionClusters.removeClass('-active');
  } else {
    self.suggestionClusters.removeClass('-active');
    $(suggestionCluster).addClass('-active');
  }
};
