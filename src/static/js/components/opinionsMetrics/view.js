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

  events.highlightExcerpt.subscribe(function (excerptElement) {
    self.highlightExcerpt(excerptElement);
  });
};

OpinionMetricsView.prototype.publishers = function() {
  $('.js-excerptWrapper').on('click', function() {
    if (!$(this).closest('.js-excerptWrapper').hasClass('-enabled')) {
      events.showOpinions.publish($(this).children('.js-documentExcerpt').data('id'));
    }
    events.highlightExcerpt.publish($(this).closest('.js-excerptWrapper'));
  });
  // $('.js-opinions').on('click .js-suggestionOpinion', function(e) {
  //   var excerptId = $(e.target).closest('.js-suggestionOpinion').data('excerptId');
  //   var currentId = $(e.target).closest('.js-suggestionOpinion').data('opinionId');
  //   var excerpt = $(`.js-documentExcerpt[data-id='${excerptId}']`);
  //   events.openHighlightTooltip.publish(excerpt, currentId.toString());
  // });
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

    var excerptId = $(suggestionOpinion).data('excerptId');
    var currentId = $(suggestionOpinion).data('opinionId');
    var excerpt = $(`.js-documentExcerpt[data-id='${excerptId}']`);
    events.openHighlightTooltip.publish(excerpt, currentId.toString());
  }
};

OpinionMetricsView.prototype.highlightExcerpt = function (excerptElement) {
  if (excerptElement.hasClass('-enabled')) {
    $('.js-documentEditor').removeClass('-supressed')
    $('.js-excerptWrapper').removeClass('-enabled');
    this.opinionsElement.html(`
      <div class="empty">
        Selecione um trecho ao lado para ver as opiniões.
      </div>
    `)
  } else {
    $('.js-excerptWrapper').removeClass('-enabled');
    $('.js-documentEditor').addClass('-supressed')
    excerptElement.addClass('-enabled')
  }
};