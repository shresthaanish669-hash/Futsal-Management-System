// Minimal enhancement: hide status messages after they have been read.
window.setTimeout(() => {
  document.querySelectorAll('.message').forEach((message) => {
    message.style.transition = 'opacity 350ms ease';
    message.style.opacity = '0';
    window.setTimeout(() => message.remove(), 350);
  });
}, 5000);

