/* exported events */

var events = {
  // Triggered when user starts to select the text
  // Params: excerptId
  startTextSelection: 'startTextSelection',

  // Triggered when user ends the text selections
  endTextSelection: 'endTextSelection',

  // Triggered when user cancel the text selection by clicking on body
  cancelTextSelection: 'cancelTextSelection',

  // Triggered when user tries to select the text starting outside of the document
  outsideDocumentMouseDown: 'outsideDocumentMouseDown',

  // Triggered when user tries to select the text starting outside of the document
  outsideDocumentMouseUp: 'outsideDocumentMouseUp',

  // Trigger when user tries to send a suggestion but the server return an error
  // Params: message
  showSuggestionInputError: 'showSuggestionInputError',

  // Trigger when the server creates a suggestion successfully
  // Params: excerptId, html (excerpt)
  suggestionCreated: 'suggestionCreated',

  // Triggered when user send suggestion
  // Params: excerptId, selectedText, suggestion
  sendSuggestion: 'sendSuggestion',

  // Triggered when user open menu
  openMenu: 'openMenu',

  // Triggered when user closes menu
  closeMenu: 'closeMenu',

  // Triggered when user open document page or when user select an excerpt
  // Params: excerptId (can be null)
  openOpinionModal: 'openOpinionModal',

  // Triggered when user click on close modal
  // Params: reopen
  closeOpinionModal: 'closeOpinionModal',

  // Triggered before opinionModal opens
  // Params: user, excerpt, suggestion
  fillOpinionModal: 'fillOpinionModal',

  // Triggered when user click on opinionModal button
  // Params: suggestionId, opinion (approve, reject, neutral)
  sendOpinion: 'sendOpinion',

  // Triggered when user click on invitedGroup send button
  createInvitedGroup: 'createInvitedGroup',

  // Triggered when user click on themes
  // Params: themeId
  setThemes: 'setThemes',
};
