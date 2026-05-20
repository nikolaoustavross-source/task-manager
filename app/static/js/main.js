// Auto-dismiss flash alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(function () { alert.remove(); }, 500);
    }, 4000);
  });

  // Mark overdue tasks: inject 'today' from server is cleaner but we can also
  // do it client-side as a fallback visual cue.
  const today = new Date().toISOString().split('T')[0];
  document.querySelectorAll('.task-due').forEach(function (el) {
    const text = el.textContent.trim();
    // Already handled server-side via Jinja; this is just a safety net.
  });
});
