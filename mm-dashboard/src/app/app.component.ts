import { Component, Input, OnInit, ViewChild, ComponentFactoryResolver } from '@angular/core';

import { BodyComponentDirective } from './body-component.directive';
import { LoginComponent } from './login/login.component';
import { MainComponent } from './main/main.component';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent implements OnInit{
  title = 'MeasureMe';
  @ViewChild(BodyComponentDirective) bodyComponent: BodyComponentDirective;

  constructor(private componentFactoryResolver: ComponentFactoryResolver) { }

  ngOnInit() {
  	if(this.checkLoginStatus()){
	    this.loadComponent(MainComponent);
	}else{
		this.loadComponent(LoginComponent);
	}
  }

  checkLoginStatus() {
  	//TODO: authenticate user using django auth api
  	return false
  }

  loadComponent(loadingComponent) {

    let componentFactory = this.componentFactoryResolver.resolveComponentFactory(loadingComponent);

    let viewContainerRef = this.bodyComponent.viewContainerRef;
    viewContainerRef.clear();

    let componentRef = viewContainerRef.createComponent(componentFactory);

  }

}
