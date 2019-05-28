/*global $ events Urls */

var OpinionMetricsView = function() {};

OpinionMetricsView.prototype.initEvents = function() {
  this.opinionsElement = $('.js-opinions');
  this.subscribers();
  this.publishers();
};

OpinionMetricsView.prototype.subscribers = function() {
  var self = this;

  events.showOpinions.subscribe(function(excerptId=undefined) {
    self.get_opinions(excerptId);
  });

  events.selectSuggestion.subscribe(function (suggestionOpinion) {
    self.select(suggestionOpinion);
  });
};

OpinionMetricsView.prototype.publishers = function() {
  $('.js-excerptWrapper').on('click', function() {
    events.showOpinions.publish($(this).children('.js-documentExcerpt').data('id'));
  });
  $('.js-opinions').on('click .js-suggestionOpinion', function(e) {
    var excerptId = $(e.target).closest('.js-suggestionOpinion').data('excerptId');
    var currentId = $(e.target).closest('.js-suggestionOpinion').data('opinionId');
    var excerpt = $(`.js-documentExcerpt[data-id='${excerptId}']`);
    events.openHighlightTooltip.publish(excerpt, currentId.toString());
  });
};

OpinionMetricsView.prototype.get_opinions = function(excerptId=undefined) {
  var self = this;
  var groupId = $('.js-articleDocument').data('groupId')

  var request = $.ajax({
    url: Urls.excerpt_opinions(excerptId),
    method: 'POST',
    dataType: 'json',
    data: {
      groupId: groupId,
    }
  });

  request.done(function(data) {
    self.opinionsElement.html(data.opinionsHtml);
    $('.js-opinions .js-suggestionOpinion').on('click', function(e) {
      events.selectSuggestion.publish(e.target.closest('.js-suggestionOpinion'));
    });
  });
};

OpinionMetricsView.prototype.select = function (suggestionOpinion) {
  if ($(suggestionOpinion).hasClass('-active')) {
    events.closeHighlightTooltip.publish($('.js-documentExcerpt'));
    $('.js-opinions .js-suggestionOpinion').removeClass('-active');

  } else {
    events.closeHighlightTooltip.publish($('.js-documentExcerpt'));
    $('.js-opinions .js-suggestionOpinion').removeClass('-active');

    $(suggestionOpinion).addClass('-active');

    $(suggestionOpinion).find('.js-opinion').each(function(i, element){
      events.openHighlightTooltip.publish(
        $('.js-documentExcerpt'),
        $(element).data('opinionId').toString()
      );
    });

  }
};