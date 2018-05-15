import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { MainComponent } from './main/main.component';
import { LoginFormComponent } from './login-form/login-form.component';
import { LoginPageIntroComponent } from './login-page-intro/login-page-intro.component';
import { AppRoutingModule } from './/app-routing.module';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    MainComponent,
    LoginFormComponent,
    LoginPageIntroComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  entryComponents: [LoginComponent, MainComponent],
  bootstrap: [AppComponent]
})
export class AppModule { }
