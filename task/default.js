var gulp            = require('gulp');
var sass            = require('gulp-sass');
var autoprefixer    = require('gulp-autoprefixer');
var concat          = require('gulp-concat');
var imagemin        = require('gulp-imagemin');
var uglify          = require('gulp-uglify');
var cssnano         = require('gulp-cssnano');
var htmlmin         = require('gulp-htmlmin');

var PortadaSass        = './front/src/sass/portada/';
var PortadaDestino     = './PagGestion/static/';

gulp.task('default',function() {
  console.log("Hola");
});


// gulp.task('portada-css', function(){
//     return gulp.src(PortadaSass + 'main.scss')
//         .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
//         .pipe(autoprefixer({
//             browsers: ['last 2 versions'],
//             cascade: false
//         }))
//         .pipe(cssnano())
//         .pipe(concat('custom-portada.min.css'))
//         .pipe(gulp.dest(PortadaDestino + 'css'));
// });
