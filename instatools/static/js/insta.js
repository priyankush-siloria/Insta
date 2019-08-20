function togglePassword() {
  var x = document.getElementById("pass");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function toggleCPassword() {
  var y = document.getElementById("cpass");
  if (y.type === "password") {
    y.type = "text";
  } else {
    y.type = "password";
  }
}
function toggleloginPassword() {
  var z = document.getElementById("login_pass");
  if (z.type === "password") {
    z.type = "text";
  } else {
    z.type = "password";
  }
}


function matchPassword(){
	var password = document.getElementById("pass").value;
	var cpassword=document.getElementById("cpass").value;
	if(password!=cpassword){
		document.getElementById("mismatch").style.display = "block";
		return false;	
	}
return true;
}

function matchForgotPassword(){
  var password = document.getElementById("password").value;
  var cpassword=document.getElementById("conf_pass").value;
  if(password!=cpassword){
    document.getElementById("forgot_mismatch").style.display = "block";
    return false; 
  }
return true;
}

// test_insta_account
$('#test_insta_account').click(function() {
    
    var email= $("#email").val();
    var password=$("#insta_password").val();
    var country=$("#country").val();
    if(email =='' || email=='undefined' && password=='' || password=='undefined'){
        swal("Fields cannot be empty!");
        return false;
    }
    $("#divLoading").show();
    $.ajax({
        type: "POST",
        url: "buy-plan",
        data:{ 
            'email':email,
            'password': password,
            'country':country,
            'csrfmiddlewaretoken':token,
            }, 
        success: function(response) {    
            console.log(response);
            if(response.status){
                $("#test_insta_account").hide();
                $("#paypal_div").show();
                paypal_div
                $("#divLoading").hide();
                alert(response.msg);
            }
            else{
              $("#divLoading").hide();
              alert(response.msg);
            }
        }
    })
   });