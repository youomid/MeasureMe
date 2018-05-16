import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';


@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.css']
})
export class LoginFormComponent implements OnInit {

  username = ""
  password = ""
  message = ""

  constructor(private router: Router) {
  	this.router = router
  }

  ngOnInit() {
  }

  login(){
  	this.router.navigate(['/main']);
  }

  guestLogin(){
  	this.router.navigate(['/main']);
  }

  forgotPassword(){
  	this.message = "The forgot password feature is \
  		currently in development."
  }

}
