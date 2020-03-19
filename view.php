<html>
<head>
<?php $y = $_COOKIE["y"];?>
<title>view</title>
</head>
<body>

<?php
print "<body onScroll=\"document.cookie='y=' + window.pageYOffset\" onLoad='window.scrollTo(0,$y)'>";
?>

<h2>
Plot confirmed cases by the number of days passing 100 cases in each country. China and Itatly are used as benchmark.
</h2>
<p>Data source: https://github.com/CSSEGISandData/COVID-19</p>
<p>The data is normally delayed by 1 day</p>


<?PHP
#$imgs = glob(sprintf('images/*.png'))
#$num_of_imgs = count($imgs)
#echo $imgs
#echo $num_of_imgs
$num_of_imgs = 100;
for ($i = 1; $i <= $num_of_imgs; ++$i) {
    if (file_exists(sprintf('images/%d.png', $i))) {
        printf("<img src=\"images/%d.png\"/> </a>\n\n", $i);
    }
    else {
        break;
    }
}
#
?>

</body>
</html>

