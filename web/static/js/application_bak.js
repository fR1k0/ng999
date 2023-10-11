
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];





    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.data);
        const obj = msg.data;
        lenwc = obj.homepage.widgets[0].widgets.length;
        
        $('#sitename').html(obj.label);
        $('#wc').html('');
        $('#wl').html('');
        $('#ambient').html('');
        $('#insights').html('');
        $('#control').html('');
        $('#controlon').html('');
        $('#controloff').html('');
        $('#others').html('');
        $('#task').html('');
        $('#userconfig').html('');
        $('#adminconfig').html('');
        $('#plan').html('');
        $('#plotsetting').html('');
        $('#plotfertigation').html('');
        $('#plotirrigation').html('');
        
        

        for (let i = 0; i < obj.homepage.widgets[0].widgets.length; i++) {
				 // text += cars[i] + "<br>";
				  
//				  $('#wc').append('<hr>');
//				  $('#wc').append(obj.homepage.widgets[0].widgets[i].item.name);
//				  $('#wc').append(obj.homepage.widgets[0].widgets[i].item.state);
//				  $('#wc').append(obj.homepage.widgets[0].widgets[i].label);

					$('#wc').append('<div class="col-lg-4 col-md-6 border-end align-self-center"><div class="card-body"><div class="d-flex flex-row"><div class="col-8 p-0 align-self-center">'+
					'<h3 class="mb-0">'+obj.homepage.widgets[0].widgets[i].item.state+'</h3><h5 class="text-muted mb-0">'+obj.homepage.widgets[0].widgets[i].item.label+'<span class="sl-date text-muted ms-1">(mS/cm)</span></h5></div>'+
					'<div class="col-4 text-end">'+
					'<div class="round text-white d-inline-block text-center rounded-circle bg-success"><i class="mdi mdi-chart-line"></i></div>'+
					'</div></div></div></div>');


				}

        for (let i = 0; i < obj.homepage.widgets[1].widgets.length; i++) {
				 // text += cars[i] + "<br>";

				  
				  //$('#wl').append('<hr>');
				  //$('#wl').append(obj.homepage.widgets[1].widgets[i].item.name);
				  //$('#wl').append(obj.homepage.widgets[1].widgets[i].item.state);
				  //$('#wl').append(obj.homepage.widgets[1].widgets[i].label);


                var waterstate=(obj.homepage.widgets[1].widgets[i].item.state/1000)*100;
							
							
								if(waterstate==999999.9) {
									waterstate=0;
								}                
                
                if(waterstate>60) {
                	var badge='success';
                	var badgeTxt='Good';
                } else if (waterstate>30 && waterstate<60) {
                	var badge='warning';
                	var badgeTxt='Normal';
                } else {
                	var badge='danger';
                	var badgeTxt='Critical';
                }






					$('#wl').append('<div class="d-flex"><i class="mdi mdi-water-percent display-7"></i><div class="ms-2 align-self-center" style="width:100%">'+
						'<h6 class="text-muted mb-0"><div class="d-flex border-bottom"><div>'+obj.homepage.widgets[1].widgets[i].label+' <span class="badge ms-auto bg-'+badge+'">'+badgeTxt+'</span></div>'+
						'<div class="ms-auto flex-shrink-0"><i data-feather="info" class="feather-sm me-2"></i></div></div></h6>'+
						'<h6 class="text-muted mb-3"><div class="progress" style="100%;height:15px"><div class="progress-bar bg-'+badge+'" style="width: '+waterstate+'%;" role="progressbar">'+waterstate+'%</div></div></h6>'+
						'</div></div>');



				}
				
        for (let i = 0; i < obj.homepage.widgets[2].widgets.length; i++) {
				 // text += cars[i] + "<br>";
				  
				  // $('#ambient').append('<hr>');
				  //$('#ambient').append(obj.homepage.widgets[2].widgets[i].item.name);
				  //$('#ambient').append(obj.homepage.widgets[2].widgets[i].item.state);
				  //$('#ambient').append(obj.homepage.widgets[2].widgets[i].label);


					$('#ambient').append('<div class="col-4"><div>'+
						'<div class="d-flex align-items-center">'+
						'<i class="mdi mdi-water-percent display-8"></i>'+
						'<div class="ms-1">'+
						'<h6 class="mb-0">'+obj.homepage.widgets[2].widgets[i].item.state+'</h6>'+
						'<h6 class="card-subtitle mb-0 fs-2 fw-normal">'+obj.homepage.widgets[2].widgets[i].item.name+'</h6>'+
						'</div></div></div></div>');




				}				


        for (let i = 0; i < obj.homepage.widgets[4].widgets.length; i++) {
				 // text += cars[i] + "<br>";
				 // homepage.widgets[4].widgets[0].label
				   $('#insights').append('<li><i data-feather="star" class="feather-sm me-2"></i>'+obj.homepage.widgets[4].widgets[i].label+'</li>');
				 // $('#insights').append(obj.homepage.widgets[4].widgets[i].item.name);
				  //$('#insights').append(obj.homepage.widgets[4].widgets[i].item.state);
				 // $('#insights').append(obj.homepage.widgets[4].widgets[i].label);
            
				}			


        for (let i = 0; i < obj.homepage.widgets[5].widgets.length; i++) {
				 // text += cars[i] + "<br>";
				  
				  // $('#control').append('<hr>');
				 // $('#control').append(obj.homepage.widgets[5].widgets[i].item.name);
				 // $('#control').append(obj.homepage.widgets[5].widgets[i].item.state);
				 // $('#control').append(obj.homepage.widgets[5].widgets[i].label);
	
                if(obj.homepage.widgets[5].widgets[i].item.state=='ON') {
                	
                	$('#controlon').append('<li>'+obj.homepage.widgets[5].widgets[i].item.name+'</li>');
                	
                	
                	$('#control').append('<tr><td>'+obj.homepage.widgets[5].widgets[i].label+'</td><td><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[5].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[5].widgets[i].item.name+'" value="OFF">OFF</button></td></tr>');
                	
                } else {
                	$('#controloff').append('<li>'+obj.homepage.widgets[5].widgets[i].item.name+'</li>');
                	
                	$('#control').append('<tr><td>'+obj.homepage.widgets[5].widgets[i].label+'</td><td><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[5].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[5].widgets[i].item.name+'" value="OFF">OFF</button></td></tr>');
                }					

				}		



        for (let i = 0; i < obj.homepage.widgets[6].widgets.length; i++) {
				 // text += cars[i] + "<br>";
				  
				  // $('#control').append('<hr>');
				 // $('#control').append(obj.homepage.widgets[5].widgets[i].item.name);
				 // $('#control').append(obj.homepage.widgets[5].widgets[i].item.state);
				 // $('#control').append(obj.homepage.widgets[5].widgets[i].label);
	
                if(obj.homepage.widgets[6].widgets[i].item.state=='ON') {
                	
              	
                	$('#task').append('<tr><td>'+obj.homepage.widgets[6].widgets[i].label+'</td><td><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[6].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[6].widgets[i].item.name+'" value="OFF">OFF</button></td></tr>');
                	
                } else {
                	
                	$('#task').append('<tr><td>'+obj.homepage.widgets[6].widgets[i].label+'</td><td><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[6].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[6].widgets[i].item.name+'" value="OFF">OFF</button></td></tr>');

                }					

				}	



// create the others div first
        for (let i = 0; i < obj.homepage.widgets[3].widgets.length; i++) {
				 // text += cars[i] + "<br>";
				  			  
				  
				  //$('#others').append('<hr>');
				  //$('#others').append(obj.homepage.widgets[3].widgets[i].label);
				  $('#others').append('<div class="col-lg-6">'+
						'<div class="card">'+
						'<div class="d-flex border-bottom title-part-padding align-items-center">'+
						'<div>'+
						'<h4 class="card-title mb-0">'+obj.homepage.widgets[3].widgets[i].label+'</h4>'+
						'</div>'+
						'<div class="ms-auto flex-shrink-0">'+
						'<i data-feather="info" class="feather-sm me-2"></i>'+
						'</div>'+
						'</div>'+
						'<div class="card-body">'+
						'<div class="row" id="others'+i+'">');

                                  		                  		
						
						$('#others').append('</div></div></div></div>');
				  
				}		



// feed the others data
        for (let i = 0; i < obj.homepage.widgets[3].widgets.length; i++) {
				 // text += cars[i] + "<br>";
				  			  
  

						for (let j = 0; j < obj.homepage.widgets[3].widgets[i].widgets.length; j++) {				  	
										  
							 $('#others'+i+'').append('<div class="col-6">'+
									'<div>'+
									'<div class="d-flex align-items-center">'+
									'<i class="mdi mdi-temperature-celsius display-8"></i>'+
									'<div class="ms-2">'+
									'<h6 class="mb-0">'+obj.homepage.widgets[3].widgets[i].widgets[j].item.state+'</h4>'+
									'<h6 class="card-subtitle mb-0 fs-2 fw-normal">'+obj.homepage.widgets[3].widgets[i].widgets[j].item.name+'</h6>'+
									'</div>'+
									'</div>'+
									'</div>'+
									'</div>');



						}

				  
				}	



        for (let i = 0; i < obj.homepage.widgets[7].widgets.length; i++) {


                if(obj.homepage.widgets[7].widgets[i].type=='Setpoint') {
                	
                	$('#userconfig').append('<div class="mb-3 row"><label class="col-md-2 col-form-label">'+obj.homepage.widgets[7].widgets[i].label+'</label><div class="col-md-10"><input class="form-control" type="number" value="'+obj.homepage.widgets[7].widgets[i].item.state+'" min="'+obj.homepage.widgets[7].widgets[i].minValue+'" max="'+obj.homepage.widgets[7].widgets[i].maxValue+'" step="'+obj.homepage.widgets[7].widgets[i].step+'" id="'+obj.homepage.widgets[7].widgets[i].item.name+'"/></div></div>');
                	
                	
                } else {
                	
                	if(obj.homepage.widgets[7].widgets[i].item.state=='ON') {
                		$('#userconfig').append('<div class="mb-3 row"><label class="col-md-2 col-form-label">'+obj.homepage.widgets[7].widgets[i].label+'</label><div class="col-md-10"><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[7].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[7].widgets[i].item.name+'" value="OFF">OFF</button></div></div>');              		
                	} else {
                		$('#userconfig').append('<div class="mb-3 row"><label class="col-md-2 col-form-label">'+obj.homepage.widgets[7].widgets[i].label+'</label><div class="col-md-10"><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[7].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[7].widgets[i].item.name+'" value="OFF">OFF</button></div></div>');
                		
                	}
                	
                	
                }					

				}	


        for (let i = 0; i < obj.homepage.widgets[8].widgets.length; i++) {


                if(obj.homepage.widgets[8].widgets[i].type=='Setpoint') {
                	
                	$('#adminconfig').append('<div class="mb-3 row"><label class="col-md-2 col-form-label">'+obj.homepage.widgets[8].widgets[i].label+'</label><div class="col-md-10"><input class="form-control" type="number" value="'+obj.homepage.widgets[8].widgets[i].item.state+'" min="'+obj.homepage.widgets[8].widgets[i].minValue+'" max="'+obj.homepage.widgets[8].widgets[i].maxValue+'" step="'+obj.homepage.widgets[8].widgets[i].step+'" id="'+obj.homepage.widgets[8].widgets[i].item.name+'"/><span class="help-block text-muted"><small>help text</small></span></div></div>');
                	
                	
                } else {
                	
                	if(obj.homepage.widgets[8].widgets[i].item.state=='ON') {
                		$('#adminconfig').append('<div class="mb-3 row"><label class="col-md-2 col-form-label">'+obj.homepage.widgets[8].widgets[i].label+'</label><div class="col-md-10"><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[8].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[8].widgets[i].item.name+'" value="OFF">OFF</button></br><span class="help-block text-muted"><small>help text</small></span></div></div>');              		
                	} else {
                		$('#adminconfig').append('<div class="mb-3 row"><label class="col-md-2 col-form-label">'+obj.homepage.widgets[8].widgets[i].label+'</label><div class="col-md-10"><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[8].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[8].widgets[i].item.name+'" value="OFF">OFF</button></br><span class="help-block text-muted"><small>help text</small></span></div></div>');
                		
                	}
                	
                	
                }					

				}	
//fertigation plan
        for (let i = 0; i < obj.homepage.widgets[9].widgets[0].widgets.length; i++) {


                if(obj.homepage.widgets[9].widgets[0].widgets[i].type=='Setpoint') {
                	
                	$('#plan').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[0].widgets[i].label+'</label><input class="form-control" type="number" value="'+obj.homepage.widgets[9].widgets[0].widgets[i].item.state+'" min="'+obj.homepage.widgets[9].widgets[0].widgets[i].minValue+'" max="'+obj.homepage.widgets[9].widgets[0].widgets[i].maxValue+'" step="'+obj.homepage.widgets[9].widgets[0].widgets[i].step+'" id="'+obj.homepage.widgets[9].widgets[0].widgets[i].item.name+'"/><small class="form-control-feedback">This is inline help</small></div></div>');


                	
                	
                } else if(obj.homepage.widgets[9].widgets[0].widgets[i].type=='Switch') {
                	
	                	if(obj.homepage.widgets[9].widgets[0].widgets[i].item.state=='ON') {
	                		$('#plan').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[0].widgets[i].label+'</label><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[9].widgets[0].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[9].widgets[0].widgets[i].item.name+'" value="OFF">OFF</button></div></div>');

	                	} else {
	                		$('#plan').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[0].widgets[i].label+'</label><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[9].widgets[0].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[9].widgets[0].widgets[i].item.name+'" value="OFF">OFF</button></div></div>');

	                	}                	
                } else {
                	               	
                	$('#plan').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[0].widgets[i].label+'</label><input class="form-control" type="text" value="'+obj.homepage.widgets[9].widgets[0].widgets[i].item.state+'"  id="'+obj.homepage.widgets[9].widgets[0].widgets[i].item.name+'"/ disabled><small class="form-control-feedback">This is inline help</small></div></div>');
                	
                }					

				}	


// plot setting
        for (let i = 0; i < obj.homepage.widgets[9].widgets[1].widgets.length; i++) {


                if(obj.homepage.widgets[9].widgets[1].widgets[i].type=='Setpoint') {
                	
                	$('#plotsetting').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[1].widgets[i].label+'</label><input class="form-control" type="number" value="'+obj.homepage.widgets[9].widgets[1].widgets[i].item.state+'" min="'+obj.homepage.widgets[9].widgets[1].widgets[i].minValue+'" max="'+obj.homepage.widgets[9].widgets[1].widgets[i].maxValue+'" step="'+obj.homepage.widgets[9].widgets[1].widgets[i].step+'" id="'+obj.homepage.widgets[9].widgets[1].widgets[i].item.name+'"/><small class="form-control-feedback">This is inline help</small></div></div>');


                	
                	
                } else if(obj.homepage.widgets[9].widgets[1].widgets[i].type=='Switch') {
                	
	                	if(obj.homepage.widgets[9].widgets[1].widgets[i].item.state=='ON') {
	                		$('#plotsetting').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[1].widgets[i].label+'</label><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[9].widgets[1].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[9].widgets[1].widgets[i].item.name+'" value="OFF">OFF</button></div></div>');

	                	} else {
	                		$('#plotsetting').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[1].widgets[i].label+'</label><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[9].widgets[1].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[9].widgets[1].widgets[i].item.name+'" value="OFF">OFF</button></div></div>');

	                	}                	
                } else {
                	               	
                	$('#plotsetting').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[1].widgets[i].label+'</label><input class="form-control" type="text" value="'+obj.homepage.widgets[9].widgets[1].widgets[i].item.state+'"  id="'+obj.homepage.widgets[9].widgets[1].widgets[i].item.name+'"/ disabled><small class="form-control-feedback">This is inline help</small></div></div>');
                	
                }					

				}


// plot fertigation
        for (let i = 0; i < obj.homepage.widgets[9].widgets[2].widgets.length; i++) {


                if(obj.homepage.widgets[9].widgets[2].widgets[i].type=='Setpoint') {
                	
                	$('#plotfertigation').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[2].widgets[i].label+'</label><input class="form-control" type="number" value="'+obj.homepage.widgets[9].widgets[2].widgets[i].item.state+'" min="'+obj.homepage.widgets[9].widgets[2].widgets[i].minValue+'" max="'+obj.homepage.widgets[9].widgets[2].widgets[i].maxValue+'" step="'+obj.homepage.widgets[9].widgets[2].widgets[i].step+'" id="'+obj.homepage.widgets[9].widgets[2].widgets[i].item.name+'"/><small class="form-control-feedback">This is inline help</small></div></div>');


                	
                	
                } else if(obj.homepage.widgets[9].widgets[2].widgets[i].type=='Switch') {
                	
	                	if(obj.homepage.widgets[9].widgets[2].widgets[i].item.state=='ON') {
	                		$('#plotfertigation').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[2].widgets[i].label+'</label><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[9].widgets[2].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[9].widgets[2].widgets[i].item.name+'" value="OFF">OFF</button></div></div>');

	                	} else {
	                		$('#plotfertigation').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[2].widgets[i].label+'</label><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[9].widgets[2].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[9].widgets[2].widgets[i].item.name+'" value="OFF">OFF</button></div></div>');

	                	}                	
                } else {
                	               	
                	$('#plotfertigation').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[2].widgets[i].label+'</label><input class="form-control" type="text" value="'+obj.homepage.widgets[9].widgets[2].widgets[i].item.state+'"  id="'+obj.homepage.widgets[9].widgets[2].widgets[i].item.name+'"/ disabled><small class="form-control-feedback">This is inline help</small></div></div>');
                	
                }					

				}	
				
				
// plot irrigation
        for (let i = 0; i < obj.homepage.widgets[9].widgets[3].widgets.length; i++) {


                if(obj.homepage.widgets[9].widgets[3].widgets[i].type=='Setpoint') {
                	
                	$('#plotirrigation').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[3].widgets[i].label+'</label><input class="form-control" type="number" value="'+obj.homepage.widgets[9].widgets[3].widgets[i].item.state+'" min="'+obj.homepage.widgets[9].widgets[3].widgets[i].minValue+'" max="'+obj.homepage.widgets[9].widgets[3].widgets[i].maxValue+'" step="'+obj.homepage.widgets[9].widgets[3].widgets[i].step+'" id="'+obj.homepage.widgets[9].widgets[3].widgets[i].item.name+'"/><small class="form-control-feedback">This is inline help</small></div></div>');


                	
                	
                } else if(obj.homepage.widgets[9].widgets[3].widgets[i].type=='Switch') {
                	
	                	if(obj.homepage.widgets[9].widgets[3].widgets[i].item.state=='ON') {
	                		$('#plotirrigation').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[3].widgets[i].label+'</label><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[9].widgets[3].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[9].widgets[3].widgets[i].item.name+'" value="OFF">OFF</button></div></div>');

	                	} else {
	                		$('#plotirrigation').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[3].widgets[i].label+'</label><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-light" id="'+obj.homepage.widgets[9].widgets[3].widgets[i].item.name+'" value="ON">ON</button><button type="button" class="btn waves-effect waves-light px-4 ms-2 btn-danger" id="'+obj.homepage.widgets[9].widgets[3].widgets[i].item.name+'" value="OFF">OFF</button></div></div>');

	                	}                	
                } else {
                	               	
                	$('#plotirrigation').append('<div class="col-md-6"><div class="mb-3"><label class="control-label">'+obj.homepage.widgets[9].widgets[3].widgets[i].label+'</label><input class="form-control" type="text" value="'+obj.homepage.widgets[9].widgets[3].widgets[i].item.state+'"  id="'+obj.homepage.widgets[9].widgets[3].widgets[i].item.name+'"/ disabled><small class="form-control-feedback">This is inline help</small></div></div>');
                	
                }					

				}	
    });

});


