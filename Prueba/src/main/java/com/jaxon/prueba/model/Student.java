package com.jaxon.prueba.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.SequenceGenerator;

import org.springframework.hateoas.ResourceSupport;

@Entity
public class Student extends ResourceSupport {
	
    @GeneratedValue(strategy=GenerationType.SEQUENCE, generator="student_seq")
	@SequenceGenerator(name="student_seq", initialValue=1, allocationSize=1)
	@Id
	@Column(name="idt")
	private Long idt;
	
	private String firstName;

	private String lastName;
	
	private String email;

	public Student() {
		
	}
	
	public Student(Long idt, String firstName, String lastName, String mail) {
		super();
		this.idt = idt;
		this.firstName = firstName;
		this.lastName = lastName;
		this.email = mail;
	}

	public Long getIdt() {
		return idt;
	}

	public void setIdt(Long idt) {
		this.idt = idt;
	}

	public String getFirstName() {
		return firstName;
	}

	public void setFirstName(String firstName) {
		this.firstName = firstName;
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
