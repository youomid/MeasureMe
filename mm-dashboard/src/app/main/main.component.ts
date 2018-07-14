import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import { AuthService } from './../auth.service';


@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})


export class MainComponent implements OnInit {

  constructor(private router: Router, private _auth: AuthService) {
  	this.router = router
  }

  ngOnInit() {
    var authToken = this._auth.getToken();

  	if(authToken){
      this._auth.validateToken(authToken)
        .subscribe(
            res => {
              this.goToDashboard()
            },
            err => {
              this.router.navigate(['/login']);
            }
        );
    }else{
      this.router.navigate(['/login']);
    }

  }

  goToDashboard(){
    this.router.navigate(['/main/dashboard']);
  }

}
