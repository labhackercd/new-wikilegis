/* global DocumentSideBarView OpinionMetricsView TextHighlightView
ReduceExcerptsView PageMinimap DocumentOpinionsBodyView */

var documentSideBarView = new DocumentSideBarView();
documentSideBarView.initEvents();

var opinionMetricsView = new OpinionMetricsView();
opinionMetricsView.initEvents();

var textHighlightView = new TextHighlightView();
textHighlightView.initEvents();

var reduceExcerptsView = new ReduceExcerptsView();
reduceExcerptsView.initEvents();

var pageMinimap = new PageMinimap();
pageMinimap.initEvents();

var documentOpinionsBodyView = new DocumentOpinionsBodyView();
documentOpinionsBodyView.initEvents();
