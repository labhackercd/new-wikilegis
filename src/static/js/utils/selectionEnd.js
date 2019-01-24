var selectionEndTimeout = null;
document.onselectionchange = userSelectionChanged;

function userSelectionChanged() {

  if (selectionEndTimeout) {
    clearTimeout(selectionEndTimeout);
  }

  selectionEndTimeout = setTimeout(function () {
    $('.js-documentExcerpt').trigger('selectionend');
  }, 500);
};