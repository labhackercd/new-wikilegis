/*global $ events Urls */

var PublicFormController = function () { };

PublicFormController.prototype.initEvents = function () {
  this.subscribers();
};

PublicFormController.prototype.subscribers = function () {
  var self = this;

  events.sendPublicForm.subscribe(function (documentId, closingDate, congressmanId, linkVideo, versionId) {
    self.sendForm(documentId, closingDate, congressmanId, linkVideo, versionId);
  });

  events.sendUpdatePublicForm.subscribe(function (groupId, closingDate, linkVideo, congressmanId) {
    self.sendUpdateForm(groupId, closingDate, linkVideo, congressmanId);
  });

  events.openPublicFormModal.subscribe(function () {
    self.populateNamedVersions();
  });
};

PublicFormController.prototype.populateNamedVersions = function () {
  var documentId = $('.js-documentEditor').data('documentId');
  var request = $.ajax({
    url: Urls.list_document_versions(documentId),
    method: 'GET',
  });

  request.done(function (data) {
    var versionList = $('.js-publicFormModal .js-versionsSelect');
    versionList.html('');
    $.each(data.versions, function (idx, value) {
      versionList.append(`<option value="${value.pk}">${value.name}</option>`);
    });
    versionList.parent().addClass('-filled');
  });
};

PublicFormController.prototype.sendForm = function (documentId, closingDate, congressmanId, urlVideo, versionId) {
  var request = $.ajax({
    url: Urls.new_public_participation(documentId),
    method: 'POST',
    data: {
      closing_date: closingDate,
      congressman_id: congressmanId,
      url_video: urlVideo,
      versionId: versionId
    }
  });

  request.done(function () {
    events.closePublicFormModal.publish();
    events.openPublicInfoModal.publish();
    $('.js-openPublicParticipation').after(`
        <a href="#" class="js-waitingButton">
          <span>Participação Pública</span>
          <div class="info">
            <div class="item -blue">Aguardando</div>
          </div>
        </a>
      `);
    $('.js-openPublicParticipation').remove();
  });

  request.fail(function (jqXHR) {
    $('.js-publicFormModal .js-formError').html(`
        <li>${jqXHR.responseJSON.error}</li>
    `);
  });

};

PublicFormController.prototype.sendUpdateForm = function (groupId, closingDate, urlVideo, congressmanId) {
  var request = $.ajax({
    url: Urls.update_public_participation(groupId),
    method: 'POST',
    data: {
      closing_date: closingDate,
      congressman_id: congressmanId,
      url_video: urlVideo
    }
  });

  request.done(function () {
    events.closePublicFormModal.publish();
    events.openPublicInfoModal.publish();
  });

  request.fail(function (jqXHR) {
    $('.js-formError').html(`
        <li>${jqXHR.responseJSON.error}</li>
    `);
  });

};
