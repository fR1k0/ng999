$(document).ready(function(){


	  const socket = new WebSocket('wss://' + location.host + '/echo');
	  socket.addEventListener('message', ev => {
	     const obj = JSON.parse(ev.data);

        //console.log("Received number" + JSON.parse(ev.data));




                	if(obj.type=='OnOff') 
                	{
                		
                		if(obj.state=='ON')
                		{
											$('#'+obj.name+'').prop("checked", true);
	                		//if($('#'+obj.name+'').bootstrapSwitch('state')==false) {
	                		//	$('#'+obj.name+'').bootstrapSwitch('state', true);
	                		//}


							        $('#on_'+obj.name+'').removeClass('hide');
							        $('#off_'+obj.name+'').addClass('hide');




                			
                		} else {
                			$('#'+obj.name+'').prop("checked", false);
	                		//if($('#'+obj.name+'').bootstrapSwitch('state')==true) {
	                		//	$('#'+obj.name+'').bootstrapSwitch('state', false);
	                		//}                			

							        $('#off_'+obj.name+'').removeClass('hide');
							        $('#on_'+obj.name+'').addClass('hide');

                		}
                		
                		//if($('#'+obj.name+'').bootstrapSwitch('state')==false) {
                		//	$('#'+obj.name+'').bootstrapSwitch('state', true);
                		//}
                		//$('#'+obj.name+'').prop("checked", true);
                		
                	
                	}	else if(obj.type=='Decimal' || obj.type=='Quantity') {    
                		
                		
										if(obj.name=='Water_EC' || obj.name=='Water_EC1' || obj.name=='Water_EC2') {
											n=parseFloat(obj.state).toFixed(2);
										}
										else {
											n=obj.state;
										}
                		          		
                		$('#'+obj.name+'').val(''+n+'');
                		$('#'+obj.name+'').html(''+n+'');
                	} else {
                		
										if(obj.name=='Water_EC' || obj.name=='Water_EC1' || obj.name=='Water_EC2') {
											n=parseFloat(obj.state).toFixed(2);
										}
										else {
											n=obj.state;
										}
                		$('#'+obj.name+'').html(''+obj.state+'');
                	}
                	
                	



	  });


});


