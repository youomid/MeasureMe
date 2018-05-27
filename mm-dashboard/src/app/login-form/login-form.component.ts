import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import { AuthService } from './../auth.service';


@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.css']
})
export class LoginFormComponent implements OnInit {

  username = ""
  password = ""
  message = ""

  constructor(private router: Router, private _auth: AuthService) {
  	this.router = router
  }

  ngOnInit() {
  }

  login(){
    this._auth.login(this.username, this.password)
      .subscribe(
          res => {
            this._auth.storeToken(res.key);
            this.router.navigate(['/main']);
          },
          err => {
            this.message = "Login was not successful."
          }
      );
  }

  guestLogin(){
  	this._auth.login("guest", "guest")
  }

  forgotPassword(){
  	this.message = "The forgot password feature is \
  		currently in development."
  }

}
