const gulp = require('gulp');
const { src, dest, parallel } = require('gulp');

const gzip = require('gulp-gzip');
const closureCompiler = require('google-closure-compiler').gulp();
const htmlmin = require('gulp-htmlmin');
const cleanCSS = require('gulp-clean-css');

const gzipOptions = { gzipOptions: { level: 9,memLevel: 9 } }

const exec = require('child_process').exec;
const execSync = require('child_process').execSync;
const fs = require('fs');

//https://www.npmjs.com/package/gulp-gzip
//https://github.com/jonschlinkert/gulp-htmlmin
//https://www.npmjs.com/package/google-closure-compiler
//https://github.com/google/closure-compiler-npm/blob/master/packages/google-closure-compiler/docs/gulp.md


function uploadFile(file){

 	console.log(file);

	let command = "ampy --port /dev/ttyUSB0 put ./"+file

  	execSync(command);

}


//-----------------------------------------------------------------------------
gulp.task('css', () => {
  return gulp.src('./www/main.css', {base: './www'})
    .pipe(cleanCSS())

        .pipe(gzip(gzipOptions))
        .pipe(gulp.dest('build/'));
});

//-----------------------------------------------------------------------------
gulp.task('js', function () {
  	return gulp.src('./www/*.js', {base: './'})
      	.pipe(closureCompiler({
        	compilation_level: 'SIMPLE',
        	warning_level: 'VERBOSE',
          	language_in: 'ECMASCRIPT6_STRICT',
          	language_out: 'ECMASCRIPT5_STRICT',
          	output_wrapper: '(function(){\n%output%\n}).call(this)',
          	js_output_file: 'main.js'
        }, {
          	platform: ['native', 'java', 'javascript']
        }))

        .pipe(gzip(gzipOptions))
        .pipe(gulp.dest('./build'));
});


//-----------------------------------------------------------------------------
gulp.task('html', () => {
  return gulp.src('./www/index.html', {base: './www'})

    .pipe(htmlmin({ collapseWhitespace: true }))
    .pipe(gzip(gzipOptions))
    .pipe(gulp.dest('build/'));
});


//-----------------------------------------------------------------------------
gulp.task('fillBuild', (cb) => {

	let files = [
		"boot.py",
		"hardware.py",
		"wifi.py",
		"microWebSrv.py",
		"stepper_lib/ULN2003-for-ESP32/stepper.py",
		"webinterface.py",
		"cfg/network.cfg",
		"cfg/hardware.cfg"
	]


	files.forEach(function (file) {

    	return gulp.src('./'+ file)
      	.pipe(gulp.dest('./build/'));
  	});

  	cb();
  
 
});


//-----------------------------------------------------------------------------
gulp.task('build', gulp.parallel('html', 'js','css','fillBuild'));



//-----------------------------------------------------------------------------
gulp.task('initBoard', function (cb) {

	fs.readdirSync("./build",{"withFileTypes":true}).forEach(file => {
 
 		uploadFile("build/"+file);

	});

cb()
})




