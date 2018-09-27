package com.jaxon.prueba.controller.advice;

import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import com.jaxon.prueba.controller.response.Response;

@ControllerAdvice(basePackages = "com.jaxon.prueba.controller")
public class RestControllerExceptionHandler {

	
	@ExceptionHandler(Throwable.class)
	public Response<Void> handleThrowable (Throwable ex) {
    	return new Response<Void>(Boolean.FALSE, "An unexpected internal server error occured");
    }
	
}
