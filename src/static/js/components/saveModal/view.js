/*global $ events */

var SaveModalView = function() {};

SaveModalView.prototype.initEvents = function() {
  this.saveModal = $('.js-saveModal');
  this.sendButton = $('.js-saveModal .js-send');
  this.sendButtonLoad = $('.js-saveModal .js-send .js-load');
  this.sendButtonText = $('.js-saveModal .js-send .js-text');
  this.nameInput = $('.js-saveModal .js-name');

  this.subscribers();
  this.publishers();
};

SaveModalView.prototype.subscribers = function() {
  var self = this;

  events.openSaveModal.subscribe(function() {
    self.saveModal.addClass('-show');
  });

  events.documentSaved.subscribe(function() {
    self.saveModal.removeClass('-show');
    self.nameInput.val('');
    events.closeModal.publish();
  });

  events.documentSaved.subscribe(function() {
    self.hideLoading();
  });
};

SaveModalView.prototype.publishers = function() {
  var self = this;

  self.sendButton.on('click', function() {
    if (self.nameInput.val() === '') {
      $('.js-saveModal .js-formError').html(`
          <li>Nome é obrigatório.</li>
      `);
      return false;
    }

    var html = '';
    var editor = $('.js-textEditor')[0];
    if (editor.innerText.length >= 2) {
      html = editor.innerHTML;
    }

    var data = {
      pk: $('.js-documentEditor').data('documentId'),
      title: $('.js-documentEditor .js-titleInput').val(),
      description: $('.js-documentEditor .js-descriptionInput').val(),
      html: html,
      autoSave: false,
      name: self.nameInput.val()
    };

    events.saveDocument.publish(data);
    self.showLoading();
    return false;
  });
};

SaveModalView.prototype.showLoading = function() {
  this.sendButtonLoad.removeClass('_hidden');
  this.sendButtonText.text('Salvando');

  this.sendButton.attr('disabled', 'disabled');
  this.sendButton.removeClass('-green');
  this.sendButton.addClass('-gray');
};

SaveModalView.prototype.hideLoading = function() {
  this.sendButtonLoad.addClass('_hidden');
  this.sendButtonText.text('Salvar');

  this.sendButton.removeAttr('disabled');
  this.sendButton.removeClass('-gray');
  this.sendButton.addClass('-green');
};