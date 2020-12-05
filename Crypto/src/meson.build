project('des', 'c', default_options:['c_std=c11'])
sources = ['crack.c']
ssl = dependency('openssl')
omp = dependency('openmp')
executable('crack', sources, dependencies:[ssl, omp])
executable('enc', 'enc.c', dependencies:[ssl, omp])
