function addEvent(element, event, fn) {
    if (element.addEventListener) {
        element.addEventListener(event, fn, false);
    } else if (element.attachEvent) {
        element.attachEvent('on' + event, fn);
    }
}

//this function will work cross-browser for loading scripts asynchronously
function loadScript(src, callback) {
  var s,
      r,
      t,
      write;

  
  r = false;
  s = document.createElement('script');
  s.type = 'text/javascript';
  s.src = src;
  s.onload = s.onreadystatechange = function() {
    //console.log( this.readyState ); //uncomment this line to see which ready states are called.
    if ( !r && (!this.readyState || this.readyState == 'complete') )
    {
      r = true;
      if (callback !== undefined) {
        callback();
      }
    }
  };
  t = document.getElementsByTagName('script')[0];
  t.parentNode.insertBefore(s, t);
}
addEvent(window, 'load', function(){ loadScript('/static/js/loader.js')
        // '/static/js/loader.js',
        // function () { loadScript('/static/js/loader.js')} );
});
