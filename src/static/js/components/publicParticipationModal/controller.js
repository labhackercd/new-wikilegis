/*global $ events Urls */

var PublicFormController = function() {};

PublicFormController.prototype.initEvents = function() {
  this.subscribers();
};

PublicFormController.prototype.subscribers = function() {
  var self = this;

  events.sendPublicForm.subscribe(function(documentId, closingDate, congressmanId) {
    self.sendForm(documentId, closingDate, congressmanId);
  });
};

PublicFormController.prototype.sendForm = function(documentId, closingDate, congressmanId) {
  var request = $.ajax({
    url: Urls.new_public_participation(documentId),
    method: 'POST',
    data: {
      closing_date: closingDate,
      congressman_id: congressmanId
    }
  });

  request.done(function() {
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

  request.fail(function(jqXHR) {
    $('.js-formError').html(`
        <li>${jqXHR.responseJSON.error}</li>
    `);
  });

};
