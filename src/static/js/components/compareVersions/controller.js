/*global $ events */

var CompareVersionsController = function() {};

CompareVersionsController.prototype.initEvents = function() {
}

CompareVersionsController.prototype.loadDiffText = function(documentId, versionNumber) {
  var request = $.ajax({
    url: Urls.document_text(documentId) + '?format=html&version=' + versionNumber,
    method: 'GET',
  });

  request.done(function(data) {
    events.textVersionLoaded.publish(data);
  });

  request.fail(function(jqXHR) {
    var data = jqXHR.responseJSON;
    events.showMessage.publish(data.message, 'fail', null);
  });
};