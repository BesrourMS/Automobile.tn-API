<?php header('Access-Control-Allow-Origin: *'); ?>
<?php
	require_once('simpledom.php');
	$html = new simple_html_dom();
	$page = new simple_html_dom();
		
	$page->load_file('https://www.automobile.tn/fr/neuf/recherche');
	$t = $page->find('//*[@id="facets"]/fieldset/div[1]/button');
	$total = trim(strip_tags($t[0]->innertext));
	$count = explode(" ",$total);
	$limit = 0;
	foreach($page->find('//*[@id="w0"]/div[4]/*') as $a) { $limit++; }
	($count[1] % $limit) != 0 ? $pager = intdiv($count[1], $limit) + 1 : $pager = intdiv($count[1], $limit);
	$page->clear(); 
	unset($page);
	$j = 1;
	while($j <= $pager) {
		//$html->load_file('https://www.sayarti.tn/prix-des-voitures/page/'.$j.'/?view_type=list&sort_order=price_low');
		$html->load_file('https://www.automobile.tn/fr/neuf/recherche/s=sort%21price?sort=price&page='.$j);
		$i= 1;
		while($i <= $limit) {
			$id = $html->find('//*[@id="w0"]/div[4]/span['.$i.']');
			$v = $html->find('//*[@id="w0"]/div[4]/span['.$i.']/div/a/h2');
			$x = $html->find('//*[@id="w0"]/div[4]/span['.$i.']/div/a/div/span');
			$img = $html->find('//*[@id="w0"]/div[4]/span['.$i.']/div/a/img');
			$l = $html->find('//*[@id="w0"]/div[4]/span['.$i.']/div/a');
				
			$d = trim(strip_tags($id[0]->attr["data-key"]));
			$voiture = trim(strip_tags($v[0]->innertext));
			$prix = trim(strip_tags($x[0]->innertext));
			$lien = trim(strip_tags($l[0]->href));
			$logo = trim(strip_tags($img[0]->src));
				
			$arrayclassement[] = array(
				'ID' => $d,
				'Voiture' => $voiture,
				'Image' => $logo,
				'Prix' =>  $prix,
				'Lien' => 'https://www.automobile.tn'.$lien,
			);
			$i++;
		}
		$j++;
	}
	array_splice($arrayclassement, $count[1]);
	$html->clear(); 
	unset($html);
	header("Content-type: application/json; charset=utf-8");
	header('X-Total-Pages: '.$pager);
	header('X-Total-Cars: '.$count[1]);
	header('X-Powered-By: Mohamed Safouan Besrour');
	print_r(json_encode($arrayclassement));	
?>