import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';


@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})


export class MainComponent implements OnInit {

  constructor(private router: Router) {
  	this.router = router
  }

  ngOnInit() {

  	// if(!this.isAuthenticated()){
  		// this.router.navigate(['/login']);
  	// }

  }

  isAuthenticated(){
  	return false;
  }

  summary(){
    this.router.navigate(['/main/summary']);
  }

}
