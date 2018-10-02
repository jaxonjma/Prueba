package com.jaxon.prueba.controller;

import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.List;

import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import com.jaxon.prueba.model.Student;
import com.jaxon.prueba.service.impl.StudentService;
import com.jaxon.prueba.util.EntityBuilder;

@Ignore
@RunWith(MockitoJUnitRunner.class)
public class StudentControllerUnitTest {

	@InjectMocks
	StudentController studentController=new StudentController();
	
	@Mock
	StudentService studentService;
	
	@Test
	public void getAllStudentsTest() {
		List<Student> students=new ArrayList<>();
		students.add(EntityBuilder.newStudentComplete());
		when(studentService.getAllStudents()).thenReturn(students);
		//studentController.getAllStudents();
	}
}
