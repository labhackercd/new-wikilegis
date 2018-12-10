/*global $ events Urls */

var InvitedGroupController = function() {};

InvitedGroupController.prototype.initEvents = function() {
  this.createGroup();
};

InvitedGroupController.prototype.createGroup = function() {
  var document_id = window.location.pathname.split('/').pop()
  $('.js-send-button').on('click', function() {
    var participants = []
    $(".js-user").each(function() {
      participants.push($(this).data('userId'));
    });
    var emails = []
    $(".js-email").each(function() {
      emails.push($(this).data('email'));
    });
    $.ajax({
      url: Urls.new_group(document_id),
      method: 'POST',
      data: {
        participants: participants,
        emails: emails,
        document: $("#id_document option:selected").val(),
        public_participation: $('#id_public_participation').prop('checked'),
        closing_date: $("#id_closing_date").val(),
        group_name: $("#id_group_name").val(),
      }
    });
  });
};