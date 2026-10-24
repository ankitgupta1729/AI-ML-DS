<!DOCTYPE html>
    <html lang="en">
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" >
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PY4E - Python for Everybody</title>
<script>
 var _TSUGI = {
            ajax_session: false,
heartbeat: 1500000,
heartbeat_url: "https://www.py4e.com/tsugi/util/heartbeat",
rest_path: {"parent":"","base_url":"https:\/\/www.py4e.com","controller":"","extra":"","action":false,"parameters":[],"current":"","full":""},
spinnerUrl: "https://static.tsugi.org/img/spinner.gif",
staticroot: "https://static.tsugi.org",
apphome: "https://www.py4e.com",
wwwroot: "https://www.py4e.com/tsugi",
websocket_url: false,
websocket_token: false,
react_token: "k4in1mk78tfbfd8tbmjr7cd8am",
window_close_message: "Application complete - You can close this tab.",
session_expire_message: "Your session has expired"

}
</script>
        <!-- Tiny bit of JS -->
        <script src="https://static.tsugi.org/js/tsugiscripts_head.js"></script>
        <!-- Le styles -->
        <link href="https://static.tsugi.org/bootstrap-3.4.1/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://static.tsugi.org/js/jquery-ui-1.11.4/jquery-ui.min.css" rel="stylesheet">
                <link href="https://static.tsugi.org/fontawesome-free-5.8.2-web/css/all.css" rel="stylesheet">
        <link href="https://static.tsugi.org/fontawesome-free-5.8.2-web/css/v4-shims.css" rel="stylesheet">
        <style>:root {--primary:#0D47A1;
--primary-menu:#0D47A1;
--primary-border:#0d4295;
--primary-darker:#0c4091;
--primary-darkest:#0b3b85;
--background-color:#FFFFFF;
--background-focus:#F5F5F5;
--background-accent:#0D47A1;
--secondary:#EEEEEE;
--secondary-menu:#EEEEEE;
--text:#111111;
--text-light:#5E5E5E;
--font-family:sans-serif;
--font-size:14px;
}</style>
          <link href="https://static.tsugi.org/css/tsugi2.css" rel="stylesheet">

          <style>
                        </style>

        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
          <script src="https://www.py4e.com/tsugi/vendor/tsugi/lib/static/js/html5shiv/html5shiv.js"></script>
          <script src="https://www.py4e.com/tsugi/vendor/tsugi/lib/static/js/respond/respond.min.js"></script>
        <![endif]-->

    <script type="text/javascript">CSRF_TOKEN = "TODORemoveThis";</script>
<style>
body {
    font-family: var(--font-family);
    font-size: 1.2rem;
    line-height: 1.93rem;
    color: var(--text);
    background-color: var(--background-color);
}
</style>
</head>
<body prefix="oer: http://oerschema.org">
<div id="body_container">
<script>
if (window!=window.top) {
    document.getElementById("body_container").className = "container-fluid";
} else {
    document.getElementById("body_container").className = "container";
}
</script>
<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation" id="tsugi_main_nav_bar" style="display:none">  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="https://www.py4e.com">PY4E</a>
    </div>
    <div class="navbar-collapse collapse">
      <ul class="nav navbar-nav navbar-main">
        <li><a href="https://www.py4e.com/lessons" >Lessons</a></li>
        <li><a href="https://www.py4e.com/discussions" >Discussions</a></li>
        <li><a href="https://www.py4e.com/materials" >OER</a></li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        <li><a href="https://online.dr-chuck.com" target="_blank" >Instructor</a></li>
        <li><a href="https://www.py4e.com/book" >Book</a></li>
        <li><a href="https://www.py4e.com/login" >Login</a></li>
      </ul>
    </div> <!--/.nav-collapse -->
  </div> <!--container -->
</nav>
<script>
if ( ! inIframe() ) {
  document.getElementById('tsugi_main_nav_bar').style.display = 'block';
  document.getElementsByTagName('body')[0].style.paddingTop = '5.93rem';
} else {
  document.getElementsByTagName('body')[0].style.paddingTop = '1.0rem';
}
</script>
<div id="flashmessages"></div><div id="container">
<div style="margin-left: 10px; float:right">
<iframe width="400" height="225" src="https://www.youtube.com/embed/UjeNA_JtXME?rel=0" frameborder="0" allowfullscreen></iframe>
</div>
<h1>Python for Everybody</h1>
<p>
This web site is building a set of free 
<a href="lessons">materials</a>, 
<a href="https://www.youtube.com/watch?v=UjeNA_JtXME&list=PLlRFEj9H3Oj7Bp8-DfGpfAfDBiblRfl5p&index=1" target="_blank">lectures</a>, 
<a href="book.php">book</a>
and assignments to help students
learn how to program in Python.
You can take this course and receive a certificate at:
<ul>
<li><a href="https://www.coursera.org/specializations/python" target="_blank">Coursera: Python for Everybody Specialization</a> </li>
<li><a href="https://www.edx.org/bio/charles-severance" target="_blank">edX: Python for Everybody</a></li>
<!--
<li><a href="https://www.futurelearn.com/courses/programming-for-everybody-python" target="_blank">FutureLearn: Programming for Everybody (Getting Started with Python)</a></li>
-->
<li><a href="https://www.youtube.com/watch?v=8DvywoWv6fI" target="_blank">FreeCodeCamp</a></li>
<li><a href="https://online.umich.edu/series/python-for-everybody/" target="_blank">Free certificates for University of Michigan students and staff</a></li>
</ul>
<p>
If you <a href="tsugi/login.php">log in</a> to this site
you have joined a free, global
open and online course.  You have a grade book, autograded assignments, discussion forums, and can earn
badges for your efforts.</p>
<p>
We take your privacy seriously on this site, you can review our
<a href="privacy">Privacy Policy</a> for more details.
</p>
<p>
If you want to use these materials
in your own classes you can download or link to the artifacts on this site,
<a href="tsugi/cc/">export the course material</a> as an
IMS Common Cartridge®, or apply for
an IMS Learning Tools Interoperability® (LTI®)
<a href="tsugi/admin/key/index.php">key and secret</a>
 to launch the autograders from your LMS.
</p>
<p>
The code for this site including the autograders, slides, and course content is all available on
<a href="https://github.com/csev/py4e" target="_blank">GitHub</a>.  That means you could make your own
copy of the course site, publish it and remix it any way you like.  Even more exciting, you could translate
the entire site (course) into your own language and publish it.  I have provided
some <a href="https://github.com/csev/py4e/blob/master/TRANSLATION.md" target="_new">
instructions on how to translate this course</a> in my GitHub repository.
</p>
This site uses <a href="http://www.tsugi.org" target="_blank">Tsugi</a>
framework to embed a learning management system into this site and
provide the autograders.
If you are interested in collaborating
to build these kinds of sites for yourself, please see the
<a href="http://www.tsugi.org" target="_blank">tsugi.org</a> website and/or
contact me.
</p>
<p>
And yes, Dr. Chuck actually has a race car - it is called the
<a href="https://www.sakaiger.com/sakaicar/" target=_blank">SakaiCar</a>.
He races in a series called
<a href="https://www.24hoursoflemons.com" target="_blank">24 Hours of Lemons</a>.
</p>
<!--
array(4) {
  ["LAST_ACTIVITY"]=>
  int(1713709404)
  ["HEARTBEAT_COUNT"]=>
  int(0)
  ["tsugi_theme"]=>
  array(14) {
    ["primary"]=>
    string(7) "#0D47A1"
    ["primary-menu"]=>
    string(7) "#0D47A1"
    ["primary-border"]=>
    string(7) "#0d4295"
    ["primary-darker"]=>
    string(7) "#0c4091"
    ["primary-darkest"]=>
    string(7) "#0b3b85"
    ["background-color"]=>
    string(7) "#FFFFFF"
    ["background-focus"]=>
    string(7) "#F5F5F5"
    ["background-accent"]=>
    string(7) "#0D47A1"
    ["secondary"]=>
    string(7) "#EEEEEE"
    ["secondary-menu"]=>
    string(7) "#EEEEEE"
    ["text"]=>
    string(7) "#111111"
    ["text-light"]=>
    string(7) "#5E5E5E"
    ["font-family"]=>
    string(10) "sans-serif"
    ["font-size"]=>
    string(4) "14px"
  }
  ["tsugi_top_nav_https://www.py4e.com/tsugi"]=>
  string(523) "{"home":{"link":"PY4E","href":"https:\/\/www.py4e.com","attr":false},"left":[{"link":"Lessons","href":"https:\/\/www.py4e.com\/lessons","attr":false},{"link":"Discussions","href":"https:\/\/www.py4e.com\/discussions","attr":false},{"link":"OER","href":"https:\/\/www.py4e.com\/materials","attr":false}],"right":[{"link":"Instructor","href":"https:\/\/online.dr-chuck.com","attr":false},{"link":"Book","href":"https:\/\/www.py4e.com\/book","attr":false},{"link":"Login","href":"https:\/\/www.py4e.com\/login","attr":false}]}"
}
NULL
-->
</div>
<script src="https://static.tsugi.org/js/jquery-1.11.3.js"></script>
<script src="https://static.tsugi.org/bootstrap-3.4.1/js/bootstrap.min.js"></script>
<script src="https://static.tsugi.org/js/jquery-ui-1.11.4/jquery-ui.min.js"></script>
<script src="https://static.tsugi.org/js/jquery.timeago-1.6.3.js"></script>
<script src="https://static.tsugi.org/js/handlebars-v4.0.2.js"></script>
<script src="https://static.tsugi.org/tmpljs-3.8.0/tmpl.min.js"></script>
<script src="https://static.tsugi.org/js/tsugiscripts.js"></script>
<script type="text/javascript">
    HEARTBEAT_TIMEOUT = setTimeout(doHeartBeat, _TSUGI.heartbeat);
    tsugiEmbedMenu();
    $(document).ready(function() { jQuery("time.timeago").timeago(); });
</script>
<script>
$('a').each(function (x) {
    var href = $(this).attr('href');
    if ( ! href ) return;
    if ( ! href.startsWith('#') ) return;
    var pos = href.indexOf('/?');
    if ( pos < 1 ) return;
    // console.dir('Patching broken # href='+href);
    href = href.substring(0,pos);
    $(this).attr('href', href);
});

</script>

</div></body>
</html>
