/*global $ events */

var ClustersView = function() {};

ClustersView.prototype.initEvents = function() {
  this.clustersElement = $('.js-clusters');
  this.subscribers();
  this.publishers();
};

ClustersView.prototype.subscribers = function() {
  var self = this;

  events.showClusters.subscribe(function(groupId=undefined) {
    self.clustering(groupId);
  });

  events.selectSuggestion.subscribe(function (suggestionCluster) {
    self.select(suggestionCluster);
  });
};

ClustersView.prototype.publishers = function() {
  events.showClusters.publish();
};

ClustersView.prototype.clustering = function(groupId=undefined) {
  var self = this;
  var documentId = $('.js-documentEditor').data('documentId');

  var request = $.ajax({
    url: Urls.document_clusters(documentId),
    method: 'POST',
    dataType: 'json',
    data: {
      groupId: groupId,
    }
  })

  request.done(function(data) {
    self.clustersElement.html(data.clustersHtml);
    $('.js-clusters .js-suggestionCluster').on('click', function(e) {
      events.selectSuggestion.publish(e.target.closest('.js-suggestionCluster'));
    });
  });
};

ClustersView.prototype.select = function (suggestionCluster) {
  if ($(suggestionCluster).hasClass('-active')) {
    events.closeHighlightTooltip.publish($('.js-documentExcerpt'));
    $('.js-clusters .js-suggestionCluster').removeClass('-active');

  } else {
    events.closeHighlightTooltip.publish($('.js-documentExcerpt'));
    $('.js-clusters .js-suggestionCluster').removeClass('-active');

    $(suggestionCluster).addClass('-active');

    $(suggestionCluster).find('.js-opinion').each(function(i, element){
      events.openHighlightTooltip.publish(
        $('.js-documentExcerpt'),
        $(element).data('opinionId').toString()
      );
    })

  }
};