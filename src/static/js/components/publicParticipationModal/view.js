/*global $ events */

var PublicFormModalView = function () { };

PublicFormModalView.prototype.initEvents = function () {
  this.publicFormModalElement = $('.js-publicFormModal');
  this.publicInfoModalElement = $('.js-publicInfoModal');
  this.openPublicFormButton = $('.js-openPublicParticipation');
  this.closeFormElement = $('.js-publicFormModal .js-close');
  this.closeInfoElement = $('.js-publicInfoModal .js-close');
  this.subscribers();
  this.publishers();
};

PublicFormModalView.prototype.subscribers = function () {
  var self = this;
  events.openPublicFormModal.subscribe(function () {
    self.publicFormModalElement.addClass('-show');
  });
  events.closePublicFormModal.subscribe(function () {
    self.publicFormModalElement.removeClass('-show');
  });
  events.openPublicInfoModal.subscribe(function () {
    self.publicInfoModalElement.addClass('-show');
  });
  events.closePublicInfoModal.subscribe(function () {
    self.publicInfoModalElement.removeClass('-show');
  });
};

PublicFormModalView.prototype.publishers = function () {
  var self = this;

  self.openPublicFormButton.on('click', function (e) {
    e.preventDefault();
    events.openPublicFormModal.publish();
  });

  self.closeFormElement.on('click', function () {
    events.closePublicFormModal.publish();
  });

  $('.js-menuList').on('click', '.js-waitingButton', function () {
    events.openPublicInfoModal.publish();
  });

  self.closeInfoElement.on('click', function () {
    events.closePublicInfoModal.publish();
  });

  $('.js-publicFormModal .js-send').on('click', function (e) {
    e.preventDefault();
    if ($('.js-publicFormModal').data('groupId')) {
      self.sendUpdatePublicForm();
    } else {
      self.sendPublicForm();
    }
  });
};

PublicFormModalView.prototype.sendPublicForm = function () {
  var documentId = $('.js-documentEditor').data('documentId');
  var closingDate = $('.js-publicFormModal .js-closingDate').val();
  var congressmanId = $('.js-publicFormModal .js-congressmanId').val();
  var urlVideo = $('.js-publicFormModal .js-urlVideo').val();
  var versionId = $('.js-publicFormModal .js-versionsSelect').val();

  events.sendPublicForm.publish(
    documentId,
    closingDate,
    congressmanId,
    urlVideo,
    versionId
  );
};

PublicFormModalView.prototype.sendUpdatePublicForm = function () {
  var groupId = $('.js-publicFormModal').data('groupId');
  var closingDate = $('.js-closingDate').val();
  var congressmanId = $('.js-congressmanId').val();
  var urlVideo = $('.js-publicFormModal .js-urlVideo').val();

  events.sendUpdatePublicForm.publish(
    groupId,
    closingDate,
    urlVideo,
    congressmanId
  );
};