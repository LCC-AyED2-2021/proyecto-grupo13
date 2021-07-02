slides.pdf: slides.md title.png logo-small.png load.png
	pandoc -t beamer $< -o $@

title.png: title.jpg
	convert -units PixelsPerInch title.jpg -resample 300 -resize 40% title.png

logo-small.png: logo.jpg
	convert -units PixelsPerInch logo.jpg -resample 300 -resize 25% $@

load.png: ../hash_load.py
	python ../hash_load.py | gnuplot -p -e "set terminal png size 400,200; set output 'load.png';  set xlabel 'Cell' ; set ylabel 'Count'; set arrow from 0,23 to 547,23 nohead lc 2 lw 4; plot '<cat' with boxes notitle;"
