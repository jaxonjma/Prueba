package com.jaxon.prueba.controller;

import static org.springframework.hateoas.mvc.ControllerLinkBuilder.linkTo;

import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.MessageSource;
import org.springframework.hateoas.Link;
import org.springframework.validation.BindingResult;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jaxon.prueba.controller.response.Response;
import com.jaxon.prueba.model.Student;
import com.jaxon.prueba.model.validators.StudentValidator;
import com.jaxon.prueba.service.IStudentService;
import com.jaxon.prueba.service.exceptions.BDException;

@RestController
@RequestMapping("/api/students")
public class StudentController {
	
	@Autowired
	private IStudentService studentService;
	
    @Autowired
    private MessageSource messages;
	
	@Autowired
	private StudentValidator studentValidator;

	@InitBinder
	protected void initBinder(WebDataBinder binder) {
		binder.addValidators(studentValidator);
	}
	
	@GetMapping
	public Response<List<Student>> getAllStudents() {
		
		List<Student> students = studentService.getAllStudents();
		
	    for (Student student : students) {
	        String studentId = student.getIdt().toString();
	        Link selfLink = linkTo(StudentController.class).slash(studentId).withSelfRel();
	        student.add(selfLink);
	    }

        return new Response<>(Boolean.TRUE,students);

	}

	@PutMapping
	public Response<Void> createStudent(@RequestBody @Validated Student student, BindingResult result) throws BDException {

		if(result.hasErrors()) {
			
			String errors = result.getAllErrors()
					.stream()
					.map(objectError -> messages.getMessage(objectError.getCode(), null, Locale.ENGLISH))
					.collect(Collectors.joining(", "));
			
			return new Response<>(Boolean.FALSE,StringUtils.capitalize(errors).concat("."));
		}
		
		studentService.create(student);
		return new Response<>(Boolean.TRUE,"Student created");
	}
	
	@DeleteMapping("/{idt}")
	public Response<Void> deleteStudent(@PathVariable Long idt) throws BDException {
			studentService.delete(idt);
			return new Response<>(Boolean.TRUE,"Student deleted");
	}
	
}
