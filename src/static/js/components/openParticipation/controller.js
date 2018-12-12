/*global $ events Urls */

var InvitedGroupController = function() {};

InvitedGroupController.prototype.initEvents = function() {
  this.subscribers();
};

InvitedGroupController.prototype.subscribers = function() {
  var self = this;

  $.Topic(events.createInvitedGroup).subscribe(function() {
    self.createInvitedGroup();
  });
};

InvitedGroupController.prototype.createInvitedGroup = function() {
  var document_id = window.location.pathname.split('/').pop();
  var participants = [];
  $('.js-user').each(function() {
    participants.push($(this).data('userId'));
  });
  var emails = [];
  $('.js-email').each(function() {
    emails.push($(this).data('email'));
  });
  $.ajax({
    url: Urls.new_group(document_id),
    method: 'POST',
    data: {
      participants: participants,
      emails: emails,
      document: $('#id_document option:selected').val(),
      public_participation: $('#id_public_participation').prop('checked'),
      closing_date: $('#id_closing_date').val(),
      group_name: $('#id_group_name').val(),
    }
  });
};