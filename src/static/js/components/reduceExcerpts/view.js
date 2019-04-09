/*global $ events */

var ReduceExcerptsView = function() {};

ReduceExcerptsView.prototype.initEvents = function () {
  this.excerptsWithoutOpinion = $('.js-excerptWrapper.-reduce');
  this.subscribers();
  this.publishers();
};

ReduceExcerptsView.prototype.subscribers = function () {
  var self = this;
  events.toggleExcerpt.subscribe(function (excerptElement) {
    self.toggleExceprt(excerptElement);
  });
  events.collapseExpandExcerpts.subscribe(function (display) {
    self.collapseExpandExcerpts(display);
  });
};

ReduceExcerptsView.prototype.publishers = function () {
  var self = this;
  $(window).on('load', function() {
    self.excerptsWithoutOpinion.children().not('b, .js-defaultText').hide();
  });
  self.excerptsWithoutOpinion.on('click', function(e) {
    events.toggleExcerpt.publish($(e.target).closest('.js-excerptWrapper'));
  });

  $('.js-collapseExpand').on('click', function(e) {
    e.preventDefault();
    if ($(e.target).closest('.js-collapseExpand').hasClass('-collapsed')) {
      events.collapseExpandExcerpts.publish(false);
    } else {
      events.collapseExpandExcerpts.publish(true);
    }
  });
};

ReduceExcerptsView.prototype.toggleExceprt = function (excerptElement) {
  excerptElement.children().not('b').toggle();
};

ReduceExcerptsView.prototype.collapseExpandExcerpts = function (display) {
  var self = this;
  if (display) {
    $('.js-collapseExpand').addClass('-collapsed');
    $('.js-collapseExpand').attr('aria-label', 'Expandir');
    $('.js-defaultText').show();
    self.excerptsWithoutOpinion.children().not('b, .js-defaultText').hide();
  } else {
    $('.js-collapseExpand').removeClass('-collapsed');
    $('.js-collapseExpand').attr('aria-label', 'Comprimir');
    $('.js-defaultText').hide();
    self.excerptsWithoutOpinion.children().not('b, .js-defaultText').show();
  }
};
