(function () {
  var video = document.querySelector('video');

  var pictureWidth = 640;
  var pictureHeight = 480;

  function checkRequirements() {
    var deferred = new $.Deferred();

    //camera access
    if (!Modernizr.getusermedia) {
      deferred.reject('Your browser doesn\'t support getUserMedia (according to Modernizr).');
    }
    //web workers, typed arrays and file API are required by gif.js
    if (!Modernizr.webworkers) {
      deferred.reject('Your browser doesn\'t support web workers (according to Modernizr).');
    }
    if (!Modernizr.filereader) {
      deferred.reject('Your browser doesn\'t support File API (according to Modernizr).');
    }
    if (!Modernizr.typedarrays) {
      deferred.reject('Your browser doesn\'t support typed arrays (according to Modernizr).');
    }

    deferred.resolve();

    return deferred.promise();
  }

  function searchForFrontCamera() {
    var deferred = new $.Deferred();

    //MediaStreamTrack.getSources seems to be supported only by Chrome
    if (MediaStreamTrack && MediaStreamTrack.getSources) {
      MediaStreamTrack.getSources(function (sources) {
        var rearCameraIds = sources.filter(function (source) {
          return (source.kind === 'video' && source.facing === 'user');
        }).map(function (source) {
          return source.id;
        });

        if (rearCameraIds.length) {
          deferred.resolve(rearCameraIds[0]);
        } else {
          deferred.resolve(null);
        }
      });
    } else {
      deferred.resolve(null);
    }

    return deferred.promise();
  }

  function setupVideo(frontCameraId) {
    var deferred = new $.Deferred();
    var getUserMedia = Modernizr.prefixed('getUserMedia', navigator);
    var videoSettings = {
      video: {
        optional: [
          {
            width: {max: pictureWidth}
          },
          {
            height: {max: pictureHeight}
          }
        ]
      }
    };

    //if front camera is available - use it
    if (frontCameraId) {
      videoSettings.video.optional.push({
        sourceId: frontCameraId
      });
    }

    getUserMedia(videoSettings, function (stream) {
      //Setup the video stream
      video.src = window.URL.createObjectURL(stream);

      window.stream = stream;

      video.addEventListener("loadedmetadata", function (e) {
        //get video width and height as it might be different than we requested
        pictureWidth = this.videoWidth;
        pictureHeight = this.videoHeight;

        if (!pictureWidth && !pictureHeight) {
          //firefox fails to deliver info about video size on time (issue #926753), we have to wait
          var waitingForSize = setInterval(function () {
            if (video.videoWidth && video.videoHeight) {
              pictureWidth = video.videoWidth;
              pictureHeight = video.videoHeight;

              clearInterval(waitingForSize);
              deferred.resolve();
            }
          }, 100);
        } else {
          deferred.resolve();
        }
      }, false);
    }, function () {
      deferred.reject('There is no access to your camera, have you denied it?');
    });

    return deferred.promise();
  }

  function setupVideoPush() {
    var deferred = new $.Deferred();

    var rcanvas = document.querySelector('#step1 canvas.visible');
    var rctx = rcanvas.getContext('2d');

    var canvas = document.querySelector('#step1 canvas.hidden');
    var ctx = canvas.getContext('2d');

    var scaledWidth = 480, scaledHeight = Math.round((scaledWidth / pictureWidth) * pictureHeight);
    canvas.width = pictureWidth;
    canvas.height = pictureHeight;

    rcanvas.width = scaledWidth;
    rcanvas.height = scaledHeight;

    function pushFrame() {
        console.log('Width: ' + canvas.width + ', Height: ' + canvas.height);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        $.ajax({type: 'POST', url: 'api', dataType: 'json', data: {'imgBase64': canvas.toDataURL()}}).done(function(data) {
            var img = new Image();
            img.src = data.imgBase64;
            img.onload = function() {
                rctx.drawImage(img, 0, 0, rcanvas.width, rcanvas.height);
            }

            var emotionsX = [];
            var emotionsY = [];

            $.each(data.emotions, function(key, value) {
                emotionsY.push(key);
                emotionsX.push(value);
            });

            var emotionsData = [{
                x: emotionsX,
                y: emotionsY,
                type:'bar',
                orientation: 'h',
                marker: { color: ['red', 'green', 'blue', 'red', 'green', 'blue'] }
            }];
            var emotionsLayout = {title:'Emotions', showlegend:false, xaxis:{range:[0.0, 1.0]}};

            Plotly.newPlot('panel1', emotionsData, emotionsLayout, {staticPlot: true});
        });

        setTimeout(pushFrame, 200);
    }

    setTimeout(pushFrame, 0);

    deferred.resolve();
    return deferred.promise();
  }

  function setupAll() {
    checkRequirements()
      .then(searchForFrontCamera)
      .then(setupVideo)
      .then(setupVideoPush)
      .done(function () {
        //Hide the 'enable the camera' info
        $('#step1 figure').removeClass('not-ready');
      })
      .fail(function (error) {
        showError(error);
      });
  }

  setupAll();
  $('.help').popover();

  video.play();

  function showError(text) {
    $('.alert').show().find('span').text(text);
  }
})();
