window.addEventListener('load', () => {
    const audio = document.getElementById('background-audio');
    const startButton = document.querySelector('.primary-btn');
  
    if (startButton && audio) {
      startButton.addEventListener('click', () => {
        audio.muted = false; // unmute
        audio.volume = 0.3;  // set soft volume
        audio.play();        // try playing again
      });
    }
  });
  