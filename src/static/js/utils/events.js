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
};