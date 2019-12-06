/* exported events */
/* global $ */

var events = {
  // Triggered when user starts to select the text
  // Params: excerptId
  startTextSelection: $.Topic('startTextSelection'),

  // Triggered when user ends the text selections
  endTextSelection: $.Topic('endTextSelection'),

  // Triggered when user cancel the text selection by clicking on body
  cancelTextSelection: $.Topic('cancelTextSelection'),

  // Triggered when user tries to select the text starting outside of the document
  outsideDocumentMouseDown: $.Topic('outsideDocumentMouseDown'),

  // Triggered when user tries to select the text starting outside of the document
  outsideDocumentMouseUp: $.Topic('outsideDocumentMouseUp'),

  // Trigger when user tries to send a suggestion but the server return an error
  // Params: message
  showSuggestionInputError: $.Topic('showSuggestionInputError'),

  // Trigger when the server creates a suggestion successfully
  // Params: excerptId, html (excerpt)
  suggestionCreated: $.Topic('suggestionCreated'),

  // Triggered when user send suggestion
  // Params: excerptId, startIndex, endIndex, suggestion
  sendSuggestion: $.Topic('sendSuggestion'),

  // Triggered when user open menu
  openMenu: $.Topic('openMenu'),

  // Triggered when user closes menu
  closeMenu: $.Topic('closeMenu'),

  // Triggered when user ends text selection
  // Params: excerptId (can be null)
  activateOpinionCards: $.Topic('activateOpinionCards'),

  // Triggered when user open document page or when user select an excerpt
  // Params: excerptId (can be null)
  openOpinionModal: $.Topic('openOpinionModal'),

  // Triggered when user click on 'next suggestion'
  nextOpinion: $.Topic('nextOpinion'),

  // Triggered when user click on close modal
  closeOpinionModal: $.Topic('closeOpinionModal'),

  // Triggered when a modal is closed
  closeModal: $.Topic('closeModal'),

  // Triggered when a modal is opened
  openModal: $.Topic('openModal'),

  // Triggered before opinionModal opens
  // Params: user, excerpt, suggestion
  fillOpinionModal: $.Topic('fillOpinionModal'),

  // Triggered when user click on opinionModal button
  // Params: suggestionId, opinion (approve, reject, neutral)
  sendOpinion: $.Topic('sendOpinion'),

  // Triggered after the server processed the opinionVote
  // Params: opinion
  opinionSent: $.Topic('opinionSent'),

  // Triggered when user click on invitedGroup send button
  createInvitedGroup: $.Topic('createInvitedGroup'),

  // Triggered when user click on save in filter modal
  filterButton: $.Topic('filterButton'),

  // Triggered when user click on seleted profiles
  // Params: userId
  removeParticipant: $.Topic('removeParticipant'),

  // Triggered when user click on seleted profiles
  // Params: email
  removeEmail: $.Topic('removeEmail'),

  // Triggered when show selectables profiles
  // Params: countSelectables
  setCounterSelectables: $.Topic('setCounterSelectables'),

  // Triggered when show selecteds profiles
  // Params: countSelecteds
  setCounterSelecteds: $.Topic('setCounterSelecteds'),

  // Triggered when user clicks on openParticipation filter
  openFilterModal: $.Topic('openFilterModal'),

  // Triggered when user clicks on FilterModal close button or save button
  // Params: applyFilter
  closeFilterModal: $.Topic('closeFilterModal'),

  // Triggered when user clicks on clear button
  resetFilterModalForm: $.Topic('resetFilterModalForm'),

  // Triggered when user clicks on clear button
  clearFilters: $.Topic('clearFilters'),

  // Triggered when user clicks on apply filter
  showFilters: $.Topic('showFilters'),

  // Triggered when user send filter modal
  updateSearchParticipants: $.Topic('updateSearchParticipants'),

  // Triggered when user click on infoButton
  openInfoModal: $.Topic('openInfoModal'),

  // Triggered on highlight mouseenter
  // Params: parentNode, activeId
  openHighlightTooltip: $.Topic('openHighlightTooltip'),

  // Triggered on highlight mouseleave
  // Params: parentNode
  closeHighlightTooltip: $.Topic('closeHighlightTooltip'),

  // Triggered to show alert message
  // Params: message, messageType (success, fail, default), action ({name, text, link})
  showMessage: $.Topic('showMessage'),

  // Triggered after 5 seconds that showMessage was triggered
  // Params: cancelAction
  stopAlertProgress: $.Topic('stopAlertProgress'),

  // Triggered on alertMessage mouseover
  pauseAlertProgress: $.Topic('pauseAlertProgress'),

  // Triggered on alertMessage mouseleave
  resumeAlertProgress: $.Topic('resumeAlertProgress'),

  // Triggered when user click on alertMessage action
  // Params: actionUrl
  activateAlertAction: $.Topic('activateAlertAction'),

  // Triggered when the user undo suggestion succesfully
  // Params: {content, excerptId, excerptHtml, selectedText}
  suggestionUndone: $.Topic('suggestionUndone'),

  // Triggered when a user click on a howtoButton
  openAppOnboarding: $.Topic('openAppOnboarding'),

  // Triggered when a user close a appOnboarding
  closeAppOnboarding: $.Topic('closeAppOnboarding'),

  // Triggered after a user skips or select an opinion from the opinion-modal
  showNextSuggestion: $.Topic('showNextSuggestion'),

  // Triggered right after a user clicks on a button from the opinion-modal
  // Params: opinion
  showSubmissionCue: $.Topic('showSubmissionCue'),

  // Triggered when all opinions from excerpt are voted
  // Params: excerptId
  hideExcerptOpinionBalloon: $.Topic('hideExcerptOpinionBalloon'),

  // Triggered when all opinions from document are voted
  hideDocumentOpinionBalloon: $.Topic('hideDocumentOpinionBalloon'),

  // Triggered when user click on element to animate scroll
  // Params: position, element
  scrollToPosition: $.Topic('scrollToPosition'),

  // Triggered when user click on toggle button
  toggleSideBar: $.Topic('toggleSideBar'),

  // Triggered when user click on suggestion opinion
  selectSuggestion: $.Topic('selectSuggestion'),

  // Triggered when load document page or user click in filters
  showOpinions: $.Topic('showOpinions'),

  // Triggered when user click in collapsed excerpts
  // Params: element
  toggleExcerpt: $.Topic('toggleExcerpt'),

  // Triggered when user click Expand or Zip button
  collapseExpandExcerpts: $.Topic('collapseExpandExcerpts'),

  // Triggered when user ends document title edition
  // Params: newTitle
  documentTitleEditionEnd: $.Topic('documentTitleEditionEnd'),

  // Triggered when user clicks inside of text editor
  focusEditor: $.Topic('focusEditor'),

  // Triggered when user clicks outside of text editor
  blurEditor: $.Topic('blurEditor'),

  // Triggered when the contextualToolbar is opened
  openContextualToolbar: $.Topic('openContextualToolbar'),

  // Triggered when the contextualToolbar is closed
  closeContextualToolbar: $.Topic('closeContextualToolbar'),

  // Triggered when user click on openValidationButton
  openValidationModal: $.Topic('openValidationModal'),

  // Triggered when user click on closeValidationModal
  closeValidationModal: $.Topic('closeValidationModal'),

  // Triggered when user click on openConfirmFormButton
  openConfirmFormModal: $.Topic('openConfirmFormModal'),

  // Triggered when user click on closeConfirmFormModal
  closeConfirmFormModal: $.Topic('closeConfirmFormModal'),

  // Triggered when user click on openPublicFormModal
  openPublicFormModal: $.Topic('openPublicFormModal'),

  // Triggered when user click on closePublicFormModal
  closePublicFormModal: $.Topic('closePublicFormModal'),

  // Triggered when user click on openPublicInfoModal
  openPublicInfoModal: $.Topic('openPublicInfoModal'),

  // Triggered when user click on closePublicInfoModal
  closePublicInfoModal: $.Topic('closePublicInfoModal'),

  // Triggered when user create invited group
  closeInfoMessage: $.Topic('closeInfoMessage'),

  // Triggered when user click on send button
  // Params: documentId, closingDate, congressmanId, linkVideo, versionId
  sendPublicForm: $.Topic('sendPublicForm'),

  // Triggered when user click on send button
  // Params: groupId, closingDate, linkVideo, congressmanId
  sendUpdatePublicForm: $.Topic('sendUpdatePublicForm'),

  // Triggered when users want to save the document
  // Params: data (pk, title, description, html, autoSave, name)
  saveDocument: $.Topic('saveDocument'),

  // Triggered on auto save
  autoSaveDocument: $.Topic('autoSaveDocument'),

  // Trigger after any document save
  // Params: data (message, updated, timelineHTML, dropdownHTML, version)
  documentSaved: $.Topic('documentSaved'),

  // Triggered while the user is typing
  documentChanged: $.Topic('documentChanged'),

  // Triggered when the document text is loaded
  // Params: data (html, versionName, date, autoSave)
  documentTextLoaded: $.Topic('documentTextLoaded'),

  // Triggered before a text is loaded
  loadDocumentText: $.Topic('loadDocumentText'),

  // Triggered when user clicks on save at toolbar
  openSaveModal: $.Topic('openSaveModal'),

  // Triggered when user closes notificationList
  closeNotificationList: $.Topic('closeNotificationList'),

  // Triggered when user click on notification button
  updateNotifications: $.Topic('updateNotifications'),

  // Triggered when user selects an version to compare
  versionSelectedToCompare: $.Topic('versionSelectedToCompare'),

  // Triggered when the server returns data from diff text
  // Params: data (html, versionName, date, auto_save)
  textVersionLoaded: $.Topic('textVersionLoaded'),

  // Triggered when the versions are ready and will show the diff
  // Params: text1 (html, versionName, date, auto_save), text2 (html, versionName, date, autoSave)
  showDiff: $.Topic('showDiff'),

  // Triggered when user click on closeDiffButton
  closeDiff: $.Topic('closeDiff'),

  // Triggered when user click on excerpt
  highlightExcerpt: $.Topic('highlightExcerpt'),

  // Triggered when the document owner starts typing a document for the very first time
  showModifyExcerptTip: $.Topic('showModifyExcerptTip'),

  // Triggered when user click on openFeedbackFormModal
  openFeedbackFormModal: $.Topic('openFeedbackFormModal'),

  // Triggered when user click on closeFeedbackFormModal
  closeFeedbackFormModal: $.Topic('closeFeedbackFormModal'),

  // Triggered when user click on openFeedbackInfoModal
  openFeedbackInfoModal: $.Topic('openFeedbackInfoModal'),

  // Triggered when user click on closeFeedbackInfoModal
  closeFeedbackInfoModal: $.Topic('closeFeedbackInfoModal'),

  // Triggered when user click on openFeedbackWaitingModal
  openFeedbackWaitingModal: $.Topic('openFeedbackWaitingModal'),

  // Triggered when user click on closeFeedbackWaitingModal
  closeFeedbackWaitingModal: $.Topic('closeFeedbackWaitingModal'),

  // Triggered when user click on send button
  // Params: groupId, youtubeId, versionId
  sendFeedbackForm: $.Topic('sendFeedbackForm'),

  // Switches texts between their original version, the diff version and final version 
  switchTexts: $.Topic('switchTexts')
};
