slides.pdf: slides.md title.png logo-small.png
	pandoc -t beamer $< -o $@

title.png: title.jpg
	convert -units PixelsPerInch title.jpg -resample 300 -resize 40% title.png

logo-small.png: logo.jpg
	convert -units PixelsPerInch logo.jpg -resample 300 -resize 25% $@
