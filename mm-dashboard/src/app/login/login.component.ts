import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import { AuthService } from './../auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private router: Router, private _auth: AuthService) {
    this.router = router
  }

  ngOnInit() {
    var authToken = this._auth.getToken();

    if(authToken){
      this._auth.validateToken(authToken)
        .subscribe(
            res => {
              this.router.navigate(['/main']);
            },
            err => {
              console.log('Token not valid');
            }
        );
    }
  }

}
