package com.jaxon.prueba.model.validators;

import java.util.regex.Pattern;

public class ValidationPatterns {
	
	private ValidationPatterns() {}
	
	public static final Pattern EMAIL_PATTERN = Pattern.compile("^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,6}$",
            Pattern.CASE_INSENSITIVE);

}
