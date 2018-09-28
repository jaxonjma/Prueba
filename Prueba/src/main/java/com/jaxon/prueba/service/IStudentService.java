package com.jaxon.prueba.service;

import java.util.List;

import com.jaxon.prueba.model.Student;
import com.jaxon.prueba.service.exceptions.BDException;
import com.jaxon.prueba.service.exceptions.ElementNotFoundException;

public interface IStudentService {

	List<Student> getAllStudents();
	
	void saveStudentsInDataBase();

	List<Student> generateAleatoryStudents(boolean generateId);
	
	Student create(Student student) throws BDException;

	Student modifiy(Student student) throws ElementNotFoundException;
	
	void delete(Long idt) throws BDException;


}
