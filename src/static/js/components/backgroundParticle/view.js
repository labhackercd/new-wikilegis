/*global $ prefixURL */

var BackgroundParticle = function() {};

BackgroundParticle.prototype.initEvents = function() {
  particlesJS.load('headerParticles', prefixURL + '/static/js/components/backgroundParticle/config.json');
};
