"use strict";
(function($){
	var app = {
		init:function(){
			this.variables();
			this.elements();
			this.actions();
		},
		variables:function(){
			this.ids=[];
			this.sendData;
			this.dataRow;
			this.table;
			this.urlBase='/Prueba';
		},
		elements:function(){
			//Guardar
			this.$iptFirstName = $("#ipt-first-name");
			this.$iptLastName = $("#ipt-last-name");
			this.$iptEmail = $("#ipt-email");
			this.$btnGuardar = $("#btn-guardar");
			//Tabla
			app.$tableList = $("#table-list");
		},
		functions:{
			
		},
		actions:function(){
			//Initializers
		    this.table = app.$tableList.DataTable({
				dom:"<>t<'row'<'col-md-4'l><'col-md-4'i><'col-md-4'p>>",
				processing:true,
				serverSide:true,
				scrollX:true,
				scrollCollapse:true,
				ordering: false,
				autoWidth: true,
				paging: false,
		        columnDefs: [ {
		            targets: 4,
		            data: null,
		            defaultContent: "<button class='btn btn-danger delete-action'>Delete</button>"
		        	} 
		        ],
				  ajax:{
					  url: app.urlBase+"/api/students",
					  type: "GET"
		    		},
		    	    columns: [
		    	        { data: 'idt' },
		    	        { data: 'firstName' },
		    	        { data: 'lastName' },
		    	        { data: 'email' }
		    	    ]
		    	});

		    //Events
		    this.$btnGuardar.on("click", function() {

		    	let student = {
		    			"firstName": app.$iptFirstName.val(),
		    			"lastName": app.$iptLastName.val(),
		    			"email": app.$iptEmail.val()
		    			};

				  $.ajax({
					  type: "PUT",
					  url: app.urlBase+"/api/students",
					  data: JSON.stringify(student),
					  contentType: 'application/json'
					}).done(function(response) {
						if(response.success) {
							swal("Success!", response.message, "success");
							app.table.ajax.reload();
						}
						else 
							swal("Error!", response.message, "error");
					});
		    });
		    
		    app.$tableList.find('tbody').on( 'click', 'button', function () {

				app.dataRow = app.table.row($(this).parents('tr')).data();

				if($(this).hasClass("delete-action")) {
					
					  $.ajax({
						  type: "DELETE",
						  url: app.dataRow.links[0].href,
						  contentType: 'application/json'
						}).done(function(response) {
							if(response.success) {
								swal("Success!", response.message, "success");
								app.table.ajax.reload();
							}
							else 
								swal("Error!", response.message, "error");
						});
				}
			});
		    
		}
	}
	return {
		init:app.init(),
	}
})(jQuery)