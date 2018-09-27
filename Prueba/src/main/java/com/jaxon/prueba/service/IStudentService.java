package com.jaxon.prueba.service;

import java.util.List;

import com.jaxon.prueba.model.Student;

public interface IStudentService {

	List<Student> getAllStudents();
	
	void saveStudentsInDataBase();

	List<Student> generateAleatoryStudents(boolean generateId);
	
	Student create(Student student) throws Exception;

	Student modifiy(Student student) throws Exception;
	
	void delete(Long idt) throws Exception;


}
