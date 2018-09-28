package com.jaxon.prueba.service;

import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertSame;
import static org.mockito.Matchers.any;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.List;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import com.jaxon.prueba.model.Student;
import com.jaxon.prueba.repository.IStudentRepository;
import com.jaxon.prueba.service.exceptions.BDException;
import com.jaxon.prueba.service.impl.StudentService;
import com.jaxon.prueba.util.EntityBuilder;

@RunWith(MockitoJUnitRunner.class)
public class StudentServiceUnitTest {

	
	@InjectMocks 
	private IStudentService studentService = new StudentService();
	
	@Mock 
	private IStudentRepository studentRepository;
	
	private List<Student> response;
	
	@Before 
	public void setUp() {
		response=new ArrayList<>();
	}
	
	@Test
	public void getAllStudentsTest() {
		response.clear();
		response.add(EntityBuilder.newStudentOnlyIdt());
		when(studentRepository.findAll()).thenReturn(response);
		assertSame(studentService.getAllStudents().get(0).getIdt(),EntityBuilder.getIdtStudentOnlyIdt());
	}
	
	@Test
	public void createTest() throws BDException {
		when(studentRepository.save(any(Student.class))).thenReturn(null);
		assertNull(studentService.create(new Student()));
	}
}
