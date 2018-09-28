package com.jaxon.prueba.util;

import com.jaxon.prueba.model.Student;

public final class EntityBuilder {

	private static final Long idStudentOnlyIdt=1L;
	private static final Long idStudentComplete=2L;

	public static Student newStudentOnlyIdt() {
		return new Student(idStudentOnlyIdt);
	}
	
	public static Student newStudentComplete() {
		Student student=new Student(idStudentComplete);
		student.setFirstName("aFirstName");
		student.setLastName("aLastName");
		student.setEmail("anEmail@test.co");
		return student;
	}
	
	public static Long getIdtStudentOnlyIdt() {
		return idStudentOnlyIdt;
	}
	
	public static Long getIdtStudentComplete() {
		return idStudentComplete;
	}
	
}
