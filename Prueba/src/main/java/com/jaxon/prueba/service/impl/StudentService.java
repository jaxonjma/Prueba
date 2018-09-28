package com.jaxon.prueba.service.impl;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.stream.LongStream;

import javax.annotation.PostConstruct;

import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.data.domain.Example;
import org.springframework.stereotype.Service;

import com.jaxon.prueba.model.Student;
import com.jaxon.prueba.repository.IStudentRepository;
import com.jaxon.prueba.service.IStudentService;
import com.jaxon.prueba.service.exceptions.BDException;
import com.jaxon.prueba.service.exceptions.ElementNotFoundException;

@Service
public class StudentService implements IStudentService{
	
    private Random randomGenerator = new Random();

	private List<String> firstNames = Arrays.asList("George", "Michael", "Tim", "Peter", "Mary", "Louise", "Anna", "Harry", "Allan", "Ariel", "Bill", "Bob");
	private List<String> lastNames = Arrays.asList("Morgan", "Smith", "Johnson", "Jones", "Brown", "Taylor", "Williams", "Miller", "Lam", "Anderson", "Wilson");
	private List<String> domains = Arrays.asList("test.test", "test.com", "trying.dot", "replaytest.tk", "mydomain.wiki", "domain.test", "mytestmail.test");

	private Boolean persistedData = Boolean.FALSE;
	
	private static final Logger LOG = LoggerFactory.getLogger("prueba");
	
	@Autowired
	private IStudentRepository studentRepository;

    @Autowired
    private Environment environment;
	
    @PostConstruct
    public void init() {
    	this.saveStudentsInDataBase();
    }
	
	@Override
	public List<Student> getAllStudents() {
		return studentRepository.findAll();
	}

	@Override
	public Student create(Student student) throws BDException {
		return studentRepository.save(student);
	}
	
	@Override
	public Student modifiy(Student student) throws ElementNotFoundException {
		
		if(studentRepository.exists(Example.of(student)))
			return studentRepository.save(student);
		
		throw new ElementNotFoundException(environment.getProperty("student.element.not.found"));
		
	}
	
	@Override
	public void delete(Long idt) throws BDException {
		studentRepository.delete(idt);
	}
	
	@Override
	public void saveStudentsInDataBase() {

		if (!persistedData) {
			List<Student> students = this.generateAleatoryStudents(Boolean.FALSE);
			studentRepository.save(students);
			persistedData = Boolean.TRUE;
		} 
		LOG.info("Data already persisted");
		
	}

	@Override
	public List<Student> generateAleatoryStudents(boolean generateId) {
		
		List<Student> students = new ArrayList<>();

		LongStream.range(0, 5).forEach(i -> {
        	Student student = new Student();

        	if(generateId)
        		student.setIdt(i+1L);
        	
        	student.setFirstName(firstNames.get(randomGenerator.nextInt(firstNames.size())));
        	student.setLastName(lastNames.get(randomGenerator.nextInt(lastNames.size())));
        	student.setEmail(
        			StringUtils.lowerCase(student.getFirstName().concat(".").concat(student.getLastName()))
        			.concat("@")
        			.concat(domains.get(randomGenerator.nextInt(domains.size())))
        			);
        	students.add(student);
        });
        
		return students;

	}

}
