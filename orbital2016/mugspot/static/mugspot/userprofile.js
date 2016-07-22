$('#accInfoForm').on('submit', function(event){
	event.preventDefault();
	console.log("form submitted!");
	update_account();
})

function update_account() {
	console.log("Update account is working!");
	var xhr = new XMLHttpRequest();
	var fd = new FormData();
	fd.append('user_name',$('#User-username').val());
	fd.append('user_email',$('#User-useremail').val());
	fd.append('user_faculty',$('#User-userfaculty').val());
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.status == 200) {
			var response = JSON.parse(xhr.responseText);
			testing_2(response);
		}
	}
	function testing_2(res_obj) {
		console.log(res_obj);
	}
	xhr.open('POST', "{% url 'mugspot:update_account_view' %}", true);
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie !== '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) === (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');
	xhr.setRequestHeader("X-CSRFToken", csrftoken);
	xhr.send(fd);
}