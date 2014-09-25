<!DOCTYPE html>
<html lang="en">

<head>
        
    <title>{if $kbarticle.title}{$kbarticle.title} - {/if}{$pagetitle} - {$companyname}</title>

	<meta name="author" content="DanThemes" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<meta charset="utf-8" />

	<!-- css files -->
    <link href="templates/{$template}/css/bootstrap.css" rel="stylesheet">
    <link href="templates/{$template}/css/whmcs.css" rel="stylesheet">
    <link href="../css/red.css" rel="stylesheet" title="red" />
    <link href="../css/blue.css" rel="alternate stylesheet" title="blue" />
    <link href="../css/green.css" rel="alternate stylesheet" title="green" />
    <link href="../css/brown.css" rel="alternate stylesheet" title="brown" />
    <link href="../css/purple.css" rel="alternate stylesheet" title="purple" />
    <link href="../css/black.css" rel="alternate stylesheet" title="black" />
    <link href="../css/font-awesome.css" rel="stylesheet" />
    <link href="../css/responsive.css" rel="stylesheet" />
	
	<!-- javascript files -->
	<script src="js/superfish.js"></script>
	<script src="js/main.js"></script>
	<script src="js/responsive-nav.js"></script>

	{if $systemurl}<base href="{$systemurl}" />
    {/if}<script type="text/javascript" src="includes/jscript/jquery.js"></script>
    {if $livehelpjs}{$livehelpjs}
    {/if}

    <script src="templates/{$template}/js/whmcs.js"></script>

    {$headoutput}

	<link href='http://fonts.googleapis.com/css?family=Open+Sans:400,400italic,700,700italic' rel='stylesheet' type='text/css' />
	<link href='http://fonts.googleapis.com/css?family=Ubuntu:400,500,700,400italic,500italic,700italic' rel='stylesheet' type='text/css' />
	
</head>

<body>

	<div class="top_area">
		<div class="wrap">
			<ul class="social">
				<li><a href="#"><i class="icon-twitter-sign"></i></a></li>
				<li><a href="#"><i class="icon-facebook-sign"></i></a></li>
				<li><a href="#"><i class="icon-google-plus-sign"></i></a></li>
				<li><a href="#"><i class="icon-pinterest-sign"></i></a></li>
				<li><a href="#"><i class="icon-tumblr-sign"></i></a></li>
				<li><a href="#"><i class="icon-flickr"></i></a></li>
				<li><a href="#"><i class="icon-linkedin-sign"></i></a></li>
				<li><a href="#"><i class="icon-pinterest-sign"></i></a></li>
			</ul>

			<ul id="top_area_links">
				<li><i class="icon-phone"></i>1.888-888-8888</li>
				<li><i class="icon-envelope"></i><a href="#">support@website.com</a></li>
				<li><i class="icon-headphones"></i><a href="#">Live Chat</a></li>
				<li><i class="icon-comments"></i><a href="#">Send a Ticket</a></li>
			</ul>
		</div>
		<div class="clear"></div>
	</div>

	<header id="top">
		<div class="wrap">
		
			<div id="logo">
				<p><a href="index.html">Hostify</a></p>
			</div>
			
			<a href="#nav" id="toggle"><i class="icon-reorder"></i></a>

			<nav class="nav-collapse" id="nav">
				<ul class="sf-menu">
					<li><a href="index.html">Home<span>homepage</span></a>
						<ul>
							<li><a href="index.html">Home</a></li>
							<li><a href="index-bxslider.html">Home - Bx Slider</a></li>
							<li><a href="index-sequence.html">Home - Sequence</a></li>
							<li><a href="index-unslider.html">Home - Un Slider</a></li>
						</ul>
					</li>
					<li><a class="selected" href="#">Pages<span>all features</span></a>
						<ul>
							<li><a href="column-layouts.html">Column Layouts</a></li>
							<li><a href="full-width.html">Full Width</a></li>
							<li><a href="typography.html">Typography</a></li>
							<li><a class="selected" href="elements.html">Elements</a></li>
							<li><a href="icons.html">Icons</a></li>
							<li><a href="sidebar-left.html">Sidebar Left</a></li>
							<li><a href="sidebar-right.html">Sidebar Right</a></li>
							<li><a href="#">Portfolio</a>
								<ul>
									<li><a href="portfolio-one-column.html">One Column</a></li>
									<li><a href="portfolio-two-columns.html">Two Columns</a></li>
									<li><a href="portfolio-three-columns.html">Three Columns</a></li>
									<li><a href="portfolio-four-columns.html">Four Columns</a></li>
								</ul>
							</li>
							<li><a href="#">Blog</a>
								<ul>
									<li><a href="blog-sidebar-left.html">Blog - Sidebar Left</a></li>
									<li><a href="blog-sidebar-right.html">Blog - Sidebar Right</a></li>
									<li><a href="single-post.html">Single Post</a></li>
								</ul>
							</li>
							<li><a href="404.html">404 - Error Page</a></li>
						</ul>
					</li>
					<li><a href="web-hosting.html">Web Hosting<span>our hosting plans</span></a></li>
					<li><a href="about-us.html">About Us<span>our team</span></a></li>
					<li><a href="contact.html">Contact<span>get in touch</span></a></li>
				</ul><div class="clear"></div>
			</nav>
			
			<div class="clear"></div>

		</div>
	</header>

	<div id="slider_wrapper2">
		<div class="wrap">

			<h1>WHMCS</h1>

		</div>
	</div>

	<div class="clear"></div>

	<div class="content">
		<div class="wrap">


{$headeroutput}

  <div class="navbar navbar-fixed-top">
    <div class="navbar-inner">
      <div class="container">
        <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </a>
        <div class="nav-collapse">
		<ul class="nav">
			<li><a href="{if $loggedin}clientarea{else}index{/if}.php">{$LANG.hometitle}</a></li>
		</ul>
{if $loggedin}
    <ul class="nav">
        <li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">{$LANG.navservices}&nbsp;<b class="caret"></b></a>
          <ul class="dropdown-menu">
            <li><a href="clientarea.php?action=products">{$LANG.clientareanavservices}</a></li>
            {if $condlinks.pmaddon}<li><a href="index.php?m=project_management">{$LANG.clientareaprojects}</a></li>{/if}
            <li class="divider"></li>
            <li><a href="cart.php">{$LANG.navservicesorder}</a></li>
            <li><a href="cart.php?gid=addons">{$LANG.clientareaviewaddons}</a></li>
          </ul>
        </li>
      </ul>


		  <ul class="nav">
			<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">{$LANG.navdomains}&nbsp;<b class="caret"></b></a>
			  <ul class="dropdown-menu">
				<li><a href="clientarea.php?action=domains">{$LANG.clientareanavdomains}</a></li>
				<li class="divider"></li>
				<li><a href="cart.php?gid=renewals">{$LANG.navrenewdomains}</a></li>
				<li><a href="cart.php?a=add&domain=register">{$LANG.navregisterdomain}</a></li>
				<li><a href="cart.php?a=add&domain=transfer">{$LANG.navtransferdomain}</a></li>
				<li class="divider"></li>
				<li><a href="domainchecker.php">{$LANG.navwhoislookup}</a></li>
			  </ul>
			</li>
		  </ul>

		  <ul class="nav">
			<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">{$LANG.navbilling}&nbsp;<b class="caret"></b></a>
			  <ul class="dropdown-menu">
				<li><a href="clientarea.php?action=invoices">{$LANG.invoices}</a></li>
				<li><a href="clientarea.php?action=quotes">{$LANG.quotestitle}</a></li>
				<li class="divider"></li>
				{if $condlinks.addfunds}<li><a href="clientarea.php?action=addfunds">{$LANG.addfunds}</a></li>{/if}
				{if $condlinks.masspay}<li><a href="clientarea.php?action=masspay&all=true">{$LANG.masspaytitle}</a></li>{/if}
				{if $condlinks.updatecc}<li><a href="clientarea.php?action=creditcard">{$LANG.navmanagecc}</a></li>{/if}
			  </ul>
			</li>
		  </ul>

		  <ul class="nav">
			<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">{$LANG.navsupport}&nbsp;<b class="caret"></b></a>
			  <ul class="dropdown-menu">
				<li><a href="supporttickets.php">{$LANG.navtickets}</a></li>
				<li><a href="knowledgebase.php">{$LANG.knowledgebasetitle}</a></li>
				<li><a href="downloads.php">{$LANG.downloadstitle}</a></li>
				<li><a href="serverstatus.php">{$LANG.networkstatustitle}</a></li>
			  </ul>
			</li>
		  </ul>

		  <ul class="nav">
			<li><a href="submitticket.php">{$LANG.navopenticket}</a></li>
		  </ul>

		  <ul class="nav">
            <li><a href="affiliates.php">{$LANG.affiliatestitle}</a></li>
		  </ul>

		  <ul class="nav pull-right">
			<li class="dropdown">
			  <a href="#" class="dropdown-toggle" data-toggle="dropdown">{$LANG.hello}, {$loggedinuser.firstname}!&nbsp;<b class="caret"></b></a>
			  <ul class="dropdown-menu">
				<li><a href="clientarea.php?action=details">{$LANG.editaccountdetails}</a></li>
				{if $condlinks.updatecc}<li><a href="clientarea.php?action=creditcard">{$LANG.navmanagecc}</a></li>{/if}
				<li><a href="clientarea.php?action=contacts">{$LANG.clientareanavcontacts}</a></li>
				{if $condlinks.addfunds}<li><a href="clientarea.php?action=addfunds">{$LANG.addfunds}</a></li>{/if}
				<li><a href="clientarea.php?action=emails">{$LANG.navemailssent}</a></li>
				<li><a href="clientarea.php?action=changepw">{$LANG.clientareanavchangepw}</a></li>
				<li class="divider"></li>
				<li><a href="logout.php">{$LANG.logouttitle}</a></li>
			  </ul>
			</li>
		  </ul>
{else}
		  <ul class="nav">
			<li><a href="announcements.php">{$LANG.announcementstitle}</a></li>
		  </ul>
          
		  <ul class="nav">
			<li><a href="knowledgebase.php">{$LANG.knowledgebasetitle}</a></li>
		  </ul>
          
		  <ul class="nav">
			<li><a href="serverstatus.php">{$LANG.networkstatustitle}</a></li>
		  </ul>
          
		  <ul class="nav">
			<li><a href="affiliates.php">{$LANG.affiliatestitle}</a></li>
		  </ul>
          
		  <ul class="nav">
			<li><a href="contact.php">{$LANG.contactus}</a></li>
		  </ul>

		  <ul class="nav pull-right">
			<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">{$LANG.account}&nbsp;<b class="caret"></b></a>
			  <ul class="dropdown-menu">
				<li><a href="clientarea.php">{$LANG.login}</a></li>
				<li><a href="register.php">{$LANG.register}</a></li>
				<li class="divider"></li>
				<li><a href="pwreset.php">{$LANG.forgotpw}</a></li>
			  </ul>
			</li>
		  </ul>
{/if}

        </div><!-- /.nav-collapse -->
      </div>
    </div><!-- /navbar-inner -->
  </div><!-- /navbar -->


<div class="whmcscontainer">
    <div class="contentpadded">

{if $pagetitle eq $LANG.carttitle}<div id="whmcsorderfrm">{/if}

