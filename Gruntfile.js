module.exports = function(grunt){
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        coffee: {
            default: {
                expand: true,
                flatten: true,
                cwd: 'src/js',
                src: ['*.coffee'],
                dest: 'krympa/static/js/',
                ext: '.js'
            }
        },
        copy: {
            default: {
                files: [
                    { expand: true,
                      cwd: 'src/js/',
                      src: ['*.js'],
                      dest: 'krympa/static/js/'
                    },
                    { expand: true,
                      cwd: 'src/styles/',
                      src: ['*.css'],
                      dest: 'krympa/static/styles/'
                    }
                ]
            }
        },
        less: {
            default: {
                expand: true,
                cwd: 'src/styles/',
                src: ['*.less'],
                dest: 'krympa/static/styles/',
                ext: '.css'
            }
        },
        bower: {
            default: {
                options: {
                    targetDir: 'krympa/static/',
                }
            }
        },
    });

    grunt.registerTask('default', ['coffee', 'less', 'copy', 'bower']);
}
