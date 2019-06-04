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
  var self = this;

  $('.js-excerptWrapper').on('click', function() {
    if (!$(this).closest('.js-excerptWrapper').hasClass('-enabled')) {
      events.showOpinions.publish($(this).children('.js-documentExcerpt').data('id'));
    }
    events.highlightExcerpt.publish($(this).closest('.js-excerptWrapper'));
  });

  $('.js-documentEditor').on('click', function(e) {
    if (!$(e.target).hasClass('js-metricsIcons') &&
        $(e.target).closest('.js-excerptWrapper').length === 0 &&
        $(e.target).closest('.js-sideBar').length === 0 &&
        $(e.target).closest('.js-toolBar').length === 0 &&
        $(e.target).closest('.js-metricsButtons').length === 0
      ) {
        self.resetOpinions();
    }
  });
};

OpinionMetricsView.prototype.get_opinions = function(excerptId=undefined) {
  var self = this;
  var groupId = $('.js-articleDocument').data('groupId');

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
      var suggestionOpinion = $(e.target).closest('.js-suggestionOpinion');
      events.selectSuggestion.publish(suggestionOpinion);
    });

    $('.js-opinions .js-suggestionOpinion').on('mouseenter', function(e) {
      var suggestionOpinion = $(e.target).closest('.js-suggestionOpinion');
      var excerptId = $(suggestionOpinion).data('excerptId');
      var currentId = $(suggestionOpinion).data('opinionId');
      var excerpt = $(`.js-documentExcerpt[data-id='${excerptId}']`);

      events.openHighlightTooltip.publish(excerpt, currentId.toString());
    });

    $('.js-opinions .js-suggestionOpinion').on('mouseleave', function(e) {
      events.closeHighlightTooltip.publish($('.js-documentExcerpt'));
    });

    $('.js-suggestionText').truncate({lines: 3});
  });
};

OpinionMetricsView.prototype.select = function (suggestionOpinion) {
  if ($(suggestionOpinion).hasClass('-active')) {
    suggestionOpinion.removeClass('-active');

    suggestionOpinion.find('.js-suggestionText').truncate('collapse')

  } else {
    $('.js-opinions .js-suggestionOpinion').removeClass('-active');

    $(suggestionOpinion).addClass('-active');

    suggestionOpinion.find('.js-suggestionText').truncate('expand');
  }
};

OpinionMetricsView.prototype.resetOpinions = function () {
  var self = this;
  
  $('.js-documentEditor').removeClass('-supressed');
  $('.js-excerptWrapper').removeClass('-enabled');
  self.opinionsElement.html(`
    <div class="empty">
      Selecione um trecho ao lado para ver as opiniões.
    </div>
  `);
};

OpinionMetricsView.prototype.highlightExcerpt = function (excerptElement) {
  var self = this;

  events.closeHighlightTooltip.publish($('.js-documentExcerpt'));
  if (excerptElement.hasClass('-enabled')) {
    self.resetOpinions();
  } else {
    $('.js-excerptWrapper').removeClass('-enabled');
    $('.js-documentEditor').addClass('-supressed');
    excerptElement.addClass('-enabled');
  }
};
