import { Component, Input } from '@angular/core';
import { LoginComponent } from './login/login.component';
import { MainComponent } from './main/main.component';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {
  title = 'MeasureMe';

  constructor() { }

  checkLoginStatus() {
  	//TODO: authenticate user using django auth api
  	return false
  }

}
