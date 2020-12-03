       var instances;
	   document.addEventListener('DOMContentLoaded', function() {
		var elems = document.querySelectorAll('select');
		const options = [
		{ name : 'start 1',  value : '1'},
		{ name : 'start 2',  value : '2'},
		{ name : 'end 3 ',  value : '3 '},
		{ name : 'end 4 ', value : '4 '},
		{ name : 'end 5 ',  value : '5'},
		{ name : 'go 6 ',  value : '6'}
		]
		 instances = M.FormSelect.init(elems, options);



	  });
	  		function getVAl(){
			//console.log(instances[0].getSelectedValues());
			console.log(document.getElementById("xxxx").value);
		}
