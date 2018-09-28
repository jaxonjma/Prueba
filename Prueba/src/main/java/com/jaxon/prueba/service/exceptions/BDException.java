package com.jaxon.prueba.service.exceptions;

public class BDException extends Exception  {

	private static final long serialVersionUID = 1L;
	
	public BDException() {
		super();
	}
	
	public BDException(String message) {
		super(message);
	}
}
