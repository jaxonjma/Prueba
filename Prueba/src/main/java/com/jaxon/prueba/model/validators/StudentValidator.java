package com.jaxon.prueba.model.validators;

import static com.jaxon.prueba.model.validators.ValidationPatterns.EMAIL_PATTERN;

import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Component;
import org.springframework.validation.Errors;
import org.springframework.validation.ValidationUtils;
import org.springframework.validation.Validator;

import com.jaxon.prueba.model.dto.StudentDTO;

@Component
public class StudentValidator implements Validator {

	@Override
	public boolean supports(Class<?> clazz) {		
      return StudentDTO.class.isAssignableFrom(clazz);
	}

	@Override
	public void validate(Object obj, Errors err) {

	      ValidationUtils.rejectIfEmpty(err, "firstName", "student.firstName.empty");
	      ValidationUtils.rejectIfEmpty(err, "lastName", "student.lastName.empty");
	      ValidationUtils.rejectIfEmpty(err, "email", "student.email.empty");

	      StudentDTO student = (StudentDTO) obj;
	      
	      if (!StringUtils.isBlank(student.getEmail()) && !(EMAIL_PATTERN.matcher(student.getEmail()).matches()))
	         err.rejectValue("email", "student.email.invalid");

	}

}
