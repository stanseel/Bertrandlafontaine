// Menu op telefoon
(function () {
  var kop = document.querySelector('.kop');
  var knop = document.querySelector('.menuknop');
  if (!kop || !knop) return;
  knop.addEventListener('click', function () {
    var open = kop.classList.toggle('open');
    knop.setAttribute('aria-expanded', open ? 'true' : 'false');
    knop.textContent = open ? 'Sluit' : 'Menu';
  });
})();

// Homepage: de twee loops spelen om beurten
(function () {
  var video = document.querySelector('.home-loop video');
  if (!video) return;
  var loops = JSON.parse(video.getAttribute('data-loops') || '[]');
  var titel = document.querySelector('.home-loop .loop-titel');
  var stil = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var i = 0;
  function zet(n) {
    var l = loops[n];
    video.src = l.src;
    video.poster = l.poster;
    if (titel) { titel.textContent = l.titel; titel.href = l.href; }
    if (!stil) video.play().catch(function () {});
  }
  if (stil) { video.removeAttribute('autoplay'); video.pause(); return; }
  video.addEventListener('ended', function () { i = (i + 1) % loops.length; zet(i); });
})();

// Filmografie: filter op soort
(function () {
  var knoppen = document.querySelectorAll('[data-filter]');
  if (!knoppen.length) return;
  var rijen = document.querySelectorAll('.fg-rij');
  var teller = document.querySelector('.fg-teller');
  knoppen.forEach(function (k) {
    k.addEventListener('click', function () {
      var f = k.getAttribute('data-filter');
      knoppen.forEach(function (x) { x.setAttribute('aria-pressed', x === k ? 'true' : 'false'); });
      var n = 0;
      rijen.forEach(function (r) {
        var toon = f === 'alles' || r.getAttribute('data-soort') === f;
        r.parentElement.hidden = !toon;
        if (toon) n++;
      });
      if (teller) teller.textContent = n + (n === 1 ? ' productie' : ' producties');
    });
  });
})();
