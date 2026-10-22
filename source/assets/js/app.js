(function(){
  'use strict';
  // Mobile menu
  var t=document.querySelector('.toggle'),m=document.getElementById('menu');
  if(t&&m){t.addEventListener('click',function(){var o=m.classList.toggle('open');t.setAttribute('aria-expanded',o)});}
  // AdSense: slots stay hidden until a real publisher ID is added (see README)
  var slots=document.querySelectorAll('ins.adsbygoogle'),live=false;
  slots.forEach(function(s){
    var c=s.getAttribute('data-ad-client')||'',sl=s.getAttribute('data-ad-slot')||'';
    if(/^ca-pub-\d{10,}$/.test(c)&&/^\d{6,}$/.test(sl)&&!/^0+$/.test(sl)){
      live=true;try{(window.adsbygoogle=window.adsbygoogle||[]).push({});}catch(e){}
    }
  });
  document.documentElement.classList.add(live?'ad-on':(/adpreview/.test(location.search)?'ad-preview':'ad-off'));
  // Cookie / privacy notice
  var cb=document.getElementById('cookie');
  try{
    if(cb&&!localStorage.getItem('agri_notice')){cb.classList.add('show');}
    var ok=document.getElementById('cookie-ok');
    if(ok)ok.addEventListener('click',function(){localStorage.setItem('agri_notice','1');cb.classList.remove('show');});
  }catch(e){if(cb)cb.classList.add('show');}
})();
