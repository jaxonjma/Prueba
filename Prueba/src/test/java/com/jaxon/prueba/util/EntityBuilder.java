package com.jaxon.prueba.util;

import com.jaxon.prueba.model.Student;

public final class EntityBuilder {

	private static final Long idStudentOnlyIdt=1L;

	public static Student newStudentOnlyIdt() {
		return new Student(idStudentOnlyIdt);
	}
	
	public static Long getIdtStudentOnlyIdt() {
		return idStudentOnlyIdt;
	}
	
}
