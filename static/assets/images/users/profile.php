<?php
include("header.php");


		$resultx="SELECT * from PMSv2.users where email='".$_SESSION['email']."'";
		$queryx = mysqli_query($conn,$resultx); 
		$rowx = mysqli_fetch_array($queryx);


?>
      <div class="page-wrapper">
        <!-- ============================================================== -->
        <!-- Bread crumb and right sidebar toggle -->
        <!-- ============================================================== -->
        <div class="row page-titles">
          <div class="col-md-5 col-12 align-self-center">
            <h3 class="text-themecolor mb-0">Profile Page</h3>
            <ol class="breadcrumb mb-0">
              <li class="breadcrumb-item">
                <a href="javascript:void(0)">Home</a>
              </li>
              <li class="breadcrumb-item active">Profile Page</li>
            </ol>
          </div>
        </div>
        <!-- ============================================================== -->
        <!-- End Bread crumb and right sidebar toggle -->
        <!-- ============================================================== -->
        <!-- -------------------------------------------------------------- -->
        <!-- Container fluid  -->
        <!-- -------------------------------------------------------------- -->
        <div class="container-fluid">
          <!-- -------------------------------------------------------------- -->
          <!-- Start Page Content -->
          <!-- -------------------------------------------------------------- -->
          <!-- Row -->
          <div class="row">
            <!-- Column -->
            <div class="col-lg-4 col-xlg-3 col-md-5">
              <div class="card">
                <div class="card-body">
                  <center class="mt-4">
                    <img
                      src="assets/images/users/5.jpg"
                      class="rounded-circle"
                      width="150"
                    />
                    <h4 class="card-title mt-2"><?=$_SESSION['email_name'];?></h4>
                    <h6 class="card-subtitle"><?=$rowx['designation'];?></h6>
                    <div class="row text-center justify-content-md-center">
                    </div>
                  </center>
                </div>
                <div>
                  <hr />
                </div>
                <div class="card-body">
                  <small class="text-muted">Email address </small>
                  <h6><?=$_SESSION['email'];?></h6>
                  <small class="text-muted pt-4 db">Phone</small>
                  <h6><?=$rowx['contactNumber'];?></h6>
                  <small class="text-muted pt-4 db">Extension</small>
                  <h6><?=$rowx['extensionNumber'];?></h6>
                </div>
              </div>
            </div>
            <!-- Column -->
            <!-- Column -->
            <div class="col-lg-8 col-xlg-9 col-md-7">
              <div class="card">
                <!-- Tabs -->
                <ul
                  class="nav nav-pills custom-pills"
                  id="pills-tab"
                  role="tablist"
                >

                  <li class="nav-item">
                    <a
                      class="nav-link active"
                      id="pills-profile-tab"
                      data-bs-toggle="pill"
                      href="#last-month"
                      role="tab"
                      aria-controls="pills-profile"
                      aria-selected="true"
                      >Profile</a
                    >
                  </li>
                  <li class="nav-item">
                    <a
                      class="nav-link"
                      id="pills-setting-tab"
                      data-bs-toggle="pill"
                      href="#previous-month"
                      role="tab"
                      aria-controls="pills-setting"
                      aria-selected="false"
                      >Setting</a
                    >
                  </li>
                </ul>
                <!-- Tabs -->
                <div class="tab-content active" id="pills-tabContent">
                  <div
                    class="tab-pane fade show active"
                    id="last-month"
                    role="tabpanel"
                    aria-labelledby="pills-profile-tab"
                  >
                    <div class="card-body">
                      <div class="row">


                        <div class="col-md-12 col-xs-12 b-r">
                          <strong>Full Name</strong>
                          <br />
                          <p class="text-muted"><?=$rowx['name'];?></p>
                        </div>
                        <div class="col-md-12 col-xs-12 b-r">
                          <strong>Company</strong>
                          <br />
                          <p class="text-muted"><?=get_company($rowx['company']);?></p>
                        </div>
                        <div class="col-md-12 col-xs-12 b-r">
                          <strong>Department</strong>
                          <br />
                          <p class="text-muted"><?=get_department($rowx['department']);?></p>
                        </div>
                        <div class="col-md-12 col-xs-12 b-r">
                          <strong>Designation</strong>
                          <br />
                          <p class="text-muted"><?=$rowx['designation'];?></p>
                        </div>
                        <div class="col-md-12 col-xs-12 b-r">
                          <strong>Job Grade</strong>
                          <br />
                          <p class="text-muted"><?=get_joblevel($rowx['joblevel']);?></p>
                        </div>
                        <div class="col-md-12 col-xs-12 b-r">
                          <strong>HOD</strong>
                          <br />
                          <p class="text-muted"><?=email2name($rowx['superior_email']);?></p>
                        </div>
                        <div class="col-md-12 col-xs-12 b-r">
                          <strong>Location</strong>
                          <br />
                          <p class="text-muted"><?=$rowx['location'];?></p>
                        </div>
                      </div>

                    </div>
                  </div>
                  <div
                    class="tab-pane fade"
                    id="previous-month"
                    role="tabpanel"
                    aria-labelledby="pills-setting-tab"
                  >
                    <div class="card-body">


                      <form class="form-horizontal form-material" method=post action=api.php>
												<input type=hidden name=updateprofile value="<?=time();?>">
                        <div class="mb-3">
                          <label class="col-md-12">Phone No</label>
                          <div class="col-md-12">
                            <input
                              type="text"
                              value="<?=$rowx['contactNumber'];?>"
                              class="form-control form-control-line"
                              name="contactNumber"
                            />
                          </div>
                        </div>
                        <div class="mb-3">
                          <label class="col-md-12">Extension No</label>
                          <div class="col-md-12">
                            <input
                              type="text"
                              value="<?=$rowx['extensionNumber'];?>"
                              class="form-control form-control-line"
                              name="extensionNumber"
                            />
                          </div>
                        </div>


                    <div class="mb-3">
                      <div class="custom-control custom-radio">
                        <input
                          type="radio"
                          id="customRadio1"
                          name="contactNumberStatus"
                          class="form-check-input"
                          value=1
                           <?=($row['contactNumberStatus']==1 ? 'checked':'');?>
                        />
                        <label class="form-check-label" for="customRadio1"
                          >Show my mobile number at Contacts</label
                        >
                      </div>
                      <div class="custom-control custom-radio">
                        <input
                          type="radio"
                          id="customRadio2"
                          name="contactNumberStatus"
                          class="form-check-input"
                          value=0
                          <?=($row['contactNumberStatus']==0 ? 'checked':'');?>
                        />
                        <label class="form-check-label" for="customRadio2"
                          >Hide my mobile number at Contacts</label
                        >
                      </div>
                    </div>


                        <div class="mb-3">
                          <div class="col-sm-12">
                            <button class="btn btn-success">
                              Update Profile
                            </button>
                          </div>
                        </div>
                      </form>
                      
 </hr>                     



          <div class="row el-element-overlay">
            <div class="col-lg-3 col-md-6">
              <div class="card">
                <div class="el-card-item pb-3">
                  <div
                    class="
                      el-card-avatar
                      mb-3
                      el-overlay-1
                      w-100
                      overflow-hidden
                      position-relative
                      text-center
                    "
                  >
                    <img
                      src="assets/images/big/img1.jpg"
                      class="d-block position-relative w-100"
                      alt="user"
                    />
                  </div>
                  <div class="el-card-content text-center">
                    <h4 class="mb-0">Project title</h4>
                    <span class="text-muted">subtitle of project</span>
                  </div>
                </div>
              </div>
            </div>

          </div>









                      
                      
                      
                      
                      
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Column -->
          </div>
          <!-- Row -->
          <!-- -------------------------------------------------------------- -->
          <!-- End PAge Content -->
          <!-- -------------------------------------------------------------- -->
        </div>
        <!-- -------------------------------------------------------------- -->
        <!-- End Container fluid  -->
        <!-- -------------------------------------------------------------- -->
        <!-- -------------------------------------------------------------- -->
        <!-- footer -->
        <!-- -------------------------------------------------------------- -->
        <footer class="footer text-center">
          All Rights Reserved by Materialpro admin.
        </footer>
        <!-- -------------------------------------------------------------- -->
        <!-- End footer -->
        <!-- -------------------------------------------------------------- -->
      </div>

<?php
include("footer.php");
?>