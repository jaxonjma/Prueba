package com.jaxon.prueba.service;

import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertSame;
import static org.mockito.Matchers.any;
import static org.mockito.Matchers.anyString;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.List;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;
import org.springframework.core.env.Environment;
import org.springframework.data.domain.Example;

import com.jaxon.prueba.model.Student;
import com.jaxon.prueba.repository.IStudentRepository;
import com.jaxon.prueba.service.exceptions.BDException;
import com.jaxon.prueba.service.exceptions.ElementNotFoundException;
import com.jaxon.prueba.service.impl.StudentService;
import com.jaxon.prueba.util.EntityBuilder;

@RunWith(MockitoJUnitRunner.class)
public class StudentServiceUnitTest {

	
	@InjectMocks 
	private IStudentService studentService = new StudentService();
	
	@InjectMocks
	StudentService ss= new StudentService();
	
	@Mock 
	private IStudentRepository studentRepository;
	
	@Mock
	private Environment environment;
	
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
	
	@Test
	public void modifyTestExistTrue() throws ElementNotFoundException {
		Student student= EntityBuilder.newStudentComplete();
		when(studentRepository.exists(Example.of(student))).thenReturn(Boolean.TRUE);
		when(studentRepository.save(any(Student.class))).thenReturn(null);
		assertNull(studentService.modify(student));
	}

	@Test(expected = ElementNotFoundException.class) 
	public void modifyTestExistFalse() throws ElementNotFoundException {
		Student student= EntityBuilder.newStudentComplete();
		when(studentRepository.exists(Example.of(student))).thenReturn(Boolean.FALSE);
		when(studentRepository.save(any(Student.class))).thenReturn(null);
		when(environment.getProperty(anyString())).thenReturn("aText");
		assertNull(studentService.modify(student));
	}

	@Test
	public void deleteTest() throws BDException {
		studentService.delete(1L);
	}
	
	@Test
	public void saveStudentsInDataBaseTest(){
		when(studentRepository.save(Matchers.anyListOf(Student.class))).thenReturn(null);
		studentService.saveStudentsInDataBase();
		ss.init();
	}
}






