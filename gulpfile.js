var gulp = require('gulp');
var browserSync = require('browser-sync');
var reload = browserSync.reload;

// watch files for changes and reload
gulp.task('serve', function() {
  browserSync({
    server: {
      baseDir: '.'
    },
    port: 3333
  });

  gulp.watch(['*.html', 'css/*.css', 'js/*.js'], reload);
});
