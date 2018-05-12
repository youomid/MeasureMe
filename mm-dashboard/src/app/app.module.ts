import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { MainComponent } from './main/main.component';
import { BodyComponentDirective } from './body-component.directive';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    MainComponent,
    BodyComponentDirective
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  entryComponents: [LoginComponent, MainComponent],
  bootstrap: [AppComponent]
})
export class AppModule { }
