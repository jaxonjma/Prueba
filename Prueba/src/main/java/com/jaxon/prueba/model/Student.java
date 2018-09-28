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
	
	public Student(Long idt) {
		super();
		this.idt = idt;
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

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = super.hashCode();
		result = prime * result + ((email == null) ? 0 : email.hashCode());
		result = prime * result + ((firstName == null) ? 0 : firstName.hashCode());
		result = prime * result + ((idt == null) ? 0 : idt.hashCode());
		result = prime * result + ((lastName == null) ? 0 : lastName.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (!super.equals(obj) || getClass() != obj.getClass())
			return false;
		Student other = (Student) obj;
		if (email == null && other.email != null) {
			return false;
		} 
		if (firstName == null && other.firstName != null) {
			return false;
		} 
		if (idt == null && other.idt != null) {
			return false;
		} 
		if (lastName == null && other.lastName != null) {
			if (other.lastName != null)
				return false;
		} else if (!other.lastName.equals(lastName)) {
			return false;}
		return true;
	}

	
}
