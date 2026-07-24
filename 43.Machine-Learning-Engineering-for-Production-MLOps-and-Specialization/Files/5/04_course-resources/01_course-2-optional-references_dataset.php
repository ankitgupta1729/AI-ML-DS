<!DOCTYPE html>
<!--[if IE 8]><html class="no-js lt-ie9" lang="en" > <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en" > <!--<![endif]-->

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">    <title>WISDM Lab: Dataset</title>
     <link rel="stylesheet" href="includes/css/foundation.css">
    <link rel="stylesheet" href="includes/css/wisdm.css">
	<script src="includes/js/vendor/custom.modernizr.js"></script></head>
<body id="purple">
    <!-- Header and Nav -->
    <header>        
    <div class="sticky">
    <nav class="top-bar">
        <ul class="title-area">
            <!-- Title Area -->
            <li class="name"><a href="index.php">WISDM<span class="show-for-medium-up">: WIreless Sensor Data Mining</span></a></li>
            <li class="toggle-topbar menu-icon"><a href="#"><span>Menu</span></a></li>
        </ul>
    
        <section class="top-bar-section">
        <!-- Right Nav Section -->
        <ul class="main-nav right">
            <li><a href="index.php">Home</a></li>
            <li class="has-dropdown"><a href="about.php">About</a>
                <ul class="dropdown">
                    <li><a href="about.php">Overview</a></li>
                    <li><a href="publications.php">Publications</a></li>
                    <li><a href="funding.php">Funding</a></li>
                    <li><a href="equipment.php">Equipment</a></li>
                    <li><a href="news.php">News</a></li>
                </ul>
            </li>
            <li><a href="dataset.php">Datasets</a>
            </li>
            <li class="has-dropdown"><a href="resources.php">Resources</a>
                <ul class="dropdown">
                    <li><a href="resources.php">Dev Tools</a></li>
                    <li><a href="relatedwork.php">Related Work</a></li>
                    <li><a href="relatedapplications.php">Related Applications</a></li>
                    <li><a href="conferences.php">Conferences</a></li>
                </ul>
            </li>
            <li><a href="members.php">Members</a></li>
        </ul>
        </section>
    </nav>
    </div>
     
    
        <div class="row  hide-for-small" id="page-banner">
        	<div id="title-box"><h1 class="page-title" id="dataset">Dataset</h1></div>
    	</div>
        <div class="row hide-for-medium-up">
        	<div class="large-12 small-12 columns text-center"><h1 class="page-title" id="dataset">Dataset</h1></div>
		</div>
	 </header>
    <!-- End Header and Nav -->
    
    <div class="row">
    <div class="large-12 columns">
    	<div class="section-container vertical-tabs" data-section="vertical-tabs" data-options:"deep_linking: true">
        	<section class="active">
            <p class="title" data-section-title><a href="#activityprediction">Activity Prediction</a></p>
				<div class="content" data-slug="activityprediction" data-section-content>
                	<div class="row">
                    <div class="large-6 small-12 columns">
                    	<h6>Last Updated: Dec. 2, 2012</h6>
                        <p class="dataset-text">
                        This dataset contains data collected through controlled, laboratory conditions. If you are interested in "real world" data, please consider our <a href="#actitracker">Actitracker Dataset</a>.<br /><br />
                        The data in this file corresponds with the data used in the following paper:<br />
                        <blockquote>
                        Jennifer R. Kwapisz, Gary M. Weiss and Samuel A. Moore (2010).
                        Activity Recognition using Cell Phone Accelerometers, 
                        <i>Proceedings of the Fourth International Workshop on Knowledge
                        Discovery from Sensor Data (at KDD-10)</i>, Washington DC. 
                        <a href="includes/files/sensorKDD-2010.pdf">[PDF]</a>
						</blockquote>
                        <p class="dataset-text">
                        When using this dataset, we request that you cite this paper. <br />
                        You may also want to cite our other relevant articles,
                        which can be found <a href="publications.php">here</a>.
                        <br /><br />
                        When sharing or redistributing this dataset, we request that the readme.txt file is always included. 
                        
                        <h3>Statistics</h3>
                        <ul class="dataset-text">
                        	<li><h6>Raw Time Series Data</h6>
                        	<ul>
                            	<li>Number of examples: 1,098,207</li>
                        		<li>Number of attributes: 6</li>
                        		<li>Missing attribute values: None</li>
                        		<li>Class Distribution
                        		<ul>
                                	<li>Walking: 424,400 (38.6%)</li>
                        			<li>Jogging: 342,177 (31.2%)</li>
                        			<li>Upstairs: 122,869 (11.2%)</li>
                        			<li>Downstairs: 100,427 (9.1%)</li>
                        			<li>Sitting: 59,939 (5.5%)</li>
                        			<li>Standing: 48,395 (4.4%)</li>
                        		</ul>
                                </li>
							</ul>
                            </li>
                            <li><h6>Transformed Examples</h6>
                        	<ul>
                            	<li>Number of transformed examples: 5,424</li>
                        		<li>Number of transformed attributes: 46</li>
                        		<li>Missing attribute values: None</li>
                        		<li>Class Distribution
                        		<ul>
                                	<li>Walking: 2,082 (38.4%)</li>
                        			<li>Jogging: 1,626 (30.0%)</li>
                        			<li>Upstairs: 633 (11.7%)</li>
                        			<li>Downstairs: 529 (9.8%)</li>
                        			<li>Sitting: 307 (5.7%)</li>
                        			<li>Standing: 247 (4.6%)</li>
								</ul>
                                </li>
							</ul>
                            </li>
						</ul>
					</p>
                    </div>
                    
                    <div class="large-6 small-12 columns">
                    <a href="includes/datasets/latest/WISDM_ar_latest.tar.gz" class="button radius">Download Latest Version</a><br />
                    
                    <ul class="dataset-text">
                    	<li><h6>Changelog:</h6>
                            <ul>
                                <li><a href="includes/dataset/latest/WISDM_ar_v1.1.tar.gz">(v1.1)</a>
								<ul>
                                	<li>about files updated with summary information</li>
                        			<li>file naming convention updated to include version numbers</li>
                        			<li>readme.txt updated to include relevant papers</li>
                        			<li>WISDM_ar_v1.1_trans_about.txt updated with citation to paper describing the attributes.</li>
								</ul>
                        		</li>
                                <li>(v1.0)
                                <ul>
                                	<li>user names masked with ID numbers 1-36</li>
									<li>dataset initialized</li>
								</ul>
                                </li>
							</ul>
                            </li>
                            <br />
                        	<li><h6>Files:</h6>
								<ul>
                                	<li>readme.txt</li>
                        			<li>WISDM_ar_v1.1_raw_about.txt</li>
                        			<li>WISDM_ar_v1.1_trans_about.txt</li>
                        			<li>WISDM_ar_v1.1_raw.txt</li>
                        			<li>WISDM_ar_v1.1_transformed.arff</li>
                        		</ul>
                            </li>
						</ul>
						
                    </div> <!-- END INNER COLUMNS -->
				</div> <!-- END INNER ROW -->
                </div> <!-- END TAB CONTENT -->
            </section>
            
            <section>
            <p class="title" data-section-title><a href="#actitracker">Actitracker</a></p>
                <div class="content" data-slug="actitracker" data-section-content>
                	<div class="row">
                    <div class="large-6 small-12 columns">
                    	<h6>Last Updated: Oct. 22, 2013</h6>
                        <p class="dataset-text">
						This dataset contains "real world" data. If you are interested in controlled testing data, please consider our <a href="#activityprediction">Actitivty Prediction Dataset</a>.<br /><br />
                        
                        This data has been released by the Wireless Sensor Data Mining  			
                        (WISDM) Lab. <http://www.cis.fordham.edu/wisdm/>

                        The data in this set were collected with our Actitracker system,
                        which is available online for free at <http://actitracker.com>
                        and in the Google Play store.  The system is described in the 
                        following paper: <br />
                        <blockquote>
                        Jeffrey W. Lockhart, Gary M. Weiss, Jack C. Xue, Shaun T. Gallagher, 
						Andrew B. Grosner, and Tony T. Pulickal (2011). "Design Considerations
						for the WISDM Smart Phone-Based Sensor Mining Architecture," <i>Proceedings 
						of the Fifth International Workshop on Knowledge Discovery from Sensor 
						Data (at KDD-11)</i>, San Diego, CA.  
                        <a href="includes/files/Lockhart-Design-SensorKDD11.pdf">[PDF]</a>
						</blockquote>
                        <p class="dataset-text">
                        When using this dataset, we request that you cite this paper. <br />
                        You may also want to cite our other relevant articles,
                        which can be found <a href="publications.php">here</a>, specifically:<br />
                        <blockquote>
                        Gary M. Weiss and Jeffrey W. Lockhart (2012). "The Impact of
                        Personalization on Smartphone-Based Activity Recognition,"
                        Proceedings of the AAAI-12 Workshop on Activity Context
                        Representation: Techniques and Languages, Toronto, CA.
                		<br /><br />
                		Jennifer R. Kwapisz, Gary M. Weiss and Samuel A. Moore (2010).
                     	"Activity Recognition using Cell Phone Accelerometers,"
                        Proceedings of the Fourth International Workshop on
                        Knowledge Discovery from Sensor Data (at KDD-10), Washington
                        DC.</blockquote>
                        <br />
                        When sharing or redistributing this dataset, we request that the 
                        readme.txt file is always included. 
					</p>
                        <h3>Statistics</h3>
                        <ul class="dataset-text">
                        	<li><h6>Demographics</h6></li>
                            <ul>
                            	<li>Number of examples: 563</li>
                                <li>Number of attributes: 6</li>
                                <li>Missing attribute values: No</li>
                            </ul>
                            <li><h6>Raw Data</h6></li>
                             <ul>
                            	<li>Number of examples: 2,980,765</li>
                                <li>Number of attributes: 6</li>
                                <li>Missing attribute values: No</li>
                                <li>Class Distribution:</li>
                                <ul>
                                	<li>Walking: 1,255,923 (42.1%)</li>
                                    <li>Jogging: 438,871 (14.7%)</li>
                                    <li>Stairs: 57,425 (1.9%)</li>
                                    <li>Sitting: 663,706 (22.3%)</li>
                                    <li>Standing: 288,873 (9.7%)</li>
                                    <li>Lying Down: 275,967 (9.3%)</li>
                                </ul>
                            </ul>
                             <li><h6>Raw Data (Unlabeled)</h6></li>
                            <ul>
                            	<li>Number of examples: 38,209,772</li>
                                <li>Number of attributes: 6</li>
                                <li>Missing attribute values: No</li>
                            </ul>
                            <li><h6>Transformed Data</h6></li>
                             <ul>
                            	<li>Number of examples: 5435</li>
                                <li>Number of attributes: 46</li>
                                <li>Missing attribute values: No</li>
                                <li>Class Distribution:</li>
                                <ul>
                                	<li>Walking: 2,185 (40.2%)</li>
                                    <li>Jogging: 130 (2.4%)</li>
                                    <li>Stairs:  251 (4.6%)</li>
                                    <li>Sitting: 1,410 (25.9%)</li>
                                    <li>Standing: 840 (15.5%)</li>
                                    <li>Lying Down: 619 (11.4%)</li>
                                </ul>
                            </ul>
                            <li><h6>Transformed Data (Unlabeled)</h6></li>
                            <ul>
                            	<li>Number of examples: 1,369,349</li>
                                <li>Number of attributes: 46</li>
                                <li>Missing attribute values: No</li>
                                <li>Class Distribution:</li>
                                <ul>
                                	<li>Walking: 281,169 (20.5%)</li>
                                    <li>Jogging: 2,130 (0.2%)</li>
                                    <li>Stairs:  31,268 (2.3%)</li>
                                    <li>Sitting: 655,362 (47.9%)</li>
                                    <li>Standing: 158,457 (11.6%)</li>
                                    <li>Lying Down: 240,963 (17.6%)</li>
                                </ul>                            
                            </ul>
                                                                                                                                         
                        </ul>                    
                    </div>
                    
                    <div class="large-6 small-12 columns">
                    <a href="includes/datasets/latest/WISDM_at_latest.tar.gz" class="button radius">Download Latest Version</a><br />
                    	<ul class="dataset-text">
                            <li><h6>Changelog:</h6>
                            <ul>
                                <li><a href="includes/dataset/latest/WISDM_at_v2.0.tar.gz">(v2.0)</a>
								<ul>
                                	<li>activity label predictions added to unlabeled_transformed</li>
								</ul>
                        		</li>
							</ul>
                            </li>
                            <br />
                        	<li><h6>Files:</h6>
								<ul>
                                	<li>readme.txt</li>
                                    <li>WISDM_at_v2.0_raw_about.txt
									<ul>
                                    	<li>WISDM_at_v2.0_transformed_about.arff</li>
                                        <li>WISDM_at_v2.0_unlabeled_raw_about.txt</li>
                                        <li>WISDM_at_v2.0_unlabeled_transformed_about.arff</li>
									</ul>
                                    </li>
                                    <li>WISDM_at_v2.0_demographics_about.txt</li>
                                    <li>WISDM_at_v2.0_raw.txt</li>
                                    <li>WISDM_at_v2.0_transformed.arff</li>
                                    <li>WISDM_at_v2.0_unlabeled_raw.txt</li>
                                    <li>WISDM_at_v2.0_unlabeled_transformed.arff</li>
                                    <li>WISDM_at_v2.0_demographics.txt</li>
                        		</ul>
                            </li>
                            <br /><br />
                            Both labeled and unlabeled data are contained in this dataset.

                            Labeled data is from when the user trained Actitracker with "Training Mode" 
                            The user physically specifies which activity is being performed.
                            In both the raw and transformed files for labeled data, the 
                            activity label is determined by the user's input.
                        
                            Unlabeled data is from when the user was running Actitracker for 
                            regular use.  The user does not specify which activity is being performed.
                            In the unlabeled raw data file, the activity label is "NoLabel" 
                            In the unlabeled transformed file, the activity label is the activity
                            that our system predicted the user to be performing.
						</ul>
                    </div>
				</div> <!-- END ROW -->
                </div> <!-- END TAB CONTENT -->
            </section>
          <section>
            <p class="title" data-section-title><a href="#datatransformation">Dataset Transformation Process</a></p>
				<div class="content" data-slug="datatransformation" data-section-content>
                	<div class="row">
                    <div class="large-6 small-12 columns">
                    	<h6>Last Updated: Jul. 14, 2014</h6>
                        <p class="dataset-text">
 						The data transformation process in this file corresponds with the one used in the
						following paper:<br /><br />
                        <blockquote>
                        Jeffrey W. Lockhart, Gary M. Weiss, Jack C. Xue, Shaun T. Gallagher,
                        Andrew B. Grosner, and Tony T. Pulickal (2011). "Design Considerations
                        for the WISDM Smart Phone-Based Sensor Mining Architecture," Proceedings
                        of the Fifth International Workshop on Knowledge Discovery from Sensor
                        Data (at KDD-11), San Diego, CA. <a href="http://www.cis.fordham.edu/wisdm/public_files/Lockhart-Design-SensorKDD11.pdf">[PDF]</a>
						</blockquote>
                        <p class="dataset-text">
                        When using this dataset, we request that you cite this paper. <br />
 						You may also want to cite our other relevant articles, which can be found <a href="http://www.cis.fordham.edu/wisdm/publications.php">here.</a><br /><br />
                        </p>
                        <blockquote>
                        Gary M. Weiss and Jeffrey W. Lockhart (2012). "The Impact of
                               Personalization on Smartphone-Based Activity Recognition,"
                               Proceedings of the AAAI-12 Workshop on Activity Context
                               Representation: Techniques and Languages, Toronto, CA.
                        </blockquote>
                        <br />
			<p class="dataset-text">
                        <blockquote>
                        Jennifer R. Kwapisz, Gary M. Weiss and Samuel A. Moore (2010).
                               "Activity Recognition using Cell Phone Accelerometers,"
                               Proceedings of the Fourth International Workshop on
                               Knowledge Discovery from Sensor Data (at KDD-10), Washington
                               DC.
                        </blockquote></p>
                        <br />
                        <p class="dataset-text">
                        These files enact the data transfromation process where files of raw accelerometer
                        data are converted to Attribute-Relation File Format (ARFF files) for use with WEKA 
                        machine learning software.<br /><br />
                   		standalone_public_v1.0.jar is called with two arguments, a filepath to the input file 
                        (i.e. raw data file to read) and a filepath to the output file (i.e. arff file to be 
                        written to)<br /><br />
                        The source code for standalone_public_v1.0.jar is also provided with:<br /> 
                        StandAloneFeat.java<br />
                        TupFeat.java<br />
                        FeatureLib.java<br /><br />
                        Descriptions of the features produced by this process can be found in the literature 
                        mentioned above as well as the about files for the transformed data of our published 
                        datasets.<br /><br />
                        For our transformation process, we take 10 seconds worth of
                        accelerometer samples (200 records/lines in the raw file)
                        and transform them into a single example/tuple of 46 values.
                        Most of the features we generate are simple statistical
                        measures.<br /><br />
                        Things to note:<br />
                        An error concerning the number of tuples saved was recently found and corrected 
                        in the source code, so this particular version of the JAR file is not the same 
                        one used to create the transformed data from the raw data that is currently 
                        published on our site.<br /><br />
                        During the transformation process, only the first character of the activity label 
                        from the raw data files are used when creating the arff files.  Because some of 
                        our activities begin with the same letter (i.e. Stairs, Standing, Sitting) if these 
                        labels are present in the raw files and the JAR file is called, one cannot distinguish
                        between the activites in the arff files because theu activity label will be the same 
                        for multiple activites.  WISDM uses a single-character labeling system to represent 
                        the activities we recognize, and simple perl scipts are called when it is necessary 
                        to translate between the full activity label and our single character system.<br/><br />                        
                        Walking   - A<br />
                        Jogging   - B<br />
                        Stairs    - C<br />
                        Sitting   - D<br />
                        Standing  - E<br />
                        LyingDown - F<br />
                        NoLabel   - G<br /></p>
                    </div>
                    
                    <div class="large-6 small-12 columns">
                    <a href="includes/datasets/WISDM_transformation_v1.0.tar.gz" class="button radius">Download Latest Version</a><br />
                    
                    <ul class="dataset-text">
                        	<li><h6>Files:</h6>
								<ul>
                                	<li>readme.txt</li>
                        			<li>FeatureLib.java</li>
                        			<li>StandAloneFeat.java</li>
                        			<li>TupFeat.java</li>
                        			<li>standalone_public_v1.0.jar</li>
                        		</ul>
                            </li>
						</ul>
						
                    </div> <!-- END INNER COLUMNS -->
				</div> <!-- END INNER ROW -->
                </div> <!-- END TAB CONTENT -->
            </section>
		</div>
	</div>
	</div>
<!-- Footer -->
<footer class="row">
<div class="large-12 columns">
    <hr />
    <div class="row">
        <div class="large-6 columns">
            <p>&copy;2013 WISDM Lab, All Rights Reserved<br />Department of Computer & Information Science, Fordham University, Bronx, NY</p>
        </div>
        <div class="large-6 columns">
        <div class="row">
        	<div class="large-12 columns">
                <ul class="inline-list right" id="footer-nav">
                    <li><a href="index.php">Home</a></li>
                    <li><a href="about.php">About</a></li>
                    <li><a href="dataset.php">Dataset</a></li>
                    <li><a href="resources.php">Resources</a></li>
                    <li><a href="members.php">Members</a></li>
                </ul>
			</div>
		</div>
        <div class="row">
        	<div class="large-12 columns text-right">
				<ul class="inline-list right">
                	<li><a href="https://www.facebook.com/actitracker">Facebook</a></li>
                	<li><a href="http://www.twitter.com/actitracker">Twitter</a></li>
                	<li><a href="http://www.linkedin.com/company/wisdm-lab/actitracker-20111091/product">LinkedIn</a></li>
                	<li><a href="https://plus.google.com/105766712847037079253">Google+</a></li>
                </ul>
            </div>
        </div>
        </div>
    </div>
</div>
</footer>

  <script>
  document.write('<script src=' +
  ('__proto__' in {} ? 'includes/js/vendor/zepto' : 'includes/js/vendor/jquery') +
  '.js><\/script>')
  </script>
  
  <!--<script src="includes/js/foundation.min.js"></script> -->
  
  <script src="includes/js/foundation/foundation.js"></script>
  <script src="includes/js/foundation/foundation.interchange.js"></script>
  <script src="includes/js/foundation/foundation.abide.js"></script>
  <script src="includes/js/foundation/foundation.dropdown.js"></script>
  <script src="includes/js/foundation/foundation.placeholder.js"></script>
  <script src="includes/js/foundation/foundation.forms.js"></script>
  <script src="includes/js/foundation/foundation.alerts.js"></script>
  <script src="includes/js/foundation/foundation.magellan.js"></script>
  <script src="includes/js/foundation/foundation.reveal.js"></script>
  <script src="includes/js/foundation/foundation.tooltips.js"></script>
  <script src="includes/js/foundation/foundation.clearing.js"></script>
  <script src="includes/js/foundation/foundation.cookie.js"></script>
  <script src="includes/js/foundation/foundation.joyride.js"></script>
  <script src="includes/js/foundation/foundation.orbit.js"></script>
  <script src="includes/js/foundation/foundation.section.js"></script>
  <script src="includes/js/foundation/foundation.topbar.js"></script>
    
  <script>
    $(document).foundation();
  </script>
</body>
</html>
