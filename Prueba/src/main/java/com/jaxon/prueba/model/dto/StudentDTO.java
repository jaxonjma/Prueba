package com.jaxon.prueba.model.dto;

public class StudentDTO {

	private String firstName;
	private String lastName;
	private String email;
	
	public StudentDTO() {}
	
	public StudentDTO(String firstName,String lastName,String email) {
		this.firstName=firstName;
		this.lastName=lastName;
		this.email=email;
	}
	
	public String getFirstName() {
		return firstName;
	}
	public void setFirstNme(String firstname) {
		this.firstName = firstname;
	}
	public String getLastName() {
		return lastName;
	}
	public void setLastName(String lastName) {
		this.lastName = lastName;
	}
	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	
	
}
