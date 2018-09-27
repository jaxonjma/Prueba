package com.jaxon.prueba.views;


import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class ViewController {

	@GetMapping({"/","/home"})
	public String getHome() {
		return "home";
	}

	@GetMapping({"/students",})
	public String getStudentse() {
		return "students";
	}

}
