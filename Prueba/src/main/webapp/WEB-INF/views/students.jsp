<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags"%>

<html>
<head>
  <!-- Standard Meta -->
  <jsp:include page="common/meta.jsp"/>
  <!-- Common styles -->
  <jsp:include page="common/css.jsp"/>
  <link rel="stylesheet" type="text/css" href="resources/js/datatables/datatables.min.css" />
  
</head>
<body>
  <div class="wrapper">
	<!-- Menu -->
	<jsp:include page="common/menu.jsp"/>
  	<!-- Content -->
	<div id="content" class="container-fluid">
		  <div class="row">
		  	  <div class="form-row">
		  	
			    <div class="col">
			      <input id="ipt-first-name" type="text" class="form-control" placeholder="First name">
			    </div>
			    <div class="col">
			      <input id="ipt-last-name" type="text" class="form-control" placeholder="Last name">
			    </div>
			    <div class="col">
			      <input id="ipt-email" type="text" class="form-control" placeholder="Email">
			    </div>
			    <div class="col">
  						<button id="btn-guardar" class="btn btn-success mb-2">Save</button>
			    </div>
			  </div>	
		  </div>	
			<br>
			<div class="row">
				<div class="col-md-12">
					<table id="table-list" class="ui celled table" width="100%">
					  <thead>
					    <th>Id</th>
					    <th>First Name</th>
					    <th>Last Name</th>
					    <th>Email</th>
					    <th>Actions</th>
					  </tr></thead>
					  <tbody>
					  </tbody>
					</table>
				</div>
			</div>
	</div>

  </div>
	<!-- Footer -->
    <jsp:include page="common/footer.jsp"/>
</body>
<!-- Common JavaScript -->
<jsp:include page="common/js.jsp"/>
<!-- View's JavaScript -->
<script type="text/javascript" src="resources/js/datatables/datatables.min.js" charset="UTF-8"></script>
<script src="resources/js/students.js"></script>
</html>
