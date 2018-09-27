package com.jaxon.prueba.service.exceptions;

public class ElementNotFoundException extends Exception {

	private static final long serialVersionUID = 1L;
	
	public ElementNotFoundException() {
		super();
	}
	
	public ElementNotFoundException(String message) {
		super(message);
	}

}
